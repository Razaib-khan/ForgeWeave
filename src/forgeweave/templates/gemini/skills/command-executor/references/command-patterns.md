# Command Routing Patterns

## Pattern: Direct Mapping
`/forge-review` → `validation-engine` skill → run validation workflow

## Pattern: Pipeline Mapping
`/forge-research` → `deep-research` skill → planner → research agents → validator → synthesizer

## Pattern: Composite Mapping
`/forge-deploy` → `workflow-orchestrator` → [test-generator, code-builder, command-executor]

## Registry Format
```json
{
  "forge-<name>": {
    "skill": "<skill-id>",
    "pipeline": ["<skill-id>", ...],
    "subagents": ["<agent-id>", ...]
  }
}
```

## Invocation Rules
1. Executor never runs logic directly — it resolves the command
2. Resolution loads the skill's SKILL.md
3. SKILL.md defines the workflow
4. Executor follows the workflow, not its own logic
