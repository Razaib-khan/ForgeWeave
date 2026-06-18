# Testing Guidelines

## Test Structure (AAA Pattern)
```
Arrange  — Set up test data and dependencies
Act      — Execute the function under test
Assert   — Verify the result
```

## What to Test
- Happy path: normal inputs produce correct output
- Edge cases: empty input, null, max/min values, boundaries
- Error cases: invalid input produces proper error
- State changes: mutations, side effects

## What NOT to Test
- Framework internals (React, Next.js, Express — trust them)
- Third-party library behavior (mock it)
- Generated code (test the generator instead)
- Configuration files (test the config loading, not the file itself)

## Coverage Targets
- New code: 90%+ line coverage
- Critical paths: 100% branch coverage
- Error handlers: each error path tested

## Test Naming
- Python: `test_<function>_<scenario>`
- TypeScript: `<function> should <expected> when <condition>`
- Test files mirror source structure
