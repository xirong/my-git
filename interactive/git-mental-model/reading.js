/* Small, deterministic teaching models. No shell commands run in the browser. */
(() => {
  'use strict';
  const en = new URLSearchParams(location.search).get('lang') === 'en';
  let language = en ? 'en' : 'zh';
  const pick = (zh, english) => language === 'en' ? english : zh;
  const media = matchMedia('(max-width: 600px)');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const escape = value => String(value).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const text = (x,y,value,cls='') => `<text x="${x}" y="${y}" class="${cls}">${escape(value)}</text>`;
  const line = (x1,y1,x2,y2,active=false) => {
    const route=`M${x1},${y1} L${x2},${y2}`;
    return `<path class="${active?'active-edge':'edge'}" d="${route}"/>`+
      (active?`<circle r="3" class="packet" style="offset-path:path('${route}')"/>`:'');
  };
  const box = (x,y,w,h,title,lines,cls='') => `<g class="node ${cls}"><rect x="${x}" y="${y}" width="${w}" height="${h}"/>${text(x+12,y+24,title)}${lines.map((s,i)=>text(x+12,y+46+i*19,s,'small')).join('')}</g>`;
  const snapshots = [
    {v:[1,1,1],zh:'起点：三个位置都是 version=1。HEAD 指向已有提交。',en:'Start: all three locations contain version=1. HEAD points to an existing commit.',cmd:'git show HEAD:app.txt\ngit show :app.txt\ncat app.txt',out:'version=1\nversion=1\nversion=1'},
    {v:[1,1,2],zh:'编辑只改变工作区。历史和提交草稿仍然保留 version=1。',en:'Editing changes only the working tree. History and the draft still contain version=1.',cmd:"printf 'version=2\\n' > app.txt\ngit status --short",out:' M app.txt'},
    {v:[1,2,2],zh:'git add 把此刻的内容写入 Index。草稿现在是 version=2。',en:'git add stages the content as it is now. The draft becomes version=2.',cmd:'git add app.txt\ngit show :app.txt',out:'version=2'},
    {v:[1,2,3],zh:'再次编辑后，三个版本同时存在。git add 不会持续跟踪你的编辑。',en:'Edit again: three versions coexist. git add does not keep tracking subsequent edits.',cmd:"printf 'version=3\\n' > app.txt\ngit status --short",out:'MM app.txt'},
    {v:[2,2,3],zh:'普通 git commit 记录 Index 中的 version=2。version=3 仍是未提交改动。',en:'A plain git commit records version=2 from the index. version=3 remains uncommitted.',cmd:'git commit -m "record version 2"\ngit show HEAD:app.txt\ngit status --short',out:'version=2\n M app.txt'}
  ];
  const graphCopy = [
    ['从名字开始。main 保存一个 commit 的对象 ID；它本身不是快照。','Start with a name. main stores a commit object ID; the branch itself is not a snapshot.'],
    ['读取 commit 才知道根 tree。parent 指向更早的提交，不是文件目录。','Reading the commit reveals its root tree. Its parent points to earlier history, not a directory.'],
    ['根 tree 的条目把文件名或目录名映射到对象。现在才知道 docs 在哪里。','Root-tree entries map filenames and directory names to objects. Only now do we know where docs is.'],
    ['进入 docs 的 tree，找到所选文件对应的 blob ID。','Read the docs tree to find the blob ID associated with the selected filename.'],
    ['blob 给出文件内容。改选另一个文件试试：不同路径可以共享同一份内容。','The blob supplies the content. Try the other filename: different paths can share the same content.']
  ];
  const drafts = [
    {index:[false,false],head:[false,false],zh:'Agent 改了两个地方：修复超时，也打开调试。先把它们分开判断。',en:'The agent made two changes: a timeout fix and debug logging. Evaluate them separately.',cmd:'git diff -- app.conf',out:'-timeout=10\n+timeout=30\n-debug=false\n+debug=true'},
    {index:[true,false],head:[false,false],zh:'只接受超时改动。Index 仍是完整文件：debug=false 也保留在草稿里。',en:'Stage only the timeout change. The index is a complete file: debug=false remains in the draft.',cmd:'git add -p -- app.conf\ngit show :app.conf',out:'timeout=30\n…\ndebug=false'},
    {index:[true,true],head:[false,false],zh:'如果把调试改动也暂存，它就会一起进入提交。文件名相同不代表意图相同。',en:'Staging debug logging too includes it in the next commit. One file can contain multiple intentions.',cmd:'git add -- app.conf\ngit show :app.conf',out:'timeout=30\n…\ndebug=true'},
    {index:[true,false],head:[false,false],zh:'只取消调试这一段的暂存，工作区仍保留两处改动。',en:'Unstage only the debug hunk. Both edits remain in the working tree.',cmd:'git restore --staged -p -- app.conf\ngit show :app.conf',out:'timeout=30\n…\ndebug=false'},
    {index:[true,false],head:[true,false],zh:'提交只包含超时修复；debug=true 仍在工作区。审查的是提交边界内的行为。',en:'The commit contains only the timeout fix; debug=true stays in the working tree. Review behavior within the commit boundary.',cmd:'git commit -m "fix: adjust timeout"\ngit show HEAD:app.conf\ngit status --short',out:'timeout=30\n…\ndebug=false\n M app.conf'}
  ];
  class Experiment {
    constructor(root) {
      this.root=root; this.kind=root.dataset.experiment; this.step=0; this.running=false; this.visible=false; this.autoStarted=false; this.elapsed=0; this.last=0; this.raf=0;
      this.root.innerHTML=`<div class="figure-shell"><div class="figure-top"><span class="figure-label"></span><select class="choice" ${this.kind==='graph'?'':'hidden'}><option value="guide">docs/guide.txt</option><option value="copy">docs/copy.txt</option></select><span class="metric"></span></div><svg class="diagram" role="img"></svg><div class="transport"><button class="previous" type="button">←</button><button class="play" type="button"></button><button class="next" type="button">→</button><input class="scrub" type="range" min="0" max="4" step="1" value="0"><output>1 / 5</output></div></div><p class="caption" aria-live="polite"></p><details class="commands"><summary></summary><p class="command-note"></p><pre class="command"></pre><pre class="output"></pre></details>`;
      this.svg=root.querySelector('svg'); this.caption=root.querySelector('.caption'); this.slider=root.querySelector('.scrub'); this.playButton=root.querySelector('.play');
      root.querySelector('.previous').addEventListener('click',()=>this.seek(this.step-1));
      root.querySelector('.next').addEventListener('click',()=>this.seek(this.step+1));
      this.slider.addEventListener('input',()=>this.seek(Number(this.slider.value)));
      ['keydown','pointerdown'].forEach(event=>this.slider.addEventListener(event,()=>{this.autoStarted=true;this.pause();}));
      this.playButton.addEventListener('click',()=>{if(this.running)this.pause();else {if(this.step===4){this.step=0;this.elapsed=0;this.render();}this.start();}});
      root.querySelector('.choice').addEventListener('change',()=>this.seek(0));
      this.render();
    }
    seek(step){this.autoStarted=true;this.pause();this.step=Math.min(4,Math.max(0,step));this.elapsed=0;this.render();}
    start(){if(this.running)return;this.autoStarted=true;this.running=true;this.last=0;this.updateControls();this.raf=requestAnimationFrame(t=>this.tick(t));}
    pause(){this.running=false;cancelAnimationFrame(this.raf);this.last=0;this.updateControls();}
    tick(t){if(!this.running)return;if(this.last)this.elapsed+=Math.min(t-this.last,100);this.last=t;if(this.elapsed>=3000){this.elapsed=0;if(this.step<4){this.step++;this.render();}else{this.pause();return;}}this.raf=requestAnimationFrame(ts=>this.tick(ts));}
    updateControls(){this.root.classList.toggle('paused',!this.running);this.playButton.textContent=this.running?pick('暂停','Pause'):(this.step===4?pick('重播','Replay'):pick('播放','Play'));this.playButton.setAttribute('aria-pressed',String(this.running));}
    render(){
      const mobile=media.matches,w=mobile?360:720,h=mobile?390:320;
      this.svg.setAttribute('viewBox',`0 0 ${w} ${h}`);
      let drawing='',caption='',cmd='',out='';
      if(this.kind==='snapshots'){
        const state=snapshots[this.step];caption=state[language];cmd=state.cmd;out=state.out;
        const labels=['HEAD','INDEX','WORKING TREE'];
        const roles=[pick('已提交','Committed'),pick('下次提交的草稿','Next commit draft'),pick('正在编辑','Editing')];
        for(let i=0;i<3;i++){
          const x=mobile?82:35+i*232,y=mobile?18+i*118:95;
          drawing+=box(x,y,mobile?206:184,94,labels[i],[roles[i],`app.txt   version=${state.v[i]}`],i===0?'green':i===1?'orange':'blue');
          if(i<2)drawing+=mobile?line(185,y+94,185,y+118):line(x+184,y+47,x+232,y+47);
        }
        if(!mobile)drawing+=text(35,46,pick('同一个文件 · 三个版本','ONE FILE · THREE VERSIONS'),'small')+text(35,259,pick('提交之后，工作区也可以和 HEAD 不同。','The working tree can differ from HEAD even after a commit.'),'small');
      } else if(this.kind==='graph') {
        drawing+='<defs><marker id="lookup-arrow" markerWidth="5" markerHeight="5" refX="5" refY="2.5" orient="auto"><path d="M0,0 L5,2.5 L0,5" fill="none" stroke="var(--muted)" stroke-width=".8"/></marker></defs>';
        const filename=this.root.querySelector('.choice').value==='copy'?'copy.txt':'guide.txt';
        caption=graphCopy[this.step][language==='en'?1:0];
        const cx=mobile?20:38,tx=mobile?158:256,bx=mobile?158:502;
        drawing+=text(cx,25,'REF / COMMIT','small')+text(tx,25,'TREE','small')+(mobile?'':text(bx,25,'BLOB','small'));
        drawing+=line(cx+50,71,cx+50,119,this.step===1);
        drawing+=line(cx+100,155,tx,155,this.step===2);
        drawing+=line(tx+62,191,tx+62,228,this.step===3);
        drawing+=mobile?line(tx+62,294,tx+62,325,this.step===4):line(tx+124,262,bx,262,this.step===4);
        drawing+=line(cx+50,191,cx+50,245);
        drawing+=box(cx,41,100,30,'main',[],this.step===0?'orange':'');
        drawing+=box(cx,119,100,72,'commit C2',['root → T1'],this.step>=1?'green':'pending');
        drawing+=box(cx,245,100,54,'parent C1',[],'pending');
        drawing+=box(tx,119,124,72,'root T1',['docs → T2'],this.step>=2?'orange':'pending');
        drawing+=box(tx,228,124,66,'docs T2',[`${filename} → B1`],this.step>=3?'orange':'pending');
        drawing+=box(bx,mobile?325:228,mobile?124:160,mobile?52:66,'blob B1',['hello'],this.step>=4?'blue':'pending');
        if(!mobile)drawing+=text(502,133,pick('名字属于 tree。','Names belong to trees.'),'small')+text(502,153,pick('内容属于 blob。','Content belongs to blobs.'),'small');
        const commands=['git rev-parse main','git cat-file -p main','git ls-tree main','git ls-tree main:docs',`git show main:docs/${filename}`];
        const outputs=['<C2 commit ID>','tree <T1 ID>\nparent <C1 ID>\n…','040000 tree <T2 ID>\tdocs','100644 blob <B1 ID>\tcopy.txt\n100644 blob <B1 ID>\tguide.txt','hello'];
        cmd=commands[this.step];out=outputs[this.step];
      } else {
        const state=drafts[this.step];caption=state[language];cmd=state.cmd;out=state.out;
        const values=[[true,true],state.index,state.head];
        ['WORKING TREE','INDEX','HEAD'].forEach((title,i)=>{
          const x=mobile?80:30+i*233,y=mobile?15+i*119:97;
          drawing+=box(x,y,mobile?210:196,97,title,[`timeout=${values[i][0]?30:10}`,'…',`debug=${values[i][1]?'true':'false'}`],i===1?'orange':i===2?'green':'blue');
          if(i<2)drawing+=mobile?line(185,y+97,185,y+119):line(x+196,y+46,x+233,y+46,this.step===1&&i===0||this.step===4&&i===1);
        });
        if(!mobile)drawing+=text(30,44,pick('app.conf · 一个文件，两种意图','app.conf · ONE FILE, TWO INTENTIONS'),'small')+text(30,255,pick('Index 保存完整草稿，未修改的内容也在其中。','The index holds a complete draft, including unchanged content.'),'small');
      }
      this.svg.innerHTML=drawing;this.svg.setAttribute('aria-label',caption);this.caption.textContent=caption;
      this.root.querySelector('.figure-label').textContent={snapshots:pick('图 01 / 快照与状态','FIG 01 / SNAPSHOTS'),graph:pick('图 02 / 沿引用查找','FIG 02 / OBJECT LOOKUP'),index:pick('图 03 / 选择提交内容','FIG 03 / THE COMMIT DRAFT')}[this.kind];
      this.root.querySelector('.metric').textContent=this.kind==='graph'?pick(`读取 ${this.step} 个对象`,`${this.step} OBJECTS READ`):pick('状态示意','STATE MODEL');
      this.root.querySelector('.choice').setAttribute('aria-label',pick('选择要查找的文件','Choose a file to look up'));
      this.root.querySelector('.previous').setAttribute('aria-label',pick('上一步','Previous step'));this.root.querySelector('.next').setAttribute('aria-label',pick('下一步','Next step'));
      this.root.querySelector('.previous').disabled=this.step===0;this.root.querySelector('.next').disabled=this.step===4;
      this.slider.value=String(this.step);this.slider.setAttribute('aria-label',pick('演示进度','Demonstration progress'));this.slider.setAttribute('aria-valuetext',`${this.step+1}/5: ${caption}`);
      this.root.querySelector('output').textContent=`${this.step+1} / 5`;
      this.root.querySelector('summary').textContent=pick('用真实 Git 验证这一步','Verify this step with Git');
      this.root.querySelector('.command-note').textContent=this.kind==='graph'?pick('C2、T1、T2、B1 是示意标识，真实 ID 取决于实验仓库。','C2, T1, T2 and B1 are diagram labels. Real IDs depend on the lab repository.'):pick('命令与输出仅摘录相关部分。省略号代表未修改的中间行；部分暂存需按实际补丁逐段选择。浏览器不执行命令。','Commands and output are excerpts. Ellipses stand for unchanged middle lines; select hunks after inspecting the actual patch. The browser does not execute commands.');
      const setup=document.createElement('a');setup.href='../../labs/git-mental-model/reading-experiments/README.md';setup.textContent=pick(' 完整初始化与真实 Git 自测 ↗',' Complete setup and real Git checks ↗');this.root.querySelector('.command-note').append(setup);
      this.root.querySelector('.command').textContent=cmd;this.root.querySelector('.output').textContent=out;this.updateControls();
    }
  }
  const experiments=[...document.querySelectorAll('[data-experiment]')].map(el=>new Experiment(el));
  function translate(){
    document.documentElement.lang=language==='en'?'en':'zh-CN';
    document.querySelectorAll('[data-en]').forEach(el=>{if(!el.dataset.zh)el.dataset.zh=el.textContent;el.textContent=el.dataset[language];});
    document.querySelectorAll('[data-link-en]').forEach(el=>{if(!el.dataset.linkZh)el.dataset.linkZh=el.getAttribute('href');el.setAttribute('href',language==='en'?el.dataset.linkEn:el.dataset.linkZh);});
    document.querySelectorAll('[data-demo-link]').forEach(el=>{const url=new URL(el.getAttribute('href'),location.href);url.searchParams.set('lang',language);el.setAttribute('href',url.pathname+url.search+url.hash);});
    document.title=document.querySelector('h1').textContent+' | My Git';
    document.querySelector('.language').textContent=pick('English','中文');experiments.forEach(e=>e.render());
  }
  document.querySelector('.language').addEventListener('click',()=>{language=language==='zh'?'en':'zh';translate();const url=new URL(location.href);url.searchParams.set('lang',language);history.replaceState(null,'',url);});
  const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{const e=experiments.find(item=>item.root===entry.target);e.visible=entry.isIntersecting&&entry.intersectionRatio>=.5;if(!e.visible)e.pause();else if(!e.autoStarted&&!motion.matches&&!document.hidden){e.autoStarted=true;e.start();}}),{threshold:[0,.5]});
  experiments.forEach(e=>observer.observe(e.root));
  document.addEventListener('visibilitychange',()=>{if(document.hidden)experiments.forEach(e=>e.pause());});
  media.addEventListener('change',()=>experiments.forEach(e=>e.render()));motion.addEventListener('change',()=>{if(motion.matches)experiments.forEach(e=>e.pause());});
  translate();
})();
