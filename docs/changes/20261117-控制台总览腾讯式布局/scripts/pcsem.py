#!/usr/bin/env python3
"""我的产品卡片版：按腾讯控制台规范整理语义色和页面元素（幂等，标记 pcsem-v1，需在 pc.py 之后跑）。
规则（腾讯设计文档 #semantic / #detail）：
- 状态分三档轻重：需立刻处理（攻击中 / 已到期）= 错误浅色标签；需要关注（即将到期 / 接近上限）= 警告浅色标签；
  只需知晓（运行中 / 已完成）= 单独的图标 + 灰字，不加底色。
- 浅底上的字和图标用 9 阶（错误 #b42c3f、警告 #c04100）；单独出现的状态图标、文字、进度条用 8 阶
  （错误 #f64041、警告 #ff7800、成功 #0cbf5b）；中性用 #e9ecf1 底 + 黑 50% 字。
- 文字用黑色透明度 .9 / .7 / .5，正文 12/20；产品图标块只用蓝 #e3ecff、薄荷 #d3f4ef、灰 #e5e9f0 三种淡彩，按分类区分。
- 进度条直角 4px，轨道 #e6e9ef，纯色不用渐变；卡片悬停只加 md 阴影，不加蓝框；选中才用品牌色描边。
- 需处理的计数用红色数字。
用法: pcsem.py AcctProducts.dc.html
"""
import sys

CSS = r'''
/* pcsem-v1 语义色和元素（腾讯控制台规范） */
.pc{--e1:#fce8e8;--e8:#f64041;--e9:#b42c3f;--w1:#ffeddf;--w8:#ff7800;--w9:#c04100;--s1:#e7f8f0;--s8:#0cbf5b;--s9:#088f50;--n1:#e9ecf1;--t9:rgba(0,0,0,.9);--t7:rgba(0,0,0,.7);--t5:rgba(0,0,0,.5);--t3:rgba(0,0,0,.3)}
.pc .pc-mk.err{background:var(--e8)}.pc .pc-mk.warn{background:var(--w8)}.pc .pc-mk.ok{background:var(--s8)}.pc .pc-mk.mut{background:#bcc4d0}
.pc .pc-chip,.pc-dw .pc-chip{height:20px;padding:0 6px;border-radius:2px!important;font-size:12px;font-weight:400;line-height:20px;gap:4px}
.pc .pc-chip.err,.pc-dw .pc-chip.err{background:var(--e1,#fce8e8);color:var(--e9,#b42c3f)}
.pc .pc-chip.err .pc-mk,.pc-dw .pc-chip.err .pc-mk{background:var(--e9,#b42c3f)}
.pc .pc-chip.warn,.pc-dw .pc-chip.warn{background:var(--w1,#ffeddf);color:var(--w9,#c04100)}
.pc .pc-chip.warn .pc-mk,.pc-dw .pc-chip.warn .pc-mk{background:var(--w9,#c04100)}
.pc .pc-chip.ok,.pc-dw .pc-chip.ok{padding:0;background:none;color:rgba(0,0,0,.7)}
.pc .pc-chip.ok .pc-mk,.pc-dw .pc-chip.ok .pc-mk{background:#0cbf5b}
.pc .pc-chip.mut,.pc-dw .pc-chip.mut{padding:0;background:none;color:rgba(0,0,0,.5)}
.pc .pc-chip.mut .pc-mk,.pc-dw .pc-chip.mut .pc-mk{background:#bcc4d0}
.pc .pc-st{color:var(--t7)}
.pc .pc-ico,.pc-dw .pc-ico{border-radius:0;background:#e3ecff}
.pc .pc-ico.t2,.pc-dw .pc-ico.t2{background:#d3f4ef}
.pc .pc-ico.t3,.pc-dw .pc-ico.t3{background:#e5e9f0}
.pc .pc-nm b{font-weight:500;color:var(--t9)}
.pc .pc-nm small{color:var(--t5)}
.pc .pc-tx{font-size:12px;line-height:20px;color:var(--t7)}
.pc .pc-ub{height:4px;border-radius:0;background:#e6e9ef}
.pc .pc-ub i,.pc .pc-ub i.o,.pc .pc-ub i.r{border-radius:0;background:#1664ff}
.pc .pc-ub i.o{background:var(--w8)}
.pc .pc-ub i.r{background:var(--e8)}
.pc .pc-u em{color:var(--t5)}
.pc .pc-u:has(i.r) em{color:var(--e8)}
.pc .pc-u:has(i.o) em{color:var(--w8)}
.pc .pc-ex{color:var(--t5)}
.pc .pc-ex.o{color:var(--w8)}
.pc .pc-ex.r{color:var(--e8)}
.pc .pc-c{box-shadow:0 0 0 1px #e9ecf1}
.pc .pc-c:hover{box-shadow:0 0 0 1px #e6e9ef,0 8px 24px -4px rgba(0,0,0,.1),0 8px 12px -8px rgba(0,0,0,.05)}
.pc .pc-c.cur{box-shadow:0 0 0 1px #1664ff,0 8px 24px -4px rgba(0,0,0,.1)}
.pc .pc-ft{background:#f7f8fb;border-top-color:#f0f2f5;font-size:12px}
.pc .pc-act,.pc .pc-con{color:var(--t9)}
.pc .pc-act:hover,.pc .pc-con:hover{color:#1664ff}
.pc .pc-act.pri{color:#1664ff;font-weight:400}
.pc .pc-lh>span{background:var(--n1);color:var(--t5)}
.pc .pc-sc button>.pc-n{color:var(--t5)}
.pc .pc-sc button>.pc-n.r{color:var(--e8);font-weight:500}
.pc .pc-rp{color:var(--t5)}.pc .pc-rt{color:var(--t7)}
.pc .pc-rw{font-size:12px}
.pc .pc-rw:hover,.pc .pc-c.cur .pc-rw{background:#f7f8fb}
.pc-dw .pc-dd{font-size:12px;line-height:20px;color:rgba(0,0,0,.7)}
.pc-dw .pc-kv{font-size:12px}
.pc-dw .pc-kv dt{color:rgba(0,0,0,.5)}
.pc-dw .pc-steps{background:#f7f8fb}
.pc-dw .pc-steps li{font-size:12px;color:rgba(0,0,0,.7)}
.pc-dw .pc-steps time{color:rgba(0,0,0,.5)}
'''

R = [
    # 图标块按分类上淡彩
    ('<span class="pc-tt"><span class="pc-ico"><i class="{{p.di}}"></i></span>', '<span class="pc-tt"><span class="{{p.ic}}"><i class="{{p.di}}"></i></span>'),
    ('<span class="pc-rn"><span class="pc-ico sm"><i class="{{p.di}}"></i></span>', '<span class="pc-rn"><span class="{{p.icS}}"><i class="{{p.di}}"></i></span>'),
    ('<div class="pc-dh"><span class="pc-ico"><i class="{{pcD.di}}"></i></span>', '<div class="pc-dh"><span class="{{pcD.ic}}"><i class="{{pcD.di}}"></i></span>'),
    # 列表视图和抽屉的状态也用同一套标签
    ('<span class="pc-st"><i class="{{p.mk}}"></i>{{p.sw}}</span>', '<span class="pc-st"><span class="{{p.chip}}"><i class="{{p.mk}}"></i>{{p.sw}}</span></span>'),
    ('<span class="{{pcD.tag}}">{{pcD.sw}}</span>', '<span class="{{pcD.tag}}"><i class="{{pcD.mk}}"></i>{{pcD.sw}}</span>'),
    # 需处理计数红色
    ('<em class="pc-n">{{s.c}}</em>', '<em class="{{s.nc}}">{{s.c}}</em>'),
    # JS
    ("const TAG = { err: 'kc-tag err', warn: 'kc-tag warn', ok: 'kc-tag ok', mut: 'kc-tag mut' };",
     "const TAG = { err: 'pc-chip err', warn: 'pc-chip warn', ok: 'pc-chip ok', mut: 'pc-chip mut' };\n    const TINT = { '云安全': '', '主机安全': ' t2', '安全运营': ' t2', 'IDC 服务': ' t3', '安全服务': ' t3' };"),
    ("map(([k, n, c]) => ({ n, c, on:", "map(([k, n, c]) => ({ n, c, nc: k === 'need' && c ? 'pc-n r' : 'pc-n', on:"),
    ("chip: 'pc-chip ' + p[6],", "chip: 'pc-chip ' + p[6], ic: 'pc-ico' + (TINT[p[3]] || ''), icS: 'pc-ico sm' + (TINT[p[3]] || ''),"),
    ("tag: TAG[D[6]], di:", "tag: TAG[D[6]], mk: 'pc-mk ' + D[6], ic: 'pc-ico' + (TINT[D[3]] || ''), di:"),
    ("{ n: '', plan: '', text: '', sw: '', tag: '', di: '',", "{ n: '', plan: '', text: '', sw: '', tag: '', mk: '', ic: 'pc-ico', di: '',"),
]

for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    if 'pcsem-v1' in s:
        print('skip', p); continue
    for a, b in R:
        n = s.count(a)
        if n != 1:
            sys.exit(f'pattern count {n}: {a[:60]}')
        s = s.replace(a, b)
    i = s.index('<x-dc>'); j = s.index('</style>', i)
    s = s[:j] + CSS + s[j:]
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', p)
