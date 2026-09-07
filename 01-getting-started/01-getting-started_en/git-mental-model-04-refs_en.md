# Git Mental Model 04: Refs, HEAD, and Identity

English | [中文](../git-mental-model-04-refs.md) | [Interactive demo](../../interactive/git-mental-model/refs-and-head.html?lang=en) | [Runnable lab](../../labs/git-mental-model/04-refs/README.md)

When an agent says, "I switched branches" or "I tagged this version," the useful question is which reference now names which commit, and whether HEAD is attached to a branch or directly names a commit.

That determines which reference the next commit will move and whether a commit made from detached HEAD will be difficult to find later.

## The conclusion first

~~~text
HEAD -> refs/heads/main -> C3
refs/heads/agent/draft -> C2
refs/tags/v1-light -> C1
refs/tags/v1-annotated -> T1(tag object) -> C1
~~~

- A branch is a movable reference under <code>refs/heads/</code> and normally names a commit.
- A tag is a reference under <code>refs/tags/</code>. A lightweight tag directly names an object; an annotated tag first names a tag object that names its target.
- When attached, HEAD holds a symbolic reference such as <code>ref: refs/heads/main</code>. A commit creates a new commit object and advances <code>main</code>.
- A detached HEAD directly records a commit ID. A commit advances HEAD to the new commit; existing branches stay where they are.
- Moving a reference does not change the contents of the old commit. Local updates to branches and HEAD with reflogs also leave recovery clues; long-term retention of an old object depends on later reachability, reflog protection, and GC policy.

<code>gitrevisions</code> accepts branch names, tag names, and full object IDs as revision syntax; <code>HEAD</code> names the commit on which the working tree is based. [Official revision documentation](https://git-scm.com/docs/gitrevisions)

## Scenario: one project appears to have three histories

The temporary repository has three commits:

~~~text
C1 baseline
├── C2 agent draft       refs/heads/agent/draft
└── C3 main release      HEAD -> refs/heads/main

v1-light     -> C1
v1-annotated -> tag object -> C1
~~~

<code>C1</code>, <code>C2</code>, and <code>C3</code> are objects. <code>main</code>, <code>agent/draft</code>, <code>v1-light</code>, and <code>v1-annotated</code> are references that name objects. One object can have several names; moving one name does not change other names or turn the old object into different content.

This explains the key difference during branch operations: switching branches attaches HEAD to a different branch; creating a branch adds a name for an existing commit; creating a commit on a branch advances only that branch.

## What branches, tags, and HEAD express

| Name | Usual location | What it names | What a new commit does |
| --- | --- | --- | --- |
| branch | <code>refs/heads/</code> | usually a commit | advances the attached branch |
| lightweight tag | <code>refs/tags/</code> | the target object directly, usually a commit | keeps its value |
| annotated tag | <code>refs/tags/</code> | a tag object that names the target | keeps its value |
| attached HEAD | <code>.git/HEAD</code> | a symbolic reference to a branch | follows that branch |
| detached HEAD | <code>.git/HEAD</code> | a commit ID directly | advances HEAD; branches stay put |

<code>git symbolic-ref HEAD</code> reads the branch named by HEAD. The official documentation defines a symbolic reference as a regular file beginning with <code>ref: refs/</code>; with <code>-q</code>, the read exits nonzero when HEAD is detached. [git-symbolic-ref](https://git-scm.com/docs/git-symbolic-ref)

## Attached and detached: what moves on the next commit

When HEAD is attached:

~~~text
HEAD -> main -> C3
git commit
HEAD -> main -> C4
~~~

When HEAD is detached:

~~~text
HEAD -> C1
git commit
HEAD -> C4
main -> C3
agent/draft -> C2
~~~

Both states can create commits. The risk is that a detached commit has no branch name automatically carrying it forward. After further switching or reference updates, it may have only a short-lived clue in the HEAD reflog.

To retain detached work, create a branch before leaving:

~~~bash
git branch agent/experiment HEAD
git switch main
~~~

Those commands do not copy files or commit objects. They add a reference, then return to the main line.

## Tag type changes the object graph

Git's official documentation says that <code>git tag</code> without <code>-a</code>, <code>-s</code>, or <code>-u</code> creates a lightweight tag directly pointing at the target object. Those options create a tag object. Annotated tags contain tagger data, a date, a message, and an optional signature; a lightweight tag is only a name for an object. [git-tag](https://git-scm.com/docs/git-tag)

Check the difference through object types:

~~~bash
git cat-file -t v1-light
git cat-file -t v1-annotated
git rev-parse 'v1-annotated^{}'
~~~

Expected:

~~~text
commit
tag
<baseline-commit-id>
~~~

The final command peels the tag object to its final non-tag object. Release versions commonly need annotated tags because their metadata is reviewable; temporary navigation or local experiments often use lightweight tags. Teams still need a separate agreement about tag movement, signing, and publication.

## Run the temporary-repository lab

The lab data matches this chapter's graph: <code>service.txt</code> starts as <code>release=base</code>, <code>agent/draft</code> adds <code>agent.txt</code>, and <code>main</code> changes <code>service.txt</code> to <code>release=main-1</code>.

### 1. Create the isolated repository and verify its initial state

From the repository root:

~~~bash
lab_path=$(bash labs/git-mental-model/04-refs/setup.sh)
bash labs/git-mental-model/04-refs/verify.sh "$lab_path"
~~~

Object IDs vary by Git version and object format, but the structure is fixed:

~~~text
ok: HEAD -> refs/heads/main -> <main-id>
ok: refs/heads/agent/draft -> <agent-id>
ok: refs/tags/v1-light -> <baseline-id>
ok: refs/tags/v1-annotated -> tag -> <baseline-id>
~~~

<code>setup.sh</code> prints only the temporary directory path and isolates the lab from system and global Git configuration, commit and tag signing, and hooks.

### 2. Follow names to objects

~~~bash
git -C "$lab_path" for-each-ref \
  --format='%(refname:short) %(objecttype) %(objectname)' \
  refs/heads refs/tags
git -C "$lab_path" symbolic-ref --short HEAD
git -C "$lab_path" rev-parse HEAD
git -C "$lab_path" rev-parse refs/heads/main
~~~

Expected meaning:

~~~text
agent/draft points at a commit
main points at a different commit
v1-light has object type commit
v1-annotated has object type tag
HEAD is attached to main
HEAD and refs/heads/main resolve to the same commit ID
~~~

Compare the IDs for <code>main</code> and <code>agent/draft</code> to see both branches exist at once. Read the files they name:

~~~bash
git -C "$lab_path" show refs/heads/main:service.txt
git -C "$lab_path" show refs/heads/agent/draft:service.txt
git -C "$lab_path" show refs/heads/agent/draft:agent.txt
~~~

The expected values are <code>release=main-1</code>, <code>release=base</code>, and <code>proposal=retry</code>.

### 3. Detach HEAD and name the new commit

The following actions apply only to the newly created lab directory. They create a new temporary commit:

~~~bash
git -C "$lab_path" switch --detach v1-annotated
git -C "$lab_path" symbolic-ref -q HEAD || printf 'HEAD is detached\n'
printf 'keep this detached commit\n' > "$lab_path/detached.txt"
git -C "$lab_path" add detached.txt
git -C "$lab_path" commit -m "detached experiment"
git -C "$lab_path" branch keep-detached HEAD
git -C "$lab_path" switch main
~~~

Key expected output:

~~~text
HEAD is detached
~~~

<code>keep-detached</code> then names the new commit, while <code>main</code> still names the main commit from step 1. Before deleting <code>keep-detached</code>, decide whether that commit needs to be retained or shared.

### 4. Remove the temporary repository

~~~bash
bash labs/git-mental-model/04-refs/cleanup.sh "$lab_path"
~~~

The cleanup script requires a lab-specific marker and refuses the repository root, the user home directory, and the filesystem root.

## Safety boundaries

### Check objects, references, and sharing before moving a branch

Before rewriting local history, moving a branch, or force-moving a tag, preserve the current reference:

~~~bash
git status --short
git branch safety/before-rewrite HEAD
git show --no-patch --oneline safety/before-rewrite
git reflog show -n 5 HEAD
~~~

This adds a local branch and gives the current commit a clear name. It does not preserve uncommitted edits or replace a remote backup. If the history was pushed and other people may have built on it, first assess collaboration impact; many shared undo cases need <code>git revert</code>.

<code>git tag -f</code> moves an existing tag name. If that tag represents a released version, a build input, or a signed statement, moving it changes the object downstream users resolve. Establish a new tag name or obtain the team's agreement first.

### Name detached work before leaving it

When an experiment, bisect, or old-version inspection needs a commit, first run:

~~~bash
git branch agent/experiment HEAD
~~~

This branch is a recovery clue. It remains local until pushed, so it does not create a remote backup.

## Common misconceptions

### "A branch is a separate directory"

A branch is a reference. Switching branches aligns HEAD and the working tree with another commit snapshot; the branch does not store a separate copy of the files.

### "Switching branches rewrites the old commit"

Switching and advancing a branch change reference targets. New content is represented by a new commit, while the old commit retains its object ID and contents.

### "Tags can never move"

Git can force-update a tag reference. Release processes often treat published tags as stable identifiers; whether movement is permitted is a team release decision.

### "HEAD is the current branch name"

When attached, HEAD indirectly names a branch through a symbolic reference. When detached, it directly records a commit ID. Check how HEAD resolves before deciding which reference the next commit moves.

### "Detached HEAD cannot commit"

It can commit. The new commit has no branch automatically carrying it forward, so create one before leaving.

## Agent migration question

An agent tests an older version with:

~~~bash
git switch --detach <old-commit>
git commit -am "try a compatibility fix"
~~~

It then reports, "the change is committed." Answer two questions during acceptance:

1. Which branch did the new commit advance?
2. Which reference can stably name the experiment if it must be retained?

Answer: HEAD directly names the new commit, so no ordinary branch advanced. First inspect <code>git log -1 --decorate HEAD</code>, <code>git symbolic-ref -q HEAD</code>, and <code>git show-ref --heads</code>; then run <code>git branch agent/compatibility-test HEAD</code>. Verify that the new branch resolves to that object ID, and state whether it must be pushed or backed up elsewhere.

## Further reading

- [gitrevisions](https://git-scm.com/docs/gitrevisions)
- [git-symbolic-ref](https://git-scm.com/docs/git-symbolic-ref)
- [git-tag](https://git-scm.com/docs/git-tag)
- [Next chapter: Reachability, reflog, and recovery](git-mental-model-05-recovery_en.md)
- [Previous chapter: The Index Is the Next Commit Draft](git-mental-model-03-index_en.md)
