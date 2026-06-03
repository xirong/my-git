# Resolve Conflicts

English | [中文](../resolve-conflicts.md)

The key to resolving conflicts is to first understand the intent of both sides, then decide which side to keep or how to merge.

Do not mechanically choose `ours` or `theirs` just because you see conflict markers.

## What a Conflict Looks Like

```text
  <<<<<<< HEAD
Current branch content
  =======
Merged branch content
  >>>>>>> feature/login
```

You need to organize this content into the final desired state and delete the conflict markers.

## Conflicts During Merge

Check status:

```bash
git status
git diff
```

After resolving files:

```bash
git add <resolved-files>
git merge --continue
```

If things go wrong:

```bash
git merge --abort
```

## Conflicts During Rebase

Check status:

```bash
git status
git diff
```

After resolving files:

```bash
git add <resolved-files>
git rebase --continue
```

If things go wrong:

```bash
git rebase --abort
```

## Handling Advice

- First identify which business domain the conflicting file belongs to
- Identify what problems both sides are trying to solve
- Check commit history if necessary
- Run the minimal relevant tests after resolving
- When unsure, loop in the relevant owner

Check conflict sources:

```bash
git log --oneline --left-right --merge
```

## AI Programming Scenarios

AI is prone to just doing text splicing when handling conflicts.

Have AI explain the semantics of both sides, then let a human confirm the final result.

## Further Reading

- [GitHub Docs: Resolving a merge conflict using the command line](https://docs.github.com/en/get-started/using-git/resolving-merge-conflicts-after-a-git-rebase)
- [Atlassian: Merge conflicts](https://www.atlassian.com/git/tutorials/using-branches/merge-conflicts)
- [Git Troubleshooting Playbook](git-troubleshooting-playbook_en.md)
