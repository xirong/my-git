# Code Review Checklist

English | [中文](../code-review-checklist.md)

## Intent

- [ ] The purpose of the change is clear
- [ ] The PR solves one problem
- [ ] Unrelated changes are split out

## Behavior Changes

- [ ] Existing behavior is preserved unless intentionally changed
- [ ] Edge cases are considered
- [ ] Error handling is explicit

## Tests

- [ ] Tests cover the changed behavior
- [ ] Tests are meaningful
- [ ] Verification steps are documented

## Maintainability

- [ ] Code follows existing style
- [ ] Naming is clear
- [ ] No unnecessary abstraction is introduced

## Risk

- [ ] Security impact is considered
- [ ] Rollback path is clear
- [ ] Operational impact is documented
