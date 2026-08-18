# Python Open Source Template

A starter repository for Python packages with `uv`, Ruff, ty, pytest, Sphinx,
GitHub Actions, and agent-friendly project guidance.

## Start a Project

1. Use this template to create a repository.
2. Complete [TEMPLATE_SETUP.md](TEMPLATE_SETUP.md) before the first release.
3. Install development dependencies:

   ```sh
   make install
   ```

The template intentionally does not define a package, API, or application.
Choose those when adapting it.

## Development

```sh
make check   # Fast lint, format, and type checks
make verify  # Checks, tests, package build, and strict documentation build
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for contributor guidance and
[AGENTS.md](AGENTS.md) for agent instructions.

## Documentation and Releases

Documentation lives in `docs/` and is built with Sphinx using the Palewire
theme. The documentation workflow builds every push and pull request.

Follow [RELEASING.md](RELEASING.md) for the release checklist and
[CHANGELOG.md](CHANGELOG.md) for user-facing changes.
