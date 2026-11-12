# boss #4 (2026-11-12): 服务器购买页太挤 -> single-column form + sticky bottom price bar (Aliyun/Tencent buy-page pattern).
# Reuses data from docs/generator/serverbuy.py; extracts base css + quick-nav from the current ServerBuy.dc.html.
# usage: python3 serverbuy2.py ServerBuy.dc.html
import sys, os, json, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import serverbuy as SB

CSS = r"""
/* ---- 服务器购买页 v2（老板 2026-11-12：更简洁） ---- */
.sb{background:#F7F8FA}
.sb-top{background:#FFFFFF;border-bottom:1px solid #E5E6EB}
.sb-gift{display:flex;flex-wrap:wrap;gap:6px 20px;font-size:13px;color:#4E5969}
.sb-gift span::before{content:"";display:inline-block;width:4px;height:4px;margin:0 8px 2px 0;background:#86909C;border-radius:50%}
.sb2{padding-top:20px;padding-bottom:40px}
.sb2-card{background:#FFFFFF;border:1px solid #E5E6EB}
.sb2-sec{padding:28px 32px}
.sb2-sec+.sb2-sec{border-top:1px solid #F2F3F5}
.sb2-sec h2{margin:0 0 22px;font-size:16px;line-height:24px;font-weight:600;color:#1D2129;display:flex;align-items:baseline;gap:12px}
.sb2-sec h2 small{font-size:13px;font-weight:400;color:#86909C}
.sb2-row{display:grid;grid-template-columns:96px minmax(0,1fr);gap:16px;align-items:start;justify-items:start}
.sb2-row+.sb2-row{margin-top:20px}
.sb2-lb{font-size:14px;color:#4E5969;line-height:32px}
.sb2-seg{display:inline-flex;flex-wrap:wrap;border:1px solid #E5E6EB;border-radius:2px;overflow:hidden}
.sb2-seg button{all:unset;cursor:pointer;height:32px;padding:0 18px;font-size:14px;line-height:32px;color:#1D2129;border-left:1px solid #E5E6EB;transition:color .15s,background .15s}
.sb2-seg button:first-child{border-left:0}
.sb2-seg button:hover{color:#165DFF}
.sb2-seg button.sb-on{background:#165DFF;color:#FFFFFF}
.sb2-hint{margin-top:8px;font-size:13px;line-height:20px;color:#86909C}
.sb2-chips{display:flex;flex-wrap:wrap;gap:8px}
.sb2-chips button{all:unset;cursor:pointer;height:30px;padding:0 14px;font-size:13px;line-height:30px;color:#1D2129;border:1px solid #E5E6EB;border-radius:2px;transition:border-color .15s,color .15s}
.sb2-chips button:hover{border-color:#94BFFF;color:#165DFF}
.sb2-chips button.sb-on{border-color:#165DFF;color:#165DFF;background:#F2F7FF}
.sb2-chips button small{margin-left:4px;font-size:12px;color:#86909C}
.sb2-tbl{width:100%;border-collapse:collapse;font-size:14px}
.sb2-tbl th{text-align:left;font-weight:400;color:#86909C;font-size:13px;height:36px;padding:0 12px;border-bottom:1px solid #E5E6EB}
.sb2-tbl td{height:52px;padding:0 12px;border-bottom:1px solid #F2F3F5;color:#1D2129}
.sb2-tbl tr.sb-tr{cursor:pointer}
.sb2-tbl tr.sb-tr:hover td{background:#F7F8FA}
.sb2-tbl tr.sb-tr-on td,.sb2-tbl tr.sb-tr-on:hover td{background:#F2F7FF}
.sb2-tbl .rd{width:14px;height:14px;border-radius:50%;border:1px solid #C9CDD4;box-sizing:border-box;display:inline-block;vertical-align:middle}
.sb2-tbl .sb-tr-on .rd{border:4px solid #165DFF}
.sb2-tbl .mem{color:#86909C;margin-left:12px;font-size:13px}
.sb2-tbl .hot{margin-left:8px;font-size:12px;color:#86909C;border:1px solid #E5E6EB;padding:0 5px;border-radius:2px}
.sb2-tbl .pr{text-align:right;font-family:"DIN Alternate","Helvetica Neue",Arial,sans-serif;font-size:16px;font-weight:600;white-space:nowrap}
.sb2-tbl .pr small{font-family:inherit;font-size:12px;font-weight:400;color:#86909C;margin-left:2px}
.sb2-sels{display:flex;gap:12px;flex-wrap:wrap}
.sb2-sel{height:32px;min-width:180px;padding:0 32px 0 12px;border:1px solid #E5E6EB;border-radius:2px;background:#FFFFFF url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2386909C' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E") no-repeat right 10px center;font-size:14px;color:#1D2129;font-family:inherit;-webkit-appearance:none;appearance:none}
.sb2-sel.w{min-width:280px}
.sb2-sel:focus{outline:none;border-color:#165DFF}
.sb-step{display:inline-flex;height:32px;border:1px solid #E5E6EB;border-radius:2px;overflow:hidden}
.sb-step button{width:32px;border:0;background:#FFFFFF;font-size:16px;color:#4E5969;cursor:pointer;font-family:inherit}
.sb-step button:hover{color:#165DFF;background:#F7F8FA}
.sb-step span{width:48px;display:flex;align-items:center;justify-content:center;font-size:14px;border-left:1px solid #E5E6EB;border-right:1px solid #E5E6EB}
.sb2-link{all:unset;cursor:pointer;font-size:13px;color:#165DFF;line-height:32px}
.sb-ta{width:100%;box-sizing:border-box;min-height:72px;padding:8px 12px;border:1px solid #E5E6EB;border-radius:2px;font-size:14px;font-family:inherit;resize:vertical;color:#1D2129}
.sb-ta:focus{outline:none;border-color:#165DFF}
.sb2-notes{margin-top:16px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px 32px;font-size:13px;line-height:20px;color:#86909C}
.sb2-notes b{font-weight:500;color:#4E5969;margin-right:6px}
.sb2-bar{position:sticky;bottom:0;z-index:4;background:#FFFFFF;border-top:1px solid #E5E6EB;box-shadow:0 -4px 16px rgba(29,33,41,.06)}
.sb2-bar .wrap{display:flex;align-items:center;gap:32px;min-height:72px}
.sb2-sum{flex:1;min-width:0;font-size:13px;line-height:20px;color:#4E5969;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sb2-sum b{font-weight:500;color:#1D2129}
.sb2-tot{display:flex;align-items:baseline;gap:8px;white-space:nowrap}
.sb2-tot > span{font-size:13px;color:#86909C}
.sb2-tot b{font-family:"DIN Alternate","Helvetica Neue",Arial,sans-serif;font-size:28px;line-height:32px;font-weight:600;color:#1D2129}
.sb2-tot small{font-size:12px;color:#86909C}
.sb-buy{height:40px;padding:0 32px;border:0;border-radius:2px;background:#165DFF;color:#FFFFFF;font-size:15px;font-weight:500;cursor:pointer;font-family:inherit;transition:background .15s}
.sb-buy:hover{background:#4080FF}
.sb-buy[disabled]{background:#94BFFF;cursor:not-allowed}
.sb2-cs{font-size:13px;color:#4E5969;white-space:nowrap}
.sb-pr{font-weight:600;font-family:"DIN Alternate","Helvetica Neue",Arial,sans-serif}
.sb-dl{margin:0;padding:16px 24px;display:grid;grid-template-columns:96px minmax(0,1fr);gap:10px 12px;font-size:13px;line-height:20px}
.sb-dl dt{color:#86909C}.sb-dl dd{margin:0;color:#1D2129;word-break:break-all}
.sb-mask{position:fixed;inset:0;z-index:50;background:rgba(29,33,41,0.45);display:flex;align-items:center;justify-content:center}
.sb-dlg{width:560px;max-width:calc(100vw - 32px);background:#FFFFFF;border-radius:2px;box-shadow:0 12px 40px rgba(0,0,0,0.18)}
.sb-dlg header{display:flex;justify-content:space-between;align-items:center;padding:18px 24px;border-bottom:1px solid #F2F3F5;font-size:16px;font-weight:600}
.sb-x{width:28px;height:28px;border:0;background:none;font-size:20px;color:#86909C;cursor:pointer}
.sb-pay{margin:0 24px;padding:12px 16px;background:#F7F8FA;border-radius:2px;font-size:13px;line-height:22px;color:#4E5969}
.sb-ft{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:16px 24px;border-top:1px solid #F2F3F5;margin-top:16px}
.sb-ck{display:inline-flex;align-items:center;gap:8px;font-size:13px;color:#4E5969;cursor:pointer;background:none;border:0;padding:0;font-family:inherit}
.sb-ck i{width:16px;height:16px;border:1px solid #C9CDD4;border-radius:2px;box-sizing:border-box;display:inline-flex;align-items:center;justify-content:center}
.sb-ck-on i{background:#165DFF;border-color:#165DFF}
.sb-ck-on i::after{content:"";width:7px;height:4px;border-left:1.5px solid #FFFFFF;border-bottom:1.5px solid #FFFFFF;transform:translateY(-1px) rotate(-45deg)}
.sb-ok{padding:36px 24px 8px;text-align:center}
.sb-ok i{display:inline-flex;width:48px;height:48px;border-radius:50%;background:#E8FFEA;align-items:center;justify-content:center}
.sb-ok h4{margin:16px 0 8px;font-size:18px}
.sb-ok p{margin:0;font-size:14px;line-height:22px;color:#4E5969}
@media (max-width:1100px){.sb2-notes{grid-template-columns:1fr}.sb2-sum{display:none}}
"""

BODY = """
<div class="tcx sb" data-pg="ServerBuy" style="min-width:0">
<div style="position:sticky;top:0;z-index:5"><dc-import name="Header" active="products" hint-size="100%,60px"></dc-import></div>
<section class="sb-top">
  <div class="wrap" style="padding-top:20px;padding-bottom:20px;display:flex;flex-direction:column;gap:10px">
    <nav aria-label="面包屑" class="crumb" style="display:flex;gap:8px;flex-wrap:wrap"><a href="Main.dc.html">首页</a> <span aria-hidden="true">/</span> <a href="Products.dc.html">产品与服务</a> <span aria-hidden="true">/</span> <span style="color:#1D2129">服务器租用</span></nav>
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap">
      <h1 style="margin:0;font-size:24px;line-height:34px;font-weight:600;color:#1D2129">服务器租用</h1>
      <div class="sb-gift"><span>每台赠送：自主化管理平台</span><span><a href="ProductHost.dc.html" style="color:inherit">德迅安全卫士</a></span><span>Web 云防护</span><span>1V1 专家 7×24 支撑</span></div>
    </div>
  </div>
</section>
<section>
<div class="wrap sb2">
  <div class="sb2-card">
    <div class="sb2-sec">
      <h2>机房与防护</h2>
      <div class="sb2-row"><div class="sb2-lb">类型</div>
        <div><div class="sb2-seg">TYPES_STATIC</div><div class="sb2-hint">{{ tyDesc }}</div></div>
      </div>
      <div class="sb2-row"><div class="sb2-lb">机房</div>
        <div><div class="sb2-chips"><sc-for list="{{ regs }}" as="o" hint-placeholder-count="8"><button type="button" class="{{ o.cls }}" onClick="{{ o.go }}">{{ o.n }}<sc-if value="{{ o.tj }}" hint-placeholder-val="{{ false }}"><small>推荐</small></sc-if></button></sc-for></div>
        <div class="sb2-hint">{{ regDesc }}</div></div>
      </div>
      <div class="sb2-row"><div class="sb2-lb">DDoS 防护</div>
        <div class="sb2-seg"><sc-for list="{{ fhs }}" as="o" hint-placeholder-count="5"><button type="button" class="{{ o.cls }}" onClick="{{ o.go }}">{{ o.n }}</button></sc-for></div>
      </div>
    </div>
    <div class="sb2-sec">
      <h2>机型<small>该机房当前在售，价格为每台每月</small></h2>
      <table class="sb2-tbl">
        <thead><tr><th style="width:28px"></th><th>CPU / 内存</th><th style="width:120px">IP</th><th style="width:200px">带宽</th><th style="width:120px;text-align:right">月付</th></tr></thead>
        <tbody><sc-for list="{{ cfgs }}" as="o" hint-placeholder-count="6"><tr class="sb-tr {{ o.cls }}" onClick="{{ o.go }}"><td><span class="rd"></span></td><td>{{ o.cpu }}<span class="mem">{{ o.mem }}</span><sc-if value="{{ o.hot }}" hint-placeholder-val="{{ false }}"><span class="hot">爆款</span></sc-if></td><td>{{ o.ip }}</td><td>{{ o.bw }}</td><td class="pr">¥{{ o.p }}<small>/月</small></td></tr></sc-for></tbody>
      </table>
    </div>
    <div class="sb2-sec">
      <h2>系统与时长</h2>
      <div class="sb2-row"><div class="sb2-lb">操作系统</div>
        <div class="sb2-sels"><select class="sb2-sel" value="{{ osFi }}" onChange="{{ osFam }}" aria-label="系统"><sc-for list="{{ osf }}" as="o" hint-placeholder-count="7"><option value="{{ o.i }}">{{ o.n }}</option></sc-for></select><select class="sb2-sel w" value="{{ osV }}" onChange="{{ osPick }}" aria-label="系统版本"><sc-for list="{{ osvs }}" as="v" hint-placeholder-count="4"><option value="{{ v.n }}">{{ v.n }}</option></sc-for></select></div>
      </div>
      <div class="sb2-row"><div class="sb2-lb">购买时长</div>
        <div class="sb2-seg"><sc-for list="{{ months }}" as="o" hint-placeholder-count="7"><button type="button" class="{{ o.cls }}" onClick="{{ o.go }}">{{ o.n }}</button></sc-for></div>
      </div>
      <div class="sb2-row"><div class="sb2-lb">数量</div>
        <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap"><div class="sb-step"><button type="button" onClick="{{ qDec }}" aria-label="减少">−</button><span>{{ q }}</span><button type="button" onClick="{{ qInc }}" aria-label="增加">+</button></div><span style="font-size:13px;color:#86909C">台，单次最多 20 台</span><sc-if value="{{ spN }}" hint-placeholder-val="{{ true }}"><button type="button" class="sb2-link" onClick="{{ spTog }}">+ 填写特殊要求</button></sc-if></div>
      </div>
      <sc-if value="{{ spY }}" hint-placeholder-val="{{ false }}"><div class="sb2-row"><div class="sb2-lb">特殊要求</div><div><textarea class="sb-ta" placeholder="如需定制分区、额外 IP、指定上架时间等，工程师会在交付前与您确认"></textarea></div></div></sc-if>
    </div>
  </div>
  <div class="sb2-notes"><div><b>付款</b>对公转账，财务核验到账后交付</div><div><b>实名</b>下单前需完成实名认证</div><div><b>承诺</b>标注机房在防护峰值内被打死，按天退款</div></div>
</div>
</section>
<div class="sb2-bar"><div class="wrap">
  <div class="sb2-sum"><b>{{ sType }} · {{ sReg }} · {{ sFh }}</b>　{{ sCpu }} · {{ sMem }} · {{ sBw }} · {{ osV }} · {{ sM }} × {{ q }} 台</div>
  <div class="sb2-tot"><span>配置费用</span><b>¥{{ total }}</b><small>¥{{ sP }}/月</small></div>
  <button type="button" class="sb-buy" onClick="{{ openDlg }}">立即购买</button>
  <a class="sb2-cs" href="Contact.dc.html">咨询售前</a>
</div></div>
<dc-import name="Footer" hint-size="100%,480px"></dc-import>
QNAV
DLGS
</div>
"""

LOGIC_PATCH = [
  ("const o = {", "const o = {\n  tyDesc: T[1],\n  osFi: String(osF), osFam: (e) => set({ osF: +e.target.value, osV: null }),\n  spY: !!s.sp, spN: !s.sp, spTog: () => set({ sp: !s.sp }),"),
  ("osf: D.OS.map((x, i) => ({ n: x[0], cls", "osf: D.OS.map((x, i) => ({ i: String(i), n: x[0], cls"),
]

def main(f):
    s = open(f).read()
    i = s.find('<helmet>\n') + len('<helmet>\n'); j = s.find('/* ---- 服务器')
    base = s[i:j]
    k = s.find('<dc-import name="Footer"'); k = s.find('\n', k) + 1
    k2 = s.find('<sc-if value="{{ dlg1 }}"'); qnav = s[k:k2].strip()
    k3 = s.find('</x-dc>'); dlgs = s[k2:s.rfind('</div>', 0, k3)].strip()
    types = ''.join('<button type="button" class="{{ tyC%d }}" onClick="{{ tyP%d }}">%s</button>' % (n, n, t[0]) for n, t in enumerate(SB.T))
    body = BODY.replace('TYPES_STATIC', types).replace('QNAV', qnav).replace('DLGS', dlgs)
    logic = SB.LOGIC.replace('__DATA__', json.dumps(SB.DATA, ensure_ascii=False))
    for a, b in LOGIC_PATCH:
        assert a in logic, a; logic = logic.replace(a, b, 1)
    head = s[:i]
    out = head + base.rstrip() + "\n" + CSS + "</style>\n</helmet>\n" + body + "</x-dc>\n" + logic + "</body>\n</html>\n"
    open(f, 'w').write(out); print('ok', f)

main(sys.argv[1])
