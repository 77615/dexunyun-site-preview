# -*- coding: utf-8 -*-
"""Point server entries (高防服务器 / 裸金属服务器 / 服务器租用) at ServerBuy.dc.html. usage: serverlinks.py <dir>"""
import re, sys, os
MAP = {'高防服务器': 'ServerBuy.dc.html', '裸金属服务器': 'ServerBuy.dc.html?t=2', '服务器租用': 'ServerBuy.dc.html'}
FILES = ['Header', 'MegaMenu', 'Main', 'Products', 'MobileNav']
d = sys.argv[1]
for f in FILES:
    p = os.path.join(d, f + '.dc.html')
    if not os.path.exists(p): continue
    s = open(p).read(); n = 0
    def rep(m):
        global n
        txt = re.sub(r'<[^>]+>', '', m.group(3)).strip()
        for k, v in MAP.items():
            if txt.startswith(k):
                n += 1
                return '<a href="%s"%s>%s</a>' % (v, m.group(2), m.group(3))
        return m.group(0)
    s = re.sub(r'<a href="([^"]*)"([^>]*)>((?:(?!</a>).)*?)</a>', rep, s, flags=re.S)
    # Products card price: 高防服务器 / 裸金属服务器 now have live prices
    s = re.sub(r'(高防服务器</span><span class="cd"[^>]*>[^<]*</span><span class="cp">)面谈', r'\1¥399/月起', s)
    s = re.sub(r'(裸金属服务器</span><span class="cd"[^>]*>[^<]*</span><span class="cp">)面谈', r'\1¥599/月起', s)
    s = s.replace('<span class="cb">了解详情</span></a>', '<span class="cb">了解详情</span></a>')
    open(p, 'w').write(s); print(f, n)

# Main homepage cards: price + button after each ServerBuy title (idempotent)
p = os.path.join(d, 'Main.dc.html')
if os.path.exists(p):
    s = open(p).read()
    def card(m):
        href, rest = m.group(1), m.group(2)
        rest = rest.replace('面谈', '¥599/月起' if '?t=2' in href else '¥399/月起', 1)
        rest = re.sub(r'<a href="Contact\.dc\.html" class="(btn btn-sm btn-[ps])">立即咨询', r'<a href="%s" class="\1">立即选购' % href, rest, count=1)
        return '<a href="%s" class="t"%s' % (href, rest)
    s = re.sub(r'<a href="(ServerBuy\.dc\.html(?:\?t=2)?)" class="t"((?:(?!class="t").)*?立即(?:咨询|选购))', card, s, flags=re.S)
    open(p, 'w').write(s); print('Main cards patched')
p = os.path.join(d, 'Products.dc.html')
if os.path.exists(p):
    s = open(p).read()
    s = re.sub(r'(<a href="ServerBuy[^"]*"(?:(?!</a>).)*?<span class="cb">)了解详情', r'\1立即选购', s, flags=re.S)
    open(p, 'w').write(s)
