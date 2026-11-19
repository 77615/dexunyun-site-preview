#!/usr/bin/env python3
"""费用、企业分组页的页签和背景和「我的产品」同步（幂等，标记 bsy-v1，在 hier2.py 之后跑）。
77（2026-11-19）：「费用、企业这两页的标签样式和背景也同步一下」。
- 二级页签（概览 / 订单 / 付款… ；企业信息 / 成员…）：胶囊改成分段切换（灰色轨道，选中白底），同「按产品 / 按资源」
- 卡片里的状态页签：灰底分段改成安静页签（选中浅灰底，未选中无底无框），同「我的产品」状态筛选
- 背景：容器去掉描边改成浅阴影；只有一张表格的页面（订单、发票、合同）容器内全白，表格卡片并进容器，同「按资源」；
  有多块内容的页面保留浅灰内底，同「我的产品」卡片视图的分组底
用法: billsync.py X.dc.html [...]
"""
import sys, re

ONE = {'BillOrders', 'BillInvoice', 'BillContract'}

CSS = r'''
/* bsy-v1 费用、企业页签和背景同步「我的产品」 */
.kc main.kc-main>.hier-box.bsy{border:0;box-shadow:0 1px 4px rgba(0,0,0,.05)}
.kc main.kc-main>.hier-box.bsy>nav.ia-tabs.ia-tabs{padding:16px 20px!important;border-bottom:1px solid #e5e6eb!important;gap:8px!important}
.kc .kc-main>.hier-box.bsy>nav.ia-tabs>.bsy-seg{display:inline-flex;gap:2px;padding:2px;background:#f2f3f5}
.kc .kc-main>.hier-box.bsy>nav.ia-tabs>.bsy-seg>a{display:inline-flex;align-items:center;height:28px!important;padding:0 14px!important;margin:0!important;border:0!important;border-radius:0!important;background:transparent!important;box-shadow:none!important;font-size:12px!important;font-weight:400!important;color:rgba(0,0,0,.6)!important;text-decoration:none}
.kc .kc-main>.hier-box.bsy>nav.ia-tabs>.bsy-seg>a::before,.kc .kc-main>.hier-box.bsy>nav.ia-tabs>.bsy-seg>a::after{display:none!important}
.kc .kc-main>.hier-box.bsy>nav.ia-tabs>.bsy-seg>a:hover{color:rgba(0,0,0,.9)!important}
.kc .kc-main>.hier-box.bsy>nav.ia-tabs>.bsy-seg>a.on{background:#fff!important;color:rgba(0,0,0,.9)!important;font-weight:500!important;box-shadow:0 1px 2px rgba(0,0,0,.06)!important}
.kc main.kc-main>.hier-box.bsy>.hier-in .kc-card>.kc-tabs.kc-tabs.kc-tabs{gap:4px!important;margin:16px 20px 0!important;padding:0!important;background:none!important}
.kc main.kc-main>.hier-box.bsy>.hier-in .kc-card>.kc-tabs.kc-tabs>.kc-tab.kc-tab{height:28px!important;padding:0 10px!important;border-radius:2px!important;font-size:12px!important;color:rgba(0,0,0,.7)!important;background:transparent!important;box-shadow:none!important}
.kc main.kc-main>.hier-box.bsy>.hier-in .kc-card>.kc-tabs.kc-tabs>.kc-tab.kc-tab:hover{background:#f7f8fb!important;color:rgba(0,0,0,.9)!important}
.kc main.kc-main>.hier-box.bsy>.hier-in .kc-card>.kc-tabs.kc-tabs>.kc-tab.kc-tab.on{background:#f2f4f8!important;color:rgba(0,0,0,.9)!important;font-weight:500!important;box-shadow:none!important}
.kc main.kc-main>.hier-box.bsy>.hier-in .kc-card>.kc-tabs.kc-tabs>.kc-tab>.kc-cnt{color:rgba(0,0,0,.5)!important}
.kc main.kc-main>.hier-box.bsy>.hier-in .kc-card>.kc-tabs.kc-tabs>.kc-tab>.kc-cnt.r{color:#f64041!important;font-weight:500!important}
.kc main.kc-main>.hier-box.bsy .kc-card>.lf-bar{padding-left:20px!important;padding-right:20px!important}
.kc main.kc-main>.hier-box.bsy.bsy-one>.hier-in{padding:0;background:#fff}
.kc main.kc-main>.hier-box.bsy.bsy-one>.hier-in>section.kc-card{box-shadow:none!important;border:0!important}
'''

for p in sys.argv[1:]:
    name = p.rsplit('/', 1)[-1].replace('.dc.html', '')
    s = open(p, encoding='utf-8').read()
    if 'bsy-v1' in s:
        print('skip', name); continue
    m = re.search(r'<div class="hier-box"><nav class="ia-tabs"([^>]*)>((?:<a[^>]*>[^<]*</a>)+)', s)
    assert m, name
    cls = 'hier-box bsy' + (' bsy-one' if name in ONE else '')
    s = s[:m.start()] + '<div class="' + cls + '"><nav class="ia-tabs"' + m.group(1) + '><span class="bsy-seg">' + m.group(2) + '</span>' + s[m.end():]
    i = s.index('<x-dc>'); j = s.index('</style>', i)
    s = s[:j] + CSS + s[j:]
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', name)
