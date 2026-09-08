# Contributing to FortSight AI

We welcome contributions from the community! Please read through these guidelines before submitting a pull request.

## How to Contribute

1. **Fork the Repository**
2. **Create a Feature Branch:** `git checkout -b feature/amazing-feature`
3. **Commit your Changes:** `git commit -m 'Add some amazing feature'`
4. **Push to the Branch:** `git push origin feature/amazing-feature`
5. **Open a Pull Request**

## Development Standards

### Code Style
- **Python:** Follow PEP-8. We use `flake8` and `black` for formatting.
- **TypeScript:** We use ESLint and Prettier.

### Testing
- Ensure that all new features are covered by tests.
- Run `pytest` for the backend and `vitest` for the frontend before opening a PR.
- Code coverage should not decrease.

### Commit Messages
Write clear, concise commit messages. Prefix your commits with the area of change (e.g., `feat(frontend): add map component`, `fix(backend): resolve visibility bug`).
