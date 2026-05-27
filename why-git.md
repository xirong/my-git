English | [中文](zh/why-git.md)

SVN has been working just fine — so why switch to Git? What are Git's advantages and disadvantages? And what are the most noticeable differences between the two in day-to-day use?

(For a refresher on SVN, check out [How To Use Svn in Daily Work](using-svn.md))

- [Why is Git better than Subversion?](http://stackoverflow.com/questions/871/why-is-git-better-than-subversion) — A detailed Stack Overflow discussion on the differences between SVN and Git.
- [What are the differences between SVN and Git?](https://help.github.com/articles/what-are-the-differences-between-svn-and-git/) — GitHub's comparison of the two, covering repository structure, history, and submodules.
- [Jiang Xin: Why is Git better than SVN?](http://www.worldhello.net/2012/04/12/why-git-is-better-than-svn.html "蒋鑫 - Why `Git` is better than `SVN`")

The following content is from [@oldratlee](https://github.com/oldratlee)'s [repo](https://github.com/oldratlee/software-practice-miscellany/blob/master/git/README.md).

Notable Differences Between SVN and Git in Daily Use
=========================

![git vs svn](http://static.ixirong.com/pic/mygit/why-git.png)

:point_right: My own experience switching from `svn` to `git` — what changed most dramatically.

:beer: Merge Preserves Commit History
-------------------

- `git`: A merge operation preserves the original commit history — including the original authors, number of commits, and the individual commit contents from the source branch.
- `svn`: A merge squashes multiple source commits into a single merge commit, effectively destroying the natural commit history.

Preserving the original commit history means you can, without tediously digging through logs:

1. Track how changes evolved over time.
1. See the original author directly from the commit — a sign of respect for contributors.
1. Follow the natural flow of development, which makes it much easier to understand how code details evolved.
1. Quickly identify who made a specific change and when.  
   With `svn`, because merges destroy the natural commit history, tracking down changes is painful.

:beer: Amending Commits
-------------------

- `git`: You can amend commits.  
  Using a feature-branch workflow, you can freely revise commits on your own branch without affecting anyone else.
- `svn`: Once you commit, it's on the server — in practice, it's permanent.  
  (Technically `svn` allows server-side modifications, but the process is complex and requires special permissions, so it never actually happens.)

In practice, accidental commits happen — like committing a log file that shouldn't be there. With `svn`, everyone has to keep seeing that junk commit forever.

Messy commits seriously hurt `Code Review` and raise its cost.

They also get in the way for anyone trying to understand how the code evolved.

:beer: Cheap and Convenient Local Branches
-------------------

- `git`: Has local branches.
- `svn`: Has no local branches.

`git` makes it trivially easy to create local branches, and branch creation is `O(1)` — instantaneous. Because branches can be purely local, there are no SVN-style directory permission issues to worry about.

You can spin up a local branch from any point in the history in the blink of an eye, experiment with uncertain changes locally, and throw the branch away if needed. Branching is so cheap that `git` actively encourages it as the standard way to isolate changes.

:beer: Smarter, More Powerful Merging
----------------

- `git`: A commit that renames a file or directory can still be merged with commits made to that file *before* the rename.
- `svn`: After a rename commit, if you have local changes or branch commits touching the pre-rename filename and try to merge — congratulations :see_no_evil:, you've just hit the legendary ***tree conflict***!

Because of my fear of `svn` ***tree conflicts***, before any package rename (directory rename) or class rename (file rename), I had to broadcast to the whole team:

1. Commit your changes.
1. Stop modifying the affected classes.
1. I'm starting the refactor.
1. Wait until I'm done :scream:, then you can resume.

OMG~ :confounded:~~

Because of how tedious this process is, people become reluctant to do these kinds of refactors at all, which ultimately hurts the overall quality of the codebase.

And don't forget — if your project is open source, contributors come from all over the world. You can't broadcast to all of them :kissing:

:beer: First-Class `tag` Support
-------------------

- `svn` has no real model-level concept of branches or `tag`s. Tags are simulated by setting directory permissions to read-only for developers.
- `git` treats `tag` as a first-class citizen in its model, with true read-only guarantees.

Doesn't that give you a much stronger sense of confidence? :sparkles:

:beer: A Complete Development Ecosystem
-------------------

`github` and `gitlab` (which many companies self-host) — both built around `git` — provide:

- `Markdown`: Efficient document writing and rendering.
- `Issue` & `Milestone`: Bug tracking, task assignment, release planning and management.
- `Wiki`: Structured, organized documentation.
- Comments: Inline comments on commits (i.e., Code Review) and on Issues.  
  Everything is recorded, preserving the communication trail.

Remember: all of the above is managed alongside your code, keeping everything code-centric and making the engineering process easy to navigate.

Working code that delivers the intended functionality (call it the *target deliverable*) is the only true output of the entire project.

Anything that doesn't serve the *target deliverable* is just **noise**.  
\# Doesn't that make you think of certain things — like top-down scheduling plans — that like to present themselves as the real deliverable, as if all that's left is for the developers to crank out code like bricklayers?

:beer: Lightning-Fast Hot Operations
-------------------

### Committing

- `git` commits are local operations — lightning fast compared to `svn`.
- `git` provides a staging area, letting you precisely choose what goes into each commit rather than committing everything at once.  
  PS: `git` can even commit just part of a file's changes (`git add -p`), though this is a bit more involved. (Honestly, I rarely do it in practice :grin:)

This encourages developers to keep commits tidy and self-contained, which in turn benefits:

- `Code Review`
- Fast, precise rollback-based fixes for production `Bug`s

### Viewing Logs

Viewing logs is something you do constantly.

- `git`: The full log is stored locally — instant access, no network required.
- `svn`: Every log lookup requires a round-trip to the server.

Once you've used `git`, waiting for `svn` logs (or diffs between two revisions) is absolutely maddening.
