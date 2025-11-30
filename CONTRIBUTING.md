# Contributing

Thanks for contributing! A few guidelines:

- Run the test suite before opening a PR: `cd backend && python -m pytest tests`.
- Follow the existing code style. This repo uses `ruff` for linting and `mypy` for optional typing checks in CI.
- Add unit tests for any new behavior under `backend/tests/`.
- For database schema changes, update the SQL files under `database/` and add a migration in `database/migrations/`.

To propose changes, open a GitHub pull request against `main`. The CI workflow will run linting and tests.
