# boss #3 (2026-11-12): 高防IP / 游戏盾 / SCDN packages = full spec comparison (tiers as columns, params as grouped rows)
# Data: live dexun.com /DDOS and /Myapp tables (2026-11-12). SCDN has no public price: specs follow console ScdnPlan sample values.
import re,sys
YES='<i class="pl12-y" aria-label="包含"></i>'; NO='<i class="pl12-n" aria-label="不含">—</i>'
CSS='''
.pl12-sec{padding:88px 0;background:#FFFFFF;border-top:1px solid #F2F3F5}
.pl12-hd{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;flex-wrap:wrap}
.pl12-sub{margin:12px 0 0;font-size:15px;line-height:24px;color:#4E5969}
.pl12-seg{display:inline-flex;padding:3px;background:#F2F3F5;border-radius:2px}
.pl12-seg button{all:unset;cursor:pointer;padding:7px 20px;font-size:14px;color:#4E5969;border-radius:2px;transition:background .2s,color .2s}
.pl12-seg button.on{background:#FFFFFF;color:#1D2129;font-weight:500;box-shadow:0 1px 2px rgba(0,0,0,.06)}
.pl12-seg button small{margin-left:6px;font-size:12px;color:#86909C}
.pl12{margin-top:32px;border:1px solid #E5E6EB;overflow-x:auto;background:#FFFFFF}
.pl12-t{width:100%;border-collapse:separate;border-spacing:0;table-layout:fixed;min-width:960px;font-size:14px;color:#1D2129}
.pl12-t col.c0{width:176px}
.pl12-t thead th{background:#FFFFFF;vertical-align:top;text-align:left;font-weight:400;padding:24px 20px 20px;border-bottom:1px solid #E5E6EB;border-left:1px solid #F2F3F5}
.pl12-t thead th.c0{border-left:0;vertical-align:bottom;font-size:13px;color:#86909C}
.pl12-t thead th.rec{box-shadow:inset 0 2px 0 #165DFF;background:#F7FAFF}
.pl12-nm{display:flex;align-items:center;gap:8px;font-size:16px;font-weight:600;line-height:24px;white-space:nowrap}
.pl12-tag{font-size:12px;line-height:18px;padding:0 6px;font-weight:400;color:#165DFF;background:#E8F0FF;border-radius:2px}
.pl12-key{margin-top:4px;font-size:13px;color:#4E5969;white-space:nowrap}
.pl12-pr{margin-top:16px;display:flex;align-items:baseline;gap:4px;white-space:nowrap}
.pl12-pr b{font-family:"DIN Alternate","Helvetica Neue",Arial,sans-serif;font-size:26px;line-height:32px;font-weight:600;letter-spacing:-.01em}
.pl12-pr small{font-size:12px;color:#86909C}
.pl12-pr.q b{font-family:inherit;font-size:20px}
.pl12-btn{margin-top:14px;display:flex;align-items:center;justify-content:center;height:34px;font-size:14px;border:1px solid #C9CDD4;color:#1D2129;border-radius:2px;transition:border-color .2s,color .2s,background .2s}
.pl12-btn:hover{border-color:#165DFF;color:#165DFF}
.rec .pl12-btn{background:#165DFF;border-color:#165DFF;color:#FFFFFF}.rec .pl12-btn:hover{background:#4080FF;border-color:#4080FF;color:#FFFFFF}
.pl12-t tbody th,.pl12-t tbody td{padding:13px 20px;border-bottom:1px solid #F2F3F5;text-align:left;font-weight:400;line-height:22px}
.pl12-t tbody td{border-left:1px solid #F2F3F5}
.pl12-t tbody th{color:#4E5969}
.pl12-t tbody td.rec{background:#F7FAFF}
.pl12-t tbody tr.same td{color:#4E5969}
.pl12-t tbody tr.diff td{font-weight:500}
.pl12-t tbody tr.g th{padding:20px 20px 8px;font-size:13px;font-weight:600;color:#1D2129;border-bottom:1px solid #E5E6EB;background:#FFFFFF}
.pl12-t tbody tr:hover td,.pl12-t tbody tr:hover th{background:#FAFBFC}.pl12-t tbody tr.g:hover th{background:#FFFFFF}
.pl12-t tbody tr:last-child th,.pl12-t tbody tr:last-child td{border-bottom:0}
.pl12-y{display:inline-block;width:14px;height:8px;border-left:2px solid #165DFF;border-bottom:2px solid #165DFF;transform:rotate(-45deg) translate(1px,-2px)}
.pl12-n{font-style:normal;color:#C9CDD4}
.pl12-ft{margin-top:16px;display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;font-size:13px;line-height:20px;color:#86909C}
.pl12-ft a{color:#165DFF}
'''
def table(tiers,groups,rec,buy):
    n=len(tiers)
    h='<table class="pl12-t"><colgroup><col class="c0">'+'<col>'*n+'</colgroup><thead><tr><th class="c0" scope="col">规格参数</th>'
    for i,(nm,key,price,unit) in enumerate(tiers):
        r=' rec' if i==rec else ''
        tag='<span class="pl12-tag">推荐</span>' if i==rec else ''
        if isinstance(price,int):
            pr=f'<div class="pl12-pr"><b>{price:,}</b><small>{unit}</small></div>'; bl,bh='立即购买',buy(i)
        else:
            pr=f'<div class="pl12-pr q"><b>{price}</b></div>'; bl,bh='咨询专家','Contact.dc.html'
        h+=f'<th scope="col" class="{r.strip()}"><div class="pl12-nm">{nm}{tag}</div><div class="pl12-key">{key}</div>{pr}<a class="pl12-btn" href="{bh}">{bl}</a></th>'
    h+='</tr></thead><tbody>'
    for g,rows in groups:
        h+=f'<tr class="g"><th colspan="{n+1}" scope="colgroup">{g}</th></tr>'
        for lab,vals in rows:
            if not isinstance(vals,list): vals=[vals]*n
            cls='same' if len(set(vals))==1 else 'diff'
            h+=f'<tr class="{cls}"><th scope="row">{lab}</th>'+''.join(f'<td class="{"rec" if i==rec else ""}">{v}</td>' for i,v in enumerate(vals))+'</tr>'
    return h+'</tbody></table>'

DDOS_T=[('基础型','100G 防御',1999,'元/月'),('专业型','200G 防御',2999,'元/月'),('企业型','300G 防御',3999,'元/月'),('商务型','400G 防御',5999,'元/月'),
 ('旗舰型-01','600G 防御',9999,'元/月'),('旗舰型-02','800G 防御',19999,'元/月'),('全力防护','1000G 防御','面议','')]
DDOS_G=[('防护能力',[('DDoS 防御',['100GB 峰值','200GB 峰值','300GB 峰值','400GB 峰值','600GB 峰值','800GB 峰值','1000GB 峰值']),
   ('CC 防御',['20 万 QPS','30 万 QPS','50 万 QPS','80 万 QPS','100 万 QPS','200 万 QPS','100 万 QPS']),('Web 应用防火墙',YES)]),
 ('业务规格',[('线路',['BGP 多线']*5+['BGP 线路','BGP 多线']),('业务带宽','100 Mbps'),('转发端口','100 个'),('防护域名','50 个')]),
 ('服务',[('专家服务',YES),('计费方式','按月')])]
G1=[('入门级','在线峰数 200',799),('基础级','在线峰数 300',1399),('专业级','在线峰数 400',1999),('企业级','在线峰数 600',3999),('尊享级','在线峰数 1000',6999)]
G2=[('旗舰 A 型','在线峰数 1500',9999,100000,1500,15),('旗舰 B 型','在线峰数 2000',19999,100000,2000,20),('旗舰 C 型','在线峰数 2500',29999,100000,2500,20),
 ('旗舰 D 型','在线峰数 3000',50000,100000,3000,20),('旗舰 E 型','在线峰数 5000',80000,100000,5000,30)]
def game_groups(peak,conc,src):
    return [('业务规格',[('在线峰数',[f'{x:,} 个' for x in peak]),('并发数',[f'{x:,} 个' for x in conc]),('支持源机',[f'{x} 个' for x in src]),('转发端口','1,000 个')]),
     ('防护能力',[('DDoS / CC 防御','无上限'),('TCP 协议 CC 防护',YES),('断线自动切换',YES)]),
     ('接入与服务',[('接入方式','EXE 封装 / SDK'),('支持系统','Win / iOS / Android'),('封装失败无理由退款',YES),('运维支持','7×24 在线')])]
SC_T=[('标准版','10 个域名','咨询报价',''),('企业版','50 个域名','咨询报价',''),('旗舰版','不限域名','咨询报价','')]
SC_G=[('加速',[('加速域名',['10 个','50 个','不限']),('流量包',['1 TB / 月','3 TB / 月','按需定制']),('边缘节点','全球 1700+'),('HTTPS 证书托管',['5 张','20 张','不限'])]),
 ('防护能力',[('DDoS 防护',['保底防护','弹性 · 300 Gbps 保底','不计流量全力防护']),('CC 攻击防护',YES),('WAF 漏洞入侵防护',['规则组','规则组 + 自定义规则','规则组 + 自定义规则']),
   ('语义分析引擎',[NO,YES,YES]),('Bot 行为管理',['基础爬虫识别','含 AI 行为识别','含 AI 行为识别']),('访客鉴权（APP / API）',[NO,YES,YES]),('内容安全（永远在线 / 敏感词）',[NO,YES,YES])]),
 ('服务',[('日志保存',['7 天','30 天','180 天']),('专家服务',['工单','7×24 响应','专属安全顾问'])])]

def section(title,sub,body,seg=''):
    return (f'<section id="price" class="pl12-sec"><div class="wrap"><div class="pl12-hd"><div><h2 class="sec-t">{title}</h2><p class="pl12-sub">{sub}</p></div>{seg}</div>'
            f'{body}<div class="pl12-ft"><span>价格为官网标价，按月计费；七天无理由按天退款。</span><span>需要更高规格或多实例组合？<a href="Contact.dc.html">咨询专家</a> · 热线 0577-26676666</span></div></div></section>')

def build(page):
    if page=='ProductDDoS':
        b='<div class="pl12">'+table(DDOS_T,DDOS_G,2,lambda i:f'console/AcctPurchase.dc.html?p=ddos&amp;v={i}')+'</div>'
        return section('套餐与规格','7 档套餐按防御峰值区分，全部含 Web 应用防火墙与专家服务。',b),None
    if page=='ProductGame':
        t1=table([(a,b,c,'元/月') for a,b,c in G1],game_groups([200,300,400,600,1000],[10000]*5,[10]*5),2,lambda i:f'console/AcctPurchase.dc.html?p=game&amp;v={i}')
        t2=table([(a,b,c,'元/月') for a,b,c,*_ in G2],game_groups([x[4] for x in G2],[x[3] for x in G2],[x[5] for x in G2]),None,lambda i:'Contact.dc.html')
        seg=('<div class="pl12-seg" role="tablist"><button type="button" role="tab" class="{{pvC0}}" onClick="{{pvP0}}">基础版<small>5 档</small></button>'
             '<button type="button" role="tab" class="{{pvC1}}" onClick="{{pvP1}}">增强版<small>大型游戏</small></button></div>')
        b=('<sc-if value="{{pv0}}" hint-placeholder-val="{{ true }}"><div class="pl12">'+t1+'</div></sc-if>'
           '<sc-if value="{{pv1}}" hint-placeholder-val="{{ false }}"><div class="pl12">'+t2+'</div></sc-if>')
        return section('套餐与规格','按在线峰数选择；在线超过 1000 人或并发超过 1 万，选增强版。',b,seg),'"pv": [2, 0, "on", ""]'
    if page=='ProductSCDN':
        b='<div class="pl12">'+table(SC_T,SC_G,1,None)+'</div>'
        s=section('套餐与规格','官网暂未公开标准价，按域名数量、流量与防护规格报价；下表规格为示例值，以报价单为准。',b)
        s=s.replace('价格为官网标价，按月计费；七天无理由按天退款。','可先申请 7 天免费测试，再按实际流量选规格。')
        return s,None

for f in sys.argv[1:]:
    page=f.split('/')[-1].replace('.dc.html','')
    s=open(f).read()
    i=s.find('<section id="price"'); 
    if i<0: print('no price',f); continue
    d=0
    for m in re.finditer(r'<section\b|</section>',s[i:]):
        d+=1 if m.group(0)=='<section' else -1
        if d==0: e=i+m.end();break
    new,gk=build(page)
    s=s[:i]+new+s[e:]
    if gk and '"pv":' not in s:
        s=re.sub(r'const G = \{(.*?)\}',lambda m:'const G = {'+m.group(1)+', '+gk+'}',s,count=1)
    if '.pl12-sec{' not in s: s=s.replace('</style>',CSS+'</style>',1)
    open(f,'w').write(s); print('ok',f)
