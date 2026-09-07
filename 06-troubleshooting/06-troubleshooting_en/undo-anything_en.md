# Undo Anything

English | [中文](../undo-anything.md)

Before undoing in Git, first determine the state of the changes.

Only three questions matter:

1. Have the changes been committed?
2. Has the commit been pushed?
3. Has anyone continued development based on it?

## Local Uncommitted Changes

Discard Working Tree changes for a tracked path whose ownership and disposal have been confirmed:

```bash
git restore --worktree -- <owned-path>
```

Unstage:

```bash
git restore --staged -- <owned-path>
```

Expand to the whole worktree only when every tracked edit belongs to you, has been checked path by path, and the owner authorizes discarding all of it:

```bash
git restore --worktree -- .
```

Check before executing:

```bash
git status --porcelain
git diff -- <owned-path>
git diff --cached -- <owned-path>
```

If status shows content with an uncertain source, another owner, or staged, unstaged, or untracked content that must be retained, stop rather than run restore, clean, or reset.

## Committed but Not Pushed

The following resets apply only to your own last commit that has not been pushed or used by collaborators. First require `git status --porcelain` to print nothing; existing staged content would share the Index with content left by `reset --soft`, so preserve the state or use a clean worktree first.

Amend the last commit:

```bash
git commit --amend
```

Undo the last commit, but keep changes in the staging area:

```bash
git reset --soft HEAD~1
```

Undo the last commit, and keep changes in the working tree:

```bash
git reset HEAD~1
```

## Pushed Public Commits

For public commits, prioritize using:

```bash
git revert <commit-sha>
```

This will add a reverse commit, keeping history clear without breaking collaborators' local branches.

## High-Risk Commands

These commands respectively rewrite local state, rewrite remote history, or delete untracked files. Confirm ownership with explicit paths and read-only checks first, then let the owner decide whether content may be discarded.

First run:

```bash
git status --porcelain
```

If `git status --porcelain` prints anything, stop and preserve the state. Only when the worktree is clean, `<verified-ref>` has been verified, and local history may really be rewritten, create a backup branch before reset:

```bash
git branch backup-before-undo HEAD
git reset --hard <verified-ref>
```

Preview untracked candidate paths separately:

```bash
git clean -nd
```

`git clean -nd` only lists candidates. Run `git clean -f -- <owned-untracked-path>` only after the owner confirms that exact untracked path may be discarded; do not turn the preview into `git clean -fd`. `git push --force` is a separate remote operation that also needs remote authorization, branch-rule, and collaborator confirmation.

## Further Reading

- [GitHub Blog: How to undo almost anything with Git](https://github.blog/open-source/git/how-to-undo-almost-anything-with-git/)
- [git restore Official Documentation](https://git-scm.com/docs/git-restore)
- [git revert Official Documentation](https://git-scm.com/docs/git-revert)
- [Git Troubleshooting Playbook](git-troubleshooting-playbook_en.md)
