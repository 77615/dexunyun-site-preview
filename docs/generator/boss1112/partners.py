# boss #9: homepage 安全伙伴 section drops the 4 cert cards; link text -> 查看全部客户
import re,sys
f=sys.argv[1]; s=open(f).read()
i=s.find('安全伙伴'); k=s.find('ISO 27001',i)
if k<0 or k-i>20000: sys.exit('nothing')
g=s.rfind('<div',0,s.rfind('<div class="card lift',0,k))
d=0
for m in re.finditer(r'<div\b|</div>',s[g:]):
    d+=1 if m.group(0)=='<div' else -1
    if d==0: e=g+m.end();break
s=s[:g]+s[e:]
j=s.find('查看全部资质',i)
if 0<j<i+5000:
    a=s.rfind('<a ',0,j); s=s[:a]+s[a:j].replace('Trust.dc.html"','Trust.dc.html#clients"')+'查看全部客户'+s[j+len('查看全部资质'):]
open(f,'w').write(s); print('ok')
