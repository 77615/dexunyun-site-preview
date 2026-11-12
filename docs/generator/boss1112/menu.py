# 2026-11-12 boss feedback #5: product menu drops 应用加固/数据与审计/身份核验; 主机与容器安全 -> 主机安全 (capability categories)
import re,sys
HOST=[('资产管理','HostFeature-asset.dc.html','主机、进程、端口、账号与软件自动盘点'),
('风险治理','HostFeature-baseline.dc.html','漏洞、基线与主机加固检测，附修复建议'),
('威胁狩猎','HostFeature.dc.html','AI 研判，行为快照串联完整攻击链'),
('病毒与威胁防护','HostFeature-malware.dc.html','病毒查杀、WebShell 语义检测、挖矿清除'),
('应用运行防护','HostFeature-semantic.dc.html','高危命令、反弹 Shell、本地提权实时阻断'),
('文件安全防护','HostFeature-ransom.dc.html','网页防篡改、防勒索与数据备份'),
('登录安全防护','HostFeature-remote.dc.html','远程登录审计、异常登录告警、二次认证'),
('网络访问防护','ProductHost.dc.html','暴力破解封禁、端口扫描拦截、主机防火墙')]
G='<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:4px 8px">'
def mi(n,h,d,b=''): return f'<a href="{h}" class="mi"><b>{n}{b}</b><span class="d">{d}</span></a>'
head=('<a href="ProductHost.dc.html" class="hsx"><span class="hsx-t">德迅卫士<span class="badge b-new">NEW</span></span>'
 '<span class="hsx-d">一个轻量客户端，覆盖主机安全全部 8 类能力，适配云主机、物理机与私有化部署</span><span class="hsx-l">了解产品</span></a>')
PANEL='<div><div class="gt">主机安全</div>'+head+'<div class="sep"></div><div class="gt">核心能力</div>'+G+''.join(mi(*x) for x in HOST)+'</div></div>'
CSS=('.hsx{display:flex;align-items:center;gap:16px;margin:0 0 4px;padding:12px 14px;border-radius:2px;transition:background .2s}'
 '.hsx:hover{background:linear-gradient(90deg,#F2F6FF 0%,#F7F9FD 100%)}'
 '.hsx-t{display:flex;align-items:center;gap:6px;font-size:14px;font-weight:500;color:#1D2129;flex:none}'
 '.hsx-d{font-size:12px;color:#6B7380;flex:1;min-width:0}.hsx-l{font-size:12px;color:#165DFF;flex:none}.hsx-l::after{content:" →"}')
for f in sys.argv[1:]:
    s=open(f).read()
    if 'class="hsx"' in s: print('skip',f); continue
    def panel(i): return re.search(r'<sc-if value="\{\{show%d\}\}"[^>]*>.*?</sc-if>'%i,s,re.S)
    p=[panel(i) for i in range(8)]
    # 云眼 moves to 云安全 (was in 容器与资产)
    p1=p[1].group(0)
    eye=mi('德迅云眼','ProductEye.dc.html','云资产风险持续监测，网站安全监测')
    p1=p1.replace('</div></div></sc-if>',eye+'</div></div></sc-if>',1) if '德迅云眼' not in p1 else p1
    p0=p[0].group(0).replace(mi('德迅蜂巢','ProductHost.dc.html','容器安全，从镜像到运行时'),mi('德迅云眼','ProductEye.dc.html','云资产风险持续监测'))
    p2=re.sub(r'(<sc-if value="\{\{show2\}\}"[^>]*>).*(</sc-if>)',lambda m:m.group(1)+PANEL+m.group(2),p[2].group(0),flags=re.S)
    p6=p[6].group(0).replace('show6','show3'); p7=p[7].group(0).replace('show7','show4')
    new=p0+p1+p2+p6+p7
    s=s[:p[0].start()]+new+s[p[7].end():]
    s=s.replace('"主机与容器安全", "应用加固", "数据与审计", "身份核验", ','"主机安全", ')
    s=s.replace('</style>',CSS+'</style>',1)
    open(f,'w').write(s); print('ok',f)
