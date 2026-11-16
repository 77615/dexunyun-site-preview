# 2026-11-12 (77): 资质荣誉 = all 61 items from dexun.com/honor with their certificate images (img/hn-00..60.webp,
# captured from the live page; order = 资质 21, 荣誉 29, 软件著作权 11). Replaces the honor/certs section on About + Trust.
import re, sys
Q='''温州市网络和数据安全技术支撑单位|全国网络安全标准化技术委员会成员单位|网络安全顾问单位|温州市网络安全技术支撑单位|浙江省专精特新中小企业|省级高新技术企业研究开发中心|信息安全管理体系认证（ISO 27001）|国家信息安全漏洞库技术支撑单位|信息技术服务管理体系认证|知识产权管理体系认证|ISO 9001 质量管理体系认证|增值电信业务经营许可证|国家高新技术企业|软件产品认证|软件企业证书|信息技术服务标准符合性证书|信息系统安全等级保护备案|温州市企业技术研究开发中心|浙江省科技型中小企业|浙江省创新型中小企业|中国网络安全威胁治理小组成员'''.split('|')
R='''龙港市先进基层党组织|瓯越铸盾网络安全集中检测优秀攻击团队|最美温州人 · 最美互联网人|浙江省“守合同重信用”A 级企业|华侨大学研究生工作站|温州市护航亚运网络安全攻防演练第三名|护航亚运实战攻防演练优秀攻击团队|2022-2023 年度数字化创新优秀实践单位|2022 年温州网络安全短视频优秀作品|2021-2022 网络信息安全影响力人物|温州市青年网络创业协会理事单位|浙江省软件行业协会理事单位|慈善之星|CSA 2020 安全创新奖|产学研合作基地|创新创业基地|2021 年度网络安全企业之星|中国网络安全产业联盟会员单位|浙江省高新技术企业协会理事单位|2020-2021 中国网络信息安全卓越企业|温州市网络空间安全协会理事单位|浙江省网络空间安全协会理事单位|浙江省互联网协会团体会员|2020 行业信息化创新产品|2020 行业信息化创新企业|中国网络安全行业 AAA 级诚信单位|CSA 云安全联盟会员单位|中国网络空间安全协会会员单位|浙江电信 2017 年度 IDC 优秀合作伙伴'''.split('|')
C='''德迅安全检测系统|德迅工单系统|德迅攻击溯源系统|德迅抗拒绝服务系统|德迅卫士安全软件|德迅云 WAF 系统|德迅云防系统|德迅云分发系统|德迅云服务系统|德迅云监控系统|德迅内部管理系统'''.split('|')
assert (len(Q),len(R),len(C))==(21,29,11)
CSS='''
.hn61-hd{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap}
.hn61-sub{margin-top:12px;font-size:14px;line-height:22px;color:#4E5969}
.hn61-tb{margin-top:32px}
.hn61-g{list-style:none;margin:24px 0 0;padding:0;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:24px 16px}
.hn61-g li{margin:0;min-width:0}
.hn61-g .ph{height:160px;background:#F7F8FA;border:1px solid #F2F3F5;display:flex;align-items:center;justify-content:center;padding:14px;box-sizing:border-box;overflow:hidden;transition:border-color .2s,background .2s}
.hn61-g img{display:block;max-width:100%;max-height:100%;object-fit:contain;box-shadow:0 1px 3px rgba(29,33,41,.12);transition:transform .3s}
.hn61-g li:hover .ph{border-color:#BEDAFF;background:#F2F7FF}
.hn61-g li:hover img{transform:scale(1.04)}
.hn61-g p{margin:10px 0 0;font-size:13px;line-height:20px;color:#1D2129;text-align:center}
.hn61-g.sw .ph{height:190px}
'''
LB=('<sc-if value="{{lbOpen}}" hint-placeholder-val="{{ false }}"><div class="hn61-lb" onClick="{{lbX}}" role="dialog" aria-modal="true" aria-label="证书大图">'
    '<figure class="hn61-lbx" onClick="{{lbStop}}">'+''.join(f'<sc-if value="{{{{lbI{i}}}}}" hint-placeholder-val="{{{{ false }}}}"><img src="img/hnb-{i:02d}.webp" alt="{n}"></sc-if>' for i,n in enumerate(Q+R+C))+'<figcaption><b>{{lbCap}}</b><span>{{lbPos}}</span></figcaption></figure>'
    '<button type="button" class="lb-cl" onClick="{{lbX}}" aria-label="关闭">×</button>'
    '<button type="button" class="lb-pv" onClick="{{lbPrev}}" aria-label="上一张">‹</button>'
    '<button type="button" class="lb-nx" onClick="{{lbNext}}" aria-label="下一张">›</button></div></sc-if>')
LBCSS='''
.hn61-g li.zm{cursor:zoom-in}
.hn61-g li.zm .ph{position:relative}
.hn61-g li.zm .ph::after{content:"";position:absolute;right:8px;bottom:8px;width:26px;height:26px;background:rgba(29,33,41,.55) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2.4' stroke-linecap='round'%3E%3Ccircle cx='10.5' cy='10.5' r='6.5'/%3E%3Cpath d='M15.5 15.5 21 21M10.5 7.5v6M7.5 10.5h6'/%3E%3C/svg%3E") center/14px no-repeat;opacity:0;transform:translateY(4px);transition:opacity .2s,transform .2s}
.hn61-g li.zm:hover .ph::after{opacity:1;transform:none}
.hn61-lb{position:fixed;inset:0;z-index:2000;background:rgba(15,18,24,.86);display:flex;align-items:center;justify-content:center;padding:56px 96px;box-sizing:border-box;animation:hnFade .2s ease-out;cursor:zoom-out}
.hn61-lbx{margin:0;display:flex;flex-direction:column;align-items:center;gap:16px;max-width:100%;max-height:100%;cursor:default;animation:hnZoom .24s cubic-bezier(.2,.8,.2,1)}
.hn61-lbx img{display:block;max-width:min(960px,100%);max-height:calc(100vh - 160px);width:auto;height:auto;object-fit:contain;background:#FFFFFF;box-shadow:0 12px 48px rgba(0,0,0,.45)}
.hn61-lbx figcaption{display:flex;align-items:baseline;gap:12px;color:#FFFFFF;font-size:15px;line-height:22px}
.hn61-lbx figcaption span{font-family:"DIN Alternate","Helvetica Neue",Arial,sans-serif;font-size:13px;color:rgba(255,255,255,.6)}
.hn61-lb button{all:unset;cursor:pointer;position:absolute;display:flex;align-items:center;justify-content:center;color:#FFFFFF;background:rgba(255,255,255,.1);transition:background .2s}
.hn61-lb button:hover{background:rgba(255,255,255,.22)}
.hn61-lb .lb-cl{top:20px;right:24px;width:40px;height:40px;font-size:26px;line-height:1}
.hn61-lb .lb-pv,.hn61-lb .lb-nx{top:50%;width:48px;height:64px;margin-top:-32px;font-size:34px;line-height:1}
.hn61-lb .lb-pv{left:24px}.hn61-lb .lb-nx{right:24px}
@keyframes hnFade{from{opacity:0}to{opacity:1}}
@keyframes hnZoom{from{opacity:0;transform:scale(.94)}to{opacity:1;transform:none}}
'''
LOGIC='''
// certificate lightbox (资质荣誉): lb = index into HN (-1 = closed); prev/next stay inside the open tab's group
const HN = %s;
const HNG = [[0, 21], [21, 50], [50, 61]];
const lb = s.lb ?? -1;
const lbGrp = HNG.find(([a, b]) => lb >= a && lb < b) || [0, 61];
const lbGo = (d) => (e) => { if (e && e.stopPropagation) e.stopPropagation(); const [a, b] = lbGrp; this.setState({ lb: a + ((lb - a + d + (b - a)) %% (b - a)) }); };
o.lbOpen = lb >= 0;
o.lbSrc = lb >= 0 ? 'img/hnb-' + String(lb).padStart(2, '0') + '.webp' : '';
o.lbCap = lb >= 0 ? HN[lb] : '';
o.lbPos = lb >= 0 ? (lb - lbGrp[0] + 1) + ' / ' + (lbGrp[1] - lbGrp[0]) : '';
o.lbX = (e) => { if (e && e.stopPropagation) e.stopPropagation(); this.setState({ lb: -1 }); };
o.lbStop = (e) => { if (e && e.stopPropagation) e.stopPropagation(); };
o.lbPrev = lbGo(-1); o.lbNext = lbGo(1);
for (let i = 0; i < HN.length; i++) { o['lbO' + i] = () => this.setState({ lb: i }); o['lbI' + i] = lb === i; }
'''
MOUNT='''componentDidMount() { this._tcxReveal(); this._lbKey = (e) => { const lb = (this.state || {}).lb ?? -1; if (lb < 0) return; const G = [[0, 21], [21, 50], [50, 61]].find(([a, b]) => lb >= a && lb < b); const n = G[1] - G[0]; if (e.key === 'Escape') this.setState({ lb: -1 }); else if (e.key === 'ArrowRight') this.setState({ lb: G[0] + (lb - G[0] + 1) %% n }); else if (e.key === 'ArrowLeft') this.setState({ lb: G[0] + (lb - G[0] - 1 + n) %% n }); }; if (typeof window !== 'undefined') window.addEventListener('keydown', this._lbKey); }
componentWillUnmount() { if (this._lbKey && typeof window !== 'undefined') window.removeEventListener('keydown', this._lbKey); }'''
def honor(key, title):
    tabs=[('资质认证',Q,0),('荣誉奖项',R,21),('软件著作权',C,50)]
    tb='<div class="hn12-tb hn61-tb" role="tablist">'+''.join(f'<button type="button" role="tab" class="{{{{{key}C{i}}}}}" onClick="{{{{{key}P{i}}}}}">{n}<b>{len(l)}</b></button>' for i,(n,l,o) in enumerate(tabs))+'</div>'
    gs=''
    for i,(n,l,o) in enumerate(tabs):
        items=''.join(f'<li class="zm" onClick="{{{{lbO{o+j}}}}}" title="点击查看大图"><div class="ph"><img src="img/hn-{o+j:02d}.webp" alt="{x}" loading="lazy"></div><p>{x}</p></li>' for j,x in enumerate(l))
        gs+=f'<sc-if value="{{{{{key}{i}}}}}" hint-placeholder-val="{{{{ {"true" if i==0 else "false"} }}}}"><ul class="hn61-g{" sw" if i==2 else ""}">{items}</ul></sc-if>'
    return (f'<div class="hn61-hd"><div><h2 class="sec-t">{title}</h2><p class="hn61-sub">国家及地方主管部门、行业组织颁发的资质认证与荣誉，以及自主研发产品的软件著作权。</p></div></div>'
            + tb + gs + LB)
def span(s,sid):
    i=s.find(f'id="{sid}"'); a=s.rfind('<section',0,i); d=0
    for m in re.finditer(r'<section\b|</section>',s[a:]):
        d+=1 if m.group(0)=='<section' else -1
        if d==0: return a,a+m.end()
for f in sys.argv[1:]:
    s=open(f).read()
    sid,title=('honor','资质荣誉') if f.endswith('About.dc.html') else ('certs','权威认证，<span class="grad">合规可信</span>')
    a,e=span(s,sid)
    s=s[:a]+f'<section id="{sid}" style="padding:96px 0">\n  <div class="wrap">'+honor('hn',title)+'</div>\n</section>'+s[e:]
    if '.hn61-g{' not in s: s=s.replace('</style>',CSS+'</style>',1)
    if '.hn61-lb{' not in s: s=s.replace('</style>',LBCSS+'</style>',1)
    if 'const HN = ' not in s:
        import json
        anchor="    o[k + 'P' + i] = () => this.setState({ [k]: i });\n  }\n}\n"
        assert anchor in s
        s=s.replace(anchor,anchor+LOGIC%json.dumps(Q+R+C,ensure_ascii=False),1)
        assert 'componentDidMount() { this._tcxReveal(); }' in s
        s=s.replace('componentDidMount() { this._tcxReveal(); }',MOUNT%(),1)
    open(f,'w').write(s); print('ok',f)
