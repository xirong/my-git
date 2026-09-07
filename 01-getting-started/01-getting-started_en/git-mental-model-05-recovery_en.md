# Git Mental Model 05: Reachability, Reflog, and Recovery

English | [中文](../git-mental-model-05-recovery.md) | [Interactive demo](../../interactive/git-mental-model/reachability-and-recovery.html?lang=en) | [Runnable lab](../../labs/git-mental-model/05-recovery/README.md)

Before <code>reset --hard</code>, rebase, amend, branch deletion, or a forced remote update, determine whether a recovery clue exists. Git recovery comes from objects, references, and the local reflog, not from the fact that a command was just run.

This chapter establishes recovery capability before explaining dangerous rewrites. It separates "the branch name disappeared" from "the object is no longer recoverable."

## The conclusion first

~~~text
refs/heads/main -> C1
refs/heads/recovered -> C2

HEAD reflog earlier value -> C3

no ref, no reflog, object pruned -> cannot resolve C4
~~~

- Reachability describes whether an object can be found by following commit, tree, and blob edges from a set of starting points. Branches, tags, and other refs are common starting points.
- Deleting a branch name or resetting a branch to an older commit only removes or moves a reference. The old commit often remains in the object database and may temporarily be named by reflog.
- A reflog records branch-tip and other reference updates in a local repository. The HEAD reflog also records branch switches. It does not travel through push as a remote backup.
- Reflogs have retention periods. The current official defaults are 90 days for reachable entries and 30 days for entries unreachable from the current branch tip; configuration and explicit expiration can change those periods.
- Once an object loses ref and reflog protection, GC can remove it. After removal, Git cannot recover it from its object database.
- An edit never recorded through <code>git add</code> or <code>git commit</code> has no content for Git objects to recover; use editor, filesystem, or other backups.

The official documentation describes reflogs as records of reference-tip updates in the local repository and supports revision syntax such as <code>HEAD@{2}</code> for earlier HEAD values. [git-reflog](https://git-scm.com/docs/git-reflog)

## Object states from named to unprotected

The lab uses this object relationship:

~~~text
main -> C1 baseline

C2 keep recoverable commit
  no ref reaches it
  HEAD reflog still names C2

C3 discard after expiry
  no ref reaches it
  HEAD reflog still names C3
~~~

After running <code>git branch recovered C2</code>:

~~~text
refs/heads/recovered -> C2
~~~

<code>C2</code> again has a direct reference, so GC treats it as protected. For <code>C3</code>, explicitly expire reflogs and then prune:

~~~text
no ref -> no reflog -> object pruned
~~~

The object ID may no longer resolve through <code>git cat-file</code>. Recovery therefore has time and retention conditions; it is not a permanent-backup strategy.

## Reachability depends on the starting points in use

<code>git log main</code> walks ancestors from <code>main</code>. If <code>main</code> was reset from <code>C2</code> to <code>C1</code>, then <code>C2</code> is no longer part of main's history.

That does not prove <code>C2</code> has disappeared from the repository's disk. By default, <code>git fsck</code> uses the index, <code>refs</code>, and reflogs as heads for its reachability trace. Adding <code>--no-reflogs</code> helps reveal an old object that remains only through a reflog clue. [git-fsck](https://git-scm.com/docs/git-fsck)

~~~bash
git fsck --no-reflogs --unreachable
~~~

Expected output includes a line such as:

~~~text
unreachable commit <old-commit-id>
~~~

This is a check result, not a promise about how long the object remains recoverable. The object database, reflog expiration, and GC status can all change the conclusion.

## Reflog is a local recovery clue with a lifetime

Inspect local HEAD and branch movement:

~~~bash
git reflog show --oneline HEAD
git reflog show --oneline main
~~~

The output can include commits, resets, and checkouts. <code>HEAD@{1}</code> means the previous HEAD reflog value; <code>main@{1}</code> means main's previous value. <code>gitrevisions</code> defines these forms as the local ref's value at an earlier time or ordinal. [gitrevisions](https://git-scm.com/docs/gitrevisions)

Read local retention overrides:

~~~bash
git config --get gc.reflogExpire
git config --get gc.reflogExpireUnreachable
~~~

Without a local override, Git's current documentation gives defaults of <code>gc.reflogExpire=90 days</code> and <code>gc.reflogExpireUnreachable=30 days</code>. The first applies to general entries; the second removes entries unreachable from the current branch tip earlier. Repository configuration, organization templates, manual expiration, and maintenance can all alter actual retention. [git-reflog expiration options](https://git-scm.com/docs/git-reflog)

Reflog is useful for short-lived incident recovery. It does not replace a remote repository, bundle, backup, or formal release artifact. Each clone has its own reflog; <code>HEAD@{1}</code> in repository A does not automatically exist in repository B.

## Establish a recovery point before a dangerous operation

Before a local rewrite, run:

~~~bash
git status --short
git branch safety/before-rewrite HEAD
git show --no-patch --oneline safety/before-rewrite
git reflog show -n 5 HEAD
~~~

These commands have three purposes:

1. <code>git status --short</code> exposes uncommitted state first. Choose an appropriate way to preserve edits that matter.
2. <code>safety/before-rewrite</code> gives the current commit an explicit reference instead of relying only on reflog.
3. <code>git reflog</code> records the local recovery clues available before the operation, so they can be checked afterward.

If history was pushed or other people may have built on it, also inspect remote, collaborator, and release impact. A shared undo often needs a new <code>git revert</code> commit. Git has no automatic recovery for database writes, deployments, messages, or other external side effects.

The commit form of <code>git reset</code> changes the commit named by HEAD and records the prior branch tip in <code>ORIG_HEAD</code>. <code>--hard</code> also overwrites the working tree and index; official documentation says it may overwrite untracked files. [git-reset](https://git-scm.com/docs/git-reset)

## Run the temporary-repository lab

The lab script creates a marked temporary repository, sets a local identity, and disables signing and hooks. In that temporary repository, <code>setup.sh</code> makes <code>C2</code>, runs one <code>reset --hard</code>, removes <code>ORIG_HEAD</code>, then creates and deletes the temporary branch that carried <code>C3</code>. None of those actions modify the host repository.

### 1. Create the temporary repository and inspect reflog protection

From the repository root:

~~~bash
lab_path=$(bash labs/git-mental-model/05-recovery/setup.sh)
git -C "$lab_path" show-ref --heads
git -C "$lab_path" reflog show --oneline HEAD
git -C "$lab_path" fsck --no-reflogs --unreachable
~~~

Expected meaning:

~~~text
main points to the baseline commit
HEAD reflog contains "keep recoverable commit"
HEAD reflog contains "discard after expiry"
fsck without reflogs reports both commits as unreachable
~~~

Object IDs and reflog ordinal numbers vary. First identify the object ID beside <code>keep recoverable commit</code> and call it <code>&lt;recoverable-id&gt;</code>; do not infer it from its format.

### 2. Create a recovery branch from the reflog object ID

~~~bash
git -C "$lab_path" branch recovered <recoverable-id>
git -C "$lab_path" show --no-patch --oneline recovered
git -C "$lab_path" rev-parse refs/heads/recovered
~~~

Expected:

~~~text
keep recoverable commit
<recoverable-id>
~~~

The recovery action only creates a branch reference. It does not rewrite commit contents. You can then inspect changes, decide on merge or rebase, or keep the branch as a recovery point.

### 3. Let the verification script exercise both outcomes

Step 2 wrote <code>recovered</code> into the temporary repository. The verifier needs its initial state, where no ref reaches either commit, so remove that lab and create a fresh one first:

~~~bash
bash labs/git-mental-model/05-recovery/cleanup.sh "$lab_path"
lab_path=$(bash labs/git-mental-model/05-recovery/setup.sh)
~~~

Then run:

~~~bash
bash labs/git-mental-model/05-recovery/verify.sh "$lab_path"
~~~

Expected structure:

~~~text
ok: reset moved main to <baseline-id> while reflog retained <recoverable-id>
ok: recovered branch now names <recoverable-id>
ok: after explicit reflog expiry and gc --prune=now, <expired-id> no longer resolves
~~~

The first assertion confirms that no ref reaches <code>C2</code> or <code>C3</code>, both remain in the HEAD reflog, and both are reported by <code>git fsck --no-reflogs --unreachable</code>. The second creates <code>recovered</code>. The third intentionally removes reflog protection from <code>C3</code> and prunes it immediately.

### 4. Observe expiration and pruning risk in the lab

The verifier's final assertion uses the following two commands to remove recovery clues and immediately prune unprotected objects. Run them only against the <code>$lab_path</code> that this chapter's <code>setup.sh</code> just created. Do not copy them into an active repository, a shared repository, or a repository with another Git process writing to it. To reproduce the entire sequence manually, run <code>setup.sh</code> again, inspect the reflog first, then run these commands:

~~~bash
git -C "$lab_path" reflog expire --expire=now --expire-unreachable=now --all
git -C "$lab_path" gc --prune=now
~~~

Git documentation says that <code>gc --prune=now</code> prunes unnecessary loose objects of every age and raises corruption risk when another process is writing to the repository concurrently. Ordinary <code>git gc</code> uses a default prune threshold of two weeks ago, which <code>gc.pruneExpire</code> can override. [git-gc](https://git-scm.com/docs/git-gc)

### 5. Remove the temporary repository

~~~bash
bash labs/git-mental-model/05-recovery/cleanup.sh "$lab_path"
~~~

The cleanup script checks the lab marker and refuses the repository root, the user home directory, and the filesystem root.

## Safety boundaries

### Continue investigating when a branch name is gone

Check in this order:

~~~bash
git show-ref --heads --tags
git reflog show --oneline HEAD
git fsck --no-reflogs --unreachable
git cat-file -t <candidate-object-id>
~~~

These commands answer, respectively: whether an explicit reference exists, whether HEAD recorded the object, whether it is unreachable when reflogs are removed from the trace heads, and whether the object remains readable. Only when the clues are absent or the object is already pruned can you conclude that Git's object database has no recovery clue.

### "I did not change a file" does not prove the working tree is safe

<code>reset --hard</code> can overwrite the working tree, index, and untracked files. Inspect <code>git status --short</code> and actual file contents first. If work includes an edit never recorded through <code>git add</code> or <code>git commit</code>, the Git object database has no corresponding recovery evidence; pause the dangerous operation and use editor history, filesystem snapshots, or other backups.

### Reflog does not provide cross-machine or long-term retention

Reflog belongs to the local repository and its entries expire. Important recovery points need an explicit branch or tag and, under the team's policy, a push, backup, or verifiable release artifact.

## Common misconceptions

### "Deleting a branch immediately deletes its commit"

Deleting the branch first removes one reference. If other refs, reflogs, or retention mechanisms still name the object and it has not been pruned, it may still be found.

### "Reflog is permanent history"

It is a local, expiring record of reference updates. Defaults can also be changed through configuration and commands.

### "Knowing an object ID always enables recovery"

An ID only resolves while the object still exists. With no refs, reflogs, or other retention, GC may already have removed it.

### "Git recovers every uncommitted edit"

Git works from objects and references it actually recorded. An edit never recorded through <code>git add</code> or <code>git commit</code> needs a recovery source outside Git.

### "An unreachable result from git fsck means corruption"

Unreachable means the object cannot be found from the starting points used by that check. The object can still be complete in the object database and recoverable by creating a new branch.

## Agent migration question

An agent creates a reviewable local commit, then runs <code>git reset --hard HEAD~1</code>. It reports, "the commit is lost." It did not push and did not say whether other working-tree edits exist.

Complete these checks before selecting a recovery action:

1. Run <code>git status --short</code> to find uncommitted edits that need protection.
2. Run <code>git reflog show --oneline HEAD</code> to find the pre-reset object ID.
3. Run <code>git cat-file -t &lt;id&gt;</code> and <code>git show --stat &lt;id&gt;</code> to confirm the type and contents.
4. Create <code>git branch recovery/agent-reset &lt;id&gt;</code> so the recovered object receives an explicit reference again.
5. Decide whether that branch should be pushed, merged, retained for review, or replaced by an undo strategy suitable for shared history.

If the agent's important edit was never recorded through <code>git add</code> or <code>git commit</code>, reflog and the object graph cannot recover it. State the missing Git evidence and inspect editor history or backups within the authorized scope.

## Further reading

- [git-reflog](https://git-scm.com/docs/git-reflog)
- [git-fsck](https://git-scm.com/docs/git-fsck)
- [git-gc](https://git-scm.com/docs/git-gc)
- [git-reset](https://git-scm.com/docs/git-reset)
- [gitrevisions](https://git-scm.com/docs/gitrevisions)
- [Previous chapter: Refs, HEAD, and Identity](git-mental-model-04-refs_en.md)
