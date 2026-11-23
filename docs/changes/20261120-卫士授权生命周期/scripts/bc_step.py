import sys
f=sys.argv[1]; t=open(f).read()
R=[
('<span class="kc-sub">共 {{n}} 项</span></div>',
 '<span class="kc-sub">共 {{n}} 项</span></div>\n        <div class="fl-row" style="border-top:0"><span>卫士授权台数</span><div><span class="pu-step"><button type="button" aria-label="减少" onClick="{{gDec}}">−</button><b>{{gq}}</b><button type="button" aria-label="增加" onClick="{{gInc}}">+</button></span><span class="pu-formula" style="margin-left:12px">{{gTip}}</span></div></div>'),
('<div class="fl-row" style="border-top:0;border-bottom:1px solid #f2f4f8"><span>续费时长</span>',
 '<div class="fl-row" style="border-bottom:1px solid #f2f4f8"><span>续费时长</span>'),
("    const fmt = (v) =>",
 "    const gq = st.gq === undefined ? 54 : st.gq; const gCut = 54 - gq;\n    const fmt = (v) =>"),
("    const sum = IT.reduce(",
 "    rows.push(ROW([{ t: 'dx-guard-01', a: 'https://claude.ai/artifact/LE5cNnQWZjPMjXvXCC4MG7#play-de5201e8a0c7', s: '德迅安全卫士授权' }, gq + ' 台', { t: '2026-11-01', s: '宽限至 11-08', sc: 'o' }, { t: add('2026-11', m) + '-01', c: 'ac-n' }, { t: '待定 /台/年', c: 'ac-n m', td: 'num' }, { t: '价格待定', c: 'ac-n', td: 'num' }], []));\n    const sum = IT.reduce("),
("return Object.assign({ nav }, { durs, rows, n: IT.length,",
 "return Object.assign({ nav }, { gq, gDec: () => this.setState({ gq: Math.max(0, gq - 1) }), gInc: () => this.setState({ gq: Math.min(999, gq + 1) }), gTip: gCut > 0 ? '减少 ' + gCut + ' 台：核验到账后这 ' + gCut + ' 台停止检测，可以先在资产列表选择保留哪些主机' : gCut < 0 ? '增加的台数请走扩容，续费只能保持或减少台数' : '现有 54 台，续费可以减少台数', durs, rows, n: IT.length + 1,"),
('<div class="fl-tot"><div>商品合计<b>¥{{sum}}</b></div>',
 '<div class="fl-tot"><div>商品合计<b>¥{{sum}} + 卫士授权（价格待定）</b></div>'),
]
n=0
for o,nw in R:
    if nw in t: continue
    assert t.count(o)==1,(o,t.count(o)); t=t.replace(o,nw); n+=1
open(f,'w').write(t); print('patched',n)
