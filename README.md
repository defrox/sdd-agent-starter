# Spec-Driven Development (SDD) Agent Starter

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Powered-1C3C3C?logo=langgraph&logoColor=white)](https://langchain-ai.github.io/langgraph/)

A deterministic **Spec-Driven Development (SDD)** agentic workflow built with **LangGraph**. Instead of relying on open-ended prompting, this blueprint enforces formal contracts (OpenAPI / JSON Schema) and automated static verification gates (`mypy`, `pytest`, schema validation) before any AI-generated code can reach a Pull Request.

## Architecture

```mermaid
flowchart LR
    A[OpenAPI / JSON Spec] --> B[Architect Agent]
    B --> C[Generated Code]
    C --> D{Sandbox Verifier}
    D -- Validation Failed --> B
    D -- Passed All Gates --> E[PR Ready Artifact]
```

## Key Features
* **Contract-First Generation:** Eliminates structural hallucinations by binding agent output to strict OpenAPI specifications.
* **Self-Healing Verification Loop:** Automatically feeds linter, type-check, and contract errors back into the agent state up to a bounded retry limit.
* **Provider Agnostic:** Pre-configured to route inference through LiteLLM or local vLLM endpoints.

## Quickstart

```bash
# 1. Install dependencies
pip install -e .

# 2. Run the SDD verification workflow
python -m src.graph
```

## Author
**Christian Axel Schmidt** — Principal AI & Systems Architect