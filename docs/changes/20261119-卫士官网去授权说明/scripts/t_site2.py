# 77：官网卫士页的授权规则属于产品开通规则，官网不需要。删 #price 区、页内导航「价格与授权」、底部「了解收费方式」。幂等。用法：python3 t_site2.py <目录>
import sys, re, os
f = os.path.join(sys.argv[1], 'ProductHost.dc.html')
s = open(f, encoding='utf-8').read()
s = re.sub(r'<section id="price".*?</section>\n', '', s, flags=re.S)
s = s.replace('<a href="#price" class="tab" style="display:inline-block">价格与授权</a>', '')
s = re.sub(r'/\* lic19.*?\n(#price[^\n]*\n|@media[^\n]*#price[^\n]*\n)+', '', s)
s = s.replace('<a href="#price" class="btn" style="border-color:rgba(255,255,255,0.35);color:#FFFFFF;background:rgba(255,255,255,0.06)">了解收费方式</a>',
              '<a href="Contact.dc.html" class="btn" style="border-color:rgba(255,255,255,0.35);color:#FFFFFF;background:rgba(255,255,255,0.06)">预约产品演示</a>')
open(f, 'w', encoding='utf-8').write(s)
print('price' in s, s.count('#price'), s.count('lic-'))
