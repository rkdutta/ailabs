---
description: Rules for Jupyter notebooks
globs: "**/*.ipynb"
---

- Every notebook must start with a title markdown cell and an overview of what it covers
- Group imports in the first code cell
- Use markdown cells to separate logical sections and explain concepts before code
- Keep code cells short and focused — one concept per cell
- nbstripout is configured via pre-commit, so outputs are stripped before commits
- Use inline CSV/data generation rather than external data files when possible
- Include visualizations using matplotlib where they aid understanding
