#!/usr/bin/env python3
"""产品与服务弹窗左栏放固定的中心入口；菜单按钮放到顶栏最左（幂等，标记 pin-v1，在 ctrnav.py 之后跑）。
77（2026-11-19 画板评论，ConsoleHome）：「我把菜单按钮放在了最左边，然后点击以后的弹出菜单，我想要在左侧菜单放置最常使用和固定位置的几个中心入口」。
- 左栏顶部固定入口（带图标，位置不变）：控制台总览、我的产品、安全中心（德迅安全卫士，带待处理数）、费用中心、企业中心、支持中心
- 下面保留 最近访问、我的收藏；原来分散的「安全中心」「管理中心」两组并入固定入口
- 全部页面同 77 在总览、我的产品上的改动：菜单按钮在 Logo 左边
用法: pinnav.py <dir>
"""
import sys, re, os, glob

SEC = 'https://claude.ai/artifact/LE5cNnQWZjPMjXvXCC4MG7#play-de5201e8a0c7'
FIX = [('控制台总览', 'ConsoleHome.dc.html', 'grid', ''), ('我的产品', 'AcctProducts.dc.html', 'box', ''),
       ('安全中心', None, 'shield', '18 条待处理'), ('费用中心', 'BillOverview.dc.html', 'doc', ''),
       ('企业中心', 'OrgInfo.dc.html', 'users', ''), ('支持中心', 'SupTickets.dc.html', 'help', '')]

CSS = r'''
/* pin-v1 产品与服务弹窗左栏：固定的中心入口 */
.tp-pp .tp-l>ul.tp-fix{margin:0 0 8px;padding:0 0 8px;border-bottom:1px solid #eef0f3}
.tp-pp .tp-l>ul.tp-fix>li>a{display:flex;align-items:center;justify-content:space-between;gap:8px;height:36px}
.tp-pp .tp-l>ul.tp-fix .tp-n{display:inline-flex;align-items:center;gap:10px;font-size:13px;color:rgba(0,0,0,.9)}
.tp-pp .tp-l>ul.tp-fix .tp-n b{font-weight:500}
.tp-pp .tp-l>ul.tp-fix .kc-ic{display:inline-block;flex:none;width:16px;height:16px;-webkit-mask-size:16px 16px;mask-size:16px 16px;background:rgba(0,0,0,.6)!important;margin:0}
.tp-pp .tp-l>ul.tp-fix>li>a:hover .kc-ic,.tp-pp .tp-l>ul.tp-fix>li>a.on .kc-ic{background:#1664ff!important}
.tp-pp .tp-l>ul.tp-fix>li>a.on .tp-n{color:#1664ff}
.tp-pp .tp-l>ul.tp-fix small.r{color:#f64041}
'''

def run(p):
    s = open(p, encoding='utf-8').read()
    if 'pin-v1' in s or 'class="tp-l"' not in s:
        return 'skip'
    stem = os.path.basename(p)
    cur = {'ConsoleHome.dc.html': '控制台总览', 'ConsoleHomeNew.dc.html': '控制台总览', 'GlobalSearch.dc.html': '控制台总览', 'TopMenus.dc.html': '控制台总览'}.get(stem)
    if not cur:
        if stem.startswith('Acct'): cur = '我的产品'
        elif stem.startswith('Bill') or stem == 'NoAccess.dc.html': cur = '费用中心'
        elif stem.startswith('Org'): cur = '企业中心'
        elif stem.startswith('Sup') or stem == 'Notifications.dc.html': cur = '支持中心'
    def li(n, h, ic, b):
        if h is None:
            m = re.search(r'<a class="sx-pin" href="([^"]*)"', s); h = m.group(1) if m else SEC
        cls = ' class="on"' if n == cur else ''
        return '<li><a%s href="%s"><span class="tp-n"><i class="kc-ic i-%s"></i><b>%s</b></span>%s</a></li>' % (cls, h, ic, n, '<small class="r">%s</small>' % b if b else '')
    fix = '<ul class="tp-fix" aria-label="常用入口">' + ''.join(li(*f) for f in FIX) + '</ul>'
    s2 = re.sub(r'<h4>安全中心</h4><ul class="sx-pinl">.*?</ul>', lambda m: fix, s, count=1, flags=re.S)
    if s2 == s:
        return 'NO PIN BLOCK'
    s = s2
    s = re.sub(r'\s*<h4>管理中心</h4><ul>.*?</ul>', '', s, count=1, flags=re.S)
    # 菜单按钮放到 Logo 左边
    top = s.index('<header class="kc-top">')
    lg = re.search(r'<a class="kc-logo".*?</a>\s*', s[top:], re.S)
    dw = s.find('<span class="tp-dw">', top)
    if lg and top + lg.start() < dw:
        logo = lg.group(0).strip()
        s = s[:top + lg.start()] + s[top + lg.end():]
        dw = s.find('<span class="tp-dw">', top)
        e = s.index('</sc-if></span>', dw) + len('</sc-if></span>')
        s = s[:e] + logo + s[e:]
    j0 = s.index('<x-dc>'); j = s.index('</style>', j0)
    s = s[:j] + CSS + s[j:]
    open(p, 'w', encoding='utf-8').write(s)
    return 'ok ' + (cur or '-')

for p in sorted(glob.glob(os.path.join(sys.argv[1], '*.dc.html'))):
    print(os.path.basename(p), run(p))
