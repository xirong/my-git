# 旧内容迁移清单

这个清单用于跟踪旧文章如何进入新的学习路径。

原则：

1. 有长期价值的内容迁入新目录
2. 仍有参考价值但时效性较弱的内容放入资源索引
3. 不再推荐的做法放入归档说明
4. 根目录保留入口时，要指向更完整的新文章
5. 迁移时优先补充场景、风险、推荐做法和延伸阅读

## 根目录文章

| 旧文件 | 新位置 | 状态 | 处理建议 |
| --- | --- | --- | --- |
| `why-git.md` | `01-getting-started/why-git.md` | 已迁入 | README 优先指向新目录 |
| `useful-git-command.md` | `02-daily-workflow/everyday-git-commands.md` | 已迁入 | 后续补常见场景和风险提示 |
| `git-workflow-tutorial.md` | `03-team-collaboration/` | 部分迁入 | 拆到 GitHub Flow、Gitflow、Trunk-Based Development、团队工作流指南 |
| `how-to-use-github.md` | `04-github-engineering/` | 部分迁入 | 拆到 GitHub 工程治理、分支保护、Rulesets、Actions、Release |
| `use-gitlab-github-together.md` | `03-team-collaboration/gitlab-flow.md`、`09-resources/` | 待评估 | 保留 GitLab / GitHub 混用经验，补时效性说明 |
| `using-svn.md` | `01-getting-started/git-vs-svn.md`、`09-resources/deprecated-resources.md` | 待评估 | 作为历史迁移参考，不作为主学习路径 |
| `ixirong.com.md` | `09-resources/resources-index.md` | 待评估 | 只保留和项目有关的资料入口 |

## 中文目录

| 旧文件 | 状态 | 处理建议 |
| --- | --- | --- |
| `zh/readme.md` | 待评估 | 保留历史入口，后续和 README 的内容关系要重新定义 |
| `zh/why-git.md` | 待评估 | 和 `01-getting-started/why-git.md` 对齐 |
| `zh/useful-git-command.md` | 待评估 | 和 `02-daily-workflow/everyday-git-commands.md` 对齐 |
| `zh/git-workflow-tutorial.md` | 待评估 | 拆到团队协作目录 |
| `zh/how-to-use-github.md` | 待评估 | 拆到 GitHub 工程治理目录 |

## 资源类内容

| 内容 | 新位置 | 状态 | 处理建议 |
| --- | --- | --- | --- |
| 书籍资料 | `09-resources/books.md` | 已建入口 | 定期检查链接有效性 |
| 工具资料 | `09-resources/tools.md` | 已建入口 | 标注推荐场景和维护状态 |
| 可视化学习资料 | `09-resources/visual-learning.md` | 已建入口 | 保留适合新手理解的资料 |
| 大厂实践案例 | `10-company-practices/` | 已独立成一级目录 | 每个案例都要回链到对应主题文章 |
| 过时资料 | `09-resources/deprecated-resources.md` | 已建入口 | 标注为什么不作为主路径推荐 |

## 下一步

1. 给根目录旧文章增加指向新文章的提示
2. 把 `git-workflow-tutorial.md` 中仍有价值的内容拆到 `03-team-collaboration/`
3. 把 `how-to-use-github.md` 中仍有价值的内容拆到 `04-github-engineering/`
4. 检查 `zh/` 下旧文章是否需要保留、合并或归档
5. 清理 README 中仍指向旧入口的链接
