#!/usr/bin/env python3
"""费用概览 / 收支明细：按模块分层级（幂等，标记 bmod-v1，在 billsync.py 之后跑）。
77（2026-11-19，附 Permissions 页截图）：内容区改成整块白底后，模块只剩一点阴影，看不清边界；参考图片按模块划分层级。
- 模块标题放到模块外面：13px 灰字标题 + 右侧链接 / 切换，标题下面是模块框
- 模块框：白底、1px #e9ecf1 描边、4px 圆角，不用阴影；模块之间 24px
- 模块里的次级面板（余额、可开票金额、待办）用浅灰 #f7f8fa 底、无描边，形成「页面白 → 模块描边框 → 灰色面板」三层
- 待付款模块的标题用原来的「待付款 · 1 笔订单」，底色淡蓝渐变突出
- 画板里加在待付款、近三月账单上的灰色行内底色去掉（由新的层级代替）
用法: bmod.py BillOverview.dc.html BillBalance.dc.html
"""
import sys, re

CSS = r'''
/* bmod-v1 费用页按模块分层 */
.kc .hier-box.bsy>.hier-in:has(>.b8){padding:20px 20px 24px!important;background:#fff!important}
.kc .hier-box.bsy .b8.b8{gap:20px!important;margin:0!important;border-top:0!important;padding:0!important}
.kc .hier-box.bsy .b8 .b8-m,.kc .hier-box.bsy .b8 .b8-r{padding:0!important;border:0!important;background:none!important;box-shadow:none!important}
.kc .hier-box.bsy .b8 .b8-hero,.kc .hier-box.bsy .b8 .b8-sec{position:relative;margin:32px 0 0!important;padding:20px!important;background:#fff!important;border:1px solid #e9ecf1!important;border-radius:4px!important;box-shadow:none!important;overflow:visible!important}
.kc .hier-box.bsy .b8 .b8-hero+.b8-sec,.kc .hier-box.bsy .b8 .b8-sec+.b8-sec{margin-top:56px!important}
.kc .hier-box.bsy .b8 .b8-hero{background:linear-gradient(100deg,#f2f6ff 0%,#fff 72%)!important}
.kc .hier-box.bsy .b8 .b8-hero::after{display:none!important}
.kc .hier-box.bsy .b8 .b8-st{position:absolute;left:0;right:0;top:-32px;height:22px;margin:0!important}
.kc .hier-box.bsy .b8 .b8-st h2{font-size:13px!important;line-height:22px;font-weight:500!important;color:rgba(0,0,0,.6)!important}
.kc .hier-box.bsy .b8 .b8-st h2 small{font-weight:400;color:rgba(0,0,0,.4)!important}
.kc .hier-box.bsy .b8 .b8-hero>.b8-lb{position:absolute;left:0;top:-32px;height:22px;font-size:13px;font-weight:500;color:rgba(0,0,0,.6)}
.kc .hier-box.bsy .b8 .b8-hero>.b8-amt{margin-top:0!important}
.kc .hier-box.bsy .b8 .b8-inv{border:0!important;background:#f7f8fa!important;border-radius:4px!important}
.kc .hier-box.bsy .b8 .b8-todo{background:#f7f8fa!important;border-radius:4px!important}
.kc .hier-box.bsy .b8 .b8-todo a:hover{background:#fff!important}
.kc .hier-box.bsy .b8 .b8-sec>.b8-t{margin:-4px 0 -8px}
.kc .hier-box.bsy .b8 .b8-t th{background:#f7f8fa!important}
.kc .hier-box.bsy .b8 .b8-t tr:last-child td{border-bottom:0!important}
.kc .hier-box.bsy .b8 .b8-set li{min-height:44px}
'''

for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    if 'bmod-v1' in s:
        print('skip', p); continue
    assert 'bsy-v1' in s
    s = s.replace('<div class="b8-hero" style="background-color: var(--bg-2, #f7f8fa)">', '<div class="b8-hero">')
    s = s.replace('<div class="b8-sec" style="background-color: var(--bg-2, #f7f8fa)">', '<div class="b8-sec">')
    s = s.replace('<div class="b8-hero" style="border-width: 1px; border-color: var(--border-1, #e5e6eb)">', '<div class="b8-hero">')
    i = s.index('<x-dc>'); j = s.index('</style>', i)
    s = s[:j] + CSS + s[j:]
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', p)
