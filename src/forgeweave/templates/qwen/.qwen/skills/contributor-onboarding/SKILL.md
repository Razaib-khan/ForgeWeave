---
skill_id: contributor-onboarding
name: Contributor Onboarding
version: 1.0.0
description: Guide a new contributor through the ForgeWeave repo — project structure, development setup, branch strategy, and how to pick and start an issue.
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - onboarding
  - contributing
  - community
---

# Contributor Onboarding

## Purpose

This skill exists to turn a newcomer into a productive contributor within a single session. It provides a guided walkthrough of the ForgeWeave repository — the specs, the CLI, the template structure, and the contribution process — so the contributor understands the project's architecture and can pick an issue, set up their environment, and make their first PR with confidence.

ForgeWeave is a behavioral execution framework for AI agents inside development environments. It is not a general-purpose tool. This skill ensures every contributor understands that core identity before they write code.

## When to Use

- A new contributor asks "where do I start?" or "how do I contribute?"
- A contributor has cloned the repo but hasn't set up their environment.
- A contributor needs help picking their first issue.
- During a PR review, a contributor's changes indicate they don't understand the project's deterministic-first philosophy.

## When Not to Use

- The contributor has already made multiple PRs and understands the workflow — they need task-specific help, not onboarding.
- The question is about a specific technical issue (Python dependency conflict, an adapter bug) — route to the relevant skill or discussion.
- The contributor is asking about something outside ForgeWeave (general Python questions, third-party TUI issues) — route to external resources.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `contributor_level` | enum: `beginner`, `intermediate`, `advanced` | Yes | How familiar the contributor is with Python CLI tools and agent frameworks |
| `interest_area` | enum: `core`, `adapters`, `skills`, `agents`, `docs`, `templates`, `ci` | Yes | Which part of the project the contributor wants to work on |
| `has_setup_env` | boolean | No (default: false) | Whether the contributor has already run the development setup |

## Expected Outputs

| Output | Description |
|---|---|
| Project map | A list of the key files and directories the contributor needs to understand for their interest area |
| Environment check | Report of what's set up and what's missing |
| Issue suggestions | 1-3 open issues matching their interest area, with links and difficulty labels |
| Next-step instructions | The exact commands and files they should look at next |

## Exact Workflow Steps

### Step 1: Assess contributor level and interest

1. Read the `contributor_level` and `interest_area` inputs.
2. If `has_setup_env` is false, proceed to Step 2. Otherwise, skip to Step 3.

### Step 2: Guide environment setup

1. Confirm the contributor has Python 3.14+ installed (`python --version`).
2. Guide them to fork the repo, clone it, and add the upstream remote.
3. Walk them through creating a virtual environment and activating it.
4. Run `python -m pip install -e ".[dev]"` to install with dev dependencies.
5. Run `forge doctor` to confirm the environment is ready.

### Step 3: Map the project for their interest area

1. Read the content of `CONTRIBUTING.md` (project structure section).
2. Read the relevant spec file based on their interest:

   | Interest | Spec to read |
   |---|---|
   | `skills` | `SKILL_SPEC.md` |
   | `agents` | `AGENT_SPEC.md` |
   | `adapters` | `ADAPTER_SPEC.md` |
   | `core` / `cli` | `PROJECT_CONTEXT.md` |
   | `docs` / `templates` / `ci` | `CONTRIBUTING.md` |

3. Present the contributor with a 3-5 sentence summary of the relevant subsystem and its key files.
4. Point them to the `skill-authoring` skill if they need to create a new skill.

### Step 4: Find matching issues

1. List open issues in `https://github.com/Razaib-khan/forgeweave/issues` filtered by the `interest_area` label.
2. Select 1-3 that match their level:
   - `beginner` → issues labeled `good-first-issue` or `docs`
   - `intermediate` → issues labeled `help-wanted` or `enhancement`
   - `advanced` → issues labeled `proposal` or `new-adapter`
3. For each suggestion, note:
   - The issue title and number
   - The area it touches
   - Whether it requires discussion before a PR

### Step 5: Explain the contribution workflow

1. Branch strategy: branch from `dev`, name branches `feature/<name>` or `fix/<number>-<desc>`.
2. Commit style: Conventional Commits (`feat:`, `fix:`, `docs:`, etc.).
3. PR target: always `dev`, never `main`.
4. PR requirements: tests (80%+ coverage), docs, changelog entry, pre-commit passing.

### Step 6: Summarize and set next steps

1. Print a clear, concise summary with:
   - What they learned about the project
   - What's still needed for their setup (if anything)
   - The issue(s) they should look at
   - The exact next command or file to open

## Required Checks

- [ ] The contributor understands that ForgeWeave is a behavioral execution framework, not a general-purpose tool.
- [ ] The contributor has forked the repo and set up their local environment.
- [ ] `forge doctor` passes all checks.
- [ ] The contributor has a clear next action (an issue to work on or a file to read).
- [ ] The contributor knows not to push directly to `main` and to target `dev` for PRs.

## Failure Modes

| Failure Condition | Response |
|---|---|
| Python version is below 3.14 | Stop. Report: "ForgeWeave requires Python >= 3.14. Current version: <version>. Please upgrade before proceeding." |
| `forge doctor` shows failures | Stop. Report: "Environment check failed: <details>. Run `forge doctor` to see details and fix the issues." |
| No matching issues found for interest area | Report: "No open issues found for '<area>'. Suggest checking Discussions for feature proposals or working on documentation improvements." |
| Contributor cannot find the spec files | Report: "Spec files are in the project root: SKILL_SPEC.md, AGENT_SPEC.md, ADAPTER_SPEC.md, PROJECT_CONTEXT.md." |
| Contributor asks about an unsupported interest area | Report: "ForgeWeave currently supports: core, adapters, skills, agents, docs, templates, and CI. Choose one of these areas." |

## Examples

### Example 1: Beginner interested in documentation

**Input:**
```json
{
  "contributor_level": "beginner",
  "interest_area": "docs",
  "has_setup_env": false
}
```

**Expected output summary:**
```
Project: ForgeWeave — behavioral execution framework for AI agents
Status: v2.0.0 stable (scaffolding CLI with 4 TUI adapters)

Your area: Documentation
Key files: README.md, CONTRIBUTING.md, SKILL_SPEC.md, AGENT_SPEC.md

Next steps:
1. Fork and clone the repo
2. Run: python -m venv .venv
3. Run: python -m pip install -e ".[dev]"
4. Run: forge doctor
5. Look at issues labeled "docs" and "good-first-issue"
6. Branch from dev, target dev for PRs
```

## References

| Reference | Path |
|---|---|
| Contributor Guide | `../../../CONTRIBUTING.md` |
| Code of Conduct | `../../../CODE_OF_CONDUCT.md` |
| Skill Authoring skill | `../skill-authoring/SKILL.md` |
| Project Context | `../../../PROJECT_CONTEXT.md` |
