#!/usr/bin/env python3
"""按资源页（AcctSubs）顶部和「我的产品 · 按产品」统一（幂等，标记 sbu-v1，在 hier2.py 之后跑）。
77（2026-11-19）：「改成统一的」。
- 去掉容器顶部单独的胶囊条；卡片顶部一行：左边状态筛选（安静页签），右边「按产品 / 按资源」分段切换 + 权益转移、到期提醒设置
- 容器白底不再有灰色内底，表格的筛选栏、表格、分页不变
用法: subsuni.py AcctSubs.dc.html
"""
import sys, re

CSS = r'''
/* sbu-v1 按资源页顶部和按产品统一 */
.kc main.kc-main>.hier-box.sbu{border:0;box-shadow:0 1px 4px rgba(0,0,0,.05)}
.kc main.kc-main>.hier-box.sbu>.hier-in{padding:0;background:#fff}
.kc main.kc-main>.hier-box.sbu>.hier-in>section.kc-card{box-shadow:none!important;border:0!important}
.sbu .sbu-top{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:32px;padding:16px 20px;border-bottom:1px solid #e5e6eb}
.kc .sbu .sbu-top>.kc-tabs.kc-tabs{display:inline-flex!important;gap:4px!important;height:auto!important;margin:0!important;padding:0!important;background:none!important;border:0!important;box-shadow:none!important}
.kc .sbu .sbu-top>.kc-tabs>.kc-tab{display:inline-flex!important;align-items:center;gap:6px;height:28px!important;min-width:0!important;padding:0 10px!important;margin:0!important;border:0!important;border-radius:2px!important;background:transparent!important;box-shadow:none!important;font-size:12px!important;font-weight:400!important;color:rgba(0,0,0,.7)!important}
.kc .sbu .sbu-top>.kc-tabs>.kc-tab::before,.kc .sbu .sbu-top>.kc-tabs>.kc-tab::after{display:none!important}
.kc .sbu .sbu-top>.kc-tabs>.kc-tab:hover{background:#f7f8fb!important;color:rgba(0,0,0,.9)!important}
.kc .sbu .sbu-top>.kc-tabs>.kc-tab.on{background:#f2f4f8!important;color:rgba(0,0,0,.9)!important;font-weight:500!important}
.kc .sbu .sbu-top>.kc-tabs>.kc-tab>.kc-cnt{min-width:0!important;height:auto!important;padding:0!important;background:none!important;font-size:12px!important;font-weight:400!important;color:rgba(0,0,0,.5)!important}
.kc .sbu .sbu-top>.kc-tabs>.kc-tab>.kc-cnt.r{color:#f64041!important;font-weight:500!important}
.kc .sbu .kc-card>.lf-bar{padding:16px 20px 12px!important}
.sbu .sbu-tools{display:flex;align-items:center;gap:8px}
.sbu .sbu-tools>nav.pc-tabs{display:inline-flex;gap:2px;padding:2px;margin:0;border:0;background:#f2f3f5}
.sbu .sbu-tools>nav.pc-tabs>a{display:inline-flex;align-items:center;height:28px;padding:0 12px;border:0;border-radius:0;background:transparent;font-size:12px;font-weight:400;color:rgba(0,0,0,.6);text-decoration:none}
.sbu .sbu-tools>nav.pc-tabs>a:hover{color:rgba(0,0,0,.9)}
.sbu .sbu-tools>nav.pc-tabs>a.on{background:#fff;color:rgba(0,0,0,.9);font-weight:500;box-shadow:0 1px 2px rgba(0,0,0,.06)}
'''

for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    if 'sbu-v1' in s:
        print('skip', p); continue
    m = re.search(r'<div class="hier-box"><nav class="ia-tabs"[^>]*>(<a[^>]*>按产品</a><a[^>]*>按资源</a>)<div class="kc-btns tcl-r">(.*?)</div></nav><div class="hier-in">', s, re.S)
    assert m, 'hier-box nav'
    s = s[:m.start()] + '<div class="hier-box sbu"><div class="hier-in">' + s[m.end():]
    t = re.search(r'(<section class="kc-card">\s*)(<div class="kc-tabs" role="tablist">.*?</sc-for></div>)', s, re.S)
    assert t, 'kc-tabs'
    top = ('<div class="sbu-top">' + t.group(2) + '<div class="sbu-tools"><nav class="pc-tabs" aria-label="查看方式">' + m.group(1) + '</nav>' + m.group(2) + '</div></div>')
    s = s[:t.start(2)] + top + s[t.end(2):]
    i = s.index('<x-dc>'); j = s.index('</style>', i)
    s = s[:j] + CSS + s[j:]
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', p)
