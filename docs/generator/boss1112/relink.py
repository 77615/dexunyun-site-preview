# 2026-11-12: point every link whose title names a page that now exists at that page (only when it
# currently goes to a generic fallback such as the overview page). usage: python3 relink.py <files...>
import re, sys

MAP = {
 'Web 应用防火墙 WAF': 'ProductWAF.dc.html', 'Web 应用防火墙': 'ProductWAF.dc.html', 'WAF': 'ProductWAF.dc.html',
 'WAAP': 'ProductWAAP.dc.html', 'WAAP 全站防护': 'ProductWAAP.dc.html', 'WAAP全站防护': 'ProductWAAP.dc.html',
 '应用加速': 'ProductAccel.dc.html', '德迅蜂巢': 'ProductBeehive.dc.html', '容器安全': 'ProductBeehive.dc.html',
 '德迅猎鹰': 'ProductHoneypot.dc.html', '云蜜罐': 'ProductHoneypot.dc.html', '德迅零域': 'ProductMicro.dc.html', '微隔离': 'ProductMicro.dc.html',
 '德迅云图': 'ProductAtlas.dc.html', '威胁检测与分析': 'ProductAtlas.dc.html', '态势感知': 'ProductSitu.dc.html',
 '网络访问防护': 'HostFeature-network.dc.html', '裸金属服务器': 'ProductBareMetal.dc.html', '弹性云服务器': 'ProductECS.dc.html',
 '专家服务': 'ServiceExpert.dc.html', '渗透测试': 'ServicePentest.dc.html', '风险评估': 'ServiceRisk.dc.html', '代码审计': 'ServiceCode.dc.html',
 '攻防对抗演习': 'ServiceDrill.dc.html', '攻防演练': 'ServiceDrill.dc.html', '信息安全对抗演习': 'ServiceDrill.dc.html',
 '应急响应': 'ServiceEmergency.dc.html', '网络安全应急中心': 'ServiceEmergency.dc.html', '安全重保': 'ServiceGuard.dc.html',
 '驻场支撑': 'ServiceOnsite.dc.html', '安全代维': 'ServiceOps.dc.html', '日志分析': 'ServiceLog.dc.html', '专家报告': 'ServiceReport.dc.html',
 '新闻媒体': 'SolutionMedia.dc.html', '元宇宙': 'SolutionMeta.dc.html', 'SASE 安全接入': 'SolutionSASE.dc.html', 'SASE': 'SolutionSASE.dc.html',
 '公安监督检查': 'SolutionPolice.dc.html', '办公网络安全': 'SolutionOffice.dc.html', '网络空间资产': 'SolutionCyber.dc.html',
 '常见问题': 'Faq.dc.html', '行业白皮书': 'Whitepaper.dc.html', '产品白皮书': 'Whitepaper.dc.html', '备案中心': 'Beian.dc.html',
 '意见反馈': 'Feedback.dc.html', '推广合作': 'Partner.dc.html', '举报中心': 'Report.dc.html',
}
FALLBACK = re.compile(r'^(Products|Services|Solutions|Docs|Contact|ProductSCDN|ProductHost|ServerBuy|About|Main)\.dc\.html(\?t=\d)?$|^#$')
A = re.compile(r'<a href="([^"]*)"([^>]*)>(.*?)</a>', re.S)

def title(inner):
    parts = [p.strip() for p in re.split(r'<[^>]+>', inner) if p.strip()]
    if not parts:
        return ''
    t = parts[0]
    return re.sub(r'\s*(HOT|NEW)$', '', t)

def fix(s):
    n = 0
    def rep(m):
        nonlocal n
        h, attrs, inner = m.groups()
        t = title(inner)
        if t in MAP and FALLBACK.match(h) and MAP[t] != h:
            n += 1
            return f'<a href="{MAP[t]}"{attrs}>{inner}</a>'
        return m.group(0)
    return A.sub(rep, s), n

if __name__ == '__main__':
    for f in sys.argv[1:]:
        s = open(f).read()
        s2, n = fix(s)
        if n:
            open(f, 'w').write(s2)
            print(f, n)
