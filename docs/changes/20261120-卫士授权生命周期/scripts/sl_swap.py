import sys
f=sys.argv[1]; t=open(f).read()
R=[
('卫士管理可以提前在<a href="SecHosts.dc.html">资产列表</a>里更换保留的 3 台。','卫士管理可以提前<a href="#" onClick="{{st.swOpen}}">更换保留的 3 台</a>。'),
("'宽限期', 'sl-st r', '数据保留至 11-08', [lk('续费')]]","'宽限期', 'sl-st r', '宽限至 11-08', [lk('续费'), { n: '更换保留主机', href: '#', go: ev(() => S({ slSw: 1 })) }]]"),
('      <sc-if value="{{st.tsOn}}" hint-placeholder-val="{{false}}"><div class="sh-toast',
 '''      <sc-if value="{{st.swOn}}" hint-placeholder-val="{{false}}"><div class="sh-mask sh-fx" onClick="{{st.swX}}"></div><aside class="sh-dw sh-fx" role="dialog" aria-modal="true" aria-label="更换保留主机"><header><h3>更换保留主机</h3><button type="button" class="sh-x" aria-label="关闭" onClick="{{st.swX}}">×</button></header><div class="sh-dwb"><div class="ac-al i" style="margin:0 0 16px"><i>i</i><span>11-08 宽限期结束后只剩免费 3 台。默认保留最早接入的 3 台，其余 54 台停止检测，数据保留 30 天；续费核验到账后全部恢复。只有卫士管理可以更换</span></div><div style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px"><input class="kc-in" type="search" placeholder="搜索主机名称或 IP" aria-label="搜索主机" style="width:280px"><span class="sl-sub">已选 {{st.swN}} / 3 台</span></div><div class="kc-tw"><table class="kc-t"><thead><tr><th style="width:40px"><span class="sl-sub">保留</span></th><th>主机</th><th>接入时间</th><th>11-08 后</th></tr></thead><tbody><sc-for list="{{st.swRows}}" as="r" hint-placeholder-count="8"><tr><td><button type="button" class="{{r.c}}" role="checkbox" aria-checked="{{r.a}}" aria-label="保留 {{r.n}}" onClick="{{r.pick}}"></button></td><td><div class="sl-a">{{r.n}}</div><div class="sl-sub">{{r.ip}}</div></td><td>{{r.j}}</td><td><span class="{{r.sc}}">{{r.st}}</span></td></tr></sc-for></tbody></table></div><p class="sl-sub" style="margin-top:8px">共 57 台，显示最早接入的 10 台</p></div><footer><button type="button" class="kc-btn" onClick="{{st.swX}}">取消</button><button type="button" class="kc-btn pri" onClick="{{st.swOk}}">保存</button></footer></aside></sc-if>
      <sc-if value="{{st.tsOn}}" hint-placeholder-val="{{false}}"><div class="sh-toast'''),
("        .map(([id, n, ed, use, t, s2, sc, why, ops]) => ({ id, n, ed, use, t, st: s2, sc, why, ops }));\n    }",
 """        .map(([id, n, ed, use, t, s2, sc, why, ops]) => ({ id, n, ed, use, t, st: s2, sc, why, ops }));
      /* sl-swap 2026-11-23 更换保留主机 */
      const KP0 = { 'web-prod-01': 1, 'web-prod-02': 1, 'db-01': 1 }; const keep = st.slKeep || KP0;
      const HL = [['web-prod-01', '10.0.1.11', '2025-11-02'], ['web-prod-02', '10.0.1.12', '2025-11-02'], ['db-01', '10.0.4.41', '2025-11-03'], ['web-prod-03', '10.0.1.13', '2025-11-05'], ['app-01', '10.0.2.21', '2025-11-08'], ['app-02', '10.0.2.22', '2025-11-08'], ['app-03', '10.0.2.23', '2025-11-12'], ['cache-01', '10.0.3.31', '2025-12-01'], ['cache-02', '10.0.3.32', '2025-12-01'], ['api-01', '10.0.5.51', '2026-01-15']];
      o.swOn = !!st.slSw; o.swOpen = ev(() => S({ slSw: 1 })); o.swX = ev(() => S({ slSw: 0 })); o.swN = Object.keys(keep).length;
      o.swRows = HL.map(([n, ip, j]) => { const on = !!keep[n]; return { n, ip, j, c: on ? 'sh-ck on' : 'sh-ck', a: on ? 'true' : 'false', st: on ? '继续检测' : '停止检测', sc: on ? 'kc-tag ok' : 'kc-tag mut',
        pick: ev(() => { const k = Object.assign({}, keep); if (k[n]) delete k[n]; else { if (Object.keys(k).length >= 3) { toast('最多保留 3 台，先取消一台', 'info'); return; } k[n] = 1; } S({ slKeep: k }); }) }; });
      o.swOk = ev(() => { if (!Object.keys(keep).length) { toast('至少保留 1 台', 'info'); return; } S({ slSw: 0 }); toast('已保存：11-08 后保留 ' + Object.keys(keep).join('、') + ' 继续检测'); });
    }"""),
]
n=0
for o,nw in R:
    if nw in t: continue
    assert t.count(o)==1,(o[:60],t.count(o)); t=t.replace(o,nw); n+=1
open(f,'w').write(t); print('patched',n)
