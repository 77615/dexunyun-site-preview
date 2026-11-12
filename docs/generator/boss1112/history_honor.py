# boss #7/#8 (2026-11-12): 发展历程 = year selector + full year list; 资质荣誉 = 3 tabs with all 61 items (source: live dexun.com /history, /honor)
import re,sys
H={2026:'''09-14 多位成员受聘为温州市网络安全专家
08-11 入选安全牛《中国网络安全行业全景图（第十三版）》
07-27 入选中国信通院《数字安全护航技术能力全景图》
07-01 党支部获评“龙港市先进基层党组织”
05-18 再度入选《嘶吼 2026 网络安全产业图谱》
03-19 受邀与温州市网安支队共商全市网络安全生态''',
2025:'''09-26 董事长叶德望受聘华侨大学研究生导师
09-10 再次入选温州市网络和数据安全技术支撑单位
08-20 入选数说安全全景图，覆盖云安全与应用安全两个领域
07-03 UEBA 方案入选嘶吼安全 2025 中国网络安全优秀解决方案
05-27 入选《嘶吼 2025 网络安全产业图谱》多个领域
05-20 成为全国网络安全标准化技术委员会 WG5 成员单位
05-08 入选安全牛《中国网络安全行业全景图》多项细分领域''',
2024:'''07-05 获 2024 年温州市互联网企业“Z 世代”比赛三等奖
07-04 入选数说安全《2024 年中国网络安全市场全景图》
05-24 入选国家信息安全漏洞库（CNNVD）技术支撑单位
03-28 入选 CCIA “2024 年网络安全服务阳光行动”成员单位
03-09 在西安成立 APT 研究实验室
02-21 获中共龙港市委授予“网络安全顾问单位”''',
2023:'''11-09 获评省级高新技术企业研究开发中心
10-25 与华侨大学战略合作并授牌
09-12 入选温州市网络安全技术支撑单位
09-11 入选 2022 年度“浙江省网安成长十强”企业
06-20 获温州市“护航亚运”网络安全实战攻防演练“优秀攻击团队”
05-12 获“2022-2023 年度数字化创新优秀实践单位”
02-15 获评市级高新技术企业研究开发中心
01-23 入选 2022 年度浙江省专精特新企业''',
2022:'''12-15 德迅卫士推出企业级一站式私有云安全中心方案
11-27 入选国内网络安全行业全景图
09-05 获“2022 年温州网络安全宣传周短视频大赛”优秀作品
07-13 CEO 叶德望获“2021-2022 网络信息安全影响力人物”
01-20 在网络安全和信息化杂志社获奖''',
2021:'''12-24 获“2021 年度网络安全企业之星”
11-09 CEO 获“温州创业新锐人物奖”
07-12 当选浙江省高新技术企业协会理事单位
05-05 获“2020 中国网络信息卓越企业奖”
03-09 安全云加速正式上线
02-11 漏洞扫描系统正式上线''',
2020:'''12-16 当选浙江省互联网协会理事单位
12-05 获“中国 CSA 安全创新奖”
12-04 与 360、腾讯安全、安恒信息共同协办云安全联盟大中华区大会
12-01 获评国家高新技术企业
11-12 系统通过公安部信息系统安全等级保护备案
10-24 获“2020 行业信息化创新企业”“创新产品”
06-19 获评国家科技型中小企业
01-08 更名为浙江德迅网络安全技术有限公司，启用 dexunyun.com
01-03 获 ISO/IEC 27001 信息安全管理体系认证
01-02 获软件企业认证与软件产品认证（双软）''',
2019:'''12-26 受国家互联网应急中心邀请加入网络安全空间治理联盟（CCTGA）
12-02 成为中国 CSA 云安全联盟成员
10-15 成为浙江网络空间安全协会理事单位
08-09 成为中国网络空间安全协会成员
03-24 发布网游安全解决方案“游戏盾”
01-05 自定义微隔离上线''',
2018:'''12-10 “门神”安全软件升级至 2.2 版
08-16 与中国电信（温州）战略合作
05-03 获 ISO 9001 质量管理体系认证
04-06 推出攻击溯源服务''',
2017:'''10-01 官网焕新上线
09-28 DDoS 高防 IP 上线
09-10 德迅卫士 V2.2.0 上线，新增云监控、门神、必加锁
01-15 与温州电信合作近源清洗服务
01-04 获工信部 ISP/IDC 业务牌照''',
2016:'''04-28 德迅 WAF 安全防火墙发布
03-09 德迅抗拒绝服务系统发布''',
2015:'''12-01 德迅卫士 V1.0 正式发布
10-12 1V1 专席秘书服务上线
05-02 研发团队成立
01-13 温州德迅网络科技有限公司成立'''}
KEY={2026:'入选信通院、安全牛全景图',2025:'全国信安标委 WG5 成员',2024:'CNNVD 技术支撑单位',2023:'省级研发中心 · 专精特新',2022:'私有云安全中心',2021:'安全云加速上线',2020:'国家高新技术企业',2019:'发布游戏盾',2018:'ISO 9001 认证',2017:'DDoS 高防 IP 上线',2016:'WAF 发布',2015:'公司成立'}
YEARS=sorted(H)  # 2015..2026
HCSS='''
.hy12{margin-top:56px}
.hy12-rail{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(12,minmax(0,1fr));position:relative}
.hy12-rail::before{content:"";position:absolute;left:0;right:0;top:41px;height:1px;background:#E5E6EB}
.hy12-rail li{position:relative}
.hy12-rail button{all:unset;cursor:pointer;display:flex;flex-direction:column;gap:12px;width:100%;box-sizing:border-box;padding-right:8px}
.hy12-rail b{font-family:"DIN Alternate","Helvetica Neue",Arial,sans-serif;font-size:22px;line-height:28px;font-weight:600;color:#C9CDD4;transition:color .2s}
.hy12-rail i{display:block;width:9px;height:9px;border-radius:50%;background:#FFFFFF;border:1.5px solid #C9CDD4;box-sizing:border-box;transition:all .2s}
.hy12-rail span{font-size:12px;line-height:18px;color:#86909C;padding-right:4px}
.hy12-rail button:hover b{color:#4E5969}
.hy12-rail button.on b{color:#165DFF}
.hy12-rail button.on i{background:#165DFF;border-color:#165DFF;box-shadow:0 0 0 5px rgba(22,93,255,.12)}
.hy12-rail button.on span{color:#1D2129}
.hy12-pn{margin-top:40px;display:grid;grid-template-columns:220px minmax(0,1fr);gap:48px;padding:36px 40px;background:#FFFFFF;border:1px solid #E5E6EB}
.hy12-big{font-family:"DIN Alternate","Helvetica Neue",Arial,sans-serif;font-size:72px;line-height:72px;font-weight:600;color:#1D2129;letter-spacing:-.02em}
.hy12-cnt{margin-top:12px;font-size:14px;color:#86909C}
.hy12-ls{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:48px}
.hy12-ls li{display:flex;gap:16px;padding:12px 0;border-bottom:1px solid #F2F3F5;font-size:14px;line-height:22px;color:#1D2129}
.hy12-ls time{flex:none;width:44px;font-family:"DIN Alternate","Helvetica Neue",Arial,sans-serif;color:#86909C}
'''
def history(s):
    rail='<ol class="hy12-rail">'+''.join(f'<li><button type="button" class="{{{{hyC{i}}}}}" onClick="{{{{hyP{i}}}}}"><b>{y}</b><i></i><span>{KEY[y]}</span></button></li>' for i,y in enumerate(YEARS))+'</ol>'
    pn=''
    for i,y in enumerate(YEARS):
        ev=[l.split(' ',1) for l in H[y].split('\n')]
        li=''.join(f'<li><time>{d.replace("-",".")}</time><span>{t}</span></li>' for d,t in ev)
        pn+=f'<sc-if value="{{{{hy{i}}}}}" hint-placeholder-val="{{{{ {"true" if y==2026 else "false"} }}}}"><div class="hy12-pn"><div><div class="hy12-big">{y}</div><div class="hy12-cnt">{len(ev)} 项大事</div></div><ol class="hy12-ls">{li}</ol></div></sc-if>'
    new=('<section id="history" style="padding:96px 0;background:#F7F8FA">\n  <div class="wrap">\n'
         '    <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:16px"><h2 class="sec-t">从温州出发，服务全国</h2><div class="ab10-span"><b>11</b>年专注云上业务安全</div></div>\n'
         f'    <div class="hy12">{rail}{pn}</div>\n  </div>\n</section>')
    return new

Q='''温州市网络和数据安全技术支撑单位|全国网络安全标准化技术委员会成员单位|网络安全顾问单位|温州市网络安全技术支撑单位|浙江省专精特新中小企业|省级高新技术企业研究开发中心|信息安全管理体系认证（ISO 27001）|国家信息安全漏洞库技术支撑单位|信息技术服务管理体系认证|知识产权管理体系认证|ISO 9001 质量管理体系认证|增值电信业务经营许可证（B1-20171400）|国家高新技术企业|软件产品认证|软件企业证书|信息技术服务标准符合性证书|信息系统安全等级保护备案|温州市企业技术研究开发中心|浙江省科技型中小企业|浙江省创新型中小企业|中国网络安全威胁治理小组成员'''.split('|')
R='''龙港市先进基层党组织|瓯越铸盾网络安全集中检测优秀团队|最美温州人 · 最美互联网人|守合同重信用企业|华侨大学研究生工作站|温州市护航亚运网络安全攻防演练|网络安全实战攻防演练优秀团队|2022-2023 年度数字化创新优秀实践单位|2022 年温州网络安全短视频优秀作品|2021-2022 网络信息安全影响力人物|温州市青年网络创业协会|浙江省软件行业协会理事单位|慈善之星|中国 CSA 安全创新奖|产学研合作基地|创新创业基地|2021 年度网络安全企业之星|中国网络安全产业联盟|浙江省高新技术企业协会|中国网络信息安全卓越企业|温州网络空间安全理事|浙江网络空间安全理事|互联网协会团体成员|2020 创新产品奖|2020 创新企业奖|网络安全 AAA 企业|中国 CSA 云安全联盟|中国安全协会成员|IDC 优秀合作伙伴'''.split('|')
C='''德迅安全检测系统|德迅工单系统|德迅攻击溯源系统|德迅抗拒绝服务系统|德迅卫士安全软件|德迅云 WAF 系统|德迅云防系统|德迅云分发系统|德迅云服务系统|德迅云监控系统|内部管理系统'''.split('|')
SCANS=[('img/cert-nb16.png','增值电信业务经营许可证'),('img/cert-nb15.png','国家高新技术企业'),('img/cert-nb14.png','ISO 9001'),('img/cert-nb17.png','信息技术服务管理体系')]
OCSS='''
.hn12{display:grid;grid-template-columns:340px minmax(0,1fr);gap:40px;margin-top:40px;align-items:start}
.hn12-sc{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.hn12-sc figure{margin:0;background:#F7F8FA;border:1px solid #F2F3F5;padding:14px 12px 10px;display:flex;flex-direction:column;align-items:center;gap:8px}
.hn12-sc img{height:132px;width:auto;max-width:100%;object-fit:contain;box-shadow:0 0 0 1px #E5E6EB;background:#FFFFFF}
.hn12-sc figcaption{font-size:12px;line-height:18px;color:#4E5969;text-align:center}
.hn12-tb{display:flex;gap:32px;border-bottom:1px solid #E5E6EB}
.hn12-tb button{all:unset;cursor:pointer;padding:0 0 12px;font-size:15px;color:#4E5969;position:relative;display:flex;align-items:baseline;gap:6px}
.hn12-tb button b{font-family:"DIN Alternate","Helvetica Neue",Arial,sans-serif;font-size:20px;font-weight:600;color:#1D2129}
.hn12-tb button.on{color:#165DFF}.hn12-tb button.on b{color:#165DFF}
.hn12-tb button.on::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:#165DFF}
.hn12-ls{list-style:none;margin:8px 0 0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:40px}
.hn12-ls li{display:flex;align-items:center;gap:12px;padding:11px 0;border-bottom:1px solid #F2F3F5;font-size:14px;line-height:22px;color:#1D2129}
.hn12-ls li::before{content:"";flex:none;width:5px;height:5px;background:#C9CDD4;transform:rotate(45deg)}
'''
def honor(key,title,link=True):
    tabs=[('资质认证',Q),('荣誉奖项',R),('软件著作权',C)]
    tb='<div class="hn12-tb" role="tablist">'+''.join(f'<button type="button" role="tab" class="{{{{{key}C{i}}}}}" onClick="{{{{{key}P{i}}}}}">{n}<b>{len(l)}</b></button>' for i,(n,l) in enumerate(tabs))+'</div>'
    ls=''.join(f'<sc-if value="{{{{{key}{i}}}}}" hint-placeholder-val="{{{{ {"true" if i==0 else "false"} }}}}"><ul class="hn12-ls">'+''.join(f'<li>{x}</li>' for x in l)+'</ul></sc-if>' for i,(n,l) in enumerate(tabs))
    sc='<div class="hn12-sc">'+''.join(f'<figure><img src="{a}" alt="{b}证书"><figcaption>{b}</figcaption></figure>' for a,b in SCANS)+'</div>'
    more='<a href="Trust.dc.html#certs" style="font-size:14px">查看全部资质 →</a>' if link else ''
    return (f'<div style="display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap"><h2 class="sec-t">{title}</h2>{more}</div>'
            f'<div class="hn12">{sc}<div>{tb}{ls}</div></div>')

def span(s,sid):
    i=s.find(f'id="{sid}"'); a=s.rfind('<section',0,i); d=0
    for m in re.finditer(r'<section\b|</section>',s[a:]):
        d+=1 if m.group(0)=='<section' else -1
        if d==0: return a,a+m.end()
def addG(s,k,n,dft):
    if f'"{k}":' in s: return s
    return re.sub(r'const G = \{(.*?)\}',lambda m:'const G = {'+(m.group(1)+', ' if m.group(1).strip() else '')+f'"{k}": [{n}, {dft}, "on", ""]'+'}',s,count=1)
for f in sys.argv[1:]:
    s=open(f).read()
    if f.endswith('About.dc.html'):
        a,e=span(s,'history'); s=s[:a]+history(s)+s[e:]
        a,e=span(s,'honor'); s=s[:a]+'<section id="honor" style="padding:96px 0">\n  <div class="wrap">'+honor('hn','资质荣誉')+'</div>\n</section>'+s[e:]
        s=addG(s,'hy',12,11); s=addG(s,'hn',3,0)
        css=HCSS+OCSS
    else:
        a,e=span(s,'certs'); s=s[:a]+'<section id="certs" style="padding:96px 0">\n  <div class="wrap">'+honor('hn','权威认证，<span class="grad">合规可信</span>',False)+'</div>\n</section>'+s[e:]
        s=addG(s,'hn',3,0); css=OCSS
    if '.hn12{' not in s: s=s.replace('</style>',css+'</style>',1)
    open(f,'w').write(s); print('ok',f)
