# Code Review Best Practices

English | [中文](../code-review-best-practices.md)

The core goal of Code Review is to confirm the intent of changes, behavioral boundaries, risks, and long-term maintenance costs.

A good review finds bugs and helps the team maintain shared engineering judgment.

## Review Order

We recommend reviewing in this order:

1. Is the PR goal clear?
2. Is the diff scope focused?
3. Do behavioral changes match expectations?
4. Are tests and validations reliable?
5. Are error handling and boundary conditions complete?
6. Are naming, structure, and style consistent with existing code?
7. Are security risks and rollback paths clear?

## What Reviewers Should Ask

- Is the problem solved by this change clear?
- Are there any unrelated changes?
- Is the blast radius explained?
- Do tests cover the actual behavior?
- Do naming and structure match the existing project?
- Is it easy to roll back if issues occur?

## Review Standards

Google's public Code Review documentation emphasizes that the goal of code review is to ensure the codebase remains healthy and continues to improve over time.

This leads to a practical judgment: if a PR clearly improves the system and introduces no obvious risks, reviewers should lean towards approving it, rather than delaying indefinitely over non-critical details.

Teams can categorize comments into three types:

- Blocking issues: correctness, security, compatibility, obvious maintenance risks.
- Suggestion issues: naming, local structure, readability improvements.
- Optional issues: stylistic preferences, minor optimizations, non-essential content for the current PR.

## What Authors Should Do

- Self-review the diff before opening a PR.
- Proactively explain risks and validation methods.
- Provide additional context for complex designs.
- Respond to review comments item by item.
- Do not throw large, unexplained changes directly at reviewers.

## How to Review AI-Generated Code

Pay special attention to AI-generated code:

- Is the diff too large?
- Did it silently change behavioral boundaries?
- Are tests merely superficial coverage?
- Did it introduce unnecessary abstractions?
- Are unrelated formatting changes or generated files mixed in?

For details, see [AI-Generated Code Review](../../05-ai-native-development/05-ai-native-development_en/ai-generated-code-review_en.md).

## Governance Insights from Large Projects

Kubernetes' OWNERS model splits reviews into two layers: reviewers and approvers. The former focus on code quality, while the latter focus on overall acceptance criteria, compatibility, and long-term impact.

Enterprise teams can learn from this tiering: general reviewers are responsible for finding specific issues, while code owners or module leads are responsible for final approval.

## Templates

See [Code Review Checklist](../../08-templates/08-templates_en/code-review-checklist_en.md).

## Extended Reading

- [GitHub Docs: About pull request reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)
- [Atlassian: Pull requests and code review](https://www.atlassian.com/git/tutorials/making-a-pull-request)
- [Google Engineering Practices: Code Review](https://google.github.io/eng-practices/review/)
- [Google Code Review Practices](../../10-company-practices/10-company-practices_en/google-code-review_en.md)
- [Open Source Project Git Governance Practices](../../09-resources/09-resources_en/open-source-governance-practices_en.md)
- [Gerrit Code Review Governance Reference](../../09-resources/09-resources_en/gerrit-code-review-governance_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
