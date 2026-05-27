English | [中文](zh/readme.md)

# About

This repository is a curated collection of resources for learning Git — the distributed version control system — and GitHub. Most of the content comes from the community; what I've done here is organize it into a coherent learning path. The goal is to take you from zero to confident: starting with the basics, building up practical skills, and eventually understanding how Git works under the hood.

With so many Git articles scattered across the internet, why bother with yet another repo? Because most of them are either too shallow or too narrow. I wanted something comprehensive and well-structured — so I decided to build it myself.

Want to contribute? It's simple: `Fork → Edit → Pull Request`.

# Getting Started
- [Why Git? Git vs. SVN](why-git.md)
- [A Beginner's Guide to Git Resources](ixirong.com.md) — My own introductory writeup. Feedback welcome!
- [GitHub Cheat Sheet](https://github.com/tiimgreen/github-cheat-sheet) — Tips and tricks for Git and GitHub. Also available in [Chinese](https://github.com/tiimgreen/github-cheat-sheet/blob/master/README.zh-cn.md).
- [Git for Beginners: The Definitive Practical Guide (Stack Overflow)](http://stackoverflow.com/questions/315911/git-for-beginners-the-definitive-practical-guide?rq=1) — An excellent community-driven guide. Just open it, read, and practice.
- [Visual Git Cheat Sheet](http://ndpsoftware.com/git-cheatsheet.html) — Organizes common Git commands by workspace: Stash, Workspace, Index, Local Repository, and Upstream Repository. Great for quick reference.

# Git Clients

On macOS and Linux, the terminal is all you need. Yes, the commands can feel overwhelming at first — but there's no shortcut, just practice. Pairing your workflow with [command aliases](https://git-scm.com/book/tr/v2/Git-Basics-Git-Aliases) or a powerful shell like [Oh My Zsh](http://www.ixirong.com/2015/04/27/strong-bash-use-oh-my-zsh/) can make a huge difference. If you prefer a GUI, there are plenty of options. On Windows, a GUI client is especially recommended since the native shell experience leaves a lot to be desired:

- [GUI Clients (Official)](https://git-scm.com/downloads/guis) — The official list of graphical clients for macOS, Windows, and Linux, both free and paid.
- [Git for Windows](https://msysgit.github.io/) — A Windows client with an integrated shell for command-line operations.
- [TortoiseGit](https://code.google.com/p/tortoisegit/) — The classic "Tortoise" right-click integration for Windows. If you're coming from TortoiseSVN, you'll feel right at home.
- [Tower](http://www.git-tower.com/) — Often called the best Git client. macOS only, paid, with GitHub, GitLab, and Xcode integration.
- [SourceTree](https://www.sourcetreeapp.com/) — Free, full-featured, available on macOS and Windows. Integrates with GitHub and other services.
- [SmartGit](http://www.syntevo.com/smartgit/) — Free for non-commercial use, cross-platform, with built-in SSH client and diff/merge tools.
- [Fork](https://git-fork.com) — Free, available on macOS and Windows. Lightweight, fast, and fully featured.

# Branching Strategies
- [A Successful Git Branching Model](http://nvie.com/posts/a-successful-git-branching-model/) — The classic branching model guide. Practice it interactively with [Learn Git Branching](http://pcottle.github.io/learnGitBranching/).
- [Git Workflow Guide](git-workflow-tutorial.md) — A thorough comparison of Centralized (SVN-style), Feature Branch, Gitflow, Forking, and Pull Request workflows. Highly recommended. See the original paginated version at [Git Workflow Translations](https://github.com/oldratlee/translations/tree/master/git-workflows-and-tutorials).
- Ready to collaborate on GitHub? Here's a complete guide: [How to Use GitHub Effectively](how-to-use-github.md).
- [Understanding the GitHub Flow](https://guides.github.com/introduction/flow/index.html) — A concise guide explaining how and why GitHub Flow works.
- [GitHub Collaborative Development Workflow](http://www.ruanyifeng.com/blog/2015/08/git-use-process.html) (Chinese) — Great diagrams, clear and concise.

# Advanced Git
- When your project depends on shared code (common CSS, DLLs, etc.), Git Submodules handle it elegantly. Start with [Git Tools - Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules), then refer to the [Git Submodule Tutorial](https://git.wiki.kernel.org/index.php/GitSubmoduleTutorial) or this [Chinese tutorial](http://www.kafeitu.me/git/2012/03/27/git-submodule.html).
- [Git Submodule Gotchas](http://blog.devtang.com/blog/2013/05/08/git-submodule-issues/) (Chinese) — Important caveats to keep in mind.

# Books
- [Pro Git](http://git-scm.com/book/zh/v1) — Written by Scott Chacon (GitHub employee), widely regarded as the Git bible. Clear illustrations, great for deep learning. The latest English edition: [Pro Git (Edition 2)](http://git-scm.com/book/en/v2).
- [Git Internals (PDF)](https://github.com/pluralsight/git-internals-pdf) — Covers everything from installation to internal design principles. [Direct download](ebooks/git-internals.pdf).
- [Git Community Book](http://gitbook.liuhui998.com/) — A community-curated collection that dives into Git's object model and internals. [Direct download (PDF)](ebooks/Git Community Book.pdf).
- [Git: The Definitive Guide](http://book.douban.com/subject/6526452/) (Chinese) — By Jiang Xin, a version control consultant in China. [About the book](http://www.worldhello.net/gotgit/).
- [Git Reference](http://gitref.org/) ([Chinese](http://gitref.org/zh/index.html)) — A quick-lookup reference for the most essential Git commands.
- [Git Magic (Stanford)](https://github.com/blynn/gitmagic) — A Stanford guide to Git. Great for getting up to speed quickly.

# Productivity Tools
- [Git Flow (CLI tool)](https://github.com/petervanderdoes/gitflow)
- [Git Flow Cheat Sheet](http://danielkummer.github.io/git-flow-cheatsheet/index.zh_CN.html) (Chinese)
- [Learn Git Branching](http://pcottle.github.io/learnGitBranching/) — A fun interactive game for learning Git commands.
- [Git Tab Completion](https://github.com/git/git/tree/master/contrib/completion) — Enables Tab-key autocompletion for Git commands in Bash, Zsh, and other shells. For Bash: download the script, add `source ~/git-completion.bash` to your `~/.bashrc`, and you're set. Alternative setup: [Quick Tip: Autocomplete Git Commands and Branch Names in Bash](http://code-worrier.com/blog/autocomplete-git/).
- [.gitignore Templates](https://github.com/github/gitignore) — Ready-made `.gitignore` files for various languages and editors. Not sure what `.gitignore` does? It tells Git which files to ignore. Details: http://git-scm.com/docs/gitignore
   **Tip:** Use a `.gitignore_global` file for system-wide rules (e.g., macOS `.DS_Store` files) so you don't have to configure each repo individually. Global templates: https://github.com/github/gitignore/tree/master/Global

# Extensions
- [Git LFS](https://github.com/github/git-lfs) — Large File Storage for Git. Git is notoriously slow with large files. As noted in [Working with Large Files (GitHub Help)](https://help.github.com/articles/working-with-large-files/), it's best to avoid versioning large files like logs and databases. When you must, Git LFS is the way to go.

# Practical Tips & Cheat Sheet
- [Everyday Git Commands](useful-git-command.md) — A handy cheat sheet for daily development.
- Always use `git merge --no-ff` instead of `git merge` to preserve branch history. Details: http://stackoverflow.com/questions/9069061/what-is-the-difference-between-git-merge-and-git-merge-no-ff
- Use `git pull --rebase` to keep your history clean and avoid unnecessary merge commits. Details: http://stackoverflow.com/questions/2472254/when-should-i-use-git-pull-rebase — "You should use `git pull --rebase` when your changes do not deserve a separate branch."

- [Git Flight Rules](https://github.com/k88hudson/git-flight-rules) — Real-world scenarios: committed to the wrong branch, wrong user/email, need to discard commits, move uncommitted changes to another branch, and more.
- [How to Undo (Almost) Anything with Git](https://github.com/blog/2019-how-to-undo-almost-anything-with-git) — A comprehensive guide to rolling back and undoing changes.
- [Using GitLab and GitHub on the Same Machine](use-gitlab-github-together.md) — How to manage different SSH keys for your company GitLab and personal GitHub accounts.
- [How to Write a Git Commit Message](http://chris.beams.io/posts/git-commit/) — Seven rules for writing great commit messages.
- [Commit Message and Changelog Conventions](http://www.ruanyifeng.com/blog/2016/01/commit_message_change_log.html) (Chinese) — Good commit logs pay off. See also: [AngularJS Git Commit Message Conventions](https://docs.google.com/document/d/1QrDFcIiPjSLDn3EL15IJygNPiHORgU1_OOAqWjiDU5Y/edit#heading=h.uyo6cb12dt6w).
- [git-recipes](https://github.com/geeeeeeeeek/git-recipes/wiki) (Chinese) — Curated and translated articles by @童仲毅.
- [Githug](https://github.com/Gazler/githug) — Git your game on! Learn Git commands through an interactive adventure game.
