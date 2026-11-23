# 卫士授权生命周期：服务器画布 IdcServerDetail + 官网 Register 补丁（幂等）。
# 用法：python3 t_srv_site.py <服务器 project 目录> <官网 project 目录>
import sys, os
J = [
 (sys.argv[1], 'IdcServerDetail.dc.html', '<li>释放 1 个德迅安全卫士授权，可以绑定到其他服务器</li>',
  '<li>这台服务器的防护随服务器赠送，不占授权台数；卸载后停止检测，不会空出其他名额</li>'),
 (sys.argv[2], 'Register.dc.html', '注册后完成实名认证，即可申请免费试用。',
  '注册即送德迅安全卫士 3 台主机防护；购买产品前需完成实名认证。'),
]
for d, fn, a, b in J:
    f = os.path.join(d, fn); t = open(f, encoding='utf-8').read()
    if b in t: continue
    if a not in t: print('MISS', fn); continue
    open(f, 'w', encoding='utf-8').write(t.replace(a, b)); print('patched', fn)
