# 说明
这整个 repository 是关于分布式版本管理工具 Git 及托管商github 的使用，大部分都是网友写的内容，在这里只是做一个资源的汇总和合理的安排，希望能成为最好的学习 git 的资源，从开始入门使用，到慢慢的提高，再到理解各种原理，希望能够达成这个目标。

网络上面已经有了那么多的关于git的文章，为什么还要弄一个repo来专门记录？网上的文章都是片面的，稍微全点的讲解的不够全面、深入，没能满足我对于文章的想象，所以决定自己来写。

怎么写？
每个介绍的后面都应该有一些实践练习，有原理的部分，也应该有实践，手把手教学，这样子才能适合初学来快速上手学习。

如果你要有一些资源，希望和我一起，把这个搞起来，很简单，`fork-修改-pull request` 就ok。

# 入门介绍资料
- [为什么开始使用Git版本管理，Git VS SVN 有哪些区别？](https://github.com/xirong/my-git/blob/master/why-git.md)
- [开篇：一篇适合入门学习git的资料汇总](https://github.com/xirong/my-git/blob/master/ixirong.com.md) 本人的拙笔，欢迎吐槽！
- [github-cheat-sheet](https://github.com/tiimgreen/github-cheat-sheet) 关于使用 git 和 github 的一些技巧汇总，中文版在此[GitHub秘籍](https://github.com/tiimgreen/github-cheat-sheet/blob/master/README.zh-cn.md)
- [Git for beginners: The definitive practical guide - from stackoverflow.com](http://stackoverflow.com/questions/315911/git-for-beginners-the-definitive-practical-guide?rq=1)  It's so useful to a beginner ,just open the url , read and practice . 

# git branch 
- [A successful Git branching model](http://nvie.com/posts/a-successful-git-branching-model/) 介绍日常推荐的分支开发模型，基于此模型可以通过这个小游戏来进行学习 [Learn Git Branch](http://pcottle.github.io/learnGitBranching/)
- [git工作流指南](https://github.com/xirong/my-git/blob/master/workflow-translations.md)完整的对比目前使用的集中式（svn）工作流、功能分支工作流、gitflow工作流、forking工作流、pull request 等几种不同的模式，通俗易懂，强烈推荐看一看，如果觉的排版不好，请查看原分页文章 [git-workflow-translations](https://github.com/oldratlee/translations/tree/master/git-workflows-and-tutorials) 
- 熟悉的工作流后，你是否也想要在github上与他人一起协同工作？那么问题来了，[Github全程指南-如何高效使用？](how-to-use-github.md)

# git expert 
- 项目依赖其他项目，比如公共css、dll等等，强大的git-submodule 优雅的解决这类问题。理解阅读 [Git Tools - Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) ，备忘或者查看命令阅读[Git Submodule Tutorial](https://git.wiki.kernel.org/index.php/GitSubmoduleTutorial) 或者 [Git Submodule使用完整教程](http://www.kafeitu.me/git/2012/03/27/git-submodule.html)


# git 书籍
- [Pro Git](http://git-scm.com/book/zh/v1) 作者Scott Chacon是github的员工，git的布道者，这本书被誉为git学习圣经，中间有好多插图描述的浅显易懂，挺适合详细学习下的，最新英文第二版《[pro git (Editon 2)](http://git-scm.com/book/en/v2)》；
- [git-internals-pdf](https://github.com/pluralsight/git-internals-pdf) 老外写的，很给力，蒋鑫推荐，从目录上面包括安装使用以及设计原理都有讲解，有机会看看。pdf电子版本直接下载地址 [git-internals.pdf](ebooks/git-internals.pdf)
- [Git Community Book](http://gitbook.liuhui998.com/) 汇聚了Git社区的很多精华,  并对git的对象模型原理等做了解释，可以深入的了解下git原理。pdf电子版本直接下载地址 [Git Community Book.pdf](ebooks/Git Community Book.pdf)

# git 工具
- [git flow 工具](https://github.com/nvie/gitflow)
- [git flow 中文备忘清单](http://danielkummer.github.io/git-flow-cheatsheet/index.zh_CN.html)
- 一个很有意思的学习 git 的小游戏 http://pcottle.github.io/learnGitBranching/ 

# 最佳实践备注
- 常用命令手册 [git-cheat-sheet && Git常用命令列表](command-handbook/) 
- 总是使用 `git merge --no-ff` 而不是 `git merge` ，记录下分支的变更历史。 详情 http://stackoverflow.com/questions/9069061/what-is-the-difference-between-git-merge-and-git-merge-no-ff
- 恰当的使用 `git pull --rebase` 避免不必要的merge记录。 详情 http://stackoverflow.com/questions/2472254/when-should-i-use-git-pull-rebase