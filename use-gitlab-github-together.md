English | [中文](zh/use-gitlab-github-together.md)

Overview
====================

My company team uses GitLab to host code, while I also have personal repositories on GitHub. Since my work email and personal email are different, the SSH keys generated from them are also different — which creates a conflict. This article provides a solution to this problem: **how to use both GitHub and GitLab on the same machine.**

# The Problem
-------------

## The Secret to Password-free Remote Server Interaction — SSH
When you use the `ssh protocol` or `git protocol` to `push` to a remote repository via terminal commands, the process roughly goes like this (assuming you have already configured your local SSH Public Key on GitHub):

1. The client initiates a Public Key authentication request and sends the RSA key modulus as an identifier. (For details on RSA keys, see [Wikipedia](https://en.wikipedia.org/wiki/RSA_(algorithm)))
2. The server checks whether the public key for the requested account exists (stored in `~/.ssh/authorized_keys` on Linux) and verifies its access permissions.
3. The server encrypts a random 256-bit string using the corresponding public key and sends it to the client.
4. The client decrypts the string using its private key, combines it with the session ID to generate an MD5 hash, and sends it back to the server. The session ID is included to prevent replay attacks.
5. The server generates an MD5 hash in the same way and compares it with the one returned by the client, completing client authentication.
6. The pushed content is encrypted and transmitted to the server.

For more on SSH, see [SSH Principle Introduction](http://erik-2-blog.logdown.com/posts/74081-ssh-principle). For a more accessible read, see [Ruan Yifeng - SSH Principles and Usage (Part 1): Remote Login](http://www.ruanyifeng.com/blog/2011/12/ssh_remote_login.html).

## The Specific Scenario
Regardless of which hosting provider you use, Git identifies users solely by `email address`. When you use different providers with different emails, the SSH keys generated from those emails will naturally differ. When you try to `push` between providers, Git doesn't know which SSH key to use, which causes the `push` to fail. Common scenarios include:

1. Using a company-hosted GitLab service with the work email `xirong.liu@corp.xx.com`, and personal GitHub with `ixirong.liu@gmail.com` (the same applies to Bitbucket).
2. Having two GitHub accounts that push to different repositories.

# Solutions

## Option 1: Use the Same Email Address
Since email is the sole means of identification, the simplest approach is to use the same email for both. This produces the same public key, which you upload to both GitHub and GitLab. Then set a global Git config: `git config --global user.name 'xirong.liu' && git config --global user.email 'xirong.liu@corp.xx.com'`. This works fine for day-to-day development.

In practice, using the same email for both isn't always feasible, which leads us to Option 2.

## Option 2: Using a Config File

Option 2 works by configuring an SSH `config` file that tells SSH to use different authentication keys for different hostnames.

#### Introduction to git config
Git includes a tool called `git config` that lets you get and set configuration variables, which control how Git looks and behaves. These variables can be stored in three different locations:

1. `/etc/gitconfig` — Contains values for every user on the system and all their repositories. Pass `--system` to `git config` to explicitly read from and write to this file.
2. `~/.gitconfig` — Specific to your user. Pass `--global` to make Git read from or write to this file.
3. The `config` file inside a Git directory (i.e., `.git/config`) — Specific to that single repository, regardless of which one you're currently using. Each level overrides the one above it, so values in `.git/config` override those in `/etc/gitconfig`. Pass `--local` to make Git read from or write to this file.

Since we're using different emails for different providers, the commonly used `git config --global` is no longer sufficient — you must configure your username and email in each repository's directory. (Don't want the hassle? Here's how xirong handles it: since there are more personal GitHub repos than work repos, the global config is set to the personal email with `git config --global user.email 'ixirong.liu@gmail.com'`, and the work email is configured only in each team project directory.)

### 1. Configure Git Username and Email

As described above, xirong's setup looks like this:

``` bash
# Global config — used by default for GitHub repositories
git config --global user.name 'xirong' && git config --global user.email 'ixirong.liu@gmail.com' 

# Team project config — run this each time a new project is created
git config --local user.name 'xirong.liu' && git config --local user.email 'xirong.liu@corp.example.com' 
```

### 2. Generate SSH Keys and Upload to GitHub/GitLab

By default, SSH keys are saved under `~/.ssh/`, with the default filenames `id_rsa` and `id_rsa.pub`. Since we need separate keys, do the following:

``` bash 
# Generate a key with a custom filename for GitLab
ssh-keygen -t rsa -f ~/.ssh/id_rsa.gitlab -C "xirong.liu@corp.example.com"

# Generate the default key for GitHub
ssh-keygen -t rsa -C "ixirong.liu@gmail.com"
```

After running these commands, two new files — `id_rsa.gitlab` and `id_rsa.gitlab.pub` — will appear in `~/.ssh/`. The contents of `id_rsa.gitlab.pub` are the key you'll upload to GitLab.

### 3. Configure the Config File
In the `~/.ssh` directory, create the config file if it doesn't already exist with `touch ~/.ssh/config`, then add the following:

``` bash 
Host corp.example.com
     HostName git.corp.example.com
     IdentityFile ~/.ssh/id_rsa.gitlab
     User xirong.liu
```

- The `Host` parameter matches the hostname given on the command line. For example, with `ssh -T git@corp.example.com`, the host is `corp.example.com`.
- Only when `Host` matches will SSH translate `git@corp.example.com` into `git.corp.example.com`.
- `Host` does not support mixing wildcards with hostnames (e.g., `*.example.com`); a standalone `*` matches all hosts and acts as a catch-all default rule.
- `HostName` is required — fill it in based on the actual hostname used in your commands.

Once configured, any Git repository matching `git.corp.example.com` will use the `~/.ssh/id_rsa.gitlab` key for authentication; all others will use the default.

### 4. Upload the Public Key to GitHub/GitLab

Using GitHub as an example:

1. Log in to GitHub.
2. Click the account settings icon in the top right corner.
3. Select **SSH keys**.
4. Click **Add SSH key**.

In the form that appears, give the key a name of your choice, then paste the contents of `~/.ssh/id_rsa.pub` into the **key** field, and click **Add key**.

GitHub will prompt you to enter your password once to confirm. The process for GitLab is the same — go ahead and do it yourself.

### 5. Verify Everything Works
Each hosting provider has a unique SSH endpoint. For GitHub it's `git@github.com:*`. You can test your setup like this:

``` bash 
➜  ~  ssh -T git@github.com
Hi xirong! You've successfully authenticated, but GitHub does not provide shell access.
➜  ~  ssh -T git@gitlab.dev
Welcome to GitLab, xirong.liu!
```

If you see these `Welcome` messages, you're good to go.

This same approach works for any additional hosting providers you need to add. Here's a look at xirong's `~/.ssh` directory with multiple providers configured:

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
