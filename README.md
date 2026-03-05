## Description

This is playground for machine learning and ai experiments. 
Use your choice of editor like VSCODE for example to load the Jupyter notebook.

### Python virtual environment(optional)
```bash
python3 -m venv ailab
pip3 install -r requirements.txt
nbstripout --install
pre-commit install

```


# .claude/ Directory

Project-level configuration for Claude Code.

## Structure

```
.claude/
├── .mcp.json                    # MCP server configuration
├── settings.json                # Project-level tool permissions
├── memory/
│   └── MEMORY.md                # Persistent memory across sessions
├── rules/
│   ├── python.md                # Python coding rules (*.py files)
│   ├── notebooks.md             # Jupyter notebook rules (*.ipynb files)
│   └── git.md                   # Git workflow rules
├── agents/
│   ├── data-explorer.md         # Analyzes datasets, suggests ML approaches
│   └── notebook-builder.md      # Creates structured educational notebooks
└── commands/
    ├── setup.md                 # /setup — bootstrap dev environment
    ├── notebook.md              # /notebook <path> — explore a notebook
    ├── explain.md               # /explain <path> — explain ML concepts
    └── new-notebook.md          # /new-notebook <topic> — scaffold notebook
```

## Components

### settings.json

Project-level permissions that pre-approve safe, read-only commands (git status, git diff, python3, ls, etc.) so you don't get prompted every time.

### rules/

Auto-applied contextual rules based on file globs:

- **python.md** — Triggers on `*.py` files. Enforces Python 3.10+ features, numpy vectorized ops, scikit-learn conventions.
- **notebooks.md** — Triggers on `*.ipynb` files. Enforces notebook structure (title cell, grouped imports, markdown sections, short cells).
- **git.md** — Triggers on all files. Enforces conventional commit prefixes, no credentials in commits, no skipping pre-commit hooks.

### agents/

Specialized sub-agents that run on Sonnet for cost efficiency:

- **data-explorer** (green) — Exploratory data analysis, statistical summaries, visualizations, and ML model recommendations.
- **notebook-builder** (blue) — Creates well-structured educational Jupyter notebooks following repo conventions.

Note: The global `code-improver` agent at `~/.claude/agents/` is also available across all projects.

### commands/

Custom slash commands for common workflows:

- **/setup** — Bootstraps the full dev environment (venv, pip install, pre-commit hooks).
- **/notebook `<path>`** — Reads and summarizes a Jupyter notebook, then asks what you want to change.
- **/explain `<path>`** — Breaks down ML/AI concepts or code step by step.
- **/new-notebook `<topic>`** — Scaffolds a new Jupyter notebook with proper structure in the correct directory.

### memory/

Persistent memory that Claude builds on across sessions. `MEMORY.md` is loaded into every conversation's context. Additional topic files can be created and linked from `MEMORY.md` as knowledge grows.

### .mcp.json

MCP (Model Context Protocol) server configuration:

- **filesystem** — Scoped file access to this repository.
- **memory** — Persistent knowledge graph memory.

Additional servers (fetch, brave-search, github, etc.) can be added as needed.
