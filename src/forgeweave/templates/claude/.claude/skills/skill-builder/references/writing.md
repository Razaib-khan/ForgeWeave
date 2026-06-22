# Skill Writing Guide — Style, Description Engineering & Anti-Patterns

---

## The Writing Philosophy

Claude is intelligent. Treat it that way. The goal is to transmit understanding — the mental model, the why, the edge cases you've already thought through — not to issue commands at a model that needs to be beaten into submission.

**The test for every instruction:** Would Claude, being smart and well-meaning, get this wrong without being told? If no → cut it. If yes → explain *why* the correct approach matters, not just what it is.

If you find yourself writing `ALWAYS` or `NEVER` in all caps, that's a signal. Either the instruction is actually important (in which case explain why), or it's filler that feels important but isn't.

---

## Description Engineering (The Most Important Thing)

The description is the only thing Claude reads before deciding whether to trigger the skill. Get it wrong and the skill never fires. Get it wrong the other way and it fires on everything.

### What a Good Description Contains

1. **What the skill does** — concise, domain-specific
2. **When to use it** — explicit trigger scenarios
3. **Specific trigger phrases** — the actual words users say
4. **Negative scope** (optional) — what it does NOT cover, when it distinguishes from a similar skill

### The "Pushy" Principle

Claude undertriggers by default. It will try to handle things itself rather than read a skill it's not sure about. Your description needs to be assertive:

❌ Weak: `"Helps with PDF tasks."`

✓ Strong: `"Use this skill whenever the user wants to do anything with PDF files — reading, merging, splitting, filling forms, OCR, watermarking, encrypting, or creating PDFs. If the user mentions a .pdf file or asks to produce one, use this skill."`

The strong version:
- Lists specific operations (gives Claude pattern-matching anchors)
- Explicitly states the trigger condition ("if the user mentions")
- Covers the no-brainer case (mentions the file type)

### Trigger Phrase Examples (Real Patterns That Work)

```
"Use when user says 'write a skill', 'build a SKILL.md', 
'make an agent skill for', 'how do I teach Claude to', 
or any request to capture repeatable workflows as skills."

"Triggers on: 'deploy to AWS', 'push to production', 
'run the CI pipeline', or whenever the user mentions 
staging, deployment, or release automation."

"Use when a file has been uploaded but its content is NOT 
in context — only its path at /mnt/user-data/uploads/ is visible."
```

### Distinguishing From Adjacent Skills

When two skills cover adjacent domains, add explicit differentiation:

```
"Use for PDF creation, manipulation, and OCR. 
Do NOT use for reading/extracting content from PDFs already in context 
(use pdf-reading for that) or for Word documents (use docx)."
```

### Description Anti-Patterns

| Anti-Pattern | Problem |
|-------------|---------|
| `"Helps with X tasks."` | Too vague — Claude won't trigger |
| `"A comprehensive guide to..."` | Describes the skill, not when to use it |
| No trigger phrases | Claude can't recognize the context |
| `"Use when the user explicitly asks for this skill"` | Requires user to know skill exists — never works |
| Over 1024 characters | Hard cap — truncated, may break triggering |

---

## Writing Patterns

### Defining a Workflow (Numbered Steps)

Number steps when order matters. Put the rationale after the action:

```markdown
## Workflow
1. **Read the uploaded file** — Don't assume content from context; always re-read from disk.
2. **Extract fields** — Run `scripts/extract.py` rather than parsing manually; it handles edge cases.
3. **Validate output** — Check for errors before saving. An empty output is worse than a visible error.
```

### Defining Output Formats (Template Pattern)

When the output must match a specific structure:

```markdown
## Output Format
Use this exact structure every time:

# [Report Title]
## Executive Summary
[2-3 sentences max]

## Key Findings
[Numbered list, each item < 50 words]

## Recommendations
[Actionable items, ranked by priority]
```

### Decision Trees (Table Pattern)

For skill types where the path depends on input characteristics:

```markdown
## Which Approach to Use

| Input Type | Correct Approach | Notes |
|------------|-----------------|-------|
| Scanned PDF (no text layer) | OCR → extract | pytesseract required |
| Text-based PDF | pdfplumber | Handles tables well |
| Password-protected | qpdf decrypt first | Password from user |
| > 100 pages | Process in batches | Memory limit |
```

### Gotcha Tables (The Most Underrated Pattern)

The most valuable thing a skill can contain is knowledge Claude will get wrong from pure reasoning:

```markdown
## Gotchas

| Situation | Wrong Approach | Correct Approach |
|-----------|---------------|-----------------|
| pip install in this env | `pip install X` | `pip install X --break-system-packages` |
| Unicode subscripts in ReportLab | Use ₂ character | Use `<sub>2</sub>` XML tag |
| Formula recalculation in xlsx | openpyxl alone | Run LibreOffice via `scripts/recalc.py` |
```

### Examples Pattern

Show don't tell, especially for formatting rules:

```markdown
## Commit Message Format

**Input:** Added user authentication with JWT tokens  
**Output:** `feat(auth): implement JWT-based authentication`

**Input:** Fixed crash when network is offline  
**Output:** `fix(network): handle offline state gracefully`
```

### Negative Examples (When to Include)

When Claude reliably makes a specific mistake, show what NOT to do:

```markdown
## Output Quality

**DO NOT** return raw extracted text:
```
Name: John Smith Phone: 555-1234 Email: j@example.com
```

**DO** structure it as JSON:
```json
{"name": "John Smith", "phone": "555-1234", "email": "j@example.com"}
```
```

---

## Style Guide

**Imperative form.** Instructions, not descriptions.
- ✓ "Read the SKILL.md before writing code."
- ✗ "The SKILL.md should be read before writing code."

**Explain the why.** Especially for non-obvious rules.
- ✓ "Use `--isolated` so each test run starts from a clean browser state (cookies from a prior run will break auth flows)."
- ✗ "Always use `--isolated`."

**Match formality to the domain.** A financial modeling skill can be precise and structured. A creative writing skill should be more conversational.

**Short paragraphs over long ones.** Claude parses short paragraphs reliably. Dense walls of text increase the chance of a key constraint being missed.

**Tables over prose lists when structure matters.** Especially for lookup tables, decision trees, and error reference.

**Code over explanation when precision matters.** Show the correct import, the correct flag, the correct function call. Prose descriptions of code are lossy.

---

## How Claude Reads a Skill (Cognitive Model)

Understanding how Claude processes a skill makes you a better skill author.

1. Claude sees `name` + `description` at startup (Level 1)
2. User message arrives — Claude scans available skills
3. If description matches the task, Claude reads `SKILL.md` body (Level 2)
4. Claude uses the skill as its working guide, reading reference files when explicitly triggered (Level 3)
5. Claude executes scripts when instructed, without loading them (Level 4)

**Implication for writing:**
- The SKILL.md body is read as a whole before Claude acts. Put the most important constraint first, not at the end where it may be deprioritized in a long doc.
- Reference file triggers should be specific ("if the user is filling a form, read references/forms.md") not vague ("see references/ for more").
- If a script name is mentioned explicitly, Claude will run it. If it's buried 400 lines down, it may not be found.

---

## Content That Should Be Scripted (Not Written as Instructions)

If Claude will need to do it repeatedly and it's deterministic, script it.

| Task | Why Script It |
|------|--------------|
| Extract PDF form fields | Deterministic; manual parsing is error-prone |
| Recalculate xlsx formulas | Requires LibreOffice; can't be done via openpyxl alone |
| Validate output format | Consistent, rerunnable; LLM validation is unreliable |
| Create boilerplate file structures | Exact output required every time |
| Sort, hash, count, calculate | Pure computation — LLM generation is wasteful and unreliable |

Include scripts when: 3+ test cases required a similar piece of ad-hoc code; the task is clearly algorithmic; or the correct result is not probabilistic.

---

## Improving an Existing Skill

When improving a skill (not creating from scratch):

1. **Read the skill first.** Understand the current intent before changing anything.
2. **Preserve the name.** The `name` field is the install ID — changing it breaks installations.
3. **Copy before editing if the path is read-only.** `cp -r /mnt/skills/public/my-skill /tmp/my-skill`
4. **Edit from the failure, not the general.** Map each specific failure to a specific fix.
5. **Generalize, don't over-fit.** A skill that works perfectly for 3 test cases but nothing else is worthless.
6. **Read the transcript, not just the output.** The transcript shows where Claude went off-track — which step it skipped, which file it didn't read.
7. **If multiple test cases independently wrote the same helper script, bundle it.** That's the strongest signal that a script belongs in the skill.

---

## The "Write-Review-Cut" Cycle

Every skill draft deserves a second pass with fresh eyes:

**Write** — get everything important into the file.

**Review** — read it as Claude would:
- Is the opening clear about what this skill does?
- Could Claude extract the right path in < 5 seconds of reading?
- Is there anything here Claude would already do without being told?
- Is there anything missing that caused the real failures?

**Cut** — remove anything that survives all three questions with "yes, but it doesn't hurt":
- It does hurt. Every unnecessary token is attention diluted.
- Lean skills outperform bloated ones.

A good skill often ends up 30% shorter after the cut pass, and 50% more effective.