---
description: Rules for Python files in this ML/AI repository
globs: "**/*.py"
---

- Use Python 3.10+ features (match statements, type unions with `|`, etc.)
- Prefer list comprehensions over map/filter for readability
- Use numpy vectorized operations over Python loops for numerical computation
- Always use `python3` and `pip3` (not `python` or `pip`)
- Use descriptive variable names — avoid single-letter names except for loop indices and standard math conventions (x, y, n)
- Follow scikit-learn conventions: X for features, y for labels
