# 卫士授权生命周期：账号与费用画布补丁（幂等）。用法：python3 t_acct2.py <project 目录>
import sys, os
D = sys.argv[1]
SECBUY = 'AcctPurchase.dc.html'
P = {
 'AcctProductDetail.dc.html': [
  ('<div class="ac-stats c3" style="margin:0"><div class="ac-st"><span>授权总数</span><b>52 <small>台</small></b></div><div class="ac-st r"><span>已使用</span><b>70 <small>台</small></b><em>使用率 134.6%</em></div><div class="ac-st r"><span>超出</span><b>18 <small>台</small></b><em>超出的主机不受保护<a href="BillConfirm.dc.html">扩容</a></em></div></div>',
   '<div class="ac-stats c3" style="margin:0"><div class="ac-st"><span>授权台数</span><b>57 <small>台</small></b><em>免费 3 + 已购 54</em></div><div class="ac-st r"><span>已用</span><b>57 <small>/ 57</small></b><em>已用满，新主机无法加入</em></div><div class="ac-st r"><span>宽限期剩余</span><b>4 <small>天</small></b><em>11-08 后 54 台停止检测<a href="BillConfirm.dc.html">续费</a></em></div></div>'),
  ('<span>1 项服务已到期 · 授权已用满（57 / 57）<em>续费和购买授权在下方对应服务里操作</em></span>',
   '<span>已购的 54 台授权 11-01 到期，宽限期到 11-08 · 授权已用满（57 / 57）<em>宽限期内只能续费，不能扩容；11-08 后超出免费 3 台的主机停止检测，数据保留 30 天</em></span>'),
  ("const svcs = [ROW([{ t: 'dx-guard-01', a: '#' }, '购买授权', { t: '54 台', s: '另有免费 3 台，共 57 / 57 已用满', sc: 'o' }, { t: '运行中', tag: 'ok' }, '2027-01-26'], [['扩容', 'BillConfirm.dc.html'], ['转移权益', 'AcctTransfer.dc.html']]),\n      ROW([{ t: 'dx-guard-02', a: '#' }, '购买授权', '2 台', { t: '已到期 · 保留中', tag: 'err' }, { t: '2026-10-25', s: '保留至 11-08', sc: 'r' }], [['续费', 'BillConfirm.dc.html']])];",
   "const svcs = [ROW([{ t: 'dx-guard-01', a: '#' }, '购买授权', { t: '54 台', s: '另有免费 3 台，共 57 / 57 已用满', sc: 'o' }, { t: '宽限期', tag: 'err' }, { t: '2026-11-01', s: '宽限至 11-08', sc: 'r' }], [['续费', 'BillConfirm.dc.html']])];"),
  ("const ods = [['DX20261007003', '扩容', '授权 +25 台', ['已完成', 'ok'], '¥25.00'], ['DX20260801004', '续费', 'dx-guard-02 续费 3 个月', ['已完成', 'ok'], '¥995.00'], ['DX20260412002', '扩容', '授权 +10 台', ['已完成', 'ok'], '¥990.00'], ['DX20260126001', '新购', '授权 20 台 · 1 年', ['已完成', 'ok'], '¥3,980.00']]",
   "const ods = [['DX20260412002', '扩容', '授权 +4 台 · 折算至 2026-11-01', ['已完成', 'ok'], '单价待定'], ['DX20251025002', '新购', '授权 50 台 · 1 年', ['已完成', 'ok'], '单价待定']]"),
 ],
 'AcctSubs.dc.html': [
  ("{ t: '已到期 · 保留中', tag: 'err' }, { t: '2026-10-25', s: '保留至 11-08', sc: 'r' }], [['续费', 'BillConfirm.dc.html'], ['扩容', 'BillConfirm.dc.html'], ['进入控制台', SECH]], 'att exp lic sec']",
   "{ t: '宽限期', tag: 'err' }, { t: '2026-11-01', s: '宽限至 11-08', sc: 'r' }], [['续费', 'BillConfirm.dc.html'], ['进入控制台', SECH]], 'att exp lic sec']"),
 ],
 'BillConfirm.dc.html': [
  ('续费从各资源的当前到期日起算；已到期资源在保留期内续费，防护立即恢复',
   '续费从各资源的当前到期日起算；已到期资源在保留期内续费，核验到账后恢复。德迅安全卫士授权续费时可以减少台数，减少的部分从当前到期日起停止检测'),
 ],
 'AcctPurchase.dc.html': [
  ('每个账号免费 3 台，当前已用满（57 / 57）。买几台就能多加几台主机；只数台数，不绑定 IP 和设备，换机器时删掉旧主机再加新主机即可。德迅云服务器随服务器赠送，不占授权。</p>',
   '每个账号免费 3 台，当前已用满（57 / 57）。买几台就能多加几台主机；只数台数，不绑定 IP 和设备，换机器时删掉旧主机再加新主机即可。德迅云服务器随服务器赠送，不占授权。</p><div class="ac-al e" style="margin:12px 0 0"><i>!</i><span>你已有 54 台已购授权，11-01 到期，现在处于宽限期（到 11-08）：宽限期内不能扩容，请先<a href="BillConfirm.dc.html">续费</a>。扩容会并入现有授权，按剩余天数折算价格，到期日不变；剩余不足 30 天时也请先续费。没有已购授权时，这里是新购，需要选择服务期限。</span></div>'),
 ],
 'Notifications.dc.html': [
  ("'德迅安全卫士 dx-guard-01 已到期', '资源保留至 11-08，续费后恢复防护', '10-25'",
   "'德迅安全卫士已购授权 11-01 到期', '宽限期到 11-08，之后超出免费 3 台的 54 台主机停止检测；续费核验到账后恢复', '11-01'"),
 ],
}
for fn, reps in P.items():
    f = os.path.join(D, fn); t = open(f, encoding='utf-8').read(); o = t
    for a, b in reps:
        if b not in t:
            if a not in t: print('MISS', fn, a[:40])
            t = t.replace(a, b)
    if t != o: open(f, 'w', encoding='utf-8').write(t); print('patched', fn)
