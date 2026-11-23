# Apply kyno3x 3903f36 console hunks to target files by substring-level diff with context.
import sys,subprocess,difflib,re,os
REPO='/home/user/dexunyun-site-preview'
diff=subprocess.run(['git','-C',REPO,'show','-U0','--format=','3903f36','--','console/'],capture_output=True,text=True).stdout
files={}; cur=None
for l in diff.splitlines():
    if l.startswith('diff --git'): cur=l.split(' b/')[-1].split('/')[-1]; files[cur]=[]
    elif l.startswith('@@'): files[cur].append([[],[]])
    elif l.startswith('-') and not l.startswith('---'): files[cur][-1][0].append(l[1:])
    elif l.startswith('+') and not l.startswith('+++'): files[cur][-1][1].append(l[1:])
def edits(old,new,ctx=40):
    sm=difflib.SequenceMatcher(None,old,new,autojunk=False)
    out=[]
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='equal': continue
        a=max(0,i1-ctx); b=min(len(old),i2+ctx)
        # expand context left/right to make unique later
        out.append((old,i1,i2,new[j1:j2]))
    return out
def apply(t,old,new):
    if not old: return None
    if old in t: return t.replace(old,new,1)
    # segment-level
    sm=difflib.SequenceMatcher(None,old,new,autojunk=False)
    ops=[o for o in sm.get_opcodes() if o[0]!='equal']
    for op,i1,i2,j1,j2 in reversed(ops):
        ok=False
        for ctx in (30,60,120,250):
            L=old[max(0,i1-ctx):i1]; R=old[i2:i2+ctx]
            pat=L+old[i1:i2]+R
            if t.count(pat)==1:
                t=t.replace(pat,L+new[j1:j2]+R); ok=True; break
        if not ok:
            # try only left or only right context
            for ctx in (40,80,160):
                L=old[max(0,i1-ctx):i1]
                if L and t.count(L+old[i1:i2])==1 and i2==i1: t=t.replace(L,L+new[j1:j2]); ok=True; break
                R=old[i2:i2+ctx]
                if R and t.count(old[i1:i2]+R)==1 and old[i1:i2]: t=t.replace(old[i1:i2]+R,new[j1:j2]+R); ok=True; break
        if not ok: return ('FAIL',old[max(0,i1-60):i2+60],new[j1:j2])
    return t
target_dir=sys.argv[1]; only=sys.argv[2:] 
for fn,hunks in files.items():
    if only and fn not in only: continue
    p=os.path.join(target_dir,fn)
    if not os.path.exists(p): print('skip (missing)',fn); continue
    t=open(p).read()
    for old,new in hunks:
        o='\n'.join(old); n='\n'.join(new)
        if n and n in t: continue  # already applied
        if not o:
            print('PURE ADD',fn,n[:150]); continue
        r=apply(t,o,n)
        if isinstance(r,tuple): print('FAIL',fn,'|',r[1][:200],'| ->',r[2][:120])
        else: t=r
    open(p,'w').write(t); print('done',fn)
