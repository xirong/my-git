# How to Review AI-Generated Code

English | [中文](../ai-generated-code-review.md)

The risk with AI-generated code is that it often changes boundaries, semantics, dependencies, and long-term maintenance costs while in a state that "looks reasonable."

When reviewing AI code, review the intent first, then the diff, and then the validation.

## 1. Review Order

### Understand Intent First

Ask first:

- What problem is being solved this time?
- What are the success criteria?
- Which behaviors should not change?
- What are the scopes of impact?

For an AI diff without clear intent, do not enter code details first.

### Then Look at Diff Size

```bash
git diff --stat
```

If the number of files is too large, split them first:

- Behavioral fixes
- Test additions
- Refactoring and cleanup
- Documentation descriptions
- Dependency or configuration adjustments

### Then Look at Behavioral Changes

Focus checks on:

- Public API
- Error codes
- Configuration default values
- Database reads and writes
- Concurrency and retries
- Permissions and security
- Compatibility

### Finally Look at Tests

AI-written tests easily verify only "the implementation it just wrote" and do not verify real business boundaries.

Good tests should answer:

- Will it fail before the fix?
- Does it cover exception paths?
- Does it cover boundary conditions?
- Is it just proving itself correct in a mock?

## 2. High-Risk Signals

- Large amounts of irrelevant formatting
- Modifying multiple business problems at once
- Adding a new abstraction but with only one call point
- Changing configuration without explaining runtime impact
- Modifying lock files without explaining dependency changes
- New tests not asserting core behavior
- Deleting exception handling or swallowing errors
- Modifying public API without compatibility notes
- Appearance of hard-coded tokens, keys, accounts, or internal addresses

## 3. Review Checklist

- [ ] I can explain the goal of this change in one sentence.
- [ ] The diff can be reviewed within a reasonable time.
- [ ] Irrelevant changes have been split out.
- [ ] Behavioral changes are clearly marked.
- [ ] Error handling has not become weaker.
- [ ] Tests can prove real behavior.
- [ ] No sensitive information has been added.
- [ ] No unnecessary dependencies have been introduced.
- [ ] The rollback path is clear.

## 4. Prompt Examples

### Let AI Perform Risk Review

```text
Please review the current git diff.
Output only specific risks, do not provide vague summaries.
Focus checks on: behavioral boundaries, compatibility, error handling, test validity, security risks, and irrelevant changes.
Give file paths, risk descriptions, and suggested modification methods for each problem.
```

### Let AI Split Commits

```text
Based on the current git diff, please suggest how to split it into multiple logical commits.
Provide a title, included files, and reason for splitting for each commit.
Do not modify files.
```

### Let AI Generate PR Description

```text
Please generate a PR description based on the current git diff.
Include What changed, Why, How tested, Risk, and Rollback plan.
Mark content that cannot be confirmed from code as "requires manual input."
```

## 5. Humans Assume Final Responsibility

AI can help you find problems faster, but it cannot assume merge responsibility for you.

The final reviewer should at least confirm:

- They understand this change.
- The validation results are credible.
- The risks and rollback plans are acceptable.
- They can locate responsibility boundaries if problems occur after merging.

## 6. How to Use AI Review Tools

AI Review tools are suitable for the first round of scanning, especially for finding obvious bugs, test gaps, security risks, irrelevant changes, and maintainability issues.

Teams should maintain three boundaries when using them:

1. AI review results do not constitute owner approval.
2. High-risk directories still require human owner review.
3. False positives and false negatives of AI review should be periodically reviewed.

Put AI review results into the PR process, but do not let them replace human merge judgment.

## Extended Reading

- [AI Code Review Checklist](../../08-templates/08-templates_en/ai-code-review-checklist_en.md)
- [AI Change Review Practice Example](ai-change-review-example_en.md)
- [Pull Request Template](../../08-templates/08-templates_en/pull-request-template_en.md)
- [Responsible use of GitHub Copilot code review](https://docs.github.com/en/copilot/responsible-use/code-review)
- [Review AI-generated code](https://docs.github.com/en/enterprise-cloud@latest/copilot/tutorials/review-ai-generated-code)
- [Git Integration Practices for AI Coding Tools](ai-coding-tools-git-integration_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
