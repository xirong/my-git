# AI Reviewer and Human Reviewer

English | [中文](../ai-reviewer-and-human-reviewer.md)

AI Reviewers are suitable for finding repetitive problems, checking for omissions, and generating review checklists.

Human Reviewers are responsible for judging intent, boundaries, long-term maintenance costs, and whether a merge is permissible.

## AI Reviewer Suitable for Checking

- Whether the diff is too large
- Whether there are irrelevant changes
- Whether there are obvious bugs
- Whether there are test gaps
- Whether there are security risks
- Whether there are style inconsistencies

## Human Reviewer Responsible for Judging

- Whether this requirement should be implemented this way
- Whether semantic boundaries are correct
- Whether an abstraction is worth introducing
- Whether risks are acceptable
- Whether merging is allowed

## Reusable Prompt

```text
Please act as an AI reviewer and review the current git diff.
List only specific risks, sorted by severity.
Each entry includes file location, problem, and suggestion.
Do not output vague praise or summaries.
```

## Collaboration Principles

AI Reviewers can increase check coverage, but they cannot replace human owner judgment.

Recommended process:

1. The author self-reviews the diff first.
2. The AI Reviewer performs the first round of risk scanning.
3. The author addresses clear problems.
4. The Human Reviewer makes the final judgment.
5. Merge only after CI and necessary manual verification pass.

## Cooperation with CODEOWNERS

The AI Reviewer can perform a general risk scan first, and CODEOWNERS can then assign the PR to the person who truly understands that directory.

Recommended combination:

```text
AI reviewer -> author self-fix -> code owner review -> CI -> merge
```

This can reduce low-value checks for reviewers and save human attention for semantics, boundaries, long-term maintenance costs, and deployment risks.

## Extended Reading

- [Responsible use of GitHub Copilot code review](https://docs.github.com/en/copilot/responsible-use/code-review)
- [AI Generated Code Review](ai-generated-code-review_en.md)
- [Open Source Git Governance Practices](../../09-resources/09-resources_en/open-source-governance-practices_en.md)
- [AI Code Review Checklist](../../08-templates/08-templates_en/ai-code-review-checklist_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
