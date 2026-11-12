# boss #1/#2 (2026-11-12): ConsoleHome header card redesigned (white, label-over-number KPIs, no gradient/underlines);
# 待处理 / 其他待办 / 资源概览 colours cut back: red only for 紧急 and live attacks, everything else neutral grey.
import sys
OLD_START='<div class="h8-box h8-acc">'
NEW=('<div class="h8-box h8-id"><div class="h8-id-l"><div class="h8-av">德</div><div class="h8-who"><b>wangqi</b><span class="kc-tag info">主账号</span>'
 '<a class="kc-tag ok" href="OrgVerify.dc.html" style="text-decoration:none">企业已认证</a><p>德迅科技 · 账号 ID 100014655316</p></div></div>'
 '<div class="h8-id-k">'
 '<a href="BillOverview.dc.html"><span>账户余额<em>充值</em></span><strong>¥1,260.00</strong></a>'
 '<a href="BillPayment.dc.html"><span>待付款</span><strong>1<small>笔</small></strong></a>'
 '<a href="AcctSubs.dc.html?ft=exp"><span><i class="h8-dot"></i>到期与即将到期</span><strong>5<small>项</small></strong></a>'
 '<a href="SupTickets.dc.html"><span>未关闭工单</span><strong>4<small>个</small></strong></a>'
 '<a href="OrgSecurity.dc.html"><span>账号安全分</span><strong>81<small>/ 100</small></strong></a>'
 '</div></div>')
CSS='''
/* ---- boss 2026-11-12：头部卡片重做 + 待处理降色 ---- */
.h8-id{display:flex;align-items:center;gap:0;padding:24px 8px 24px 28px;background:#fff !important}
.h8-id-l{display:flex;align-items:center;gap:14px;width:340px;flex:none;padding-right:28px;border-right:1px solid #eaedf1}
.h8-id .h8-av{width:44px;height:44px;font-size:18px;background:#f2f3f5;color:#4e5969}
.h8-id-k{flex:1;min-width:0;display:grid;grid-template-columns:1.3fr repeat(4,minmax(0,1fr));padding-left:12px}
.h8-id-k a{display:flex;flex-direction:column;gap:8px;padding:6px 16px;border-radius:6px;text-decoration:none;transition:background .15s}
.h8-id-k a:hover{background:#f7f8fa}
.h8-id-k span{display:flex;align-items:center;gap:6px;font-size:13px;line-height:20px;color:#4e5969;white-space:nowrap}
.h8-id-k a:hover span{color:#1664ff}
.h8-id-k em{font-style:normal;color:#1664ff;margin-left:6px;padding-left:8px;border-left:1px solid #e5e6eb;line-height:12px}
.h8-id-k strong{font-family:Barlow,Inter,"PingFang SC",sans-serif;font-variant-numeric:tabular-nums;font-size:24px;line-height:30px;font-weight:600;color:#0c0d0e;white-space:nowrap}
.h8-id-k strong small{font-family:"PingFang SC",sans-serif;font-size:12px;font-weight:400;color:#86909c;margin-left:4px}
.h8-dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:#ff7d00}
.sa{background:#fff !important}
.sa-dist i.d-o,.sa-lg span.d-o::before{background:#86909c !important}
.sa-dist i.d-y,.sa-lg span.d-y::before{background:#c9cdd4 !important}
.sa-dist i.d-g,.sa-lg span.d-g::before{background:#e5e6eb !important}
.sa-nm .kc-lv3.o,.sa-nm .kc-lv3.y,.sa-nm .kc-lv3.g{background:#c9cdd4 !important}
.sa-lvt.r,.sa-lvt.o,.sa-lvt.y{color:#86909c !important}
.sa-t .kc-tag{background:#fff !important;border-color:#e5e6eb !important;color:#4e5969 !important}
.sa-t .kc-tag.err{color:#cb2634 !important}
.sa-sp i,.sa-sp i.r{background:#e5e6eb}
.sa-sp i:last-child:not(.s0){background:#86909c}
.sa-sp i.r:last-child:not(.s0){background:#f53f3f}
.sa .kc-cnt.r{color:inherit !important;background:none !important}
.vt-c{background:#fff !important}
.vt-c p em{font-style:normal;color:inherit !important}
.h8-res a > i.w{color:#737a87 !important}
'''
f=sys.argv[1]; s=open(f).read()
if 'h8-id-k' in s: sys.exit('already')
i=s.find(OLD_START); assert i>0
# end of h8-acc box: it ends right before '<div class="h8-cols">'
j=s.find('<div class="h8-cols">',i)
s=s[:i]+NEW+'\n        '+s[j:]
k=s.rfind('</style>')
s=s[:k]+CSS+s[k:]
open(f,'w').write(s); print('ok')
