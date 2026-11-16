# -*- coding: utf-8 -*-
"""2026-11-16 控制台顶栏「产品与服务」面板：分组对齐官网（云安全 / 主机安全 / 业务安全 / 安全运营 / 服务器），
删掉官网已下线的日志审计、数据库审计、应用加固、身份核验和机柜托管；未开通产品不再是 '#'，按面板底部说明进官网产品页。
可重复运行。用法：python3 panel.py <repo>/console
"""
import re, sys, os, glob
D = sys.argv[1] if len(sys.argv) > 1 else 'console'
NEW = """const P = [['云安全', [['DDoS 高防 IP', '大流量攻击清洗', 'DdosInstances.dc.html', 1, 'ddos 高防'], ['游戏盾', '游戏 TCP/UDP 防护', 'GameAccess.dc.html', 1, 'game'], ['SCDN', '加速 + Web 防护', 'Main.dc.html', 1, 'cdn 加速 域名 证书'],
        ['应用加速', '跨地域跨运营商加速', '../ProductAccel.dc.html', 0, '加速'], ['WAAP 全站防护', 'Web 与 API 一体防护', '../ProductWAAP.dc.html', 0, 'waap api'], ['Web 应用防火墙', 'WAF', '../ProductWAF.dc.html', 0, 'waf'], ['SSL 证书', 'HTTPS 加密', 'AcctProducts.dc.html', 1, '证书 https ssl']]],
      ['主机安全', [['德迅安全卫士', '安全中心 · 主机安全', 'SecHome.dc.html', 1, '主机 hids 卫士 安全中心 告警 漏洞 基线 入侵']]],
      ['业务安全', [['德迅云眼', '网站安全监测', 'EyeRisk.dc.html', 1, '监测 暗链 篡改'], ['德迅云图', '威胁检测与分析', '../ProductAtlas.dc.html', 0, '威胁'], ['态势感知', '安全态势总览', '../ProductSitu.dc.html', 0, '态势'], ['德迅蜂巢', '容器安全', '../ProductBeehive.dc.html', 0, '容器 k8s'], ['德迅零域', '微隔离', '../ProductMicro.dc.html', 0, '微隔离'], ['德迅猎鹰', '云蜜罐', '../ProductHoneypot.dc.html', 0, '蜜罐']]],
      ['安全运营', [['漏洞扫描 VSS', '网站与主机漏洞', 'AcctProducts.dc.html', 1, 'vss 漏洞'], ['等保合规', '等保咨询与测评', '../Services.dc.html#djbh', 0, '等保']]],
      ['服务器', [['服务器租用', '高防 / 电信 / 高性能', 'IdcServers.dc.html', 1, '服务器 主机 idc 重装 重启 高防服务器'], ['弹性云服务器', '弹性伸缩的云主机', '../ProductECS.dc.html', 0, 'ecs 云服务器 云主机'], ['裸金属服务器', '独享物理机', '../ProductBareMetal.dc.html', 0, '裸金属 物理机']]]];"""
pat = re.compile(r"const P = \[\['云安全', \[\[.*?\]\]\]\];", re.S)
n = 0
for p in sorted(glob.glob(os.path.join(D, '*.dc.html'))):
    s = open(p, encoding='utf-8').read(); o = s
    s = pat.sub(lambda m: NEW, s, count=1)
    s = s.replace("href: op ? href : '#'", "href")  # 未开通也给真实地址（官网产品页）
    if s != o:
        open(p, 'w', encoding='utf-8').write(s); n += 1
print('patched', n)

# 我的产品：德迅安全卫士「进入控制台」点了没反应 → 安全中心；等保咨询名字 → 服务报告
p = os.path.join(D, 'AcctProducts.dc.html'); s = open(p, encoding='utf-8').read()
s = s.replace("[{ t: '德迅安全卫士', a: '#' }", "[{ t: '德迅安全卫士', a: 'SecHome.dc.html' }")
s = s.replace("{ t: '已到期 · 保留中', tag: 'err' }], [['进入控制台'], ['续费', 'BillConfirm.dc.html']]", "{ t: '已到期 · 保留中', tag: 'err' }], [['进入控制台', 'SecHome.dc.html'], ['续费', 'BillConfirm.dc.html']]")
s = s.replace("[{ t: '等保咨询', a: '#' }", "[{ t: '等保咨询', a: 'SupDocs.dc.html' }")
open(p, 'w', encoding='utf-8').write(s)

# 规格板 Switcher：静态面板里的 '#' 按同样规则改
p = os.path.join(D, 'Switcher.dc.html'); s = open(p, encoding='utf-8').read()
MAP = {'用户中心': 'ConsoleHome.dc.html', '费用': 'BillOverview.dc.html', 'Web 应用防火墙': '../ProductWAF.dc.html', '德迅零域': '../ProductMicro.dc.html', '德迅蜂巢': '../ProductBeehive.dc.html', '德迅猎鹰': '../ProductHoneypot.dc.html',
       '德迅云图': '../ProductAtlas.dc.html', '态势感知': '../ProductSitu.dc.html', '等保合规': '../Services.dc.html#djbh', '云服务器': '../ProductECS.dc.html', '裸金属': '../ProductBareMetal.dc.html', '查看全部产品与价格': 'AcctPurchase.dc.html'}
def fix(m):
    a = m.group(0)
    for k, v in MAP.items():
        if re.search(r'>\s*(<[^>]+>\s*)*' + re.escape(k), a):
            return a.replace('href="#"', 'href="%s"' % v, 1)
    return a
s = re.sub(r'<a [^>]*href="#"[^>]*>.{0,160}?</a>', fix, s, flags=re.S)
open(p, 'w', encoding='utf-8').write(s)
print('acct+switcher ok')

# 面板新名字补图标（复用现有图标）
ADD = '"应用加速": "scdn", "WAAP 全站防护": "waf", "弹性云服务器": "idc", "裸金属服务器": "idc", '
for p in sorted(glob.glob(os.path.join(D, '*.dc.html'))):
    s = open(p, encoding='utf-8').read()
    if '"应用加速": "scdn"' in s: continue
    s2 = s.replace('const k = {"DDoS 高防 IP": "ddos",', 'const k = {' + ADD + '"DDoS 高防 IP": "ddos",')
    if s2 != s: open(p, 'w', encoding='utf-8').write(s2)
print('icons ok')
