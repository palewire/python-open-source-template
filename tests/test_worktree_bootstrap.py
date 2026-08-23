"""Tests for the worktree development bootstrap."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import pytest

from scripts.worktree_bootstrap import (
    GitCheckout,
    bootstrap,
    ensure_shared_env,
    ensure_worktree_override,
    parse_primary_checkout,
    worktree_identifier,
)

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path


class FakeRunner:
    """Return fixed Git metadata and record command orchestration."""

    def __init__(self, current: Path, primary: Path) -> None:
        self.current = current
        self.primary = primary
        self.captured: list[tuple[tuple[str, ...], Path]] = []
        self.executed: list[tuple[tuple[str, ...], Path]] = []

    def capture(self, command: Sequence[str], cwd: Path) -> str:
        self.captured.append((tuple(command), cwd))
        if command == ("git", "rev-parse", "--show-toplevel"):
            return f"{self.current}\n"
        if command == ("git", "worktree", "list", "--porcelain"):
            return (
                f"worktree {self.primary}\n"
                "HEAD abc123\n"
                "branch refs/heads/main\n\n"
                f"worktree {self.current}\n"
                "HEAD def456\n"
                "branch refs/heads/feature\n"
            )
        msg = f"Unexpected command: {command}"
        raise AssertionError(msg)

    def execute(self, command: Sequence[str], cwd: Path) -> None:
        self.executed.append((tuple(command), cwd))


@pytest.mark.unit
def test_worktree_identifier_is_stable_and_environment_safe(tmp_path: Path) -> None:
    checkout = tmp_path / "My Feature@2"
    checkout.mkdir()

    first = worktree_identifier(checkout)
    second = worktree_identifier(checkout)

    assert first == second
    assert re.fullmatch(r"my-feature-2-[0-9a-f]{8}", first)
    assert first != worktree_identifier(tmp_path)


@pytest.mark.unit
def test_parse_primary_checkout_uses_first_porcelain_entry(tmp_path: Path) -> None:
    primary = tmp_path / "main checkout"
    linked = tmp_path / "linked checkout"
    output = (
        f"worktree {primary}\nHEAD abc\nbranch refs/heads/main\n\n"
        f"worktree {linked}\nHEAD def\nbranch refs/heads/feature\n"
    )

    assert parse_primary_checkout(output) == primary.resolve()


@pytest.mark.unit
def test_checkout_discovery_uses_git_metadata(tmp_path: Path) -> None:
    primary = tmp_path / "primary"
    current = tmp_path / "current"
    primary.mkdir()
    current.mkdir()
    runner = FakeRunner(current, primary)

    checkout = GitCheckout.discover(runner, current / "nested")

    assert checkout == GitCheckout(current.resolve(), primary.resolve())
    assert runner.captured == [
        (("git", "rev-parse", "--show-toplevel"), current / "nested"),
        (("git", "worktree", "list", "--porcelain"), current.resolve()),
    ]


@pytest.mark.unit
def test_shared_env_symlink_is_created_and_idempotent(tmp_path: Path) -> None:
    primary = tmp_path / "primary"
    current = tmp_path / "current"
    primary.mkdir()
    current.mkdir()
    source = primary / ".env"
    source.write_text("SECRET=not-printed\n", encoding="utf-8")
    checkout = GitCheckout(current, primary)

    ensure_shared_env(checkout)
    ensure_shared_env(checkout)

    destination = current / ".env"
    assert destination.is_symlink()
    assert destination.resolve() == source.resolve()


@pytest.mark.unit
def test_shared_env_refuses_to_replace_existing_file(tmp_path: Path) -> None:
    primary = tmp_path / "primary"
    current = tmp_path / "current"
    primary.mkdir()
    current.mkdir()
    (primary / ".env").write_text("PRIMARY=1\n", encoding="utf-8")
    destination = current / ".env"
    destination.write_text("LOCAL=1\n", encoding="utf-8")

    with pytest.raises(FileExistsError, match="Refusing to replace"):
        ensure_shared_env(GitCheckout(current, primary))

    assert destination.read_text(encoding="utf-8") == "LOCAL=1\n"


@pytest.mark.unit
def test_primary_checkout_does_not_replace_its_env(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("PRIMARY=1\n", encoding="utf-8")

    ensure_shared_env(GitCheckout(tmp_path, tmp_path))

    assert not env_file.is_symlink()
    assert env_file.read_text(encoding="utf-8") == "PRIMARY=1\n"


@pytest.mark.unit
def test_worktree_override_is_created_and_preserves_local_settings(
    tmp_path: Path,
) -> None:
    ensure_worktree_override(tmp_path, "feature-12345678")
    override = tmp_path / ".env.worktree"
    assert override.read_text(encoding="utf-8") == (
        "# Worktree-local overrides. Load this after .env when supported.\n"
        "WORKTREE_ID=feature-12345678\n"
    )

    override.write_text(
        "# Local setting\nPORT=8123\nWORKTREE_ID=old-00000000\n",
        encoding="utf-8",
    )
    ensure_worktree_override(tmp_path, "feature-12345678")

    assert override.read_text(encoding="utf-8") == (
        "# Local setting\nPORT=8123\nWORKTREE_ID=feature-12345678\n"
    )


@pytest.mark.unit
def test_bootstrap_orchestrates_files_and_locked_sync(tmp_path: Path) -> None:
    primary = tmp_path / "primary"
    current = tmp_path / "feature"
    primary.mkdir()
    current.mkdir()
    (primary / ".env").write_text("SHARED=1\n", encoding="utf-8")
    runner = FakeRunner(current, primary)

    checkout = bootstrap(current, "custom-uv", runner)

    assert checkout == GitCheckout(current.resolve(), primary.resolve())
    assert (current / ".env").resolve() == (primary / ".env").resolve()
    assert (
        (current / ".env.worktree")
        .read_text(encoding="utf-8")
        .startswith("# Worktree-local overrides.")
    )
    assert runner.executed == [
        (
            ("custom-uv", "sync", "--all-groups", "--locked"),
            current.resolve(),
        )
    ]
