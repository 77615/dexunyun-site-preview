import sys
f=sys.argv[1]; t=open(f).read()
DDSTART='<div class="fl-row" style="border-top:0"><span>购买产品</span><div><span class="{{ddC0}}">'
i=t.find(DDSTART)
if i>=0:
    j=t.find('</sc-if></span></div></div>',i)+len('</sc-if></span></div></div>')
    t=t[:i]+'<div class="fl-row" style="border-top:0"><span>购买产品</span><div><b style="font-weight:500">德迅安全卫士 · 主机授权</b><p class="kc-hint">按台购买的产品在这里下单。服务器去<a href="https://claude.ai/artifact/JTatd1LoQ65E2izzN6Aizu#artboard-ServerBuy">服务器选购页</a>选配置；高防 IP、SCDN、游戏盾等按规格购买的产品，在官网产品页选择规格后下单</p></div></div>'+t[j:]
R=[
('<sc-if value="{{isGrace}}" hint-placeholder-val="{{false}}"><div class="ac-al e"><i>!</i><span>你已有 54 台已购授权，2026-11-01 到期，宽限至 11-08。宽限期内不能扩容，请先续费；过了宽限期需要重新购买</span><a class="kc-btn sm" href="BillConfirm.dc.html">去续费</a></div></sc-if>',
 '<sc-if value="{{hasAl}}" hint-placeholder-val="{{false}}"><div class="{{alC}}"><i>!</i><span>{{alT}}</span><a class="kc-btn sm" href="{{alHref}}">{{alBtn}}</a></div></sc-if>'),
('<span class="pu-formula" style="margin-left:12px">购买后共 {{hosts}} 台（含免费 3 台）</span>','<span class="pu-formula" style="margin-left:12px">{{qtyTip}}</span>'),
('<a class="{{subCls}}" href="BillPayment.dc.html">提交订单</a></div>','<a class="{{subCls}}" href="{{subHref}}">{{subTxt}}</a></div>'),
("    const MD = [['演示：新购', 'new'], ['演示：扩容', 'add'], ['演示：宽限期', 'grace']];",
 "    const MD = [['新购', 'new'], ['扩容', 'add'], ['不足 30 天', 'near'], ['宽限期', 'grace'], ['已过宽限期', 'lapsed'], ['有待付款单', 'pending']];"),
("    const isNew = mode === 'new', isAdd = mode === 'add', isGrace = mode === 'grace';\n    const qty = st.q || 5; const base = isNew ? 3 : 57;",
 "    const isLap = mode === 'lapsed', isNear = mode === 'near', isPend = mode === 'pending';\n    const isNew = mode === 'new' || isLap, isAdd = mode === 'add' || isNear || isPend, isGrace = mode === 'grace';\n    const blocked = isGrace || isNear || isPend;\n    const qty = st.q || 5; const base = mode === 'new' ? 3 : isLap ? 3 : 57;\n    const AL = { grace: ['ac-al e', '你已有 54 台已购授权，2026-11-01 到期，宽限至 11-08。宽限期内不能扩容，请先续费；过了宽限期需要重新购买', '去续费', 'BillConfirm.dc.html'], near: ['ac-al e', '现有 54 台授权 2026-12-10 到期，只剩 17 天。剩余不足 30 天不能扩容，请先续费，续费到账后再扩容', '去续费', 'BillConfirm.dc.html'], pending: ['ac-al', '这份授权已有 1 笔待付款订单 DX20261102005（续费 1 年）。同一份授权同时只能有 1 笔待付款订单，请先付款，或在订单里取消后再下单', '去付款', 'BillPayment.dc.html'], lapsed: ['ac-al', '已购的 54 台授权 11-08 宽限期已过，54 台主机已停止检测，数据保留至 12-08。这次按新购计算，从到账日起算；到账后先按最早接入的顺序恢复被停的主机，买几台恢复几台', '查看被停主机', 'https://claude.ai/artifact/LE5cNnQWZjPMjXvXCC4MG7#play-de5201e8a0c7'] }[mode];"),
("      modeT: isNew ? '新购' : isAdd ? '扩容' : '宽限期内',\n      modeB: isNew ? '新购授权' : '扩容 · 并入现有授权',\n      modeH: isNew ? '账号还没有已购授权，选择台数和服务期限' : isAdd ? '现有 54 台，2027-01-26 到期（剩 64 天）。扩容的台数跟随这个到期日，按剩余天数折算价格；剩余不足 30 天时请先续费' : '现有 54 台已到期，处于宽限期',\n      termTxt: isAdd ? '跟随现有授权，到期 2027-01-26（折算 64 天）' : '宽限期内不能扩容，请先续费',",
 "      modeT: isLap ? '重新购买' : isNew ? '新购' : isGrace ? '宽限期内' : '扩容',\n      modeB: isLap ? '重新购买授权' : isNew ? '新购授权' : '扩容 · 并入现有授权',\n      modeH: isLap ? '原授权已过宽限期，重新购买的授权从到账日起算，和原授权无关' : isNew ? '账号还没有已购授权，选择台数和服务期限' : isNear ? '现有 54 台，2026-12-10 到期（剩 17 天）' : isPend ? '现有 54 台，2027-01-26 到期（剩 64 天）' : isAdd ? '现有 54 台，2027-01-26 到期（剩 64 天）。扩容的台数跟随这个到期日，按剩余天数折算价格；剩余不足 30 天时请先续费' : '现有 54 台已到期，处于宽限期',\n      termTxt: isGrace ? '宽限期内不能扩容，请先续费' : isNear ? '剩余不足 30 天，不能扩容' : '跟随现有授权，到期 2027-01-26（折算 64 天）',\n      hasAl: !!AL, alC: AL ? AL[0] : '', alT: AL ? AL[1] : '', alBtn: AL ? AL[2] : '', alHref: AL ? AL[3] : '#',\n      qtyTip: isLap ? '购买后共 ' + (3 + qty) + ' 台（含免费 3 台）；到账后恢复 ' + Math.min(qty, 54) + ' 台被停主机' + (qty < 54 ? '，其余 ' + (54 - qty) + ' 台仍停止检测' : '') : '购买后共 ' + (base + qty) + ' 台（含免费 3 台）',\n      subTxt: isPend ? '去付款' : '提交订单', subHref: isPend ? 'BillPayment.dc.html' : 'BillPayment.dc.html',"),
("rows, cons, stepCls: isGrace ? 'pu-step dis' : 'pu-step',","rows, cons, stepCls: blocked ? 'pu-step dis' : 'pu-step',"),
("subCls: can ? 'kc-btn pri' : 'kc-btn pri dis' });","subCls: isPend ? 'kc-btn pri' : can ? 'kc-btn pri' : 'kc-btn pri dis' });"),
("const agree = st.agree !== false; const can = agree && !isGrace;","const agree = st.agree !== false; const can = agree && !blocked;"),
("    const term = isNew ? dn : isAdd ? '折算 64 天' : '—';","    const term = isNew ? dn : (isAdd && !isNear) ? '折算 64 天' : '—';"),
("    const exp = isNew ?","    const exp = isLap ? { t: '到账日起 ' + dn, s: '原授权已过宽限期', sc: '' } : isNear ? { t: '2026-12-10', s: '剩 17 天', sc: 'o' } : isNew ?"),
("{ t: '德迅安全卫士授权', s: isNew ? '新购' : '扩容 · 并入现有授权' }","{ t: '德迅安全卫士授权', s: isLap ? '重新购买' : isNew ? '新购' : '扩容 · 并入现有授权' }"),
("used: isNew ? '3 / 3' : '57 / 57',","used: mode === 'new' ? '3 / 3' : isLap ? '3 / 3（另有 54 台已停止检测）' : '57 / 57',"),
]
n=0
for o,nw in R:
    if nw in t: continue
    assert t.count(o)==1,(o[:80],t.count(o)); t=t.replace(o,nw); n+=1
open(f,'w').write(t); print('patched',n)
