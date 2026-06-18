# Common Refactoring Patterns

## 1. Extract Function
When: A code block has a clear, single purpose
Before: 20 lines inline with a comment
After: Named function with the 20 lines, comment becomes function name

## 2. Rename Symbol
When: A name is unclear, misleading, or inconsistent
Check: Update ALL references across the codebase

## 3. Consolidate Duplicate Code
When: Same logic appears in multiple places
Before: Copy-pasted code in 3 places
After: One shared function called from 3 places

## 4. Split Loop
When: One loop does two different things
Before: Loop that both filters and transforms
After: One loop to filter, one to transform

## 5. Replace Conditional with Polymorphism
When: Switch/if-else chain dispatches on type
Before: `if type == 'a': ... elif type == 'b': ...`
After: Each type has its own class/function

## 6. Introduce Parameter Object
When: Multiple parameters are always passed together
Before: `function(date_from, date_to, date_format)`
After: `function(DateRange { from, to, format })`

## Golden Rule
Make ONE refactoring at a time. Run tests after each change.
