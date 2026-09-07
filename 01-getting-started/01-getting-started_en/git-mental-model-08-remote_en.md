# Git Mental Model 08: A Remote Is Another Repository; `origin/main` Is a Local Record

English | [中文](../git-mental-model-08-remote.md) | [Interactive demo](../../interactive/git-mental-model/remote-and-fetch.html?lang=en) | [Runnable lab](../../labs/git-mental-model/08-remote/README.md)

When an agent reports, “I have seen the latest remote `main`,” a reviewer needs two follow-up questions: did it inspect the branch on the remote service now, or the local `origin/main` left by an earlier fetch? Did it integrate that record into the local working directory? Those answers determine whether the next step is read-only inspection, integration, or conflict handling.

This chapter uses `reader`, `writer`, and a temporary bare `origin.git` to show that ordinary `git fetch origin` updates a remote-tracking ref without automatically changing the current branch, index, or working tree. An explicit fast-forward integration brings files into the working directory. A push also goes through server authentication, authorization, branch policy, and fast-forward rules.

## Scenario: someone pushes a commit first

Initially, `reader` has local `main` and its local record `origin/main` at commit A:

```text
reader
  HEAD -> main -> A
  origin/main -> A
  Index / Working Tree: story.txt = version=1

writer pushes B to the bare origin
```

After `reader` runs an ordinary fetch:

```text
reader
  HEAD -> main -> A
  origin/main -> B
  Index / Working Tree: story.txt = version=1
```

The object for `B` has arrived locally and `origin/main` points to B. `main` remains at A, so files do not change. Then run explicitly:

```bash
git merge --ff-only origin/main
```

Only then does the state become:

```text
reader
  HEAD -> main -> B
  origin/main -> B
  Index / Working Tree: story.txt = version=2
```

## Concepts: remote names, remote branches, and remote-tracking refs

`origin` is a local configuration name for a remote repository, commonly the default after cloning. It points to a URL; it is not a branch.

`main` is a local branch ref, normally under `refs/heads/main`. `origin/main` is a local remote-tracking ref, normally under `refs/remotes/origin/main`. It records the remote `main` tip observed by the last successful fetch.

The following can therefore coexist:

```text
main          A   local working baseline
origin/main   B   remote tip last observed by fetch
HEAD          main
```

The remote service may advance again a second later. Without another network query, `origin/main` proves only the local observation already recorded, not that the service still has the same tip.

An ordinary `git fetch origin` downloads required objects and updates configured remote-tracking refs. It also updates `FETCH_HEAD` and can trigger automatic maintenance. It does not run merge, rebase, switch, or checkout, so it does not write B’s file content into the current working tree. Lower-level fetches with custom refspecs can have different destinations; this chapter covers the common cloned-repository form, `git fetch origin`.

## Observe first, then decide whether to integrate

First establish which refs you are standing on:

```bash
git status --short
git branch -vv
git log --oneline --decorate --graph --all -n 12
git rev-parse main origin/main
```

To obtain remote information only:

```bash
git fetch origin
git log --left-right --graph --oneline main...origin/main
git diff --stat main..origin/main
```

The expected result is that `origin/main` may move while the current `main` and checked-out files stay unchanged. `main...origin/main` makes commits unique to each side visible, which helps distinguish behind, ahead, and diverged states.

When the remote-tracking tip is a descendant of the local branch and you want its files in the working directory:

```bash
git merge --ff-only origin/main
git status --short
git rev-parse HEAD main origin/main
```

`--ff-only` places the “straight advance only” condition in the command. If the histories diverged, the command stops without changing state, leaving a person to choose merge, rebase, or another team-approved integration. `git pull` combines fetch and a later integration; whether it uses merge or rebase depends on options and configuration. Separate commands make state changes easier to review.

## Push: the local client asks to update; the remote decides whether to accept

```bash
git push origin main
```

This asks to push local `main` to `main` on the remote named `origin`. Git sends objects missing from the remote and attempts to update the destination ref. Completion depends on several conditions:

1. The transport connects and credentials authenticate.
2. The service authorizes the identity to write the repository and branch.
3. Server protection rules or hooks accept the update.
4. The destination branch can fast-forward from its old tip to the local commit.

A non-fast-forward rejection has this graph:

```text
          C  reader local main
         /
        B
         \
          D  origin main after writer push
```

Remote `D` is not an ancestor of local `C`. Replacing D with C would lose the D path, so the default push rejects it. A safe recovery sequence is:

```bash
git fetch origin
git log --left-right --graph --oneline main...origin/main
# Merge or rebase according to the team agreement, then resolve conflicts.
# Run the repository-required checks.
git push origin main
```

`git push --force` can rewrite published history and leave other people’s commits without a branch ref. On a shared branch, discuss `--force-with-lease` only after explicit team authorization, impact review, and the relevant checks. It is not the default repair for a non-fast-forward rejection.

A local bare repository reproduces Git graph rules and server-side hook rejection, but it cannot replace the real account authentication or branch-protection configuration of GitHub, GitLab, or another host. The lab’s `protected` hook demonstrates only the boundary that a server can refuse a client request.

## Run the temporary-repository lab

The lab creates its own temporary root, bare origin, and two clones. Every push goes only to that temporary bare path:

```bash
cd labs/git-mental-model/08-remote
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
sed -n '1,240p' "$lab_path/observations.txt"
sed -n '1,240p' "$lab_path/push-results.txt"
bash cleanup.sh "$lab_path"
```

`verify.sh` asserts real Git results:

- During fetch-only, `reader`’s `origin/main` moves from A to B while `reader/main`, the index, and the working tree remain at A.
- After `merge --ff-only origin/main`, `reader`’s HEAD, `main`, index, and working tree all reach B.
- After `reader` creates C and `writer` pushes D to the temporary bare origin, `reader`’s direct push fails.
- The temporary bare origin’s hook rejects an update to `protected`.

The lab disables global Git configuration, signing, and caller hooks. `cleanup.sh` accepts only a marked, structurally complete temporary root. Do not run cleanup while you still want to inspect the state.

Run the complete self-test:

```bash
bash labs/git-mental-model/08-remote/test.sh
```

## Prediction: did the change come from fetch or integration?

`writer` has pushed B, while `reader` initially remains at A. Write the prediction before running the lab:

| Operation | `reader/main` | `reader/origin/main` | `story.txt` |
| --- | --- | --- | --- |
| `git fetch origin` | A | B | `version=1` |
| Then `git merge --ff-only origin/main` | B | B | `version=2` |

The changed condition is the explicit integration command in the second row. If the remote-tracking tip and local branch have diverged after fetch, `--ff-only` stops and preserves the state. Show the commits on both sides and the team’s integration agreement before choosing merge, rebase, or abandoning local commits.

## Agent migration exercise: make “latest” an auditable state claim

An agent handoff should include at least:

```text
fetch time: 2026-... with remote origin
local branch and HEAD: main -> <oid>
remote-tracking ref after fetch: origin/main -> <oid>
working-tree change performed: none | merge --ff-only origin/main | other approved integration
push result: not attempted | accepted | rejected, with reason
```

This record separates “saw a remote tip,” “updated local files,” and “has remote write permission” into verifiable facts. When automation performs fetch only, report “updated local `origin/main`,” not “the local repository is synchronized” or “push permission was obtained.”

## Further reading

- [Official git-fetch documentation](https://git-scm.com/docs/git-fetch)
- [Official git-push documentation](https://git-scm.com/docs/git-push)
- [Official git-remote documentation](https://git-scm.com/docs/git-remote)
- [Lab instructions](../../labs/git-mental-model/08-remote/README.md)
