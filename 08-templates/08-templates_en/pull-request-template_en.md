# Pull Request Template

English | [中文](../pull-request-template.md)

> Complete the sections that apply to this pull request. Write “Not used” in the AI collaboration record when no AI tool was used. State the fact when human review has not happened or validation is incomplete.

## What Changed

Briefly describe the main changes.

## Why This Change

Explain the reason for this change and the intended result.

## Task Scope

- Allowed changes:
- Excluded scope or intentionally unchanged:

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Refactoring
- [ ] Documentation
- [ ] Tests
- [ ] Engineering maintenance

## AI Collaboration Record (Optional)

- Tool and model, if known: Enter the tool and model; write “Not used” when no tool was used.
- AI participation scope:
- Files or content generated, changed, or suggested by AI:

Recording tool participation here does not replace the human-review and validation records below.

## Human Review

- Files actually reviewed by a person, with the review focus:
  - `<path>`:
- Human review not completed or not performed:

List only review that actually happened. If no person has reviewed the change, state “No human review performed.” Write “None” only after confirming that no review remains.

## Validation Evidence

| Command or check | Actual result | Covered scope or evidence |
| --- | --- | --- |
|  | Passed / failed / not run |  |

- Unverified gaps, reasons, and possible impact:

Write “None” only after checking that no validation gaps remain.

## Risk and Rollback

- Risks and mitigations:
- Rollback plan:

## Review Hints

- Files, behavior, or scenarios reviewers should prioritize:

## Before Requesting Review

- Is the diff focused and ready for a serious review:
- Have tests been added or updated; if not applicable, why:
- Has necessary documentation been updated; if not applicable, why:
- Has the change been checked for committed secrets or sensitive data:
