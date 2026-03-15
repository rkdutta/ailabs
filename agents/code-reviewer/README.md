## Description

This is a code reviewer agent. It fixes buggy code and validate against tests.

## Generate api key
any one of the provider
```bash
ollama: https://ollama.com/settings/keys
github: https://github.com/marketplace/models/azure-openai/gpt-5/playground
```

## set environment variables
```bash
export GITHUB_TOKEN="token"
export OLLAMA_API_KEY="token"
```

## run (any one provider)
```bash
agent.github.py
agent.ollama.py
```

## validation
```bash
pytest test_utils.py -v
```

## Roadmap: What to Learn Next
### Stage 1 — Strengthen the Core (next 2–3 demos)
1. Structured output + output parsing
Your current agent returns free text. Learn to force the LLM to return JSON so downstream code can reliably consume it. Use response_format: { type: "json_object" } or Pydantic models.

2. Memory
Your agent forgets everything between runs. Learn the two types:

In-context: summarize past turns before the context window fills up
Persistent: write/read from a file or vector DB (you already have chromadb in this repo — great fit)
3. Error handling in the loop
What happens when a tool call fails, returns garbage, or the model hallucinates a bad tool argument? Add retry logic and graceful fallbacks to your loop.

### Stage 2 — Agent Patterns (the Anthropic playbook)
Read this closely — you linked it in your notebook. Then build one demo per pattern:

Pattern	What it does	Demo idea
Prompt chaining	Break a task into sequential LLM calls	Write → review → rewrite
Routing	Classify input, send to the right sub-agent	Bug report → triager → fixer or docs writer
Parallelization	Run multiple agents concurrently, merge results	Review 3 files simultaneously
Evaluator-optimizer	One agent generates, another critiques in a loop	Essay drafter + quality evaluator
### Stage 3 — Multi-Agent Systems
Build an orchestrator + subagent architecture:

Orchestrator: receives the high-level goal, breaks it into subtasks, delegates
Subagents: specialists (one reads docs, one writes code, one runs tests)
This is where agents become genuinely powerful and also where failure modes multiply — good time to think about guardrails (input validation, max loop iterations, cost caps).

### Stage 4 — Production Concerns
Observability: log every tool call, token count, and latency
Evals: automated tests that score agent output quality (not just pass/fail)
Cost management: track spend per run, cache repeated calls
Human-in-the-loop: when should the agent pause and ask rather than act?
