#!/usr/bin/env python3
"""产品与服务弹窗贴住顶栏（幂等，标记 gap-v1）。顶栏实际高 50px，弹窗和遮罩原来从 56px 开始，中间露出 6px。
77（2026-11-19 画板评论）：「切换菜单这里菜单和顶栏不应该有间距的」。
用法: gapfix.py <dir>
"""
import sys, os, glob
CSS = '''
/* gap-v1 产品与服务弹窗贴住顶栏 */
.kc-top .tp-pp{top:100%!important}
.kc-top .tp-dim{top:50px!important}
'''
for p in sorted(glob.glob(os.path.join(sys.argv[1], '*.dc.html'))):
    s = open(p, encoding='utf-8').read()
    if 'gap-v1' in s or 'class="tp-pp"' not in s:
        continue
    j0 = s.index('<x-dc>'); j = s.index('</style>', j0)
    open(p, 'w', encoding='utf-8').write(s[:j] + CSS + s[j:])
    print('ok', os.path.basename(p))
