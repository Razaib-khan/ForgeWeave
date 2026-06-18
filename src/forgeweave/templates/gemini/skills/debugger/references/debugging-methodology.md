# Systematic Debugging Methodology

## The Scientific Method for Bugs

1. **Observe**: What exactly is happening? Get the exact error message, stack trace, unexpected output.
2. **Hypothesize**: What could cause this? List 2-3 possible root causes.
3. **Design a test**: For each hypothesis, design a test that would confirm or eliminate it.
4. **Test**: Run the diagnostic test. Collect data.
5. **Eliminate**: Eliminate hypotheses that don't match the evidence.
6. **Repeat**: If more than one hypothesis remains, design finer-grained tests.
7. **Isolate**: When one hypothesis remains, confirm it with a minimal reproduction.
8. **Fix**: Design the minimal fix. Verify it resolves the symptom.
9. **Prevent**: Add a regression test and document the root cause.

## Common Bug Categories

| Category | Signs | Approach |
|---|---|---|
| Logic error | Wrong output, no crash | Trace values through the logic |
| Null/undefined | TypeError, AttributeError | Check what's null and why |
| Race condition | Intermittent failure | Add logging, check shared state |
| Resource leak | Memory grows, ports exhausted | Add instrumentation, check cleanup |
| Configuration | Works on one machine, not another | Compare configs, check env vars |
| API contract | Integration fails | Mock the API, check request/response |

## Bisection Strategy

For regression bugs:
1. `git bisect start`
2. `git bisect bad HEAD`
3. `git bisect good <known-good-commit>`
4. At each step: test if the bug exists
5. Git finds the exact commit that introduced the bug
