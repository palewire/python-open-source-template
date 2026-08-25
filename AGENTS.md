# Agent Guide

This repository is a template for an open-source Python package. It provides
tooling, documentation, tests, and release automation, but intentionally does
not define a library package or its behavior.

## Repository Structure

- `pyproject.toml`: Package metadata and tool configuration.
- `tests/`: Tests for the library once it is added.
- `docs/`: Sphinx documentation source.
- `.github/workflows/`: Continuous integration, documentation, and release workflows.
- `Makefile`: Common development and verification commands.

Choose the library's package name, location, public API, and implementation
when adapting this template. Update the placeholder metadata and tool settings
in `pyproject.toml` at the same time.

## Project Setup

Before the first release, replace all placeholder package metadata in
`pyproject.toml`: name, description, author, keywords, URLs, license, and
development-status classifier. Set the status to match the package's actual
release maturity.

Use a `src/<package_name>/` layout for a new library. Enable the commented
setuptools package-discovery configuration, then set the coverage source and ty
include path to that package. If the project provides a Click CLI, uncomment
and update the example in `[project.scripts]`.

Keep only publishable, user-facing optional features in
`[project.optional-dependencies]`. Development, test, documentation, and
notebook tools belong in `[dependency-groups]`.

Keep tests serial until the independent test suite is large enough for parallel
workers to reduce wall-clock time. At that point, change CI to use
`make test-parallel`; use `make test-serial` when debugging shared-state tests.
Complete `TEMPLATE_SETUP.md` before the first release. Set
`PACKAGE_IMPORT_NAME` to enable CI package import and coverage checks.

## Documentation

Document the package's public behavior in the Sphinx source under `docs/`.
Update it with every user-facing API or behavior change, and build it with
`make docs-check`. The same repository's documentation workflow builds the
site on pushes and pull requests, checks links weekly, and deploys only its
reviewed build artifact. To publish, protect the `docs-production` environment,
configure an AWS OIDC role with `DOCS_AWS_ROLE_ARN` and `DOCS_AWS_REGION`, and
set the `DOCS_DEPLOY_ENABLED` repository variable to `true`.

When instantiating the template, replace the distribution placeholder in
`docs/conf.py`, set `html_baseurl` to the production documentation URL, and
add an API reference page using autosummary for the package's public modules.
The `palewire` extension derives the canonical theme URL from `html_baseurl`
and provides the `wide` layout and `sidebar` navigation presets; adjust those
settings only when the project needs a different presentation. For a brand-new,
simpler documentation project, `uvx sphinx-palewire-theme init` is an optional
shortcut, not a replacement for this template's richer configuration. Add
host-specific linkcheck exclusions only for documented, reproducibly unstable
URLs.

## Development Workflow

Install dependencies with:

```sh
make bootstrap
```

The bootstrap uses Git metadata to identify the primary checkout. In a linked
worktree, it can share the primary checkout's ignored `.env` and creates an
ignored `.env.worktree` with a stable `WORKTREE_ID`. Applications must
explicitly load dotenv files; when they do, `.env.worktree` should load after
`.env`.

Use these commands while making changes:

```sh
make check   # Fast, non-mutating lint, format, and type checks
make verify  # Full local CI suite: checks, tests, build, and docs
make test-serial  # Debug tests without parallel workers
make test-parallel  # Use for a large, independent test suite
```

Use `make fix` or `make format` only when changes to source files are
intended. `make hooks` may also modify files.

## Worktrees and Parallel Agents

- Edit only the current checkout. Never modify the primary checkout or sibling
  worktrees.
- Avoid broad clean, reset, or delete operations. Do not stop services that may
  be shared with another checkout or agent.
- Coordinate ownership of conflict-prone files such as lockfiles, schemas,
  migrations, snapshots, and generated artifacts.
- Serialize or stack changes that update state which cannot be merged safely.
- Never hand-edit files declared as generated; use their generator.
- `pytest-xdist` runs tests in parallel, but it does not isolate external
  resources across worktrees. Give each worktree separate ports, databases,
  caches, containers, and similar resources when tests use them.

After adding a library package, verify its wheel can be installed and imported:

```sh
make package-check PACKAGE=your_package_name
make coverage PACKAGE=your_package_name
```

## Changelog

For user-facing behavior, compatibility, or security changes, add a concise
entry under the appropriate `Unreleased` category in `CHANGELOG.md`. Do not
add entries for internal-only changes. Maintainers move entries into versioned
release sections.

## Releases

Follow `RELEASING.md` for the full checklist. The routine order is: merge the
approved release PR, confirm the exact version tag resolves to its merge
commit, obtain explicit approval for the tag-triggered package publication,
then create a public GitHub Release from that existing tag with concise
changelog-based notes. Verify that the release is neither a draft nor a
prerelease and that its tag still resolves to the expected commit. Agents may
prepare release notes and validate a release, but must not create tags,
releases, documentation deployments, or package publications without explicit
human approval.

## Change Guidelines

- Keep production code, tests, package configuration, and documentation aligned.
- Add tests for new library behavior under `tests/`.
- Use the configured Ruff and ty checks; do not introduce duplicate tooling
  without a project need.
- Copy `.env.example` to `.env` or use `make bootstrap` in a linked worktree.
  Do not commit generated build output, virtual environments, `.env` files,
  `.env.worktree`, or credentials.
