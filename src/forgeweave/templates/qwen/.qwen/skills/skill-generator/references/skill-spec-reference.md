# SKILL.md Structure Reference

## Frontmatter (Required)
```yaml
skill_id: kebab-case-id
name: Title Case Name
version: 1.0.0
description: One sentence — what it does AND when to use it
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - tag1
  - tag2
```

## Body Sections (10 sections, in order)

| # | Section | Content |
|---|---|---|
| 1 | Purpose | 2-4 sentences. What problem? When to invoke? |
| 2 | When to Use | Numbered list of exact, testable trigger conditions |
| 3 | When Not to Use | Edge cases where skill looks relevant but shouldn't be used |
| 4 | Inputs | Table: name, type, required/optional, description |
| 5 | Expected Outputs | Table: output name, description, file path |
| 6 | Exact Workflow Steps | Ordered, atomic, verifiable steps |
| 7 | Required Checks | Pass/fail checklist after execution |
| 8 | Failure Modes | Table: failure condition, agent response |
| 9 | Examples | Complete worked example with inputs → outputs |
| 10 | References | Links to scripts, assets, external docs |

## Bundle Structure
```
my-skill/
  SKILL.md         # Entrypoint + metadata (required)
  scripts/         # Automation scripts (recommended)
  references/      # Knowledge base docs (recommended)
  templates/       # Scaffolding files (recommended)
  examples/        # Worked examples (recommended)
  evals/           # Validation tests (recommended)
```
