# Skill Testing, Iteration & Packaging

---

## Why Test Before Shipping

A skill that looks correct on paper often fails in practice because:
- The description doesn't match how real users phrase requests
- SKILL.md instructions are ambiguous in ways the author doesn't see
- Claude reads the skill but makes a different inference than intended
- An edge case wasn't covered that appears in the second real prompt

The minimum test set is **3 diverse real prompts** — things an actual user would type, not synthetic examples designed to make the skill look good.

---

## The Test Workflow (Claude.ai / No Subagents)

Since Claude.ai doesn't have subagents, run tests sequentially:

### Step 1: Write prompts first, before running anything

Save to `evals/evals.json`:

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "The exact thing a real user would type",
      "expected_output": "Description of what good looks like",
      "files": []
    },
    {
      "id": 2,
      "prompt": "A different real user phrasing",
      "expected_output": "...",
      "files": ["evals/files/sample.pdf"]
    }
  ]
}
```

**What makes a good test prompt:**
- Realistic user language (casual, abbreviated, sometimes incomplete)
- Doesn't name the skill explicitly ("use the pdf skill to...")
- Represents a case that's caused real problems before
- Diverse — different input types, different intents

**What makes a bad test prompt:**
- "Please use my skill to do X exactly as described" — too synthetic
- Three prompts that all test the same path
- A prompt designed to succeed rather than to probe weaknesses

### Step 2: Execute each prompt with the skill loaded

For each test case:
1. Read `SKILL.md` (simulate what Claude does on trigger)
2. Complete the task as instructed by the skill
3. Note: did you read all the files the skill pointed to? Did you run the scripts it mentioned?
4. Save outputs

### Step 3: Evaluate what went wrong

After each run, ask:

| Check | Questions |
|-------|-----------|
| Trigger | Did the skill trigger? Would the description have matched? |
| Navigation | Did Claude read the right reference files? |
| Script usage | Did Claude run the scripts instead of reinventing them? |
| Output | Does the output match the expected format / quality? |
| Specific failures | What *exactly* went wrong? Not "it was off" — what specifically? |

### Step 4: Write assertions

Assertions are the specific, verifiable things the skill should guarantee. Write them *after* seeing what went wrong — the failures reveal what matters.

Good assertions are **discriminating**: they pass when the skill works and fail when it doesn't.

```json
"expectations": [
  "Output is a valid .docx file",
  "The document uses Arial font throughout",
  "All formula cells reference assumption cells rather than hardcoded numbers",
  "The skill's extract_fields.py script was used rather than manual parsing"
]
```

Weak assertions (pass regardless):
```
"The output is helpful"       ← not verifiable
"Claude was responsive"       ← irrelevant
"A file was created"          ← too easy to satisfy
```

### Step 5: Revise and re-run

See "Improving from Failures" table in `references/writing.md`.

Run the same prompts again after revising. Compare outputs directly. Stop when:
- All prompts produce output you'd actually want to deliver
- All your assertions pass
- There are no new specific failures in the latest run

---

## evals.json Full Schema

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User prompt text",
      "expected_output": "Human-readable success description",
      "files": ["evals/files/input.pdf"],
      "expectations": [
        "Output is a .pdf file",
        "All form fields from the input are populated",
        "The extract_fields.py script was used",
        "No field was left blank when data was available"
      ]
    }
  ]
}
```

**Fields:**
- `id` — unique integer
- `prompt` — what the user types
- `expected_output` — human description of success (for review)
- `files` — input files relative to skill root (optional)
- `expectations` — verifiable assertions (add after first run)

---

## What to Look for in the Transcript

The transcript is more informative than the output. Read it to find:

| Pattern in Transcript | Meaning |
|----------------------|---------|
| Claude reads SKILL.md immediately | Trigger worked |
| Claude proceeds without reading SKILL.md | Trigger failed — fix the description |
| Claude reads SKILL.md but not the referenced file | Reference trigger too weak — make it more explicit |
| Claude writes its own helper script | Bundle that script; it clearly recurs |
| Claude uses the bundled script | 
| Claude describes what it's about to do differently than the skill intends | Instructions ambiguous — reframe with why |
| Claude skips a step and gives a reason | Either update the skill to address that reason, or add more explicit motivation |

---

## Description Trigger Testing

The skill description is a separate thing to test from the skill body. A skill that triggers incorrectly (too often or not enough) is broken regardless of how good the body is.

**Test trigger accuracy by asking:**
1. Does the description fire when a user says the trigger phrases I listed?
2. Does it fire when a user says something *adjacent* that shouldn't trigger it?
3. Does it stay silent on clearly unrelated prompts?

Test this with representative prompts — both should-trigger and should-not-trigger — and check whether Claude reads the skill in each case.

**Signs of over-triggering:**
- Claude reads the skill on generic questions in an adjacent area
- Users mention the domain casually and the skill loads unnecessarily

**Signs of under-triggering:**
- Claude handles the task without reading the skill even when it should
- The skill only fires when the user explicitly names it

Fix over-triggering: add a "Do NOT use for X" clause to the description.  
Fix under-triggering: add more trigger phrases; use more specific language about contexts.

---

## Pre-Packaging Checklist

Before running `package_skill.py`:

**Content:**
- [ ] `name` is lowercase, hyphens only, max 64 chars, no reserved words
- [ ] `description` is under 1024 chars, contains trigger phrases, describes when to use it
- [ ] SKILL.md body is under 500 lines (or has clear `references/` delegation)
- [ ] All referenced files (`references/`, `scripts/`) actually exist
- [ ] Scripts are executable and have been tested
- [ ] `evals/evals.json` exists with at least 3 prompts
- [ ] All 3+ test prompts produce correct output

**No-ships:**
- [ ] No hardcoded credentials or secrets
- [ ] No calls to untrusted external URLs in scripts
- [ ] No instructions that direct Claude to exfiltrate data
- [ ] No content that would surprise a user who read the description

**Updating an existing skill:**
- [ ] Preserved the original `name` (changing it breaks installations)
- [ ] Copied to a writable location before editing (`cp -r /mnt/skills/... /tmp/...`)
- [ ] Tested the new version against the same prompts used for the original

---

## Packaging Command

```bash
# From the directory containing your skill folder:
python package_skill.py my-skill/

# Specify an output directory:
python package_skill.py my-skill/ ./dist/
```

This creates `my-skill.skill` — a ZIP archive ready for installation.

**What's included:** SKILL.md, references/, scripts/, assets/, LICENSE.txt  
**What's excluded:** evals/, __pycache__/, node_modules/, *.pyc, .DS_Store

---

## The Minimum Viable Skill vs The Good Skill

| | Minimum Viable | Good |
|-|---------------|------|
| Frontmatter | name + description | All relevant fields + version |
| Description | Vague but correct | Specific trigger phrases, explicit scope |
| Body | Steps + basic gotchas | Steps + why + gotcha table + quick reference |
| References | None | Key sub-guides separated by domain |
| Scripts | None | Any deterministic task that recurred in tests |
| Evals | None | 3+ real prompts, 3+ assertions each |
| Test coverage | Assumed | Verified — all prompts produce acceptable output |

Don't ship the minimum viable. Ship the good one.

---

## Common Eval Failures and What They Mean for the Skill

| Eval Failure | Root Cause | Skill Fix |
|-------------|-----------|-----------|
| Claude didn't read the skill at all | Description doesn't match user's phrasing | Add trigger phrases matching how users actually talk |
| Claude read SKILL.md but skipped reference file | Pointer to reference was too weak or conditional | Make the read instruction more direct and conditional trigger more specific |
| Output format was wrong | No template or example in skill | Add a template with "Use this exact structure" |
| Claude invented a workaround instead of using the script | Script reference buried or unclear | Move script reference earlier; say "run this before doing anything else" |
| Claude got a specific library call wrong | Wrong API not documented | Add a gotcha entry for that exact mistake |
| Two test cases produced very different outputs | Skill too vague — Claude improvises | Add more concrete examples for both cases |
| High variance (passes sometimes, fails other times) | Skill relies on Claude's judgment for a non-deterministic choice | Make the choice explicit (table, rule, or script) |