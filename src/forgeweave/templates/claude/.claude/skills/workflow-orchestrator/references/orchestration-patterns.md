# Orchestration Patterns

## Sequential Pipeline
Steps run one after another. Each step can depend on the previous step's output.
```
A → B → C → D
```
Use: When each step needs results from the previous step.

## Parallel Fan-Out
One step spawns multiple independent branches.
```
    ┌→ B1 ─┐
A ──┼→ B2 ─┼→ D
    └→ B3 ─┘
```
Use: When multiple independent tasks can run simultaneously.

## Conditional Branching
Pipeline branches based on a condition.
```
    ┌→ B (if condition)
A ──┤
    └→ C (else)
```
Use: When different paths are needed based on intermediate results.

## Retry with Backoff
Failed steps are retried with increasing delays.
```
A → B → (fail) → wait 1s → B → (fail) → wait 2s → B
```
Use: When steps depend on unreliable external systems.
