说明
=======
Git 常用、不常用、实用的命令，这些命令都是在日常使用过程中遇到过整理下来的，留作备忘，如果对这些命令还不明白什么意思，请参考学习：[Git 新手入门](readme.md#新手入门) 。

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

# Add/Commit/Rm/Pull/Merge
- 添加文件到暂存区（staged）：`git add filename` / `git stage filename` 
- 将所有修改文件添加到暂存区（staged）： `git add --all` / `git add -A`
- 提交修改到暂存区（staged）：`git commit -m 'commit message'` / `git commit -a -m 'commit message'` 注意理解 -a 参数的意义
- 从Git仓库中删除文件：`git rm filename`
- 从Git仓库中删除文件，但本地文件保留：`git rm --cached filename`
- 重命名某个文件：`git mv filename newfilename` 或者直接修改完毕文件名 ，进行`git add -A && git commit -m 'commit message'` Git会自动识别是重命名了文件
- 获取远程最新代码到本地：`git pull (origin branchname)` 可以指定分支名，也可以忽略。pull 命令自动 fetch 远程代码并且 merge，如果有冲突，会显示在状态栏，需要手动处理。更推荐使用：`git fetch` 之后 `git merge --no-ff origin branchname` 拉取最新的代码到本地仓库，并手动 merge 。

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
	+ 试试这个 ： `git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit`  感觉好用就加成 alias ，方便日后用，方法：`git config --global alias.aliasname 'alias-content'`
	+ 更多用法：[Viewing the History -- 《Pro Git2》](http://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)

# Undo things
- 上次提交msg错误/有未提交的文件应该同上一次一起提交，需要重新提交备注：`git commit --amend -m 'new msg'` 
- 一次`git add -A`后，需要将某个文件撤回到工作区，即：某个文件不应该在本次commit中：`git reset HEAD filename`
- 撤销某些文件的修改内容：`git checkout -- filename` 注意：一旦执行，所有的改动都没有了，谨慎！谨慎！谨慎！
- 将工作区内容回退到远端的某个版本：`git reset --hard <sha1-of-commit>`
	+ `--hard`：reset stage and working directory ,<commitid> 以来所有的变更全部丢弃，并将 HEAD 指向<commitid>
	+ `--soft`：nothing changed to stage and working directory ,仅仅将HEAD指向<commitid> ，所有变更显示在”changed to be committed”中
	+ `--mixed`：default,reset stage ,nothing to working directory ，这也就是第二个例子的原因

# Diff 
- 查看工作区（working directory）和暂存区（staged）之间差异：`git diff`
- 查看工作区（working directory）与当前仓库版本（repository）HEAD版本差异：`git diff HEAD`
- 查看暂存区（staged）与当前仓库版本（repository）差异：`git diff --cached` / `git diff --staged`

# Merge
- 解决冲突后/获取远程最新代码后合并代码：`git merge branchname`
- 保留该存在版本合并log：`git merge --no-ff branchname` 参数`--no-ff`防止 fast-forward 的提交，详情参考：[the difference](http://stackoverflow.com/questions/9069061/what-is-the-difference-between-git-merge-and-git-merge-no-ff)

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

# Tag 

- 查看 tag：`git tag`
- 查找指定 tag，比如查找 V1.0.* ：`git tag -l 'V1.0.*'` 会列出匹配到的，比如 V1.0.1,V1.0.1.1,V1.0.2 等
- 创建轻量级 tag（lightweight tags）：`git tag tag-name` ，例如: `git tag v1.0`
- 创建 tag（annotated tags）：`git tag -a tag-name -v 'msg'` ，例如：`git tag -a v1.0.0 -m '1.0.0版本上线完毕打tag'`
	+ annotated tags VS lightweight tags 可以通过命令真实查看下：`git show v1.0` / `git show v1.0.0`
	+ “A lightweight tag is very much like a branch that doesn’t change – it’s just a pointer to a specific commit.
Annotated tags, however, are stored as full objects in the Git database. They’re checksummed; contain the tagger name, e-mail, and date; have a tagging message; and can be signed and verified with GNU Privacy Guard (GPG). ”
- 查看指定 tag 信息：`git show tag-name`
- 基于历史某次提交（commit）创建 tag ：`git tag -a tagname <sha1-of-commit>`
	+ 例：基于上线时的提交 a207a38d634cc10441636bc4359cd8a18c502dea 创建tag：`git tag -a v1.0.0 a207a38`
- 删除 tag ：`git tag -d tagname`
- 拉取远程 tag 到本地：`git pull remotename --tags` 例如：`git pull origin --tags`
- 推送 tag 到远程服务器：`git push remotename tagname`  例如：`git push origin v1.0.0`
- 将本地所有 tag 推送到远程：`git push remotename --tags` 例如：`git push origin --tags`
- 删除远程 tag ：`git push origin :tagname` 或者 `git push origin --delete tagname`
