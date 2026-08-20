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
`docs/conf.py`, set the Palewire theme canonical and base URLs, and add an API
reference page using autosummary for the package's public modules. Add
host-specific linkcheck exclusions only for documented, reproducibly unstable
URLs.

## Development Workflow

Install dependencies with:

```sh
make install
```

Use these commands while making changes:

```sh
make check   # Fast, non-mutating lint, format, and type checks
make verify  # Full local CI suite: checks, tests, build, and docs
make test-serial  # Debug tests without parallel workers
make test-parallel  # Use for a large, independent test suite
```

Use `make fix` or `make format` only when changes to source files are
intended. `make hooks` may also modify files.

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

Follow `RELEASING.md`, including the post-merge GitHub Release follow-up. Agents
may prepare release notes and validate a release, but must not create tags,
releases, documentation deployments, or package publications without explicit
human approval.

## Change Guidelines

- Keep production code, tests, package configuration, and documentation aligned.
- Add tests for new library behavior under `tests/`.
- Use the configured Ruff and ty checks; do not introduce duplicate tooling
  without a project need.
- Copy `.env.example` to `.env` for local environment configuration. Do not
  commit generated build output, virtual environments, `.env` files, or
  credentials.
