# agent.ollama.py
import os, subprocess
import ollama

# --- Ollama cloud client ---
API_KEY = os.environ["OLLAMA_API_KEY"]
client = ollama.Client(
    host="https://api.ollama.com",
    headers={"Authorization": f"Bearer {API_KEY}"},
)

MODEL = "glm-5:cloud"


# --- Tools ---

def read_file(filepath: str) -> str:
    """Read the contents of a file."""
    with open(filepath, "r") as f:
        return f.read()

def write_file(filepath: str, content: str) -> str:
    """Write content to a file."""
    with open(filepath, "w") as f:
        f.write(content)
    return f"Written to {filepath}"

def run_tests(command: str) -> str:
    """Run a shell command and return output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {"filepath": {"type": "string"}},
                "required": ["filepath"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["filepath", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_tests",
            "description": "Run a shell command and return its output.",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"],
            },
        },
    },
]

TOOL_MAP = {
    "read_file": read_file,
    "write_file": write_file,
    "run_tests": run_tests,
}

SYSTEM_PROMPT = """You are a senior Python engineer doing a thorough code review.

For every file you review:
1. Read the file using read_file
2. Identify bugs (crashes, edge cases, logic errors)
3. Flag security issues (eval, shell injection, open file handles)
4. Check for Python anti-patterns (mutable defaults, bare except)
5. Fix all issues using write_file
6. Run pytest using run_tests to verify fixes

Be specific — explain what each bug is and why your fix works."""


# --- Agent loop ---

def run_agent(prompt: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    print(f"Prompt: {prompt}\n{'=' * 50}")

    while True:
        response = client.chat(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
        )

        message = response.message
        messages.append(message)

        if not message.tool_calls:
            print("\nAgent response:")
            print(message.content)
            break

        for call in message.tool_calls:
            fn_name = call.function.name
            fn_args = call.function.arguments  # already a dict in ollama
            print(f"Tool called: {fn_name}({fn_args})")

            result = TOOL_MAP[fn_name](**fn_args)

            messages.append({
                "role": "tool",
                "content": result,
            })


if __name__ == "__main__":
    run_agent(
        "Review utils.py for all bugs and security issues. "
        "Fix every issue, then run pytest to confirm tests pass."
    )
