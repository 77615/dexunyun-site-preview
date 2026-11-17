#!/usr/bin/env python3
"""控制台总览改成腾讯式布局（幂等）。
- 去掉左侧菜单（只在 ConsoleHome）
- 欢迎语下方加横排页签：总览 / 我的产品 / 费用 / 企业
- 顶部账号条 + 右栏「费用信息」合并成右上账户卡（内容不删）
- 企业卡改紧凑，右栏不再吸顶
用法: tcl.py ConsoleHome.dc.html  (原地改写)
"""
import re, sys

p = sys.argv[1]
s = open(p, encoding='utf-8').read()
if 'tcl-v1' in s:
    print('already applied'); sys.exit(0)
ann = 'data-annotation-id=' in s
A = (lambda k: f' data-annotation-id="{k}"') if ann else (lambda k: '')

# 1 去左侧菜单
s, n = re.subn(r'<input type="checkbox" id="kcf-ConsoleHome".*?(?=<main data-pg="ConsoleHome")', '', s, count=1, flags=re.S)
assert n == 1, 'sidebar'

# 2 页签
TABS = ('<nav class="tcl-tabs" aria-label="控制台分区"><a class="on" aria-current="page" href="ConsoleHome.dc.html">总览</a>'
        '<a href="AcctProducts.dc.html">我的产品</a><a href="BillOverview.dc.html">费用</a><a href="OrgInfo.dc.html">企业</a></nav>')
s, n = re.subn(r'(<main data-pg="ConsoleHome" class="kc-main">\s*<div class="kc-hd">.*?<div class="kc-btns"></div>\s*</div>)',
               lambda m: m.group(1) + '\n      ' + TABS, s, count=1, flags=re.S)
assert n == 1, 'tabs'

# 3 取出账号条
m = re.search(r'\n[^\n]*<div class="h8-box h8-id"[^\n]*\n', s)
assert m, 'h8-id'
idb = m.group(0)
s = s.replace(idb, '\n', 1)
who = re.search(r'<div class="h8-who">(.*?)</div>', idb, flags=re.S).group(1)

# 4 取出费用信息 section
m = re.search(r'<section class="h8-sec"><div class="h8-st"><h2[^>]*>费用信息</h2>.*?</section>', s, flags=re.S)
assert m, 'fee'
fee = m.group(0)
hint = re.search(r'<span class="note kc-tipai">(.*?)</span></span>', fee, flags=re.S).group(1)
bars = re.findall(r'<div class="bar( cur)?" style="height:([\d.]+)%" title="([^"]+)"><span>([^<]+)</span></div>', fee)
upd = re.search(r'<header>近半年付款 <small>([^<]+)</small>', fee).group(1)
mini = ''.join(f'<i class="{"cur" if c else ""}" style="height:{h}%" title="{t}"><em>{"本月" if c else lab}</em></i>' for c, h, t, lab in bars)
ARR = '<svg class="rx" width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.1717 12.0007L8.22192 7.05093L9.63614 5.63672L16.0001 12.0007L9.63614 18.3646L8.22192 16.9504L13.1717 12.0007Z"></path></svg>'
CARD = f'''<section class="h8-sec tcl-acct"{A('home-account')}>
          <div class="tcl-who"><div class="h8-av">德</div><div class="h8-who">{who}</div></div>
          <div class="kc-tipai tcl-hint">{hint}</div>
          <div class="tcl-fee"{A('home-fees')}>
            <div class="tcl-lh"><label>账户余额（元）</label><nav><a href="BillOrders.dc.html">查订单</a><a href="BillBalance.dc.html">收支明细</a><a href="BillInvoice.dc.html">发票</a><a href="BillOverview.dc.html">账务概览</a></nav></div>
            <div class="tcl-big"><strong>1,260<small>.00</small></strong><a href="BillOverview.dc.html">充值</a></div>
            <div class="tcl-pay"><div class="tcl-pl"><label>待付款（元）<span>1 笔</span></label><strong>320<small>.00</small></strong><div class="kc-btns"><a class="kc-btn pri sm" href="BillPayment.dc.html">去付款</a><a class="kc-btn sm" href="BillInvoiceApply.dc.html">申请开票</a></div></div>
              <div class="tcl-mc"><header>近半年付款<small>{upd}</small></header><div class="tcl-bars">{mini}</div></div></div>
            <dl class="tcl-kv"><div><dt>本月已付款（元）</dt><dd>1,305.00</dd></div><div><dt>可开票金额（元）</dt><dd>1,169.84</dd></div>
              <div><dt><i class="h8-dot"></i>到期与即将到期</dt><dd><a href="AcctSubs.dc.html?ft=exp">5</a> 项</dd></div><div><dt>未关闭工单</dt><dd><a href="SupTickets.dc.html">4</a> 个</dd></div></dl>
          </div>
        </section>'''
s = s.replace(fee, CARD, 1)

# 5 原账号条上的 data-annotation-id 已随元素移走；保证其余 id 不重复
CSS = '''<style>/* tcl-v1 控制台总览 · 腾讯式布局 */
.kc .kc-body>.kc-main{flex:1 1 100%;min-width:0;margin-left:0!important}
.kc main.kc-main>.kc-hd.kc-hd{padding:28px 24px 0!important}
.kc main.kc-main>.kc-hd.kc-hd .kc-h1{font-size:22px!important;line-height:32px!important}
.kc .kc-main>nav.tcl-tabs{margin:12px 24px 20px!important}
.tcl-tabs{display:flex;gap:32px;height:48px;align-items:flex-end;border-bottom:1px solid rgba(0,0,0,.06)}
.tcl-tabs a{position:relative;display:flex;align-items:center;height:40px;font-size:14px;color:rgba(0,0,0,.7);text-decoration:none;transition:color .15s}
.tcl-tabs a:hover{color:rgba(0,0,0,.9)}
.tcl-tabs a.on{color:rgba(0,0,0,.9);font-weight:600}
.tcl-tabs a.on::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:rgba(0,0,0,.9)}
.kc .kc-main>.h8{margin:0 24px 32px!important}
.kc .h8-cols{grid-template-columns:minmax(0,1fr) 440px!important}
.kc .h8-rl{position:static!important}
.tcl-acct{padding:24px!important}
.tcl-who{display:flex;align-items:center;gap:14px}
.tcl-who .h8-av{width:44px;height:44px;flex:none;border-radius:50%;display:grid;place-items:center;font-size:16px;background:#e3ecff;color:#1664ff}
.tcl-who .h8-who{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px}
.tcl-who .h8-who b{font-size:16px;font-weight:600;color:rgba(0,0,0,.9)}
.tcl-who .h8-who p{flex-basis:100%;margin:0;font-size:12px;color:rgba(0,0,0,.5)}
.tcl-hint{display:flex!important;margin:16px 0 0!important;border-radius:18px;padding:8px 14px!important;font-size:12px}
.tcl-fee{margin-top:20px}
.tcl-lh{display:flex;align-items:center;justify-content:space-between;font-size:12px;color:rgba(0,0,0,.5)}
.tcl-lh nav{display:flex}
.tcl-lh nav a{padding:0 10px;color:rgba(0,0,0,.7);text-decoration:none;border-left:1px solid #e6e9ef;line-height:12px}
.tcl-lh nav a:first-child{border-left:0}
.tcl-lh nav a:last-child{padding-right:0}
.tcl-lh nav a:hover{color:#1664ff}
.tcl-big{display:flex;align-items:baseline;gap:16px;margin:6px 0 4px}
.tcl-big strong,.tcl-pay strong{font-family:Barlow,Inter,"PingFang SC",sans-serif;font-variant-numeric:tabular-nums;font-size:28px;line-height:36px;font-weight:600;color:rgba(0,0,0,.9)}
.tcl-big strong small,.tcl-pay strong small{font-size:20px}
.tcl-big a{font-size:14px;color:#1664ff;text-decoration:none}
.tcl-pay{display:grid;grid-template-columns:150px 1fr;gap:24px;align-items:end;margin-top:16px;padding-top:16px;border-top:1px solid #e9ecf1}
.tcl-pl label{display:block;font-size:12px;color:rgba(0,0,0,.5)}
.tcl-pl label span{margin-left:6px;color:#ff7d00}
.tcl-pay strong{font-size:22px;line-height:32px;display:block;margin:4px 0 10px}
.tcl-pay strong small{font-size:16px}
.tcl-pl .kc-btns{display:flex;gap:8px}
.tcl-mc header{display:flex;white-space:nowrap;gap:8px;justify-content:space-between;font-size:12px;color:rgba(0,0,0,.5);margin-bottom:6px}
.tcl-mc header small{font-size:11px;color:rgba(0,0,0,.3)}
.tcl-bars{position:relative;display:flex;align-items:flex-end;gap:10px;height:64px;padding-bottom:18px;border-bottom:1px solid #e9ecf1}
.tcl-bars i{position:relative;flex:1;background:#b4ceff;min-height:2px}
.tcl-bars i:hover{background:#1664ff}
.tcl-bars i.cur{background:#1664ff}
.tcl-bars em{position:absolute;left:50%;bottom:-19px;transform:translateX(-50%);font-style:normal;font-size:11px;color:rgba(0,0,0,.5);white-space:nowrap}
.tcl-kv{display:grid;grid-template-columns:1fr 1fr;gap:12px 24px;margin:18px 0 0}
.tcl-kv div{display:flex;justify-content:space-between;align-items:center;font-size:12px}
.tcl-kv dt{color:rgba(0,0,0,.5);display:flex;align-items:center;gap:6px}
.tcl-kv dd{margin:0;color:rgba(0,0,0,.9);font-family:Barlow,Inter,"PingFang SC",sans-serif;font-variant-numeric:tabular-nums;font-size:14px;font-weight:500}
.tcl-kv dd a{color:#1664ff;text-decoration:none}
.kc .h8-rl .h8-g3{grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:12px}
.kc .h8-rl .h8-ac{flex-direction:column;align-items:flex-start;gap:10px;padding:14px 16px!important}
.kc .h8-rl .h8-tip.lu b{white-space:nowrap}
.kc .h8-rl .h8-ac .kc-btn{height:28px;padding:0 12px;font-size:12px}
</style>
'''
i = s.index('<x-dc>'); j = s.index('</style>', i)
CSSR = CSS.replace('<style>', '').replace('</style>\n', '')
s = s[:j] + '\n' + CSSR + s[j:]
open(p, 'w', encoding='utf-8').write(s)
print('ok', 'annotations' if ann else '')
