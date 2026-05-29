English | [中文](zh/useful-git-command.md)

Overview

A collection of common, uncommon, and practical Git commands gathered from day-to-day usage, kept here as a personal reference. If you are not familiar with what these commands mean, please refer to: [Git for Beginners](https://github.com/xirong/my-git#新手入门).

Since Git is used as the version control system in daily development, working with the command line is routine. This document records and organizes the commands used most often, making it easy to look things up later.

[TOC]
# Concept 
```
master : default development branch 
origin : default upstream repository 
HEAD : current branch and commit
HEAD^ : parent of HEAD 
HEAD~4 : the great-great grandparent of HEAD
```
# Alias
The examples below are just suggestions — feel free to use whatever abbreviations work for you.
``` bash
git config --global alias.st status    // abbreviate status as st
git config --global alias.co checkout  // abbreviate checkout as co
git config --global alias.br branch    // abbreviate branch as br
git config --global alias.ci commit    // abbreviate commit as ci
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
```
To remove an alias, simply delete the corresponding line from the config file. For global aliases, run `vim ~/.gitconfig` and remove the entry under `[alias]`; for repository-level aliases, edit `.git/config` instead.

# Git Config
Git configuration has three levels: system (`--system`), user (`--global`), and repository (`--local`). The closer the config is to the repository, the higher its priority. When all three define the same setting, the effective order is **repository > user > system**. Run `git config --help` for more details.

+ System-level config is stored in `/etc/gitconfig`. Configure it with `git config --system user.name "jim"` and `git config --system user.email "jim.jim@gmail.com"`. This applies to all users and all repositories on the system.
+ User-level config is stored in `~/.gitconfig` for each user. Configure it with `git config --global user.name "jim"` and `git config --global user.email "jim.jim@gmail.com"`. This applies to all repositories for the current user.
+ Repository-level config is stored in `.git/config` inside each repository. Configure it with `git config --local user.name "jim"` and `git config --local user.email "jim.jim@gmail.com"`. This applies only to the current repository.

# Basic Usage
- Add a file to the staging area: `git add filename` / `git stage filename`
- Add all modified files to the staging area: `git add --all` / `git add -A`
- Commit staged changes: `git commit -m 'commit message'` / `git commit -a -m 'commit message'` — note the meaning of the `-a` flag
- Remove a file from the Git repository: `git rm filename`
- Remove a file from the Git repository but keep it locally: `git rm --cached filename`
- Rename a file: `git mv filename newfilename` — or rename the file directly and run `git add -A && git commit -m 'commit message'`; Git will automatically detect the rename
- Pull the latest remote changes to local: `git pull (origin branchname)` — the branch name is optional. `pull` automatically fetches and merges; any conflicts will appear in the status output and must be resolved manually. A more recommended approach: run `git fetch` first, then `git merge --no-ff origin branchname` to fetch the latest code and merge manually.

# Repository
- Clone a repository: `git clone repository-url` / `git clone repository-url local-directoryname`
	+ Example — clone the jQuery repo locally: `git clone git://github.com/jquery/jquery.git`
	+ Clone the jQuery repo and rename it to my-jquery: `git clone git://github.com/jquery/jquery.git my-jquery`
- View remote repositories: `git remote -v`
- Add a remote repository: `git remote add [name] [repository-url]`
- Remove a remote repository: `git remote rm [name]`
- Change a remote repository URL: `git remote set-url origin new-repository-url`
- Pull from a remote repository: `git pull [remoteName] [localBranchName]`
- Push to a remote repository: `git push [remoteName] [localBranchName]` — example: `git push -u origin master` pushes the current branch to the remote master branch
- Push local branch `test` to remote `master`: `git push origin test:master` (pushes the local `test` branch as the remote `master` branch). To push local `test` as remote `test`: `git push origin test:test`

# Checkout
The checkout command copies files from the history (or the staging area) to the working directory, and can also be used to switch branches.

![](./_image/2016-07-14 21-26-37.jpg?r=49) ![](./_image/2016-07-14 21-15-47.jpg?r=49&f=2)

**Anonymous branch (detached HEAD)**: If you specify neither a filename nor a branch name, but instead give a tag, remote branch, SHA-1 value, or something like `master~3`, you end up on an anonymous branch known as a detached HEAD.

![](./_image/2016-07-14 21-44-06.jpg?r=56)

When HEAD is in a detached state (not attached to any named branch), commits still work normally, but no named branch is updated. (Think of it as committing to an anonymous branch.) Once you switch to another branch (e.g. master), that commit node may no longer be reachable and will eventually be garbage-collected. Note that after this, nothing refers to `2eecb` anymore. For more detail, see: [visual-git-guide#detached](http://marklodato.github.io/visual-git-guide/index-zh-cn.html#detached)

If you want to keep the state, use `git checkout -b name` to create a new branch from it.

![](./_image/2016-07-14 21-45-50.jpg?r=56)

# Log
> Description: Shows the commit logs.
The command takes options applicable to the git rev-list command to control what is shown and how, and options applicable to the git diff-* commands to control how the changes each commit introduces are shown.
> git log [options] [revision range] [path]

Commonly used log commands:
- View the log: `git log`
- View the log with diff for each commit: `git log -p`
- View the log with a brief summary of file changes per commit: `git log --stat`
- Show one line per commit: `git log --pretty=oneline` / `git log --pretty='format:"%h - %an, %ar : %s'`
- Filter log by range:
	+ View the last 10 commits: `git log -10`
	+ View commits older than 2 weeks: `git log --until=2week` or specify an exact date: `git log --until=2015-08-12`
	+ View commits from the last 2 weeks: `git log --since=2week` or specify an exact date: `git log --since=2015-08-12`
	+ Show commits by a specific user: `git log --committer=user.name` / `git log --author=user.name`
	+ Show commits whose message contains a keyword, e.g. 'test': `git log --grep 'test'`
	+ Try this one-liner: `git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit` — if you find it useful, save it as an alias: `git config --global alias.aliasname 'alias-content'`
	+ More: [Viewing the History -- Pro Git 2](http://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)

The purpose of `log` is to trace changes and investigate issues. Besides `git log`, you can also use `git show` and `git blame` to inspect file changes.
- See who changed what and when in a file: `git blame $file`
- See which files were changed in a specific commit: `git show --pretty="" --name-only <sha1-of-commit>` or `git diff-tree --no-commit-id --name-only -r <sha1-of-commit>`


# Undo things
- Fix a wrong commit message or include a forgotten file in the last commit: `git commit --amend -m 'new msg'`
- Change the author and email of the last commit: `git commit --amend --author="newName <newEmail>"`
- Fix incorrect author or email throughout the entire commit history: use `git rebase` or `git filter-branch`
    ``` bash
    # git rebase approach
    git rebase -i -p 76892625a7b126f4772f8d7e331ada3552c11ce1 
    # An editor opens; change "pick" to "edit" for the commit you want to modify, then save and quit (:wq in vim)
    git commit --amend --author 'newName <newEmail>'
    # This updates the author and email for that commit
    git rebase --continue 
    ################################################################
    # git filter-branch approach: https://help.github.com/articles/changing-author-info/
git filter-branch --env-filter '
OLD_EMAIL="your-old-email@example.com"
CORRECT_NAME="Your Correct Name"
CORRECT_EMAIL="your-correct-email@example.com"
if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
    ```
![](./_image/2017-06-02-11-51-27.jpg?r=54)

- After `git add -A`, unstage a specific file (i.e. exclude it from the current commit): `git reset HEAD filename`
- Discard changes to specific files in the working directory: `git checkout -- filename` — Warning: once run, all changes to those files are gone. Use with caution!
- Reset the working directory to a specific commit: `git reset --hard <sha1-of-commit>`

# Reset 
The reset command moves the current branch pointer to another position, and optionally modifies the working directory and the index. It can also be used to copy files from a historical commit into the index without touching the working directory.

![](./_image/2016-07-14 20-31-39.png?r=64&f=1)

Reset the working directory to a specific commit: `git reset --hard <sha1-of-commit>`
- `git reset --hard HEAD^` — resets both the index and the working directory; all changes since `<commitid>` are discarded, and HEAD is moved to `<commitid>`
* `git reset --soft HEAD^` — leaves the index and working directory unchanged; only moves HEAD to `<commitid>`, and all changes appear under "Changes to be committed"
* `git reset --mixed HEAD^` — the default; resets the index but leaves the working directory untouched; changes are moved back to the index area

# Revert
> `git revert` will create a new commit that's the opposite (or inverse) of the given SHA. If the old commit is "matter", the new commit is "anti-matter"—anything removed in the old commit will be added in the new commit and anything added in the old commit will be removed in the new commit.
> This is Git's safest, most basic "undo" scenario, because it doesn't alter history—so you can now git push the new "inverse" commit to undo your mistaken commit.

```bash
git revert [--[no-]edit] [-n] [-m parent-number] [-s] [-S[<keyid>]] <commit>…​
git revert --continue
git revert --quit
git revert --abort
```

To undo a single commit from a series without affecting later commits: `git revert c2`

(https://blog.csdn.net/u013066244/article/details/79920012) https://blog.csdn.net/u013066244/article/details/79920012

# Restore
`restore` takes over the file-restoration responsibility that was previously part of `checkout`. While `checkout` could both switch branches and restore working tree files, `restore` now handles only the restoration side.

`git restore` restores files in the working tree from either the index or another commit. This command does not update your branch. It can also be used to restore files in the index from another commit.


## Revert VS Reset VS Restore

Consider a simple scenario: branch A has five commits — c1, c2, c3, c4, c5. You later discover that commit c2 is problematic and needs to be rolled back. How do you handle it?

**Option 1: Using reset**
Create a new branch `A_bak` as a copy of the current branch, then run `git reset --hard c2` on branch A (this drops c3, c4, c5). Then use `git cherry-pick` to replay c3, c4, and c5 back onto branch A.

**Option 2: Using revert**
Run `git revert c2`. This may produce conflicts — resolve them and proceed. If c2 was a merge commit, you need an extra step: `git revert c2 -m 1` or `git revert c2 -m 2`. See: https://blog.csdn.net/u013066244/article/details/79920012

Result: a new commit c6 is created that inverts the changes introduced by c2. If there are conflicts, the conflicting file contents will be shown for manual resolution.

`revert` is purpose-built for exactly this kind of scenario and should be the go-to command in daily work.


# Diff
- Show differences between the working directory and the staging area: `git diff`
- Show differences between the working directory and the current HEAD commit: `git diff HEAD`
- Show differences between the staging area and the current HEAD commit: `git diff --cached` / `git diff --staged`
- Show only which files changed, without showing the diff content: `git diff --stat`

# Merge
![](./_image/2016-07-14 20-53-25.jpg?r=80)


- Merge a branch into the current branch (after resolving conflicts or pulling the latest remote changes): `git merge branchname`
- Preserve branch history in the merge log (prevent fast-forward): `git merge --no-ff branchname` — the `--no-ff` flag prevents a fast-forward merge. See [the difference](http://stackoverflow.com/questions/9069061/what-is-the-difference-between-git-merge-and-git-merge-no-ff). In a fast-forward merge, the pointer simply moves forward when the branch contents are identical, and no branch history is visible.

# Rebase
Rebase and merge produce the same end result — integrating local and remote changes — but they differ in how they do it.
``` bash
git checkout mywork
git rebase origin
```
These commands take each commit on the `mywork` branch, temporarily save them as patches (stored in `.git/rebase`), update `mywork` to the latest `origin` branch, and then reapply the saved patches on top.

A diagram showing the difference between rebase and merge:

![](./_image/2016-07-19 20-35-30.jpg?r=56)

During a rebase, conflicts may occur. When they do, Git pauses and lets you resolve them. After resolving, use `git add` to update the index, then run `git rebase --continue` (no need to commit) to apply the remaining patches. At any point you can abort the rebase with `git rebase --abort`, which returns `mywork` to its state before the rebase started.

# Cherry Pick
The cherry-pick command "copies" a commit node and creates an identical new commit on the current branch.

![](./_image/2016-07-14 20-57-04.jpg?r=65)

# Branch workflow
Aone2 Git branch development and deployment model — detailed breakdown: [http://docs.alibaba-inc.com:8090/pages/viewpage.action?pageId=194872297](http://docs.alibaba-inc.com:8090/pages/viewpage.action?pageId=194872297)

Branch structure on origin:
- master
- develop
- release
    - 20161129163217010_r_release_yingyongming
    - 20161029163217010_r_release_yingyongming
- feature
    - 20161129_163448_newfeature_1
    - 20161129_163448_newfeature_2
- hotfix
    - 20161129_163448_hotfix_1
- tags
    - 20161129163217010_r_release_newfeature_yingyongming

To create a branch directly: `git checkout -b feature/20161129_163448_newfeature_1`

![](./_image/2016-09-22-20-57-27.jpg)

- **master**: master always reflects production code — the most stable branch, containing code that can be deployed to the production environment at any time. After a release succeeds, Aone2 merges the code into master and updates the branch. Once Aone2 is in use, write access to master is revoked for everyone.
- **develop**: the branch holding the latest development output. Code here is typically ready for nightly builds. Only development leads have write access to develop.
- **feature**: feature branches, one per feature, named `feature/<name>`. After development and self-testing are done, they are merged into develop.
- **hotfix**: emergency bug-fix branches. After the fix goes live, they can be merged directly into master.

![](./_image/2016-07-19 19-58-15.jpg?r=60)

The Git-Develop branching model is a development workflow built around strict control of release quality and cadence. `develop` serves as the fixed continuous integration and release branch; code can only be merged into it after passing a Code Review. The basic flow is:
- Each requirement or change gets its own branch created from master.
- Developers do their work on that branch.
- When the code is ready for release, a Code Review is submitted via Aone; once approved, the code is automatically merged into develop.
- Once all planned change branches have been merged into develop, the system rebases master onto develop, then triggers build, packaging, and deployment automatically.
- After a successful release, Aone tags the current develop release version as the "current production version" baseline.
- After a successful release, Aone automatically merges the develop release version back into master.


## Branch Commands
- List branches: `git branch`, `git branch -v`, `git branch -vv` (shows which remote branch each local branch tracks), `git branch --merged`, `git branch --no-merged`
- Create a branch: `git branch branchname`
	
	+ Example — create a `dev` branch from master: `git branch dev`
- Create a branch from a specific commit: `git branch branchname <sha1-of-commit>`
	+ Example — create a `hotfix` branch from the production commit `a207a38d634cc10441636bc4359cd8a18c502dea`: `git branch hotfix a207a38`
	+ Example — create a branch from a remote branch, local branch, commit ID, or tag: `git checkout -b newbranch localBranch/remoteBranch/commitId/tag`
	+ Example — create an empty branch:
    	``` bash
      	git checkout --orphan gh-pages  # create an orphan branch (fully independent)
        Switched to a new branch 'gh-pages'
        git rm -rf .  # delete all files from the current working tree
        rm '.gitignore'
        # Note: git branch won't show the branch name until you make your first commit. Add files and commit to make it visible.
    ````
- Switch branches: `git checkout branchname`
	
	+ Example — switch from master to dev: `git checkout dev`
- Create a new branch and switch to it: `git checkout -b branchname` or `git branch branchname && git checkout branchname`
	
	+ Example — create `dev` from master and switch to it: `git checkout -b dev` or `git branch dev && git checkout dev`
- Compare branches: `git diff branchname` — shows differences between `branchname` and the current branch. To see only which files differ (no diff content): `git diff branchName --stat`
- Merge a branch: `git merge branchname` — merges `branchname` into the current branch
- Delete a branch: `git branch -d branchname` — force delete an unmerged branch: `git branch -D branchname`
- Rename a branch: `git branch -m dev development` — renames `dev` to `development`
- List remote branches: `git branch -r` or `git branch -r -v`
- Fetch a remote branch to local: `git checkout -b local-branchname origin/remote-branchname`
- Push a local branch to remote: `git push origin remote-branchname` or `git push origin local-branchname:remote-branchname`
	+ Push local `dev` to remote `dev`: `git push (-u) origin dev` or `git push origin dev:dev`
	+ (Tip) Push local `dev` to remote `master`: `git push origin dev:master`
- Delete a remote branch: `git push origin :remote-branchname` or `git push origin --delete remote-branchname`
- Manually set up branch tracking — track `origin/next` from local master: `git branch --track master origin/next` or `git branch --set-upstream-to=origin/master` (depending on your Git version).
- Tracking branches: use `git branch -vv` to see which remote branch each local branch currently tracks. When you create a branch with `git checkout -b sf origin/serverfix`, it automatically sets up tracking (output: `Branch sf set up to track remote branch serverfix from origin. Switched to a new branch 'sf'`). You can also set tracking manually: `git branch -u origin/serverfix` (equivalent to `git checkout --track origin/serverfix`).

> "Checking out a local branch from a remote branch automatically creates what is called a 'tracking branch' (or sometimes an 'upstream branch'). Tracking branches are local branches that have a direct relationship to a remote branch. If you're on a tracking branch and type git pull, Git automatically knows which server to fetch from and branch to merge into.
> When you clone a repository, it generally automatically creates a master branch that tracks origin/master. However, you can set up other tracking branches if you wish — ones that track branches on other remotes, or don't track the master branch. The simple case is the example you just saw, running git checkout -b [branch] [remotename]/[branch]. This is a common enough operation that git provides the --track shorthand."


# Tag
- List tags: `git tag`
- Find tags matching a pattern, e.g. `V1.0.*`: `git tag -l 'V1.0.*'` — lists matches such as V1.0.1, V1.0.1.1, V1.0.2, etc.
- Create a lightweight tag: `git tag tag-name` — example: `git tag v1.0`
- Create an annotated tag: `git tag -a tag-name -m 'msg'` — example: `git tag -a v1.0.0 -m 'tagging v1.0.0 after successful release'`
	+ Compare annotated vs. lightweight tags with: `git show v1.0` / `git show v1.0.0`
	+ "A lightweight tag is very much like a branch that doesn't change — it's just a pointer to a specific commit. Annotated tags, however, are stored as full objects in the Git database. They're checksummed; contain the tagger name, e-mail, and date; have a tagging message; and can be signed and verified with GNU Privacy Guard (GPG)."
- Show information for a specific tag: `git show tag-name`
- Create a tag from a historical commit: `git tag -a tagname <sha1-of-commit>`
	+ Example — tag the production commit `a207a38d634cc10441636bc4359cd8a18c502dea`: `git tag -a v1.0.0 a207a38`
- Delete a tag: `git tag -d tagname`
- Pull remote tags to local: `git pull remotename --tags` — example: `git pull origin --tags`
- Push a tag to remote: `git push remotename tagname` — example: `git push origin v1.0.0`
- Push all local tags to remote: `git push remotename --tags` — example: `git push origin --tags`
- Delete a remote tag: `git push origin :tagname` or `git push origin --delete tagname` or `git push origin :refs/tags/v0.9`

# Submodule
Add a submodule: `$ git submodule add [url] [path]`
    Example: `$ git submodule add git://github.com/soberh/ui-libs.git src/main/webapp/ui-libs`
Initialize submodules: `$ git submodule init` — only needs to be run once after the initial clone
Update submodules: `$ git submodule update` — run this after every pull or branch switch
Remove a submodule (four steps):
 1) `$ git rm --cached [path]`
 2) Edit `.gitmodules` and remove the submodule's configuration section
 3) Edit `.git/config` and remove the submodule's configuration section
 4) Manually delete the leftover submodule directory

# Stash
It often happens that while you're working on part of your project and things are in a messy state, you want to switch branches to work on something else. You don't want to commit half-done work, but you also don't want to lose it. The solution is `git stash`.

`stash` captures the intermediate state of your working directory — your tracked modified files and staged changes — and saves them to a stack of unfinished changes that can be reapplied at any time.

```
usage: git stash list [<options>]                                         -- list current stashes
   or: git stash show [<stash>]                                           -- show the contents of a stash entry
   or: git stash drop [-q|--quiet] [<stash>]                             -- remove a stash entry
   or: git stash ( pop | apply ) [--index] [-q|--quiet] [<stash>]        -- apply a stash entry to the working directory
   or: git stash branch <branchname> [<stash>]
   or: git stash [save [--patch] [-k|--[no-]keep-index] [-q|--quiet]
		       [-u|--include-untracked] [-a|--all] [<message>]]
   or: git stash clear                                                    -- remove all stash entries
```

# oh-my-zsh Common Aliases
```
alias g='git'
alias ga='git add'
alias gco='git checkout'
alias gcb='git checkout -b'
alias gcm='git checkout master'
alias gcd='git checkout develop'
alias gd='git diff'
alias gf='git fetch'
alias gfo='git fetch origin'
alias gl='git pull'
alias gp='git push'
```
