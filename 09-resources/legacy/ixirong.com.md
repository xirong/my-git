English | [中文](zh/ixirong.com.md)

Original post: http://ixirong.com/2014/11/19/the-way-to-learn-git/

## 1. What is Git?

> Git is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.

The [Git Wikipedia page](http://zh.wikipedia.org/wiki/Git) covers Git in depth — its history, usage, and a wealth of reference material. One thing to keep in mind: the most effective way to learn is to **read the documentation**. Going straight to the official docs is the fastest path to mastering Git.

Since Git is a distributed version control system, how does it differ from SVN?

1. **Distributed vs. centralized** — multiple full copies of the repository vs. one central copy. What happens when the central server goes down?
2. **No network required** — you can do version control anytime, anywhere. Want to roll back to a previous version without network access? SVN basically can't do that.
3. **Branching and merging are fast and cheap** — nearly instantaneous, with no real overhead. In SVN, branching is essentially copying the entire codebase.

For a thorough discussion of Git vs. SVN on **Stack Overflow**, see [Why is Git better than Subversion?](http://stackoverflow.com/questions/871/why-is-git-better-than-subversion)

**GitHub** compares the two in terms of repository structure, history, and submodule support: [What are the differences between SVN and Git?](https://help.github.com/articles/what-are-the-differences-between-svn-and-git/)

## 2. Installing Git

*Pro Git* has clear instructions for [installing Git on all platforms](http://git-scm.com/book/zh/v1/%E8%B5%B7%E6%AD%A5-%E5%AE%89%E8%A3%85-Git). If that feels too dense, check out [Liao Xuefeng's Git installation guide](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/00137396287703354d8c6c01c904c7d9ff056ae23da865a000) for a more approachable walkthrough.

## 3. Getting Started with Git

- If you already know SVN, jump straight to [Git - SVN Crash Course](http://git.or.cz/course/svn.html). It maps equivalent SVN commands to their Git counterparts, giving you a quick on-ramp.

- For complete beginners who just want to get something done — initialize a repo, commit, push, create a branch, tag a release — without worrying about internals, this step-by-step illustrated tutorial (using Git on Windows) is a great start: [A Hands-On Guide to Git](http://blog.jobbole.com/78960/)

- For a comprehensive Chinese tutorial series, see [The Clearest Git Tutorial Ever Written!](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)

- After working through the above, you should be able to use Git for everyday tasks. Practice is what turns knowledge into skill. When you're ready to go deeper, the [official Chinese e-book](http://git-scm.com/book/zh/v1) has everything you need — or read the latest [English V2 edition](http://git-scm.com/book/en/v2), available to download as epub or PDF.

## 4. Branches and Tags

One of Git's best features is how it handles branches — fast and effortless. A single command:

``` bash
git branch branch-name
```

creates a new branch in milliseconds. But precisely because it's so easy, poor branch hygiene can lead to **a tangled mess that's impossible to follow**. I recommend reading Ruan Yifeng's article [Git Branching Strategy](http://www.ruanyifeng.com/blog/2012/07/git.html), which is based on the classic post [A successful Git branching model](http://nvie.com/posts/a-successful-git-branching-model/). A Chinese translation is also available on OSChina: [Introducing a Successful Git Branching Model](http://www.oschina.net/translate/a-successful-git-branching-model).

![Messy branches](http://static.ixirong.com/pic/git/git-branchs-messy.webp)

## 5. Common Git Commands

A solid PDF reference for everyday Git commands: [Git Cheat Sheet](http://www.cheat-sheets.org/saved-copy/git-cheat-sheet.pdf). There's also a handy visual summary: [Common Git Commands](http://www.cnblogs.com/1-2-3/archive/2010/07/18/git-commands.html). I've compiled both into an XMind mind map, available on [Baidu Pan](http://pan.baidu.com/s/1c052yVu) (password: `6x7u`) — updated periodically. Preview below:

![Git XMind mind map](http://static.ixirong.com/pic/git/git-xmind.webp)

The most powerful **command reference** of all is right in your terminal: `man git`, `man git <command>`, `git --help`, or `git <command> --help`. Everything you could ever need is there.

## 6. Books and Resources

- **[Pro Git](http://git-scm.com/book/zh/v1)** — Written by Scott Chacon, a GitHub employee and Git evangelist. Widely regarded as the definitive Git learning resource, with clear diagrams throughout. The latest edition is available in English as **[Pro Git (Edition 2)](http://git-scm.com/book/en/v2)**.

- **[Git Community Book](http://gitbook.liuhui998.com/)** — A distillation of community knowledge, including in-depth coverage of Git's object model and internals. Great for understanding how Git works under the hood.

*Added 2015-01-22*
- Recommended workflow guide: [git workflow](http://documentup.com/skwp/git-workflows-book)

*Added 2015-04-05 — git-flow tooling*
- [git-flow tool](https://github.com/nvie/gitflow)
- [git-flow cheat sheet (Chinese)](http://danielkummer.github.io/git-flow-cheatsheet/index.zh_CN.html)
- A fun interactive game for learning Git branching: http://pcottle.github.io/learnGitBranching/
- [Visual Git Guide](http://marklodato.github.io/visual-git-guide/index-zh-cn.html) — explains many Git <code>concepts</code> through diagrams, making them immediately intuitive
- [Git Guide for Absolute Beginners (with illustrations)](http://backlogtool.com/git-guide/cn/) — comprehensive, lively, and easy to follow. Highly recommended!

---

**Finally: once you start using Git, get comfortable with the terminal. Curious about a command? Just run `git branch --help` (or any other command) and let Git explain itself.**
