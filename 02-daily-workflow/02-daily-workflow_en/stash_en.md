# Stash

English | [中文](../stash.md)

`git stash` is used to temporarily save uncommitted changes.

Use it when you have unfinished code but need to switch branches, pull code, or fix a hotfix right now.

## Suitable Scenarios

- Current changes are not yet ready to commit
- Temporarily need to switch to another branch
- Want to preserve the current state before a pull / rebase
- Want to quickly create a local checkpoint

## Basic Usage

Save current changes, including untracked files:

```bash
git stash push -u -m "wip: describe current work"
```

View the stash list:

```bash
git stash list
```

Apply a specific stash, but keep the stash record:

```bash
git stash apply stash@{0}
```

Apply and delete the stash:

```bash
git stash pop
```

Delete a specific stash:

```bash
git stash drop stash@{0}
```

## Choosing Between apply and pop

For important changes, prioritize using `apply`.

`pop` deletes the stash after a successful apply. If a conflict occurs during apply, recovering cleanly is harder.

A safer workflow:

```bash
git stash apply stash@{0}
git status
git diff
git stash drop stash@{0}
```

## Common Misconceptions

### 1. Treating Stash as Long-Term Storage

Stash is meant for temporary saving, not for long-term storage of important work.

Important work should be committed to a distinct branch as soon as possible.

### 2. Forgetting to Save Untracked Files

By default, `git stash` might not save untracked files. Use:

```bash
git stash push -u
```

### 3. Not Cleaning Up When Stashes Accumulate

When there are too many stashes, it is hard to know what each save point is for.

Add `-m` every time to explain the purpose.

## Further Reading

- [git stash official documentation](https://git-scm.com/docs/git-stash)
- [Pro Git: Stashing and Cleaning](https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning)
- [Atlassian: git stash](https://www.atlassian.com/git/tutorials/saving-changes/git-stash)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
