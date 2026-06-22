---
skill_id: skill-authoring
name: Skill Authoring
version: 1.0.0
description: Create or revise a ForgeWeave skill — from identifying the repeatable job to writing the bundle and validating it with eval checks.
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - meta
  - authoring
  - workflow
---

# Skill Authoring

## Purpose

A ForgeWeave skill is a **versioned workflow bundle**, not a single prompt file. This skill guides an agent through the process of identifying, designing, writing, and validating a new skill for the ForgeWeave framework. It exists to ensure every skill in the project meets the same quality bar: repeatable workflows become skills, deterministic steps become scripts, and uncertain outcomes are covered by eval checks.

When an agent is asked to "create a skill" or "write a SKILL.md", this skill provides the canonical process — from scoping the job, through structuring the bundle, to proving the skill works with an eval.

## When to Use

- The agent is asked to create a new ForgeWeave skill.
- An existing skill needs revision, expansion, or restructuring.
- A contributor asks for guidance on the skill format.
- A review finds that a skill is missing sections, scripts, or evals.
- The agent needs to convert an ad-hoc workflow into a repeatable skill.

## When Not to Use

- The work is a one-time task that will never be repeated — a skill is for repeatable jobs.
- The work is pure code that does not involve agent judgment — use a regular script or module instead.
- The work requires modifying the skill specification itself (`SKILL_SPEC.md`); that should be handled as a specification change, not a skill invocation.
- The agent is being asked to *execute* a skill, not *create* one — use the skill's own triggers instead.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `domain` | string | Yes | The repeatable job the skill should cover (e.g., "adapter implementation", "release verification") |
| `use_cases` | array of string | Yes | 2-3 concrete situations where this skill applies |
| `existing_steps` | string | No | Any existing workflow notes, prompts, or scripts the skill should be based on |
| `tui_targets` | array of enum | No (default: all four) | Which TUIs the skill should target: opencode, claude, gemini, qwen |

## Expected Outputs

| Output | Description |
|---|---|
| `SKILL.md` | Complete skill manifest and workflow, following the 10-section order |
| `scripts/` directory | Deterministic automation that the skill may invoke |
| `references/` directory | Supporting docs, specs, examples, or decision notes |
| `evals/` directory | Lightweight end-to-end tests that validate the skill still works |

The bundle is written to `templates/<tui>/skills/<skill-name>/`.

## Exact Workflow Steps

### Step 1: Scope the skill to one repeatable job

1. Identify the single, concrete, repeatable job this skill will cover.
2. If the job has more than 2–3 use cases, split it into multiple skills.
3. Write a one-sentence description that front-loads the use case and trigger words.
4. Confirm the skill passes the test: "Would I reach for this the next time I do this exact job?"

### Step 2: Choose the bundle structure

Create the directory layout:

```
<skill-name>/
  SKILL.md
  scripts/
  references/
  assets/
  evals/
```

Remove any directory the skill does not need. Every skill must have at least `SKILL.md`; `scripts/` and `evals/` are strongly recommended for any skill that invokes code or has pass/fail criteria.

### Step 3: Write the SKILL.md frontmatter

Populate:

```yaml
skill_id: <kebab-case-id>
name: <Title Case Name>
version: 1.0.0
description: <One sentence — what it does AND when to use it>
author: <GitHub username or "ForgeWeave Core">
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - <tag>
  - <tag>
```

The `description` is the routing signal. Agents match skills against tasks using this field. Front-load the trigger words so implicit matching works.

### Step 4: Write the SKILL.md body (10 sections, in order)

| # | Section | What to include |
|---|---|---|
| 1 | **Purpose** | 2–4 sentences. What problem does this skill solve? When should an agent invoke it? What is out of scope? |
| 2 | **When to Use** | Numbered list of exact, testable conditions that trigger this skill. |
| 3 | **When Not to Use** | Edge cases where the skill looks relevant but should not be invoked. |
| 4 | **Inputs** | Table: name, type, required/optional, description. Every input the skill expects. |
| 5 | **Expected Outputs** | What the skill produces — files, console output, side effects. Be explicit about file paths. |
| 6 | **Exact Workflow Steps** | Ordered, atomic, verifiable steps. No "try this or that" branching without documented decision rules. |
| 7 | **Required Checks** | Pass/fail checks that must be run after execution to confirm the skill succeeded. |
| 8 | **Failure Modes** | Table: failure condition, agent response, error message. Every possible failure mode. |
| 9 | **Examples** | At least one complete worked example showing inputs → expected outputs. |
| 10 | **References** | Links to scripts, assets, and external docs used by this skill. |

### Step 5: Write deterministic steps into scripts/

1. Identify every step in the workflow that does not require agent judgment (verification, formatting, copy operations, parsing).
2. Move those steps into standalone scripts under `scripts/`.
3. The SKILL.md references each script by relative path.

### Step 6: Write the evaluation layer into evals/

1. Create one eval per major workflow path (happy path, each failure mode).
2. Each eval is a lightweight end-to-end test: define a minimal input, run the skill (or a simulation), capture output, run checks.
3. Store checks as simple assertions in `evals/`.

### Step 7: Validate the skill bundle

1. Confirm `skill_id` matches the directory name.
2. Confirm all frontmatter fields are present.
3. Confirm all 10 body sections are present and in order.
4. Confirm all referenced scripts exist under `scripts/`.
5. Confirm all referenced assets exist under `assets/`.
6. Run each eval and confirm it passes.

## Required Checks

- [ ] `skill_id` matches the parent directory name.
- [ ] All required frontmatter fields are present and valid (`skill_id`, `name`, `version`, `description`, `author`, `tui_compatibility`).
- [ ] All 10 body sections are present and in the correct order.
- [ ] Every script referenced in the SKILL.md exists in `scripts/`.
- [ ] Every asset referenced exists in `assets/`.
- [ ] The `description` field front-loads the use case and is less than 200 characters.
- [ ] At least one eval exists in `evals/` for the primary workflow path.
- [ ] The skill does not contain placeholder text (`<...>` patterns) unless documented as intentional.
- [ ] The skill passes manual validation against SKILL_SPEC.md.

## Failure Modes

| Failure Condition | Response |
|---|---|
| `domain` is too broad (covers >3 use cases) | Stop. Report: "Skill domain is too broad. Narrow to one repeatable job with at most 2–3 use cases." |
| Frontmatter validation fails | Stop. Report: "Frontmatter missing required field(s): <fields>. See SKILL_SPEC.md for the full schema." |
| Section order is incorrect | Stop. Report: "SKILL.md sections are out of order. Expected: Purpose, When to Use, When Not to Use, Inputs, Expected Outputs, Exact Workflow Steps, Required Checks, Failure Modes, Examples, References." |
| Referenced script does not exist | Stop. Report: "Script '<path>' referenced in SKILL.md but not found under scripts/." |
| Eval check fails | Stop. Report: "Eval '<name>' failed: <details>. Fix the skill or update the eval before proceeding." |
| Manual validation finds violations | Stop. Report: "Validation failed: <errors>. Fix all validation errors before submitting." |

## Examples

### Example 1: Creating a new skill from scratch

**Input:**
```json
{
  "domain": "adapter implementation",
  "use_cases": [
    "Implementing a new TUI adapter from the ADAPTER_SPEC.md interface",
    "Updating an existing adapter when the target TUI changes its config format",
    "Adding template files for a new adapter under templates/<tui>/"
  ],
  "tui_targets": ["opencode"]
}
```

**Expected output:**
```
templates/opencode/skills/adapter-implementation/
  SKILL.md
  scripts/
    validate_adapter.py
    scaffold_adapter.py
  references/
    ADAPTER_SPEC.md
  evals/
    test_happy_path.json
    test_missing_methods.json
```

### Example 2: Revising an existing skill

**Input:**
```json
{
  "domain": "template sync",
  "use_cases": [
    "Adding a new section to the skill template across all TUIs",
    "Updating the SKILL.md format in an existing skill bundle"
  ],
  "existing_steps": "Current workflow: manually edit each SKILL.md, validate against spec"
}
```

**Expected output:** The revised `templates/opencode/skills/template-sync/SKILL.md` with a new section, plus updated evals that validate the new format.

## References

| Reference | Path |
|---|---|
| Skill Specification Standard | `../../../SKILL_SPEC.md` |
| Agent Specification Standard | `../../../AGENT_SPEC.md` |
| Project Context | `../../../PROJECT_CONTEXT.md` |
| Skill eval template | `./assets/eval-template.json` |
