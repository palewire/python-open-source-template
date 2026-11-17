"""Prepare a Git worktree for local development."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from collections.abc import Sequence

WORKTREE_ID_VARIABLE = "WORKTREE_ID"


class Runner(Protocol):
    """Run commands needed by the bootstrap."""

    def capture(self, command: Sequence[str], cwd: Path) -> str:
        """Run a command and return its standard output.

        Args:
            command: The program and its arguments.
            cwd: The directory to run the command in.

        Returns:
            The text the command printed to standard output.

        Examples:
            >>> runner.capture(("git", "status", "-sb"), Path("."))  # doctest: +SKIP
            'On branch main'
        """

    def execute(self, command: Sequence[str], cwd: Path) -> None:
        """Run a command with output attached to the terminal.

        Args:
            command: The program and its arguments.
            cwd: The directory to run the command in.

        Examples:
            >>> runner.execute(("uv", "sync"), Path("."))  # doctest: +SKIP
        """


class SubprocessRunner:
    """Run bootstrap commands in subprocesses."""

    def capture(self, command: Sequence[str], cwd: Path) -> str:
        """Run a command and return its standard output.

        Args:
            command: The program and its arguments.
            cwd: The directory to run the command in.

        Returns:
            The text the command printed to standard output.

        Examples:
            >>> SubprocessRunner().capture(("echo", "-n", "hi"), Path("."))
            'hi'
        """
        result = subprocess.run(  # noqa: S603 - Commands are never shell strings.
            command,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE,
            text=True,
        )
        return result.stdout

    def execute(self, command: Sequence[str], cwd: Path) -> None:
        """Run a command with output attached to the terminal.

        Args:
            command: The program and its arguments.
            cwd: The directory to run the command in.

        Examples:
            >>> SubprocessRunner().execute(("true",), Path("."))
        """
        subprocess.run(  # noqa: S603 - Commands are never shell strings.
            command,
            cwd=cwd,
            check=True,
        )


@dataclass(frozen=True)
class GitCheckout:
    """Paths Git reports for the current and primary checkouts."""

    current: Path
    primary: Path

    @classmethod
    def discover(cls, runner: Runner, cwd: Path) -> GitCheckout:
        """Discover checkout paths from Git metadata.

        Args:
            runner: Runs the Git commands.
            cwd: A directory inside the checkout.

        Returns:
            The current and primary checkout paths.

        Examples:
            >>> GitCheckout.discover(SubprocessRunner(), Path("."))  # doctest: +SKIP
            GitCheckout(current=PosixPath('/code/app'), primary=PosixPath('/code/app'))
        """
        current_output = runner.capture(
            ("git", "rev-parse", "--show-toplevel"),
            cwd,
        )
        current = Path(current_output.strip()).resolve()
        worktree_output = runner.capture(
            ("git", "worktree", "list", "--porcelain"),
            current,
        )
        primary = parse_primary_checkout(worktree_output)
        return cls(current=current, primary=primary)

    @property
    def is_linked_worktree(self) -> bool:
        """Report whether the current checkout is a linked worktree.

        Returns:
            True if the current checkout is not the primary checkout.

        Examples:
            >>> GitCheckout(
            ...     current=Path("/a-feature"), primary=Path("/a")
            ... ).is_linked_worktree
            True
        """
        return self.current != self.primary


def parse_primary_checkout(output: str) -> Path:
    """Find the primary checkout in Git's porcelain worktree listing.

    Args:
        output: The text printed by `git worktree list --porcelain`.

    Returns:
        The path of the first listed worktree, which is the primary checkout.

    Raises:
        ValueError: If the listing contains no worktree.

    Examples:
        >>> parse_primary_checkout("worktree /tmp/primary").name
        'primary'
    """
    for line in output.splitlines():
        if line.startswith("worktree "):
            return Path(line.removeprefix("worktree ")).resolve()
    msg = "Git did not report a primary checkout."
    raise ValueError(msg)


def worktree_identifier(checkout: Path) -> str:
    """Build a stable, environment-safe identifier for a checkout.

    Args:
        checkout: The path of the checkout.

    Returns:
        The lowercase folder name with a short hash of the full path.

    Examples:
        >>> worktree_identifier(Path("/tmp/My App")).startswith("my-app-")
        True
    """
    resolved = checkout.resolve()
    slug = re.sub(r"[^a-z0-9]+", "-", resolved.name.lower()).strip("-")
    safe_slug = slug or "worktree"
    path_hash = hashlib.sha256(os.fsencode(resolved)).hexdigest()[:8]
    return f"{safe_slug}-{path_hash}"


def ensure_shared_env(checkout: GitCheckout) -> None:
    """Link the primary .env into a linked worktree without overwriting files.

    Args:
        checkout: The current and primary checkout paths.

    Raises:
        FileExistsError: If the worktree already has a different `.env`.

    Examples:
        >>> ensure_shared_env(GitCheckout(current=Path("."), primary=Path(".")))
    """
    if not checkout.is_linked_worktree:
        return

    source = checkout.primary / ".env"
    destination = checkout.current / ".env"
    if not source.exists():
        return

    if destination.is_symlink() and destination.resolve() == source.resolve():
        return
    if destination.exists() or destination.is_symlink():
        msg = f"Refusing to replace existing {destination}."
        raise FileExistsError(msg)

    destination.symlink_to(source)


def ensure_worktree_override(checkout: Path, identifier: str) -> None:
    """Create or update the managed identifier while preserving local settings.

    Args:
        checkout: The checkout folder that holds `.env.worktree`.
        identifier: The value to store as the worktree identifier.

    Raises:
        ValueError: If the file assigns the identifier more than once.

    Examples:
        >>> import tempfile
        >>> with tempfile.TemporaryDirectory() as folder:
        ...     ensure_worktree_override(Path(folder), "demo-1234")
        ...     (Path(folder) / ".env.worktree").read_text().splitlines()[-1]
        'WORKTREE_ID=demo-1234'
    """
    override = checkout / ".env.worktree"
    assignment = f"{WORKTREE_ID_VARIABLE}={identifier}"
    if not override.exists():
        override.write_text(
            "# Worktree-local overrides. Load this after .env when supported.\n"
            f"{assignment}\n",
            encoding="utf-8",
        )
        return

    original = override.read_text(encoding="utf-8")
    lines = original.splitlines()
    matching_indexes = [
        index
        for index, line in enumerate(lines)
        if line.startswith(f"{WORKTREE_ID_VARIABLE}=")
    ]
    if len(matching_indexes) > 1:
        msg = f"{override} contains multiple {WORKTREE_ID_VARIABLE} assignments."
        raise ValueError(msg)
    if matching_indexes:
        index = matching_indexes[0]
        if lines[index] == assignment:
            return
        lines[index] = assignment
    else:
        if lines and lines[-1]:
            lines.append("")
        lines.append(assignment)

    override.write_text("\n".join(lines) + "\n", encoding="utf-8")


def bootstrap(cwd: Path, uv: str, runner: Runner) -> GitCheckout:
    """Prepare local environment files and install locked dependencies.

    Args:
        cwd: A directory inside the checkout.
        uv: The uv program to run.
        runner: Runs the Git and uv commands.

    Returns:
        The checkout that was prepared.

    Examples:
        >>> bootstrap(Path("."), "uv", SubprocessRunner())  # doctest: +SKIP
        GitCheckout(current=PosixPath('/code/app'), primary=PosixPath('/code/app'))
    """
    checkout = GitCheckout.discover(runner, cwd)
    ensure_shared_env(checkout)
    ensure_worktree_override(
        checkout.current,
        worktree_identifier(checkout.current),
    )
    runner.execute(
        (uv, "sync", "--all-groups", "--locked"),
        checkout.current,
    )
    return checkout


def main() -> None:
    """Run the worktree bootstrap from the command line.

    Examples:
        >>> main()  # doctest: +SKIP
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--uv", default=os.environ.get("UV", "uv"))
    args = parser.parse_args()

    checkout = bootstrap(Path.cwd(), args.uv, SubprocessRunner())
    location = "linked worktree" if checkout.is_linked_worktree else "primary checkout"
    print(f"Bootstrap complete for {location}.")


if __name__ == "__main__":
    main()
