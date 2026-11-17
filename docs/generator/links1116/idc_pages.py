# -*- coding: utf-8 -*-
"""2026-11-16 补齐服务器控制台缺页：监控报表 IdcMonitor、操作记录 IdcLogs。
以 IdcServers.dc.html 为外壳（顶栏、侧栏、运行时不变），替换 <main> 和 _rv() 数据部分；
同时把 3 个现有服务器页侧栏的「监控报表」「操作记录」接上真实页面。可重复运行。
用法：python3 idc_pages.py <repo>/console
"""
import re, sys, os
D = sys.argv[1] if len(sys.argv) > 1 else 'console'
SHELL = open(os.path.join(D, 'IdcServers.dc.html'), encoding='utf-8').read()
PAGES = "{ '服务器列表': 'IdcServers.dc.html', '防护设置': 'IdcProtect.dc.html', '安全组': 'IdcSecGroup.dc.html', '监控报表': 'IdcMonitor.dc.html', '操作记录': 'IdcLogs.dc.html' }"
NAV = """const nav = [
      { label: '工作区', items: [L("服务器列表", 'box')] },
      { label: '网络与安全', items: [L("防护设置", 'shield'), L("安全组", 'lock')] },
      { label: '运维', items: [L("监控报表", 'chart'), L("操作记录", 'doc')] }
    ];"""
NAVPAT = re.compile(r"const nav = \[\s*\{ label: '工作区', items: \[L\(\"服务器(?:列表)?\", 'box'\).*?\];", re.S)
CHEV = '<svg class="rx" width="12" height="12" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M11.9999 13.1714L16.9497 8.22168L18.3639 9.63589L11.9999 15.9999L5.63599 9.63589L7.0502 8.22168L11.9999 13.1714Z"></path></svg>'

def dd(i, label=None, cls='kc-dd', up=False):
    lab = '<span>%s</span>' % label if label else ''
    return ('<span class="{{ddC%d}}"><button data-dd="%d" class="%s" type="button" aria-haspopup="listbox" onClick="{{ddT%d}}">%s<b>{{ddV%d}}</b>%s</button>'
            '<sc-if value="{{ddO%d}}" hint-placeholder-val="{{false}}"><span class="dd-m" onClick="{{ddX}}"></span><span class="dd-p%s" role="listbox"><sc-for list="{{ddL%d}}" as="o" hint-placeholder-count="4"><button type="button" role="option" class="{{o.cls}}" onClick="{{o.go}}">{{o.t}}</button></sc-for></span></sc-if></span>') % (i, i, cls, i, lab, i, CHEV, i, ' up' if up else '', i)

FOOT = SHELL[SHELL.find('<div class="kc-foot lf-foot">'):]
FOOT = FOOT[:FOOT.find('</section>')]

# ---------- 监控报表 ----------
MON_CSS = '''
.mo-ch{display:flex;align-items:flex-end;gap:3px;height:150px;padding-top:8px}
.mo-ch i{flex:1;background:#bedaff;min-width:3px}
.mo-ch i.hi{background:#165dff}
.mo-ch i.w{background:#ff9a2e}
.mo-ln{display:flex;gap:16px;font-size:12px;color:rgba(0,0,0,.6);margin-top:8px}
.mo-ln b{font-weight:400;color:rgba(0,0,0,.9)}
.mo-tr{display:inline-block;width:64px;height:6px;background:#f2f3f5;vertical-align:middle;margin-right:8px}
.mo-tr i{display:block;height:6px;background:#165dff}
.mo-tr i.o{background:#ff7d00}
.mo-tr i.r{background:#f53f3f}
.kc .kc-kpi b{font-size:24px;line-height:32px;font-weight:600;font-family:Barlow,Inter,sans-serif}
.kc .kc-kpi b span{font-size:inherit;color:inherit}
.kc .kc-kpi b i,.kc .kc-kpi b i span{font-size:13px!important;font-weight:400;font-style:normal;color:rgba(0,0,0,.5)}
.mo-sel{display:flex;align-items:center;gap:8px;margin:20px 0 4px;font-size:12px;color:rgba(0,0,0,.7)}
'''
MON_MAIN = '''<main data-pg="IdcMonitor" class="kc-main">
      <div class="mo-sel"><span>服务器</span>''' + dd(0) + '''</div>
      <div class="kc-hd">
        <div class="kc-hdl"><div><h1 class="kc-h1">监控报表</h1><p class="kc-desc">服务器的 CPU、内存、带宽和攻击情况。单台服务器的详细曲线也可以在服务器详情的「监控与报表」里看。</p></div></div>
        <div class="kc-btns">''' + dd(1, '时间') + '''<button type="button" class="kc-btn" onClick="{{exp}}">导出报表</button></div>
      </div>
      <sc-if value="{{expOn}}" hint-placeholder-val="{{false}}"><div class="ac-al i"><i>✓</i><span><b>报表已生成</b>{{expT}}，已开始下载（示例）。</span><a class="s1-x" href="#" onClick="{{expX}}">知道了</a></div></sc-if>
      <div class="kc-kpis"><sc-for list="{{kpis}}" as="k" hint-placeholder-count="4"><div class="kc-card kc-kpi"><span>{{k.n}}</span><b>{{k.v}} <i>{{k.u}}</i></b><i>{{k.s}}</i></div></sc-for></div>
      <sc-if value="{{warnOn}}" hint-placeholder-val="{{true}}"><div class="kc-alert"><span class="kc-tag warn">接近上限</span><span>{{warnT}}</span><a href="BillConfirm.dc.html" style="margin-left:auto">升级带宽</a></div></sc-if>
      <div class="kc-g2">
        <section class="kc-card">
          <div class="kc-ch"><h2>{{c1T}}</h2><div class="kc-sg" role="group" aria-label="指标"><sc-for list="{{m1}}" as="m" hint-placeholder-count="2"><button class="{{m.cls}}" type="button" onClick="{{m.go}}">{{m.n}}</button></sc-for></div></div>
          <div class="kc-cb"><div class="mo-ch"><sc-for list="{{bars1}}" as="b" hint-placeholder-count="24"><i class="{{b.c}}" style="{{b.h}}" title="{{b.t}}"></i></sc-for></div><div class="kc-axis"><sc-for list="{{ax}}" as="a" hint-placeholder-count="5"><span>{{a}}</span></sc-for></div><div class="mo-ln"><span>平均 <b>{{c1Avg}}</b></span><span>峰值 <b>{{c1Max}}</b></span></div></div>
        </section>
        <section class="kc-card">
          <div class="kc-ch"><h2>{{c2T}}</h2><div class="kc-sg" role="group" aria-label="方向"><sc-for list="{{m2}}" as="m" hint-placeholder-count="2"><button class="{{m.cls}}" type="button" onClick="{{m.go}}">{{m.n}}</button></sc-for></div></div>
          <div class="kc-cb"><div class="mo-ch"><sc-for list="{{bars2}}" as="b" hint-placeholder-count="24"><i class="{{b.c}}" style="{{b.h}}" title="{{b.t}}"></i></sc-for></div><div class="kc-axis"><sc-for list="{{ax}}" as="a" hint-placeholder-count="5"><span>{{a}}</span></sc-for></div><div class="mo-ln"><span>平均 <b>{{c2Avg}}</b></span><span>峰值 <b>{{c2Max}}</b></span><span>套餐 <b>{{c2Cap}}</b></span></div></div>
        </section>
      </div>
      <section class="kc-card">
        <div class="kc-ch"><h2>各服务器资源使用</h2><span class="kc-sub">{{rng}} · 示例数据</span></div>
        <div class="kc-tw"><table class="kc-t op-fix">
          <thead><tr><th>服务器</th><th>CPU 平均 / 峰值</th><th>内存</th><th>出带宽峰值</th><th>今日攻击</th><th>状态</th><th>操作</th></tr></thead>
          <tbody><sc-for list="{{rows}}" as="r" hint-placeholder-count="5"><tr class="{{r.rc}}">
            <td><a href="IdcServerDetail.dc.html">{{r.n}}</a><div class="kc-sub">{{r.ip}}</div></td>
            <td><span class="mo-tr"><i class="{{r.cc}}" style="{{r.cw}}"></i></span>{{r.cpu}}</td>
            <td><span class="mo-tr"><i class="{{r.mc}}" style="{{r.mw}}"></i></span>{{r.mem}}</td>
            <td>{{r.bw}}<div class="kc-sub">套餐 {{r.cap}}</div></td>
            <td>{{r.atk}}<div class="kc-sub">{{r.atkS}}</div></td>
            <td><span class="{{r.tc}}">{{r.st}}</span></td>
            <td><a href="#" onClick="{{r.pick}}">看曲线</a><a href="IdcServerDetail.dc.html?tab=mon">详情</a></td>
          </tr></sc-for></tbody>
        </table></div>
      </section>
    </main>'''
MON_JS = r'''
    const SV = [['全部服务器（9 台）', '', 'all'], ['web-prod-01', '115.231.**.12', 'web-prod-01'], ['db-01', '115.231.**.13', 'db-01'], ['backup-02', '60.191.**.40', 'backup-02'], ['web-new-03', '115.231.**.21', 'web-new-03'], ['web-new-04', '115.231.**.22', 'web-new-04'], ['web-new-05', '115.231.**.25', 'web-new-05'], ['web-old-01', '115.231.**.30', 'web-old-01'], ['ecs-app-01', '47.98.**.61', 'ecs-app-01'], ['bm-db-01', '115.231.**.40', 'bm-db-01']];
    const TM = ['近 24 小时', '近 7 天', '近 30 天'];
    const s0 = st.ddv0 || SV[0][0]; const t0 = st.ddv1 || TM[0];
    const D = { 'web-prod-01': [23, 61, 41, 100, 8, 3, '运行中'], 'db-01': [41, 78, 12, 50, 52, 0, '运行中'], 'backup-02': [8, 22, 2, 20, 6, 0, '运行中'], 'web-new-03': [3, 9, 1, 50, 2, 0, '运行中'], 'web-new-04': [2, 7, 1, 50, 1, 0, '运行中'], 'web-new-05': [1, 5, 0, 50, 1, 0, '运行中'], 'web-old-01': [0, 0, 0, 20, 0, 0, '已停机'], 'ecs-app-01': [17, 44, 4, 10, 6, 0, '运行中'], 'bm-db-01': [36, 71, 28, 100, 40, 1, '运行中'] };
    const memU = { 'web-prod-01': [64, 38], 'db-01': [128, 101], 'backup-02': [32, 9], 'web-new-03': [64, 6], 'web-new-04': [64, 5], 'web-new-05': [64, 4], 'web-old-01': [32, 0], 'ecs-app-01': [8, 5], 'bm-db-01': [256, 141] };
    const one = s0.indexOf('全部') < 0 ? s0 : '';
    const pick = one ? [one] : Object.keys(D);
    const seed = (s) => { let h = 7; for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) % 9973; return h; };
    const N = t0 === '近 24 小时' ? 24 : t0 === '近 7 天' ? 28 : 30;
    const ax = t0 === '近 24 小时' ? ['00:00', '06:00', '12:00', '18:00', '23:00'] : t0 === '近 7 天' ? ['11-10', '11-12', '11-14', '11-16'] : ['10-18', '10-25', '11-01', '11-08', '11-16'];
    const wave = (base, peak, k, sd) => Array.from({ length: N }, (_, i) => { const d = Math.sin((i / N) * Math.PI * 2 - 1.8) * 0.5 + 0.5; const n = ((sd * (i + 3) * 17) % 23) / 23; return Math.max(0, Math.round(base * (0.55 + d * 0.7) + n * base * 0.25 + (i === k ? peak - base : 0))); });
    const agg = (f) => { const arrs = pick.map((n) => f(n)); return Array.from({ length: N }, (_, i) => arrs.reduce((a, x) => a + x[i], 0) / (one ? 1 : arrs.length)); };
    const m1k = st.m1 || 'cpu'; const m2k = st.m2 || 'out';
    const cpuS = agg((n) => wave(D[n][0], D[n][1], Math.floor(N * 0.72), seed(n)));
    const memS = agg((n) => wave(memU[n][1] / memU[n][0] * 100, memU[n][1] / memU[n][0] * 100 + 6, Math.floor(N * 0.4), seed(n) + 3));
    const s1v = m1k === 'cpu' ? cpuS : memS;
    const capBw = pick.reduce((a, n) => a + D[n][3], 0);
    const outS = agg((n) => wave(D[n][2], Math.round(D[n][3] * (n === 'web-prod-01' ? 0.92 : 0.6)), Math.floor(N * 0.72), seed(n) + 5)).map((v) => v * (one ? 1 : pick.length));
    const inS = outS.map((v, i) => Math.round(v * 0.35 + ((i * 7) % 5)));
    const s2v = m2k === 'out' ? outS : inS;
    const BARS = (a, cap, unit, warnAt) => { const mx = Math.max(Math.max(...a) * 1.25, 1); return a.map((v, i) => ({ h: 'height:' + Math.max(2, Math.round(v / mx * 100)) + '%', c: warnAt && v >= warnAt ? 'w' : v === Math.max(...a) ? 'hi' : '', t: Math.round(v) + unit })); };
    const avg = (a) => a.reduce((x, y) => x + y, 0) / a.length;
    const all = Object.keys(D).map((n) => { const [c, cm, bw, cap, ab, atk, s] = D[n]; const [mt, mu] = memU[n]; const mp = Math.round(mu / mt * 100); const bp = Math.round(cap * (n === 'web-prod-01' ? 0.92 : 0.6) * (s === '运行中' ? 1 : 0));
      return { n, ip: (SV.find((x) => x[0] === n) || [])[1], cpu: s === '运行中' ? c + '% / ' + cm + '%' : '—', cw: 'width:' + cm + '%', cc: cm >= 80 ? 'r' : cm >= 60 ? 'o' : '', mem: s === '运行中' ? mu + ' / ' + mt + ' GB' : '—', mw: 'width:' + mp + '%', mc: mp >= 80 ? 'o' : '', bw: s === '运行中' ? bp + ' Mbps' : '—', cap: cap + 'M', atk: atk ? atk + ' 次' : '无', atkS: atk ? '已全部拦截' : '', st: n === 'web-prod-01' ? '带宽偏高' : s, tc: n === 'web-prod-01' ? 'kc-tag warn' : s === '运行中' ? 'kc-tag ok' : 'kc-tag mut', rc: one === n ? 'on' : '', pick: (e) => { ev(e); this.setState({ ddv0: n }); try { window.scrollTo({ top: 0, behavior: 'smooth' }); } catch (x) {} } }; });
    const rows = one ? all.filter((r) => r.n === one).concat(all.filter((r) => r.n !== one)) : all;
    const isOff = one === 'web-old-01';
    const sum = pick.reduce((a, n) => a + D[n][5], 0);
    const kpis = [
      { n: one ? 'CPU · 当前' : 'CPU · 平均', v: isOff ? '—' : Math.round(avg(cpuS)), u: isOff ? '' : '%', s: '峰值 ' + Math.round(Math.max(...cpuS)) + '%' },
      { n: '内存 · 已用', v: isOff ? '—' : Math.round(avg(memS)), u: isOff ? '' : '%', s: one ? memU[one][1] + ' / ' + memU[one][0] + ' GB' : '共 ' + pick.reduce((a, n) => a + memU[n][0], 0) + ' GB' },
      { n: '出带宽 · 峰值', v: Math.round(Math.max(...outS)), u: 'Mbps', s: '套餐合计 ' + capBw + ' Mbps' },
      { n: '攻击 · ' + t0.replace('近 ', ''), v: sum, u: '次', s: sum ? '全部已拦截 · 峰值 12 Gbps' : '未发现攻击' }];
    const warn = !one || one === 'web-prod-01';
    const M = (defs, key, cur) => defs.map(([k, n]) => ({ n, cls: k === cur ? 'on' : '', go: () => this.setState({ [key]: k }) }));
    const __R = { nav, kpis, rows, ax, rng: t0,
      warnOn: warn, warnT: 'web-prod-01 出带宽峰值 92 Mbps，已到套餐 100M 的 92%。持续超过后会丢包，建议升级带宽或开启 SCDN 分担。',
      c1T: (m1k === 'cpu' ? 'CPU 使用率' : '内存使用率') + (one ? ' · ' + one : ' · 平均'), m1: M([['cpu', 'CPU'], ['mem', '内存']], 'm1', m1k), bars1: BARS(s1v, 100, '%'), c1Avg: Math.round(avg(s1v)) + '%', c1Max: Math.round(Math.max(...s1v)) + '%',
      c2T: (m2k === 'out' ? '出带宽' : '入带宽') + (one ? ' · ' + one : ' · 合计'), m2: M([['out', '出方向'], ['in', '入方向']], 'm2', m2k), bars2: BARS(s2v, capBw, ' Mbps', m2k === 'out' && one === 'web-prod-01' ? 85 : 0), c2Avg: Math.round(avg(s2v)) + ' Mbps', c2Max: Math.round(Math.max(...s2v)) + ' Mbps', c2Cap: capBw + ' Mbps',
      exp: () => this.setState({ exp: 1 }), expOn: !!st.exp, expT: (one || '全部服务器') + ' · ' + t0, expX: (e) => { ev(e); this.setState({ exp: 0 }); } };
    const DDS = [[SV[0][0], SV.map((x) => x[0])], [TM[0], TM]];
'''

# ---------- 操作记录 ----------
LOG_CSS = '''
.lg-dw-m{position:fixed;inset:0;background:rgba(0,0,0,.35);z-index:1000}
.lg-steps{list-style:none;margin:0;padding:0}
.lg-steps li{position:relative;padding:0 0 16px 20px;font-size:12px;color:rgba(0,0,0,.7)}
.lg-steps li:before{content:"";position:absolute;left:3px;top:5px;width:7px;height:7px;background:#165dff}
.lg-steps li.err:before{background:#f53f3f}
.lg-steps li:after{content:"";position:absolute;left:6px;top:14px;bottom:0;width:1px;background:#e6e9ef}
.lg-steps li:last-child:after{display:none}
.lg-steps b{display:block;font-weight:500;color:rgba(0,0,0,.9);margin-bottom:2px}
.lg-h{font-size:13px;font-weight:500;margin:20px 0 10px}
.kc-t td .lg-src{font-size:12px;color:rgba(0,0,0,.5)}
'''
LOG_MAIN = '''<main data-pg="IdcLogs" class="kc-main">
      <div class="kc-hd">
        <div class="kc-hdl"><div><h1 class="kc-h1">操作记录</h1><p class="kc-desc">所有服务器的开关机、重启、重装系统、改密码、续费和到期停机记录，保留 180 天。</p></div></div>
        <div class="kc-btns"><button type="button" class="kc-btn" onClick="{{exp}}">导出</button></div>
      </div>
      <sc-if value="{{expOn}}" hint-placeholder-val="{{false}}"><div class="ac-al i"><i>✓</i><span><b>已导出 {{total}} 条记录</b>CSV 文件已开始下载（示例）。</span><a class="s1-x" href="#" onClick="{{expX}}">知道了</a></div></sc-if>
      <section class="kc-card">
        <div class="kc-tabs" role="tablist"><sc-for list="{{tabs}}" as="t" hint-placeholder-count="4"><button class="{{t.cls}}" type="button" role="tab" aria-selected="{{t.on}}" onClick="{{t.pick}}">{{t.n}} <span class="{{t.cc}}">{{t.c}}</span></button></sc-for></div>
        <div class="kc-bar lf-bar lf-s"><div class="lf-q"><input class="kc-in" style="width:300px" type="search" aria-label="搜索服务器名称、IP 或操作人" placeholder="搜索服务器名称、IP 或操作人" value="{{q}}" onChange="{{onQ}}"></div>''' + dd(0, '服务器') + dd(1, '操作类型') + dd(2, '时间') + '''</div>
        <div class="kc-tw"><table class="kc-t op-fix">
          <thead><tr><th>时间</th><th>服务器</th><th>操作</th><th>操作人</th><th>结果</th><th>操作</th></tr></thead>
          <tbody><sc-for list="{{rows}}" as="r" hint-placeholder-count="6"><tr>
            <td>{{r.tm}}</td>
            <td><a href="IdcServerDetail.dc.html">{{r.sv}}</a><div class="kc-sub">{{r.ip}}</div></td>
            <td>{{r.op}}<div class="kc-sub">{{r.d}}</div></td>
            <td>{{r.who}}<div class="kc-sub">{{r.src}}</div></td>
            <td><span class="{{r.tc}}">{{r.rs}}</span></td>
            <td><a href="#" onClick="{{r.open}}">详情</a></td>
          </tr></sc-for></tbody>
        </table></div>
        <sc-if value="{{none}}" hint-placeholder-val="{{false}}"><div class="kc-empty" style="padding:48px 0;text-align:center;color:rgba(0,0,0,.5);font-size:12px">没有符合条件的记录 · <a href="#" onClick="{{reset}}">清空筛选</a></div></sc-if>
        ''' + re.sub(r'<div class="kc-pg">.*?</div>', '<div class="kc-pg"><button type="button" aria-label="上一页" onClick="{{prev}}">‹</button><sc-for list="{{pages}}" as="p" hint-placeholder-count="2"><button type="button" class="{{p.cls}}" onClick="{{p.go}}">{{p.n}}</button></sc-for><button type="button" aria-label="下一页" onClick="{{next}}">›</button></div>', FOOT, count=1, flags=re.S).replace('{{ddC1}}', '{{ddC3}}').replace('{{ddT1}}', '{{ddT3}}').replace('{{ddV1}}', '{{ddV3}}').replace('{{ddO1}}', '{{ddO3}}').replace('{{ddL1}}', '{{ddL3}}').replace('data-dd="1"', 'data-dd="3"') + '''
      </section>
      <sc-if value="{{dwOn}}" hint-placeholder-val="{{false}}"><div class="lg-dw-m" onClick="{{dwX}}"></div><aside class="kc-dw" role="dialog" aria-modal="true" aria-label="操作详情">
        <div class="kc-dwh">操作详情<button type="button" class="kc-btn sm" aria-label="关闭" onClick="{{dwX}}">×</button></div>
        <div class="kc-dwb">
          <div class="kc-kv"><span>操作</span><b>{{dw.op}}</b><span>服务器</span><span>{{dw.sv}} · {{dw.ip}}</span><span>操作人</span><span>{{dw.who}}（{{dw.src}}）</span><span>登录 IP</span><span>{{dw.lip}}</span><span>开始时间</span><span>{{dw.tm}}</span><span>结果</span><span><span class="{{dw.tc}}">{{dw.rs}}</span></span><span>请求 ID</span><span>{{dw.rid}}</span></div>
          <div class="lg-h">执行过程</div>
          <ol class="lg-steps"><sc-for list="{{dw.steps}}" as="s" hint-placeholder-count="3"><li class="{{s.c}}"><b>{{s.n}}</b>{{s.t}}</li></sc-for></ol>
          <sc-if value="{{dw.fail}}" hint-placeholder-val="{{false}}"><div class="kc-alert"><span class="kc-tag err">失败原因</span><span>{{dw.why}}</span></div></sc-if>
        </div>
        <div class="kc-dwf"><sc-if value="{{dw.fail}}" hint-placeholder-val="{{false}}"><a class="kc-btn" href="SupTicketNew.dc.html">提交工单</a></sc-if><a class="kc-btn" href="IdcServerDetail.dc.html">查看服务器</a><button type="button" class="kc-btn pri" onClick="{{dwX}}">关闭</button></div>
      </aside></sc-if>
    </main>'''
LOG_JS = r'''
    const IP = { 'web-prod-01': '115.231.**.12', 'db-01': '115.231.**.13', 'backup-02': '60.191.**.40', 'web-new-03': '115.231.**.21', 'web-new-04': '115.231.**.22', 'web-new-05': '115.231.**.25', 'web-old-01': '115.231.**.30', 'ecs-app-01': '47.98.**.61', 'bm-db-01': '115.231.**.40' };
    const LG = [
      ['11-16 10:12', 'web-prod-01', '重启', '正常重启', 'wangqi', '控制台', 'ok', '0'],
      ['11-16 09:40', 'web-new-05', '安装客户端', '德迅安全卫士 V4.3.2 自动安装', '系统', '交付任务', 'ok', '0'],
      ['11-15 22:05', 'db-01', '修改密码', 'root 密码', '张三', '控制台', 'ok', '0'],
      ['11-15 17:31', 'web-new-04', '安装客户端', '连不上安装源，已自动重试 3 次', '系统', '交付任务', 'err', '0'],
      ['11-15 14:20', 'web-prod-01', '重装系统', 'CentOS 7.9 → CentOS 7.9，保留数据盘', 'wangqi', '控制台', 'ok', '1'],
      ['11-14 03:00', 'backup-02', '关机', '计划任务：每周日 03:00 维护', '李四', 'API', 'ok', '0'],
      ['11-14 03:12', 'backup-02', '开机', '计划任务结束', '李四', 'API', 'ok', '0'],
      ['11-12 16:48', 'web-prod-01', '续费', '续费 1 个月，到期 2026-11-20 → 2026-12-20', 'wangqi', '控制台', 'ing', '0'],
      ['11-10 11:02', 'web-new-03', '重装系统', 'Ubuntu 22.04 → CentOS 7.9', '王五', '控制台', 'err', '2'],
      ['11-05 00:00', 'web-old-01', '到期停机', '已到期，自动停机，数据保留 7 天', '系统', '到期处理', 'warn', '0'],
      ['11-01 15:30', 'web-new-04', '服务器交付', 'Ubuntu 22.04 · 温州电信 A 机房', '系统', '交付任务', 'ok', '0'],
      ['11-13 20:30', 'ecs-app-01', '升级配置', '2 核 4G → 4 核 8G，重启后生效', 'wangqi', '控制台', 'ok', '0'],
      ['11-08 10:00', 'bm-db-01', '服务器交付', 'Rocky Linux 9 · 温州电信 A 机房', '系统', '交付任务', 'ok', '0'],
      ['10-30 09:18', 'db-01', '重启', '强制重启（系统无响应）', '张三', '控制台', 'ok', '0']];
    const RS = { ok: ['成功', 'kc-tag ok'], err: ['失败', 'kc-tag err'], ing: ['付款核验中', 'kc-tag info'], warn: ['已执行', 'kc-tag warn'] };
    const TY = ['全部', '开关机与重启', '重装系统', '修改密码', '续费与到期', '安全客户端'];
    const tyOf = (op) => /开机|关机|重启/.test(op) ? '开关机与重启' : op === '重装系统' ? '重装系统' : op === '修改密码' ? '修改密码' : /续费|到期|交付|升级/.test(op) ? '续费与到期' : '安全客户端';
    const SVS = ['全部'].concat(Object.keys(IP)); const TMS = ['近 7 天', '近 30 天', '近 180 天'];
    const fs = st.ddv0 || '全部', ft = st.ddv1 || '全部', fm = st.ddv2 || '近 30 天', qq = (st.q || '').trim();
    const tab = st.lt || '全部';
    const STEPS = (r) => r[2] === '重装系统' ? (r[6] === 'err' ? [['', '提交重装', r[0] + ' · ' + r[3]], ['', '关机并挂载镜像', '用时 1 分 20 秒'], ['err', '写入系统盘失败', '镜像校验不通过，已自动回滚到原系统，数据未受影响']] : [['', '提交重装', r[0]], ['', '关机并挂载镜像', '用时 1 分 05 秒'], ['', '写入系统盘', '用时 6 分 40 秒'], ['', '首次开机并初始化', '已重新安装德迅安全卫士客户端']])
      : r[2] === '安装客户端' ? (r[6] === 'err' ? [['', '开始安装', r[0]], ['err', '下载安装包', '连不上 agent.dexunyun.com:443，常见原因是出方向 443 被拦'], ['err', '自动重试 3 次', '15:31、15:36、15:51 均失败']] : [['', '开始安装', r[0]], ['', '下载并安装', 'V4.3.2，用时 48 秒'], ['', '首次检测', '已开始，约 10 分钟']])
      : r[2] === '续费' ? [['', '提交续费订单', 'DX20261112007 · ¥399.00'], ['', '对公转账', '已上传回单'], ['', '付款核验', '1–2 个工作日，核验通过后到期时间自动顺延']]
      : [['', '提交', r[0]], ['', '执行', r[3]], ['', '完成', RS[r[6]][0]]];
    let all = LG.map((r, i) => ({ tm: r[0], sv: r[1], ip: IP[r[1]], op: r[2], d: r[3], who: r[4], src: r[5], rs: RS[r[6]][0], tc: RS[r[6]][1], k: (r[5] === '控制台' || r[5] === 'API' ? 'me' : 'sys') + (r[6] === 'err' ? ' err' : ''), ty: tyOf(r[2]), i, raw: r,
      open: (e) => { ev(e); this.setState({ dw: i }); } }));
    all = all.filter((r) => (fs === '全部' || r.sv === fs) && (ft === '全部' || r.ty === ft) && (fm !== '近 7 天' || r.tm >= '11-10') && (!qq || (r.sv + r.ip + r.who + r.op).indexOf(qq) >= 0));
    const TD = [['全部', ''], ['人工操作', 'me'], ['系统任务', 'sys'], ['失败', 'err']];
    const tabs = TD.map(([n, k]) => { const c = all.filter((r) => !k || r.k.indexOf(k) >= 0).length; return { n, c, on: n === tab, cls: n === tab ? 'kc-tab on' : 'kc-tab', cc: k === 'err' && c ? 'kc-cnt r' : 'kc-cnt', pick: () => this.setState({ lt: n, pg: 1 }) }; });
    const kk = (TD.find((d) => d[0] === tab) || TD[0])[1];
    const rows0 = all.filter((r) => !kk || r.k.indexOf(kk) >= 0); const psz = parseInt(st.ddv3 || '10', 10); const pgN = Math.max(1, Math.ceil(rows0.length / psz)); const pg = Math.min(st.pg || 1, pgN); const rows = rows0.slice((pg - 1) * psz, pg * psz);
    const pgs = Array.from({ length: pgN }, (_, i) => ({ n: i + 1, cls: i + 1 === pg ? 'on' : '', go: () => this.setState({ pg: i + 1 }) }));
    const dwi = st.dw === undefined || st.dw === null ? -1 : st.dw; const dr = dwi >= 0 ? LG[dwi] : null;
    const dw = dr ? { op: dr[2] + ' · ' + dr[3], sv: dr[1], ip: IP[dr[1]], who: dr[4], src: dr[5], lip: dr[5] === '控制台' ? '115.236.**.20（浙江 温州）' : dr[5] === 'API' ? '10.0.3.8（API 密钥 AK-****3f2a）' : '—', tm: '2026-' + dr[0] + ':06', rs: RS[dr[6]][0], tc: RS[dr[6]][1], rid: 'req-' + (91234 + dwi * 37).toString(16) + '-idc', steps: STEPS(dr).map(([c, n, t]) => ({ c, n, t })), fail: dr[6] === 'err', why: dr[2] === '重装系统' ? '镜像校验不通过，系统已回滚。可以换一个镜像重试，或提交工单让工程师处理。' : '服务器出方向 443 端口不通。检查安全组或防火墙放行后，在服务器详情「安全」里点「重试安装」。' } : {};
    const __R = { nav, tabs, rows, total: rows0.length, none: !rows0.length, pages: pgs, prev: () => this.setState({ pg: Math.max(1, pg - 1) }), next: () => this.setState({ pg: Math.min(pgN, pg + 1) }), q: st.q || '', onQ: (e) => this.setState({ q: e.target.value }),
      reset: (e) => { ev(e); this.setState({ q: '', ddv0: '全部', ddv1: '全部', ddv2: '近 30 天', lt: '全部' }); },
      dwOn: !!dr, dw, dwX: (e) => { ev(e); this.setState({ dw: -1 }); },
      exp: () => this.setState({ exp: 1 }), expOn: !!st.exp, expX: (e) => { ev(e); this.setState({ exp: 0 }); } };
    const DDS = [['全部', SVS], ['全部', TY], ['近 30 天', TMS], ['10 条/页', ['10 条/页', '20 条/页', '50 条/页', '100 条/页']]];
'''

DDJS = r'''
    const __s = this.state || {}; const __o = __s.ddo === undefined ? -1 : __s.ddo; const DDX = { ddX: () => this.setState({ ddo: -1 }) };
    DDS.forEach(([v0, opts], i) => { const v = __s['ddv' + i] || v0; const on = __o === i; DDX['ddV' + i] = v; DDX['ddO' + i] = on; DDX['ddC' + i] = on ? 'dd-w on' : 'dd-w';
      DDX['ddT' + i] = () => this.setState({ ddo: on ? -1 : i }); DDX['ddL' + i] = opts.map((t) => ({ t, cls: t === v ? 'on' : '', go: () => this.setState({ ['ddv' + i]: t, ddo: -1 }) })); });
    return Object.assign(__R, DDX);
  }
}
</script>
</body>
</html>'''


# ---------- 防护设置 ----------
PRO_CSS = MON_CSS + LOG_CSS + """
.pr-row{display:flex;align-items:center;justify-content:space-between;gap:24px;padding:14px 0;border-bottom:1px solid #f2f3f5}
.pr-row:last-child{border-bottom:0}
.pr-row .kc-sub{margin-top:2px}
.pr-add{display:flex;gap:8px;align-items:center;margin:0 0 12px}
.pr-add .kc-in{width:220px}
.kc .kc-sw{flex:none}
"""
PRO_MAIN = """<main data-pg="IdcProtect" class="kc-main">
      <div class="mo-sel"><span>服务器</span>""" + dd(0) + """</div>
      <div class="kc-hd">
        <div class="kc-hdl"><div><h1 class="kc-h1">防护设置</h1><p class="kc-desc">服务器的 DDoS 防护、CC 防护和 IP 黑白名单。改完立即生效，不需要重启服务器。</p></div></div>
        <div class="kc-btns"><a class="kc-btn" href="IdcLogs.dc.html">操作记录</a><a class="kc-btn pri" href="BillConfirm.dc.html">升级防护</a></div>
      </div>
      <sc-if value="{{tOn}}" hint-placeholder-val="{{false}}"><div class="ac-al i"><i>✓</i><span><b>{{tT}}</b>{{tD}}</span><a class="s1-x" href="#" onClick="{{tX}}">知道了</a></div></sc-if>
      <div class="kc-kpis"><sc-for list="{{kpis}}" as="k" hint-placeholder-count="4"><div class="kc-card kc-kpi"><span>{{k.n}}</span><b>{{k.v}} <i>{{k.u}}</i></b><i>{{k.s}}</i></div></sc-for></div>
      <div class="kc-g2">
        <section class="kc-card">
          <div class="kc-ch"><h2>DDoS 防护</h2><span class="kc-sub">{{line}}</span></div>
          <div class="kc-cb">
            <div class="pr-row"><div>防护等级<div class="kc-sub">{{lvD}}</div></div><div class="kc-sg" role="group" aria-label="防护等级"><sc-for list="{{lv}}" as="m" hint-placeholder-count="3"><button class="{{m.cls}}" type="button" onClick="{{m.go}}">{{m.n}}</button></sc-for></div></div>
            <sc-for list="{{sws}}" as="w" hint-placeholder-count="3"><div class="pr-row"><div>{{w.n}}<div class="kc-sub">{{w.d}}</div></div><button type="button" class="{{w.cls}}" role="switch" aria-checked="{{w.on}}" aria-label="{{w.n}}" onClick="{{w.go}}"></button></div></sc-for>
          </div>
        </section>
        <section class="kc-card">
          <div class="kc-ch"><h2>CC 防护</h2><span class="kc-sub">只对网站（HTTP / HTTPS）生效</span></div>
          <div class="kc-cb">
            <sc-for list="{{cc}}" as="w" hint-placeholder-count="2"><div class="pr-row"><div>{{w.n}}<div class="kc-sub">{{w.d}}</div></div><button type="button" class="{{w.cls}}" role="switch" aria-checked="{{w.on}}" aria-label="{{w.n}}" onClick="{{w.go}}"></button></div></sc-for>
            <div class="pr-row"><div>单 IP 访问频率上限<div class="kc-sub">超过后要求验证，验证不过再拦截</div></div><span>{{ccRate}}</span></div>
          </div>
        </section>
      </div>
      <section class="kc-card">
        <div class="kc-tabs" role="tablist"><sc-for list="{{tabs}}" as="t" hint-placeholder-count="2"><button class="{{t.cls}}" type="button" role="tab" aria-selected="{{t.on}}" onClick="{{t.pick}}">{{t.n}} <span class="kc-cnt">{{t.c}}</span></button></sc-for></div>
        <div class="kc-cb">
          <div class="pr-add"><input class="kc-in" aria-label="IP 或网段" placeholder="IP 或网段，例如 203.0.113.0/24" value="{{nIp}}" onChange="{{onIp}}"><input class="kc-in" aria-label="备注" placeholder="备注（选填）" value="{{nNote}}" onChange="{{onNote}}"><button type="button" class="{{addCls}}" onClick="{{add}}">添加到{{tabN}}</button><span class="kc-sub">{{tabD}}</span></div>
          <div class="kc-tw"><table class="kc-t op-fix">
            <thead><tr><th>IP / 网段</th><th>备注</th><th>添加人</th><th>添加时间</th><th>操作</th></tr></thead>
            <tbody><sc-for list="{{rows}}" as="r" hint-placeholder-count="3"><tr><td>{{r.ip}}</td><td>{{r.note}}</td><td>{{r.who}}</td><td>{{r.tm}}</td><td><a href="#" onClick="{{r.del}}">删除</a></td></tr></sc-for></tbody>
          </table></div>
          <sc-if value="{{none}}" hint-placeholder-val="{{false}}"><div style="padding:32px 0;text-align:center;color:rgba(0,0,0,.5);font-size:12px">还没有{{tabN}}</div></sc-if>
        </div>
      </section>
    </main>"""
PRO_JS = r"""
    const SV = [['web-prod-01', '高防服务器 · 200G 保底', 200, 12, 3, '高防'], ['db-01', '电信服务器 · 基础防护 10G', 10, 0, 0, '基础'], ['backup-02', 'BGP 服务器 · 基础防护 20G', 20, 0, 0, '基础'], ['ecs-app-01', '弹性云服务器 · 基础防护 5G', 5, 0, 0, '基础'], ['bm-db-01', '裸金属服务器 · 基础防护 10G', 10, 2.4, 1, '基础']];
    const sn = st.ddv0 || SV[0][0]; const S = SV.find((x) => x[0] === sn) || SV[0];
    const key = (k) => sn + ':' + k; const g = (k, d) => (st[key(k)] === undefined ? d : st[key(k)]);
    const T = (k, d, n, desc) => { const on = g(k, d); return { n, d: desc, on: on ? 'true' : 'false', cls: on ? 'kc-sw on' : 'kc-sw', go: () => this.setState({ [key(k)]: !on, tOn: 1, tT: n + (on ? '已关闭' : '已开启'), tD: '对 ' + sn + ' 立即生效，已记入操作记录。' }) }; };
    const lvK = g('lv', '正常');
    const LVD = { '宽松': '只拦截明显的攻击流量，误拦最少，适合业务刚接入时观察', '正常': '推荐。拦截攻击流量和异常连接，对正常访问基本无影响', '严格': '被持续攻击时使用。可能误拦少量正常访问，攻击结束后建议调回正常' };
    const lv = ['宽松', '正常', '严格'].map((n) => ({ n, cls: n === lvK ? 'on' : '', go: () => this.setState({ [key('lv')]: n, tOn: 1, tT: '防护等级已改为「' + n + '」', tD: '对 ' + sn + ' 立即生效。' }) }));
    const hi = S[5] === '高防';
    const sws = [T('el', false, '超出保底后弹性防护', hi ? '攻击超过 ' + S[2] + 'G 时自动扩到 300G，按实际峰值计费；关闭则超过后进入黑洞' : '基础防护不支持弹性，需要的话请升级为高防服务器'), T('sms', true, '攻击开始和结束时通知我', '短信 + 站内信，发给服务器负责人和主账号'), T('auto', true, '黑洞后自动解封', '黑洞 30 分钟后自动尝试解封，每天最多 3 次')];
    if (!hi) sws[0] = { n: sws[0].n, d: sws[0].d, on: 'false', cls: 'kc-sw dis', go: () => this.setState({ tOn: 1, tT: '基础防护不支持弹性防护', tD: '可以在「升级防护」里换成高防服务器。' }) };
    const cc = [T('cc', hi, 'CC 防护', '识别并拦截刷接口、刷页面的请求'), T('js', false, '可疑请求先做人机验证', '浏览器访问会看到一次验证，接口调用不受影响')];
    const BL0 = { 'web-prod-01': { b: [['45.134.**.12', '反弹 Shell 来源', '系统', '11-15 17:40'], ['103.97.**.0/24', '持续 CC 攻击', 'wangqi', '11-12 21:03']], w: [['115.236.**.20', '办公室出口', 'wangqi', '10-28 10:11']] } };
    const lists = st[key('bl')] || BL0[sn] || { b: [], w: [] };
    const tab = st.ptab || '黑名单'; const tk = tab === '黑名单' ? 'b' : 'w';
    const tabs = [['黑名单', 'b'], ['白名单', 'w']].map(([n, k]) => ({ n, c: lists[k].length, on: n === tab, cls: n === tab ? 'kc-tab on' : 'kc-tab', pick: () => this.setState({ ptab: n }) }));
    const nIp = st.nIp || '', nNote = st.nNote || ''; const ok = /^\d{1,3}(\.\d{1,3}|\.\*\*){3}(\/\d{1,2})?$/.test(nIp.trim());
    const rows = lists[tk].map((r, i) => ({ ip: r[0], note: r[1] || '—', who: r[2], tm: r[3], del: (e) => { ev(e); const nl = { b: lists.b.slice(), w: lists.w.slice() }; nl[tk].splice(i, 1); this.setState({ [key('bl')]: nl, tOn: 1, tT: '已从' + tab + '删除 ' + r[0], tD: '立即生效。' }); } }));
    const __R = { nav, kpis: [{ n: '保底防护', v: S[2], u: 'Gbps', s: hi ? '高防服务器 · 可弹性到 300G' : '基础防护' }, { n: '当前状态', v: S[3] ? '已清洗' : '正常', u: '', s: S[3] ? '最近一次 11-15 17:31，已结束' : '近 24 小时无攻击' }, { n: '近 7 天攻击', v: S[4], u: '次', s: S[4] ? '峰值 ' + S[3] + ' Gbps · 全部拦截' : '未发现攻击' }, { n: '黑洞', v: '未触发', u: '', s: '超过保底且未开弹性时触发' }],
      line: S[1], lv, lvD: LVD[lvK], sws, cc, ccRate: g('cc', hi) ? '每秒 60 次' : '未开启', tabs, rows, none: !rows.length, tabN: tab, tabD: tk === 'b' ? '这些 IP 的所有请求直接拦截' : '这些 IP 不做任何拦截，请只放自己的出口 IP',
      nIp, nNote, onIp: (e) => this.setState({ nIp: e.target.value }), onNote: (e) => this.setState({ nNote: e.target.value }), addCls: ok ? 'kc-btn pri' : 'kc-btn pri dis',
      add: () => { if (!ok) { this.setState({ tOn: 1, tT: '请输入正确的 IP 或网段', tD: '例如 203.0.113.12 或 203.0.113.0/24。' }); return; } const nl = { b: lists.b.slice(), w: lists.w.slice() }; nl[tk].unshift([nIp.trim(), nNote.trim(), 'wangqi', '刚刚']); this.setState({ [key('bl')]: nl, nIp: '', nNote: '', tOn: 1, tT: '已添加到' + tab + '：' + nIp.trim(), tD: '约 10 秒内生效。' }); },
      tOn: !!st.tOn, tT: st.tT || '', tD: st.tD || '', tX: (e) => { ev(e); this.setState({ tOn: 0 }); } };
    const DDS = [[SV[0][0], SV.map((x) => x[0])]];
"""

# ---------- 安全组 ----------
SG_CSS = LOG_CSS + """
.sg-add td .kc-in{width:100%;box-sizing:border-box}
.sg-pol{display:inline-flex;gap:0}
"""
SG_MAIN = """<main data-pg="IdcSecGroup" class="kc-main">
      <div class="kc-hd">
        <div class="kc-hdl"><div><h1 class="kc-h1">安全组</h1><p class="kc-desc">安全组是服务器的虚拟防火墙，按规则放行或拒绝进出服务器的流量。一台服务器可以关联多个安全组，规则修改后立即生效。</p></div></div>
        <div class="kc-btns"><button type="button" class="kc-btn pri" onClick="{{newSg}}">新建安全组</button></div>
      </div>
      <sc-if value="{{fixShow}}" hint-placeholder-val="{{true}}"><div class="{{fixCls}}"><i>{{fixI}}</i><span><b>{{fixT}}</b>{{fixD}}</span><sc-if value="{{fixIdle}}" hint-placeholder-val="{{true}}"><button type="button" class="kc-btn sm pri" onClick="{{fix}}">一键放行</button></sc-if></div></sc-if>
      <sc-if value="{{tOn}}" hint-placeholder-val="{{false}}"><div class="ac-al i"><i>✓</i><span><b>{{tT}}</b>{{tD}}</span><a class="s1-x" href="#" onClick="{{tX}}">知道了</a></div></sc-if>
      <section class="kc-card">
        <div class="kc-tw"><table class="kc-t op-fix">
          <thead><tr><th>安全组</th><th>关联服务器</th><th>入站规则</th><th>出站规则</th><th>说明</th><th>创建时间</th><th>操作</th></tr></thead>
          <tbody><sc-for list="{{groups}}" as="g" hint-placeholder-count="3"><tr>
            <td><a href="#" onClick="{{g.open}}">{{g.n}}</a><div class="kc-sub">{{g.id}}</div></td>
            <td>{{g.svs}}<div class="kc-sub">{{g.svN}}</div></td><td>{{g.inN}} 条</td><td>{{g.outN}} 条</td><td>{{g.d}}</td><td>{{g.tm}}</td>
            <td><a href="#" onClick="{{g.open}}">配置规则</a><a href="#" onClick="{{g.del}}">{{g.delT}}</a></td>
          </tr></sc-for></tbody>
        </table></div>
      </section>
      <sc-if value="{{dwOn}}" hint-placeholder-val="{{false}}"><div class="lg-dw-m" onClick="{{dwX}}"></div><aside class="kc-dw" role="dialog" aria-modal="true" aria-label="{{dwT}}" style="width:760px">
        <div class="kc-dwh">{{dwT}}<button type="button" class="kc-btn sm" aria-label="关闭" onClick="{{dwX}}">×</button></div>
        <div class="kc-dwb">
          <sc-if value="{{isNew}}" hint-placeholder-val="{{false}}"><div class="kc-kv"><span>名称</span><input class="kc-in" aria-label="安全组名称" value="{{nName}}" onChange="{{onName}}" placeholder="例如 sg-web"><span>模板</span><div class="kc-sg" role="group" aria-label="模板"><sc-for list="{{tpls}}" as="m" hint-placeholder-count="3"><button class="{{m.cls}}" type="button" onClick="{{m.go}}">{{m.n}}</button></sc-for></div><span></span><span class="kc-sub">{{tplD}}</span></div></sc-if>
          <div class="kc-tabs" role="tablist"><sc-for list="{{dirs}}" as="t" hint-placeholder-count="2"><button class="{{t.cls}}" type="button" role="tab" aria-selected="{{t.on}}" onClick="{{t.pick}}">{{t.n}} <span class="kc-cnt">{{t.c}}</span></button></sc-for></div>
          <div class="kc-tw" style="margin-top:12px"><table class="kc-t">
            <thead><tr><th>策略</th><th>协议端口</th><th>{{peer}}</th><th>备注</th><th>操作</th></tr></thead>
            <tbody><sc-for list="{{rules}}" as="r" hint-placeholder-count="3"><tr><td><span class="{{r.pc}}">{{r.p}}</span></td><td>{{r.port}}</td><td>{{r.src}}</td><td>{{r.note}}</td><td><a href="#" onClick="{{r.del}}">删除</a></td></tr></sc-for>
              <tr class="sg-add"><td><div class="kc-sg" role="group" aria-label="策略"><sc-for list="{{pols}}" as="m" hint-placeholder-count="2"><button class="{{m.cls}}" type="button" onClick="{{m.go}}">{{m.n}}</button></sc-for></div></td><td><input class="kc-in" aria-label="协议端口" placeholder="TCP:443" value="{{rPort}}" onChange="{{onPort}}"></td><td><input class="kc-in" aria-label="来源或目标" placeholder="0.0.0.0/0" value="{{rSrc}}" onChange="{{onSrc}}"></td><td><input class="kc-in" aria-label="备注" placeholder="选填" value="{{rNote}}" onChange="{{onNote}}"></td><td><a href="#" onClick="{{addRule}}">添加</a></td></tr>
            </tbody>
          </table></div>
          <p class="kc-sub" style="margin-top:12px">规则从上到下匹配，命中第一条即停止；新加的允许规则会放在「拒绝 ALL」兜底规则之前。没有命中任何规则时：入站默认拒绝，出站默认允许。</p>
        </div>
        <div class="kc-dwf"><button type="button" class="kc-btn" onClick="{{dwX}}">取消</button><button type="button" class="kc-btn pri" onClick="{{save}}">{{saveT}}</button></div>
      </aside></sc-if>
    </main>"""
SG_JS = r"""
    const G0 = [
      { n: 'sg-web', id: 'sg-3f2a91c0', svs: ['web-prod-01', 'web-new-03', 'web-new-05', 'ecs-app-01'], d: '网站服务器：放行 80 / 443 / 22', tm: '2026-08-12', in: [['允许', 'TCP:80,443', '0.0.0.0/0', '网站访问'], ['允许', 'TCP:22', '115.236.**.20/32', '办公室 SSH'], ['拒绝', 'ALL', '0.0.0.0/0', '其余全部拒绝']], out: [['允许', 'ALL', '0.0.0.0/0', '']] },
      { n: 'sg-db', id: 'sg-7c10de44', svs: ['db-01', 'bm-db-01'], d: '数据库：只放行内网 3306', tm: '2026-08-12', in: [['允许', 'TCP:3306', '10.0.0.0/16', '内网应用'], ['允许', 'TCP:22', '115.236.**.20/32', '办公室 SSH']], out: [['允许', 'ALL', '0.0.0.0/0', '']] },
      { n: 'sg-strict', id: 'sg-a90b2e17', svs: ['web-new-04'], d: '严格模式：出站只放行 DNS 和 80', tm: '2026-10-30', in: [['允许', 'TCP:22', '115.236.**.20/32', '办公室 SSH']], out: [['允许', 'UDP:53', '0.0.0.0/0', 'DNS'], ['允许', 'TCP:80', '0.0.0.0/0', ''], ['拒绝', 'ALL', '0.0.0.0/0', '']] },
      { n: 'default', id: 'sg-00000001', svs: ['backup-02', 'web-old-01'], d: '默认安全组：放行全部出站，入站只放行 22', tm: '2026-03-01', in: [['允许', 'TCP:22', '0.0.0.0/0', '']], out: [['允许', 'ALL', '0.0.0.0/0', '']] }];
    const G = st.sgs || G0; const fx = st.fx || '';
    const put = (gs, t, d) => this.setState(Object.assign({ sgs: gs }, t ? { tOn: 1, tT: t, tD: d || '立即生效，已记入操作记录。' } : {}));
    const groups = G.map((g, i) => ({ n: g.n, id: g.id, svs: g.svs.slice(0, 2).join('、') + (g.svs.length > 2 ? ' 等' : ''), svN: g.svs.length + ' 台', inN: g.in.length, outN: g.out.length, d: g.d, tm: g.tm,
      open: (e) => { ev(e); this.setState({ dw: i, dir: 'in', rPort: '', rSrc: '', rNote: '', rPol: '允许' }); }, delT: g.svs.length ? '解绑后可删除' : '删除',
      del: (e) => { ev(e); if (g.svs.length) { this.setState({ tOn: 1, tT: g.n + ' 还关联着 ' + g.svs.length + ' 台服务器', tD: '先在服务器详情里换绑到其他安全组，再删除。' }); return; } put(G.filter((_, j) => j !== i), '已删除安全组 ' + g.n); } }));
    const dwi = st.dw === undefined ? -1 : st.dw; const isNew = dwi === 'new';
    const TPL = { 'Web 服务器': [[['允许', 'TCP:80,443', '0.0.0.0/0', '网站访问'], ['允许', 'TCP:22', '0.0.0.0/0', 'SSH，建议改成办公室 IP']], '放行 80 / 443 / 22'], '仅 SSH': [[['允许', 'TCP:22', '0.0.0.0/0', '']], '只放行 22，其余入站拒绝'], '自定义': [[], '不带规则，自己添加'] };
    const tplK = st.tpl || 'Web 服务器';
    const cg = isNew ? (st.draft || { n: '', id: '', svs: [], d: '', tm: '刚刚', in: TPL[tplK][0].slice(), out: [['允许', 'ALL', '0.0.0.0/0', '']] }) : (dwi >= 0 ? G[dwi] : null);
    const dir = st.dir || 'in';
    const setCur = (c) => { if (isNew) this.setState({ draft: c }); else { const gs = G.slice(); gs[dwi] = c; this.setState({ sgs: gs }); } };
    const rules = cg ? cg[dir].map((r, i) => ({ p: r[0], pc: r[0] === '允许' ? 'kc-tag ok' : 'kc-tag err', port: r[1], src: r[2], note: r[3] || '—', del: (e) => { ev(e); const c = Object.assign({}, cg); c[dir] = cg[dir].filter((_, j) => j !== i); setCur(c); } })) : [];
    const rPol = st.rPol || '允许';
    const __R = { nav, groups, dwOn: !!cg, isNew, dwT: isNew ? '新建安全组' : cg ? '配置规则 · ' + cg.n : '', peer: dir === 'in' ? '来源' : '目标',
      dirs: [['入站规则', 'in'], ['出站规则', 'out']].map(([n, k]) => ({ n, c: cg ? cg[k].length : 0, on: k === dir, cls: k === dir ? 'kc-tab on' : 'kc-tab', pick: () => this.setState({ dir: k }) })), rules,
      pols: ['允许', '拒绝'].map((n) => ({ n, cls: n === rPol ? 'on' : '', go: () => this.setState({ rPol: n }) })),
      rPort: st.rPort || '', rSrc: st.rSrc || '', rNote: st.rNote || '', onPort: (e) => this.setState({ rPort: e.target.value }), onSrc: (e) => this.setState({ rSrc: e.target.value }), onNote: (e) => this.setState({ rNote: e.target.value }),
      addRule: (e) => { ev(e); const pt = (st.rPort || '').trim(); if (!pt) { this.setState({ tOn: 1, tT: '请填写协议端口', tD: '例如 TCP:443、UDP:53 或 ALL。' }); return; } const c = Object.assign({}, cg); const nr = [rPol, pt, (st.rSrc || '').trim() || '0.0.0.0/0', (st.rNote || '').trim()]; const ca = cg[dir].findIndex((r) => r[0] === '拒绝' && r[1] === 'ALL'); c[dir] = ca >= 0 && rPol === '允许' ? cg[dir].slice(0, ca).concat([nr], cg[dir].slice(ca)) : cg[dir].concat([nr]); setCur(c); this.setState({ rPort: '', rSrc: '', rNote: '' }); },
      tpls: Object.keys(TPL).map((n) => ({ n, cls: n === tplK ? 'on' : '', go: () => this.setState({ tpl: n, draft: Object.assign({}, cg, { in: TPL[n][0].slice() }) }) })), tplD: TPL[tplK][1],
      nName: (st.draft && st.draft.n) || '', onName: (e) => this.setState({ draft: Object.assign({}, cg, { n: e.target.value }) }),
      saveT: isNew ? '创建' : '完成',
      save: () => { if (isNew) { if (!cg.n.trim()) { this.setState({ tOn: 1, tT: '请填写安全组名称', tD: '' }); return; } const ng = Object.assign({}, cg, { id: 'sg-' + (Date.now() % 1e8).toString(16), d: TPL[tplK][1] }); this.setState({ sgs: G.concat([ng]), dw: -1, draft: null, tOn: 1, tT: '已创建安全组 ' + ng.n, tD: '还没有关联服务器，可以在服务器详情里关联。' }); return; } this.setState({ dw: -1, tOn: 1, tT: '规则已保存', tD: '对 ' + cg.svs.length + ' 台服务器立即生效。' }); },
      dwX: (e) => { ev(e); this.setState({ dw: -1, draft: null }); }, newSg: () => this.setState({ dw: 'new', dir: 'in', draft: null, tpl: 'Web 服务器' }),
      fixShow: fx !== 'gone', fixIdle: !fx, fixCls: fx === 'ok' ? 'ac-al i' : 'ac-al', fixI: fx === 'ok' ? '✓' : '!',
      fixT: fx === 'ok' ? '已放行 sg-strict 出方向 TCP:443' : 'web-new-04 的安全组 sg-strict 拦截了出方向 443，德迅安全卫士客户端装不上',
      fixD: fx === 'ok' ? '已在服务器上重新安装客户端，约 2 分钟。' : '一键放行会在 sg-strict 出站规则里加一条「允许 TCP:443 → agent.dexunyun.com」，只放行安装源，不影响其他规则。',
      fix: () => { const gs = G.map((g) => g.n !== 'sg-strict' ? g : Object.assign({}, g, { out: [['允许', 'TCP:443', 'agent.dexunyun.com', '德迅安全卫士安装源']].concat(g.out) })); this.setState({ sgs: gs, fx: 'ok' }); },
      tOn: !!st.tOn, tT: st.tT || '', tD: st.tD || '', tX: (e) => { ev(e); this.setState({ tOn: 0 }); } };
    const DDS = [];
"""

def build(name, title, cur, css, main, js):
    s = SHELL
    s = s.replace('<title>服务器列表</title>', '<title>%s</title>' % title, 1)
    s = s.replace('</style>\n</head>', css + '</style>\n</head>', 1)
    s = re.sub(r'<b>服务器(?:列表)?</b></nav>', '<b>%s</b></nav>' % cur, s, count=1)
    s = s.replace('id="kcf-IdcServers"', 'id="kcf-%s"' % name).replace('for="kcf-IdcServers"', 'for="kcf-%s"' % name)
    a = s.find('<main data-pg="IdcServers"'); b = s.find('</main>', a) + len('</main>')
    s = s[:a] + main + s[b:]
    s = re.sub(r"const cur = '[^']*';", "const cur = '%s';" % cur, s, count=1)
    s = re.sub(r"const pages = \{ '服务器(?:列表)?': 'IdcServers\.dc\.html'[^}]*\};", "const pages = %s;" % PAGES, s, count=1)
    s = NAVPAT.sub(lambda m: NAV, s, count=1)
    a = s.find('    const R = [[', s.find('  _rv() {')); assert a > s.find('  _rv() {') > 0
    s = s[:a] + js + DDJS
    open(os.path.join(D, name + '.dc.html'), 'w', encoding='utf-8').write(s)

build('IdcMonitor', '服务器 · 监控报表', '监控报表', MON_CSS, MON_MAIN, MON_JS)
build('IdcLogs', '服务器 · 操作记录', '操作记录', LOG_CSS, LOG_MAIN, LOG_JS)
build('IdcProtect', '服务器 · 防护设置', '防护设置', PRO_CSS, PRO_MAIN, PRO_JS)
build('IdcSecGroup', '服务器 · 安全组', '安全组', SG_CSS, SG_MAIN, SG_JS)

# 现有服务器页：侧栏接上新页面；运行时兜底跳转表也改过来
for f in ['IdcServers', 'IdcServerDetail', 'IdcReinstall']:
    p = os.path.join(D, f + '.dc.html'); s = open(p, encoding='utf-8').read()
    s = re.sub(r"const pages = \{ '服务器(?:列表)?': 'IdcServers\.dc\.html'[^}]*\};", "const pages = %s;" % PAGES, s, count=1)
    s = NAVPAT.sub(lambda m: NAV, s, count=1)
    s = s.replace("const cur = '服务器';", "const cur = '服务器列表';")
    s = s.replace("'监控报表': 'IdcServerDetail.dc.html'", "'监控报表': 'IdcMonitor.dc.html'").replace("'操作记录': 'IdcServerDetail.dc.html'", "'操作记录': 'IdcLogs.dc.html'")
    open(p, 'w', encoding='utf-8').write(s)
print('ok')
