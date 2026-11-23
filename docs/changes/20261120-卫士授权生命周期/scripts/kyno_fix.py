import sys,re,os
D=sys.argv[1]
def ed(fn,fun):
    p=os.path.join(D,fn)
    if not os.path.exists(p): print('missing',fn); return
    t=open(p).read(); t2=fun(t)
    if t2!=t: open(p,'w').write(t2); print('fixed',fn)
    else: print('nochange',fn)
def bp(t):
    if '付款前需完成个人实名认证' in t: return t
    return t.replace('<li>核验结果会短信和站内信通知</li>','<li>付款前需完成个人实名认证</li><li>核验结果会短信和站内信通知</li>',1)
def bb(t):
    t=re.sub(r'(可用余额</div><div class="b8-amt"><small>¥</small>1,260\.00</div><p[^>]*>)[^<]*(</p>)',r'\1余额来自充值和旧账户迁入，目前只做展示，不能用来付款，订单按对公转账付款。退款原路退回付款账户，不进余额。\2',t,count=1)
    i=t.find('<tbody>',t.find('收支明细</h2>'))
    if i<0: return t
    j=t.find('</tbody>',i)
    rows='<tbody><tr><td>2026-11-01 09:30</td><td><span class="kc-tag ok">充值</span></td><td class="num" style="color:#00b42a">+¥1,000.00</td><td class="num">¥1,260.00</td><td><a href="BillOrderDetail.dc.html">CZ20261101001</a></td><td>对公转账充值</td></tr><tr><td>2026-09-17 00:00</td><td><span class="kc-tag info">迁入</span></td><td class="num" style="color:#00b42a">+¥260.00</td><td class="num">¥260.00</td><td>—</td><td>旧版账户余额迁入</td></tr>'
    return t[:i]+rows+t[j:]
def stn(t):
    t=t.replace("    const ty = st.ty || '产品使用'; const cur0","    const __ty = __qs && __qs.get('ty'); const __cp = __qs && __qs.get('copy'); const __od = __qs && (__qs.get('refund') || __qs.get('order') || __cp); const isRf = !!(__qs && __qs.get('refund'));\n    const ty = st.ty || __ty || '产品使用'; const cur0",1)
    if '{{odT}}' not in t:
        k='<div class="fl-row"><span>关联资源</span>'
        t=t.replace(k,'<sc-if value="{{odOn}}" hint-placeholder-val="{{false}}"><div class="fl-row" style="align-items:start"><span>{{odT}}</span><div style="max-width:640px"><b>{{odId}}</b><p class="kc-sub" style="margin:4px 0 0;line-height:1.6">{{odS}}</p></div></div></sc-if>\n        '+k,1)
    return t
ed('BillPayment.dc.html',bp); ed('BillBalance.dc.html',bb); ed('SupTicketNew.dc.html',stn)
def bo(t):
    if "'DX20261101001'" in t: return t
    row="      [[{ t: 'DX20261101001', a: 'BillOrderDetail.dc.html' }, { t: 'DDoS 高防 IP', s: '高防-002 · 10 月弹性防护账单' }, { t: '用量账单', tag: 'warn' }, '系统', '2026-11-01 00:05', { t: '待付款', tag: 'warn' }, { t: '¥385.00', c: 'ac-n' }], [['去付款', 'BillPayment.dc.html']], 'unpaid'],\n"
    i=t.find("'已退款', 'refund']]"); k=t.rfind('const R = [\n',0,i)
    return t[:k+12]+row+t[k+12:]
ed('BillOrders.dc.html',bo)
def sd(t):
    if '{{unN}}' in t: return t
    k='</sc-for>\n            </div>\n            <sc-if value="{{open}}" hint-placeholder-val="{{true}}"><div class="dt-reply">'
    assert t.count(k)==1
    return t.replace(k,'</sc-for>\n            </div>\n            <sc-if value="{{open}}" hint-placeholder-val="{{true}}"><p class="kc-sub" style="margin:0;padding:10px 24px;background:#fff7e8;border-top:1px solid #f2f3f5;line-height:1.6">{{unN}}</p></sc-if>\n            <sc-if value="{{open}}" hint-placeholder-val="{{true}}"><div class="dt-reply">')
ed('SupTicketDetail.dc.html',sd)
