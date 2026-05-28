# Remove Secret from History

把 secret 提交进 Git 历史后，第一步永远是废弃并轮换密钥。

清理历史只能减少继续传播，不能让已经泄露的 secret 恢复安全。

## 立即处理

1. 废弃 secret
2. 轮换新 secret
3. 确认访问日志和影响范围
4. 通知相关 owner
5. 清理 Git 历史

## 清理历史

推荐使用 `git filter-repo`：

```bash
git filter-repo --path path/to/secret-file --invert-paths
```

然后强推清理后的历史：

```bash
git push --force --all
git push --force --tags
```

## 注意风险

历史重写会影响所有协作者，执行前必须通知团队，并要求所有人重新同步仓库。

## 清理后

- 检查 GitHub secret scanning 或同类扫描结果
- 清理 forks 和缓存中的泄露内容
- 增加提交前扫描
- 在事故复盘里补充防护动作

## 延伸阅读

- [GitHub Docs: Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [GitHub Docs: About secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/about-secret-scanning)
- [git filter-repo](https://github.com/newren/git-filter-repo)
- [Security and Secret Scanning](../04-github-engineering/security-and-secret-scanning.md)
