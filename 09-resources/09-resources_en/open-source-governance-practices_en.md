# Open Source Project Git Governance Practice

English | [中文](../open-source-governance-practices.md)

Original links:

- [Kubernetes OWNERS Files](https://www.kubernetes.dev/docs/guide/owners/)
- [Kubernetes Pull Request Process](https://www.kubernetes.dev/docs/guide/pull-requests/)
- [Linux Kernel: Creating Pull Requests](https://docs.kernel.org/maintainer/pull-requests.html)
- [Go Contribution Guide](https://go.dev/doc/contribute)
- [Rust RFCs](https://github.com/rust-lang/rfcs)

## 1. Why Look at Open Source Governance?

The collaboration issues of mature open-source projects are very similar to enterprise teams:

- Many contributors
- Complex module boundaries
- Limited review resources
- Permissions cannot be granted carelessly
- Changes need to be traceable
- Automation is needed to assist maintainers in making decisions

Their practices offer useful reference for multi-team, multi-service, and multi-repository governance within enterprises.

## 2. Kubernetes: OWNERS and Two-Stage Review

Kubernetes uses OWNERS files to express code responsibility and splits review into two stages:

| Role | Focus |
| --- | --- |
| reviewer | Code quality, correctness, style, local implementation |
| approver | Overall acceptance criteria, compatibility, dependencies, APIs, and long-term impact |

The value of this design is separating the "people who look at the code" from the "people responsible for the module".

Enterprise teams can learn from this:

- Core directories must have owners
- The number of reviewers should be greater than approvers
- OWNER files should be maintained regularly
- People who leave the post or are no longer active should be removed from the owner list
- Automation can be responsible for assigning reviewers, checking labels, and prompting for missing approvals

If using GitHub, a simplified version can be implemented first using CODEOWNERS.

## 3. Linux Kernel: Maintainer Tree Model

The Linux Kernel's governance method is more like a multi-layered maintainer network.

Contributors submit changes to subsystem maintainers; maintainers verify, organize, and then send pull requests to higher-level maintainers.

Enterprise teams can learn from this:

- Large systems should not require a central team to review all code
- Subsystem leaders should take on first-level quality judgment
- Higher-level leaders focus on integration risks and release cadence
- Critical merges are best accompanied by signatures, tags, and change descriptions

Best suited for particularly large platforms or infrastructure teams.

## 4. Go: Gerrit and Strict Review Process

The Go project has long used Gerrit for code review.

Its inspiration is: when a project has very high requirements for compatibility, code quality, and historical cleanliness, the review tool can be a stronger constraint than an ordinary PR model.

Enterprises don't necessarily need to introduce Gerrit, but they can learn:

- Every change must have a clear change description
- Graded review permissions
- Combination of automated testing and manual review
- Maintain higher scrutiny standards for public APIs and standard library-level code

## 5. Rust: RFC and Major Change Process

Rust's RFC process works well for design changes with a wide impact.

Enterprise teams can simplify it into a lightweight ADR or design review:

```text
Background
Goals
Non-Goals
Proposal
Impact Scope
Alternatives
Risks
Unresolved Questions
Rollout and Revert
```

Scenarios where RFC/ADR applies:

- Changing public interfaces
- Changing data models
- Changing core workflows
- Changing team collaboration rules
- Introducing new infrastructure

Avoid requiring every small change to go through an RFC, otherwise the process will become too heavy.

## 6. Practices Enterprise Teams Can Land Directly

1. Use CODEOWNERS or OWNERS to express module responsibility
2. Split the reviewer and approver responsibilities
3. Raise review requirements for high-risk directories
4. Use lightweight ADRs for major changes
5. Use automation to prompt for missing owners, missing tests, and missing release notes
6. Periodically clean up the owner list and long-unaddressed PRs

## 7. Key Takeaways

The core of Git governance is responsibility boundaries.

Branch protection, CODEOWNERS, PR templates, CI, and Rulesets are just tools; ultimately, they must answer:

- Who understands this piece of code?
- Who has the right to approve this change?
- Who is responsible for the risks after merging?
- Which changes require a higher-level review?
