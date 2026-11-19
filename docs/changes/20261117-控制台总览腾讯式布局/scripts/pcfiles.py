#!/usr/bin/env python3
"""我的产品：参考 affectUI Files 页（幂等，标记 pcf-v1，在 pcboard.py 之后跑）。
77（2026-11-19）同意方案：
- 筛选合成一行：左边状态筛选（安静页签：选中浅灰底，未选中无底无框），右边「按产品 / 按资源」分段切换、卡片 / 列表、搜索、购买产品
- 搜索按产品名、套餐、分类、说明过滤，计数跟着变；搜不到时显示空状态和「清除搜索」
- 加载中：灰色占位，形状和真实卡片一致；空状态：图标 + 一句说明 + 购买产品
- 底部「原型状态」切换（数据 / 加载中 / 无产品），只用于演示
用法: pcfiles.py AcctProducts.dc.html
"""
import sys, re

SEARCH_SVG = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'
BOX_SVG = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 8 12 3 3 8v8l9 5 9-5V8z"/><path d="m3 8 9 5 9-5M12 13v8"/></svg>'

SK_CARD = ('<li class="pc-c pc-skc"><span class="pc-skr"><i class="pc-sk" style="width:40px;height:40px"></i><span class="pc-skl">'
           '<i class="pc-sk" style="width:96px;height:10px"></i><i class="pc-sk" style="width:64px;height:8px"></i></span></span>'
           '<i class="pc-sk" style="width:92%;height:8px;margin-top:22px"></i><i class="pc-sk" style="width:64%;height:8px;margin-top:12px"></i>'
           '<i class="pc-sk" style="width:100%;height:4px;margin-top:30px"></i><i class="pc-sk" style="width:40%;height:8px;margin-top:20px"></i>'
           '<span class="pc-skf"><i class="pc-sk" style="width:72px;height:8px"></i><i class="pc-sk" style="width:52px;height:28px;margin-left:auto"></i></span></li>')
SK_LANE = ('<div class="pc-lane"><header class="pc-lh"><i class="pc-sk" style="width:14px;height:14px"></i><i class="pc-sk" style="width:56px;height:10px"></i></header>'
           '<ul class="pc-grid">' + SK_CARD * 3 + '</ul></div>')

STATES = ('\n        <sc-if value="{{pcLoad}}" hint-placeholder-val="{{false}}"><div class="pc-wall pc-skw" aria-busy="true" aria-label="正在加载产品">' + SK_LANE * 2 + '</div></sc-if>'
          '\n        <sc-if value="{{pcEmpty}}" hint-placeholder-val="{{false}}"><div class="pc-emp"><span class="pc-emp-ic">' + BOX_SVG + '</span><b>还没有产品</b>'
          '<p>购买后，产品会按「需处理 / 正常运行 / 已结束」分组显示在这里，到期和用量提醒也会出现在卡片上。</p><a class="kc-btn pri" href="AcctPurchase.dc.html">购买产品</a></div></sc-if>'
          '\n        <sc-if value="{{pcNone}}" hint-placeholder-val="{{false}}"><div class="pc-emp"><span class="pc-emp-ic">' + SEARCH_SVG.replace('width="14" height="14"', 'width="28" height="28"').replace('stroke-width="2"', 'stroke-width="1.5"') + '</span><b>没有找到相关产品</b>'
          '<p>{{pcNoneT}}</p><button type="button" class="kc-btn" onClick="{{pcClrQ}}">清除搜索</button></div></sc-if>'
          '\n        <div class="pc-demo" role="group" aria-label="原型状态"><span>原型状态</span><sc-for list="{{pcModes}}" as="m" hint-placeholder-count="3"><button type="button" class="{{m.cls}}" onClick="{{m.go}}">{{m.n}}</button></sc-for></div>')

CSS = r'''
/* pcf-v1 参考 Files：筛选一行、安静页签、搜索、加载中和空状态 */
.pc .pc-bar{min-height:32px}
.pc .pc-sc{gap:4px;padding:0;background:none}
.pc .pc-sc button{height:28px;padding:0 10px;border-radius:2px;font-size:12px;color:rgba(0,0,0,.7);box-shadow:none}
.pc .pc-sc button:hover{background:#f7f8fb;color:rgba(0,0,0,.9)}
.pc .pc-sc button.on{background:#f2f4f8;color:rgba(0,0,0,.9);font-weight:500;box-shadow:none}
.pc .pc-tools{gap:8px}
.pc .pc-tools>nav.pc-tabs{display:inline-flex;gap:2px;padding:2px;margin:0;border:0;background:#f2f3f5}
.pc .pc-tools>nav.pc-tabs>a{height:28px;padding:0 12px;border:0;border-radius:0;background:transparent;font-size:12px;font-weight:400;color:rgba(0,0,0,.6)}
.pc .pc-tools>nav.pc-tabs>a:hover{color:rgba(0,0,0,.9)}
.pc .pc-tools>nav.pc-tabs>a.on{background:#fff;color:rgba(0,0,0,.9);font-weight:500;box-shadow:0 1px 2px rgba(0,0,0,.06)}
.pc-q{position:relative;display:inline-flex;align-items:center}
.pc-q svg{position:absolute;left:10px;color:rgba(0,0,0,.4);pointer-events:none}
.pc-q input{width:200px;height:32px;padding:0 10px 0 30px;border:1px solid #e6e9ef;border-radius:0;background:#fff;font:inherit;font-size:12px;color:rgba(0,0,0,.9);outline:0}
.pc-q input::placeholder{color:rgba(0,0,0,.4)}
.pc-q input:hover{border-color:#d6dbe3}
.pc-q input:focus{border-color:#1664ff}
@keyframes pcSk{0%{background-position:100% 0}100%{background-position:0 0}}
.pc-sk{display:block;flex:none;border-radius:2px;background:linear-gradient(90deg,#eef0f4 0%,#f6f7f9 40%,#eef0f4 80%);background-size:300% 100%;animation:pcSk 1.4s ease-in-out infinite}
.pc .pc-skw{background:#fff;border-top:1px solid #e5e6eb}
.pc .pc-skw .pc-lh{gap:8px}
.pc .pc-skc{height:236px;padding:20px;box-sizing:border-box;pointer-events:none}
.pc-skr{display:flex;gap:12px;align-items:center}
.pc-skl{display:grid;gap:8px}
.pc-skf{display:flex;align-items:center;margin-top:24px}
.pc-emp{display:grid;justify-items:center;gap:8px;margin:0;padding:64px 20px 72px;border-top:1px solid #e5e6eb;text-align:center}
.pc-emp-ic{display:grid;place-items:center;width:56px;height:56px;margin-bottom:8px;border-radius:50%;background:#f2f4f8;color:rgba(0,0,0,.45)}
.pc-emp b{font-size:14px;font-weight:500;color:rgba(0,0,0,.9)}
.pc-emp p{max-width:360px;margin:0 0 8px;font-size:12px;line-height:20px;color:rgba(0,0,0,.5)}
.pc-demo{position:sticky;bottom:16px;z-index:5;display:flex;align-items:center;gap:2px;width:max-content;margin:16px auto 0;padding:2px 2px 2px 10px;background:#f2f3f5;box-shadow:0 2px 8px -1px rgba(0,0,0,.08);font-size:12px}
.pc-demo>span{margin-right:6px;color:rgba(0,0,0,.45)}
.pc-demo button{height:26px;padding:0 12px;border:0;background:transparent;font:inherit;font-size:12px;color:rgba(0,0,0,.6);cursor:pointer}
.pc-demo button.on{background:#fff;color:rgba(0,0,0,.9);font-weight:500;box-shadow:0 1px 2px rgba(0,0,0,.06)}
@media (prefers-reduced-motion:reduce){.pc-sk{animation:none}}
'''

for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    if 'pcf-v1' in s:
        print('skip', p); continue
    if 'pcb-v1' not in s:
        sys.exit('run pcboard.py first')
    # 1 页签条挪进右侧工具区，去掉画板里的行内样式
    m = re.search(r'\s*<nav class="pc-tabs"[^>]*>(.*?)</nav>', s, re.S)
    nav = '<nav class="pc-tabs" aria-label="查看方式">' + re.sub(r'\s*style="[^"]*"', '', m.group(1)) + '</nav>'
    s = s[:m.start()] + s[m.end():]
    a = '<div class="pc-tools"><div class="pc-vw"'
    assert s.count(a) == 1
    s = s.replace(a, '<div class="pc-tools">' + nav + '<div class="pc-vw"')
    b = '<a class="kc-btn pri" href="AcctPurchase.dc.html">购买产品</a></div>\n        </div>'
    assert s.count(b) == 1, 'buy'
    s = s.replace(b, '<label class="pc-q">' + SEARCH_SVG + '<input type="search" aria-label="搜索产品" placeholder="搜索产品" value="{{pcQ}}" onChange="{{onPcQ}}"></label>' + b)
    # 2 状态
    c = '\n        </div>\n      </section>\n      <sc-if value="{{pcDOn}}"'
    assert s.count(c) == 1, 'states'
    s = s.replace(c, STATES + c)
    # 3 JS
    d = "    const lane = (t) =>"
    assert s.count(d) == 1
    s = s.replace(d, "    const pq = (st.pcQ || '').trim(); const pql = pq.toLowerCase(); const pm = st.pcM || 'data';\n"
                     "    const PS = pm === 'empty' ? [] : P.filter((p) => !pql || [p[1], p[2], p[3], p[4]].join(' ').toLowerCase().includes(pql));\n" + d)
    for x, y in [("P.filter((p) => lane(p[6]) === k).length", "PS.filter((p) => lane(p[6]) === k).length"),
                 ("[['all', '全部', P.length]]", "[['all', '全部', PS.length]]"),
                 ("const items = P.filter((p) => lane(p[6]) === l[0])", "const items = PS.filter((p) => lane(p[6]) === l[0])"),
                 ("map(([k, n, c]) => ({ n, c, nc:", "map(([k, n, c]) => ({ n, c: pm === 'loading' ? '' : c, nc:"),
                 ("return { pcScopes, pcLanes, pcBoard: vw === 'board', pcList: vw === 'list',",
                  "const pcHas = pm === 'data' && PS.length > 0;\n    return { pcScopes, pcLanes, pcBoard: pcHas && vw === 'board', pcList: pcHas && vw === 'list',\n"
                  "      pcLoad: pm === 'loading', pcEmpty: pm === 'empty', pcNone: pm === 'data' && !PS.length, pcNoneT: '没有和「' + pq + '」匹配的产品，换个关键词试试。',\n"
                  "      pcQ: st.pcQ || '', onPcQ: (e) => this.setState({ pcQ: e && e.target ? e.target.value : '' }), pcClrQ: () => this.setState({ pcQ: '' }),\n"
                  "      pcModes: [['data', '数据'], ['loading', '加载中'], ['empty', '无产品']].map(([k, n]) => ({ n, cls: k === pm ? 'on' : '', go: () => this.setState({ pcM: k, pcO: '' }) })),")]:
        assert s.count(x) == 1, x
        s = s.replace(x, y)
    i = s.index('<x-dc>'); j = s.index('</style>', i)
    s = s[:j] + CSS + s[j:]
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', p)
