# Remote Ref Lab / 远端引用实验

[中文文章](../../../01-getting-started/git-mental-model-08-remote.md) | [English article](../../../01-getting-started/01-getting-started_en/git-mental-model-08-remote_en.md)

## 中文

实验在一个新建临时根目录中创建一个 bare `origin.git` 和两个 clone：`reader`、`writer`。所有 `push` 都指向这个临时 bare 仓库，不读取当前项目的 remote，也不读取全局 Git 配置、签名设置或本机 hooks。

```bash
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
sed -n '1,240p' "$lab_path/observations.txt"
sed -n '1,240p' "$lab_path/push-results.txt"
bash cleanup.sh "$lab_path"
```

`fetch` 后，`reader` 的 `origin/main` 从 A 变为 B，`main`、Index 和 Working Tree 保持 A。随后实验显式执行 `merge --ff-only origin/main`，再断言这三处变为 B。两个 clone 后续各自产生提交，`reader` 向已前进的 bare `origin` push 会被 Git 拒绝。实验还安装了一个只拒绝 `protected` 分支的 bare-repo hook，用于演示服务器端策略可以拒绝客户端请求；它不模拟托管平台的真实身份认证。

`cleanup.sh` 只接受带本实验标记、且结构完整的临时根目录。希望保留现场时跳过 cleanup，完成观察后再执行它。

一次运行完整自测：

```bash
bash test.sh
```

## English

The lab creates a new temporary root containing a bare `origin.git` and two clones, `reader` and `writer`. Every `push` targets that temporary bare repository. It does not read this project's remote, global Git configuration, signing settings, or local hooks.

```bash
lab_path=$(bash setup.sh)
bash verify.sh "$lab_path"
sed -n '1,240p' "$lab_path/observations.txt"
sed -n '1,240p' "$lab_path/push-results.txt"
bash cleanup.sh "$lab_path"
```

After `fetch`, `reader` moves `origin/main` from A to B while its `main`, index, and working tree remain at A. The lab then explicitly runs `merge --ff-only origin/main` and asserts that all three move to B. The two clones subsequently create separate commits, and Git rejects `reader`'s push to the bare origin after it has advanced. The lab also installs a bare-repository hook that rejects only the `protected` branch. It demonstrates that server-side policy can reject a client request; it does not emulate hosted-service authentication.

`cleanup.sh` accepts only a marked, structurally complete lab root. Skip cleanup while inspecting the evidence, then run it when finished.

Run the complete self-test:

```bash
bash test.sh
```
