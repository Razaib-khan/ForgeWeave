# SKILL_SPEC.md Quick Reference

## Required Frontmatter Fields

| Field | Type | Required |
|---|---|---|
| `skill_id` | kebab-case | Yes |
| `name` | Title Case | Yes |
| `version` | semver | Yes |
| `description` | string (1 sentence) | Yes |
| `author` | string | Yes |
| `tui_compatibility` | list | Yes |
| `tags` | list | No |

## Required Body Sections (in order)

1. Purpose
2. Trigger Conditions → (mapped to "When to Use" + "When Not to Use")
3. Pre-conditions
4. Inputs
5. Execution Steps → (mapped to "Exact Workflow Steps")
6. Decision Rules
7. Output Format → (mapped to "Expected Outputs")
8. Failure Handling → (mapped to "Failure Modes")
9. Constraints
10. Examples

## Validation Rules

| Rule | Failure |
|---|---|
| `skill_id` matches directory name | Hard error |
| All required frontmatter fields | Hard error |
| All required sections present | Hard error |
| `tui_compatibility` not empty | Hard error |
| `version` follows semver | Warning |
| Examples section not empty | Warning |
