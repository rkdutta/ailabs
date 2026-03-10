```bash
uv init
source .venv/bin/activate 
uv add fastmcp

# server mode
uv run fastmcp run ./main.py 
```


```bash
# installing the server with claude
uv run fastmcp install claude-desktop main.py
```

Next open claude desktop and execute this query
```
I want to add a new expense of buying a horse of 1000 dollars
```

## Troubleshoot

1. Setting > Developer > Expense Tracker Server (should be in running state)
2. Chat > Connectors > Expense Tracker Server (should be enabled for use)
3. Inspect using inspector
```bash
uv run fastmcp install claude-desktop main.py
```
