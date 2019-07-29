原文出自：http://ixirong.com/2014/11/19/the-way-to-learn-git/ 

## 一、什么是git？ 

> Git is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.

[git维基百科](http://zh.wikipedia.org/wiki/Git)上详细介绍了git的资料，包括git的创建、使用以及一些参考资料，已经挺全了，记住一点，最高效的学习方式就是**读文档**，找官方文档去阅读学习是最快的掌握git的方法。

既然是分布式版本管理，那么和我们平常使用的svn有什么区别？
1. 分布式 vs 集中管理 （多份版本库 vs 一份版本库，设想下版本服务器挂了？）
2. 无需网络，随时随地进行版本控制，在没有网络的情况下你想回退到某个版本svn基本没戏；
3. 分支的新建、合并非常方便、快速，没有任何成本，基本不耗时，svn的版本基本上等同于又复制了一份代码；

**stackoverflow** 上关于svn和git的区别的讨论，说的很详细，请参考 [Why is Git better than Subversion?](http://stackoverflow.com/questions/871/why-is-git-better-than-subversion)
**github** 上通过版本库结构、历史、子项目（submudle）的不同来对比两者，请参考 [What are the differences between SVN and Git?](https://help.github.com/articles/what-are-the-differences-between-svn-and-git/)

## 二、git 安装
 《pro git》一书中已经写明白了[各个平台上怎么安装git](http://git-scm.com/book/zh/v1/%E8%B5%B7%E6%AD%A5-%E5%AE%89%E8%A3%85-Git),如果感觉晦涩，就看这个[廖雪峰安装git](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/00137396287703354d8c6c01c904c7d9ff056ae23da865a000)

## 三、git 初使用
- 对于已经熟悉svn的用户可以直接查看此文档 [Git - SVN Crash Course](http://git.or.cz/course/svn.html)，通过对比两个工具对同样的操作采取不同的命令来快速认识git的一些常用命令

- 对于一个新手来说，我不需要知道git的原理，不需要知道git那么多的命令，我只想用git完成一次仓库的从初始化、commit、push、branch、tag等一个流程，越简单越好，图文教程，以window下使用git为例，一步步走完整个流程，推荐 [手把手教你使用Git](http://blog.jobbole.com/78960/)

- 比较全面讲述的git的系列文章 [号称史上最浅显易懂的Git教程！](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)

- 看完上面的几步内容，想你习对git基本上可以使用了，要掌握还得多多练习，熟能生巧，你是不是想去看看关于git的全部内容 ，[官方中文电子版书籍](http://git-scm.com/book/zh/v1)即可满足你，当然你可以查看最新[V2版英文](http://git-scm.com/book/en/v2)或者下载epub pdf等本地阅读；

## 四、git 分支、tag
git 最帅气的就是对分支的处理，方便快速，你只需要一个简单的
``` bash
git branch branch-name
```
就能开出一个叫branch-name的分支，毫秒钟搞定，但也正是因为方便，如果使用不合理就会造成**分支混乱，分不清脉络**， 推荐看一下阮一峰写的文章 [Git分支管理策略](http://www.ruanyifeng.com/blog/2012/07/git.html) ，最原始的文章就是这篇老外写的[A successful Git branching model](http://nvie.com/posts/a-successful-git-branching-model/)，[@萌面大叔的乌托邦]()提到开源中国已经翻译成了中文，感兴趣的可以去看看[介绍一个成功的 Git 分支模型](http://www.oschina.net/translate/a-successful-git-branching-model)

![杂乱的分支](http://static.ixirong.com/pic/git/git-branchs-messy.webp)

## 五、git 常见命令
一个比较好的汇总了git的一些基本命令的pdf，可以经常看看，或者当成命令手册，推荐 [Git Cheat Sheet](http://www.cheat-sheets.org/saved-copy/git-cheat-sheet.pdf) ，还有一张图片 [Git常用命令](http://www.cnblogs.com/1-2-3/archive/2010/07/18/git-commands.html) 也不错；最近我整理了一份xmind的导图，将**这两份**资料都放到了画布里面，[百度网盘](http://pan.baidu.com/s/1c052yVu) 密码：`6x7u` 存储了，不断更新，有需要的可以下载，预览图片如下：

![Git常用xmind导图整理](http://static.ixirong.com/pic/git/git-xmind.webp)

最强大的**命令手册**还得属于终端，* man git * 或者 * man git 命令 * 或者 * git --help * 或者 * git 命令 --help *，在这里可以找到任何你想要的。

## 六、git 书籍资料
-《[Pro Git](http://git-scm.com/book/zh/v1)》 作者Scott Chacon是github的员工，git的布道者，这本书被誉为git学习圣经，中间有好多插图描述的浅显易懂，挺适合详细学习下的，最新英文第二版《[pro git (Editon 2)](http://git-scm.com/book/en/v2)》；

-《[Git Community Book](http://gitbook.liuhui998.com/)》汇聚了Git社区的很多精华,  并对git的对象模型原理等做了解释，可以深入的了解下git原理；

2015-01-22 增加
- 推荐的工作流程 [git workflow](http://documentup.com/skwp/git-workflows-book) 

2015-04-05 增加 git flow 工具
- [git flow 工具](https://github.com/nvie/gitflow)
- [git flow 中文备忘清单](http://danielkummer.github.io/git-flow-cheatsheet/index.zh_CN.html)
- 一个很有意思的学习 git 的小游戏 http://pcottle.github.io/learnGitBranching/ 
- [图解 git](http://marklodato.github.io/visual-git-guide/index-zh-cn.html) 将书籍中很多<code>术语</code>用图片的方式进行讲解，很容易就懂了 
- [图文并茂-猴子都能懂的git入门教程](http://backlogtool.com/git-guide/cn/) 全面，生动形象，图文并茂，简单易懂，强烈推荐！



关于日常中使用git来版本管理的流程写的很不错的一本书，日常工作模式、流程怎样更合理的工作！
** 最后，当你开始使用git的时候，学会用终端，比如你想看关于branch，那么大胆的时候 *git branch --help * 查看相应的命令！ **
