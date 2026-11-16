# -*- coding: utf-8 -*-
"""2026-11-16 77 选「合成一个服务器控制台」：服务器租用 / 弹性云 / 裸金属共用 Idc* 页面。
- 7 个服务器页：产品名「服务器租用」→「服务器」，侧栏标题说明改为三种类型
- IdcServers：加「类型」列和类型筛选（原「机房」下拉换成「类型」），加 1 台弹性云、1 台裸金属示例
- 所有控制台页的产品面板：「服务器」组合成一个入口
在 idc_pages.py 之后、panel.py 之后运行，可重复运行。
"""
import re, sys, os, glob
D = sys.argv[1] if len(sys.argv) > 1 else 'console'
IDC = ['IdcServers', 'IdcServerDetail', 'IdcReinstall', 'IdcMonitor', 'IdcLogs', 'IdcProtect', 'IdcSecGroup']
for f in IDC:
    p = os.path.join(D, f + '.dc.html'); s = open(p, encoding='utf-8').read()
    s = s.replace('<span class="kc-ln-c">服务器租用</span>', '<span class="kc-ln-c">服务器</span>')
    s = s.replace('aria-label="服务器租用菜单"', 'aria-label="服务器菜单"')
    s = s.replace('<b>服务器租用</b><span>德迅科技 · 7 台服务器</span>', '<b>服务器</b><span>德迅科技 · 9 台</span>')
    s = s.replace('<a href="IdcServers.dc.html">服务器租用</a>', '<a href="IdcServers.dc.html">服务器</a>')
    open(p, 'w', encoding='utf-8').write(s)

p = os.path.join(D, 'IdcServers.dc.html'); s = open(p, encoding='utf-8').read()
s = s.replace('<h1 class="kc-h1">服务器</h1>', '<h1 class="kc-h1">服务器列表</h1>').replace('<b>服务器</b></nav>', '<b>服务器列表</b></nav>')
if '<th>类型</th>' not in s:
    s = s.replace('<th>服务器</th><th>公网 IP / 线路</th>', '<th>服务器</th><th>类型</th><th>公网 IP / 线路</th>', 1)
    s = s.replace('<td><a href="IdcServerDetail.dc.html">{{r.n}}</a><div class="kc-sub">{{r.id}}</div></td>',
                  '<td><a href="IdcServerDetail.dc.html">{{r.n}}</a><div class="kc-sub">{{r.id}}</div></td><td>{{r.ty}}<div class="kc-sub">{{r.tyS}}</div></td>', 1)
    s = s.replace('<span>机房</span>', '<span>类型</span>', 1)
    s = s.replace('[["全部", ["全部", "温州电信 A 机房", "杭州 BGP 机房"]]', '[["全部", ["全部", "服务器租用", "弹性云服务器", "裸金属服务器"]]', 1)
    s = s.replace("'2026-11-05', '已到期 3 天', 'exp']];",
                  "'2026-11-05', '已到期 3 天', 'exp'],\n      ['ecs-app-01', 'ecs-hz-1032', '47.98.**.61', 'BGP · 10M 按固定带宽', '4 核 / 8G · 系统盘 80G', '杭州 BGP 可用区 B', 'CentOS 7.9', '运行中', 'ok', '17%', '4M', '2027-01-15', '剩 60 天', ''],\n      ['bm-db-01', 'bm-wz-0012', '115.231.**.40', '电信 · 100M 独享', '至强 6330×2 / 256G · NVMe 3.84T×2', '温州电信 A 机房', 'Rocky Linux 9', '运行中', 'ok', '36%', '28M', '2027-03-08', '剩 112 天', '']];", 1)
    s = s.replace("SEC['web-new-05'] = ", "SEC['ecs-app-01'] = ['正常', 'kc-tag ok', '今天 09:12 检测', '']; SEC['bm-db-01'] = ['正常', 'kc-tag ok', '今天 10:05 检测', ''];\n    SEC['web-new-05'] = ", 1)
    s = s.replace("const rows = all.filter((r) => !kk || r.k.indexOf(kk) >= 0);",
                  "const TYM = { 'ecs-app-01': ['弹性云服务器', '按月 · 可升降配'], 'bm-db-01': ['裸金属服务器', '独享物理机'], 'web-prod-01': ['服务器租用', '高防服务器 · 200G'], 'backup-02': ['服务器租用', 'BGP 服务器'] };\n    all.forEach((r) => { const t = TYM[r.n] || ['服务器租用', '电信服务器']; r.ty = t[0]; r.tyS = t[1]; });\n    const __ty = st.ddv0 || '全部';\n    const rows = all.filter((r) => (!kk || r.k.indexOf(kk) >= 0) && (__ty === '全部' || r.ty === __ty));", 1)
    open(p, 'w', encoding='utf-8').write(s)

# 产品面板：服务器组合成一个入口
OLD = re.compile(r"\['服务器', \[\['服务器租用'.*?\]\]\]\];", re.S)
NEW = "['服务器', [['服务器', '租用 / 弹性云 / 裸金属', 'IdcServers.dc.html', 1, '服务器 主机 idc 重装 重启 高防服务器 服务器租用 云服务器 弹性云 ecs 裸金属 物理机']]]];"
n = 0
for p in glob.glob(os.path.join(D, '*.dc.html')):
    s = open(p, encoding='utf-8').read(); o = s
    s = OLD.sub(lambda m: NEW, s, count=1)
    s = s.replace("const favs = st.pfav || ['DDoS 高防 IP', '服务器租用'];", "const favs = st.pfav || ['DDoS 高防 IP', '服务器'];")
    s = s.replace("['服务器租用', 'web-prod-01', 'IdcServerDetail.dc.html']", "['服务器', 'web-prod-01', 'IdcServerDetail.dc.html']")
    if '"服务器": "idc"' not in s:
        s = s.replace('const k = {"应用加速": "scdn",', 'const k = {"服务器": "idc", "应用加速": "scdn",')
    if s != o: open(p, 'w', encoding='utf-8').write(s); n += 1
print('merge ok, panel', n)
