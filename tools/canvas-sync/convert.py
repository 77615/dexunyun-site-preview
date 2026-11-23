import re, os, glob, difflib, json, sys
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../console')
S = os.path.dirname(os.path.abspath(__file__))
OUT = S + '/out'; os.makedirs(OUT, exist_ok=True)
LINK = re.compile(r'https://claude\.ai/artifact/[A-Za-z0-9]+#(?:play|artboard)-[A-Za-z0-9._-]+')
M = json.load(open(S + '/playmap.json'))
DEAD = 'https://claude.ai/artifact/E1uuQ8QtSKdrmFcHHxSRR9#play-06ca407b9cb8'
QS = re.compile(r'(\.dc\.html)\?[^"\'\s]*')
miss = set()
for f in sorted(glob.glob(S + '/*/project/*.dc.html')):
    b = os.path.basename(f)
    t = open(f, encoding='utf-8').read()
    # 已删除的产品详情中转页：行点击兜底映射去掉（同 d345f44）
    t = re.sub(r"(AcctUsage|AcctProducts|AcctSubs): '" + re.escape(DEAD) + r"', ", '', t)
    def rep(m):
        l = m.group(0)
        if l in M: return M[l]
        miss.add((b, l)); return l
    t = LINK.sub(rep, t)
    r = os.path.join(R, b)
    if os.path.exists(r):
        a = t.split('\n'); c = open(r, encoding='utf-8').read().split('\n')
        sm = difflib.SequenceMatcher(None, a, c, autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op != 'replace': continue
            for k, (x, y) in enumerate(zip(a[i1:i2], c[j1:j2])):
                if x != y and QS.sub(r'\1', y) == x: a[i1 + k] = y
        t = '\n'.join(a)
    open(os.path.join(OUT, b), 'w', encoding='utf-8').write(t)
for b, l in sorted(miss): print('MISS', b, l)
print('done', len(glob.glob(OUT + '/*.html')))
