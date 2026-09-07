# Recovering from an Agent Incident: Preserve the Scene, Then Act on Evidence

English | [中文](../ai-agent-incident-recovery.md) | [Runnable lab](../../labs/ai-agent-incidents/README.md)

An agent can modify many files, create several commits, or leave a worktree behind in minutes. Recovery starts by preserving usable evidence: who changed what, where the change is recorded in Git, and whether someone else has already built on it.

This article covers accidental deletion or edits, undoing a group of commits, worktrees left after an agent exits, and a `.env` file or credential committed by mistake. It complements the [Git Troubleshooting Playbook](git-troubleshooting-playbook_en.md), [Recover Lost Commit](recover-lost-commit_en.md), and [Remove Secret from History](remove-secret-from-history_en.md); it does not repeat the full Git object, reflog, or worktree model.

## At the incident: stop writes and record four locations separately

Stop the agent, terminal command, formatter, and generator that can still write to the directory. Do not start with `restore`, `clean`, `reset`, `stash`, or worktree deletion. Then run these read-only checks in the affected working directory:

```bash
git status --short
git diff --name-status
git diff --cached --name-status
git ls-files --others --exclude-standard
git rev-parse --verify HEAD
git log --oneline --decorate -10
git reflog -20
```

The output establishes four separate states:

| Location | Record | Do not do first |
| --- | --- | --- |
| `HEAD` | committed baseline and branch target | guess `HEAD~1` from memory |
| Index | staged, uncommitted draft | unstage everything |
| Working Tree | tracked edits not staged | restore the entire directory |
| untracked files | files Git does not track | bulk-delete with `clean` |

Record the command output, path, agent task identifier, and known owners. While content still exists, follow team policy to copy it to a protected location outside the repository, or ask its owner to confirm it in place. The copy operation must also avoid overwriting evidence.

`reflog` records Git events such as reference movements and can locate commits that were previously resolvable. **It cannot recover edits that were never saved as Git objects.** If an agent removed a file that existed only in the working tree and was not staged, committed, or backed up elsewhere, check editor local history, filesystem backups, or auditable agent output. A non-empty reflog is not evidence that every uncommitted line has a recovery point.

## Undoing a group of Agent commits: prove the range before choosing the workflow

Establish whether every intended commit came from the incident, their order, the baseline, and whether the range contains someone else's work. Replace `<agent-base>` and `<agent-tip>` with values from the inspected history:

```bash
git log --oneline --decorate <agent-base>..<agent-tip>
git diff --name-status <agent-base>..<agent-tip>
git merge-base --is-ancestor <agent-base> <agent-tip>
git branch --contains <agent-tip>
git branch -r --contains <agent-tip>
```

These commands first provide local Git evidence. `git branch -r --contains` only inspects remote-tracking refs already present on this machine. An empty result can arise from stale cache, a ref that was never fetched, or remote branch deletion or rename. It cannot establish that a commit was never pushed or that no collaborator used it. Before classifying work as unshared, identify the authoritative remote, fetch that remote’s relevant refs at an appropriate authorized time, and combine the refs with PR, task, and collaborator records. This article does not automatically fetch a real remote.

Use `<agent-base>..HEAD` only after confirming every commit in that interval belongs to the same incident. If the interval includes a human repair, other agent work, or a merge commit, use an explicit list of verified commit SHAs. Do not roll back a mixed interval for convenience.

### Unshared commits: retain a recovery ref, then move only the owned branch

The following fits a clean, agent-owned local branch where commits are contiguous from base to tip and confirmed unshared through the authoritative remote refs, PR/task records, and collaborator records. An empty `git branch -r --contains` result does not meet that condition. When unshared status cannot be established, treat the work as shared: create precise `revert` commits and do not enter the `reset --hard` flow. Once the condition is established:

```bash
git status --short
git log --oneline <agent-base>..HEAD
git branch recovery/before-agent-reset HEAD
git reset --hard <agent-base>
```

`reset --hard` makes the Index and Working Tree match `<agent-base>`. If status contains staged, unstaged, or untracked content that must be retained, stop before the command, preserve the scene, or use a separate worktree. `recovery/before-agent-reset` is a local recovery anchor, not a remote backup.

### Shared commits: make inverse commits and preserve public history

When commits were pushed, entered a PR, were fetched by others, or may be a later baseline, prefer `revert` commits on the agreed branch. List the verified agent commits explicitly from newest to oldest:

```bash
git status --short
git revert --no-edit <agent-last-sha> <agent-middle-sha> <agent-first-sha>
git log --oneline -6
git diff <agent-first-sha>^..HEAD
```

This creates new inverse commits while allowing collaborators to keep synchronizing the same history. The relevant owner controls pushing, PRs, branch rules, and release action. A successful local revert proves that Git created inverse patches. Run affected business tests and assess databases, queues, external calls, and released artifacts separately.

A revert conflict means Git cannot mechanically retain later edits and undo the target at once. Inspect the conflict. If the semantic decision is not made, return to the state before the revert:

```bash
git status
git diff
git revert --abort
```

To continue, have the owner of the business behavior decide which later changes survive, resolve the conflict, test, and record the observed result. Do not delete conflict markers and commit, and do not mix unrelated edits into an inverse commit with `--no-commit`.

## A worktree left after an Agent exits: check processes and preserve the scene

The end of an agent session does not establish that no process still writes its directory. Preserve the directory first, then ask the task runner, terminal owner, or known process record whether an agent, test, editor Git operation, or generator remains active. Record the state of each worktree:

```bash
git worktree list --porcelain
git -C <worktree-path> status --short
git -C <worktree-path> diff --name-status
git -C <worktree-path> diff --cached --name-status
git -C <worktree-path> ls-files --others --exclude-standard
```

`git worktree list` lists worktrees known to Git. It does not prove that no process is still writing files. Preserve an unknown edit or process along with the branch name and captured output, then let the relevant owner decide.

### The boundaries of lock, prune, and remove

| Command or state | Purpose | Incident decision |
| --- | --- | --- |
| `git worktree lock <path>` | marks the worktree's administrative record so `prune` does not discard it when the directory is temporarily unavailable | useful while waiting for an owner or removable media; record reason and owner |
| `git worktree unlock <path>` | removes that protection | use only after confirming the directory and its edits need no further preservation |
| `git worktree prune` | removes stale administrative records for directories that no longer exist | it cannot establish whether uncommitted work in a missing directory was preserved; complete scene checks first |
| `git worktree remove <path>` | removes a linked worktree directory and its record | use only for a confirmed-clean directory that is no longer needed; normal mode performs safety checks |

Do not manually delete `.git/worktrees/.../locked`, and do not use `git worktree remove --force` to bypass dirty-worktree or lock protection. The first action can desynchronize metadata and directories; the second can discard the original location of edits that need preservation. After a directory was moved or truly removed, run `git worktree prune` only once its branch, uncommitted content, and owner are confirmed unnecessary.

For shared objects and separate HEAD and Index state, see [Worktree for AI Agents](../../05-ai-native-development/05-ai-native-development_en/worktree-for-ai-agents_en.md) and [Git Mental Model 09: Worktree](../../01-getting-started/01-getting-started_en/git-mental-model-09-worktree_en.md).

## A `.env` file or secret entered a commit: invalidate the credential first

When a credential enters a commit, PR, log, or artifact, use this priority order:

1. Disable, revoke, or rotate it with the issuing provider, and ensure the replacement does not retain old access.
2. Limit further spread: stop automation that uses it and record known commits, remotes, branches, tags, PRs, artifacts, and logs.
3. Notify security and repository owners; assess access logs, forks, caches, and downstream systems by the known impact scope.
4. Only then handle Git history and platform-scanning results within authorized scope.

`git revert` only removes the text from a new branch tip. History rewriting cannot retract a secret already cloned, copied, cached, logged, or captured. See [Remove Secret from History](remove-secret-from-history_en.md) for the remote scope, `git filter-repo`, and collaborator recovery; see [Security and Secret Scanning](../../04-github-engineering/04-github-engineering_en/security-and-secret-scanning_en.md) for repository prevention.

Do not paste the complete credential into incident records, terminal output, or screenshots. Credential type, issuer, invalidation time, related commit SHA, and handling owner support later review without extending exposure.

## Runnable lab and next step

The [Agent Incident Recovery Lab](../../labs/ai-agent-incidents/README.md) performs real Git operations in a marked temporary directory:

- an owned, unshared set of commits is moved back locally after retaining a recovery ref;
- two Agent commits pushed to a local bare remote are reverted by verified SHA, while a human commit between them remains;
- a conflicting `git revert` is followed by `git revert --abort`, returning to the pre-conflict commit and file content;
- ordinary removal rejects a dirty worktree, while a lock retains stale worktree metadata through `prune` until it is unlocked.

The lab does not touch this repository's Git history, use a real secret, or prove recovery in GitHub, external backups, or production data. To connect an agent change's candidate SHA, business tests, and integration result in CI, continue with [CI for AI-Generated Changes](../../05-ai-native-development/05-ai-native-development_en/ci-for-ai-generated-changes_en.md).

## Further reading

- [Git Troubleshooting Playbook](git-troubleshooting-playbook_en.md)
- [Recover Lost Commit](recover-lost-commit_en.md)
- [Undo Anything](undo-anything_en.md)
- [Remove Secret from History](remove-secret-from-history_en.md)
- [AI Change Review Example](../../05-ai-native-development/05-ai-native-development_en/ai-change-review-example_en.md)
- [Engineering change course entry](../../05-ai-native-development/05-ai-native-development_en/engineering-change-course_en.md)
- [git worktree documentation](https://git-scm.com/docs/git-worktree)
- [git revert documentation](https://git-scm.com/docs/git-revert)
