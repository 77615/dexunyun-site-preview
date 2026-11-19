#!/usr/bin/env python3
"""工单、消息、权益转移等二级页和分组页统一（幂等，标记 ssy-v1）。
77（2026-11-19）：「检查一下其他的页面，比如工单等等有没有页面不适配的」。
- 卡片里的状态页签（未关闭 / 待我确认…、全部 / 我发起的…）：下划线改成安静页签（选中浅灰底），顶行留白 16/20 + 分隔线，同分组页
- 消息：「消息 / 接收设置」改成分段切换；分类筛选（全部 / 安全…）蓝框胶囊改成安静页签
- 卡片：去描边，浅阴影，同分组页容器；筛选栏左右 20
- 权益转移统计卡：去阴影，1px 细框、4px 圆角，同费用概览的模块
- 新账号总览：问候语放到一级页签上方，同总览
用法: secsync.py X.dc.html [...]
"""
import sys, re

AI = ('<svg class="kc-ai" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 1.5c.4 3.3 2.2 5.1 5.5 5.5v.9c-3.3.4-5.1 2.2-5.5 5.5h-.9c-.4-3.3-2.2-5.1-5.5-5.5V7c3.3-.4 5.1-2.2 5.5-5.5z"></path>'
      '<path d="M13.2 1.2c.1.9.6 1.4 1.5 1.5v.3c-.9.1-1.4.6-1.5 1.5h-.3c-.1-.9-.6-1.4-1.5-1.5v-.3c.9-.1 1.4-.6 1.5-1.5z" opacity=".55"></path></svg>')

CSS = r'''
/* ssy-v1 二级页（工单、消息、权益转移）页签和卡片同步分组页 */
.kc main.kc-main section.kc-card.ssy{border:0!important;border-radius:0;box-shadow:0 1px 4px rgba(0,0,0,.05)!important}
.kc main.kc-main section.kc-card.ssy>.kc-tabs.kc-tabs{display:flex!important;gap:4px!important;height:auto!important;margin:0!important;padding:16px 20px!important;border:0!important;border-bottom:1px solid #e5e6eb!important;background:none!important;box-shadow:none!important}
.kc main.kc-main section.kc-card.ssy>.kc-tabs>.kc-tab.kc-tab{display:inline-flex!important;align-items:center;gap:6px;height:28px!important;min-width:0!important;padding:0 10px!important;margin:0!important;border:0!important;border-radius:2px!important;background:transparent!important;box-shadow:none!important;font-size:12px!important;font-weight:400!important;color:rgba(0,0,0,.7)!important}
.kc main.kc-main section.kc-card.ssy>.kc-tabs>.kc-tab::before,.kc main.kc-main section.kc-card.ssy>.kc-tabs>.kc-tab::after{display:none!important}
.kc main.kc-main section.kc-card.ssy>.kc-tabs>.kc-tab:hover{background:#f7f8fb!important;color:rgba(0,0,0,.9)!important}
.kc main.kc-main section.kc-card.ssy>.kc-tabs>.kc-tab.on{background:#f2f4f8!important;color:rgba(0,0,0,.9)!important;font-weight:500!important}
.kc main.kc-main section.kc-card.ssy>.kc-tabs>.kc-tab>.kc-cnt{min-width:0!important;height:auto!important;padding:0!important;background:none!important;font-size:12px!important;font-weight:400!important;color:rgba(0,0,0,.5)!important}
.kc main.kc-main section.kc-card.ssy>.kc-tabs>.kc-tab>.kc-cnt.r{color:#f64041!important;font-weight:500!important}
.kc main.kc-main section.kc-card.ssy>.kc-tabs>.kc-tab>.kc-cnt:empty{display:none}
.kc main.kc-main section.kc-card.ssy>.lf-bar{padding-left:20px!important;padding-right:20px!important}
/* 消息：分段切换 + 安静筛选 */
.kc main.kc-main section.kc-card.ssy.ssy-seg>.kc-tabs.kc-tabs{gap:0!important}
.kc main.kc-main section.kc-card.ssy.ssy-seg>.kc-tabs.kc-tabs::before{content:none}
.kc main.kc-main section.kc-card.ssy.ssy-seg>.kc-tabs>.kc-tab.kc-tab{height:32px!important;padding:0 14px!important;border-radius:0!important;background:#f2f3f5!important;box-shadow:inset 0 0 0 2px #f2f3f5!important;color:rgba(0,0,0,.6)!important}
.kc main.kc-main section.kc-card.ssy.ssy-seg>.kc-tabs>.kc-tab.kc-tab.on{background:#fff!important;color:rgba(0,0,0,.9)!important;box-shadow:inset 0 0 0 2px #f2f3f5,0 1px 2px rgba(0,0,0,.06)!important}
.kc main.kc-main section.kc-card.ssy .ac-chips{gap:4px;padding:12px 20px 0;align-items:center}
.kc main.kc-main section.kc-card.ssy .ac-chips>button{height:28px;padding:0 10px;border:0!important;border-radius:2px;background:transparent!important;color:rgba(0,0,0,.7)!important;font-weight:400}
.kc main.kc-main section.kc-card.ssy .ac-chips>button:hover{background:#f7f8fb!important;color:rgba(0,0,0,.9)!important}
.kc main.kc-main section.kc-card.ssy .ac-chips>button.on{background:#f2f4f8!important;color:rgba(0,0,0,.9)!important;font-weight:500}
.kc main.kc-main section.kc-card.ssy .ac-chips>button[style]{background:none!important;color:#1664ff!important;font-weight:400}
/* 统计卡同费用概览模块 */
.kc main.kc-main>.ac-stats.ssy-st>.ac-st{border:1px solid #e9ecf1!important;border-radius:4px!important;box-shadow:none!important;padding:16px 20px}
.kc main.kc-main>.ac-stats.ssy-st>.ac-st:hover{border-color:#d5dae3!important}
.kc main.kc-main>.ac-stats.ssy-st>.ac-st.o b{color:#ff7800}
'''

def addcss(s):
    i = s.index('<x-dc>'); j = s.index('</style>', i)
    return s[:j] + CSS + s[j:]

for p in sys.argv[1:]:
    name = p.rsplit('/', 1)[-1].replace('.dc.html', '')
    s = open(p, encoding='utf-8').read()
    if 'ssy-v1' in s:
        print('skip', name); continue
    i = s.index('<main'); k = s.index('</main>', i)
    m = s[i:k]
    if name == 'ConsoleHomeNew':
        nav = re.search(r'<nav class="tcl-tabs"[^>]*>.*?</nav>\s*', m, re.S)
        hd = re.search(r'<div class="kc-hd">.*?<div class="kc-btns">.*?</div>\s*</div>\s*', m, re.S)
        assert nav and hd and nav.start() < hd.start()
        h = hd.group(0).replace('下午好，新用户</h1>', '下午好，新用户' + AI + '</h1>')
        m = m[:nav.start()] + h + nav.group(0).replace('class="tcl-tabs"', 'class="tcl-tabs tcl-top"') + m[hd.end():]
    else:
        n = 0
        def card(mt):
            global n; n += 1
            return '<section class="kc-card ssy' + (' ssy-seg' if name == 'Notifications' else '') + '">' + mt.group(1)
        m, n = re.subn(r'<section class="kc-card">(\s*<div class="kc-tabs" role="tablist">)', lambda mt: '<section class="kc-card ssy' + (' ssy-seg' if name == 'Notifications' else '') + '">' + mt.group(1), m, count=1)
        assert n == 1, name
        m = m.replace('<div class="ac-stats">', '<div class="ac-stats ssy-st">')
    s = s[:i] + m + s[k:]
    s = addcss(s)
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', name)
