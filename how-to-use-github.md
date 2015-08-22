
说明
==============
作为一名开发者，Github上面有很多东西值得关注学习，可是刚刚接触github，怎样一步步学习使用Github？怎样更高效的利用Github？
在这里搜集整理网络上面的资料，汇总成这么一篇repo 《Github使用指南》，供大家一起学习。 :octocat:

- [github 入门使用教程-图文并茂](http://developer.51cto.com/art/201407/446249_all.htm) 很简洁的说明如何使用，看图即可明白。	
- [github help](https://help.github.com/) Sometimes you just need a little help. 中文翻译版在此[Github 帮助文档](https://github.com/waylau/github-help)。
- [github 之 fork 简介指南](https://linux.cn/article-4292-1.html) 帮你理解清楚什么是fork，fork 的工作流有哪些。
- [github-cheat-sheet](https://github.com/tiimgreen/github-cheat-sheet) 关于使用 git 和 github 的一些技巧汇总，中文版在此[GitHub秘籍](https://github.com/tiimgreen/github-cheat-sheet/blob/master/README.zh-cn.md)
- [The GitHub Blog](https://github.com/blog) github 官方博客，关注最新动态。
- [How to Build a GitHub](http://zachholman.com/talk/how-to-build-a-github/) Github一名早期员工介绍Github的历史，5年108名员工无人离职。
- [阳志平：如何高效利用GitHub](http://www.yangzhiping.com/tech/github.html) 介绍的挺全，以及一些用法，如怎样利用Github来学习、演讲找工作等。
- [github 支持的 emoji表情 emoji-cheat-sheet](http://www.emoji-cheat-sheet.com/) :v: :clap:  感觉不好找到需要的表情？试试[Emoji Searcher](http://emoji.muan.co/) 
- [github guides](https://guides.github.com/) 从`Contributing to Open Source on GitHub`、`Hello World`、`Forking Projects`、`Be Social`、`Making Your Code Citable`、`Mastering Issues`、`Mastering Markdown`、`Mastering Wikis`、`Getting Started with GitHub Pages` 等9个方面图文详细讲解每一步如何使用，以及能做哪些功能。
- [fork-me-on-github](https://github.com/blog/273-github-ribbons) 个人博客、技术博客等如果需要添加github 的彩带，可以使用此方法。
- [蒋鑫-GotGitHub](GotGitHub.md) 《Git权威指南》的作者，对Github有很深的了解。（由于首页打开太慢，放到了本文目录中，下面的文章既是）

# Github Skills

- [Using Git blame to trace changes in a file](https://help.github.com/articles/using-git-blame-to-trace-changes-in-a-file/) 如果你想看某一个文件中每一行是谁修改的，为什么修改？那么尽情的使用 `blame` 按钮，发现文件的历史。
- [Github 搜索技巧](https://help.github.com/categories/search/)
- [Closing issues via commit messages - 通过提交信息关闭Issues](https://help.github.com/articles/closing-issues-via-commit-messages/)
- [Update your forked code from original repository - 如何更新自己 Fork 的代码](https://github.com/ysc/APDPlat/wiki/%E5%A6%82%E4%BD%95%E6%9B%B4%E6%96%B0%E8%87%AA%E5%B7%B1Fork%E7%9A%84%E4%BB%A3%E7%A0%81)

更多关于 Github 的内容请查看：[GithubHelp](https://help.github.com/) 查找需要的信息。

-------- 

原文地址：http://www.worldhello.net/gotgithub/index.html

<h1 style="margin:0px;padding:0.7em 0px 0.3em;font-size:1.5em;color:rgb(17, 85, 124);">GotGitHub<a href="http://www.worldhello.net/gotgithub/#gotgithub" title="永久链接至标题" style="color:black;text-decoration:none;font-weight:normal;visibility:hidden;font-size:1em;margin-left:6px;padding:0px 4px;">¶</a></h1>
<table style="font-size:inherit;font-weight:inherit;font-style:inherit;font-variant:inherit;border-collapse:collapse;margin:0px -0.5em;border:0px;">
<colgroup><col/>
<col/>
</colgroup><tbody valign="top">
<tr><th style="text-align:left;padding:1px 8px 1px 5px;border:0px;">Author:</th><td style="padding:1px 8px 1px 5px;text-align:left;border:0px;">Jiang Xin</td>
</tr>
<tr><th style="text-align:left;padding:1px 8px 1px 5px;border:0px;">Version:</th><td style="padding:1px 8px 1px 5px;text-align:left;border:0px;">v0.9.1-13-g5075479</td>
</tr>
<tr><th style="text-align:left;padding:1px 8px 1px 5px;border:0px;">Copyright:</th><td style="padding:1px 8px 1px 5px;text-align:left;border:0px;"><a href="http://creativecommons.org/licenses/by-nc-sa/3.0/" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">Creative Commons BY-NC-SA</a></td>
</tr>
</tbody>
</table>
<div>
<h2 style="margin:1.3em 0px 0.2em;font-size:1.35em;padding:0px;">前言<a href="http://www.worldhello.net/gotgithub/#id1" title="永久链接至标题" style="color:black;text-decoration:none;font-weight:normal;visibility:hidden;font-size:1em;margin-left:6px;padding:0px 4px;">¶</a></h2>
<p style="margin:0.8em 0px 0.5em;">动笔写GitHub不是因为我对其了解，恰恰是对其太不了解。</p>
<p style="margin:0.8em 0px 0.5em;">在我的《Git权威指南》 <a href="http://www.worldhello.net/gotgithub/#id4" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;font-size:smaller;line-height:0;vertical-align:super;margin:0px;">[1]</a> 一书中，涉及到GitHub的只有区区三页纸，这显然回答不了读者对于GitHub的诸多疑问。
记得在《Git权威指南》刚刚完稿之际，机械工业出版社华章公司的杨福川编辑就鼓动我写一本关于GitHub的书，我用了好多理由推辞了。
头条理由就是我真的累着了。在每一章节开始动笔之时，都好像是坐在了中学语文考试的考堂上写作文，时间快到了可仍然动不了笔，
再写一本书无疑要重复这一痛苦的经历。
第二个理由是我更喜欢编程，而不是写文档，尤其写GitHub会有大量截图、图像处理的琐碎工作。
第三个理由彻底让编辑投降，那就是GitHub是一个国外网站，也许书一出，【此句已被原作者删除】。</p>
<p style="margin:0.8em 0px 0.5em;">让我最终决定动笔，是源于CSDN蒋总在美国拜访GitHub总部后告诉我的一些见闻，我对GitHub如此成功运作产生了兴趣，于是开始研究GitHub的博客，愈发发现GitHub是一群有趣的人在做的有趣的事，如果只把GitHub当作一个Git服务器，实在是暴殄天物。GitHub已经并将继续获得成功，若真能凭借此书把GitHub尽量全面地展现，让每一个Git使用者用好GitHub也是一件幸事。</p>
<p style="margin:0.8em 0px 0.5em;">这本书将采用GitHub的方式进行撰写和发布 <a href="http://www.worldhello.net/gotgithub/#id5" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;font-size:smaller;line-height:0;vertical-align:super;margin:0px;">[2]</a> ，任何人都可以看到本书（包括源码），更可以用GitHub的方法参与本书的撰写和纠错。网络出版对于我和杨福川编辑都是一个全新的体验。感谢Git，让我在一年内拥有了两种不同的出版体验。</p>
<p style="margin:0.8em 0px 0.5em;">– 蒋鑫, 2011.12</p>
<hr style="border:1px solid rgb(170, 187, 204);margin:2em;"/>
<table style="font-size:inherit;font-weight:inherit;font-style:inherit;font-variant:inherit;border-collapse:collapse;margin:0px -0.5em;border:0px;">
<colgroup><col/><col/></colgroup>
<tbody valign="top">
<tr><td style="padding:1px 8px 1px 5px;text-align:left;border:0px;"><a href="http://www.worldhello.net/gotgithub/#id2" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">[1]</a></td><td style="padding:1px 8px 1px 5px;text-align:left;border:0px;"><a href="http://www.worldhello.net/gotgit/" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">http://www.worldhello.net/gotgit/</a></td></tr>
</tbody>
</table>
<table style="font-size:inherit;font-weight:inherit;font-style:inherit;font-variant:inherit;border-collapse:collapse;margin:0px -0.5em;border:0px;">
<colgroup><col/><col/></colgroup>
<tbody valign="top">
<tr><td style="padding:1px 8px 1px 5px;text-align:left;border:0px;"><a href="http://www.worldhello.net/gotgithub/#id3" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">[2]</a></td><td style="padding:1px 8px 1px 5px;text-align:left;border:0px;"><a href="https://github.com/gotgit/gotgithub" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">https://github.com/gotgit/gotgithub</a></td></tr>
</tbody>
</table>
</div>
<div>
<h2 style="margin:1.3em 0px 0.2em;font-size:1.35em;padding:0px;">目录<a href="http://www.worldhello.net/gotgithub/#id6" title="永久链接至标题" style="color:black;text-decoration:none;font-weight:normal;visibility:hidden;font-size:1em;margin-left:6px;padding:0px 4px;">¶</a></h2>
<div>
<ul>
<li><a href="http://www.worldhello.net/gotgithub/01-explore-github/index.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">1. 探索GitHub</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/01-explore-github/010-what-is-github.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">1.1. 什么是GitHub</a></li>
<li><a href="http://www.worldhello.net/gotgithub/01-explore-github/020-github-hightlights.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">1.2. GitHub亮点</a></li>
<li><a href="http://www.worldhello.net/gotgithub/01-explore-github/030-explore-github.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">1.3. 探索GitHub</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/02-join-github/index.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">2. 加入GitHub</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/02-join-github/010-account-setup.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">2.1. 创建GitHub账号</a></li>
<li><a href="http://www.worldhello.net/gotgithub/02-join-github/020-browse-repo.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">2.2. 浏览托管项目</a></li>
<li><a href="http://www.worldhello.net/gotgithub/02-join-github/030-be-social.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">2.3. 社交网络</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/index.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3. 项目托管</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/010-new-project.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.1. 创建新项目</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/010-new-project.html#new-repo" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.1.1. 新版本库即是新项目</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/010-new-project.html#init-by-clone" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.1.2. 版本库初始化</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/010-new-project.html#init-by-push" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.1.3. 从已有版本库创建</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/020-repo-operation.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.2. 操作版本库</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/020-repo-operation.html#noff-push" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.2.1. 强制推送</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/020-repo-operation.html#new-branch" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.2.2. 新建分支</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/020-repo-operation.html#default-branch" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.2.3. 设置默认分支</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/020-repo-operation.html#del-branch" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.2.4. 删除分支</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/020-repo-operation.html#git-tags" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.2.5. 里程碑管理</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/030-repo-authz.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.3. 公钥认证管理</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/030-repo-authz.html#pubkeys" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.3.1. 用户级公钥管理</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/030-repo-authz.html#deploy-keys" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.3.2. 项目级公钥管理</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/040-repo-hooks.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.4. 版本库钩子扩展</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/040-repo-hooks.html#mail-notify-hook" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.4.1. 邮件通知功能</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/040-repo-hooks.html#redmine" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.4.2. 和Redmine整合</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/050-homepage.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.5. 建立主页</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/050-homepage.html#user-homepage" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.5.1. 创建个人主页</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/050-homepage.html#project-homepage" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.5.2. 创建项目主页</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/050-homepage.html#dedicate-domain" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.5.3. 使用专有域名</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/050-homepage.html#jekyll" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.5.4. 使用Jekyll维护网站</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/index.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4. 工作协同</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/010-fork-and-pull.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.1. Fork + Pull模式</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/010-fork-and-pull.html#fork" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.1.1. 版本库派生</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/010-fork-and-pull.html#pull-request" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.1.2. Pull Request</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/010-fork-and-pull.html#merge-by-hands" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.1.3. 手工合并</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/010-fork-and-pull.html#online-edit" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.1.4. 在线编辑</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/010-fork-and-pull.html#fork-pull-request" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.1.5. 简化的 Fork + Pull Request</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/020-shared-repo.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.2. 共享版本库</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/020-shared-repo.html#collaborators" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.2.1. 版本库授权</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/020-shared-repo.html#central-model" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.2.2. 与传统集中式工作模式的异同</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/020-shared-repo.html#merge-and-push" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.2.3. 合并后推送</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/020-shared-repo.html#rebase-and-push" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.2.4. 合并还是变基</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/030-organization.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.3. 组织和团队</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/030-organization.html#new-org" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.3.1. 创建新组织</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/030-organization.html#org-settings" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.3.2. 组织管理</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/030-organization.html#org-repo-mgmt" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.3.3. 版本库管理</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/030-organization.html#pros-of-org" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.3.4. 个人还是组织</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/040-code-review.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.4. 代码评注</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/040-code-review.html#commit-comments" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.4.1. 提交评注</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/040-code-review.html#line-comments" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.4.2. 逐行评注</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/050-issue.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.5. 缺陷跟踪</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/050-issue.html#labels" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.5.1. 标签</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/050-issue.html#milestone" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.5.2. 里程碑</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/050-issue.html#issue" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.5.3. Issue的生命周期</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/050-issue.html#pull-requstissue" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.5.4. Pull Requst也是Issue</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/060-wiki.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.6. 维基</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/060-wiki.html#wiki-init" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.6.1. 维基初始化</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/060-wiki.html#use-wiki" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.6.2. 使用维基</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/060-wiki.html#git" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.6.3. 维基与Git</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/05-commercial-github/index.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">5. 付费服务</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/05-commercial-github/non-free-plans.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">5.1. GitHub收费方案</a></li>
<li><a href="http://www.worldhello.net/gotgithub/05-commercial-github/github-enterprise.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">5.2. GitHub企业版</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/index.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6. GitHub副产品</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/gist.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.1. GitHub:Gist</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/gist.html#paste" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.1.1. 数据的粘贴和引用</a></li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/gist.html#gistgit" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.1.2. Gist背后的Git库</a></li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/gist.html#greasemonkey" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.1.3. Greasemonkey</a></li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/gist.html#gist-cli" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.1.4. 命令行操作Gist</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/other-scm.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.2. 其他版本控制工具支持</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/svn.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.2.1. 用SVN操作GitHub</a></li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/hg-git.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.2.2. 用Hg操作GitHub</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/tools.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.3. 客户端工具</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/github-mac.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.3.1. github:mac</a></li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/hub.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.3.2. hub</a></li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/ios.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.3.3. iOS应用</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/others.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.4. 其他</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/jobs.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.4.1. GitHub:Jobs</a></li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/shop.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.4.2. GitHub:Shop</a></li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/short-url.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.4.3. GitHub短网址服务</a></li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/opensource.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.4.4. GitHub Open Source</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/appendix/markups.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">7. 附录：轻量级标记语言</a></li>
</ul>
</div>

