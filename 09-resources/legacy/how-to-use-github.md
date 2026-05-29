English | [中文](zh/how-to-use-github.md)

Overview
==============
As a developer, there is a lot worth learning and paying attention to on GitHub. But when you are just getting started, how do you learn to use GitHub step by step? How do you make better use of it?

This repo — *GitHub Usage Guide* — collects and organizes resources from around the web to help everyone learn together. :octocat:

- [GitHub Getting Started Tutorial — Illustrated](http://developer.51cto.com/art/201407/446249_all.htm) A concise guide on how to use GitHub. The screenshots alone make it easy to follow.
- [GitHub Help](https://help.github.com/) Sometimes you just need a little help. A Chinese translation is available here: [GitHub Help Docs](https://github.com/waylau/github-help).
- [Introduction to GitHub Forks](https://linux.cn/article-4292-1.html) Helps you understand what a fork is and what fork-based workflows look like.
- [GitHub-cheat-sheet](https://github.com/tiimgreen/github-cheat-sheet) A collection of tips and tricks for using Git and GitHub. Chinese version: [GitHub Secrets](https://github.com/tiimgreen/github-cheat-sheet/blob/master/README.zh-cn.md).
- [The GitHub Blog](https://github.com/blog) The official GitHub blog — follow it to stay up to date.
- [How to Build a GitHub](http://zachholman.com/talk/how-to-build-a-github/) An early GitHub employee talks about the company's history: 108 employees over 5 years with zero turnover.
- [Yang Zhiping: How to Get the Most Out of GitHub](http://www.yangzhiping.com/tech/github.html) A thorough overview of GitHub, including how to use it for learning, giving talks, and job hunting.
- [GitHub-supported Emoji — emoji-cheat-sheet](http://www.emoji-cheat-sheet.com/) :v: :clap: Having trouble finding the emoji you need? Try [Emoji Searcher](http://emoji.muan.co/).
- [x] [GitHub Guides](https://guides.github.com/) Step-by-step illustrated walkthroughs covering 9 topics: `Contributing to Open Source on GitHub`, `Hello World`, `Forking Projects`, `Be Social`, `Making Your Code Citable`, `Mastering Issues`, `Mastering Markdown`, `Mastering Wikis`, and `Getting Started with GitHub Pages`.
- [Fork Me on GitHub](https://github.com/blog/273-github-ribbons) If you want to add a GitHub ribbon to your personal or technical blog, this is how.
- [Jiang Xin — GotGitHub](GotGitHub.md) The author of *Pro Git* (Chinese edition), with deep expertise in GitHub. (The original page loaded too slowly, so the content has been included directly in this repo — see the article below.)

# GitHub Skills

- [Using Git blame to trace changes in a file](https://help.github.com/articles/using-git-blame-to-trace-changes-in-a-file/) Want to see who changed each line in a file, and why? Use the `blame` button to uncover a file's history.
- [GitHub Search Tips](https://help.github.com/categories/search/)
- [Closing issues via commit messages](https://help.github.com/articles/closing-issues-via-commit-messages/)
- [How to update your forked code from the original repository](https://github.com/ysc/APDPlat/wiki/%E5%A6%82%E4%BD%95%E6%9B%B4%E6%96%B0%E8%87%AA%E5%B7%B1Fork%E7%9A%84%E4%BB%A3%E7%A0%81)

For more GitHub content, visit [GitHub Help](https://help.github.com/) to find what you need.

-------- 

Original source: http://www.worldhello.net/gotgithub/index.html

<h1 style="margin:0px;padding:0.7em 0px 0.3em;font-size:1.5em;color:rgb(17, 85, 124);">GotGitHub<a href="http://www.worldhello.net/gotgithub/#gotgithub" title="Permalink to this heading" style="color:black;text-decoration:none;font-weight:normal;visibility:hidden;font-size:1em;margin-left:6px;padding:0px 4px;">¶</a></h1>
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
<h2 style="margin:1.3em 0px 0.2em;font-size:1.35em;padding:0px;">Preface<a href="http://www.worldhello.net/gotgithub/#id1" title="Permalink to this heading" style="color:black;text-decoration:none;font-weight:normal;visibility:hidden;font-size:1em;margin-left:6px;padding:0px 4px;">¶</a></h2>
<p style="margin:0.8em 0px 0.5em;">I started writing about GitHub not because I know it well, but precisely because I did not know it well enough.</p>
<p style="margin:0.8em 0px 0.5em;">In my book <em>Pro Git</em> <a href="http://www.worldhello.net/gotgithub/#id4" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;font-size:smaller;line-height:0;vertical-align:super;margin:0px;">[1]</a>, GitHub received only a mere three pages — clearly not enough to answer readers' many questions about it.
I remember that just as I was finishing <em>Pro Git</em>, Yang Fuchuan, an editor at China Machine Press's Huazhang imprint, urged me to write a book about GitHub. I turned him down with many excuses.
The main one was that I was genuinely exhausted. Every time I sat down to start a new chapter, it felt like sitting in a high school Chinese exam, staring at the blank page as the clock ticked down.
Writing another book would mean repeating that misery.
The second reason was that I much prefer coding to writing documentation, and a book about GitHub would involve an enormous amount of tedious screenshot-taking and image editing.
The third reason finally made the editor give up: GitHub is a foreign website, and once the book came out, [this sentence has been deleted by the original author].</p>
<p style="margin:0.8em 0px 0.5em;">What ultimately convinced me to write was something the head of CSDN told me after visiting GitHub's headquarters in the United States. His account sparked my curiosity about how GitHub had achieved such remarkable success. I started reading the GitHub blog and discovered, more and more, that GitHub is a fascinating thing built by fascinating people. To treat GitHub as nothing more than a Git server would be a terrible waste. GitHub has succeeded and will continue to succeed, and if this book can present it as fully as possible and help every Git user get more out of GitHub, that would be a worthy outcome.</p>
<p style="margin:0.8em 0px 0.5em;">This book is being written and published the GitHub way <a href="http://www.worldhello.net/gotgithub/#id5" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;font-size:smaller;line-height:0;vertical-align:super;margin:0px;">[2]</a>. Anyone can read it (including the source), and anyone can contribute corrections or additions the GitHub way. Online publishing is a completely new experience for both me and editor Yang Fuchuan. Thank you, Git, for giving me two very different publishing experiences within a single year.</p>
<p style="margin:0.8em 0px 0.5em;">– Jiang Xin, December 2011</p>
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
<h2 style="margin:1.3em 0px 0.2em;font-size:1.35em;padding:0px;">Table of Contents<a href="http://www.worldhello.net/gotgithub/#id6" title="Permalink to this heading" style="color:black;text-decoration:none;font-weight:normal;visibility:hidden;font-size:1em;margin-left:6px;padding:0px 4px;">¶</a></h2>
<div>
<ul>
<li><a href="http://www.worldhello.net/gotgithub/01-explore-github/index.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">1. Exploring GitHub</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/01-explore-github/010-what-is-github.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">1.1. What is GitHub</a></li>
<li><a href="http://www.worldhello.net/gotgithub/01-explore-github/020-github-hightlights.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">1.2. GitHub Highlights</a></li>
<li><a href="http://www.worldhello.net/gotgithub/01-explore-github/030-explore-github.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">1.3. Exploring GitHub</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/02-join-github/index.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">2. Joining GitHub</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/02-join-github/010-account-setup.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">2.1. Creating a GitHub Account</a></li>
<li><a href="http://www.worldhello.net/gotgithub/02-join-github/020-browse-repo.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">2.2. Browsing Hosted Projects</a></li>
<li><a href="http://www.worldhello.net/gotgithub/02-join-github/030-be-social.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">2.3. Social Networking</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/index.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3. Project Hosting</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/010-new-project.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.1. Creating a New Project</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/010-new-project.html#new-repo" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.1.1. A New Repository Is a New Project</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/010-new-project.html#init-by-clone" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.1.2. Initializing a Repository</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/010-new-project.html#init-by-push" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.1.3. Creating from an Existing Repository</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/020-repo-operation.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.2. Repository Operations</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/020-repo-operation.html#noff-push" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.2.1. Force Push</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/020-repo-operation.html#new-branch" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.2.2. Creating a Branch</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/020-repo-operation.html#default-branch" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.2.3. Setting the Default Branch</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/020-repo-operation.html#del-branch" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.2.4. Deleting a Branch</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/020-repo-operation.html#git-tags" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.2.5. Tag Management</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/030-repo-authz.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.3. Public Key Authentication</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/030-repo-authz.html#pubkeys" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.3.1. User-level Key Management</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/030-repo-authz.html#deploy-keys" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.3.2. Project-level Key Management</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/040-repo-hooks.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.4. Repository Hook Extensions</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/040-repo-hooks.html#mail-notify-hook" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.4.1. Email Notification</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/040-repo-hooks.html#redmine" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.4.2. Integration with Redmine</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/050-homepage.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.5. Setting Up a Homepage</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/050-homepage.html#user-homepage" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.5.1. Creating a Personal Homepage</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/050-homepage.html#project-homepage" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.5.2. Creating a Project Homepage</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/050-homepage.html#dedicate-domain" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.5.3. Using a Custom Domain</a></li>
<li><a href="http://www.worldhello.net/gotgithub/03-project-hosting/050-homepage.html#jekyll" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">3.5.4. Maintaining the Site with Jekyll</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/index.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4. Collaboration</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/010-fork-and-pull.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.1. Fork + Pull Model</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/010-fork-and-pull.html#fork" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.1.1. Forking a Repository</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/010-fork-and-pull.html#pull-request" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.1.2. Pull Request</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/010-fork-and-pull.html#merge-by-hands" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.1.3. Manual Merge</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/010-fork-and-pull.html#online-edit" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.1.4. Online Editing</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/010-fork-and-pull.html#fork-pull-request" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.1.5. Simplified Fork + Pull Request</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/020-shared-repo.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.2. Shared Repository</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/020-shared-repo.html#collaborators" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.2.1. Repository Authorization</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/020-shared-repo.html#central-model" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.2.2. Comparison with Traditional Centralized Workflows</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/020-shared-repo.html#merge-and-push" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.2.3. Merge Then Push</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/020-shared-repo.html#rebase-and-push" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.2.4. Merge or Rebase</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/030-organization.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.3. Organizations and Teams</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/030-organization.html#new-org" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.3.1. Creating a New Organization</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/030-organization.html#org-settings" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.3.2. Managing an Organization</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/030-organization.html#org-repo-mgmt" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.3.3. Repository Management</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/030-organization.html#pros-of-org" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.3.4. Personal Account or Organization</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/040-code-review.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.4. Code Review</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/040-code-review.html#commit-comments" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.4.1. Commit Comments</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/040-code-review.html#line-comments" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.4.2. Line-by-line Comments</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/050-issue.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.5. Issue Tracking</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/050-issue.html#labels" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.5.1. Labels</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/050-issue.html#milestone" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.5.2. Milestones</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/050-issue.html#issue" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.5.3. The Issue Lifecycle</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/050-issue.html#pull-requstissue" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.5.4. Pull Requests Are Issues Too</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/060-wiki.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.6. Wiki</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/060-wiki.html#wiki-init" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.6.1. Initializing the Wiki</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/060-wiki.html#use-wiki" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.6.2. Using the Wiki</a></li>
<li><a href="http://www.worldhello.net/gotgithub/04-work-with-others/060-wiki.html#git" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">4.6.3. Wiki and Git</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/05-commercial-github/index.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">5. Paid Services</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/05-commercial-github/non-free-plans.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">5.1. GitHub Paid Plans</a></li>
<li><a href="http://www.worldhello.net/gotgithub/05-commercial-github/github-enterprise.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">5.2. GitHub Enterprise</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/index.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6. GitHub Offshoots</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/gist.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.1. GitHub: Gist</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/gist.html#paste" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.1.1. Pasting and Embedding Data</a></li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/gist.html#gistgit" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.1.2. The Git Repository Behind Gist</a></li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/gist.html#greasemonkey" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.1.3. Greasemonkey</a></li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/gist.html#gist-cli" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.1.4. Managing Gist from the Command Line</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/other-scm.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.2. Other Version Control Tool Support</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/svn.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.2.1. Using SVN with GitHub</a></li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/hg-git.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.2.2. Using Mercurial with GitHub</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/tools.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.3. Client Tools</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/github-mac.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.3.1. GitHub for Mac</a></li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/hub.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.3.2. hub</a></li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/ios.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.3.3. iOS App</a></li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/others.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.4. Miscellaneous</a><ul>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/jobs.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.4.1. GitHub: Jobs</a></li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/shop.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.4.2. GitHub: Shop</a></li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/short-url.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.4.3. GitHub URL Shortener</a></li>
<li><a href="http://www.worldhello.net/gotgithub/06-side-projects/opensource.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">6.4.4. GitHub Open Source</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="http://www.worldhello.net/gotgithub/appendix/markups.html" style="color:rgb(85, 136, 51);text-decoration:none;font-weight:normal;">7. Appendix: Lightweight Markup Languages</a></li>
</ul>
</div>

