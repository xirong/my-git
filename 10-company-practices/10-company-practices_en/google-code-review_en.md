# Google Code Review Practice

English | [中文](../google-code-review.md)

Original links:

- [Google Engineering Practices](https://google.github.io/eng-practices/)
- [Google Code Review Introduction](https://google.github.io/eng-practices/review/)
- [The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html)

## 1. The Most Core Judgment

The most valuable takeaway from Google's Code Review documentation is that it focuses the goal of code review on long-term code health.

This means the reviewer's focus is not to polish every PR to perfection, but to determine whether the change makes the overall system better.

Enterprise teams can easily turn Code Review into a nitpicking process, eventually slowing everyone down. Google's documentation reminds us that Code Review needs to balance two things simultaneously:

- Long-term health of the codebase
- Developers can continue to advance their work

## 2. What Should Reviewers Look At

It can be broken down into these categories:

| Dimension | Focus Area |
| --- | --- |
| Design | Is the solution suitable for the current system |
| Correctness | Does it actually solve the problem, and does it introduce new bugs |
| Complexity | Is it over-engineered, and does it increase maintenance costs |
| Tests | Does it cover key behaviors and edge cases |
| Naming | Does it clearly express intent |
| Style | Does it conform to the team's existing conventions |
| Documentation | Are external behaviors or complex logic clearly explained |

## 3. Do Not Strive for "Perfect PRs"

The goal of Code Review is not to make the code completely flawless.

If a change improves the system overall and does not significantly reduce maintainability, reviewers should lean towards approving it, while marking non-critical suggestions as optional improvements.

Teams can adopt this rule:

- Blocking issues: Correctness, security, compatibility, obvious maintenance risks
- Suggestion issues: Naming, local structure, readability improvements
- Optional issues: Stylistic preferences, minor optimizations, non-essential content for the current PR

This avoids reviewers turning all comments into mandatory changes.

## 4. More Important for AI-Generated Code

AI-generated code often looks very complete, but Code Review must still return to code health:

- Has it introduced unnecessary abstractions
- Has it bypassed existing designs
- Has it weakened error handling
- Has it produced code that "looks more generic but is actually harder to maintain"
- Has it only added superficial tests

Reviewing AI code requires checking whether the syntax makes sense, but more importantly, whether the long-term maintenance cost is acceptable.

## 5. Actionable Rules for Enterprise Teams

1. Categorize review comments, clearly distinguishing between blocking and suggestions
2. Reviewers prioritize looking at design, correctness, tests, and security
3. Leave style issues to automated tools as much as possible
4. Use `nit` or similar tags for non-critical suggestions
5. Escalate prolonged disputes to owners or tech leads; do not let a PR stall indefinitely
6. Clearly state whether it can be merged when the review is concluded

## 6. Key Takeaways

Code Review is the carrier of a team's engineering judgment.

A good review must hold the baseline while also allowing valuable changes to enter the mainline as quickly as possible.
