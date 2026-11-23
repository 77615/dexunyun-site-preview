import sys
f=sys.argv[1]; t=open(f).read()
R=[("    if (t === '更多') {\n      var items = pre('Main')",
"""    if (t === '更多' && pre('AcctProducts')) {
      var pn = ((el.closest('li') || el).querySelector('.pc-nm b') || {}).textContent || '该产品'; var nr = el.getAttribute('data-nr') === '1';
      menu(el, [[nr ? '撤销到期不续' : '到期不续', function () {
        if (nr) { el.setAttribute('data-nr', '0'); toast(el, '已撤销，' + pn + ' 恢复续费提醒'); return; }
        confirmBox(el, pn + ' 到期不续？', '打开后不再发续费提醒，到期后进入保留期，保留期结束释放资源；到期前随时可以撤销。只改续费意向，不生成订单。不支持降配：想换小规格，到期后再买新规格。' + (pn === '德迅安全卫士' ? '德迅安全卫士授权到期不续，宽限期后超出免费 3 台的主机停止检测。' : ''), '确定', false, function () { el.setAttribute('data-nr', '1'); toast(el, '已设为到期不续，可在「更多」里撤销'); });
      }], ['操作记录', function () { go(el, 'Notifications.dc.html'); }]]); return;
    }
    if (t === '更多') {
      var items = pre('Main')"""),
("const item = (p) => ({ acts: p[10].map((x) => ({ t: x[0], href: x[1], cls: x[2] ? 'pc-act pri' : 'pc-act' })),",
 "const item = (p) => ({ acts: p[10].map((x) => ({ t: x[0], href: x[1], cls: x[2] ? 'pc-act pri' : 'pc-act' })).concat(p[0] === 'dj' ? [] : [{ t: '更多', href: '#', cls: 'pc-act' }]),")]
n=0
for o,nw in R:
    if nw in t: continue
    assert t.count(o)==1,(o[:50],t.count(o)); t=t.replace(o,nw); n+=1
open(f,'w').write(t); print('patched',n)
