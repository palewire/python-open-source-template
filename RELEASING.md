# Releasing

This project follows [Semantic Versioning](https://semver.org/) and [Keep a
Changelog](https://keepachangelog.com/en/1.1.0/). Package versions come from
Git tags through `setuptools-scm`; do not edit a version file.

## Release Checklist

- [ ] Replace all template metadata and configure the package layout described
      in `AGENTS.md`.
- [ ] Document public package behavior in the Sphinx source under `docs/`.
- [ ] Run `make docs-check`.
- [ ] Run `make verify`.
- [ ] Run `make package-check PACKAGE=<import-name>`.
- [ ] Run `make coverage PACKAGE=<import-name>`.
- [ ] Review `CHANGELOG.md` and move relevant `Unreleased` entries into a
      dated version section.
- [ ] Choose a major, minor, or patch version according to Semantic Versioning.
- [ ] Obtain explicit human approval for the version and release.
- [ ] Create the matching Git tag and GitHub release.
- [ ] Confirm the release workflow published the expected package to PyPI.
- [ ] Confirm the documentation workflow deployed the matching Sphinx site.

## Documentation Deployment

Package documentation lives in this repository under `docs/`. The
`.github/workflows/docs.yaml` workflow builds the Sphinx site on every push and
pull request.

Before publishing documentation, protect the `docs-production` environment and
configure an AWS OIDC role with `DOCS_AWS_ROLE_ARN` and `DOCS_AWS_REGION`. Then
set the `DOCS_DEPLOY_ENABLED` repository variable to `true`. Keep deployment in
the same workflow so the published site always comes from the reviewed Sphinx
source in this repository.

## Agent Boundaries

Agents may update release documentation and run the checklist's validation
commands. They must not create tags, GitHub releases, documentation
deployments, or package publications without explicit human approval.
