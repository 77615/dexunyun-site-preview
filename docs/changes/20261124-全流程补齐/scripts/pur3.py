#!/usr/bin/env python3
"""AcctPurchase: 按规格购买的产品（DDoS 高防 IP / 游戏盾 / SSL 证书）也能在这里下单。幂等。
用法: pur3.py <AcctPurchase.dc.html>（画布副本或仓库副本都可）"""
import sys
p = sys.argv[1]
s = open(p, encoding='utf8').read()
if 'pur3:' in s:
    print('already', p); sys.exit(0)
repo = '../ServerBuy.dc.html' in s
CONTACT = '../Contact.dc.html' if repo else 'https://claude.ai/artifact/JTatd1LoQ65E2izzN6Aizu#artboard-Contact'
LIST = {'ddos': 'DdosInstances.dc.html' if repo else 'https://claude.ai/artifact/RL3XvNLs2o41CLGG3mLqe9#play-d1c5e98bff1b',
        'game': 'GameAccess.dc.html' if repo else 'https://claude.ai/artifact/9WQ1i2DeBHUULxBDB2KQ6p#play-ef67b4d479f4',
        'ssl': 'AcctProducts.dc.html'}
n = 0
def rep(a, b):
    global s, n
    assert s.count(a) == 1, ('anchor', a[:80], s.count(a))
    s = s.replace(a, b); n += 1

# 1 页头演示：加「产品」切换；卫士状态切换只在卫士授权下显示
rep('<span class="kc-sub pu-demo-l" style="margin-right:8px">演示</span><div class="fl-seg pu-demo" aria-label="演示状态"><sc-for list="{{modes}}" as="d" hint-placeholder-count="3"><button type="button" class="{{d.cls}}" onClick="{{d.go}}">{{d.n}}</button></sc-for></div>',
    '<span class="kc-sub pu-demo-l" style="margin-right:8px">演示</span><div class="fl-seg pu-demo" aria-label="演示产品"><sc-for list="{{prods}}" as="d" hint-placeholder-count="4"><button type="button" class="{{d.cls}}" onClick="{{d.go}}">{{d.n}}</button></sc-for></div><sc-if value="{{isG}}" hint-placeholder-val="{{true}}"><div class="fl-seg pu-demo" aria-label="演示状态"><sc-for list="{{modes}}" as="d" hint-placeholder-count="3"><button type="button" class="{{d.cls}}" onClick="{{d.go}}">{{d.n}}</button></sc-for></div></sc-if>')
# 2 顶部说明条
rep('<div class="ac-al i"><i>!</i><span>德迅安全卫士每个账号免费 3 台',
    '<sc-if value="{{isS}}" hint-placeholder-val="{{false}}"><div class="ac-al i"><i>!</i><span>{{sTip}}</span></div></sc-if><sc-if value="{{isG}}" hint-placeholder-val="{{true}}"><div class="ac-al i"><i>!</i><span>德迅安全卫士每个账号免费 3 台')
rep('核验到账后生效</span></div>\n', '核验到账后生效</span></div></sc-if>\n')
# 3 购买产品行
a = s.index('<div class="fl-row" style="border-top:0"><span>购买产品</span>')
b = s.index('</div></div>', a) + len('</div></div>')
old = s[a:b]
pa = old.index('<p class="kc-hint">'); pb = old.rindex('</p>') + 4
s = s[:a] + '<div class="fl-row" style="border-top:0"><span>购买产品</span><div><b style="font-weight:500">{{prodN}}</b><sc-if value="{{isG}}" hint-placeholder-val="{{true}}">' + old[pa:pb] + '</sc-if><sc-if value="{{isS}}" hint-placeholder-val="{{false}}"><p class="kc-hint">{{prodH}}</p></sc-if></div></div>' + s[b:]
n += 1
# 4 卫士的购买方式 / 期限 / 台数行只在卫士下显示；按规格产品显示 规格 / 时长 / 数量
rep('<div class="fl-row"><span>购买方式</span>', '<sc-if value="{{isG}}" hint-placeholder-val="{{true}}"><div class="fl-row"><span>购买方式</span>')
rep('<span class="pu-formula" style="margin-left:12px">{{qtyTip}}</span></div></div>\n',
    '<span class="pu-formula" style="margin-left:12px">{{qtyTip}}</span></div></div></sc-if>\n'
    '        <sc-if value="{{isS}}" hint-placeholder-val="{{false}}"><div class="fl-row"><span>规格</span><div><div class="fl-seg" style="flex-wrap:wrap"><sc-for list="{{specs}}" as="d" hint-placeholder-count="6"><button type="button" class="{{d.cls}}" onClick="{{d.go}}">{{d.n}}</button></sc-for></div><p class="kc-hint">{{specH}}</p></div></div>'
    '<div class="fl-row"><span>购买时长</span><div><div class="fl-seg"><sc-for list="{{sdurs}}" as="d" hint-placeholder-count="4"><button type="button" class="{{d.cls}}" onClick="{{d.go}}">{{d.n}}</button></sc-for></div><p class="kc-hint">{{durH}}</p></div></div>'
    '<div class="fl-row" style="border-bottom:1px solid #f2f4f8"><span>{{qtyL}}</span><div><span class="{{sStepCls}}"><button type="button" aria-label="减少" onClick="{{sDec}}">−</button><b>{{sQty}}</b><button type="button" aria-label="增加" onClick="{{sInc}}">+</button></span><span class="pu-formula" style="margin-left:12px">{{sQtyTip}}</span></div></div></sc-if>\n')
# 5 金额
rep('<div class="fl-tot"><div>商品合计<b>价格待定</b></div><div>代金券<b>暂无可用</b></div><div class="big">应付金额<b>价格待定</b></div></div>',
    '<div class="fl-tot"><div>商品合计<b>{{totT}}</b></div><div>代金券<b>暂无可用</b></div><div class="big">应付金额<b>{{totT}}</b></div></div>')
rep('<small>应付</small><b>价格待定</b>', '<small>应付</small><b>{{totT}}</b>')
# 6 开通后去向
rep('<p class="kc-hint">提交后在付款页查看收款账户；财务核验到账后自动开通</p>', '<p class="kc-hint">{{openH}}</p>')

# 7 逻辑
rep("    const __R = Object.assign({ nav }, {",
"""    /* pur3: 按规格购买的产品 */
    const SP = { ddos: ['DDoS 高防 IP', [['基础型', '100G 防御', 1999], ['专业型', '200G 防御', 2999], ['企业型', '300G 防御', 3999], ['商务型', '400G 防御', 5999], ['旗舰型-01', '600G 防御', 9999], ['旗舰型-02', '800G 防御', 19999], ['全力防护', '1000G 防御', 0]], '个', '元/月'],
      game: ['游戏盾', [['入门级', '在线峰数 200', 799], ['基础级', '在线峰数 300', 1399], ['专业级', '在线峰数 400', 1999], ['企业级', '在线峰数 600', 3999], ['尊享级', '在线峰数 1000', 6999], ['增强版', '旗舰 A–E 型', 0]], '个', '元/月'],
      ssl: ['SSL 证书', [['PositiveSSL', '单个域名', 68], ['PositiveSSL 多域名', '多个域名', 399], ['PositiveSSL 通配符', '单个域名 · 通配符', 888]], '张', '元/年'] };
    const __qp = __qs && __qs.get('p'); const __qv = __qs ? parseInt(__qs.get('v') || '0', 10) : 0;
    const pk = st.pk || (SP[__qp] ? __qp : 'host'); const isS = pk !== 'host', isG = !isS;
    const PD = [['卫士授权', 'host'], ['DDoS 高防 IP', 'ddos'], ['游戏盾', 'game'], ['SSL 证书', 'ssl']];
    const prods = PD.map(([n, k]) => ({ n, cls: k === pk ? 'on' : '', go: () => this.setState({ pk: k, sv: undefined, sq: 1, sd: undefined }) }));
    const SPk = SP[pk] || SP.ddos; const tiers = SPk[1];
    const svi = Math.max(0, Math.min(tiers.length - 1, st.sv !== undefined ? st.sv : (pk === __qp && !isNaN(__qv) ? __qv : 0)));
    const tier = tiers[svi]; const nego = isS && !tier[2];
    const specs = tiers.map(([n, d, pr], i) => ({ n: n + ' · ' + d, cls: i === svi ? 'on' : '', go: () => this.setState({ sv: i }) }));
    const SD = pk === 'ssl' ? [['1 年', 1], ['2 年', 2], ['3 年', 3]] : [['1 个月', 1], ['3 个月', 3], ['6 个月', 6], ['1 年', 12]];
    const sdn = st.sd && SD.find((d) => d[0] === st.sd) ? st.sd : SD[0][0]; const sm = SD.find((d) => d[0] === sdn)[1];
    const sdurs = SD.map(([n]) => ({ n, cls: n === sdn ? 'on' : '', go: () => this.setState({ sd: n }) }));
    const sQty = st.sq || 1; const money = (x) => '¥' + x.toLocaleString('en-US') + '.00';
    const sTot = tier[2] * sm * sQty;
    const sRows = [ROW([{ t: SPk[0], s: '新购' }, { t: tier[0], s: tier[1] }, sdn, { t: '开通日起 ' + sdn, s: '核验到账后开通', sc: '' }, { t: nego ? '面议' : money(tier[2]).replace('.00', '') + ' ' + SPk[3], c: 'ac-n m', td: 'num' }, { t: nego ? '面议' : money(sTot), c: 'ac-n', td: 'num' }], [])];
    const OPEN = { ddos: ['实例出现在 DDoS 高防 IP 实例列表，状态「待接入」，配置转发规则、把业务解析到高防 IP 后开始防护', '%DDOS%'], game: ['实例出现在游戏盾「应用接入」，状态「待接入」，接入 SDK 或配置转发后开始防护', '%GAME%'], ssl: ['证书出现在「我的产品」，状态「待提交资料」，完成域名验证后签发（通常 10 分钟到 1 个工作日）', '%SSL%'] }[pk] || ['', ''];
""".replace('%DDOS%', LIST['ddos']).replace('%GAME%', LIST['game']).replace('%SSL%', LIST['ssl'])
+ "    const __R = Object.assign({ nav }, {")

rep("      rows, cons, stepCls: blocked ? 'pu-step dis' : 'pu-step',",
"""      rows: isS ? sRows : rows, cons, stepCls: blocked ? 'pu-step dis' : 'pu-step',
      prods, isS, isG, specs, sdurs, sQty, sStepCls: nego ? 'pu-step dis' : 'pu-step',
      sDec: () => this.setState({ sq: Math.max(1, sQty - 1) }), sInc: () => this.setState({ sq: Math.min(20, sQty + 1) }),
      qtyL: pk === 'ssl' ? '购买张数' : '购买数量', sQtyTip: nego ? '该规格没有公开价格，请咨询专家定制' : '每个' + (pk === 'ssl' ? '证书' : '实例') + '单独计费、单独到期',
      specH: nego ? '没有公开价格，提交后由专家联系你，按方案报价' : '来自官网规格选择，可以在同一产品内更换规格；升配在实例上操作',
      durH: pk === 'ssl' ? '证书按年签发，到期前 30 天提醒重新签发' : '到期前 30 / 7 / 1 天提醒；到期后保留 7 天，服务降级，续费核验到账后恢复',
      sTip: SPk[0] + '：下单前需完成个人实名认证，对公转账付款，核验到账后开通。开通后' + OPEN[0],
      prodN: isS ? SPk[0] : '德迅安全卫士 · 主机授权',
      prodH: '按规格购买，规格从官网产品页带过来。其他产品请到对应产品页选择规格',
      openH: isS ? '提交后在付款页查看收款账户；核验到账后开通，订单状态变为「开通中」，开通失败会提示提交工单' : '提交后在付款页查看收款账户；财务核验到账后自动开通',
      totT: isS ? (nego ? '面议' : money(sTot)) : '价格待定',""")

rep("      modeT: isLap ?", "      modeT: isS ? SPk[0] : isLap ?")
rep("      subTxt: isPend ? '去付款' : '提交订单', subHref: isPend ? 'BillPayment.dc.html' : 'BillPayment.dc.html',",
    "      subTxt: nego ? '咨询专家' : isS ? '提交订单' : isPend ? '去付款' : '提交订单', subHref: nego ? '%C%' : 'BillPayment.dc.html',".replace('%C%', CONTACT))
rep("subCls: isPend ? 'kc-btn pri' : can ? 'kc-btn pri' : 'kc-btn pri dis' });",
    "subCls: isS ? (agree || nego ? 'kc-btn pri' : 'kc-btn pri dis') : isPend ? 'kc-btn pri' : can ? 'kc-btn pri' : 'kc-btn pri dis' });")
open(p, 'w', encoding='utf8').write(s)
print('ok', p, n, 'repo' if repo else 'canvas')
