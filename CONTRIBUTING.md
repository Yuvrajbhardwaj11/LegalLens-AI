# Contributing to LegalLens AI

Thanks for your interest in contributing.

## Development Setup

See [README.md](README.md#getting-started) for full setup instructions.

## Workflow

1. Fork the repo and create a branch off `main`: `feature/your-feature-name`
2. Make your changes, with tests where applicable
3. Run the test suite locally:
   ```bash
   cd backend && pytest
   cd frontend && npm run build
   ```
4. Open a pull request describing what changed and why

## Code Style

- **Backend:** Python, type-hinted where practical, `black`-formatted
- **Frontend:** TypeScript, functional React components, Tailwind for styling

## Reporting Issues

Please include:
- Steps to reproduce
- Expected vs. actual behavior
- Relevant logs / stack traces
