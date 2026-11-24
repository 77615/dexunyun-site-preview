import sys
p=sys.argv[1]; s=open(p,encoding='utf8').read()
if 'ddos3:' in s: print('already',p); sys.exit()
def rep(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
rep("iss: '16 天后到期，到期后高防 IP 停止转发', fix: '续费' },",
    "iss: '16 天后到期；到期后保留 7 天，转发不断但防护降到基础防护，之后释放、高防 IP 回收', fix: '续费' },\n      /* ddos3: 保留期示例 */\n      { n: '高防-005', id: 'ddos-5b21e0', ip: '203.0.113.50', line: 'BGP 多线', spec: '保底 30 Gbps', spec2: '保留期内弹性不可用', used: '域名 3/10 · 端口 2/20', bar: 'width: 30%', st: '已到期 · 保留至 10-31', sc: 'kc-tag err', exp: '2026-10-24', left: '保留期剩 4 天', k: 'hold', lv: 'e', iss: '已到期：转发不断，防护已降到基础防护，不能改转发规则；10-31 后释放，高防 IP 回收，请续费或提前把业务切回源站', fix: '续费' },")
rep("['即将到期', (r) => r.k === 'exp'],", "['即将到期', (r) => r.k === 'exp'], ['已到期', (r) => r.k === 'hold'],")
open(p,'w',encoding='utf8').write(s); print('ok',p)
