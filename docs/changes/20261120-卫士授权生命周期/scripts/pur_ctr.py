import sys,re
SRC=sys.argv[1]; OUT=sys.argv[2]
a=open(SRC+'/AcctPurchase.dc.html').read(); b=open(SRC+'/BillConfirm.dc.html').read()
# keep AcctPurchase's dropdown logic block
sa=a.split('data-dc-script',1)[1]
dd=sa[sa.find('    const __s = this.state || {}; const __o'):sa.find('    const __pv =')]
t=b.replace('<title>确认订单 · 续费</title>','<title>选购产品</title>')
t=t.replace('kcf-BillConfirm','kcf-AcctPurchase').replace('data-pg="BillConfirm"','data-pg="AcctPurchase"')
t=t.replace('<a href="AcctSubs.dc.html">按资源</a><i>','<a href="AcctProducts.dc.html">按产品</a><i>',1).replace('<b>确认订单</b></nav>','<b>选购产品</b></nav>',1)
css='''/* pur-ctr 选购产品按费用中心结构（2026-11-23） */
.kc .pu-step.dis{opacity:.45;pointer-events:none}
.kc .pu-demo{margin-right:8px}
.kc .pu-demo button{font-size:12px}
.kc .pu-m b{font-weight:500}
</style>'''
h,rest=t.split('</helmet>',1)
h=h[::-1].replace('</style>'[::-1],css[::-1],1)[::-1]
t=h+'</helmet>'+rest
i=t.find('    <main data-pg="AcctPurchase" class="kc-main">'); j=t.find('    </main>',i)
main='''    <main data-pg="AcctPurchase" class="kc-main">
      <div class="kc-hd">
        <div class="kc-hdl"><div><h1 class="kc-h1">选购产品 · {{modeT}}</h1></div></div>
        <div class="kc-btns"><div class="fl-seg pu-demo" aria-label="演示状态"><sc-for list="{{modes}}" as="d" hint-placeholder-count="3"><button type="button" class="{{d.cls}}" onClick="{{d.go}}">{{d.n}}</button></sc-for></div><a class="kc-btn" href="AcctProducts.dc.html">返回</a></div>
      </div>
      <div class="ac-al i"><i>!</i><span>德迅安全卫士每个账号免费 3 台，当前已用 {{used}}；超出按台购买，只数台数，不绑定 IP 和设备。德迅云服务器随服务器赠送，不占授权。对公转账付款，核验到账后生效</span></div>
      <sc-if value="{{isGrace}}" hint-placeholder-val="{{false}}"><div class="ac-al e"><i>!</i><span>你已有 54 台已购授权，2026-11-01 到期，宽限至 11-08。宽限期内不能扩容，请先续费；过了宽限期需要重新购买</span><a class="kc-btn sm" href="BillConfirm.dc.html">去续费</a></div></sc-if>
      <section class="kc-card">
        <div class="kc-ch"><h2><i class="fi-i fi-box"></i>购买资源</h2><span class="kc-sub">共 1 项</span></div>
        <div class="fl-row" style="border-top:0"><span>购买产品</span><div><span class="{{ddC0}}"><button data-dd="0" class="kc-dd" type="button" aria-haspopup="listbox" onClick="{{ddT0}}"><span>产品</span><b>{{ddV0}}</b><svg class="rx" width="12" height="12" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M11.9999 13.1714L16.9497 8.22168L18.3639 9.63589L11.9999 15.9999L5.63599 9.63589L7.0502 8.22168L11.9999 13.1714Z"></path></svg></button><sc-if value="{{ddO0}}" hint-placeholder-val="{{false}}"><span class="dd-m" onClick="{{ddX}}"></span><span class="dd-p" role="listbox"><sc-for list="{{ddL0}}" as="o" hint-placeholder-count="4"><button type="button" role="option" class="{{o.cls}}" onClick="{{o.go}}">{{o.t}}</button></sc-for></span></sc-if></span></div></div>
        <div class="fl-row"><span>购买方式</span><div class="pu-m"><b>{{modeB}}</b><p class="kc-hint">{{modeH}}</p></div></div>
        <sc-if value="{{isNew}}" hint-placeholder-val="{{true}}"><div class="fl-row"><span>服务期限</span><div><div class="fl-seg"><sc-for list="{{durs}}" as="d" hint-placeholder-count="6"><button type="button" class="{{d.cls}}" onClick="{{d.go}}">{{d.n}}</button></sc-for></div></div></div></sc-if>
        <sc-if value="{{notNew}}" hint-placeholder-val="{{false}}"><div class="fl-row"><span>服务期限</span><div>{{termTxt}}</div></div></sc-if>
        <div class="fl-row" style="border-bottom:1px solid #f2f4f8"><span>购买台数</span><div><span class="{{stepCls}}"><button type="button" aria-label="减少" onClick="{{dec}}">−</button><b>{{qty}}</b><button type="button" aria-label="增加" onClick="{{inc}}">+</button></span><span class="pu-formula" style="margin-left:12px">购买后共 {{hosts}} 台（含免费 3 台）</span></div></div>
        <div class="kc-tw"><table class="kc-t">
          <thead><tr><th>资源</th><th>配置</th><th>期限</th><th>到期</th><th class="num">单价</th><th class="num">金额</th></tr></thead>
          <tbody><sc-for list="{{rows}}" as="r" hint-placeholder-count="1"><tr class="{{r.rc}}"><sc-for list="{{r.c}}" as="c" hint-placeholder-count="6"><td class="{{c.td}}"><sc-if value="{{c.a}}" hint-placeholder-val="{{false}}"><a href="{{c.href}}">{{c.t}}</a></sc-if><sc-if value="{{c.p}}" hint-placeholder-val="{{true}}"><span class="{{c.cls}}">{{c.t}}</span></sc-if><sc-if value="{{c.hasSub}}" hint-placeholder-val="{{false}}"><div class="{{c.sc}}">{{c.s}}</div></sc-if></td></sc-for></tr></sc-for></tbody>
        </table></div>
        <div class="fl-tot"><div>商品合计<b>价格待定</b></div><div>代金券<b>暂无可用</b></div><div class="big">应付金额<b>价格待定</b></div></div>
      </section>
      <section class="kc-card" style="margin-top:16px">
        <div class="kc-ch"><h2><i class="fi-i fi-wallet"></i>付款与票据</h2></div>
        <div class="fl-row"><span>付款方式</span><div><b style="font-weight:500">对公转账</b><p class="kc-hint">提交后在付款页查看收款账户；财务核验到账后自动开通</p></div></div>
        <div class="fl-row"><span>合同</span><div><div class="fl-seg"><sc-for list="{{cons}}" as="d" hint-placeholder-count="2"><button type="button" class="{{d.cls}}" onClick="{{d.go}}">{{d.n}}</button></sc-for></div></div></div>
        <div class="fl-row"><span>发票</span><div>付款完成后在「发票管理」申请，抬头默认 <b style="font-weight:500">浙江德迅科技有限公司</b></div></div>
      </section>
      <sc-if value="{{needId}}" hint-placeholder-val="{{false}}"><div class="ac-al" style="margin-top:16px"><i>!</i><span>购买前需完成个人实名认证<em>订单会保存为草稿，认证通过后回到这里继续</em></span><a class="kc-btn sm" href="OrgVerify.dc.html">去认证</a></div></sc-if>
      <div class="fl-sum"><label class="agree"><button type="button" class="{{agreeCls}}" aria-label="同意协议" onClick="{{togA}}"></button>我已阅读并同意<a href="#">《德迅云服务协议》</a></label><small>应付</small><b>价格待定</b><a class="{{subCls}}" href="BillPayment.dc.html">提交订单</a></div>
'''
t=t[:i]+main+t[j:]
logic='''    const D = [['1 个月', 1], ['3 个月', 3], ['6 个月', 6], ['1 年', 12], ['2 年', 24], ['3 年', 36]];
    const dn = st.dur || '1 年'; const m = D.find((d) => d[0] === dn)[1];
    const durs = D.map(([n]) => ({ n, cls: n === dn ? 'on' : '', go: () => this.setState({ dur: n }) }));
    const MD = [['演示：新购', 'new'], ['演示：扩容', 'add'], ['演示：宽限期', 'grace']];
    const mode = st.mode || 'new';
    const modes = MD.map(([n, k]) => ({ n, cls: k === mode ? 'on' : '', go: () => this.setState({ mode: k }) }));
    const isNew = mode === 'new', isAdd = mode === 'add', isGrace = mode === 'grace';
    const qty = st.q || 5; const base = isNew ? 3 : 57;
    const cn = st.con || '不需要';
    const cons = ['不需要', '电子合同'].map((n) => ({ n, cls: n === cn ? 'on' : '', go: () => this.setState({ con: n }) }));
    const agree = st.agree !== false; const can = agree && !isGrace;
    const term = isNew ? dn : isAdd ? '折算 64 天' : '—';
    const exp = isNew ? { t: '到账日起 ' + dn, s: '核验到账后开始计算', sc: '' } : isAdd ? { t: '2027-01-26', s: '跟随现有授权', sc: '' } : { t: '2026-11-01', s: '宽限至 11-08', sc: 'o' };
    const rows = [ROW([{ t: '德迅安全卫士授权', s: isNew ? '新购' : '扩容 · 并入现有授权' }, qty + ' 台', term, exp, { t: '待定 /台/年', c: 'ac-n m', td: 'num' }, { t: '价格待定', c: 'ac-n', td: 'num' }], [])];
    const __R = Object.assign({ nav }, {
      durs, modes, isNew, notNew: !isNew, isGrace, qty, hosts: base + qty, used: isNew ? '3 / 3' : '57 / 57',
      modeT: isNew ? '新购' : isAdd ? '扩容' : '宽限期内',
      modeB: isNew ? '新购授权' : '扩容 · 并入现有授权',
      modeH: isNew ? '账号还没有已购授权，选择台数和服务期限' : isAdd ? '现有 54 台，2027-01-26 到期（剩 64 天）。扩容的台数跟随这个到期日，按剩余天数折算价格；剩余不足 30 天时请先续费' : '现有 54 台已到期，处于宽限期',
      termTxt: isAdd ? '跟随现有授权，到期 2027-01-26（折算 64 天）' : '宽限期内不能扩容，请先续费',
      rows, cons, stepCls: isGrace ? 'pu-step dis' : 'pu-step',
      dec: () => this.setState({ q: Math.max(1, qty - 1) }), inc: () => this.setState({ q: Math.min(999, qty + 1) }), needId: false,
      agreeCls: agree ? 'ac-cbx on' : 'ac-cbx', togA: () => this.setState({ agree: !agree }), subCls: can ? 'kc-btn pri' : 'kc-btn pri dis' });

'''
sb=t.split('data-dc-script',1)
k=sb[1].find("    const D = [['1 个月'"); e=sb[1].find('  }\n}\n</script>')
sb[1]=sb[1][:k]+logic+dd+"    return Object.assign(__R, DDX);\n"+sb[1][e:]
t='data-dc-script'.join(sb)
open(OUT+'/AcctPurchase.dc.html','w').write(t)
print('ok')
