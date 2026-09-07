# Remove Secret from History

English | [中文](../remove-secret-from-history.md)

After committing a secret into Git history, the first step is always to revoke and rotate the keys.

Cleaning up history only reduces further exposure; it cannot make an already leaked secret secure again.

## Immediate Action

1. Revoke the secret
2. Rotate to a new secret
3. Confirm access logs and scope of impact
4. Notify related owners
5. Clean up Git history

## Clean Up History

Use `git filter-repo`:

```bash
git filter-repo --path path/to/secret-file --invert-paths
```

Run this first in a dedicated clone with no pending local edits. Confirm that `path/to/secret-file` is the real exposed path, and have the security owner and repository owner explicitly identify the affected remote, branches, tags, branch rules, and collaborator recovery plan.

The following force pushes apply only after confirming that every branch and tag on that remote needs the rewritten history. `<affected-remote>` is the verified remote name:

```bash
git push --force --all <affected-remote>
git push --force --tags <affected-remote>
```

## Note the Risks

History rewriting affects all collaborators. Before execution, notify the team and require everyone to resynchronize according to the agreed recovery plan. This procedure is for an exposed-secret incident only; routine history cleanup must not expand into force pushes of every branch and tag.

## After Cleanup

- Check GitHub secret scanning or similar scanning results
- Clean up leaked content in forks and caches
- Add pre-commit scanning
- Document preventive actions in the incident post-mortem

## Further Reading

- [GitHub Docs: Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [GitHub Docs: About secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/about-secret-scanning)
- [git filter-repo](https://github.com/newren/git-filter-repo)
- [Security and Secret Scanning](../../04-github-engineering/04-github-engineering_en/security-and-secret-scanning_en.md)
