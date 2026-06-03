# Gerrit Code Review Governance Reference

English | [中文](../gerrit-code-review-governance.md)

Original links:

- [Gerrit Code Review: Access Controls](https://gerrit-review.googlesource.com/Documentation/access-control.html)
- [Go Contribution Guide](https://go.dev/doc/contribute)

## 1. Why Do We Need to Compare With Gerrit?

GitHub's advantages are platform experience and ecosystem integration.

Gerrit's advantages are finer-grained review and permission semantics, best suited for teams with strong processes, strict permissions, and rigorous scrutiny.

For enterprise teams, comparing the two helps in understanding the governance models behind different tools, avoiding simply picking a side.

## 2. Typical Characteristics of Gerrit

| Capability | Meaning |
| --- | --- |
| Group-level permissions | Permissions are usually granted to groups to avoid scattering them to individuals |
| Code-Review label | Review opinions can be graded, such as -2 to +2 |
| Submit permissions | Passing a Review and final submission can be separated |
| Service Users | Automated systems use dedicated identities |
| Project ACL | Projects, branches, and references can have fine-grained permissions |

This model is more like a review hub, best suited for organizations that require clear authorization and review levels.

## 3. Differences From GitHub

GitHub's more natural path is:

```text
branch -> pull request -> review -> status checks -> merge
```

Gerrit emphasizes more on:

```text
change -> labels -> votes -> submit requirements -> submit
```

GitHub is suitable as a unified development platform; Gerrit is suitable when treating code review as a strongly constrained process.

## 4. What Can Enterprise Teams Learn?

Even without using Gerrit, teams can borrow these ideas:

- Categorize review results; not all comments are equally important
- Separate final merge permissions from general review permissions
- Automated accounts should use dedicated identities
- High-risk branches and directories should use finer permissions
- Review records must be able to explain "who approved what"

## 5. Migration Inspiration for GitHub Teams

If a team uses GitHub, they can use these capabilities to simulate some Gerrit governance:

- CODEOWNERS to express path responsibility
- Branch Protection to require owner review
- Rulesets to unify organization-level rules
- Required status checks to fix automated checks
- Environment protection rules to control deployment approvals
- Merge Queue to verify the combined results of merges

## 6. Where to Add This

Add this comparison to:

- GitHub Engineering Governance
- Code Review Best Practices
- CODEOWNERS
- Rulesets
- Enterprise Collaboration Configuration Stack
