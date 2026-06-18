# Validation Rules Reference

## Research Validation Rules
1. Every paragraph must have at least one source URL
2. No blog posts, changelogs, or marketing pages as sources
3. Code blocks must have language annotations
4. All required sections must be present
5. No contradictory claims within or across files
6. No placeholder text (TODOs, FIXMEs) in final output
7. Claims must be specific — no generic statements

## Code Validation Rules
1. Code must parse/compile without errors
2. No `print()` or `console.log()` debug statements
3. Type annotations required for all function signatures
4. No unused imports or variables
5. Error paths handled (not bare except: or empty catch)

## Plan Validation Rules
1. At least 3 steps for anything non-trivial
2. Dependencies explicitly identified
3. Each step has a clear action and expected outcome
4. Risks documented for non-trivial steps
