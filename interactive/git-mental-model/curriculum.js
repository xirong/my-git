/* Deterministic teaching diagrams. Labels such as C1 are illustrative, not object IDs. */
(() => {
  'use strict';

  const query = new URLSearchParams(location.search);
  let language = query.get('lang') === 'en' ? 'en' : 'zh';
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const narrowScreen = matchMedia('(max-width: 700px)');
  const pick = value => Array.isArray(value) ? value[language === 'en' ? 1 : 0] : value;
  const escape = value => String(value).replace(/[&<>"']/g, character => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[character]);
  const node = (id, label, type, x, y, note = '', state = '') => ({ id, label, type, x, y, note, state });
  const edge = (from, to, label = '', active = false) => ({ from, to, label, active });

  const lessons = {
    refs: {
      label: ['图 04 / 引用更新模型', 'FIG 04 / REF UPDATE MODEL'],
      choices: [
        { value: 'attached', label: ['附着在 main 后提交', 'Commit while attached to main'] },
        { value: 'detached', label: ['从附注标签 detached 后提交', 'Commit after detaching from annotated tag'] }
      ],
      states(choice) {
        const attached = choice === 'attached';
        const common = [
          { caption: ['初态：HEAD 是符号引用，main 指向 C3。轻量标签直指 C1，附注标签先指向 T1。', 'Start: HEAD is symbolic and main points to C3. The lightweight tag points to C1; the annotated tag points through T1.'], command: 'git symbolic-ref --short HEAD\ngit cat-file -t v1-light\ngit cat-file -t v1-annotated', output: 'main\ncommit\ntag' },
          { caption: attached ? ['保持 attached：下一次 commit 会通过 HEAD 更新 main。', 'Stay attached: the next commit will update main through HEAD.'] : ['切到 v1-annotated 会先解开 T1，并让 HEAD 直接指向 C1。', 'Switching to v1-annotated peels T1 and makes HEAD point directly to C1.'], command: attached ? 'git symbolic-ref --short HEAD' : 'git switch --detach v1-annotated\ngit symbolic-ref -q HEAD || printf "HEAD is detached\\n"', output: attached ? 'main' : 'HEAD is detached' },
          { caption: attached ? ['创建 C4 后，main 前移到 C4。agent/draft 和两个 tag 都保持原值。', 'After C4 is created, main advances to C4. agent/draft and both tags keep their values.'] : ['创建 C4 后，只有直接 HEAD 前移。main 仍在 C3，agent/draft 仍在 C2。', 'After C4 is created, only direct HEAD advances. main stays at C3 and agent/draft stays at C2.'], command: 'git add detached.txt\ngit commit -m "detached experiment"', output: attached ? 'HEAD -> main -> C4' : 'HEAD -> C4\nmain -> C3\nagent/draft -> C2' },
          { caption: attached ? ['attached commit 已由 main 命名，不需要额外引用来保留它。', 'The attached commit is already named by main; no extra ref is needed to retain it.'] : ['创建 keep-detached，让 C4 在离开 detached HEAD 后仍有明确名字。', 'Create keep-detached so C4 keeps an explicit name after leaving detached HEAD.'], command: attached ? 'git show-ref --heads' : 'git branch keep-detached HEAD', output: attached ? 'refs/heads/main -> C4\nrefs/heads/agent/draft -> C2' : 'refs/heads/keep-detached -> C4' },
          { caption: attached ? ['结论：附着状态的提交前移当前 branch。标签没有被移动。', 'Result: an attached commit advances the current branch. Tags do not move.'] : ['切回 main 后，HEAD 再次成为符号引用；keep-detached 继续保护 C4。', 'After switching to main, HEAD is symbolic again; keep-detached continues to retain C4.'], command: attached ? 'git rev-parse HEAD main agent/draft' : 'git switch main\ngit symbolic-ref --short HEAD', output: attached ? 'HEAD = main = C4\nagent/draft = C2' : 'main' }
        ];
        return common.map((item, step) => {
          const detached = !attached && step >= 1;
          const committed = step >= 2;
          const kept = !attached && step >= 3;
          const back = !attached && step >= 4;
          const headTarget = back ? 'main' : detached ? (committed ? 'C4' : 'C1') : 'main';
          const mainTarget = attached && committed ? 'C4' : 'C3';
          const nodes = [
            node('head', back || !detached ? 'HEAD (symbolic)' : 'HEAD (direct)', 'ref', 42, 24, back || !detached ? `→ ${headTarget}` : `→ ${headTarget}`, 'emphasis'),
            node('main', 'main', 'ref', 236, 24, `→ ${mainTarget}`, attached && committed ? 'emphasis' : ''),
            node('draft', 'agent/draft', 'ref', 430, 24, '→ C2'),
            node('light', 'v1-light', 'ref', 42, 276, '→ C1'),
            node('tag', 'v1-annotated', 'ref', 236, 276, '→ T1'),
            node('t1', 'T1 tag object', 'plain', 430, 276, '→ C1'),
            node('c1', 'C1', 'commit', 42, 150, 'baseline'),
            node('c2', 'C2', 'commit', 236, 150, 'agent draft'),
            node('c3', 'C3', 'commit', 430, 150, 'main release'),
            node('c4', 'C4', 'commit', 624, 150, attached ? 'attached commit' : 'detached commit', committed ? 'emphasis' : 'gone')
          ];
          if (kept) nodes.push(node('keep', 'keep-detached', 'ref', 624, 276, '→ C4', 'emphasis'));
          const edges = [edge('c2', 'c1'), edge('c3', 'c1'), edge('t1', 'c1')];
          if (committed) edges.push(edge('c4', attached ? 'c3' : 'c1', '', true));
          return { ...item, nodes, edges, facts: [
            ['HEAD', back || !detached ? `symbolic → ${headTarget}` : `direct → ${headTarget}`],
            ['main', mainTarget],
            ['protected C4', attached && committed ? 'main' : kept ? 'keep-detached' : committed ? 'HEAD only' : 'not created']
          ] };
        });
      }
    },
    recovery: {
      label: ['图 05 / 可达性与保留边界', 'FIG 05 / REACHABILITY AND RETENTION'],
      choices: [
        { value: 'recover', label: ['为 C2 建立 recovered 引用', 'Create recovered ref for C2'] },
        { value: 'expire', label: ['让 C3 只剩 reflog 线索', 'Leave C3 with reflog only'] }
      ],
      states(choice) {
        const rescue = choice === 'recover';
        const copy = [
          { caption: ['初态：main 已 reset 到 C1。C2 与 C3 没有 branch 指向，但 HEAD reflog 仍记录它们。', 'Start: main was reset to C1. No branch points to C2 or C3, but the HEAD reflog still records both.'], command: 'git reflog show --oneline HEAD\ngit fsck --no-reflogs --unreachable', output: 'HEAD@{...}: reset: moving to main\n<unreachable C2>\n<unreachable C3>' },
          { caption: rescue ? ['从 reflog 选择 C2。对象仍存在，所以可以先检查内容再恢复。', 'Select C2 from the reflog. The object still exists, so inspect it before recovery.'] : ['选择没有新引用保护的 C3。此刻它仍可通过对象 ID 读取。', 'Select C3, which has no new ref protection. Its object ID is still readable now.'], command: rescue ? 'git show <C2-id>' : 'git cat-file -e <C3-id>^{commit}', output: rescue ? 'recoverable commit\nrecoverable.txt' : 'exit 0' },
          { caption: rescue ? ['创建 recovered -> C2 后，C2 从 branch 起点重新可达。', 'After recovered -> C2 is created, C2 is reachable again from a branch.'] : ['不为 C3 建立 branch。它的保留仍依赖 reflog 与过期策略。', 'No branch is created for C3. Its retention still depends on reflog and expiration policy.'], command: rescue ? 'git branch recovered <C2-id>' : 'git show-ref --verify refs/heads/recovered', output: rescue ? 'refs/heads/recovered -> C2' : 'recovered protects C2 only' },
          { caption: ['实验显式过期所有 reflog，再对这个可删除临时库运行 gc --prune=now。', 'The lab explicitly expires all reflogs, then runs gc --prune=now in this disposable repository.'], command: 'git reflog expire --expire=now --expire-unreachable=now --all\ngit gc --prune=now', output: 'temporary lab cleanup completed' },
          { caption: rescue ? ['C2 仍可读，因为 recovered 使它可达。C3 已无法解析。', 'C2 remains readable because recovered makes it reachable. C3 no longer resolves.'] : ['C3 没有 ref 或 reflog 保护，清理后无法解析；未 add 或 commit 的编辑不在这个恢复承诺内。', 'C3 had no ref or reflog protection and no longer resolves after cleanup. Unstaged, uncommitted edits are outside this recovery promise.'], command: rescue ? 'git cat-file -e recovered^{commit}\ngit cat-file -e <C3-id>^{commit}' : 'git cat-file -e <C3-id>^{commit}', output: rescue ? 'C2: readable\nC3: missing' : 'fatal: Not a valid object name <C3-id>' }
        ];
        return copy.map((item, step) => {
          const expired = step >= 4;
          const protectedC2 = step >= 2;
          const nodes = [
            node('main', 'main', 'ref', 42, 25, '→ C1', step === 0 ? 'emphasis' : ''),
            node('reflog', 'HEAD reflog', 'plain', 236, 25, step >= 3 ? 'expired' : 'C3, C2, C1', step >= 3 ? 'gone' : ''),
            node('recovered', 'recovered', 'ref', 430, 25, protectedC2 ? '→ C2' : 'not created', protectedC2 ? 'emphasis' : 'gone'),
            node('c1', 'C1', 'commit', 42, 180, 'baseline'),
            node('c2', 'C2', 'commit', 236, 180, 'recoverable', expired ? '' : rescue && step >= 1 ? 'emphasis' : ''),
            node('c3', 'C3', 'commit', 430, 180, expired ? 'missing' : 'reflog only', expired ? 'gone' : !rescue && step >= 1 ? 'emphasis' : ''),
            node('edit', 'uncommitted edit', 'content', 624, 180, 'not an object', 'gone')
          ];
          return { ...item, nodes, edges: [edge('c2', 'c1'), edge('c3', 'c1'), ...(protectedC2 ? [edge('recovered', 'c2', '', true)] : [])], facts: [
            ['C2', protectedC2 ? 'reachable via recovered' : 'reflog only'],
            ['C3', expired ? 'missing' : 'reflog only'],
            ['uncommitted edit', 'not promised']
          ] };
        });
      }
    },
    merge: {
      label: ['图 06 / 共同祖先与结果形状', 'FIG 06 / ANCESTOR AND RESULT SHAPE'],
      choices: [
        { value: 'ff', label: ['目标可 fast-forward', 'Target can fast-forward'] },
        { value: 'diverged', label: ['两侧已分叉', 'Histories have diverged'] },
        { value: 'semantic', label: ['文本合并干净，行为失败', 'Text merge is clean, behavior fails'] }
      ],
      states(choice) {
        const diverged = choice !== 'ff';
        const semantic = choice === 'semantic';
        const captions = diverged ? [
          ['先找共同祖先 C1。main 与 topic 各自从 C1 产生新提交。', 'Find common ancestor C1 first. main and topic each added a commit from C1.'],
          ['比较 C1 到两侧 tip 的变化。分叉意味着不能只移动 main 来包含两边历史。', 'Compare each tip with C1. Divergence means main cannot include both histories by moving alone.'],
          ['Git 组合两侧变化。是否出现文本冲突取决于具体内容，不取决于分支名字。', 'Git combines both sides. Text conflicts depend on content, not branch names.'],
          semantic ? ['文本合并成功并创建 M，但真实 behavior_check.py 返回退出码 1。', 'Text merge succeeds and creates M, but the real behavior_check.py exits with status 1.'] : ['创建 merge commit M。M 同时记录 main tip 与 topic tip 两个 parent。', 'Create merge commit M. M records both the main and topic tips as parents.'],
          semantic ? ['干净合并只说明 Git 能组合文本。行为正确仍需要运行对应检查。', 'A clean merge only means Git combined the text. Behavior still needs its own checks.'] : ['结果保留两条历史的汇合点。两个 parent 是 merge commit 的结构特征。', 'The result records where the histories join. Two parents are the structural feature of a merge commit.']
        ] : [
          ['main 在 C1，topic 已沿同一路径到 C2。C1 是 main 的祖先。', 'main is at C1 and topic is ahead at C2 on the same path. C1 is an ancestor of topic.'],
          ['merge-base 是 C1。topic 已包含 main 的全部历史。', 'The merge base is C1. topic already contains all of main.'],
          ['不需要组合两组分叉变化，也没有新的内容结果要记录。', 'There are no divergent change sets to combine and no new content result to record.'],
          ['fast-forward 只把 main 从 C1 移到已有 C2。Git 不创建 merge commit。', 'Fast-forward only moves main from C1 to existing C2. Git creates no merge commit.'],
          ['C2 保持原来的单 parent 结构。历史没有新增一个汇合节点。', 'C2 keeps its original single-parent structure. No new join node is added.']
        ];
        return captions.map((caption, step) => {
          const merged = step >= 3;
          const nodes = [node('c1', 'C1', 'commit', 236, 215, 'common ancestor'), node('main', diverged ? 'C2 main' : 'main', diverged ? 'commit' : 'ref', 42, 95, diverged ? 'main change' : `→ ${merged ? 'C2' : 'C1'}`, !diverged && merged ? 'emphasis' : ''), node('topic', diverged ? 'C3 topic' : 'C2 topic', 'commit', 430, 95, 'topic change')];
          if (merged && diverged) nodes.push(node('result', semantic ? 'M semantic-result' : 'M merge-result', 'commit', 236, 24, semantic ? '2 parents; check fails' : '2 parents', 'emphasis'));
          if (merged && !diverged) nodes[0] = node('c1', 'C1', 'commit', 236, 215, 'parent of C2');
          return { caption, command: step === 0 ? 'git merge-base HEAD <topic>' : step === 3 ? (diverged ? 'git merge <topic>' : 'git merge --ff-only <topic>') : step === 4 && semantic ? 'python3 behavior_check.py' : 'git log --graph --oneline --all', output: step === 3 ? (diverged ? 'merge commit M created' : 'Fast-forward\nmain -> C2') : step === 4 ? (semantic ? 'exit 1' : diverged ? 'M has parent C2 and parent C3' : 'C2 has one parent') : 'state shown above', nodes, edges: [edge('main', !diverged && merged ? 'topic' : 'c1', '', !diverged && merged), edge('topic', 'c1'), ...(merged && diverged ? [edge('result', 'main', '', true), edge('result', 'topic', '', true)] : [])], facts: [
            ['result', merged ? diverged ? 'new merge commit M' : 'ref moved to C2' : 'pending'],
            ['parents', merged ? diverged ? '2' : 'C2 remains 1' : 'not decided'],
            ['behavior', semantic && step >= 4 ? 'check exits 1' : semantic ? 'not checked' : 'separate concern']
          ] };
        });
      }
    },
    rebase: {
      label: ['图 07 / 提交重放模型', 'FIG 07 / COMMIT REPLAY MODEL'],
      choices: [
        { value: 'replay', label: ['上游变化，需要重放', 'Upstream changed; replay needed'] },
        { value: 'noop', label: ['没有待重放 commit', 'No commit needs replay'] },
        { value: 'abort', label: ['冲突后执行 abort', 'Abort after a conflict'] }
      ],
      states(choice) {
        const replay = choice === 'replay', noop = choice === 'noop';
        const captions = replay ? [
          ['旧 topic commit O 的 parent 是 base B。upstream 已前进到 U。', 'Old topic commit O has parent B. upstream has advanced to U.'],
          ['rebase 选出 topic 相对 B 的提交，准备把其变化应用到 U。', 'Rebase selects topic commits relative to B and prepares to apply their changes onto U.'],
          ['应用相同变化会创建新 commit N。内容可相同，parent 已改变。', 'Applying the same change creates new commit N. Content may match, but the parent changed.'],
          ['topic 前移到 N。replay-topic-original 显式保留旧 O，因此 O 仍可读。', 'topic advances to N. replay-topic-original explicitly retains O, so O remains readable.'],
          ['O 与 N 的 ID 不同：O 的 parent 是 B，N 的 parent 是 U。', 'O and N have different IDs: O has parent B; N has parent U.']
        ] : noop ? [
          ['no-replay 已与 upstream 指向同一 commit U。', 'no-replay and upstream already point to the same commit U.'],
          ['Git 计算后没有发现需要重放的 topic commit。', 'Git finds no topic commit that needs replaying.'],
          ['没有变化需要应用，因此不会创建新 commit。', 'There is no change to apply, so no new commit is created.'],
          ['no-replay 的引用保持在 U。', 'The no-replay ref remains at U.'],
          ['结论：rebase 命令成功不等于所有 commit ID 都改变。', 'Result: a successful rebase command does not mean every commit ID changes.']
        ] : [
          ['干净开始：topic 指向 O，Working Tree 与 Index 对齐。', 'Clean start: topic points to O, with working tree and index aligned.'],
          ['rebase upstream 在第二个 topic commit 发生冲突。', 'rebase upstream conflicts on the second topic commit.'],
          ['冲突中的 stage 2 是 upstream 上的重放结果，stage 3 是正在应用的 topic commit。', 'In this rebase conflict, stage 2 is the replay result on upstream; stage 3 is the topic commit being applied.'],
          ['在这个干净实验中执行 git rebase --abort。', 'Run git rebase --abort in this clean lab.'],
          ['topic、Index 与 Working Tree 恢复到开始前；REBASE_HEAD 消失。', 'topic, index, and working tree return to the starting state; REBASE_HEAD disappears.']
        ];
        return captions.map((caption, step) => {
          const completed = step >= 3;
          const nodes = noop ? [node('u', 'U', 'commit', 236, 155, 'upstream = no-replay', completed ? 'emphasis' : '')] : [
            node('b', 'B', 'commit', 236, 245, 'base'),
            node('u', 'U', 'commit', 42, 125, 'upstream'),
            node('o', 'O old topic', 'commit', 430, 125, 'parent B', replay && completed ? '' : 'emphasis'),
            ...(replay && step >= 2 ? [node('n', 'N replayed', 'commit', 236, 24, 'parent U', 'emphasis')] : []),
            ...(!replay && !noop && step >= 1 && step < 3 ? [node('conflict', 'REBASE_HEAD', 'ref', 624, 125, 'current topic commit', 'emphasis')] : [])
          ];
          const edges = noop ? [] : [edge('u', 'b'), edge('o', 'b'), ...(replay && step >= 2 ? [edge('n', 'u', '', true)] : [])];
          const command = replay ? ['git rev-parse replay-topic-original replay-topic','git merge-base replay-topic replay-upstream','git rebase replay-upstream','git branch --contains <O-id>','git rev-parse <O-id>^ <N-id>^'][step] : noop ? ['git rev-parse no-replay replay-upstream','git log replay-upstream..no-replay','git rebase replay-upstream','git rev-parse no-replay-before no-replay','git cat-file -p no-replay'][step] : ['git status --short','git rebase upstream','git ls-files --unmerged -- app.txt','git rebase --abort','git status --short\ngit rev-parse -q --verify REBASE_HEAD'][step];
          const output = replay && step === 4 ? 'O parent = B\nN parent = U\nO != N' : noop && step === 4 ? 'no-replay ID unchanged' : !replay && !noop && step === 2 ? 'stage 1 owner=base\nstage 2 owner=upstream\nstage 3 owner=topic' : !replay && !noop && step >= 3 ? 'topic -> O\nIndex / Working Tree: clean\nREBASE_HEAD: missing' : 'state shown above';
          return { caption, command, output, nodes, edges, facts: [
            ['topic ref', noop ? 'U unchanged' : replay && completed ? 'N' : 'O'],
            ['commit identity', replay && step >= 2 ? 'O != N' : noop ? 'unchanged' : step >= 3 ? 'restored O' : 'abort pending'],
            ['Index / WT', !replay && !noop && step >= 3 ? 'restored in clean lab' : !replay && !noop && step >= 1 ? 'conflicted' : 'aligned']
          ] };
        });
      }
    },
    remote: {
      label: ['图 08 / Fetch 与整合边界', 'FIG 08 / FETCH AND INTEGRATION BOUNDARY'],
      choices: [
        { value: 'fetch', label: ['只执行 git fetch origin', 'Run git fetch origin only'] },
        { value: 'integrate', label: ['fetch 后显式 fast-forward', 'Explicitly fast-forward after fetch'] }
      ],
      states(choice) {
        const integrate = choice === 'integrate';
        const captions = [
          ['reader 初态：main 与本地 origin/main 记录都在 A，story.txt 内容是 version=1。', 'Reader starts with main and local origin/main at A; story.txt contains version=1.'],
          ['writer 把 B 推到临时 bare origin。reader 的本地记录尚未改变。', 'Writer pushes B to the temporary bare origin. Reader local refs have not changed yet.'],
          ['reader fetch：下载 B，并把本地 origin/main 从 A 更新到 B。', 'Reader fetches: B is downloaded and local origin/main moves from A to B.'],
          integrate ? ['显式 merge --ff-only origin/main，把 main 从 A 前移到 B。', 'Explicit merge --ff-only origin/main advances main from A to B.'] : ['停止在 fetch-only 状态。main 仍在 A，Index 与 Working Tree 中的 story.txt 仍是 version=1。', 'Stop at fetch-only state. main remains at A; story.txt in the index and working tree remains version=1.'],
          integrate ? ['整合后 HEAD、main 与 origin/main 都在 B；Index 与 Working Tree 中的 story.txt 是 version=2。', 'After integration, HEAD, main, and origin/main are at B; story.txt in the index and working tree is version=2.'] : ['看到 origin/main=B 只证明本地远端跟踪引用已更新，不代表本地 story.txt 已同步。', 'Seeing origin/main=B proves the local remote-tracking ref updated, not that local story.txt is synchronized.']
        ];
        return captions.map((caption, step) => {
          const fetched = step >= 2, merged = integrate && step >= 3;
          const local = merged ? 'B' : 'A', remoteRef = fetched ? 'B' : 'A', bare = step >= 1 ? 'B' : 'A';
          const nodes = [node('head', 'HEAD -> main', 'ref', 42, 35, `→ ${local}`, merged ? 'emphasis' : ''), node('track', 'origin/main', 'ref', 236, 35, `→ ${remoteRef}`, fetched && !merged ? 'emphasis' : ''), node('origin', 'bare origin/main', 'ref', 430, 35, `→ ${bare}`, step === 1 ? 'emphasis' : ''), node('a', 'A', 'commit', 236, 205, 'story.txt: version=1'), node('b', 'B', 'commit', 430, 205, 'story.txt: version=2', step >= 1 ? '' : 'gone'), node('files', 'story.txt', 'content', 624, 205, `Index + WT: version=${merged ? 2 : 1}`, merged ? 'emphasis' : '')];
          return { caption, command: ['git rev-parse main origin/main','git -C ../writer push origin main','git fetch origin', integrate ? 'git merge --ff-only origin/main' : 'git status --short', 'git rev-parse HEAD main origin/main\ncat story.txt'][step], output: step === 4 ? `HEAD/main=${local}\norigin/main=${remoteRef}\nstory.txt: version=${merged ? 2 : 1}` : 'state shown above', nodes, edges: [edge('b','a'), ...(fetched ? [edge('track','b','',true)] : []), ...(merged ? [edge('head','b','',true)] : [])], facts: [['main', local], ['origin/main', remoteRef], ['story.txt in Index / WT', merged ? 'B / version=2' : 'A / version=1']] };
        });
      }
    },
    worktree: {
      label: ['图 09 / Worktree 共享与隔离', 'FIG 09 / WORKTREE SHARING AND ISOLATION'],
      choices: [
        { value: 'same', label: ['再次检出已使用的 main', 'Check out main a second time'] },
        { value: 'different', label: ['检出不同的 feature 分支', 'Check out a distinct feature branch'] }
      ],
      states(choice) {
        const different = choice === 'different';
        const captions = [
          ['primary 已检出 main。对象库与普通 refs 位于共享 common Git directory。', 'primary has main checked out. Objects and ordinary refs live in the shared common Git directory.'],
          different ? ['请求创建 linked worktree，并为它分配 feature/parallel。', 'Request a linked worktree on feature/parallel.'] : ['请求让第二个 worktree 也把 main 作为 HEAD。', 'Request a second worktree whose HEAD is also main.'],
          different ? ['Git 允许不同 branch。新 worktree 获得独立 HEAD、Index 与 Working Tree。', 'Git allows the distinct branch. The new worktree gets its own HEAD, index, and working tree.'] : ['Git 拒绝：main 已在 primary 检出，第二个 worktree 不会建立。', 'Git rejects the request: main is already checked out in primary, so no second worktree is created.'],
          different ? ['两个 worktree 可各自暂存文件，同时解析同一对象库和 refs。', 'The two worktrees can stage different files while resolving the same object store and refs.'] : ['拒绝保护同一普通 branch 不被两个独立检出状态同时推进。', 'The refusal prevents two independent checkout states from advancing the same ordinary branch.'],
          different ? ['primary 合入 feature 后，feature 的 HEAD 仍停在 feature/parallel。仓库外资源仍需单独协调。', 'After primary merges feature, feature HEAD remains on feature/parallel. Resources outside Git still require coordination.'] : ['选择不同 branch 可以成功；若只读检查同一 commit，也可评估 detached HEAD。', 'A distinct branch succeeds; for read-only checks at the same commit, detached HEAD may also fit.']
        ];
        return captions.map((caption, step) => {
          const created = different && step >= 2;
          const nodes = [node('common', 'common git dir', 'plain', 236, 25, 'objects + refs', 'emphasis'), node('primary', 'primary', 'content', 42, 165, 'HEAD main; index A'), node('feature', different ? 'feature worktree' : 'same-main', 'content', 430, 165, created ? 'HEAD feature; index B' : step >= 2 ? 'rejected' : 'requested', !created && step >= 2 ? 'gone' : created ? 'emphasis' : ''), node('external', 'external resource', 'plain', 624, 285, 'not isolated by Git')];
          return { caption, command: step === 1 ? (different ? 'git worktree add -b feature/parallel ../feature main' : 'git worktree add ../same-main main') : step === 3 && created ? 'git rev-parse --git-common-dir\ngit -C ../feature rev-parse --git-common-dir' : step === 4 && created ? 'git merge --no-ff feature/parallel' : 'git worktree list --porcelain', output: !different && step >= 2 ? "fatal: 'main' is already checked out" : created ? 'shared common dir\nseparate HEAD and index paths' : 'primary: main', nodes, edges: [edge('primary','common'), ...(created ? [edge('feature','common','',true)] : [])], facts: [['objects / refs', 'shared'], ['HEAD / Index / WT', created ? 'separate' : 'primary only'], ['external resources', 'not isolated']] };
        });
      }
    },
    storage: {
      label: ['图 10 / 逻辑内容与物理结构', 'FIG 10 / LOGICAL CONTENT AND PHYSICAL STRUCTURE'],
      choices: [
        { value: 'repack', label: ['重排可达对象并写 commit-graph', 'Repack reachable objects and write commit-graph'] },
        { value: 'prune', label: ['清理无引用的实验 orphan', 'Prune an unreferenced lab orphan'] }
      ],
      states(choice) {
        const prune = choice === 'prune';
        const captions = prune ? [
          ['stable commit C 由 main 可达；实验还写入一个没有引用的 orphan blob O。', 'Stable commit C is reachable from main; the lab also writes unreferenced orphan blob O.'],
          ['先保存 git show C 的输出，并确认 C 与 O 此刻都可读。', 'Save git show C output and confirm both C and O are currently readable.'],
          ['显式 prune --expire=now 只在这个可删除临时库中执行。', 'Explicit prune --expire=now runs only in this disposable lab repository.'],
          ['O 没有可达路径并被移除；main 继续保护 C。', 'O has no reachable path and is removed; main continues to protect C.'],
          ['git show C 前后完全一致。删除边界由可达性与过期条件决定。', 'git show C is byte-for-byte identical before and after. Reachability and expiration decide the deletion boundary.']
        ] : [
          ['逻辑层：main -> commit C -> tree -> blobs。物理层当前可以包含 loose objects。', 'Logical layer: main -> commit C -> tree -> blobs. The physical layer may currently contain loose objects.'],
          ['保存同一个 stable commit 的 git show 输出，作为逻辑不变量。', 'Save git show output for the same stable commit as the logical invariant.'],
          ['repack 可以把对象重排进 pack，并以 delta 表示相近对象。', 'repack may rearrange objects into packs and represent similar objects with deltas.'],
          ['commit-graph 写入提交遍历辅助结构；gc --no-prune 编排维护但不执行 loose-object prune。', 'commit-graph writes traversal metadata; gc --no-prune orchestrates maintenance without pruning loose objects.'],
          ['物理文件发生变化，git show C 仍完全一致。这里不声称固定体积或性能提升。', 'Physical files changed while git show C stayed identical. This makes no fixed size or performance claim.']
        ];
        return captions.map((caption, step) => {
          const changed = step >= 2, removed = prune && step >= 3;
          const nodes = [node('main','main','ref',42,35,'→ C'), node('c','C stable commit','commit',236,35,'logical snapshot','emphasis'), node('tree','tree','plain',430,35,'names → blobs'), node('blob','blob content','content',624,35,'stable bytes'), node('physical', prune ? 'orphan O' : changed ? 'pack + graph' : 'loose objects','plain',236,245, prune ? removed ? 'missing' : 'unreferenced' : changed ? 'physical layout changed' : 'physical layout', removed ? 'gone' : changed && !prune ? 'emphasis' : '')];
          return { caption, command: prune ? ['git show <C-id>','git cat-file -e <C-id>\ngit cat-file -e <O-id>','git prune --expire=now','git cat-file -e <O-id>','diff -u show-before.txt show-after.txt'][step] : ['git count-objects -vH','git show <C-id> > show-before.txt','git repack -ad','git commit-graph write --reachable\ngit gc --no-prune','diff -u show-before.txt show-after.txt'][step], output: step === 4 ? 'no diff for stable commit C' : removed ? 'O: missing\nC: readable' : 'state shown above', nodes, edges: [edge('main','c'),edge('c','tree'),edge('tree','blob')], facts: [['git show C', 'unchanged'], ['physical structure', prune ? removed ? 'orphan removed' : 'orphan present' : changed ? 'pack / graph may change' : 'observed only'], ['performance', 'not claimed']] };
        });
      }
    }
  };

  const root = document.querySelector('[data-curriculum]');
  if (!root || !lessons[root.dataset.curriculum]) return;
  const lesson = lessons[root.dataset.curriculum];

  class Model {
    constructor(element) {
      this.element = element;
      this.choice = lesson.choices[0].value;
      this.step = 0;
      this.running = false;
      this.elapsed = 0;
      this.last = 0;
      this.frame = 0;
      this.renderShell();
      this.bind();
      this.render();
    }
    renderShell() {
      this.element.innerHTML = `<div class="figure-shell"><div class="figure-top"><span class="figure-label"></span><label><span class="condition-label"></span><select class="choice"></select></label></div><svg class="diagram" viewBox="0 0 760 370" role="img"></svg><div class="result-strip"></div><div class="transport"><button class="previous" type="button">←</button><button class="play" type="button"></button><button class="next" type="button">→</button><input class="scrub" type="range" min="0" max="4" step="1" value="0"><output>1 / 5</output></div></div><p class="caption" aria-live="polite"></p><details class="commands"><summary></summary><p class="command-note"></p><pre class="command"></pre><pre class="output"></pre></details>`;
      this.svg = this.element.querySelector('svg');
      this.slider = this.element.querySelector('.scrub');
      this.play = this.element.querySelector('.play');
      this.select = this.element.querySelector('.choice');
    }
    bind() {
      this.element.querySelector('.previous').addEventListener('click', () => this.seek(this.step - 1));
      this.element.querySelector('.next').addEventListener('click', () => this.seek(this.step + 1));
      this.slider.addEventListener('input', () => this.seek(Number(this.slider.value)));
      ['pointerdown', 'click'].forEach(event => this.slider.addEventListener(event, () => this.pause()));
      this.slider.addEventListener('keydown', event => {
        if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End', 'PageUp', 'PageDown'].includes(event.key)) this.pause();
      });
      this.play.addEventListener('click', () => this.running ? this.pause() : this.start());
      this.select.addEventListener('change', () => { this.choice = this.select.value; this.seek(0); });
      this.element.addEventListener('keydown', event => {
        if (event.target !== this.element) return;
        if (event.key === 'ArrowLeft') { event.preventDefault(); this.seek(this.step - 1); }
        if (event.key === 'ArrowRight') { event.preventDefault(); this.seek(this.step + 1); }
        if (event.key === ' ') { event.preventDefault(); this.running ? this.pause() : this.start(); }
      });
    }
    seek(value) { this.pause(); this.step = Math.max(0, Math.min(4, value)); this.elapsed = 0; this.render(); }
    start() {
      const replaying = this.step === 4;
      if (replaying) this.step = 0;
      this.running = true; this.elapsed = 0; this.last = 0;
      if (replaying) this.render(); else this.updateControls();
      this.frame = requestAnimationFrame(time => this.tick(time));
    }
    pause() { this.running = false; cancelAnimationFrame(this.frame); this.last = 0; this.updateControls(); }
    tick(time) {
      if (!this.running) return;
      if (this.last) this.elapsed += Math.min(100, time - this.last);
      this.last = time;
      if (this.elapsed >= 2800) {
        this.elapsed = 0;
        if (this.step === 4) { this.pause(); return; }
        this.step += 1; this.render();
      }
      this.frame = requestAnimationFrame(next => this.tick(next));
    }
    updateControls() {
      this.play.textContent = this.running ? pick(['暂停', 'Pause']) : this.step === 4 ? pick(['重播', 'Replay']) : pick(['播放', 'Play']);
      this.play.setAttribute('aria-pressed', String(this.running));
    }
    render() {
      const state = lesson.states(this.choice)[this.step];
      const mobile = narrowScreen.matches;
      const nodeWidth = mobile ? 164 : 116;
      const nodeHeight = mobile ? 62 : 58;
      const stateNodes = mobile ? state.nodes.map((item, index) => ({
        ...item,
        x: 16 + (index % 2) * 194,
        y: 18 + Math.floor(index / 2) * 94
      })) : state.nodes;
      this.svg.setAttribute('viewBox', mobile ? '0 0 390 500' : '0 0 760 370');
      const positions = new Map(stateNodes.map(item => [item.id, item]));
      const defs = '<defs><marker id="course-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7" fill="none" stroke="var(--muted)" stroke-width="1"/></marker></defs>';
      const edgeMarkup = state.edges.map(item => {
        const from = positions.get(item.from), to = positions.get(item.to);
        const x1 = from.x + nodeWidth / 2, y1 = from.y + nodeHeight / 2, x2 = to.x + nodeWidth / 2, y2 = to.y + nodeHeight / 2;
        return `<path class="${item.active ? 'active-edge' : 'edge'}" marker-end="url(#course-arrow)" d="M${x1},${y1} L${x2},${y2}"/>${item.label ? `<text class="edge-label" x="${(x1+x2)/2}" y="${(y1+y2)/2-5}">${escape(item.label)}</text>` : ''}`;
      }).join('');
      const nodeMarkup = stateNodes.map(item => `<g class="node ${item.type} ${item.state}" transform="translate(${item.x} ${item.y})"><rect width="${nodeWidth}" height="${nodeHeight}"/><text x="10" y="24">${escape(item.label)}</text><text x="10" y="45" class="small">${escape(item.note)}</text></g>`).join('');
      this.svg.innerHTML = defs + edgeMarkup + nodeMarkup;
      this.svg.setAttribute('aria-label', pick(state.caption));
      this.element.querySelector('.caption').textContent = pick(state.caption);
      this.element.querySelector('.figure-label').textContent = pick(lesson.label);
      this.element.querySelector('.condition-label').textContent = pick(['条件', 'Condition']);
      this.select.innerHTML = lesson.choices.map(choice => `<option value="${choice.value}">${escape(pick(choice.label))}</option>`).join('');
      this.select.value = this.choice;
      this.select.setAttribute('aria-label', pick(['选择实验条件', 'Choose experiment condition']));
      this.element.querySelector('.result-strip').innerHTML = state.facts.map(([key, value]) => `<div><small>${escape(key)}</small><strong>${escape(value)}</strong></div>`).join('');
      this.element.querySelector('.command').textContent = state.command;
      this.element.querySelector('.output').textContent = state.output;
      this.element.querySelector('summary').textContent = pick(['展开本步命令与结果摘录', 'Show command and result excerpt']);
      this.element.querySelector('.command-note').textContent = pick(['示意图使用 C1 等教学标识。真实对象 ID 由临时实验仓库生成；浏览器不会执行命令。', 'The diagram uses teaching labels such as C1. The temporary lab generates real object IDs; the browser runs no commands.']);
      this.element.querySelector('.previous').disabled = this.step === 0;
      this.element.querySelector('.next').disabled = this.step === 4;
      this.element.querySelector('.previous').setAttribute('aria-label', pick(['上一步', 'Previous step']));
      this.element.querySelector('.next').setAttribute('aria-label', pick(['下一步', 'Next step']));
      this.slider.value = String(this.step);
      this.slider.setAttribute('aria-label', pick(['模型进度', 'Model progress']));
      this.slider.setAttribute('aria-valuetext', `${this.step + 1}/5: ${pick(state.caption)}`);
      this.element.querySelector('output').textContent = `${this.step + 1} / 5`;
      this.updateControls();
    }
  }

  const model = new Model(root);
  const translate = () => {
    document.documentElement.lang = language === 'en' ? 'en' : 'zh-CN';
    document.querySelectorAll('[data-en]').forEach(element => {
      if (!element.dataset.zh) element.dataset.zh = element.textContent;
      element.textContent = element.dataset[language];
    });
    document.querySelectorAll('[data-link-en]').forEach(element => {
      if (!element.dataset.linkZh) element.dataset.linkZh = element.href;
      element.href = language === 'en' ? element.dataset.linkEn : element.dataset.linkZh;
    });
    document.querySelectorAll('[data-course-link]').forEach(element => {
      const url = new URL(element.href, location.href);
      if (language === 'en') url.searchParams.set('lang', 'en'); else url.searchParams.delete('lang');
      element.href = url.href;
    });
    document.querySelector('.language').textContent = language === 'en' ? '中文' : 'English';
    document.title = `${document.querySelector('h1').textContent} | My Git`;
    model.render();
  };
  document.querySelector('.language').addEventListener('click', () => {
    language = language === 'en' ? 'zh' : 'en';
    const url = new URL(location.href);
    if (language === 'en') url.searchParams.set('lang', 'en'); else url.searchParams.delete('lang');
    history.replaceState(null, '', url);
    translate();
  });
  reducedMotion.addEventListener('change', () => { if (reducedMotion.matches) model.pause(); });
  narrowScreen.addEventListener('change', () => model.render());
  document.addEventListener('visibilitychange', () => { if (document.hidden) model.pause(); });
  translate();
})();
