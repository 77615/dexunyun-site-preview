# drop 数据安全网关(堡垒机) cell from Products (数据与审计 module removed, boss 2026-11-12)
import sys
f=sys.argv[1]; s=open(f).read(); i=s.find('数据安全网关')
if i>0:
    a=s.rfind('<a ',0,i); b=s.find('</a>',i)+4; s=s[:a]+s[b:]; open(f,'w').write(s); print('removed')
