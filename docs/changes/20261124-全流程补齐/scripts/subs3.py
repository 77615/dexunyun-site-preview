#!/usr/bin/env python3
"""AcctSubs：补订阅到期三态（即将到期 / 已到期 · 保留期 / 已释放）示例行与页签。幂等。"""
import sys, re
p = sys.argv[1]
s = open(p, encoding='utf8').read()
if 'subs3:' in s:
    print('already', p); sys.exit(0)
def href(rowid, idx=0):
    m = re.search(r"\['" + re.escape(rowid) + r"', \[\{ t: '[^']*', a: '([^']*)'", s)
    return m.group(1)
DD = href('ddos-1e8d07'); IDC = href('idc-wz-0193'); SC = href('scdn-001'); EY = href('eye-001')
m = re.search(r"\[\['续费', 'BillConfirm.dc.html'\], \['进入控制台', '([^']*)'\]\], 'att exp'\],\n      \['ssl-shop'", s)
DDC = m.group(1)
n = 0
def rep(a, b):
    global s, n
    assert s.count(a) == 1, (a[:90], s.count(a)); s = s.replace(a, b); n += 1
anchor = "      ['backup-01', "
new = (
"      /* subs3: 到期三态 */\n"
f"      ['ddos-5b21e0', [{{ t: '高防-005', a: '{DD}', s: 'DDoS 高防 IP · ddos-5b21e0' }}, {{ t: 'DX20251024006', a: 'BillOrderDetail.dc.html', s: '子订单 -01' }}, {{ t: '保底 30 Gbps', s: 'BGP 多线' }}, '—', NA, {{ t: '已到期 · 保留期', tag: 'err', s: '转发不断，防护已降到基础防护', sc: 'r' }}, {{ t: '2026-10-24', s: '保留至 10-31 · 之后释放', sc: 'r' }}], [['续费', 'BillConfirm.dc.html'], ['进入控制台', '{DDC}']], 'att exp hold'],\n"
f"      ['scdn-002', [{{ t: 'SCDN-002', a: '{SC}', s: 'SCDN · scdn-002' }}, {{ t: 'DX20251025001', a: 'BillOrderDetail.dc.html', s: '子订单 -01' }}, {{ t: '基础版 · 3 域名', s: '中国内地' }}, '2 / 3 域名', NA, {{ t: '已到期 · 保留期', tag: 'err', s: '10-28 起 CNAME 指回源站', sc: 'r' }}, {{ t: '2026-10-25', s: '保留至 11-01 · 之后释放', sc: 'r' }}], [['续费', 'BillConfirm.dc.html']], 'att exp hold'],\n"
f"      ['idc-wz-0150', [{{ t: 'web-old-01', a: '{IDC}', s: '服务器租用 · idc-wz-0150' }}, {{ t: 'DX20241020002', a: 'BillOrderDetail.dc.html', s: '子订单 -01' }}, {{ t: 'E5-2650×2 / 32G / 20M', s: '温州' }}, '—', {{ t: '未受保护', tag: 'warn', s: '原因：服务器已停机', sc: 'o' }}, {{ t: '到期停机', tag: 'err', s: '数据盘保留', sc: 'r' }}, {{ t: '2026-10-20', s: '保留至 10-27 · 今天释放', sc: 'r' }}], [['续费', 'BillConfirm.dc.html']], 'att exp hold sec'],\n"
f"      ['eye-002', [{{ t: '云眼-002', a: '{EY}', s: '德迅云眼 · eye-002' }}, {{ t: 'DX20250901003', a: 'BillOrderDetail.dc.html', s: '子订单 -01' }}, {{ t: '基础版 · 5 资产', s: '—' }}, '—', NA, {{ t: '已释放', tag: 'mut' }}, {{ t: '2026-09-01', s: '09-08 已释放 · 记录保留至 10-08', sc: 'm' }}], [['续费记录', 'BillOrders.dc.html'], ['重新购买', 'AcctPurchase.dc.html']], 'gone'],\n"
)
rep(anchor, new + anchor)
rep("{ t: '已过期', tag: 'mut' }, { t: '2026-10-01', s: '已释放', sc: 'm' }", "{ t: '已释放', tag: 'mut' }, { t: '2026-10-01', s: '10-08 已释放 · 记录保留至 11-07', sc: 'm' }")
rep("['即将到期', 'exp'], ['已过期', 'gone']]", "['即将到期', 'exp'], ['保留期', 'hold'], ['已释放', 'gone']]")
open(p, 'w', encoding='utf8').write(s)
print('ok', p, n)
