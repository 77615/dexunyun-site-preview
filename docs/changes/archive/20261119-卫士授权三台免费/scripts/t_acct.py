# 卫士授权三台免费：账号与费用画布 + 服务器画布补丁（幂等）。用法：python3 t_acct.py <目录>
import sys, glob, os, re
D = sys.argv[1]
F = {
'AcctPurchase.dc.html': [
 ('<div class="fl-row"><span>版本</span><div><div class="pv-row"><div class="fl-seg"><button type="button" class="on" aria-pressed="true">企业版</button><button type="button" class="pv-dis" disabled="" title="当前已开通个人版">个人版（当前）</button></div><button type="button" class="pv-x" onClick="{{pvTog}}"><i class="pv-ic"></i>版本功能对比</button></div><p class="pv-sum">包含个人版全部防护能力，另有 <em>高级威胁狩猎</em> · 日志留存 <em>180 天</em> · <em>AI 辅助告警研判</em> · 7×24 小时专家支持 · 每份 52 台授权 / 年</p></div></div>',
  '<div class="fl-row"><span>授权</span><div><p class="pv-sum" style="margin:0">每个账号免费 3 台，当前已用满（57 / 57）。买几台就能多加几台主机；只数台数，不绑定 IP 和设备，换机器时删掉旧主机再加新主机即可。德迅云服务器随服务器赠送，不占授权。</p></div></div>'),
 ('<span>套餐份数</span><div><span class="pu-step"><button type="button" aria-label="减少" onClick="{{dec}}">−</button><b>{{qty}}</b><button type="button" aria-label="增加" onClick="{{inc}}">+</button></span><span class="pu-formula" style="margin-left:12px">本次共 {{hosts}} 台 · 1–20 份</span>',
  '<span>购买台数</span><div><span class="pu-step"><button type="button" aria-label="减少" onClick="{{dec}}">−</button><b>{{qty}}</b><button type="button" aria-label="增加" onClick="{{inc}}">+</button></span><span class="pu-formula" style="margin-left:12px">购买后共 {{hosts}} 台（含免费 3 台）</span>'),
 ('<div class="pu-formula">年度单价 ¥3,980.00 × {{m}} 个月 ÷ 12 × {{qty}} 份</div>', '<div class="pu-formula">单价待定（元 / 台 / 年）× {{m}} 个月 ÷ 12 × {{qty}} 台</div>'),
 ('<small>应付</small><b>¥{{pay}}</b>', '<small>应付</small><b>{{pay}}</b>'),
 ("const qty = st.q || 1;", "const qty = st.q || 5;"),
 ("const pay = (3980 * m / 12 * qty).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });", "const pay = '价格待定';"),
 ("hosts: qty * 52, pay, dec: () => this.setState({ q: Math.max(1, qty - 1) }), inc: () => this.setState({ q: Math.min(20, qty + 1) })",
  "hosts: 57 + qty, pay, dec: () => this.setState({ q: Math.max(1, qty - 1) }), inc: () => this.setState({ q: Math.min(999, qty + 1) })"),
],
'AcctProducts.dc.html': [
 ("'企业版 · 50 台', '主机安全', '授权已到期，数据保留到 11 月 8 日。目前接入 68 台主机，超出授权 18 台。'",
  "'免费 3 台 + 已购 54 台', '主机安全', '已购授权已到期，数据保留到 11 月 8 日。授权 57 台已用满，新主机无法加入；另有 7 台德迅云服务器随服务器赠送。'"),
 ("'企业版 · 50 台', { t: '68 / 50 台', c: 'r', s: '超出 18 台', sc: 'r' }", "'免费 3 + 已购 54 台', { t: '57 / 57 台', c: 'o', s: '已用满', sc: 'o' }"),
],
'AcctProductDetail.dc.html': [
 ('<span>1 项服务已到期 · 授权超出 18 台<em>续费和扩容在下方对应服务里操作</em></span>', '<span>1 项服务已到期 · 授权已用满（57 / 57）<em>续费和购买授权在下方对应服务里操作</em></span>'),
 ("'企业版 · 全局', { t: '68 / 50 台', c: 'r', s: '超出 18 台', sc: 'r' }", "'购买授权', { t: '54 台', s: '另有免费 3 台，共 57 / 57 已用满', sc: 'o' }"),
 ("ROW([{ t: 'dx-guard-02', a: '#' }, '企业版 · 全局', '2 / 2 台'", "ROW([{ t: 'dx-guard-02', a: '#' }, '购买授权', '2 台'"),
 ("'新购', '企业版 1 份 · 1 年'", "'新购', '授权 20 台 · 1 年'"),
],
'AcctSubs.dc.html': [
 ("s: '德迅安全卫士 · 企业版' }", "s: '德迅安全卫士 · 授权' }"),
 ("{ t: '企业版 · 50 台', s: '全局' }, { t: '68 / 50 台', c: 'r', s: '超出 18 台', sc: 'r' }", "{ t: '已购 54 台', s: '另免费 3 台' }, { t: '57 / 57 台', c: 'o', s: '已用满', sc: 'o' }"),
],
'AcctUsage.dc.html': [
 ("['超授权', '1', 'over', '超出部分不受保护']", "['已用满', '1', 'over', '新增资源无法加入']"),
 ("(f === 'over' ? '超授权' : '接近上限')", "(f === 'over' ? '已用满' : '接近上限')"),
 ('<span>dx-guard-01 授权超出 18 台：超出的主机不会安装防护<em>扩容后立即生效，按剩余天数补差价</em></span>', '<span>德迅安全卫士授权已用满（57 / 57）：新主机无法加入<em>删除不用的主机，或购买授权，付款核验到账后立即生效</em></span>'),
 ("{ t: '德迅安全卫士', s: '企业版' }, { t: '50 台', c: 'ac-n' }, { t: '68 台', c: 'ac-n r' }, { t: '136%', bar: 100, bc: 'r', c: 'r' }, { t: '超出 18 台', tag: 'err' }], [['扩容', 'BillConfirm.dc.html']]",
  "{ t: '德迅安全卫士', s: '免费 3 + 已购 54' }, { t: '57 台', c: 'ac-n' }, { t: '57 台', c: 'ac-n' }, { t: '100%', bar: 100, bc: 'o', c: 'o' }, { t: '已用满', tag: 'warn' }], [['购买授权', 'AcctPurchase.dc.html']]"),
 ('付款核验到账后立即生效</em></span><a class="kc-btn pri sm" href="BillConfirm.dc.html">扩容</a>', '付款核验到账后立即生效</em></span><a class="kc-btn pri sm" href="AcctPurchase.dc.html">购买授权</a>'),
],
'ConsoleHome.dc.html': [
 ("'未受保护', '未授权', 'app-07', '德迅安全卫士', '待处理', 'mut', '000000000000', '—', '11-03', '11-03 10:00', '绑定授权',",
  "'未受保护', '授权已用满', 'app-07', '德迅安全卫士', '待处理', 'mut', '000000000000', '—', '11-03', '11-03 10:00', '购买授权',"),
 ("'授权已用完，这台主机没有绑定授权。', '客户端在线但不做检测。', ['在授权管理里给它绑定授权，或扩容授权']",
  "'授权已用满（57 / 57），这台主机装好了客户端但没能加入。', '不做检测，出事也不会告警。', ['删除不用的主机，会立刻空出名额', '或购买授权，到账后自动加入']"),
],
'IdcServerDetail.dc.html': [
 ("['AI 研判', '自动分析告警真假、给出处置建议（企业版）', 'base']", "['AI 研判', '自动分析告警真假、给出处置建议', 'base']"),
 ("tp: n === 'AI 研判' ? '企业版' : t === 'base'", "tp: t === 'base'"),
 ("{ n: 'AI 研判', d: '企业版能力，自动分析告警真假'", "{ n: 'AI 研判', d: '自动分析告警真假'"),
 ("['app-07', '10.0.2.27', '未授权']", "['app-07', '10.0.2.27', '授权已用满']"),
 ('<h3 class="ss-h">防护功能<span class="kc-cnt">{{plgOn}}/7</span></h3>', '<h3 class="ss-h">防护功能<span class="kc-cnt">{{plgOn}}/7</span><span class="kc-sub" style="margin-left:12px;font-weight:400">德迅云服务器随服务器赠送德迅安全卫士，不占授权台数</span></h3>'),
],
}
PV = re.compile(r'\n  <sc-if value="\{\{pvEx\}\}".*?</aside></sc-if>', re.S)
for f in sorted(glob.glob(os.path.join(D, '*.dc.html'))):
    b = os.path.basename(f)
    if b not in F: continue
    t0 = t = open(f, encoding='utf8').read()
    for o, n in F[b]:
        if o in t: t = t.replace(o, n); print('ok ', b, o[:50])
        elif n not in t: print('MISS', b, o[:60])
    if b == 'AcctPurchase.dc.html': t, k = PV.subn('', t); print('pv drawer removed', k)
    if t != t0: open(f, 'w', encoding='utf8').write(t)
