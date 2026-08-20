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
- [ ] Merge the approved release PR.
- [ ] With explicit human approval, create or confirm the exact version tag on
      the release PR's merge commit to trigger package publication.
- [ ] Confirm the release workflow published the expected package to PyPI.
- [ ] Complete the post-merge GitHub Release follow-up below.
- [ ] Confirm the documentation workflow deployed the matching Sphinx site.

## Post-merge GitHub Release Follow-up

Do not create the GitHub Release until the release PR has merged, the exact
version tag exists, and the approved package publication has completed. The tag
must point to the expected merge commit. Creating a tag, publishing a package,
or creating a release still requires explicit human approval.

1. Record the release PR's merge commit and confirm the exact tag resolves to
   it:

   ```sh
   VERSION=2.0.1
   EXPECTED_COMMIT=<release-pr-merge-commit>
   git fetch origin --tags
   test "$(git rev-parse "${VERSION}^{commit}")" = "$EXPECTED_COMMIT"
   ```

2. Prepare concise release notes from the matching version section in
   `CHANGELOG.md`. After the package publication succeeds and with explicit
   human approval, create the GitHub Release from the existing tag:

   ```sh
   gh release create "$VERSION" \
     --verify-tag \
     --title "$VERSION" \
     --notes-file /path/to/release-notes.md
   ```

   The GitHub UI may be used instead, but select the existing tag and publish
   the release rather than creating a draft or prerelease.

3. Verify that the public release uses the expected tag and commit:

   ```sh
   test "$(gh release view "$VERSION" --json tagName --jq .tagName)" = "$VERSION"
   test "$(gh release view "$VERSION" --json isDraft,isPrerelease \
     --jq '(.isDraft == false and .isPrerelease == false)')" = "true"
   test "$(git rev-parse "${VERSION}^{commit}")" = "$EXPECTED_COMMIT"
   ```

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
