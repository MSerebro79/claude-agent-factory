# Pattern: Workflow Agent

## Description

Orchestrates a multi-step business process by calling other agents or services in sequence or in parallel. Acts as a coordinator, not an executor.

## Core Loop

1. Receive a task with structured parameters.
2. Decompose into subtasks and assign to sub-agents or tools.
3. Collect results; handle partial failures.
4. Aggregate outputs and return a final result.
5. Log run metadata (duration, costs, errors) to the project index.

## Recommended Tools

- Claude API with tool_use for sub-agent dispatch
- n8n for orchestration nodes
- Structured output (JSON mode) for reliable parsing between steps

## Typical Cost

~2 000–20 000 tokens per run depending on number of subtasks. Budget per sub-agent call separately.

## Known Risks

- Cascading failures — each subtask must have an explicit error path.
- Context overflow — pass only necessary context to sub-agents.
- Cost explosion — set per-run token caps and alert on breach.
