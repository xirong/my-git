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