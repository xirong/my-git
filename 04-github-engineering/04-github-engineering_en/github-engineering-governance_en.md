# GitHub Engineering Governance

English | [中文](../github-engineering-governance.md)

For modern engineering teams, GitHub has grown well beyond code hosting — it now spans collaboration, review, release, security, and governance.

## 1. Repository Governance Checklist

- Branch protection
- Required status checks
- Required review
- CODEOWNERS
- Rulesets
- Merge queue
- Secret scanning
- Dependabot
- Code scanning
- PR template
- Issue template
- Release process

For a more complete combination, see [Enterprise GitHub Workflow Stack](enterprise-github-workflow-stack_en.md).

## 2. Maturity Model

| Maturity | Should Have |
| --- | --- |
| L1 Personal Projects | README, LICENSE, basic directory descriptions |
| L2 Small Teams | PR, basic CI, branch protection |
| L3 Growing Teams | CODEOWNERS, Issue / PR templates, release process |
| L4 Mid-to-Large Teams | Rulesets, Merge Queue, security scanning |
| L5 Platform Teams | Unified repository standards, automated checks, metrics dashboards |

## 3. Baseline Configuration for Formal Teams

### Main branch protection

Recommended settings:

- Block direct pushes to the main branch
- Require a pull request before merging
- Require status checks to pass before merging
- Require all conversations to be resolved before merging
- Block deletion of the main branch
- Block force pushes by non-admin members

See the official GitHub documentation for [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

### Pull request template

Every PR template should require authors to fill in at least:

- What changed
- Why
- How tested
- Risk
- Rollback plan

See [Pull Request Template](../../08-templates/08-templates_en/pull-request-template_en.md) for a template.

### Basic CI

Include at least:

- lint
- unit test
- build

CI speed matters more as teams grow. Slow CI trains developers to ignore or bypass the rules.

Multi-repository teams should standardize on [Reusable Workflows](reusable-workflows_en.md) to share CI templates across repos, preventing the configuration drift that comes from copy-pasting per repository.

If your team already manages configuration, infrastructure, or release strategy through repositories, read [GitOps and Config as Code](gitops-and-config-as-code_en.md) next. Those practices extend PRs, reviews, CODEOWNERS, CI validation, and release audits beyond application code.

## 4. Configuration for Growing Teams

### CODEOWNERS

Assign owners to critical directories:

```text
/billing/ @team-billing
/auth/ @team-security
/.github/ @team-platform
```

The Kubernetes OWNERS model offers a more complete governance template: reviewers own code quality, approvers own overall acceptance. GitHub CODEOWNERS works as a lightweight alternative for enterprise teams — see [Open Source Project Git Governance Practices](../../09-resources/09-resources_en/open-source-governance-practices_en.md).

### Rulesets

Rulesets let you enforce rules on branch names, tags, and push behavior.

When multiple rulesets apply to the same target, GitHub enforces the strictest combination — see [about rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets).

### Security Checks

Recommended to enable:

- Secret scanning
- Dependabot alerts
- Code scanning

Feature availability varies by GitHub plan and repository type — check the official documentation and your repository's Settings page for what applies to you.

## 5. Advanced Configuration for Large Teams

### Merge Queue

Enable Merge Queue when PR volume is high and contention on the main branch becomes a bottleneck.

The classic scenario: each PR passes CI in isolation, but merging them in sequence breaks the main branch due to combined changes.

Merge Queue integrates with required status checks — see [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

### Repository Rule Baseline

Large organizations should define a unified baseline across all repositories:

- Default branch naming
- PR templates
- Issue templates
- Required CI items
- Secret scanning
- Dependency scanning
- Release note format
- CODEOWNERS rules

## 6. Common Mistakes

### Adding rules without investing in speed

Governance should not slow everyone down. The more rules you add, the stronger your automation needs to be, the faster CI needs to run, and the clearer your templates need to be.

### Protecting main but ignoring release branches

If your team uses `release/*` or `hotfix/*` branches, apply protection rules to those too.

### Making CODEOWNERS too granular

Over-granular ownership leaves PRs waiting for approval indefinitely. Start with critical directories and refine gradually as ownership patterns become clear.

### Enabling security scanning with no follow-through

Scanning surfaces issues — it does not resolve them. Make sure the team has defined owners, SLAs, and escalation paths before turning scanning on.

## Further Reading

- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Enterprise GitHub Workflow Stack](enterprise-github-workflow-stack_en.md)
- [GitOps and Config as Code](gitops-and-config-as-code_en.md)
- [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [Reusable Workflows](reusable-workflows_en.md)
- [Open Source Project Git Governance Practices](../../09-resources/09-resources_en/open-source-governance-practices_en.md)
- [GitHub code scanning merge protection](https://docs.github.com/en/code-security/concepts/code-scanning/merge-protection)
- [Issue and pull request templates](https://docs.github.com/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates)
- [GitHub secret scanning](https://docs.github.com/github/administering-a-repository/about-secret-scanning)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
