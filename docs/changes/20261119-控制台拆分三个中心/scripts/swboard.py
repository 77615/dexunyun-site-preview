#!/usr/bin/env python3
"""「产品与服务 · 切换菜单」规范板改成和当前顶栏一致（标记 swb-v1）：用总览页复制，菜单默认展开。
77（2026-11-19 画板评论）：「这个菜单的画板没有更新吗」。
用法: swboard.py ConsoleHome.dc.html Switcher.dc.html
"""
import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
k = s.index("prodOn: dd === 'prod'")
a = s.rfind("const dd = st.dd || '';", 0, k)
assert a > 0
s = s[:a] + "const dd = st.dd === undefined ? 'prod' : st.dd; /* swb-v1 规范板默认展开产品与服务菜单 */" + s[a + len("const dd = st.dd || '';"):]
s = re.sub(r'<title>[^<]*</title>', '<title>产品与服务切换菜单</title>', s, count=1)
s = s.replace('data-pg="ConsoleHome"', 'data-pg="Switcher"', 1)
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
