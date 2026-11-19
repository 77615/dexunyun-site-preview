#!/usr/bin/env python3
"""分组页页签分层级（同「我的产品」卡片版，幂等，标记 hier-v1）。
一级：页面下划线页签（不变）
二级：胶囊页签放进白色容器顶部（白底条 + 细分隔线）；下一个元素是卡片时和卡片连成一个容器
三级：卡片顶部的状态页签改成灰底分段筛选
用法: hier.py X.dc.html [...]
"""
import sys, os

CSS = '''
/* hier-v1 页签分层级：二级胶囊在容器顶部，三级分段筛选 */
.kc main.kc-main:has(>nav.tcl-top)>nav.ia-tabs.ia-tabs{margin-bottom:0!important;padding:16px 20px!important;background:#fff!important;border-bottom:1px solid #f0f2f5!important;box-shadow:0 1px 4px rgba(0,0,0,.05)!important;position:relative;z-index:1}
.kc main.kc-main:has(>nav.tcl-top)>nav.ia-tabs+*{margin-top:16px!important}
.kc main.kc-main:has(>nav.tcl-top)>nav.ia-tabs+section.kc-card{margin-top:0!important;border-top:0!important;box-shadow:0 2px 4px rgba(0,0,0,.05)!important}
.kc main.kc-main:has(>nav.tcl-top) .kc-card>.kc-tabs.kc-tabs{display:inline-flex!important;gap:0!important;height:auto!important;margin:16px 16px 0!important;padding:2px!important;background:#f2f3f5!important;border:0!important;box-shadow:none!important}
.kc main.kc-main:has(>nav.tcl-top) .kc-card>.kc-tabs>.kc-tab{display:inline-flex!important;align-items:center;gap:6px;height:28px!important;min-width:0!important;padding:0 14px!important;margin:0!important;border:0!important;border-radius:0!important;background:transparent!important;box-shadow:none!important;font-size:13px!important;font-weight:400!important;color:rgba(0,0,0,.6)!important}
.kc main.kc-main:has(>nav.tcl-top) .kc-card>.kc-tabs>.kc-tab::before,.kc main.kc-main:has(>nav.tcl-top) .kc-card>.kc-tabs>.kc-tab::after{display:none!important}
.kc main.kc-main:has(>nav.tcl-top) .kc-card>.kc-tabs>.kc-tab:hover{color:rgba(0,0,0,.9)!important}
.kc main.kc-main:has(>nav.tcl-top) .kc-card>.kc-tabs>.kc-tab.on{background:#fff!important;color:rgba(0,0,0,.9)!important;font-weight:500!important;box-shadow:0 1px 2px rgba(0,0,0,.08)!important}
.kc main.kc-main:has(>nav.tcl-top) .kc-card>.kc-tabs>.kc-tab>.kc-cnt{min-width:0!important;height:auto!important;padding:0!important;background:none!important;font-size:12px!important;font-weight:400!important;color:rgba(0,0,0,.4)!important}
.kc main.kc-main:has(>nav.tcl-top) .kc-card>.kc-tabs>.kc-tab>.kc-cnt.r{color:#f53f3f!important}
'''

for p in sys.argv[1:]:
    name = os.path.basename(p)
    s = open(p, encoding='utf-8').read()
    if 'hier-v1' in s:
        print('skip', name); continue
    if '<nav class="ia-tabs"' not in s or 'tcl-tabs tcl-top' not in s:
        print('NOT GROUP PAGE', name); continue
    i = s.index('<x-dc>'); j = s.index('</style>', i)
    s = s[:j] + CSS + s[j:]
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', name)
