# Security and Secret Scanning

English | [中文](../security-and-secret-scanning.md)

Security governance must at least cover credential, dependency, and code scanning.

For regular teams, the easiest way to cause a major incident is by committing tokens, passwords, private keys, internal addresses, or production configurations into the repository.

## Recommended Checks

- Secret scanning
- Push protection
- Dependabot alerts
- Code scanning
- Dependency review

Use these capabilities as security checkpoints during the PR and push stages, in combination with branch protection, Rulesets, and CI. See [Enterprise GitHub Workflow Stack](enterprise-github-workflow-stack_en.md).

## What Secret Scanning Does

GitHub secret scanning scans for credential leak risks within the repository and generates alerts upon finding suspicious secrets.

The GitHub documentation states that secret scanning will scan the Git history of all branches in the repository.

The specific availability varies by repository type, organization plan, and GitHub security capabilities; rely on the repository settings page and official documentation for actual details.

## What Push Protection Does

Push protection identifies possible secrets when a developer pushes, preventing them from entering the remote repository.

This is more valuable than post-facto discovery because it intercepts risks before they enter the history.

## If a Secret Has Already Been Committed

The first step is always to revoke and rotate the secret.

Do not assume that deleting the file or reverting the commit makes you safe. Traces may have already been left in Git history, forks, caches, and logs.

Recommended workflow:

1. Immediately revoke the secret
2. Rotate to a new secret
3. Check access logs and confirm the scope of impact
4. Clean up the Git history
5. Notify the relevant owners
6. Add pre-commit scanning

For detailed processing, see [Remove Secret from History](../../06-troubleshooting/06-troubleshooting_en/remove-secret-from-history_en.md).

## Team Rules

- Prohibit committing `.env`, private keys, and tokens to the repository
- Provide `.env.example` for local development
- CI/CD should use platform secret management
- Add secret self-check items to PR templates
- Enable secret scanning and push protection for critical repositories

## Dependabot and Code Scanning

Dependabot turns dependency upgrades and GitHub Actions version upgrades into reviewable PRs.

Code scanning is suited for shifting left static security issues into PR or main branch checks, and assigning the issues to owners via alerts.

These two types of capabilities must be coordinated with CODEOWNERS, required checks, and processing SLAs; otherwise, they merely increase the volume of alerts.

## Further Reading

- [GitHub Docs: About secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/about-secret-scanning)
- [GitHub Docs: Enabling secret scanning features](https://docs.github.com/en/code-security/secret-scanning/enabling-secret-scanning-features)
- [GitHub security features](https://docs.github.com/en/code-security/getting-started/github-security-features)
- [Enterprise GitHub Workflow Stack](enterprise-github-workflow-stack_en.md)
- [Remove Secret from History](../../06-troubleshooting/06-troubleshooting_en/remove-secret-from-history_en.md)
