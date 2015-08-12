说明
=======
Git 命令中有些是不常用、但很实用的，这些命令都是在日常使用过程中遇到过整理下来的，留作备忘。

# Repository

- 检出（clone）仓库代码：`git clone repository-url` / `git clone repository-url local-directoryname`
	+ 例如，clone jquery 仓库到本地： `git clone git://github.com/jquery/jquery.git`
	+ clone jquery 仓库到本地，并且重命名为 my-jquery ：`git clone git://github.com/jquery/jquery.git my-jquery`
- 查看远程仓库：`git remote -v`
- 添加远程仓库：`git remote add [name] [repository-url]`
- 删除远程仓库：`git remote rm [name]`
- 修改远程仓库地址：`git remote set-url origin new-repository-url`
- 拉取远程仓库： `git pull [remoteName] [localBranchName]`
- 推送远程仓库： `git push [remoteName] [localBranchName]`

# Add/Commit/Rm

- 添加文件到暂存区（staged）：`git add filename` / `git stage filename` 
- 将所有修改文件添加到暂存区（staged）： `git add --all` / `git add -A`
- 提交修改到暂存区（staged）：`git commit -m 'commit message'` / `git commit -a -m 'commit message'` 注意理解 -a 参数的意义
- 从Git仓库中删除文件：`git rm filename`
- 从Git仓库中删除文件，但本地文件保留：`git rm --cached filename`
- 重命名某个文件：`git mv filename newfilename` 或者直接修改完毕文件名 ，进行`git add -A && git commit -m 'commit message'` Git会自动识别是重命名了文件

# Log

- 查看日志：`git log`
- 查看日志，并查看每次的修改内容：`git log -p`
- 查看日志，并查看每次文件的简单修改状态：`git log --stat`
- 一行显示日志：`git log --pretty=oneline` / `git log --pretty='format:"%h - %an, %ar : %s'`
- 查看日志范围：
	+ 查看最近10条日志：`git log -10`
	+ 查看2周前：`git log --until=2week` 或者指定2周的明确日期，比如：`git log --until=2015-08-12`
	+ 查看最近2周内：`git log --since=2week` 或者指定2周明确日志，比如：`git log --since=2015-08-12`
	+ 只查看某个用户的提交：`git log --committer=user.name` / `git log --author=user.name`
	+ 只查看提交msg中包含某个信息的历史，比如包含'测试'两个字的：`git log --grep '测试'`
	+ 更多用法：[Viewing the History -- 《Pro Git2》](http://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)


# Undo things
- 上次提交msg错误/有未提交的文件应该同上一次一起提交，需要重新提交备注：`git commit --amend -m 'new msg'` 
- 一次`git add -A`后，需要将某个文件撤回到工作区，即：某个文件不应该在本次commit中：`git reset HEAD filename`
- 撤销某些文件的修改内容：`git checkout -- filename` 注意：一旦执行，所有的改动都没有了，谨慎！谨慎！谨慎！

# Branch

- 查看分支：`git branch`
- 创建分支：`git branch branchname` 
	+ 例： 基于 master 分支新建 dev 分支 ： `git branch dev`
- 基于之前的某个 Commit 新开分支： `git branch branchname <sha1-of-commit>` 
	+ 例： 基于上线的的提交 a207a38d634cc10441636bc4359cd8a18c502dea 创建 hotfix 分支 ： `git branch hotfix a207a38`
- 切换分支： `git checkout branchname`
	+ 例： 由分支 master 切换到 dev 分支：`git checkout dev`
- 创建新分支并切换到下面：`git checkout -b branchname`  或者 `git branch branchname && git checkout branchname`
	+ 例：基于 master 分支新建 dev 分支，并切换到 dev 分支上： `git checkout -b dev` 或 `git branch dev && git checkout dev ` 
- 查看分支代码不同：`git diff branchname`
- 合并分支：`git merge branchname`
- 删除分支：`git branch -d branchname` 强制删除未合并过的分支：`git branch -D branchname`
- 查看远程分支：`git branch -r` / `git branch -r -v`
- 获取远程分支到本地：`git checkout -b local-branchname origin/remote-branchname`
- 推送本地分支到远程：`git push origin remote-branchname` / `git push origin local-branchname:remote-branchname`
	+ 将本地 dev 代码推送到远程 dev 分支： `git push (-u) origin dev` / `git push origin dev:dev`
	+ （技巧）将本地 dev 分支代码推送到远程 master 分支： `git push origin dev:master`
- 删除远程分支：`git push origin :remote-branchname` / `git push origin --delete remote-branchname`

# Diff 

- 查看工作区（working directory）和暂存区（staged）之间差异：`git diff`
- 查看工作区（working directory）与当前仓库版本（repository）HEAD版本差异：`git diff HEAD`
- 查看暂存区（staged）与当前仓库版本（repository）差异：`git diff --cached` / `git diff --staged`