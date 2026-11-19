#!/usr/bin/env python3
"""三个中心的导航入口（幂等，标记 cnav-v1，在 centers.py 之后跑）。
77（2026-11-19）：「进入控制台，怎么跳转到不同的管理中心，目前也没有导航入口了」。
- 总览 / 我的产品 的页签行右侧：费用中心 · 企业中心 · 支持中心 三个入口（腾讯云首页 tab 行右侧放常用入口的做法）
- 头像菜单顶部：三个中心的入口卡（带一句说明），去掉原来零散的「费用与发票」
- 顶栏「产品与服务」面板：「账号与费用」分组改为「管理中心」，列出总览、我的产品和三个中心
- 中心左侧菜单头：中心名下方加「‹ 返回控制台总览」
- 顶栏「费用」下拉底部「前往账务概览」改「进入费用中心」，消息下拉「查看全部消息」不变
用法: ctrnav.py <dir>
"""
import sys, re, os, glob

C = [('费用中心', 'BillOverview', 'doc', '订单 · 付款 · 发票'), ('企业中心', 'OrgInfo', 'users', '认证 · 成员 · 权限'), ('支持中心', 'SupTickets', 'help', '工单 · 消息 · 文档')]

TABR = '<span class="tcl-r cnav-r">' + ''.join('<a href="%s.dc.html"><i class="kc-ic i-%s"></i>%s</a>' % (p, ic, n) for n, p, ic, _ in C) + '</span>'
ME = '<div class="cnav-me">' + ''.join('<a href="%s.dc.html"><i class="kc-ic i-%s"></i><b>%s</b><small>%s</small></a>' % (p, ic, n, d) for n, p, ic, d in C) + '</div>'
PANEL = ('<h4>管理中心</h4><ul><li><a href="ConsoleHome.dc.html">控制台总览</a></li><li><a href="AcctProducts.dc.html">我的产品</a></li>'
         + ''.join('<li><a href="%s.dc.html">%s</a></li>' % (p, n) for n, p, _, _ in C) + '</ul>')

CSS = r'''
/* cnav-v1 三个中心的导航入口 */
.kc .kc-main>nav.tcl-tabs>.cnav-r{margin-left:auto;align-self:center;display:flex;gap:4px}
.kc .kc-main>nav.tcl-tabs>.cnav-r>a{display:inline-flex;align-items:center;gap:6px;height:32px;padding:0 12px;font-size:13px;font-weight:400;color:rgba(0,0,0,.7);text-decoration:none;border-radius:2px}
.kc .kc-main>nav.tcl-tabs>.cnav-r>a::after{display:none!important}
.kc .kc-main>nav.tcl-tabs>.cnav-r>a:hover{background:rgba(255,255,255,.7);color:#1664ff}
.cnav-r .kc-ic,.cnav-me .kc-ic{display:inline-block;flex:none;width:14px;height:14px;-webkit-mask-size:14px 14px;mask-size:14px 14px;background:currentColor!important;margin:0}
.ac-pop:has(>.cnav-me){width:340px!important}
.cnav-me{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;padding:12px 16px;border-bottom:1px solid #eef0f3}
.cnav-me>a{display:flex;flex-direction:column;gap:4px;padding:10px;background:#f7f8fa;color:rgba(0,0,0,.9);text-decoration:none;border-radius:2px}
.cnav-me>a:hover{background:#eef4ff;color:#1664ff}
.cnav-me>a .kc-ic{width:16px;height:16px;-webkit-mask-size:16px 16px;mask-size:16px 16px;color:#1664ff;background:#1664ff!important}
.cnav-me>a b{font-size:13px;font-weight:500}
.cnav-me>a small{font-size:11px;color:rgba(0,0,0,.5);white-space:nowrap}
.kc-side.ctr-side .kc-sh .cnav-back{display:inline-flex;align-items:center;gap:2px;margin-top:4px;font-size:12px;color:rgba(0,0,0,.5);text-decoration:none}
.kc-side.ctr-side .kc-sh .cnav-back:hover{color:#1664ff}
'''

def run(p):
    s = open(p, encoding='utf-8').read()
    if 'cnav-v1' in s or '<main' not in s:
        return 'skip'
    n = []
    # 页签行右侧入口
    s2 = re.sub(r'(<nav class="tcl-tabs[^"]*"[^>]*>(?:<a[^>]*>[^<]*</a>)+)(</nav>)', lambda m: m.group(1) + TABR + m.group(2), s, count=1)
    if s2 != s: n.append('tabs'); s = s2
    # 头像菜单
    s2 = re.sub(r'<li><a href="BillOverview\.dc\.html">费用与发票<i[^>]*>(?:<svg.*?</svg>)?</i></a></li>', '', s, flags=re.S)
    s2 = re.sub(r'(<div class="ac-uh">(?:(?!</div></div>).)*</div></div>)(\s*<ul class="ac-rows")', lambda m: m.group(1) + ME + m.group(2), s2, flags=re.S)
    if s2 != s: n.append('me'); s = s2
    # 顶栏菜单规范板的说明文字
    s2 = re.sub(r'只放账号本身的事[^<]*', '顶部是费用、企业、支持三个中心的入口；下面只放账号本身的事：认证、安全、成员和退出。', s, count=1)
    if s2 != s: n.append('spec'); s = s2
    # 产品面板
    s2 = re.sub(r'<h4>账号与费用</h4><ul>.*?</ul>', PANEL, s, count=1, flags=re.S)
    if s2 != s: n.append('panel'); s = s2
    # 费用下拉底部
    s2 = s.replace('<a href="BillOverview.dc.html">前往账务概览', '<a href="BillOverview.dc.html">进入费用中心')
    if s2 != s: n.append('fee'); s = s2
    # 中心菜单头
    s2 = re.sub(r'(<aside class="kc-side ctr-side"[^>]*><div class="kc-sh"><b>[^<]*</b>)<span>[^<]*</span>', r'\1<a class="cnav-back" href="ConsoleHome.dc.html">‹ 返回控制台总览</a>', s, count=1)
    if s2 != s: n.append('back'); s = s2
    if not n:
        return 'none'
    j0 = s.index('<x-dc>'); j = s.index('</style>', j0)
    s = s[:j] + CSS + s[j:]
    open(p, 'w', encoding='utf-8').write(s)
    return ' '.join(n)

for p in sorted(glob.glob(os.path.join(sys.argv[1], '*.dc.html'))):
    print(os.path.basename(p), run(p))
