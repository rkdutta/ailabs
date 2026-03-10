```bash
uv init
source .venv/bin/activate 
uv add fastmcp

# opens mcp inspector [dev mode]
uv run fastmcp dev inspector ./main.py

# server mode
uv run fastmcp run ./main.py 
```


```bash
# installing the server with claude
uv run fastmcp install claude-desktop main.py
```

Next open claude desktop and execute this query
```
add 1000 + 99
```

## Troubleshoot

1. Setting > Developer > Demo Server (should be in running state)
2. Chat > Connectors > Demo Server (should be enabled for use)
3. Inspect using inspector
```bash
uv run fastmcp install claude-desktop main.py
```
