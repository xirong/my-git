# Git 2.45 to 2.54 Version Evolution Notes

English | [中文](../git-version-upgrade-notes.md)

Original links:

- [Highlights from Git 2.45](https://github.blog/open-source/git/highlights-from-git-2-45/)
- [Highlights from Git 2.46](https://github.blog/open-source/git/highlights-from-git-2-46/)
- [Highlights from Git 2.47](https://github.blog/open-source/git/highlights-from-git-2-47/)
- [Highlights from Git 2.48](https://github.blog/open-source/git/highlights-from-git-2-48/)
- [Highlights from Git 2.49](https://github.blog/open-source/git/highlights-from-git-2-49/)
- [Highlights from Git 2.50](https://github.blog/open-source/git/highlights-from-git-2-50/)
- [Highlights from Git 2.51](https://github.blog/open-source/git/highlights-from-git-2-51/)
- [Highlights from Git 2.52](https://github.blog/open-source/git/highlights-from-git-2-52/)
- [Highlights from Git 2.54](https://github.blog/open-source/git/highlights-from-git-2-54/)
- [Git BreakingChanges](https://git-scm.com/docs/BreakingChanges/2.51.0)
- [Git reftable documentation](https://git-scm.com/docs/reftable)
- [GitLab: What's new in Git 2.54.0](https://about.gitlab.com/blog/whats-new-in-git-2-54-0/)

## 1. Why Teams Should Pay Attention to New Git Versions

The Git commands used daily by most developers haven't changed much, but capabilities related to large repositories, CI, history rewriting, reference storage, security, and performance are constantly evolving.

Team leaders should focus on these areas in new Git versions:

- Large repository performance
- `sparse checkout` and `partial clone` experience
- Hooks and unified checks
- Underlying storage evolution like reftable
- SHA-256 migration preparation
- History rewriting and automated script capabilities

## 2. Most Valuable Changes for Engineering Teams

### reftable

reftable is the new backend direction for Git reference storage, used to improve performance and consistency in scenarios with massive refs.

Current suggestions:

- Pilot in non-critical repositories first
- Do not switch by default across the entire organization immediately
- Pay attention to Git 3.0 related BreakingChanges
- Before migrating, ensure the hosting platform, CI images, and developers' local Git versions all support it

### Continued Maturity of partial clone and sparse checkout

Large repository teams should continue to monitor:

- `git clone --filter=blob:none`
- `git sparse-checkout`
- Interactive add in sparse worktrees
- Trade-offs of different clone strategies in CI

These capabilities directly relate to the monorepo and large repository experience.

### config-based hooks

Git 2.54 introduced the config-based hooks direction, reducing the cost of sharing hooks across multiple repositories.

Its potential value to the team:

- Unified pre-commit checks
- Unified secret scan
- Unified commit message checks
- Configure different hooks by user, system, or repository

Things to note before implementation:

- Whether older Git versions support it
- Local hooks and CI checks must remain consistent
- Hooks can only provide early warnings and cannot replace CI and server-side rules

### `git history`

`git history reword` and `git history split` in Git 2.54 are in the experimental stage.

Use it to simplify some history rewriting tasks, like changing old commit messages or splitting commits.

Team usage suggestions:

- Only use for local, unpublished history
- Public branch history still requires caution
- When writing into troubleshooting manuals, note the Git version requirement
- At this stage, `git rebase -i` is still retained as the universal solution

## 3. Upgrade Strategy

### Personal Development Environments

Can be upgraded relatively quickly, but ensure compatibility with IDEs, GUI Git clients, and pre-commit tools.

### CI Images

The Git version in CI images is more critical.

If the documentation recommends partial clone, sparse checkout, or config hooks, you must confirm that the Git version in the CI image supports them.

### Enterprise Unified Rollout

Recommended order:

1. First, annotate command version requirements in documentation
2. Pilot in non-critical repositories
3. Upgrade CI images
4. Prompt for upgrades in developer toolchains
5. Then roll out to large or core repositories

## 4. Future Writing Notes for This Repository

When articles use new capabilities, state clearly:

- Minimum Git version
- Whether it is experimental
- Whether it affects public history
- Whether it requires hosting platform support
- Whether it works for long-term use in CI or by local developers

For example, do not use new commands like `git history` to directly replace all `rebase -i` tutorials.
