# 卫士授权三台免费：官网画布补丁（幂等）。用法：python3 t_site.py <目录>
import sys, glob, os, re
D = sys.argv[1]
PRICE = '''<section id="price" class="soft" style="padding:96px 0">
  <div class="wrap"><div style="display:flex;flex-direction:column;gap:16px"><h2 class="sec-t">注册就能用，<span class="grad">按台加授权</span></h2><p class="sec-d sub-dash" style="color:#4E5969;font-size:15px;line-height:24px;max-width:860px;width:100%"><span style="flex:0 1 auto">不分版本，所有功能对每个账号开放；只按主机台数计算授权。</span></p></div>
    <div class="lic-g">
      <div class="card lic-c"><b class="lic-n">3 台</b><h3>注册即送</h3><p>每个账号免费 3 台主机授权，长期有效。威胁狩猎、AI 研判在内的全部能力都能用。</p></div>
      <div class="card lic-c"><b class="lic-n">按台买</b><h3>超出在线购买</h3><p>买几台就能多加几台主机，在控制台在线下单，对公转账到账后立即生效。单价待定。</p></div>
      <div class="card lic-c"><b class="lic-n">不绑机器</b><h3>只数台数</h3><p>不绑定 IP、不绑定硬件、不需要激活。授权用满后，新主机无法加入。</p></div>
      <div class="card lic-c"><b class="lic-n">删旧加新</b><h3>换机器不找客服</h3><p>不用的主机从列表删除，名额立刻空出来；新主机装上客户端就自动加入。</p></div>
    </div>
    <div class="lic-ft"><span>德迅云服务器随服务器赠送德迅安全卫士，不占 3 台免费名额。</span><span style="display:flex;gap:12px;flex-wrap:wrap"><a href="Register.dc.html" class="btn btn-p">免费注册使用</a><a href="Login.dc.html" class="btn btn-s">购买更多授权</a></span></div>
  </div>
</section>
'''
CSS = '''<style>
/* lic19 卫士授权说明（2026-11-19，仅 ProductHost #price） */
#price .lic-g{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:48px}
@media (max-width:960px){#price .lic-g{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){#price .lic-g{grid-template-columns:minmax(0,1fr)}}
#price .lic-c{padding:28px 24px;display:flex;flex-direction:column;gap:8px;background:#FFFFFF}
#price .lic-n{font-size:28px;line-height:36px;font-weight:700;color:#165DFF}
#price .lic-c h3{margin:4px 0 0;font-size:17px;line-height:26px;font-weight:600;color:#1D2129}
#price .lic-c p{margin:0;font-size:14px;line-height:22px;color:#4E5969}
#price .lic-ft{margin-top:24px;display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between;font-size:14px;line-height:22px;color:#4E5969}
</style>
'''
HOST = [
 ('<a href="Contact.dc.html" class="btn btn-p">预约产品演示</a><a href="Register.dc.html" class="btn btn-s">免费试用</a><a href="Docs.dc.html"',
  '<a href="Register.dc.html" class="btn btn-p">免费注册使用</a><a href="Contact.dc.html" class="btn btn-s">预约产品演示</a><a href="Docs.dc.html"'),
 ('<h2 class="sec-t">德迅安全卫士企业版</h2>', '<h2 class="sec-t">德迅安全卫士</h2>'),
 ('<a href="#svc" class="tab" style="display:inline-block">服务支持</a>', '<a href="#price" class="tab" style="display:inline-block">价格与授权</a><a href="#svc" class="tab" style="display:inline-block">服务支持</a>'),
 ('<p style="margin:12px 0 0;font-size:16px;line-height:28px;color:rgba(255,255,255,0.78)">三分钟部署 Agent，立即获得威胁狩猎、入侵防御与风险治理的全栈守护。</p>',
  '<p style="margin:12px 0 0;font-size:16px;line-height:28px;color:rgba(255,255,255,0.78)">注册即送 3 台主机授权。三分钟部署 Agent，立即获得威胁狩猎、入侵防御与风险治理的全栈守护。</p>'),
 ('<a href="Register.dc.html" class="btn btn-p">免费试用</a>\n        <a href="Contact.dc.html" class="btn" style="border-color:rgba(255,255,255,0.35);color:#FFFFFF;background:rgba(255,255,255,0.06)">预约产品演示</a>',
  '<a href="Register.dc.html" class="btn btn-p">免费注册使用</a>\n        <a href="#price" class="btn" style="border-color:rgba(255,255,255,0.35);color:#FFFFFF;background:rgba(255,255,255,0.06)">了解收费方式</a>'),
]
for f in sorted(glob.glob(os.path.join(D, '*.dc.html'))):
    b = os.path.basename(f); t0 = t = open(f, encoding='utf8').read()
    if b == 'ProductHost.dc.html':
        for o, n in HOST:
            if n in t: continue
            if o in t: t = t.replace(o, n); print('ok ', b, o[:40])
            elif n not in t: print('MISS', b, o[:50])
        if 'id="price"' not in t:
            t = t.replace('<section id="svc" class="deep"', PRICE + '<section id="svc" class="deep"', 1); print('ok  price section')
        if 'lic19' not in t:
            t = t.replace('</helmet>', CSS + '</helmet>', 1); print('ok  css')
    if b.startswith('HostFeature'):
        k = t.count('>免费试用</a>'); t = t.replace('>免费试用</a>', '>免费注册使用</a>'); print('ok ', b, k)
    if b == 'Main.dc.html':
        t, k = re.subn(r'(漏洞、基线、入侵检测统一管理，适配等保要求</div>(?:(?!</div></div>).){0,900}?)<span style="font-size:18px;font-weight:700;color:#165DFF">面谈</span></span><a href="Contact.dc.html" class="btn btn-sm btn-(?:s|p)">立即咨询</a>',
                       r'\1<span style="font-size:18px;font-weight:700;color:#165DFF">3 台免费</span></span><a href="Register.dc.html" class="btn btn-sm btn-p">免费注册</a>', t, flags=re.S)
        print('ok  Main cards', k)
    if b == 'Products.dc.html':
        o = '主机安全防护系统：入侵检测、漏洞、基线统一管理，适配等保</span><span class="cp">面谈</span>'
        if o in t: t = t.replace(o, '主机安全防护系统：入侵检测、漏洞、基线统一管理，适配等保</span><span class="cp">3 台免费</span>'); print('ok  Products')
    if t != t0: open(f, 'w', encoding='utf8').write(t)
