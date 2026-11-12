# 2026-11-12 (77): product menu follows the live site's groups again, and every entry opens its own page.
# Rail: 精选产品 / 云安全 / 主机安全 / 业务安全 / 安全运营 / 安全服务 / IDC 服务. Run after menu.py.
import re, sys
from menu import mi, head, G, HOST

HOST2 = [(n, 'HostFeature-network.dc.html' if n == '网络访问防护' else h, d) for n, h, d in HOST]
HOT = '<span class="badge b-hot">HOT</span>'
NEW = '<span class="badge b-new">NEW</span>'

def grid(items):
    return G + ''.join(mi(*x) for x in items) + '</div>'

def group(title, items, first=False):
    return ('' if first else '<div class="sep"></div>') + f'<div class="gt">{title}</div>' + grid(items)

def panel(i, groups, pre=''):
    body = pre + ''.join(group(t, it, k == 0 and not pre) for k, (t, it) in enumerate(groups))
    return f'<sc-if value="{{{{show{i}}}}}" hint-placeholder-val="{{{{ {"true" if i == 0 else "false"} }}}}"><div>{body}</div></sc-if>'

P = [
 [('热门产品', [('DDoS 高防 IP', 'ProductDDoS.dc.html', 'T 级防护，近源清洗，业务不中断', HOT), ('游戏盾', 'ProductGame.dc.html', '分布式接入，隐藏源 IP，抗 TCP CC', HOT),
               ('安全加速 SCDN', 'ProductSCDN.dc.html', '加速与 DDoS / CC / WAF 一体'), ('德迅卫士', 'ProductHost.dc.html', '主机安全，AI 研判与威胁狩猎', NEW)]),
  ('推荐组合', [('高防服务器', 'ServerBuy.dc.html', '1000Gbps 以上定制防御'), ('漏洞扫描 VSS', 'ProductVSS.dc.html', 'Web 与系统漏洞检测'),
               ('SSL 证书', 'ProductSSL.dc.html', 'HTTPS 加密，防劫持防篡改'), ('德迅云眼', 'ProductEye.dc.html', '云资产风险持续监测')])],
 [('抗 DDoS', [('DDoS 高防 IP', 'ProductDDoS.dc.html', 'T 级防护，近源清洗，业务不中断', HOT), ('游戏盾', 'ProductGame.dc.html', '分布式接入，隐藏源 IP，抗 TCP CC', HOT),
              ('应用加速', 'ProductAccel.dc.html', '客户端安全接入，切换不断连')]),
  ('Web 与应用安全', [('安全加速 SCDN', 'ProductSCDN.dc.html', '一站式网站安全加速'), ('WAAP 全站防护', 'ProductWAAP.dc.html', 'Web 与 API 一体防护'),
                     ('Web 应用防火墙 WAF', 'ProductWAF.dc.html', '防注入、防篡改、防 CC'), ('SSL 证书', 'ProductSSL.dc.html', 'HTTPS 加密，防劫持防篡改')])],
 None,  # 主机安全 (built below)
 [('云上资产与威胁', [('德迅云眼', 'ProductEye.dc.html', '网站安全监测，云资产风险感知', HOT), ('德迅云图', 'ProductAtlas.dc.html', '威胁检测与分析，情报驱动'),
                     ('态势感知', 'ProductSitu.dc.html', '统一采集分析，威胁可感知')]),
  ('容器与内网', [('德迅蜂巢', 'ProductBeehive.dc.html', '容器安全，从镜像到运行时'), ('德迅零域', 'ProductMicro.dc.html', '微隔离，阻断横向渗透'),
                 ('德迅猎鹰', 'ProductHoneypot.dc.html', '云蜜罐，诱捕并溯源攻击者')])],
 [('检测与合规', [('漏洞扫描 VSS', 'ProductVSS.dc.html', 'Web 与系统漏洞检测'), ('等保合规咨询', 'Services.dc.html#djbh', '从定级到测评全程陪跑', HOT),
                 ('专家服务', 'ServiceExpert.dc.html', '管家式人工服务，全天候护航')]),
  ('审计', [('日志审计', 'ProductLogAudit.dc.html', '日志统一采集与关联分析'), ('数据库审计', 'ProductDBAudit.dc.html', '数据库访问审计与告警'),
           ('堡垒机', 'ProductBastion.dc.html', '运维授权、监察与审计闭环')])],
 [('安全评估', [('渗透测试', 'ServicePentest.dc.html', '比黑客更早发现漏洞'), ('风险评估', 'ServiceRisk.dc.html', '识别资产威胁与脆弱性'),
               ('代码审计', 'ServiceCode.dc.html', '从源代码挖掘安全缺陷'), ('攻防对抗演习', 'ServiceDrill.dc.html', '以攻促防，检验安全水平')]),
  ('应急与保障', [('应急响应', 'ServiceEmergency.dc.html', '7×24 小时处置入侵事件', HOT), ('安全重保', 'ServiceGuard.dc.html', '重大活动前预检、期间值守'),
                 ('驻场支撑', 'ServiceOnsite.dc.html', '工程师现场支撑')]),
  ('托管运维', [('安全代维', 'ServiceOps.dc.html', '接入、配置、策略优化与预警'), ('日志分析', 'ServiceLog.dc.html', '访客与威胁情报分析'),
               ('专家报告', 'ServiceReport.dc.html', '人工出具安全态势报告')])],
 [('服务器', [('高防服务器', 'ServerBuy.dc.html', '1000Gbps 以上定制防御', HOT), ('电信服务器', 'ServerBuy.dc.html?t=1', '骨干直连，¥399/月起'),
             ('高性能服务器', 'ServerBuy.dc.html?t=2', '单核性能约 1.5 倍')]),
  ('云计算', [('裸金属服务器', 'ProductBareMetal.dc.html', '物理机性能，分钟级交付'), ('弹性云服务器', 'ProductECS.dc.html', '弹性伸缩的计算服务', HOT)])],
]
HOSTP = (f'<sc-if value="{{{{show2}}}}" hint-placeholder-val="{{{{ false }}}}"><div><div class="gt">主机安全</div>{head}'
         f'<div class="sep"></div><div class="gt">核心能力</div>{grid(HOST2)}</div></sc-if>')
NAMES = '["精选产品", "云安全", "主机安全", "业务安全", "安全运营", "安全服务", "IDC 服务"]'

def build_panels():
    return ''.join(HOSTP if i == 2 else panel(i, g) for i, g in enumerate(P))

for f in sys.argv[1:]:
    s = open(f).read()
    a = s.find('<sc-if value="{{show0}}"')
    last = max(re.finditer(r'<sc-if value="\{\{show(\d)\}\}"', s), key=lambda m: int(m.group(1)))
    b = s.find('</sc-if>', last.start()) + len('</sc-if>')
    s = s[:a] + build_panels() + s[b:]
    s = re.sub(r'const names = \[[^\]]*\];', 'const names = ' + NAMES + ';', s)
    open(f, 'w').write(s)
    print('ok', f)
