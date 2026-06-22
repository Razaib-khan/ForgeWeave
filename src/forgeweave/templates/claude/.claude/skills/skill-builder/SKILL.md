---
name: skill-builder
description: |
  Complete guide for designing, writing, testing, iterating, and packaging Claude Skills (SKILL.md files). Use this skill whenever someone wants to: create a new skill from scratch, improve or update an existing skill, understand the skill format, write a SKILL.md, build a skill folder with scripts and references, evaluate whether a skill is well-written, package a skill for distribution, optimize a skill's trigger description, or understand best practices for Agent Skills. Triggers include phrases like "build a skill", "write a SKILL.md", "make a skill for", "improve this skill", "skill format", "create an agent skill", "how do I write a skill", or any request to teach Claude a domain-specific capability through the skills system.
---

# Claude Skill Builder

Skills are the primary way to give Claude persistent, domain-specific expertise. A skill is a folder containing a `SKILL.md` file plus optional scripts, references, and assets — all discoverable and loadable on demand without bloating context.

> **Deep dive references:**
> - `references/anatomy.md` — structure, file layout, frontmatter spec, progressive disclosure
> - `references/writing.md` — writing patterns, style guide, description engineering, pitfalls
> - `references/evals.md` — testing, grading, iteration loop, packaging

---

## The Mental Model: Onboarding Guide for an Expert Hire

Building a skill is like writing an onboarding guide for a new hire who is already highly capable but lacks your specific organizational knowledge. They don't need to be told what code is. They need to know: *your* naming conventions, *your* deployment dance, *which* script to run when, and *why* you do things a certain way.

The implication: **don't explain what Claude already knows**. Only encode knowledge Claude can't infer from its training — your procedures, your environment's quirks, your tools' gotchas, your output standards.

---

## Quick Decision: What Kind of Skill?

| Need | Skill Type |
|------|-----------|
| Teach a workflow with multiple steps | **Procedural** — numbered steps, decision tree |
| Wrap an environment's constraints (libraries, paths, formats) | **Environmental** — code snippets, gotcha table |
| Layer expert guidance on top of an MCP server | **MCP Enhancement** — workflow + tool guidance |
| Router that dispatches to other skills/files | **Router** — dispatch table, `references/` per domain |
| Style or quality standard | **Standard** — constraints, examples of good/bad |

Most skills combine types. Decide the primary type first; it governs the opening structure.

---

## The Core Loop

```
Identify gap → Draft SKILL.md → Test on 2-3 real prompts → Review outputs → 
Revise based on what Claude actually did wrong → Repeat → Package
```

This is not waterfall. The most common mistake is writing 500 lines before running a single test. **Start thin, iterate from real failures.**

### Step 1 — Capture Intent Before Writing

Answer these before touching a file:

1. What will Claude be able to do that it couldn't before?
2. What does the user say when they need this? (triggers)
3. What is the output format — a file, a code block, a decision, prose?
4. What does Claude do *wrong* without the skill? (This is your assertion list.)

If you can't answer all four, talk to the user more. The answers determine what goes in the skill.

### Step 2 — Write the SKILL.md

Start with the YAML frontmatter, then the body. See `references/anatomy.md` for the exact format.

**Frontmatter minimum:**
```yaml
---
name: my-skill           # lowercase, hyphens, max 64 chars
description: |
  What it does and when to trigger it. 1-4 sentences.
  Be specific about trigger phrases. "Pushy" is right — Claude undertriggers.
---
```

**Body structure for most skills:**
```
# [Skill Name]

Brief framing paragraph (what this is, the mental model).

## Decision Tree / When to Use What
Short table or if-then. Helps Claude pick the right path fast.

## Core Workflow
Steps or sections. Explain the *why* behind non-obvious choices.

## Gotchas / Common Mistakes
What Claude will get wrong without this section.

## Quick Reference
Copy-paste templates, code snippets, lookup tables.
```

Keep SKILL.md under 500 lines. When you exceed that: extract to `references/`.

### Step 3 — Test on Real Prompts

Run 2-3 prompts that represent what real users would actually say. Observe:
- Did Claude read the skill? (Check for `bash SKILL.md` in transcript)
- Did Claude follow the workflow or improvise its own?
- Did the output match what you'd consider correct?
- Where did it go off-track?

Write down *specific* failures — not "it was bad" but "it used pip install without `--break-system-packages`" or "it didn't read `references/forms.md` before filling the form."

### Step 4 — Revise Based on Failures

Map each failure to a skill fix:

| Failure Type | Fix |
|-------------|-----|
| Claude ignored a step | Make the step more explicit + explain *why* it matters |
| Claude reinvented a helper script | Bundle the script in `scripts/`, reference it explicitly |
| Claude read SKILL.md but missed the reference file | Make the reference call-to-action more direct |
| Output format was wrong | Add a template or example in the skill |
| Claude undertriggered (didn't read skill when it should) | Strengthen the description; add more trigger phrases |
| Claude overtriggered (read skill unnecessarily) | Tighten the description with explicit NOT triggers |

### Step 5 — Package

When the skill is stable:
```bash
python package_skill.py path/to/skill-folder/
```
This creates a `.skill` file ready for installation. See `references/evals.md` for the full packaging checklist.

---

## The Three Laws of Skill Writing

**1. Only say what Claude doesn't already know.**  
Every line competes for context window. If Claude could infer it from training, cut it. Domain-specific gotchas, environment paths, output templates — keep. Generic "be helpful and clear" — cut.

**2. Explain the why, not just the what.**  
Instructions without reasons get ignored when Claude thinks it knows better. "Use `--break-system-packages`" is weaker than "Use `--break-system-packages` because pip in this environment rejects installs without it, even for packages you need."

**3. Trust progressive disclosure — don't front-load everything.**  
The SKILL.md body is Level 2. Reference files are Level 3. Scripts are Level 4 (execute without loading). If information is only needed for a sub-case, move it to a reference file and point to it with a clear trigger.

---

## Common Pitfalls

| Mistake | What Happens | Fix |
|---------|-------------|-----|
| Front-loading the full reference manual | SKILL.md hits 800 lines, Claude struggles to extract the key steps | Split into references/ — put procedures in SKILL.md, details in references/ |
| Writing ALWAYS/NEVER without explaining why | Claude ignores caps-lock rules when its own judgment says otherwise | Replace with reasoning: "Do X because Y will happen otherwise" |
| Generic description that doesn't name triggers | Skill never fires even when it should | Name the exact phrases users say ("write a skill", "build a SKILL.md") |
| Asserting things Claude already knows | Wasted tokens, no improvement | Audit every line: "Would Claude do this without being told?" If yes, cut |
| No evals before shipping | Skill seems fine but fails on real diverse inputs | Always run 3 real prompts before packaging |
| Bundle everything in one file | Any context means all context — bloated for simple cases | Use progressive disclosure, reference files for optional content |

---

## Quick Reference: File Layout

```
my-skill/
├── SKILL.md           ← Required. Frontmatter + core instructions.
├── references/        ← Optional. Domain docs, sub-guides.
│   ├── guide-a.md
│   └── guide-b.md
├── scripts/           ← Optional. Pre-built Python/bash helpers.
│   └── process.py
├── assets/            ← Optional. Templates, fonts, icons.
└── evals/             ← Recommended. Test prompts for iteration.
    └── evals.json
```

The `.skill` file is just a zip of this folder (evals/ excluded from distribution).