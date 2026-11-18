#!/usr/bin/env python3
"""分组页：二级胶囊页签和下面整块内容包进同一个容器（幂等，标记 hier-v2，需先跑 hier.py）。
77（2026-11-18）：费用、企业页胶囊条下面不止一张卡片时，胶囊和内容没有关联、没有层级。
结构：div.hier-box（白底细边框）> nav.ia-tabs（容器顶部白条）+ div.hier-in（浅灰内底 #f5f6f8，内容卡片放在里面）
同「我的产品」卡片版：容器顶部胶囊 → 灰色内底 → 白色卡片。
用法: hier2.py X.dc.html [...]
"""
import sys, os

CSS = '''
/* hier-v2 胶囊页签和内容同一个容器 */
.kc main.kc-main>.hier-box{margin:0 24px!important;background:#fff;border:1px solid #e9ecf1;box-shadow:0 1px 4px rgba(0,0,0,.05)}
.kc main.kc-main>.hier-box>nav.ia-tabs.ia-tabs{margin:0!important;padding:16px 20px!important;background:#fff!important;border:0!important;border-bottom:1px solid #f0f2f5!important;box-shadow:none!important;animation:none!important}
.kc main.kc-main>.hier-box>.hier-in{display:block;padding:16px;background:#f5f6f8}
.kc main.kc-main>.hier-box>.hier-in>*{margin-left:0!important;margin-right:0!important;margin-top:0!important;margin-bottom:0!important;animation:none!important}
.kc main.kc-main>.hier-box>.hier-in>*+*{margin-top:16px!important}
.kc main.kc-main>.hier-box>.hier-in section.kc-card{border:0!important;box-shadow:none!important}
.kc main.kc-main>.hier-box>.hier-in .kc-card>.kc-tabs.kc-tabs{display:inline-flex!important;gap:0!important;height:auto!important;margin:16px 16px 0!important;padding:2px!important;background:#f2f3f5!important;border:0!important;box-shadow:none!important}
.kc main.kc-main>.hier-box>.hier-in .kc-card>.kc-tabs>.kc-tab{display:inline-flex!important;align-items:center;gap:6px;height:28px!important;min-width:0!important;padding:0 14px!important;margin:0!important;border:0!important;border-radius:0!important;background:transparent!important;box-shadow:none!important;font-size:13px!important;font-weight:400!important;color:rgba(0,0,0,.6)!important}
.kc main.kc-main>.hier-box>.hier-in .kc-card>.kc-tabs>.kc-tab::before,.kc main.kc-main>.hier-box>.hier-in .kc-card>.kc-tabs>.kc-tab::after{display:none!important}
.kc main.kc-main>.hier-box>.hier-in .kc-card>.kc-tabs>.kc-tab.on{background:#fff!important;color:rgba(0,0,0,.9)!important;font-weight:500!important;box-shadow:0 1px 2px rgba(0,0,0,.08)!important}
.kc main.kc-main>.hier-box>.hier-in .kc-card>.kc-tabs>.kc-tab>.kc-cnt{min-width:0!important;height:auto!important;padding:0!important;background:none!important;font-size:12px!important;font-weight:400!important;color:rgba(0,0,0,.4)!important}
.kc main.kc-main>.hier-box>.hier-in .kc-card>.kc-tabs>.kc-tab>.kc-cnt.r{color:#f53f3f!important}
.kc main.kc-main>.hier-box>.hier-in>.b8{border-top:0!important;padding-top:0!important}
.kc .kc-main>.hier-box>nav.ia-tabs{display:flex;gap:8px!important}
.kc .kc-main>.hier-box>nav.ia-tabs>a{height:32px!important;padding:0 16px!important;margin:0!important;display:inline-flex;align-items:center;border:1px solid #e6e9ef!important;border-radius:16px!important;background:#fff!important;color:rgba(0,0,0,.7)!important;font-size:13px!important;font-weight:400!important;text-decoration:none;box-shadow:none!important}
.kc .kc-main>.hier-box>nav.ia-tabs>a::after,.kc .kc-main>.hier-box>nav.ia-tabs>a::before{display:none!important}
.kc .kc-main>.hier-box>nav.ia-tabs>a:hover{color:#1664ff!important;border-color:#c6d8ff!important}
.kc .kc-main>.hier-box>nav.ia-tabs>a.on{background:#e5ecff!important;border-color:#e5ecff!important;color:#1664ff!important;font-weight:500!important}
.kc .kc-main>.hier-box>nav.ia-tabs>.tcl-r{margin-left:auto;display:flex;gap:8px;align-items:center}
.kc .kc-main>.hier-box>nav.ia-tabs>.tcl-r>a.kc-btn{height:32px!important;padding:0 16px!important;margin:0!important;display:inline-flex!important;align-items:center;gap:6px;border:1px solid #d6dbe3!important;background:#fff!important;color:rgba(0,0,0,.9)!important;font-size:13px!important;border-radius:0!important}
.kc .kc-main>.hier-box>nav.ia-tabs>.tcl-r>a.kc-btn:hover{border-color:#1664ff!important;color:#1664ff!important}
'''

for p in sys.argv[1:]:
    name = os.path.basename(p)
    s = open(p, encoding='utf-8').read()
    if 'hier-v2' in s:
        print('skip', name); continue
    if s.count('<nav class="ia-tabs"') != 1 or 'hier-v1' not in s:
        print('NOT APPLICABLE', name); continue
    i = s.index('<nav class="ia-tabs"'); j = s.index('</nav>', i) + 6; k = s.index('</main>', j)
    s = s[:i] + '<div class="hier-box">' + s[i:j] + '<div class="hier-in">' + s[j:k] + '</div></div>' + s[k:]
    a = s.index('<x-dc>'); b = s.index('</style>', a)
    s = s[:b] + CSS + s[b:]
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', name)
