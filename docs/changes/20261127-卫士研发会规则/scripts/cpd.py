import json,re
def load(path):
    s=open(path).read()
    i=s.index('const CPD = ')+len('const CPD = ')
    d,end=json.JSONDecoder().raw_decode(s[i:])
    return s,d,i,i+end
def save(path,s,d,i,j):
    s=s[:i]+json.dumps(d,ensure_ascii=False)+s[j:]
    open(path,'w').write(s)
