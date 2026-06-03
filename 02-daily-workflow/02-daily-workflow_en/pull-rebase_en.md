# Pull Rebase

English | [中文](../pull-rebase.md)

`git pull --rebase` is used to fetch remote updates and reapply local commits on top of the latest remote commits.

It is frequently used on personal feature branches, with the goal of reducing meaningless merge commits and making the history more linear.

## What a Normal Pull Does

`git pull` is roughly equivalent to:

```bash
git fetch
git merge
```

If both your local branch and the remote branch have new commits, a normal pull might produce a merge commit.

## What pull --rebase Does

```bash
git pull --rebase origin main
```

Is roughly equivalent to:

```bash
git fetch origin
git rebase origin/main
```

It will first get the remote updates, and then place your local commits after the latest remote commits.

## Suitable Scenarios

- Personal feature branches
- Local commits have not yet been pushed
- The team prefers a linear history
- You want to reduce merge commits when syncing with the main branch

## Unsuitable Scenarios

- The current branch is a shared branch among multiple people
- Your local commits have already been built upon by others
- You do not understand the impact of rebase
- The current branch has complex conflicts and lacks a backup

## Recommended Workflow

```bash
git status
git stash push -u -m "backup before pull rebase"
git pull --rebase origin main
git stash apply
```

If conflict resolution gets messy:

```bash
git rebase --abort
```

## Further Reading

- [GitHub Docs: About Git rebase](https://docs.github.com/en/get-started/using-git/about-git-rebase)
- [git pull official documentation](https://git-scm.com/docs/git-pull)
- [git rebase official documentation](https://git-scm.com/docs/git-rebase)
- [Rebase vs Merge](rebase-vs-merge_en.md)
