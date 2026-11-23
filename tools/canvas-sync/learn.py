import re, os, glob, difflib, json, sys, collections
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../console')
S = os.path.dirname(os.path.abspath(__file__))
LINK = re.compile(r'https://claude\.ai/artifact/[A-Za-z0-9]+#(?:play|artboard)-[A-Za-z0-9._-]+')
votes = collections.defaultdict(collections.Counter)
pages = sorted(glob.glob(S + '/*/project/*.dc.html'))
for f in pages:
    b = os.path.basename(f); r = os.path.join(R, b)
    if not os.path.exists(r): continue
    a = open(f, encoding='utf-8').read().split('\n'); c = open(r, encoding='utf-8').read().split('\n')
    sm = difflib.SequenceMatcher(None, a, c, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != 'replace': continue
        for x, y in zip(a[i1:i2], c[j1:j2]):
            ls = LINK.findall(x)
            if not ls: continue
            parts = LINK.split(x)
            pat = '(.*?)'.join(re.escape(p) for p in parts)
            m = re.fullmatch(pat, y, re.S)
            if not m: continue
            for l, g in zip(ls, m.groups()):
                if g != l: votes[l][g] += 1
M = {}
for l, cnt in votes.items():
    (g, n), *rest = cnt.most_common()
    if rest: print('CONFLICT', l, cnt.most_common(4), file=sys.stderr)
    M[l] = re.sub(r'\?.*$', '', g)  # base target without query
json.dump(M, open(S + '/playmap.json', 'w'), ensure_ascii=False, indent=1, sort_keys=True)
print(len(M), 'mapped')
# all links seen in canvases
allL = collections.Counter()
for f in pages:
    for l in LINK.findall(open(f, encoding='utf-8').read()): allL[l] += 1
un = {l: n for l, n in allL.items() if l not in M}
print(len(allL), 'distinct links;', len(un), 'unmapped')
for l, n in sorted(un.items(), key=lambda x: -x[1]): print('  UNMAPPED', n, l)
