# Submodule vs Subtree

English | [中文](../submodule-vs-subtree.md)

Common solutions for sharing code are submodule and subtree.

Both can incorporate external repository content into the current project, but their user experience and maintenance costs differ significantly.

## Submodule

Submodule allows the current repository to record a specific commit of another repository.

Suitable for:

- Needing to precisely reference an external repository version
- External repository has an independent lifecycle
- Current project does not want to directly copy external code

Common commands:

```bash
git submodule add <url> path/to/module
git submodule update --init --recursive
```

Disadvantages:

- New members easily forget to initialize
- Submodule state easily gets messed up after branch switching
- Need to review both parent and child repositories during PR review
- CI needs to correctly fetch submodules

## Subtree

Subtree merges external repository content into a subdirectory of the current repository.

Suitable for:

- Wanting users to be unaware
- External code update frequency is low
- Current repository wants to directly include the complete code

Common characteristics:

- Code is present immediately after clone
- No extra initialization needed
- Synchronization process with upstream/downstream is heavier
- History can become complex

## How to Choose

| Scenario | Recommendation |
| --- | --- |
| Third-party library maintained independently | submodule |
| Code shared internally within the team but needs to be simple for users | subtree |
| Core code that evolves together frequently | Consider monorepo or package management |
| Just reusing a small amount of code | Re-evaluate whether extracting a library is necessary |

## Engineering Advice

Do not introduce submodules prematurely merely for "reuse."

For many teams, submodule problems essentially stem from poorly designed code boundaries.

If shared code needs frequent modifications alongside the main repository, monorepos, package management, or directly merging modules might be more stable than submodules.

## Further Reading

- [Pro Git: Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [git submodule official documentation](https://git-scm.com/docs/git-submodule)
- [Atlassian: Git subtree](https://www.atlassian.com/git/tutorials/git-subtree)
- [Large Repository Git Practices](large-repo-git-practices_en.md)
