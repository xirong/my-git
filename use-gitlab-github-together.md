
说明
====================

由于公司团队使用 GitLab 来托管代码，同时，个人在 Github 上还有一些代码仓库，可公司邮箱与个人邮箱是不同的，由此产生的 SSH key 也是不同的，这就造成了冲突 ，文章提供此类问题的解决方案：**如何在一台机器上面同时使用 Github 与 Gitlab 的服务？**

# 问题产生场景 
-------------

## 无密码与远程服务器交互的秘密 - SSH 
如果采用`ssh 协议`或者`git 协议`通过终端命令对远程仓库进行`push`操作的时候，大概的过程如下：（前提在 Github 上已经配置的本机的 SSH Public Key）

1. 客户端发起一个 Public Key 的认证请求，并发送RSA Key的模数作为标识符。（关于 RSA Key 详细 [维基百科](https://en.wikipedia.org/wiki/RSA_(algorithm))）
2. 服务端检查是否存在请求帐号的公钥（Linux中存储在~/.ssh/authorized_keys文件中），以及其拥有的访问权限。
3. 服务端使用对应的公钥对一个随机的256位的字符串进行加密，并发送给客户端。
4. 客户端使用私钥对字符串进行解密，并将其结合session id生成一个MD5值发送给服务端。 结合session id的目的是为了避免攻击者采用重放攻击（replay attack）。
5. 服务端采用同样的方式生成MD5值与客户端返回的MD5值进行比较，完成对客户端的认证。
6. 将push的内容进行加密与服务端传输数据。

关于 SSH，请查看 [SSH原理简介](http://erik-2-blog.logdown.com/posts/74081-ssh-principle) ，更通俗易懂的文章请查看[阮一峰-SSH原理与运用（一）：远程登录](http://www.ruanyifeng.com/blog/2011/12/ssh_remote_login.html) 。

## 具体场景
无论使用哪种代码托管服务商，对于 Git 而言，`邮箱` 是识别用户的唯一手段，所以对于不同的服务商，由于邮箱不同，那么通过邮件名创建的 SSH Key 自然是不同的，这时候在不同的服务商之间进行 `push` 命令的时候，Git 是不知道使用哪个 SSH Key ，自然导致 `push` 的失败。场景如下：

1. 在公司团队使用搭建的 Gitlab 服务，提交邮箱`xirong.liu@corp.xx.com`， 个人 Github 服务，提交邮箱 `ixirong.liu@gmail.com` （Bitbucket 同理）。
2. 有两个Github账户，不同的账户提交不同的仓库内容。

# 解决方案

## 方案一：同一个邮箱
由于`邮箱`是识别的唯一手段，那么自然的，这两者采用同一个邮箱，生成的 public key 也会是同一个，上传到 Github 或者 Gitlab 上面，在 Git 的配置中 ，设置好 Global 的配置 ：` git config --global user.name 'xirong.liu' && git config --global user.email 'xirong.liu@corp.xx.com'` 进行日常的开发是没有问题的。

实际生活中采用同一个邮箱的可能性并不是太大，这就引出了方案二

## 方案二：基于config文件

所谓的方案二，原理上就是对 SSH 协议配置 config 文件，对不同的域名采用不同的认证密钥。

#### git config 介绍 
 Git有一个工具被称为git config，它允许你获得和设置配置变量；这些变量可以控制Git的外观和操作的各个方面。这些变量可以被存储在三个不同的位置： 
 
1. /etc/gitconfig 文件：包含了适用于系统所有用户和所有库的值。如果你传递参数选项’`--system`’ 给 git config，它将明确的读和写这个文件。 
2. ~/.gitconfig 文件 ：具体到你的用户。你可以通过传递 ‘`--global`’ 选项使Git 读或写这个特定的文件。
3. 位于 Git 目录的 config 文件 (也就是 .git/config) ：无论你当前在用的库是什么，特定指向该单一的库。每个级别重写前一个级别的值。因此，在 .git/config 中的值覆盖了在/etc/gitconfig中的同一个值，可以通过传递‘`--local`’选项使Git 读或写这个特定的文件。

由于采用了不同的邮箱，对不同的服务商进行提交，所以此时我们经常配置的 `git config --global` 就不能常用了，必须在每个仓库的目录下进行配置自己的用户名、邮箱。（嫌麻烦？xirong 是这么解决的，由于个人的 Github 上有较多的仓库，而自己团队的代码基本上都是稳定的，有数的几个，所以在 `git config --global user.email 'ixirong.liu@gmail.com'` 中全局配置的是个人邮箱，在团队的项目中配置）

### 1.  配置 Git 用户名、邮箱 

如刚才所说，xirong 的配置如下：

``` bash
# 全局配置，Github仓库中默认使用此配置
git config --global user.name 'xirong' && git config --global user.email 'ixirong.liu@gmail.com' 

# 团队项目配置，每次新创建一个项目，需要执行下
git config --local user.name 'xirong.liu' && git config --local user.email 'xirong.liu@corp.example.com' 
```

### 2. 生成 ssh key 上传到 Github/Gitlab

ssh key 默认生成后保存在 `~/.ssh/`目录下 ，默认为 `id_rsa 和 id_rsa.pub` 两个文件，由于我们需要分开配置，所以这么做：

``` bash 
# 生成公钥、密钥的同时指定文件名，Gitlab使用
ssh-keygen -t rsa -f ~/.ssh/id_rsa.gitlab -C "xirong.liu@corp.example.com"

# 生成默认，Github使用
ssh-keygen -t rsa -C "ixirong.liu@gmail.com"
```

命令执行完成后，这时`~/.ssh`目录下会多出`id_rsa.gitlab`和`id_rsa.gitlab.pub`两个文件，`id_rsa.gitlab.pub` 里保存的就是我们要使用的key，这个key就是用来上传到 Gitlab上的。

### 3. 配置 config 文件 
在 `~/.ssh`目录下，如果不存在，则新建 `touch ~/.ssh/config`文件 ，文件内容添加如下：

``` bash 
Host corp.example.com
     HostName git.corp.example.com
     IdentityFile ~/.ssh/id_rsa.gitlab
     User xirong.liu
```

- `Host`参数是命令行给出的主机名，比如`ssh -T git@corp.example.com`，那么此时的主机(`Host`)就是`corp.example.com`
- 只有`Host`匹配之后，`SSH`把`git@corp.example.com`转换成`git.corp.example.com`
- `Host`不支持`*`和主机名混用，即`*.example.com`；单独`*`表示匹配所有主机，也就是默认规则
- `HostName`应该是必须填写的内容，根据你使用的命令行内容来填写

配置完成后，符合`git.corp.example.com`的 Git 仓库，均采取` ~/.ssh/id_rsa.gitlab` 密钥进行验证，其它的采取默认的。

### 4. 上传public key 到 Github/Gitlab 

以Github为例，过程如下：

1. 登录github
2. 点击右上方的Accounting settings图标
3. 选择 SSH key
4. 点击 Add SSH key

在出现的界面中填写SSH key的名称，填一个你自己喜欢的名称即可，然后将上面拷贝的`~/.ssh/id_rsa.pub`文件内容粘帖到`key`一栏，在点击“`add key`”按钮就可以了。

添加过程github会提示你输入一次你的github密码 ，确认后即添加完毕。 上传Gitlab的过程一样，请自己操作。

### 5. 验证是否OK 
由于每个托管商的仓库都有唯一的后缀，比如 Github的是 `git@github.com:*`，所以可以这样测试：

``` bash 
➜  ~  ssh -T git@github.com
Hi xirong! You've successfully authenticated, but GitHub does not provide shell access.
➜  ~  ssh -T git@gitlab.dev
Welcome to GitLab, xirong.liu!
```

看到这些 `Welcome` 信息，说明就是 OK的了。

以后，如果还有任何的需求，都可以这么解决，看下 xirong 的几个托管仓库：

``` bash 
➜  ~  ll ~/.ssh
total 40
-rw-r--r-- 1 xirong staff  264 Jul 10 14:42 config
-rw------- 1 xirong staff 3243 Jul 10 14:09 id_rsa
-rw------- 1 xirong staff 1675 Jan 28 20:39 id_rsa.gitlab
-rw-r--r-- 1 xirong staff  407 Jan 28 20:39 id_rsa.gitlab.pub
-rw-r--r-- 1 xirong staff  747 Jul 10 14:09 id_rsa.pub
-rw------- 1 xirong staff 1679 Jun 22 11:42 id_rsa_gitcafe
-rw-r--r-- 1 xirong staff  407 Jun 22 11:42 id_rsa_gitcafe.pub
-rw-r--r-- 1 xirong staff 9139 Jul 29 15:08 known_hosts
```
