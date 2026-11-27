import sys,os,json,glob,shutil
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from cpd import load,save
import os
SRC=os.environ.get('P27SRC','m27orig'); DST=os.environ.get('P27DST','m27')
for f in glob.glob(SRC+'/*.dc.html'): shutil.copy(f, DST)
def rd(n): return open(DST+'/'+n).read()
def wr(n,s): open(DST+'/'+n,'w').write(s)
def rep(s,a,b,cnt=1,name=''):
    n=s.count(a)
    assert n==cnt, (name,a[:60],n)
    return s.replace(a,b)
def addcss(s,css,tag):
    if tag in s: return s
    i=s.index('</style>')
    return s[:i]+'\n/* '+tag+' */\n'+css+'\n'+s[i:]

# ---------- A. sidebar: 高危命令 敬请期待 (all pages)
SOON_CSS='.kc-side .kc-ki[href*="SecRunCmd"] em{flex:none;margin-left:auto;padding:0 6px;line-height:18px;border-radius:2px;background:#f2f3f5;color:rgba(0,0,0,.45);font-size:11px}'
for f in sorted(glob.glob(DST+'/*.dc.html')):
    n=os.path.basename(f); s=rd(n)
    if "'防护设置', '高危命令', " in s:
        s=s.replace("'防护设置', '高危命令', ","'防护设置', ['高危命令', '敬请期待'], ")
        s=addcss(s,SOON_CSS,'soon27')
        wr(n,s)

# ---------- B. SecRunCmd coming-soon page
n='SecRunCmd.dc.html'; s=rd(n)
lines=s.split('\n')
hi=[i for i,l in enumerate(lines) if 'class="kc-hd"><div class="kc-hdl"><span class="cp-ic">' in l]; assert len(hi)==1
mi=[i for i,l in enumerate(lines) if l.strip()=='</main>']; assert len(mi)==1
h=hi[0]; m=mi[0]
SOON='''      <sc-if value="{{cp.soon}}" hint-placeholder-val="{{true}}"><section class="kc-card rc-soon"><div class="rc-soon-ic" aria-hidden="true"><svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><path d="M3 3H21C21.5523 3 22 3.44772 22 4V20C22 20.5523 21.5523 21 21 21H3C2.44772 21 2 20.5523 2 20V4C2 3.44772 2.44772 3 3 3ZM4 5V19H20V5H4ZM12 15H18V17H12V15ZM8.66685 12L5.83842 9.17157L7.25264 7.75736L11.4953 12L7.25264 16.2426L5.83842 14.8284L8.66685 12Z"></path></svg></div><h2>高危命令防护 · 敬请期待</h2><p class="rc-soon-d">这项能力正在开发中，下一阶段上线。上线后会在消息中心通知你，不需要重新安装客户端。</p><ul class="rc-soon-l"><li>识别下载并执行远程脚本、清除系统日志、篡改关键文件权限、添加 SSH 公钥等高危操作</li><li>命中后按防护档位处理：只告警、确认后处置或自动拦截</li><li>支持自定义规则和按主机加白</li></ul><p class="rc-soon-n">现在遇到可疑命令，可以在「威胁调查」里按主机查看进程和命令行。</p><div class="rc-soon-b"><a class="kc-btn" href="SecHunt.dc.html">去威胁调查</a></div><p class="rc-soon-x">原型说明：上线时这一页只显示上面的内容，菜单项带「敬请期待」，不隐藏。<a href="#" onClick="{{cp.soonGo}}">查看后续版本的设计</a></p></section></sc-if>
      <sc-if value="{{cp.full}}" hint-placeholder-val="{{false}}"><div class="ac-al w rc-later"><i>!</i><span>下面是后续版本的设计，本期上线不显示。</span><a href="#" onClick="{{cp.soonBack}}">返回上线状态</a></div>'''
lines.insert(h+1,SOON)
# close sc-if before </main>  (m shifted by 1)
lines.insert(m+1,'      </sc-if>')
s='\n'.join(lines)
s=rep(s,"    const o = {};\n    const qs0 =","    const o = {};\n    /* soon27 */ o.soon = st.cpSoon === undefined ? true : !!st.cpSoon; o.full = !o.soon; o.soonGo = ev(() => set({ cpSoon: false })); o.soonBack = ev(() => set({ cpSoon: true }));\n    const qs0 =",name='cmd-o')
s=addcss(s,'''.rc-soon{padding:56px 40px 40px;text-align:center}
.rc-soon .rc-soon-ic{width:56px;height:56px;margin:0 auto 16px;border-radius:12px;background:#e8f3ff;color:#1664ff;display:flex;align-items:center;justify-content:center}
.rc-soon h2{margin:0 0 8px;font-size:18px;font-weight:600;color:rgba(0,0,0,.9)}
.rc-soon .rc-soon-d{margin:0 0 20px;font-size:13px;color:rgba(0,0,0,.55)}
.rc-soon .rc-soon-l{display:inline-block;margin:0 0 16px;padding:16px 24px 16px 40px;text-align:left;background:#f7f8fa;border-radius:4px;font-size:13px;line-height:24px;color:rgba(0,0,0,.7)}
.rc-soon .rc-soon-n{margin:0 0 16px;font-size:12px;color:rgba(0,0,0,.5)}
.rc-soon .rc-soon-b{display:flex;justify-content:center;gap:8px;margin-bottom:32px}
.rc-soon .rc-soon-x{margin:0;padding-top:16px;border-top:1px dashed #e5e6eb;font-size:12px;color:rgba(0,0,0,.4)}
.rc-soon .rc-soon-x a,.rc-later a{margin-left:8px;color:#1664ff;text-decoration:none}
.rc-later{margin-bottom:16px}''','soon27p')
wr(n,s)

# ---------- C. SecNetGuard 外联
n='SecNetGuard.dc.html'; s,d,i,j=load(DST+'/'+n)
M=dict((k,v) for k,v in d['modes'])
M['轻量模式'].append('外联：命中威胁情报里的高危 IP 只告警，不阻断')
M['标准模式'].append('外联：阻断威胁情报里的高危 IP，其他外联正常放行，不影响业务')
M['重保模式'].append('外联：阻断全部海外连接（中国大陆以外），重保期间一刀切')
d['modes']=[[k,M[k]] for k,_ in d['modes']]
out=[t for t in d['tabs'] if t['k']=='out'][0]
for r in out['rows']:
    if r['id']=='o2':
        r.update({'n':'高危 IP 阻断','obj':'威胁情报库里的远控、矿池、恶意下载地址（情报库 11-27 06:00 自动更新）','sc':'跟随防护模式'})
    if r['id']=='o3':
        r.update({'n':'数据库海外 IP 封禁'})
out['rows'].insert(2,{"id":"o7","n":"重保：阻断全部海外连接","typ":"地域规则","obj":"中国大陆以外的全部地址","act":"阻断","log":"记录","sc":"仅重保模式（未生效）","sw":True,"hit":0,"last":"11-08 09:00 至 11-10 18:20"})
lg=[t for t in d['tabs'] if t['k']=='log'][0]
lg['rows'][0:0]=[{"id":"l7","t":"11-27 06:00","ch":"威胁情报库自动更新：新增高危 IP 1,203 个，移除 85 个","who":"系统","st":"已更新"},{"id":"l6","t":"11-26 06:00","ch":"威胁情报库自动更新：新增高危 IP 964 个，移除 120 个","who":"系统","st":"已更新"}]
lg.setdefault('opsBy',{})['已更新']=[]
d['STC']['已更新']='kc-tag info'
d['help'].insert(2,'外联管控跟随防护模式：标准模式只阻断威胁情报里的高危 IP，不影响正常业务；重保模式阻断全部海外连接，适合护网、重保期间。威胁情报库每天自动更新，每次更新记在「变更记录」里，操作人显示为「系统」。')
save(DST+'/'+n,s,d,i,j)

# ---------- D. SecVirus 扫描速度
n='SecVirus.dc.html'; s,d,i,j=load(DST+'/'+n)
sc=[t for t in d['tabs'] if t['k']=='scan'][0]
sc['cols'].insert(3,["速度",90,"spd",""])
sc['rkv'].insert(3,["速度","spd"])
sc['form'].insert(3,{"f":"spd","n":"扫描速度","o":["慢","正常","快"]})
sc['blank']['spd']='慢'
for r in sc['rows']: r['spd']={'s1':'慢','s2':'慢','s3':'正常'}.get(r['id'],'慢')
d['help'].insert(1,'扫描速度分三档：慢（默认，固定占用 1 个核心，不影响业务）、正常（占用 2 个核心）、快（按主机配置自动分配，最多占约 50% CPU）。实时检测已经会检查新落地的文件，定时扫描主要查以前就存在的文件，所以默认用慢速。快速扫描最长 1 小时，到时自动结束。')
save(DST+'/'+n,s,d,i,j)
s=rd(n)
s=rep(s,"const sm = st.cpSm || '快速';","const sm = st.cpSm || '快速'; const spd = st.cpSpd || '慢'; /* spd27 */",name='spd1')
s=rep(s,"' 台在线主机' + (sm === '全盘' ?","' 台在线主机 · 速度' + spd + (sm === '全盘' ?",name='spd2')
s=rep(s,"'，全盘扫描预计 40 分钟，可以离开这个页面，完成后通知你' : '，快速扫描只查系统目录、启动项和","(spd === '快' ? '，全盘扫描预计 25 分钟' : spd === '正常' ? '，全盘扫描预计 60 分钟' : '，全盘扫描预计 2 小时') + '，可以离开这个页面，完成后通知你' : '，快速扫描最长 1 小时，只查系统目录、启动项和",name='spd3')
s=rep(s,": done ? '刚刚 · ' + nOn2 + ' 台在线主机 · 实时检测运行中' : SC.sub;",": done ? '刚刚 · ' + nOn2 + ' 台在线主机 · 实时检测运行中' : SC.sub + ' · 扫描速度：' + spd + '（' + ({ '慢': '默认，不影响业务', '正常': '占用 2 核', '快': '最多约 50% CPU' })[spd] + '）';",name='spd7')
s=rep(s,"const stp = sm === '快速' ? 2 : 1;","const stp = (sm === '快速' ? 2 : 1) * (spd === '快' ? 2 : 1);",name='spd4')
s=rep(s,"o.vscBt = ing ? '停止扫描' : '立即扫描';","o.vscSpd = [['慢', '默认：固定占用 1 个核心，不影响业务'], ['正常', '占用 2 个核心'], ['快', '按主机配置自动分配，最多占约 50% CPU']].map(([n, t]) => ({ n, t, cls: n === spd ? 'cpv-sg on' : 'cpv-sg', go: ev(() => { if (ing) { toast('扫描进行中，下次扫描按新速度执行'); } set({ cpSpd: n }); }) })); o.vscSpdT = ({ '慢': '默认，固定占用 1 个核心，不影响业务', '正常': '占用 2 个核心', '快': '最多占约 50% CPU，业务高峰慎用' })[spd];\n      o.vscBt = ing ? '停止扫描' : '立即扫描';",name='spd5')
s=rep(s,'<button type="button" class="{{cp.vscBc}}" onClick="{{cp.vscGo}}">{{cp.vscBt}}</button></div>','<button type="button" class="{{cp.vscBc}}" onClick="{{cp.vscGo}}">{{cp.vscBt}}</button><div class="cpv-spd"><span>扫描速度</span><span class="cpv-seg" role="group" aria-label="扫描速度"><sc-for list="{{cp.vscSpd}}" as="g" hint-placeholder-count="3"><button type="button" class="{{g.cls}}" title="{{g.t}}" onClick="{{g.go}}">{{g.n}}</button></sc-for></span></div></div>',name='spd6')
s=addcss(s,'''.cpv-act{flex-wrap:wrap;justify-content:flex-end;row-gap:10px;max-width:340px}
.cpv-spd{flex-basis:100%;display:flex;align-items:center;justify-content:flex-end;gap:8px;font-size:12px;color:rgba(0,0,0,.55);white-space:nowrap}
.cpv-spd .cpv-sg{height:26px;padding:0 12px;font-size:12px;white-space:nowrap}
.cpv-spd em{font-style:normal;color:rgba(0,0,0,.4);width:100%;text-align:right}''','spd27css')
wr(n,s)

# ---------- E. SecLoginAuth 登录告警 + 弱口令
n='SecLoginAuth.dc.html'; s,d,i,j=load(DST+'/'+n)
rule=[t for t in d['tabs'] if t['k']=='rule'][0]
k=[x['id'] for x in rule['rows']].index('r3')+1
rule['rows'][k:k]=[
 {"id":"r10","n":"密码错误登录","src":"系统","typ":"登录失败","cond":"进入登录界面后输错密码；同一来源 10 分钟内多次失败合并为一条，显示次数","act":"告警","sc":"全部主机","sw":True,"hit":64,"last":"11-11 09:57","kv":[["只连端口未登录","算暴力破解，在网络访问防护处理"],["登录成功","不产生告警；常用来源可以添加为可信来源"]]},
 {"id":"r11","n":"弱口令检测","src":"系统","typ":"密码强度","cond":"检查系统账号的密码强度，太弱就告警提醒修改；不强制改密码，也不禁止登录","act":"告警","sc":"全部主机","sw":True,"hit":3,"last":"11-27 08:00","kv":[["默认","开启"],["关闭或忽略","记录操作人，在变更记录和操作审计里能查到"]]}]
for sel in rule['sels']:
    if sel['f']=='typ': sel['o']+=['登录失败','密码强度']
d['help'].insert(1,'登录告警怎么分：只连到登录端口、没进入登录界面的，算暴力破解，在「网络访问防护」处理；进入登录界面但输错密码的，算异常登录，同一来源多次失败合并成一条并显示次数；登录成功不提醒。')
d['help'].insert(2,'弱口令检测默认开启，发现弱密码只告警、提醒修改，不会强制改密码，也不会禁止登录。关闭检测或忽略弱口令告警，都会记录是谁操作的。')
M=dict((k2,v) for k2,v in d['modes'])
M['标准模式'].insert(2,'输错密码的登录合并成一条告警，登录成功不提醒；弱口令检测开启')
d['modes']=[[k2,M[k2]] for k2,_ in d['modes']]
lg=[t for t in d['tabs'] if t['k']=='log'][0]
lg['rows'][0:0]=[{"id":"l3","t":"11-27 09:12","ch":"忽略弱口令告警：app-03 账号 test（原因：测试账号，下周停用）","who":"张三（安全运营）","st":"已生效"}]
save(DST+'/'+n,s,d,i,j)

# ---------- F. SecEvents 弱口令告警 + 登录失败合并
n='SecEvents.dc.html'; s=rd(n)
i=s.index('const EVD = ')+12; d,e=json.JSONDecoder().raw_decode(s[i:]); j=i+e
for ev in d['EV']:
    for r in ev['recs']:
        if r[2]=='root 密码登录失败 312 次':
            r[2]='root 输错密码 312 次（已合并为 1 条）'; r[3]='进入登录界面后输错密码 · 来源 45.142.xx.xx（荷兰），1 小时内'
pos=[k for k,ev in enumerate(d['EV']) if ev['st']=='待研判'][-1]+1
d['EV'].insert(pos,{"id":"EV-3214","lv":"低危","h":"app-03","st":"待研判","t":"账号 test 使用弱口令","f":"11-27 08:00","l":"11-27 08:00","clue":"同一账号 test","how":"仅告警","recs":[["11-27 08:00","登录安全防护","弱口令检测：账号 test 的密码太弱","8 位纯数字，命中常见弱口令字典","告警",""]],"adv":"建议尽快把 test 账号的密码改成 12 位以上、包含大小写字母、数字和符号。卫士不会强制改密码，也不会禁止登录。确认不用处理可以忽略，忽略会记录操作人。","auto":[]})
d['EV'].append({"id":"EV-3209","lv":"低危","h":"cache-01","st":"已忽略","t":"账号 backup 使用弱口令","f":"11-26 08:00","l":"11-26 08:00","clue":"同一账号 backup","how":"仅告警","recs":[["11-26 08:00","登录安全防护","弱口令检测：账号 backup 的密码太弱","与账号名相同","告警",""]],"adv":"已忽略。忽略人和原因已记录，在操作审计里可以查到。","auto":[],"ign":"内网备份专用账号，禁止远程登录 · 忽略人 张三（安全运营）· 11-26 09:12"})
s=s[:i]+json.dumps(d,ensure_ascii=False)+s[j:]
wr(n,s)
print('ok')

# ---------- G. SecHosts 主机过户
n='SecHosts.dc.html'; s=rd(n)
s=rep(s,"                ['删除', 'hs-dm', () => S({ hmq: h.n })]]",
"                ['过户到其他账号', '', () => { S({ hmo: '', xfH: h.n, xfIp: h.ip, xfAcc: '', xfP: {}, xfE: '' }); }],\n                ['删除', 'hs-dm', () => S({ hmq: h.n })]]",name='xf-more')
s=rep(s,"const o = this._rv(); o.hd = Object.assign(this._hdr(), this._top());","const o = this._rv(); o.xf = this._xf(); o.hd = Object.assign(this._hdr(), this._top());",name='xf-rv')
XF_JS='''  /* xf27 主机过户 */
  _xf() {
    const st = this.state || {}; const S = (o) => this.setState(o);
    const ev = (f) => (e) => { if (e && e.preventDefault) e.preventDefault(); if (e && e.stopPropagation) e.stopPropagation(); f(e); };
    const h = st.xfH || ''; const x = { on: !!h, h, ip: st.xfIp || '', t: st.xfT || '', tOn: !!st.xfT };
    const TK = ({ 'web-prod-01': [['病毒查杀 · 全盘扫描', '已进行 18 分钟，完成约 40%', 1]], 'db-01': [['漏洞扫描', '已进行 6 分钟，预计还要 12 分钟', 0], ['基线检查', '排队中', 1]] })[h] || [];
    const ps = st.xfP || {};
    x.tasks = TK.map(([n, s0, can]) => { const p = !!ps[n]; return { n, s: p ? '已暂停，过户后由对方决定是否重新执行' : s0, canP: !!can, pT: p ? '已暂停' : '暂停', pC: p ? 'kc-btn dis' : 'kc-btn', p: ev(() => { if (!p) S({ xfP: Object.assign({}, ps, { [n]: 1 }), xfE: '' }); }), wait: !can, w: '暂停不了，扫完才能过户' }; });
    x.noTask = !x.tasks.length; x.hasTask = !x.noTask;
    const waitScan = TK.some((t) => !t[2]); const needPause = TK.some((t) => t[2] && !ps[t[0]]);
    x.acc = st.xfAcc || ''; x.onAcc = (e) => S({ xfAcc: e.target.value, xfE: '' });
    x.err = st.xfE || ''; x.hasErr = !!x.err;
    x.okC = waitScan || needPause || !x.acc.trim() ? 'kc-btn pri dis' : 'kc-btn pri';
    x.x = ev(() => S({ xfH: '', xfAcc: '', xfP: {}, xfE: '' }));
    x.ok = ev(() => {
      if (!x.acc.trim()) { S({ xfE: '请填写接收账号' }); return; }
      if (waitScan) { S({ xfE: '漏洞扫描还没结束，扫完后才能过户' }); return; }
      if (needPause) { S({ xfE: '请先暂停正在运行的任务' }); return; }
      S({ xfH: '', xfAcc: '', xfP: {}, xfE: '', xfT: h + ' 的过户申请已提交，等对方 24 小时内确认接收' }); clearTimeout(this._xfTm); this._xfTm = setTimeout(() => this.setState({ xfT: '' }), 3200); });
    return x;
  }
'''
s=rep(s,"\n  _rv() {","\n"+XF_JS+"  _rv() {",name='xf-m')
XF_T='''      <sc-if value="{{xf.on}}" hint-placeholder-val="{{false}}"><div class="sh-mask sh-fx" onClick="{{xf.x}}"></div><aside class="sh-dw sh-fx xf-dw" role="dialog" aria-modal="true" aria-label="过户到其他账号"><header><h3>过户到其他账号</h3><button type="button" class="sh-x" aria-label="关闭" onClick="{{xf.x}}">×</button></header><div class="sh-dwb"><div class="hx-form">
        <div class="hx-f"><div class="hx-fl"><span>主机</span></div><p class="xf-v"><b>{{xf.h}}</b>{{xf.ip}}</p></div>
        <div class="hx-f"><div class="hx-fl"><span>接收账号</span><em>*</em></div><input class="kc-in" type="text" value="{{xf.acc}}" onInput="{{xf.onAcc}}" placeholder="对方的德迅云账号 ID 或手机号" aria-label="接收账号"><p class="hx-sd">适用于代运维交还主机、管理员离职交接等场景。对方 24 小时内确认接收后才完成过户，确认前主机仍在你的账号下，防护照常。</p></div>
        <div class="hx-f"><div class="hx-fl"><span>哪些数据跟着主机走</span></div><ul class="xf-l"><li class="y">防护配置：防护模式、单独调整、规则和白名单</li><li class="y">告警记录和处置结果</li><li class="n">操作记录不转：留在你的账号，在操作审计里仍可查看</li></ul></div>
        <div class="hx-f"><div class="hx-fl"><span>正在运行的任务</span></div><sc-if value="{{xf.noTask}}" hint-placeholder-val="{{true}}"><p class="hx-h">没有正在运行的任务，可以直接过户。</p></sc-if><sc-if value="{{xf.hasTask}}" hint-placeholder-val="{{false}}"><div class="xf-ts"><sc-for list="{{xf.tasks}}" as="t" hint-placeholder-count="1"><div class="xf-t"><span><b>{{t.n}}</b><em>{{t.s}}</em></span><sc-if value="{{t.canP}}" hint-placeholder-val="{{true}}"><button type="button" class="{{t.pC}}" onClick="{{t.p}}">{{t.pT}}</button></sc-if><sc-if value="{{t.wait}}" hint-placeholder-val="{{false}}"><span class="xf-w">{{t.w}}</span></sc-if></div></sc-for></div><p class="hx-sd">过户前要先暂停正在运行的任务；漏洞扫描暂停不了，要等它扫完。</p></sc-if></div>
        <div class="hx-f"><div class="hx-fl"><span>授权</span></div><p class="hx-h">过户后这台主机占用对方账号的卫士授权，你的账号空出 1 个名额。对方没有空余授权时无法确认接收。</p></div>
        <sc-if value="{{xf.hasErr}}" hint-placeholder-val="{{false}}"><p class="hx-err">{{xf.err}}</p></sc-if>
      </div></div><footer><button type="button" class="kc-btn" onClick="{{xf.x}}">取消</button><button type="button" class="{{xf.okC}}" onClick="{{xf.ok}}">提交过户</button></footer></aside></sc-if>
      <sc-if value="{{xf.tOn}}" hint-placeholder-val="{{false}}"><div class="sh-toast sh-fx" role="status"><i class="ok"></i>{{xf.t}}</div></sc-if>
'''
lines=s.split('\n'); mi=[k for k,l in enumerate(lines) if l.strip()=='</main>']; assert len(mi)==1
lines.insert(mi[0],XF_T.rstrip('\n')); s='\n'.join(lines)
s=addcss(s,'''.xf-dw .xf-v{margin:0;font-size:13px;color:rgba(0,0,0,.55)}
.xf-dw .xf-v b{margin-right:8px;font-weight:500;color:rgba(0,0,0,.9)}
.xf-dw .xf-l{margin:0;padding:0;list-style:none;display:grid;gap:6px;font-size:12px;line-height:20px;color:rgba(0,0,0,.7)}
.xf-dw .xf-l li{position:relative;padding-left:22px}
.xf-dw .xf-l li::before{position:absolute;left:0;top:2px;width:16px;height:16px;border-radius:50%;font-size:11px;line-height:16px;text-align:center}
.xf-dw .xf-l li.y::before{content:"✓";background:#e8ffea;color:#00b42a}
.xf-dw .xf-l li.n::before{content:"×";background:#f2f3f5;color:rgba(0,0,0,.45)}
.xf-dw .xf-ts{display:grid;gap:8px}
.xf-dw .xf-t{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 12px;border:1px solid #e5e6eb}
.xf-dw .xf-t span{display:grid;gap:2px}
.xf-dw .xf-t b{font-weight:500;font-size:12px;color:rgba(0,0,0,.9)}
.xf-dw .xf-t em{font-style:normal;font-size:12px;color:rgba(0,0,0,.5)}
.xf-dw .xf-w{font-size:12px;color:#d25f00;white-space:nowrap}
.xf-dw .kc-btn.dis{opacity:.45;cursor:not-allowed}''','xf27css')
wr(n,s)

# ---------- H. sidebar 告警中心 count 6 -> 7 (new weak-password alert)
for f in sorted(glob.glob(DST+'/*.dc.html')):
    n=os.path.basename(f); s=rd(n)
    if 'L("告警中心", \'bell\', \'6\')' in s:
        wr(n,s.replace('L("告警中心", \'bell\', \'6\')','L("告警中心", \'bell\', \'7\')'))
print('ok2')

# ---------- I. SecRunSet: 高危命令 row = 敬请期待
n='SecRunSet.dc.html'; s,d,i,j=load(DST+'/'+n)
for t in d['tabs']:
    for r in t['rows']:
        if r.get('id')=='i1' and r.get('n')=='高危命令': r.update({'soon':True,'cnt':'—','wln':'—'})
d['help'].append('高危命令本期上线显示「敬请期待」，下一阶段开放；其他检测项照常生效。')
save(DST+'/'+n,s,d,i,j)
s=rd(n)
s=rep(s,"t.rows.map((r) => Object.assign({}, r, { det: !cfg.on","t.rows.map((r) => r.soon ? Object.assign({}, r, { det: '敬请期待', auto: '—' }) : Object.assign({}, r, { det: !cfg.on",name='rs')
wr(n,s)
print('ok3')

# ---------- J. (PR #38 review) NetGuard out rows follow mode; Events ignore keeps who/when
n='SecNetGuard.dc.html'; s=rd(n)
s=rep(s,"      : t.k === 'items' ? t.rows.map(","      : t.k === 'out' ? (() => { const bm = cfg.mode === '自定义' ? cfg.base : cfg.mode; return t.rows.map((r) => r.id === 'o2' ? Object.assign({}, r, { act: bm === '轻量模式' ? '告警' : '阻断', sc: '跟随防护模式（' + bm + '）' }) : r.id === 'o7' ? Object.assign({}, r, { sc: bm === '重保模式' ? '全部主机（重保生效中）' : '仅重保模式（未生效）' }) : r); })()\n      : t.k === 'items' ? t.rows.map(",name='j1')
wr(n,s)
n='SecEvents.dc.html'; s=rd(n)
s=rep(s,"""    const saveS = (id, v) => { try { const c = JSON.parse(localStorage.getItem('dxEvS') || '{}'); c[id] = v; localStorage.setItem('dxEvS', JSON.stringify(c)); } catch (x) {} };""",
"""    const saveS = (id, v) => { try { const c = JSON.parse(localStorage.getItem('dxEvS') || '{}'); c[id] = v; localStorage.setItem('dxEvS', JSON.stringify(c)); const g = JSON.parse(localStorage.getItem('dxEvIgn') || '{}'); if (v === '已忽略') { const t = new Date(), p = (k) => String(k).padStart(2, '0'); g[id] = '误报，当前账号 ' + p(t.getMonth() + 1) + '-' + p(t.getDate()) + ' ' + p(t.getHours()) + ':' + p(t.getMinutes()) + ' 忽略（已写入操作日志）'; } else delete g[id]; localStorage.setItem('dxEvIgn', JSON.stringify(g)); } catch (x) {} };
    const IGN = (() => { try { return JSON.parse(localStorage.getItem('dxEvIgn') || '{}'); } catch (x) { return {}; } })();""",name='j2')
s=rep(s,"    const R = D.EV.map((x) => Object.assign({}, x, { st: ss[x.id] || x.st, ","    const R = D.EV.map((x) => Object.assign({}, x, { st: ss[x.id] || x.st, ign: (ss[x.id] || x.st) === '已忽略' ? (IGN[x.id] || x.ign) : x.ign, ",name='j3')
wr(n,s)
print('ok4')
