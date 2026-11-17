#!/usr/bin/env python3
"""账号侧页面统一成腾讯式：去掉左侧菜单，顶部横排「总览 / 我的产品 / 费用 / 企业」页签（幂等，标记 tcl2-v1）。
分组页（标题就是分组名，下面有二级页签）：标题行换成一级页签；其他页：一级页签放在标题上方。
用法: tcl2.py X.dc.html [...]
"""
import re, sys, os

TABS = [('总览', 'ConsoleHome.dc.html'), ('我的产品', 'AcctProducts.dc.html'), ('费用', 'BillOverview.dc.html'), ('企业', 'OrgInfo.dc.html')]

def group(name):
    if name.startswith('ConsoleHome'): return '总览'
    if name.startswith('Acct'): return '我的产品'
    if name.startswith('Bill') or name == 'NoAccess': return '费用'
    if name.startswith('Org'): return '企业'
    return ''

CSS = '''
/* tcl2-v1 账号侧 · 腾讯式一级页签（无左侧菜单） */
.kc .kc-body>.kc-main{flex:1 1 100%;min-width:0;margin-left:0!important}
.kc .kc-main>nav.tcl-tabs{margin:8px 20px 16px!important}
.tcl-tabs{display:flex;gap:32px;height:48px;align-items:flex-end;border-bottom:1px solid rgba(0,0,0,.06)}
.tcl-tabs>a{position:relative;display:flex;align-items:center;height:44px;font-size:16px;color:rgba(0,0,0,.7);text-decoration:none;transition:color .15s}
.tcl-tabs>a:hover{color:rgba(0,0,0,.9)}
.tcl-tabs>a.on{color:rgba(0,0,0,.9);font-weight:600}
.tcl-tabs .tcl-r{margin-left:auto;align-self:center;display:flex;gap:8px}
.kc .kc-main>nav.tcl-tabs+.ia-tabs{padding-left:0!important;padding-right:0!important}
.tcl-tabs>a.on::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:rgba(0,0,0,.9)}
'''

def nav(cur, extra=''):
    a = ''.join(f'<a class="on" aria-current="page" href="{h}">{t}</a>' if t == cur else f'<a href="{h}">{t}</a>' for t, h in TABS)
    return f'<nav class="tcl-tabs{extra}" aria-label="控制台分区">{a}</nav>'

for p in sys.argv[1:]:
    name = os.path.basename(p).replace('.dc.html', '')
    s = open(p, encoding='utf-8').read()
    if not re.search(r'L\("总览", .grid.\), L\("我的产品"', s):
        print('not account page', name); continue
    if 'tcl2-v1' in s or 'tcl-v1' in s:
        print('skip', name); continue
    s, n = re.subn(r'<input type="checkbox" id="kcf-[^"]*".*?(?=<main data-pg=)', '', s, count=1, flags=re.S)
    if n != 1:
        print('NO SIDEBAR', name); continue
    g = group(name)
    m = re.search(r'(<main data-pg="[^"]*" class="kc-main">\s*)(<div class="kc-hd">\s*<div class="kc-hdl"><div><h1 class="kc-h1">([^<]*)</h1></div></div>\s*(?:<div class="kc-btns">(.*?)</div>)?\s*</div>)', s, flags=re.S)
    if m and m.group(3).strip() == g and g:
        btns = (m.group(4) or '').strip()
        tabs = nav(g, ' tcl-top')
        if btns:
            tabs = tabs.replace('</nav>', f'<div class="kc-btns tcl-r">{btns}</div></nav>')
        s = s[:m.start(2)] + tabs + s[m.end(2):]
        mode = 'group'
    else:
        s, n = re.subn(r'(<main data-pg="[^"]*" class="kc-main">\s*)', lambda mm: mm.group(1) + nav(g) + '\n      ', s, count=1)
        assert n == 1, name
        mode = 'page'
    i = s.index('<x-dc>'); j = s.index('</style>', i)
    s = s[:j] + CSS + s[j:]
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', name, g or '-', mode)
