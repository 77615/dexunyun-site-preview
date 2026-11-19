#!/usr/bin/env python3
"""控制台结构：顶部 tab 只留视角（总览 / 我的产品），费用、企业、支持拆成带左侧菜单的中心（幂等，标记 ctr-v1）。
77（2026-11-19）：腾讯云首页 tab 是总览的不同视角，费用、企业这类功能分区是左菜单 + 右内容；工单挂在 tab 下容易误解。决策卡选「tab 留视角，拆成三个中心」。
- 费用中心：概览 / 订单 / 付款 / 收支明细 / 发票 / 合同（原二级分段改成左侧菜单）
- 企业中心：企业信息 / 成员 / 角色权限 / 安全设置
- 支持中心：我的工单 / 提交工单 / 消息 / 文档
- 中心页：加左侧菜单（可折叠，同产品控制台），去掉顶部 tab 和问候语，页头改成当前菜单名；详情和流程页高亮所属菜单
- 其余页面：顶部 tab 只留「总览 / 我的产品」
用法: centers.py <dir>（处理目录里全部 .dc.html）
"""
import sys, re, os, glob

FOLD = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">'
        '<rect x="3.5" y="4.5" width="17" height="15" rx="2"></rect><path d="M9.5 4.5v15"></path></svg>')

CENTERS = {
    '费用中心': [('概览', 'BillOverview', 'grid'), ('订单', 'BillOrders', 'doc'), ('付款', 'BillPay', 'check'),
               ('收支明细', 'BillBalance', 'chart'), ('发票', 'BillInvoice', 'layers'), ('合同', 'BillContract', 'policy')],
    '企业中心': [('企业信息', 'OrgInfo', 'box'), ('成员', 'OrgMembers', 'users'), ('角色权限', 'OrgRoles', 'lock'), ('安全设置', 'OrgSecurity', 'shield')],
    '支持中心': [('我的工单', 'SupTickets', 'doc'), ('提交工单', 'SupTicketNew', 'help'), ('消息', 'Notifications', 'bell'), ('文档', 'SupDocs', 'link')],
}
# 页面 -> (中心, 高亮菜单)
PAGE = {
    'BillOverview': ('费用中心', '概览'), 'BillOrders': ('费用中心', '订单'), 'BillPay': ('费用中心', '付款'),
    'BillBalance': ('费用中心', '收支明细'), 'BillInvoice': ('费用中心', '发票'), 'BillContract': ('费用中心', '合同'),
    'BillConfirm': ('费用中心', '订单'), 'BillOrderDetail': ('费用中心', '订单'), 'BillPayment': ('费用中心', '付款'),
    'BillPayFix': ('费用中心', '付款'), 'NoAccess': ('费用中心', '付款'), 'BillInvoiceApply': ('费用中心', '发票'),
    'BillInvoiceDetail': ('费用中心', '发票'), 'BillContractApply': ('费用中心', '合同'), 'BillContractDetail': ('费用中心', '合同'),
    'OrgInfo': ('企业中心', '企业信息'), 'OrgVerify': ('企业中心', '企业信息'), 'OrgMembers': ('企业中心', '成员'),
    'OrgMemberNew': ('企业中心', '成员'), 'OrgRoles': ('企业中心', '角色权限'), 'OrgSecurity': ('企业中心', '安全设置'),
    'SupTickets': ('支持中心', '我的工单'), 'SupTicketDetail': ('支持中心', '我的工单'), 'SupTicketNew': ('支持中心', '提交工单'),
    'Notifications': ('支持中心', '消息'), 'SupDocs': ('支持中心', '文档'),
}

CSS = r'''
/* ctr-v1 费用、企业、支持三个中心：左侧菜单 + 右内容（只作用于 .kc.ctr） */
.kc.ctr .kc-body{flex-wrap:nowrap!important}
.kc.ctr .kc-body>.kc-main{flex:1 1 0!important;min-width:0}
.kc.ctr main.kc-main.kc-main{background:#f2f4f8!important}
.kc.ctr main.kc-main>.kc-hd.kc-hd{display:flex;align-items:center;justify-content:space-between;padding:20px 24px 16px!important}
.kc.ctr main.kc-main>.kc-hd.kc-hd .kc-h1{font-size:20px!important;line-height:28px!important;font-weight:600!important}
.kc.ctr main.kc-main>.hier-box{margin-top:0!important}
.kc.ctr .kc-side .kc-sh b{font-size:14px;font-weight:600;color:rgba(0,0,0,.9)}
'''

def side(stem, center, cur):
    items = ''.join('<a class="kc-it%s" href="%s.dc.html"%s><i class="kc-ic i-%s"></i><span>%s</span></a>' % (
        ' on' if t == cur else '', p, ' aria-current="page"' if t == cur else '', ic, t) for t, p, ic in CENTERS[center])
    return ('<input type="checkbox" id="kcf-%s" class="kc-fold-ck" aria-label="收起左侧菜单">'
            '<aside class="kc-side ctr-side" aria-label="%s菜单"><div class="kc-sh"><b>%s</b><span>德迅科技 · 主账号</span></div>'
            '<nav class="kc-nv" aria-label="%s菜单">%s</nav>'
            '<div class="kc-foldbar"><label for="kcf-%s" class="kc-fold" title="收起菜单">%s</label></div></aside>'
            '<label for="kcf-%s" class="kc-unfold" title="展开菜单">%s</label>') % (stem, center, center, center, items, stem, FOLD, stem, FOLD)

def run(p):
    stem = os.path.basename(p).replace('.dc.html', '')
    s = open(p, encoding='utf-8').read()
    if 'ctr-v1' in s or '<main' not in s:
        return 'skip'
    i = s.index('<main'); k = s.index('</main>', i); m = s[i:k]
    if stem in PAGE:
        center, cur = PAGE[stem]
        m = re.sub(r'<nav class="tcl-tabs[^"]*"[^>]*>.*?</nav>\s*', '', m, count=1, flags=re.S)
        # 分组页：去掉二级分段，页头改成菜单名，分段里的按钮移到页头
        g = re.search(r'(<div class="hier-box[^"]*">)<nav class="ia-tabs"[^>]*>(?:<span class="bsy-seg">)?(?:<a[^>]*>[^<]*</a>)+(?:</span>)?(.*?)</nav>', m, re.S)
        btns = ''
        if g:
            btns = re.sub(r'class="kc-btns tcl-r"', 'class="kc-btns"', g.group(2)).strip()
            m = m[:g.start()] + g.group(1) + m[g.end():]
        hd = re.search(r'<div class="kc-hd">\s*<div class="kc-hdl"><div><h1 class="kc-h1">(.*?)</h1>', m, re.S)
        if hd and '下午好' in hd.group(1):
            m = m[:hd.start(1)] + cur + m[hd.end(1):]
            if btns:
                b = re.search(r'<div class="kc-btns">\s*</div>', m)
                inner = re.sub(r'^<div class="kc-btns">(.*)</div>$', r'\1', btns, flags=re.S)
                if b:
                    m = m[:b.start()] + '<div class="kc-btns">' + inner + '</div>' + m[b.end():]
        s = s[:i] + m + s[k:]
        s = re.sub(r'(<nav data-cb="" class="kc-crumb".*?</nav>)', lambda x: x.group(1).replace('href="BillOverview.dc.html">费用</a>', 'href="BillOverview.dc.html">费用中心</a>').replace('href="OrgInfo.dc.html">企业</a>', 'href="OrgInfo.dc.html">企业中心</a>'), s, count=1, flags=re.S)
        s = s.replace('<div class="kc ux-wrap">', '<div class="kc ux-wrap ctr">', 1)
        s = s.replace('<span class="kc-ln-c">消息中心</span>', '<span class="kc-ln-c">支持中心</span>')
        if 'kc-ln-c' not in s:
            s = re.sub(r'(<a class="kc-logo"[^>]*>\s*<span class="kc-mark">德</span>)(.*?)(</a>)',
                       lambda x: x.group(1) + '<span class="kc-ln"><span class="kc-ln-c">' + center + '</span><span class="kc-ln-b" aria-hidden="true">德迅云控制台</span></span>' + x.group(3), s, count=1, flags=re.S)
        b = s.index('<div class="kc-body">') + len('<div class="kc-body">')
        s = s[:b] + side(stem, center, cur) + s[b:]
        j0 = s.index('<x-dc>'); j = s.index('</style>', j0)
        s = s[:j] + CSS + s[j:]
        r = 'center ' + center + ' / ' + cur + (' (group)' if g else '')
    else:
        n0 = m.count('<nav class="tcl-tabs')
        m2 = re.sub(r'(<nav class="tcl-tabs[^>]*>.*?)<a[^>]*href="BillOverview\.dc\.html"[^>]*>费用</a><a[^>]*href="OrgInfo\.dc\.html"[^>]*>企业</a>', r'\1', m, flags=re.S)
        if m2 == m:
            return 'no tabs' if not n0 else 'TABS NOT CHANGED'
        s = s[:i] + m2 + s[k:]
        j0 = s.index('<x-dc>'); j = s.index('</style>', j0)
        s = s[:j] + '\n/* ctr-v1 顶部 tab 只留视角：总览 / 我的产品 */\n' + s[j:]
        r = 'view tabs'
    open(p, 'w', encoding='utf-8').write(s)
    return r

for p in sorted(glob.glob(os.path.join(sys.argv[1], '*.dc.html'))):
    print(os.path.basename(p), run(p))
