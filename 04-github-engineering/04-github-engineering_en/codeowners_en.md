# CODEOWNERS

English | [中文](../codeowners.md)

CODEOWNERS is used to declare which individuals or teams are responsible for reviewing specific paths.

When a PR modifies specific paths, GitHub can automatically request a Review from the corresponding owner. When combined with branch protection, it can also require approval from the respective owner before merging.

## Where to Place the File

GitHub supports placing the `CODEOWNERS` file in these locations:

```text
.github/CODEOWNERS
CODEOWNERS
docs/CODEOWNERS
```

Place it at `.github/CODEOWNERS`, together with repository collaboration templates.

## Example

```text
# Default owner
* @team-platform

# Platform engineering
/.github/ @team-platform
/scripts/ @team-platform

# Business modules
/billing/ @team-billing
/auth/ @team-security
/docs/ @team-docs
```

## Recommended Rules

- Cover critical directories first
- Owners must have real response capabilities
- Do not assign all paths to a single person
- Team owners are more stable than individual owners
- Regularly clean up owners who have departed or changed roles
- Require code owner review in conjunction with branch protection

## Learning from Kubernetes OWNERS

The Kubernetes OWNERS file separates reviewers and approvers:

- Reviewers focus on code quality, correctness, style, and local implementations
- Approvers focus on compatibility, APIs, dependencies, and overall acceptance criteria

GitHub CODEOWNERS does not have these two semantic layers built-in, but enterprise teams can simulate them in their processes:

- CODEOWNERS point to the module's responsible team
- Regular reviewers perform code-level Review first
- Owners finally confirm boundaries, risks, and long-term maintenance costs

## Common Issues

### 1. Owner lacks write access

GitHub requires users or teams listed as code owners to have write access to the repository; otherwise, it will not work as expected.

### 2. Team is not visible

If using a team as an owner, team visibility and permissions must also be configured correctly.

### 3. Rules are too granular

Overly granular rules can cause PRs to be blocked by too many people. Cover critical directories first and then gradually expand.

## Further Reading

- [GitHub Docs: About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [GitHub Docs: About pull request reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)
- [Open Source Project Git Governance Practices](../../09-resources/09-resources_en/open-source-governance-practices_en.md)
- [Gerrit Code Review Governance Reference](../../09-resources/09-resources_en/gerrit-code-review-governance_en.md)
- [GitHub Engineering Governance](github-engineering-governance_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
