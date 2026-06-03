# Rulesets

English | [中文](../rulesets.md)

GitHub Rulesets are used to uniformly control branch, tag, and push behaviors.

They are more suited for organizational and repository-level unified governance than single branch protection rules.

## Suitable Scenarios

- Multiple branches require unified rules
- Multiple repositories within an organization require unified standards
- Requires enabling, pausing, and auditing of rules
- Needs to restrict specific paths, file sizes, or commit metadata
- Desires centralized management of branch rules and tag rules

## What Can Be Controlled

Common rules include:

- Restrict branch creation, updates, and deletion
- Require PRs for merging
- Require status checks to pass
- Require linear history
- Restrict force pushes
- Protect tags
- Set rules for specific paths

Different rule capabilities vary depending on the GitHub version and repository type; rely on the official documentation and settings page for actual details.

## Relationship with Branch Protection

Rulesets and Branch Protection can coexist.

The official GitHub documentation states that when multiple rulesets hit the same target, the rules will be aggregated.

New teams should start with Branch Protection first. Once there are many repositories and complex rules, gradually switch to Rulesets.

## Recommended Implementation Sequence

1. Protect `main` first
2. Then protect `release/*`
3. Then abstract into a ruleset
4. Then roll out to multiple repositories within the organization
5. Periodically audit whether rules are still valid

## Recommendations for Multi-Repository Teams

In scenarios like 40+ microservices, the value of Rulesets lies in unifying baselines:

- Default branches must go through PRs
- Required check names must remain consistent
- Prohibit regular members from deleting or force pushing critical branches
- Release branches and tags have separate rules
- High-risk repositories retain stricter configurations

Rulesets are suited for expressing unified rules, while specific differences within a repository still need clear explanations preserved.

Compared to traditional Branch Protection, Rulesets are more suited for multi-rule stacking, organizational baselines, and multi-repository governance. New teams can start with Branch Protection and migrate to Rulesets as the number of repositories grows.

## Further Reading

- [GitHub Docs: About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [GitHub Docs: Creating rulesets for a repository](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)
- [Reusable Workflows](reusable-workflows_en.md)
- [Branch Protection](branch-protection_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
