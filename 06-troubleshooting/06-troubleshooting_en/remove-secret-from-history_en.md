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

Then force push the cleaned history:

```bash
git push --force --all
git push --force --tags
```

## Note the Risks

History rewriting affects all collaborators; you must notify the team before execution and require everyone to resynchronize the repository.

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
