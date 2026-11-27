# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Add project-neutral Context7 configuration, opt-in index refresh automation,
  and setup guidance for generated projects.

### Changed

### Fixed

### Removed

### Security

## [2.3.0] - 2026-11-16

### Added

- Check docstrings with Ruff's Google-style rules, require `Returns`, `Yields`
  and `Raises` sections where the code needs them, and run docstring examples
  as tests. `AGENTS.md` documents the convention ([#310]).

### Changed

- Rename the `_notebooks/` folder to `notebooks/`, the more common convention
  ([#300]).
- Update locked dependencies, including ty, Ruff, tornado and soupsieve, and
  move the Ruff pre-commit hook to match the locked version ([#301], [#302],
  [#306]).
- Bump the uv pin in the documentation and deployment workflows and align the
  CodeQL upload pins ([#307]).

### Fixed

- Rename five ty rules in `pyproject.toml` that newer ty versions renamed, so
  `make check` no longer fails with warnings ([#306]).

## [2.2.0] - 2026-11-05

### Added

- Add JupyterLab live collaboration with an AI assistant: the `notebooks`
  dependency group now includes `jupyter-collaboration`, `jupytext` and
  `vl-convert-python`, notebooks are paired with `.py` files, `make notebooks`
  launches JupyterLab with a generated token, and `AGENTS.md` documents the
  setup and notebook reproducibility practices ([#297]).

### Changed

- Update all locked dependencies and the Ruff pre-commit hook to their latest
  releases ([#298]).

### Fixed

- Include the Jupytext configuration in the source distribution so
  `make manifest-check` passes ([#298]).

### Removed

### Security

## [2.1.1] - 2026-08-25

### Added

### Changed

- Enable the Palewire Sphinx extension defaults in the template and document
  its `html_baseurl` configuration ([#278]).

### Fixed

### Removed

### Security

## [2.1.0] - 2026-08-23

### Added

- Add a development container for a consistent, ready-to-use environment
  ([#267]).
- Add repository quality checks, including manifest validation, dependency
  checks, workflow auditing, and OpenSSF Scorecard scanning ([#268], [#269],
  [#270]).
- Add an environment file template and an idempotent `make bootstrap` command
  that safely prepares primary checkouts and Git worktrees ([#271], [#273]).

### Changed

- Replace PyPI API tokens with trusted publishing and update GitHub Actions to
  supported versions, while skipping publication until a real package is
  configured ([#261], [#262]).
- Expand Ruff and ty checks, streamline pre-commit hooks, and improve the
  default pytest configuration ([#263], [#264], [#265], [#266]).
- Document the required checks and approvals for post-merge GitHub releases
  ([#272]).

### Fixed

### Removed

### Security

[Unreleased]: https://github.com/palewire/python-open-source-template/compare/2.3.0...HEAD
[2.3.0]: https://github.com/palewire/python-open-source-template/compare/2.2.0...2.3.0
[2.2.0]: https://github.com/palewire/python-open-source-template/compare/2.1.2...2.2.0
[2.1.1]: https://github.com/palewire/python-open-source-template/compare/2.1.0...2.1.1
[2.1.0]: https://github.com/palewire/python-open-source-template/compare/2.0.0...2.1.0
[#261]: https://github.com/palewire/python-open-source-template/pull/261
[#262]: https://github.com/palewire/python-open-source-template/pull/262
[#263]: https://github.com/palewire/python-open-source-template/pull/263
[#264]: https://github.com/palewire/python-open-source-template/pull/264
[#265]: https://github.com/palewire/python-open-source-template/pull/265
[#266]: https://github.com/palewire/python-open-source-template/pull/266
[#267]: https://github.com/palewire/python-open-source-template/pull/267
[#268]: https://github.com/palewire/python-open-source-template/pull/268
[#269]: https://github.com/palewire/python-open-source-template/pull/269
[#270]: https://github.com/palewire/python-open-source-template/pull/270
[#271]: https://github.com/palewire/python-open-source-template/pull/271
[#272]: https://github.com/palewire/python-open-source-template/pull/272
[#273]: https://github.com/palewire/python-open-source-template/pull/273
[#278]: https://github.com/palewire/python-open-source-template/pull/278
[#297]: https://github.com/palewire/python-open-source-template/pull/297
[#298]: https://github.com/palewire/python-open-source-template/pull/298
[#300]: https://github.com/palewire/python-open-source-template/pull/300
[#301]: https://github.com/palewire/python-open-source-template/pull/301
[#302]: https://github.com/palewire/python-open-source-template/pull/302
[#306]: https://github.com/palewire/python-open-source-template/pull/306
[#307]: https://github.com/palewire/python-open-source-template/pull/307
[#310]: https://github.com/palewire/python-open-source-template/pull/310
