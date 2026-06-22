# Skill Anatomy — Complete Structure & Format Reference

---

## SKILL.md Frontmatter Spec

Every skill starts with YAML frontmatter. Only `name` and `description` are required.

```yaml
---
name: my-skill-name          # Required. Lowercase, hyphens, max 64 chars. No "anthropic" or "claude".
description: |               # Required. The primary triggering mechanism. See Description Engineering below.
  What it does. When to use it.
  Name trigger phrases explicitly.
license: MIT                 # Optional. Include if distributing publicly.
compatibility: |             # Optional. Environment requirements.
  Requires Python 3.9+, Claude Code, bash_tool.
metadata:                    # Optional. Free-form key-value.
  author: Your Name
  version: 1.0.0
  mcp-server: your-service   # If skill layers on top of an MCP server.
---
```

**Name rules:** `my-skill` ✓ · `MySkill` ✗ · `claude-helper` ✗ (reserved prefix) · max 64 chars

**Description rules:**
- 1024 character limit (hard cap)
- No XML tags
- This is what Claude reads at startup to decide whether to trigger the skill
- Must contain: what it does, when to use it, specific trigger phrases
- "Pushy" is intentional — Claude has a strong default tendency to undertrigger

---

## Progressive Disclosure: The Three Levels

Anthropic's official framing. Load information only as needed.

```
Level 1: name + description (always in context, ~100 tokens)
              ↓ Claude decides skill is relevant
Level 2: SKILL.md body (loaded on trigger, aim for <500 lines)
              ↓ Claude reads a specific sub-case pointer
Level 3: references/ files (loaded on demand, unlimited)
              ↓ Claude runs a script without loading it
Level 4: scripts/ (executed without loading source into context)
```

This is why the context window cost of a skill is only ~100 tokens until it's needed. You can have 50 skills installed and pay almost nothing for the unused ones.

**When to move content to Level 3:**
- A section applies only to a specific sub-case (e.g., form-filling in a PDF skill)
- The content is reference-only (API docs, tool lists, code snippets)
- The SKILL.md body is approaching 400 lines
- Two sections are mutually exclusive (e.g., AWS guide vs GCP guide)

---

## File Layout Patterns

### Minimal Skill (single domain)
```
my-skill/
└── SKILL.md
```

### Standard Skill (with reference and scripts)
```
my-skill/
├── SKILL.md
├── references/
│   └── advanced.md
└── scripts/
    └── helper.py
```

### Domain-Variant Skill (multiple platforms/frameworks)
```
cloud-deploy/
├── SKILL.md          ← workflow + decision tree (which guide to read)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
Claude reads only the branch it needs. Don't merge them into one giant file.

### Full Skill with Evals
```
my-skill/
├── SKILL.md
├── references/
│   ├── guide-a.md
│   └── guide-b.md
├── scripts/
│   └── process.py
├── assets/
│   └── template.docx
└── evals/
    └── evals.json    ← excluded from .skill package on distribution
```

---

## SKILL.md Body Structure Patterns

### Procedural Skill (step-by-step workflow)
```markdown
# Skill Name

One-paragraph framing: what it is, what mental model to use.

## When to Use This Workflow
Short table or decision tree. "If X, do Y."

## Step-by-Step
1. **Step name** — Action. Why this matters.
2. **Step name** — Action.
   > Edge case: what to do if Z happens.

## Gotchas
Table of mistakes and fixes.

## Quick Reference
Code snippets, templates, lookup tables.
```

### Environmental Skill (wraps an environment's constraints)
```markdown
# Skill Name

Context: what environment this covers, what constraints exist.

## Required Patterns
Code snippets showing the correct way to do things.
Annotated with WHY this pattern is needed.

## Common Errors and Fixes
| Error | Cause | Fix |
|-------|-------|-----|

## Tool Quick Reference
| Task | Command | Notes |
|------|---------|-------|
```

### Router Skill (dispatches to sub-guides)
```markdown
# Skill Name

This skill covers X, Y, and Z scenarios. Read the relevant guide:
- `references/x.md` — when the user needs A, B, or C
- `references/y.md` — when the user mentions D or E
- `references/z.md` — for all other cases

## Decision Guide
Short table to help pick the right guide.
```

### MCP Enhancement Skill
```markdown
# Skill Name

This skill layers workflow guidance on top of the [ServiceName] MCP server.
The MCP gives you tools. This skill tells you how to use them well.

## Recommended Workflow
Named patterns for common tasks, using the MCP tools.

## What to Avoid
Anti-patterns specific to this MCP's behavior.
```

---

## How Context Window Works

At startup:
```
[System prompt] + [Skill 1: name + description] + [Skill 2: name + description] + ... + [User message]
```

On trigger (Claude reads the skill):
```
[System prompt] + [Skill descriptions] + [SKILL.md body] + [User message]
```

On deep trigger (Claude reads a reference file):
```
[System prompt] + [Skill descriptions] + [SKILL.md body] + [references/x.md] + [User message]
```

Key implication: the skill description adds ~100 tokens at all times. The SKILL.md body adds its full token count only when triggered. Reference files only when explicitly read.

**Token budget guidance:**
- Description: aim for 100-200 tokens (hard limit 1024 chars)
- SKILL.md body: aim for 500-2000 tokens (~300-1500 lines before bloat)
- Each reference file: no hard limit, but longer = more tokens when loaded
- Scripts: 0 tokens if executed without reading; full source if read as reference

---

## `references/` File Best Practices

- Each file should have a clear table of contents if over 300 lines
- Name files after what they cover, not when they're used: `forms.md` not `when-filling-forms.md`
- Reference them from SKILL.md with explicit triggers: "When the user needs to fill a form, read `references/forms.md` before proceeding"
- Make the trigger condition specific — Claude will skip optional reads if the case doesn't apply

---

## `scripts/` File Best Practices

Scripts are the most powerful component of a skill. They provide:
- **Determinism**: code is reliable; LLM generation is not
- **Token efficiency**: execute without loading source into context
- **Reusability**: every future invocation benefits immediately

Good candidates for scripting:
- File format conversion (PDF parsing, Excel manipulation)
- Validation and sanity-checking (zero formula errors, correct field values)
- Repetitive boilerplate (creating standard file structures)
- Operations too expensive or unreliable to do via generation (sorting, hashing)

In SKILL.md, reference scripts with: "Run `scripts/process.py input.pdf` to extract form fields. You do not need to read this script first."

---

## `.skill` Package Format

A `.skill` file is a ZIP archive of the skill folder, with `evals/` excluded.

To create:
```bash
cd /path/to/skills-directory
python package_skill.py my-skill/
# Creates my-skill.skill in the current directory
```

What gets included: `SKILL.md`, `references/`, `scripts/`, `assets/`, `LICENSE.txt`  
What gets excluded: `evals/`, `__pycache__/`, `node_modules/`, `*.pyc`, `.DS_Store`

The `.skill` file can be installed via claude.ai settings, Claude Code, or the Claude Agent SDK.