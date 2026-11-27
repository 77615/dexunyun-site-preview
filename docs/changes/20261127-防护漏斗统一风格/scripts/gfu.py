#!/usr/bin/env python3
"""防护漏斗统一到安全总览（腾讯式）风格。幂等，marker gfu-v1。
用法：python3 gfu.py console/SecHome.dc.html
- 图标：五色线性 → 与「防护能力」相同的面性图标 + 方形浅底块（防护层蓝，进入/放行灰）
- 条形：圆角渐变 + 多色端头 + 扫光 → 方角纯色，放行 #1664ff，拦截部分 #c7ccd6（同趋势图）
- 字号：12/500 名称、12 灰色说明、13/600 数字；时间范围用 sh-seg 同款分段
- 右侧明细：阴影小卡 → #f7f8fb 平面格；操作改蓝色文字链接
"""
import re, sys

MARK = 'gfu-v1'
f = sys.argv[1]
s = open(f, encoding='utf-8').read()
if MARK in s:
    print('already'); sys.exit(0)

def ic(name):
    m = re.search(r"\.sh-ci\.%s\{--ic:(url\('[^']*'\))" % name, s)
    assert m, name
    return m.group(1)

def svg(d):
    return ("url('data:image/svg+xml,%3Csvg viewBox=\"0 0 24 24\" fill=\"%23000\" xmlns=\"http://www.w3.org/2000/svg\"%3E%3Cpath d=\""
            + d + "\"/%3E%3C/svg%3E')")

ICON = {
    # Remix arrow-right-circle-fill
    'in': svg('M12 2C17.52 2 22 6.48 22 12C22 17.52 17.52 22 12 22C6.48 22 2 17.52 2 12C2 6.48 6.48 2 12 2ZM12 11H8V13H12V16L16 12L12 8V11Z'),
    # Remix shield-check-fill
    'fw': svg('M3.78307 2.82598L12 1L20.2169 2.82598C20.6745 2.92766 21 3.33347 21 3.80217V13.7889C21 15.795 19.9974 17.6684 18.3282 18.7812L12 23L5.6718 18.7812C4.00261 17.6684 3 15.795 3 13.7889V3.80217C3 3.33347 3.32553 2.92766 3.78307 2.82598ZM11.2071 13.1716L8.37868 10.3431L6.96447 11.7574L11.2071 16L17.5711 9.63604L16.1569 8.22183L11.2071 13.1716Z'),
    'ids': ic('ic0'),   # 与防护能力「入侵检测」同一图标
    'av': ic('ic4'),    # 与防护能力「病毒查杀」同一图标
    # Remix checkbox-circle-fill
    'out': svg('M12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22ZM11.0026 16L18.0737 8.92893L16.6595 7.51472L11.0026 13.1716L8.17421 10.3431L6.75999 11.7574L11.0026 16Z'),
}

css = ['/* gfu-v1 防护漏斗统一到安全总览风格（2026-11-27） */']
P = '.sh-gf '
css += [
 P+'.gf2{padding:20px 24px 24px;font-size:12px;color:rgba(0,0,0,.7)}',
 P+'.gf2-bar{min-height:28px;margin-bottom:16px;gap:12px}',
 P+'.gf2-tt{font-size:16px;font-weight:600;line-height:22px;color:rgba(0,0,0,.9)}',
 P+'.gf2-tot{font-size:12px;color:rgba(0,0,0,.5)}',
 P+'.gf2-tot b{margin-left:2px;font-weight:600;color:rgba(0,0,0,.9)}',
 P+'.gf2-st{gap:16px}',
 P+'.gf2-live{font-size:12px;font-weight:400;color:rgba(0,0,0,.5)}',
 P+'.gf2-live i{background:#24b47e}',
 # 时间范围 = sh-seg
 P+'.gf2-rg{gap:0;padding:2px;background:#f2f4f8}',
 P+'.gf2-rg button{height:26px;padding:0 12px;border-radius:0;font-size:12px;font-weight:400;line-height:26px;color:rgba(0,0,0,.7)}',
 P+'.gf2-rg button:hover{color:#1664ff}',
 P+'.gf2-rg button.on{background:#fff;color:#1664ff;font-weight:500;box-shadow:0 1px 2px rgba(0,0,0,.06)}',
 # 行
 P+'.gf2-stages{grid-template-rows:repeat(5,44px);margin:0 -12px}',
 P+'.gf2-row{padding:0 12px;border-radius:0}',
 P+'.gf2-row:hover{background:#f7f8fb}',
 P+'.gf2-row.on{background:#f2f4f8}',
 P+'.gf2-nm{grid-template-columns:28px minmax(0,1fr);column-gap:10px;align-items:center}',
 P+'.gf2-hd{display:contents}',
 P+'.gf2-ic{grid-row:1/3;width:28px;height:28px;background:#e8f3ff;color:#1664ff!important;-webkit-mask:none;mask:none;display:flex;align-items:center;justify-content:center}',
 P+'.gf2-ic::before{content:"";width:16px;height:16px;background:currentColor;-webkit-mask:var(--ic) center/contain no-repeat;mask:var(--ic) center/contain no-repeat}',
 P+'.gf2-ic.i-in,'+P+'.gf2-ic.i-out{background:#f2f4f8;color:rgba(0,0,0,.5)!important}',
 P+'.gf2-lb{font-size:12px;font-weight:500;line-height:18px;color:rgba(0,0,0,.9)}',
 P+'.gf2-mt{padding-left:0;font-size:12px;line-height:18px;color:rgba(0,0,0,.5)}',
 P+'.gf2-cnt{font-size:13px;font-weight:600;line-height:18px;color:rgba(0,0,0,.9)}',
 P+'.gf2-pct{font-size:12px;line-height:18px;color:rgba(0,0,0,.5)}',
 # 漏斗图：方角纯色，同趋势图配色
 P+'.gf2-tp{fill:#1664ff;fill-opacity:.05}',
 P+'.gf2-st2{height:12px}',
 P+'.gf2-end{border-radius:0;background:#e1e5eb;box-shadow:none}',
 P+'.gf2-core,'+P+'.gf2-core.last{border-radius:0;background:#94bfff;box-shadow:none}',
 P+'.gf2-sh{display:none}',
 # 右侧明细
 P+'.gf2-pn{border-color:#e9ecf1}',
 '@container gf2 (min-width: 960px){'+P+'.gf2-pn{margin-left:24px;padding-left:24px;border-left:1px solid #e9ecf1}}',
 P+'.gf2-ph{height:22px;align-items:center}',
 P+'.gf2-ph b{font-size:13px;font-weight:600;color:rgba(0,0,0,.9)}',
 P+'.gf2-ph span{font-size:12px;color:rgba(0,0,0,.5)}',
 P+'.gf2-exs{grid-auto-rows:52px;gap:8px}',
 P+'.gf2-ex,'+P+'.gf2-pt{padding:0 16px;border-radius:0;background:#f7f8fb;box-shadow:none}',
 P+'.gf2-et{font-size:12px;line-height:18px;color:rgba(0,0,0,.9)}',
 P+'.gf2-et.code{font-size:12px}',
 P+'.gf2-hit{padding:0 2px;border-radius:0;background:#e8f3ff;color:#1664ff}',
 P+'.gf2-em{height:18px;font-size:12px;line-height:18px;color:rgba(0,0,0,.5)}',
 P+'.gf2-em .t{color:rgba(0,0,0,.4)}',
 P+'.gf2-act{height:auto;padding:0;border-radius:0;background:none;box-shadow:none;font-size:12px;font-weight:400;color:#1664ff}',
 P+'.gf2-act:hover{background:none;color:#4086ff}',
 P+'.gf2-dn{font-size:12px;font-weight:400;color:rgba(0,0,0,.5)}',
 P+'.gf2-dn i{color:#24b47e}',
 P+'.gf2-pl{font-size:12px;line-height:18px}',
 P+'.gf2-pl .l{color:rgba(0,0,0,.9)}',
 P+'.gf2-pl .n,'+P+'.gf2-pl .p{font-size:12px;color:rgba(0,0,0,.5)}',
 P+'.gf2-pl .v{font-weight:600;color:rgba(0,0,0,.9)}',
 P+'.gf2-tr{height:4px;border-radius:0;background:#e6e9ef;box-shadow:none}',
 P+'.gf2-fl{border-radius:0;background:#94bfff;box-shadow:none}',
]
for k, v in ICON.items():
    css.append(P + '.gf2-ic.i-%s{--ic:%s}' % (k, v))

block = '\n'.join(css) + '\n'
anchor = '/* cnav-v1 三个中心的导航入口 */'
assert s.count(anchor) == 1
s = s.replace(anchor, block + anchor)

# 漏斗条高 12px（原 16），行高 44（原 40）：同步 SVG 过渡带和条形位置
old_tp = "const t = i * 40 + 28, u = (i + 1) * 40 + 12"
new_tp = "const t = i * 44 + 28, u = (i + 1) * 44 + 16"
assert s.count(old_tp) == 1
s = s.replace(old_tp, new_tp)
old_top = "';top:' + (i * 40 + 12) + 'px;"
assert s.count(old_top) == 1
s = s.replace(old_top, "';top:' + (i * 44 + 16) + 'px;")
old_vb = '<svg viewBox="0 0 1000 200" preserveAspectRatio="none">'
assert s.count(old_vb) == 1
s = s.replace(old_vb, '<svg viewBox="0 0 1000 220" preserveAspectRatio="none">')

open(f, 'w', encoding='utf-8').write(s)
print('ok')
