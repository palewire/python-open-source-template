# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

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

[Unreleased]: https://github.com/palewire/python-open-source-template/compare/2.1.0...HEAD
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
