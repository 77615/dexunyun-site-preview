#!/usr/bin/env python3
"""分组页（我的产品 / 费用 / 企业）头部和首页统一（幂等，标记 tcl3-v1）。
- 页签上方加首页同款欢迎语，头部同款蓝色渐变背景，左右边距 24 与首页一致
- 二级页签改成首页「最近访问」同款胶囊
- 卡片统一：无边框、直角、0 1px 4px 阴影
只处理已有 nav.tcl-tabs.tcl-top 的页面（tcl2 的分组页）。
用法: tcl3.py X.dc.html [...]
"""
import re, sys, os

AI = ('<svg class="kc-ai" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 1.5c.4 3.3 2.2 5.1 5.5 5.5v.9c-3.3.4-5.1 2.2-5.5 5.5h-.9c-.4-3.3-2.2-5.1-5.5-5.5V7c3.3-.4 5.1-2.2 5.5-5.5z"></path>'
      '<path d="M13.2 1.2c.1.9.6 1.4 1.5 1.5v.3c-.9.1-1.4.6-1.5 1.5h-.3c-.1-.9-.6-1.4-1.5-1.5v-.3c.9-.1 1.4-.6 1.5-1.5z" opacity=".55"></path></svg>')
HD = f'<div class="kc-hd tcl-hd"><div class="kc-hdl"><div><h1 class="kc-h1">下午好，wangqi{AI}</h1></div></div><div class="kc-btns"></div></div>\n      '

CSS = '''
/* tcl3-v1 分组页头部与首页统一 */
.kc main.kc-main.kc-main{background:radial-gradient(1100px 300px at 82% -40px,#d6e6ff 0,rgba(214,230,255,.45) 45%,transparent 75%),#f2f4f8!important}
.kc main.kc-main>.kc-hd.kc-hd{background:transparent!important;border:0!important;box-shadow:none!important;margin:0!important;padding:28px 24px 8px!important;min-height:0}
.kc main.kc-main>.kc-hd.kc-hd .kc-h1{font-size:22px!important;line-height:32px!important;font-weight:600!important;display:flex;align-items:center;gap:4px}
.kc-hd .kc-ai{width:16px;height:16px;fill:#1664ff}
.kc main.kc-main>*:not(.kc-hd){margin-left:24px!important;margin-right:24px!important}
.kc .kc-main>nav.tcl-tabs{margin:12px 24px 20px!important}
.kc .kc-main>nav.ia-tabs{display:flex;gap:8px!important;margin-top:0!important;margin-bottom:16px!important;padding:0!important;border:0!important;background:none!important}
.kc .kc-main>nav.ia-tabs>a{height:32px!important;padding:0 16px!important;margin:0!important;display:inline-flex;align-items:center;border:1px solid #e6e9ef!important;border-radius:16px!important;background:#fff!important;color:rgba(0,0,0,.7)!important;font-size:13px!important;font-weight:400!important;text-decoration:none;box-shadow:none!important}
.kc .kc-main>nav.ia-tabs>.tcl-r{margin-left:auto;display:flex;gap:8px;align-items:center}\n.kc .kc-main>nav.ia-tabs>.tcl-r>a.kc-btn{height:32px!important;padding:0 16px!important;margin:0!important;display:inline-flex!important;align-items:center;gap:6px;border:1px solid #d6dbe3!important;background:#fff!important;color:rgba(0,0,0,.9)!important;font-size:13px!important;border-radius:0!important}\n.kc .kc-main>nav.ia-tabs>.tcl-r>a.kc-btn:hover{border-color:#1664ff!important;color:#1664ff!important}\n.kc .kc-main>nav.ia-tabs>a::after,.kc .kc-main>nav.ia-tabs>a::before{display:none!important}
.kc .kc-main>nav.ia-tabs>a:hover{color:#1664ff!important;border-color:#c6d8ff!important}
.kc .kc-main>nav.ia-tabs>a.on{background:#e5ecff!important;border-color:#e5ecff!important;color:#1664ff!important;font-weight:500!important}
.kc .kc-main .kc-card,.kc .kc-main .b8-box,.kc .kc-main .ac-st{border:0!important;border-radius:0!important;box-shadow:0 1px 4px rgba(0,0,0,.05)!important}
'''

for p in sys.argv[1:]:
    name = os.path.basename(p)
    s = open(p, encoding='utf-8').read()
    if 'tcl3-v1' in s:
        print('skip', name); continue
    if 'class="tcl-tabs tcl-top"' not in s:
        print('not group page', name); continue
    s = s.replace('<nav class="tcl-tabs tcl-top"', HD + '<nav class="tcl-tabs tcl-top"', 1)
    # 一级页签行在各分组保持一致：页面按钮挪到二级页签行右侧
    m = re.search(r'<div class="kc-btns tcl-r">(.*?)</div></nav>', s, flags=re.S)
    if m:
        btns = m.group(0)[:-len('</nav>')]
        s = s.replace(m.group(0), '</nav>', 1)
        k = s.index('<nav class="ia-tabs"', m.start()); e = s.index('</nav>', k)
        s = s[:e] + btns + s[e:]
    i = s.index('<x-dc>'); j = s.index('</style>', i)
    s = s[:j] + CSS + s[j:]
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', name)
