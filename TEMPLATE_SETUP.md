# Instantiating This Template

Complete this checklist before the first release.

## Package

- [ ] Replace placeholder metadata in `pyproject.toml`.
- [ ] Create `src/<package_name>/` and enable setuptools package discovery.
- [ ] Set coverage source, ty include path, and the Click entry point if needed.
- [ ] Add `py.typed` when the package exposes typed public APIs.

## Documentation

- [ ] Replace the distribution placeholder and set `html_baseurl` to the
      production documentation URL in `docs/conf.py`. The `palewire` extension
      derives the canonical theme URL from it and provides the `wide` layout and
      `sidebar` navigation presets, which you can adjust for the project.
- [ ] Add an autosummary-based API reference for public modules.
- [ ] Configure S3 deployment through the protected `docs-production`
      environment, AWS OIDC variables, and `DOCS_DEPLOY_ENABLED=true`.

## Context7

The root `context7.json` uses the current schema, indexes `docs/` and the
root-level README, and excludes the template's operational files. It omits
project metadata, branch names, versions, and usage rules so Context7 can infer
safe defaults without template-specific placeholders. Adjust its paths if the
project's user documentation lives elsewhere.

- [ ] Publish useful documentation, then [submit the public repository to
      Context7](https://context7.com/add-library).
- [ ] Claim ownership from the library's Context7 admin page. Add the generated
      `url` and `public_key` values to `context7.json`, push them to the default
      branch, and complete the claim.
- [ ] After claiming, use **Apply for Verification** on the admin page and
      provide the requested project and documentation details if the automatic
      quality check does not approve it.
- [ ] Rely on Context7's usage-based automatic refreshes, refresh manually after
      important releases, or enable `.github/workflows/context7-refresh.yml` by
      setting a `CONTEXT7_API_KEY` repository secret and the
      `CONTEXT7_REFRESH_ENABLED=true` repository variable.

## Continuous Integration

- [ ] Set the `PACKAGE_IMPORT_NAME` repository variable to the package import
      name. This enables wheel-import and coverage checks in CI.
- [ ] Configure required checks and review rules for the default branch.

## Release

- [ ] Review `RELEASING.md` and verify the PyPI publication configuration.
- [ ] Confirm `CHANGELOG.md` and issue/PR templates match the project workflow.
