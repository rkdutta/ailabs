---
description: Git workflow rules
globs: "*"
---

- Use conventional commit prefixes: add, fix, update, refactor, docs, chore
- Never commit .env files, API keys, or credentials
- Pre-commit hooks (nbstripout) must pass — do not skip with --no-verify
- Keep commits focused on a single logical change
