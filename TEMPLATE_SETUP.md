# Instantiating This Template

Complete this checklist before the first release.

## Package

- [ ] Replace placeholder metadata in `pyproject.toml`.
- [ ] Create `src/<package_name>/` and enable setuptools package discovery.
- [ ] Set coverage source, ty include path, and the Click entry point if needed.
- [ ] Add `py.typed` when the package exposes typed public APIs.

## Documentation

- [ ] Replace the distribution placeholder and production URLs in `docs/conf.py`.
- [ ] Add an autosummary-based API reference for public modules.
- [ ] Configure S3 deployment through the protected `docs-production`
      environment, AWS OIDC variables, and `DOCS_DEPLOY_ENABLED=true`.

## Continuous Integration

- [ ] Set the `PACKAGE_IMPORT_NAME` repository variable to the package import
      name. This enables wheel-import and coverage checks in CI.
- [ ] Configure required checks and review rules for the default branch.

## Release

- [ ] Review `RELEASING.md` and verify the PyPI publication configuration.
- [ ] Confirm `CHANGELOG.md` and issue/PR templates match the project workflow.
