# Git Mental Model 07: Rebase Replays Changes onto a New History

English | [中文](../git-mental-model-07-rebase.md) | [Interactive demo](https://xirong.github.io/my-git/interactive/git-mental-model/rebase-and-replay.html?lang=en) | [Runnable lab](../../labs/git-mental-model/07-rebase/README.md)

After an upstream branch advances, why can `git rebase` preserve code changes while commit IDs change? Rebase does not move an old commit to a new location. It selects the changes to retain, creates replay commits with new parent relationships, then updates the branch ref.

This chapter answers five questions:

1. How does rebase select changes from an old fork point and replay them one by one?
2. Under which conditions are new commits created, and when are they not?
3. How do old objects, backup refs, reflogs, and the new branch tip relate?
4. During a conflict, how can you identify the change being replayed, and why do ours/theirs have a different view from a regular merge?
5. How should a team coordinate and validate before rewriting an already shared branch?

## Start with the causal model

At the start, `topic` and `main` diverge at `B`:

```text
          T1---T2  topic
         /
...---B---U1---U2  main
```

Run this while on `topic`:

```bash
git rebase main
```

Git identifies the commits on `topic` that should be retained relative to `main`, temporarily starts from `main`, applies those changes in order, then updates `topic` to the result tip:

```text
...---B---U1---U2  main
                 \
                  T1'---T2'  topic

          T1---T2  old objects remain findable through a backup ref or reflog
```

`T1'` and `T1` can have the same file-level change, but their parent changes from `B` to `U2`. A commit records a tree, parent, author, committer, and other data. When Git creates a new object, its object ID follows that object content. Rebase rewrites the history named by a branch ref; it does not mutate an existing commit object in place.

The official documentation describes this as listing the current branch's commits that have no equivalent upstream commit, checking out the upstream, replaying the commits in order, and updating the branch ref.

## When a rebase creates a new commit

“Every rebase changes every commit ID” is inaccurate. First establish whether Git actually creates a replay commit:

| Condition | Result |
| --- | --- |
| The current branch has a non-equivalent commit to retain relative to the new upstream, and Git replays it successfully | Git creates a replay commit; the new parent relationship makes it a new object |
| The current branch already sits at the upstream, or no commits are eligible for replay | No replay commit is created; the ref can stay unchanged |
| Upstream already contains a recognizable equivalent clean cherry-pick | Default rebase skips that commit; options such as `--reapply-cherry-picks` change this handling |
| An interactive rebase drops, combines, edits, or reorders commits | The todo list controls the result; retained replayed changes form new objects and dropped entries do not occur in the result history |

Object-ID changes come from new objects that are actually created, not from the word `rebase` in a command. Automation should compare parents, trees, commit ranges, and refs instead of assuming every invocation rewrites every ID.

## Old objects and refs: keep a readable comparison point first

Branch names are movable refs. Create an explicit backup ref so that the old history still has a stable name after the operation:

```bash
git switch topic
git branch backup/topic-before-rebase topic
git rebase origin/main
```

After a successful replay, inspect old and new histories together:

```bash
git log --graph --oneline --decorate --all
git show backup/topic-before-rebase
git show topic
git reflog show topic
```

`backup/topic-before-rebase` keeps the old tip reachable for review and recovery. A reflog commonly records ref movement too, but expiry and repository maintenance policy affect it. An explicit backup ref is clearer when a reliable comparison is needed.

## Real experiment: one new object, one no-replay run, and one conflict

The lab creates an isolated temporary repository. It disables system and global Git configuration, sets a temporary identity, disables signing, and isolates hooks. It does not modify this project:

```bash
cd labs/git-mental-model/07-rebase
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
```

It preserves three real outcomes at once:

```text
replay-topic            points to a new commit after a successful replay
replay-topic-original   explicitly names the old commit, which remains readable
no-replay               is already at the upstream tip and has no commit to replay
topic                   is rebasing onto upstream; its second commit produces a content conflict
```

`verify.sh` asserts:

```text
replay-topic-original has replay-base as its parent
replay-topic has replay-upstream as its parent
the two commit IDs differ while topic.txt content is the same
no-replay, no-replay-before, and replay-upstream name the same commit
the topic conflict has UU app.txt in the working tree and index stages 1, 2, and 3
```

This demonstrates two boundaries: a successful replay creates a new object, while a rebase with no eligible commits creates none.

To preserve and inspect the lab state:

```bash
cd "$lab_path"
git log --graph --oneline --all --decorate
git show --no-patch --format=raw replay-topic-original
git show --no-patch --format=raw replay-topic
git status --short
git rebase --show-current-patch
git ls-files --unmerged -- app.txt
```

Remove only the temporary repository marked for this lab:

```bash
bash cleanup.sh "$lab_path"
```

Create, assert, verify abort, and clean up in one run:

```bash
bash test.sh
```

See [expected.txt](../../labs/git-mental-model/07-rebase/expected.txt) for the full expected state.

## A rebase conflict: read the change being replayed first

The topic in this lab has two commits. The first, which creates `topic-note.txt`, already replayed onto `upstream`. The second changes `app.txt` to `owner=topic` and conflicts with upstream's `owner=upstream`. Inspect it with:

```bash
git status --short
git rebase --show-current-patch
git ls-files --unmerged -- app.txt
git show :1:app.txt
git show :2:app.txt
git show :3:app.txt
```

The lab's output means:

| Index stage | Content | Meaning during this rebase conflict |
| --- | --- | --- |
| 1 | `owner=base` | The three-way merge base |
| 2 | `owner=upstream` | Ours: the replay result based on `upstream` |
| 3 | `owner=topic` | Theirs: the old topic commit currently being replayed |

In a regular merge, stage 2 is usually the current branch `HEAD` and stage 3 is `MERGE_HEAD`. Rebase applies working-branch commits on top of upstream, so ours here is the so-far-rebased series combined with upstream and theirs is the working-branch commit being applied. Before using `git checkout --ours` or `git checkout --theirs`, read the stage contents instead of relying on the words alone.

Resolve the conflict with:

```bash
# Edit app.txt and select the result that matches the real contract.
git add app.txt
git rebase --continue
```

`git add` returns the conflicted path to stage 0. `git rebase --continue` then attempts later replays. If a commit's change is confirmed to be unnecessary, first understand that skipping removes it from the final history, then use `git rebase --skip`.

## Internal state is for observation, not a cross-version script contract

A rebase backend can use `rebase-merge` or `rebase-apply` in Git's directory to record temporary state. For teaching observation, ask Git for the possible paths:

```bash
for backend in rebase-merge rebase-apply; do
  state_dir=$(git rev-parse --git-path "$backend")
  test -d "$state_dir" && printf 'active backend state: %s\n' "$state_dir"
done
```

The actual directory depends on backend, version, and options. Stable inspection entry points are `git status --short`, `git rebase --show-current-patch`, `git ls-files --unmerged`, and the index-stage content. The lab does not use a fixed internal directory as an assertion condition.

## The safety boundary of abort

Before starting a rebase, inspect and preserve the work state:

```bash
git status --short
git branch backup/topic-before-rebase topic
git rebase origin/main
```

When that clean precondition holds and you decide to abandon the operation:

```bash
git rebase --abort
```

`test.sh` actually runs this command and confirms that `topic` returns to `topic-original`, the working tree becomes clean, and `REBASE_HEAD` disappears. That result covers the lab's clean-start scope. Mixing extra uncommitted edits into a rebase before it starts or while resolving conflicts broadens recovery difficulty; preserve those edits first, then choose abort or continue.

## Shared history: coordinate before the command

The author can replay a private local topic independently. Once a branch is pushed, or someone has developed from its old commits, a rewrite changes their common ancestor and later operation paths. Establish sharing state and project policy before rewriting history.

A common controlled sequence is:

```bash
git fetch origin
git switch topic
git status --short
git branch backup/topic-before-rebase topic
git rebase origin/main
# Run the affected project's build, tests, and review.
git push --force-with-lease origin topic
```

`--force-with-lease` requires the remote ref to retain the value that the local repository expects, and fails if another commit advanced it. It reduces accidental overwrite risk; it does not replace collaboration notice, review, or behavior validation. A background fetch can also affect lease checks without an explicit expected value, so important shared branches should follow the team's defined remote-update process.

| Branch state | First decision |
| --- | --- |
| Local only, used by its author | Rebase after creating a backup ref, then validate the result |
| Pushed, with no other work based on the old tip | Notify relevant people, then use the project-approved controlled push method after replaying |
| Used as a base by others or assigned a release role | Coordinate a shared migration; merge, an appended revert, or a new branch is often easier to recover than direct rewriting |

## Change-the-condition prediction

Given:

```text
          T1  topic
         /
...---B---U1  main
```

1. Why is the successful `git rebase main` result commit different from `T1`?
2. If `topic` already equals `main`, must the same command create a new commit?
3. If upstream already has an equivalent clean cherry-pick of `T1`, what may default rebase do?

Answers:

1. The new result has `U1` as its parent, so Git creates another commit object.
2. No. With no commits to replay, Git can leave the ref unchanged.
3. Git can recognize that the change is already upstream and skip it by default. If that replay behavior must be retained, select the relevant option explicitly and inspect the resulting history.

## Agent judgment question

An agent plans to rebase a pushed `topic` and says, “The code diff is small, so `git push --force` is fine.” Which action set follows an auditable collaboration workflow?

```text
A. Force-push directly as long as local tests pass
B. Confirm whether anyone built on the old tip, create a backup ref, validate affected behavior after rebase, then use force-with-lease or coordinate migration according to project policy
C. Check only whether commit IDs changed
```

Choose B. The size of a code diff says nothing about the impact of ref rewriting on collaborators. A backup ref supports review and recovery, affected validation checks replayed behavior, and a remote lease provides only part of the concurrency protection.

## Common misconceptions

### “Rebase modifies the old commit”

The old commit object remains unchanged. When replay is needed, rebase creates new objects and updates the branch ref to a new tip.

### “Every rebase changes every commit ID”

Only replay commits that Git actually creates have new IDs. When no commits are eligible, or a commit is recognized as already upstream, the result history can have no corresponding new object.

### “Ours during rebase means the same thing as ours during a regular merge”

Rebase applies working-branch changes on top of upstream. Stage 2 represents the replay result based on the new upstream, and stage 3 represents the working-branch commit being applied. Read the actual content before choosing a resolution strategy.

### “Abort unconditionally preserves all temporary edits”

The recovery result of `git rebase --abort` depends on the working-tree state before and during the operation. Start clean, explicitly preserve extra edits, then abort with a clear recovery boundary.

## Further reading

- [git rebase documentation](https://git-scm.com/docs/git-rebase)
- [git push documentation: force-with-lease](https://git-scm.com/docs/git-push)
- [git merge-base documentation](https://git-scm.com/docs/git-merge-base)
- [Chapter 06: Merge Starts with a Common Ancestor](git-mental-model-06-merge_en.md)
