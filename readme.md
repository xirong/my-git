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

# git 客户端

mac和linux系统推荐使用终端即可，git一开始的命令的确很多，别无它法，熟能生巧，多练习即可能够掌握日常使用的一些名利，再配合[常用命令的alias](https://git-scm.com/book/tr/v2/Git-Basics-Git-Aliases)或者强大的 [`zsh`](https://github.com/robbyrussell/oh-my-zsh)都能显著的提升效率，当然如果非得寻找图形化客户端，也不是没有；windows下还是尽快熟悉客户端的使用吧，因为win下面的bash太难用了：

- [GUI Clients](https://git-scm.com/downloads/guis) 官方推荐图形客户端，罗列的包括了Mac、windows、linux下的客户端，免费及付费的都有，你可以在这里面挑选一个就ok。
- [git for windows](https://msysgit.github.io/) 针对window系统发布的客户端，集成了shell窗口，方便在win下面使用命令操作。
- [TortoiseGit - The coolest Interface to Git Version Control](https://code.google.com/p/tortoisegit/) 在window下使用git，那就不得不提“乌龟”，安装了tortoise后，右键图形化操作根本分辨不出来哪是git，哪是SVN，很方便使用SVN的用户过度过来。
- [Tower2](http://www.git-tower.com/) 号称最好的git客户端，只有Mac版本，收费，集成github、gitlab、Xcode等服务。
- [SourceTree](https://www.sourcetreeapp.com/) 免费，功能齐全，Mac+window版本，集成github等服务。

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

# git 效率提升
- [git flow 工具](https://github.com/petervanderdoes/gitflow)
- [git flow 中文备忘清单](http://danielkummer.github.io/git-flow-cheatsheet/index.zh_CN.html)
- 一个很有意思的学习 git 的小游戏 http://pcottle.github.io/learnGitBranching/ 
- [git completion](https://github.com/git/git/tree/master/contrib/completion) 终端 git 命令的 Tab 键补全功能，比如打开终端，输入`git che`，按 Tab 键，则会出现`check-attr\check-ignore\checkout`等等的选项，支持bash、zsh等shell，使用方法(以bash shell为例)：下载链接中相应的版本到用户目录下，修改`~/.bashrc`文件 ，加入`source ~/git-completion.bash` ，使得每次打开终端时都执行一次`git-completion.bash`脚本，来完成git 命令的 Tab 补全。或者采用这种方法[Quick Tip: Autocomplete Git Commands and Branch Names in Bash](http://code-worrier.com/blog/autocomplete-git/)
- [.gitignore template](https://github.com/github/gitignore) 各种语言、各种编辑器的`.gitignore`文件模板，当你进行某些语言的开发时候，直接使用相应的模板即可，省去自己写的时间（还不全），当然你也可以去贡献自己的模板，不知道`.gitignore`？ 简单讲就是不让git跟踪某些文件，详情阅读：http://git-scm.com/docs/gitignore PS：推荐使用`.gitignore_global`文件进行全局过滤，比如mac下的`.DS_Store`文件，省去在每个repo下进行设置`.gitignore`文件了。全局模板参考：https://github.com/github/gitignore/tree/master/Global

# git extensions
- git 的大文件支持[Git LFS](https://github.com/github/git-lfs) ： git在对大文件进行版本管理的时候，速度上是很慢的，一个帮助处理大文件的扩展插件。


# 最佳实践备注
- 常用命令手册 [git-cheat-sheet && Git常用命令列表](command-handbook/) 
- 总是使用 `git merge --no-ff` 而不是 `git merge` ，记录下分支的变更历史。 详情 http://stackoverflow.com/questions/9069061/what-is-the-difference-between-git-merge-and-git-merge-no-ff
- 恰当的使用 `git pull --rebase` 避免不必要的merge记录。 详情 http://stackoverflow.com/questions/2472254/when-should-i-use-git-pull-rebase
- [git-flight-rules](https://github.com/k88hudson/git-flight-rules) 一些日常使用中的场景，比如提交错了分支、提交时的用户名邮箱不对、丢弃某些提交、未提交的代码直接提交到另外一个分支等等，很实用。
- [How to undo (almost) anything with Git](https://github.com/blog/2019-how-to-undo-almost-anything-with-git) 撤销一切，汇总各种回滚撤销的场景，加强学习。 （[中文翻译版本](http://www.jointforce.com/jfperiodical/article/show/796?m=d03)）

