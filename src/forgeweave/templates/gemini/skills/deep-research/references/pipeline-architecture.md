# Deep Research Pipeline Architecture

```
User Query
    │
    ▼
┌──────────────┐
│  Planner     │  → research/<topic>-plan.md
│  (1 agent)   │
└──────┬───────┘
       │ subtopics [3-7]
       ▼
┌─────────────────────────────────────┐
│  Research Agents (parallel × N)     │
│  ┌──────────┐ ┌──────────┐ ┌──────┐ │
│  │ Agent #1 │ │ Agent #2 │ │  …  │ │ → research/<topic>-raw/*.md
│  └──────────┘ └──────────┘ └──────┘ │
└──────────────────┬──────────────────┘
                   │ raw outputs
                   ▼
┌──────────────────┐
│  Validator       │  → research/<topic>-validated.md
│  (1 agent)       │  Removes: unsupported claims, duplicates, contradictions
└──────────────────┘
                   │ validated content
                   ▼
┌──────────────────┐
│  Synthesizer     │  → research/<topic>-report.md
│  (1 agent)       │  Merges into structured final report
└──────────────────┘
                   │ final report
                   ▼
┌──────────────────┐
│  Output Writer   │  → Summary for user
│  (1 agent)       │
└──────────────────┘
```

## Key Design Decisions

1. **Isolation**: Each agent has ONE job. No agent does another agent's work.
2. **Parallelism**: Research agents run concurrently. Planner, validator, synthesizer run sequentially.
3. **Validation is mandatory**: Never skip the validator. Without it, the pipeline produces hallucinations.
4. **No source = no claim**: The validator enforces this strictly.
