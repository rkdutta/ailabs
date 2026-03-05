# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based ML and AI experimentation repository (ailabs) containing educational Jupyter notebooks, vector database materials, and local AI model deployment guides.

## Setup & Commands

```bash
# Create and activate virtual environment
python3 -m venv ailab
source ailab/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Install pre-commit hooks (strips Jupyter notebook metadata via nbstripout)
nbstripout --install
pre-commit install

# Launch Jupyter Lab
jupyter lab
```

There is no build system, test suite, or linter configured beyond pre-commit hooks.

## Architecture

- **ml/supervised/** — Jupyter notebooks for supervised learning (basics, training, decision trees, confusion matrices) with inline CSV datasets
- **ml/unsupervised/** — Notebooks for unsupervised learning (hierarchical clustering, logistic regression)
- **vector databases/** — Educational documentation on vector DB concepts; uses chromadb
- **claude/** — Instructions for running models locally via Ollama
- **adk/** — Google ADK integration setup
- **ailab/** — Python virtual environment (not checked in meaningfully)

## Key Dependencies

numpy, scipy, scikit-learn, pandas, matplotlib, jupyterlab, chromadb

## Pre-commit Hooks

nbstripout is configured to automatically strip Jupyter notebook output/metadata before commits, keeping diffs clean.
