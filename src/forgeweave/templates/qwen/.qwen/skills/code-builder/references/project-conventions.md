# Code Conventions Reference

## Python
- Follow PEP 8
- Use type hints (Python 3.10+ syntax: `list[str]` not `List[str]`)
- Use `pathlib.Path` over `os.path`
- Use `f-strings` over `%` or `.format()`
- Use `ruff` for linting (line length 120)

## TypeScript / JavaScript
- Use strict TypeScript mode
- Prefer `const` over `let`, never use `var`
- Use `async/await` over raw promises
- Use `ESM` imports (not CommonJS `require`)
- Use `Vitest` or `Jest` for testing

## General
- One concern per file
- Exported functions first, private helpers below
- No commented-out code
- No print/debug statements in production code
- Errors are handled, not swallowed
