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
