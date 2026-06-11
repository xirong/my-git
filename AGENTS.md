# AGENTS.md

本仓库是面向现代工程团队与 AI 编程时代的双语 Git / GitHub 手册。欢迎用 AI 工具协助维护，约定如下。

## 仓库结构

- `01-getting-started/` 到 `10-company-practices/` 是正文目录，每个目录的中文文章在目录根，English 文章在 `<目录名>_en/` 子目录，文件名以 `_en.md` 结尾
- `00-meta/` 放维护类文档：路线图、风格规范、release notes
- `09-resources/legacy/` 是历史归档，保持原样
- `scripts/` 放文档检查脚本

## 改动后必须验证

```bash
python3 scripts/check-docs.py
python3 scripts/check-links.py --no-external
git diff --check
```

`check-docs.py` 会检查本地链接和禁用词，动笔前先看脚本里的 `FORBIDDEN_LITERAL` 列表，避免返工。

## 内容规则

- 新文章遵循 [内容风格规范](00-meta/content-style-guide.md)
- 先讲场景和判断，再给命令，危险操作必须写清风险
- 涉及 GitHub 功能的描述要引用官方文档链接
- 中英文内容成对维护：改中文文章时同步更新对应的 `_en.md` 文件，新文章要同时创建两份并互相链接
- 新文章要加进所在目录的 README 和相关导航入口

## 禁止操作

- 不修改 `09-resources/legacy/` 下的历史归档
- 不新增 pdf、docx 等二进制文档
- 不修改 `LICENSE`
- 不执行 `git commit`、`git push`、打 tag，这些由维护者确认后执行
- 不删除已有文章，废弃内容先和维护者确认

## 提交与 PR 约定

- commit message 用 `docs: ...`、`ci: ...` 风格，一个 commit 一个意图
- AI 工具参与的提交加 `Co-authored-by` trailer
- PR 描述写明使用的 AI 工具、人工检查过的文件、跑过的检查命令
