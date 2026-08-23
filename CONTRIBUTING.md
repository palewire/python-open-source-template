# Contributing

Clone the repository. Move into the directory on your terminal.

Prepare the checkout and install dependencies for development.

```sh
make bootstrap
```

The command can be run in either the primary checkout or a linked worktree.
See the [README](README.md) for its environment-file behavior.

Install pre-commit to run a battery of automatic quick fixes against your work.

```sh
uv run pre-commit install
```

Run the fast, non-mutating checks.

```sh
make check
```

Run the complete local verification suite before opening a pull request.

```sh
make verify
```

Before releasing, customize the package metadata in `pyproject.toml` and follow
the [release checklist](RELEASING.md).

## Documentation

The repository includes a ready-to-serve documentation site managed by Python's [Sphinx](https://www.sphinx-doc.org/en/master/) framework.

The configuration is stored in the `docs` directory. The default settings in `docs/conf.py` include several common Sphinx extensions. The documentation is written in [Markdown](https://en.wikipedia.org/wiki/Markdown) files stored within the directory. If you plan to publish documentation, you should started by editing `docs/index.md` and go from there. You can learn more about the options to available in the [MyST](https://myst-parser.readthedocs.io/en/latest/intro.html) guide to writing Markdown in Sphinx.

To build the documentation as a bundle of HTML files, run the following command:

```zsh
make build-docs
```

You can launch a preview site with the following command:

```zsh
make serve-docs
```

The documentation site is automatically built by a [GitHub Actions workflow](https://github.com/palewire/python-open-source-template/blob/main/.github/workflows/docs.yaml) that runs on every push and pull request. It checks links weekly. Protect the `docs-production` environment, configure its AWS OIDC role, and set `DOCS_DEPLOY_ENABLED` to `true` to publish the reviewed artifact from the main branch.

## Releasing

Follow [RELEASING.md](RELEASING.md), including its post-merge GitHub Release
follow-up. The continuous deployment workflow publishes the package when the
exact version tag is pushed.
