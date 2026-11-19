#!/usr/bin/env python3
"""我的产品卡片视图：分组容器和卡片底部操作（幂等，标记 pcb-v1，在 pcsem.py 之后跑）。
77（2026-11-19，附 Agent Inbox Board 截图）：画板的布局、背景和标题关系不够精致；操作按钮不要单独加背景色。
- 每个状态分组是一个浅灰容器，分组标题（图标 + 名称 + 计数）在容器里，卡片排在容器内，标题和卡片属于同一块
- 卡片 4px 圆角 + 极浅阴影，悬停加 md 阴影
- 卡片底部去掉灰色底条和分割线：左边「进入控制台 ›」文字链接，右边次要操作是文字按钮，主操作是白底描边小按钮（放最右）
只改 CSS，不改数据和结构。用法: pcboard.py AcctProducts.dc.html
"""
import sys

CSS = r'''
/* pcb-v1 分组容器 + 卡片操作不加底色 */
.pc .pc-wall{padding:20px}
.pc .pc-wall .pc-lane{padding:0 12px 12px;background:#f5f6f8;border-radius:4px}
.pc .pc-wall .pc-lane+.pc-lane{margin-top:16px}
.pc .pc-wall .pc-lh{height:44px;margin:0;padding:0 4px;gap:8px;font-size:13px}
.pc .pc-wall .pc-lh b{font-weight:500}
.pc .pc-wall .pc-lh>span{min-width:20px;height:18px;padding:0 6px;border-radius:9px;background:#fff;box-shadow:0 0 0 1px #e9ecf1;font-size:12px;line-height:18px;color:rgba(0,0,0,.7)}
.pc .pc-wall .pc-grid{gap:12px}
.pc .pc-wall .pc-c{border:0!important;border-radius:4px;overflow:hidden;box-shadow:0 0 0 1px rgba(0,0,0,.04),0 1px 2px rgba(0,0,0,.05)}
.pc .pc-wall .pc-c:hover{box-shadow:0 0 0 1px rgba(0,0,0,.05),0 8px 24px -4px rgba(0,0,0,.1),0 8px 12px -8px rgba(0,0,0,.05)}
.pc .pc-wall .pc-c.cur{box-shadow:0 0 0 1px #1664ff,0 8px 24px -4px rgba(0,0,0,.1)}
.pc .pc-wall .pc-cm{padding:20px 20px 12px}
.pc .pc-wall .pc-ft{height:auto;gap:4px;padding:4px 16px 16px 20px;background:none;border-top:0;font-size:12px}
.pc .pc-wall .pc-con{order:-1;margin:0 auto 0 0;color:rgba(0,0,0,.7)}
.pc .pc-wall .pc-con:hover{color:#1664ff}
.pc .pc-wall .pc-act{display:inline-flex;align-items:center;height:28px;padding:0 10px;border-radius:2px;color:rgba(0,0,0,.7);font-weight:400;transition:background-color .15s,color .15s,border-color .15s}
.pc .pc-wall .pc-act:hover{background:#f2f4f8;color:rgba(0,0,0,.9)}
.pc .pc-wall .pc-act.pri{order:2;margin-left:4px;padding:0 12px;background:#fff;box-shadow:inset 0 0 0 1px #e6e9ef;color:rgba(0,0,0,.9);font-weight:500}
.pc .pc-wall .pc-act.pri:hover{background:#fff;box-shadow:inset 0 0 0 1px #1664ff;color:#1664ff}
'''

for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    if 'pcb-v1' in s:
        print('skip', p); continue
    if 'pcsem-v1' not in s:
        sys.exit('run pcsem.py first')
    i = s.index('<x-dc>'); j = s.index('</style>', i)
    s = s[:j] + CSS + s[j:]
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', p)
