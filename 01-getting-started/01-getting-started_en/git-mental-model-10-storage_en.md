# Git Mental Model 10: Logical Snapshots and Physical Storage Are Separate Layers

English | [中文](../git-mental-model-10-storage.md) | [Interactive demo](../../interactive/git-mental-model/storage-and-maintenance.html?lang=en) | [Runnable lab](../../labs/git-mental-model/10-storage/README.md)

When a repository has many commits and similar files and `.git/objects` grows, it is tempting to explain it as “each commit copies the project.” Git’s logical model is a snapshot graph made of commits, trees, and blobs. The physical layer can retain objects as loose objects or reorganize them into pack files with delta compression for similar objects. Physical layout can change while the content visible from the same commit stays unchanged.

This chapter covers how to observe those layers, what `repack`, `gc`, and `prune` each do, and why commit-graph is acceleration metadata rather than part of a business snapshot.

## Scenario: can we “clean Git” after history grows?

When a team sees object storage grow and wants to run maintenance, split the question into four layers:

```text
logical content: the commit, tree, and blob content shown by git show <commit>
reachability: which objects can still be found through branch, tag, reflog, and other refs
physical layout: loose objects, packs, deltas, and pack indexes
auxiliary metadata: how commit-graph assists traversal of commit history
```

If `main` still points to commit C, normal repacking or writing a commit-graph must not change `git show C`. After deleting a branch ref, whether objects unique to that branch are cleaned also depends on other refs, reflogs, expiry policies, and maintenance timing. “The branch is deleted” does not prove “the objects disappeared immediately,” because it omits the recovery window.

## Concepts: snapshot meaning does not depend on pack layout

A commit points to a root tree; a tree points to paths and blobs or subtrees; a blob stores file content. Object IDs derive from object type and content, so Git can reuse an object with identical content. Multiple commits commonly share trees and blobs for unchanged files.

At the physical layer, many objects may initially be separate loose files below `.git/objects/`. `git repack` can write objects into one or more `.pack` files with `.idx` indexes. Similar objects can be expressed as deltas relative to another object. When Git reads an object, it reconstructs the same logical content.

Both statements are true:

```text
A commit is semantically a complete snapshot.
Git can share objects on disk and compress similar objects.
```

Do not infer that a snapshot requires copying the whole working directory on every commit. Do not infer that a delta in a pack makes historical content incomplete.

## Observe physical structure without making a performance claim

First inspect current object statistics and the pack directory:

```bash
git count-objects -vH
git rev-parse --git-path objects/pack
git verify-pack -v .git/objects/pack/*.idx
```

`count-objects` counts and byte sizes change with Git version, object hash format, compression parameters, file contents, prior automatic maintenance, and machine environment. `verify-pack` can show objects and delta-chain information for the current pack. They are useful for diagnosing and comparing one controlled experiment. They do not independently prove repository performance or define a fixed threshold for every project.

For a disposable copy, or a maintenance window with a verified backup and no concurrent Git writers, common commands are:

```bash
git status --short
git repack -ad
git commit-graph write --reachable
git commit-graph verify
git gc --no-prune
```

`repack -a` considers reachable objects for a new pack. `-d` removes packs superseded by the new pack and redundant loose objects already covered by packs. `gc` coordinates several repository-maintenance tasks; `--no-prune` explicitly retains loose-object deletion, making it a narrower observation step in this chapter’s lab. Maintenance for a production or collaborative repository needs an assessment of repository size, disk space, active Git processes, and the team’s release workflow.

## The safety boundary of `gc`, `prune`, and reachability

`git gc` is the higher-level entrypoint for ordinary maintenance and performs several housekeeping tasks. Its default pruning expiry does not immediately delete every unreachable object, leaving time for reflog- and mistake-recovery paths.

`git prune` is lower-level. The official manual recommends `git gc` in most cases because it handles pruning with other maintenance tasks. `git prune --expire=now` immediately processes eligible loose objects; if another Git process is writing the same repository, it increases corruption risk.

Before destructive maintenance, confirm at least:

1. The target is the exact local repository or a disposable copy, and the path matches the current directory.
2. The current worktree and every branch or tag worth retaining have been checked, and necessary objects have a recoverable source.
3. No clone, fetch, repack, GC, IDE background Git task, or other process is writing the object store concurrently.
4. The command, expiry parameter, and expected removal scope are recorded; prefer `git prune -n` to inspect candidates first.

Do not copy the lab’s `git prune --expire=now` to a collaborative repository. In this chapter’s lab it deletes exactly one blob that the script just wrote with no ref pointing to it, and the entire lab root is disposable.

## Commit-graph: an auxiliary file for faster graph walks

Commit-graph is a serialized commit-graph file. `git commit-graph write --reachable` generates the graph from reachable refs, and `git commit-graph verify` cross-checks its contents against the object database. It can help Git perform some commit-graph walks faster. When changed-path data is enabled, it can also help path-specific history queries.

It does not alter commit, tree, blob, or branch semantics, and it does not replace packs, reflogs, or backups. Seeing a commit-graph file proves only that the auxiliary structure was written. A performance difference needs measurement under a fixed workload, machine, Git version, and configuration.

## Run the temporary-repository lab

The lab creates 14 similar logical snapshots and performs physical maintenance in an isolated temporary repository:

```bash
cd labs/git-mental-model/10-storage
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
sed -n '1,200p' "$lab_path/observations.txt"
diff -u "$lab_path/show-before.txt" "$lab_path/show-after.txt"
sed -n '1,120p' "$lab_path/count-before.txt"
sed -n '1,120p' "$lab_path/count-after.txt"
bash cleanup.sh "$lab_path"
```

`verify.sh` asserts real Git behavior:

- `git show` for one stable commit is byte-for-byte identical before and after repack, commit-graph write, `gc --no-prune`, and pruning the lab orphan.
- A pack and pack index exist, and `git verify-pack` reports at least one delta object.
- The commit-graph file exists and `git commit-graph verify` succeeds.
- `git prune --expire=now` removes only the deliberately unreachable blob, while the retained commit remains showable.

The lab disables global Git configuration, signing, and caller hooks. It records real `count-objects` output without presenting bytes, object counts, or elapsed time as a performance conclusion. `cleanup.sh` deletes only a marked, structurally complete temporary root.

Run the complete self-test:

```bash
bash labs/git-mental-model/10-storage/test.sh
```

## Prediction: which change affects logical content?

Choose commit C that is still referenced by `main`:

| Operation | `git show C` | Physical object structure | Reachability |
| --- | --- | --- | --- |
| `git repack -ad` | unchanged | packs and deltas may change | C remains reachable from `main` |
| Write and verify commit-graph | unchanged | auxiliary file is added or updated | C remains reachable |
| `git gc --no-prune` | unchanged | several maintenance tasks may run | C remains reachable |
| Delete the only ref and wait for relevant expiry conditions | C can lose a reachable path | depends on later maintenance | affected by reflog, time, and configuration |

The changed condition is whether C retains a reachable ref path and whether maintenance has reached an allowed deletion expiry. Do not predict a fixed pack size, delta count, or duration; those values depend on the actual object set and Git’s compression choices.

## Agent migration exercise: an auditable maintenance record

When automation handles object maintenance, its handoff should include at least:

```text
repository path and HEAD: <path> / <oid>
worktree and refs checked: clean state, branches, tags, reflog consideration
concurrent Git activity checked: <processes or scheduling boundary>
command and expiry parameters: <exact command>
logical invariant: git show <stable-commit> before/after comparison
physical observations: pack/index/commit-graph existence and count-objects output
deletion evidence: exact disposable object or dry-run candidate
```

This record keeps maintenance traceable: which logical content remained, which physical structures changed, and which deletion actions still have recovery boundaries. An agent must not expand “GC returned successfully” into “repository performance improved” or “all history is safe.”

## Further reading

- [Official git-gc documentation](https://git-scm.com/docs/git-gc)
- [Official git-repack documentation](https://git-scm.com/docs/git-repack)
- [Official git-prune documentation](https://git-scm.com/docs/git-prune)
- [Official git-commit-graph documentation](https://git-scm.com/docs/git-commit-graph)
- [Lab instructions](../../labs/git-mental-model/10-storage/README.md)
