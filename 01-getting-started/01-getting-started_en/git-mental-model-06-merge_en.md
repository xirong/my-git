# Git Mental Model 06: Merge Starts with a Common Ancestor

English | [中文](../git-mental-model-06-merge.md) | [Interactive demo](https://xirong.github.io/my-git/interactive/git-mental-model/three-way-merge.html?lang=en) | [Runnable lab](../../labs/git-mental-model/06-merge/README.md)

Two people start from the same code. Why does Git need a common ancestor, and why does one merge merely move a branch ref while another creates a commit? Comparing only the two branch tips is insufficient. Git also needs the snapshot from which the histories diverged so that it can determine what each side changed.

This chapter answers five questions:

1. How does a common ancestor define the comparison boundary for a three-way merge?
2. What do `base`, `ours`, and `theirs` mean in a regular merge?
3. Why do fast-forwarding and a merge commit produce different history shapes?
4. What do content conflicts and semantic conflicts each fail to decide?
5. How do index stages 1, 2, and 3 support an evidence-based resolution?

## Start with the causal model

Let `B` be the common ancestor of the current branch and the branch being merged:

```text
          F1---F2  feature
         /
...---B---M1---M2  main (HEAD)
```

A regular three-way merge compares three snapshots:

```text
base   = B   the version both sides inherited before divergence
ours   = M2  the current HEAD version
theirs = F2  the version from the branch being merged
```

Git uses the `base -> ours` and `base -> theirs` changes to construct a result. Read the common ancestor directly with:

```bash
git merge-base main feature
```

Two commits can have multiple equally good common ancestors, such as after criss-cross merges. `git merge-base --all` lists every candidate. Without `--all`, do not treat one printed object ID as the sole possible candidate. For an everyday two-branch merge, establish that the reported commit is reachable from both sides.

## `base`, `ours`, and `theirs` in a regular merge

During a content conflict, Git retains more than working-tree conflict markers. The index temporarily stores three versions:

| Index stage | Content source | Meaning in the graph |
| --- | --- | --- |
| 1 | merge base | `B` |
| 2 | current `HEAD` | `ours`, or `M2` |
| 3 | `MERGE_HEAD` | `theirs`, or `F2` |

Inspect them while a regular merge is still in progress:

```bash
git status --short
git merge-base HEAD MERGE_HEAD
git ls-files --unmerged
git show :1:conflict.txt
git show :2:conflict.txt
git show :3:conflict.txt
```

The `:1:`, `:2:`, and `:3:` forms read objects from the index. They complement the conflict markers in the working tree. After editing the working-tree file, run:

```bash
git add conflict.txt
git merge --continue
```

`git add` replaces the three higher-stage entries with a stage-0 entry containing the resolution. The merge can create its result commit only after every conflicted path returns to stage 0.

Chapter 03 introduced the index as the next commit draft. Here it has a second role during a conflict: it preserves the three candidate inputs to the merge. [Return to the Index chapter](git-mental-model-03-index_en.md).

## Fast-forward or merge commit: ref movement versus a new graph object

### Fast-forward

When the current branch is an ancestor of the branch being merged:

```text
main:    B
feature: B---F1---F2
```

Git can move `main` directly to the existing `F2`:

```bash
git switch main
git merge --ff-only feature
```

```text
main, feature: B---F1---F2
```

No new commit is made. `--ff-only` requires this shape and exits non-zero when the histories have diverged, which makes it useful for encoding an expected history shape in a script. The default `--ff` fast-forwards when possible; `--no-ff` creates a merge commit even when a fast-forward is possible.

### A merge commit for divergent histories

When both sides contain commits after their common ancestor:

```text
          F1---F2  feature
         /         \
...---B---M1---M2---R  main
```

`R` is a new merge commit with two parents: the previous current-branch tip `M2` and the merged tip `F2`. It joins the histories and records the merged snapshot.

```bash
git switch main
git merge feature
git show --no-patch --format=raw HEAD
```

To inspect a merge result before creating its commit:

```bash
git merge --no-ff --no-commit feature
git diff --cached
git status --short
```

A fast-forward has no merge commit, so `--no-commit` alone cannot pause before it. `--no-ff --no-commit` creates an inspectable stopping point. Finish with `git commit`; abandon this merge with `git merge --abort`.

Before beginning, make the index agree with `HEAD` and preserve uncommitted work. The Git documentation warns that starting a merge with complex uncommitted changes can prevent `git merge --abort` from fully reconstructing the earlier state.

## What content and semantic conflicts each tell you

A content conflict means Git cannot mechanically choose a result for one overlapping text area. It commonly occurs when both sides modify the same line or overlapping hunks. Conflict markers require a human to decide the final content, and the result still needs tests.

A semantic conflict can have no conflict markers. The branches edit different files or code areas, Git merges the text successfully, yet the combined interfaces, configuration, permissions, or behavior no longer meet their agreement. A clean merge proves that Git constructed a file snapshot. It does not prove that the snapshot builds, passes tests, or satisfies a product rule.

This chapter's lab provides a reproducible counterexample:

```text
semantic-server  changes server protocol and port to https / 8443
semantic-client  changes the client address to http://service:8443
semantic-result  cleanly merges the two different-file changes
```

The lab reads files from the real Git tree of `semantic-result` and runs a standard-library Python check. It expects `https://service:8443`, receives `http://service:8443`, and exits with status `1`. That is a real failed behavior check, not a prose-only conflict.

## Run the real experiment

The lab creates an isolated temporary repository. It disables system and global Git configuration, sets a temporary identity, disables signing, and isolates hooks. It does not modify this project:

```bash
cd labs/git-mental-model/06-merge
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
```

The key assertions in `verify.sh` are:

```text
ff-target       names the same commit as fast-forward; that commit has one parent
merge-result    has two parents
semantic-result has two parents; its behavior check exits with status 1
main            is at UU conflict.txt; the index has stages 1, 2, and 3
```

To preserve the lab state and inspect it:

```bash
cd "$lab_path"
git log --graph --oneline --all --decorate
git show --no-patch --format=raw merge-result
git status --short
git merge-base HEAD MERGE_HEAD
git ls-files --unmerged -- conflict.txt
git show :1:conflict.txt
git show :2:conflict.txt
git show :3:conflict.txt
```

When finished, remove only the temporary repository marked for this lab:

```bash
bash cleanup.sh "$lab_path"
```

Create, assert, and clean up in one run:

```bash
bash test.sh
```

See [expected.txt](../../labs/git-mental-model/06-merge/expected.txt) for the full expected state.

## Change-the-condition prediction

Start with:

```text
main:    B
feature: B---F1---F2
```

1. Where does `main` point after `git merge --ff-only feature`, and how many parents does the result have?
2. What object enters the graph if the same command is changed to `git merge --no-ff feature`?
3. What happens to the exit status and history when `main` first receives `M1`, then runs `git merge --ff-only feature`?

Answers:

1. `main` points at the existing `F2`; `F2` keeps its original one parent.
2. Git creates a new merge commit whose parents are `B` and `F2`.
3. `--ff-only` exits non-zero because the histories diverged. A regular merge would attempt a two-parent result commit.

## Agent judgment question

An agent reports, “The merge succeeded and there are no conflicts, so it can ship.” Which evidence set supports an approval decision?

```text
A. Only git status has no UU paths
B. Only a merge commit exists
C. Inspect the common ancestor and result diff, confirm the index has no unmerged entries, then run affected build, test, and interface-contract checks
```

Choose C. A only rules out unresolved text conflicts, and B only shows that the object graph is connected. Behavioral correctness needs validation for the affected paths. If the agent cannot identify the contracts it changed, narrow the diff and the test scope before deciding whether to approve it.

## Common misconceptions

### “The common ancestor is the point where two branch names began”

The common ancestor comes from commit-parent relationships, not branch names or creation times. `git merge-base` calculates reachability in the object graph.

### “A fast-forward creates a merge commit”

A fast-forward only moves the current ref to an existing commit. `git rev-list --parents -n 1 HEAD` shows that the target commit's parent count did not increase because of the fast-forward.

### “No conflict markers means behavior is correct”

Conflict markers answer how text can be combined. Builds, tests, migration checks, interface contracts, and human business judgment validate the combined meaning.

### “Ours is always the business version I want to keep”

In a regular merge, ours is the current `HEAD` and theirs is `MERGE_HEAD`. Those are operation-context names, not business priority. Read the active operation and the three stage contents before using `--ours` or `--theirs`.

## Further reading

- [git merge documentation](https://git-scm.com/docs/git-merge)
- [git merge-base documentation](https://git-scm.com/docs/git-merge-base)
- [git ls-files documentation](https://git-scm.com/docs/git-ls-files)
- [Chapter 03: The Index Is the Next Commit Draft](git-mental-model-03-index_en.md)
