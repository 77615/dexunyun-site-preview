#!/usr/bin/env python3
"""账号侧页签切换改成「纸张叠放」效果（幂等，标记 tsw-v1）。
参考 77 发来的 Invoice & Credit Note 组件：切换时旧页像一张纸退到后面（上移 12px、缩到 96.5%、淡出），
新页从后面那个位置升到前面，内容延迟 200ms 淡入；页签指示条 / 胶囊从上一个页签滑到当前页签。
- 一级页签（总览 / 我的产品 / 费用 / 企业）：欢迎语和页签行不动，页签下方整块内容做切换
- 二级胶囊页签（概览 / 订单 / 付款…）：一级页签和胶囊行不动，胶囊下方内容做切换
- 欢迎语和页签行不再跟着内容一起「升起」，切换时头部保持静止，像同一个页面
用法: tsw.py X.dc.html [...]
"""
import sys, os

CSS = '''
/* tsw-v1 页签切换 · 纸张叠放 */
.kc main.kc-main>.kc-hd,.kc main.kc-main>nav.tcl-tabs{animation:none!important}
.kc main.kc-main.tsw-b>nav.ia-tabs{animation:none!important}
.kc main.kc-main.tsw{position:relative}
.kc main.kc-main.tsw::before{content:"";position:absolute;left:24px;right:24px;top:var(--tsw-top,180px);height:var(--tsw-h,640px);background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.05);transform-origin:50% 0;pointer-events:none;z-index:0;animation:tswGhost .62s cubic-bezier(.22,1,.36,1) both}
.kc main.kc-main.tsw-a>nav.tcl-tabs~*,.kc main.kc-main.tsw-b>nav.ia-tabs~*{position:relative;z-index:1;transform-origin:50% 0;animation:tswIn .62s cubic-bezier(.22,1,.36,1) both,tswFade .34s ease .14s both!important}
.kc main.kc-main.tsw-a>nav.tcl-tabs>a.on::after{transform-origin:0 50%;animation:tswBar .42s cubic-bezier(.22,1,.36,1) both}
.kc main.kc-main.tsw-b>nav.ia-tabs>a:not(.on){position:relative;z-index:1;background:transparent!important}
.kc main.kc-main.tsw-b>nav.ia-tabs>a.on{position:relative;z-index:0;isolation:isolate;background:transparent!important;border-color:transparent!important}
.kc main.kc-main.tsw-b>nav.ia-tabs>a.on::before{content:""!important;display:block!important;position:absolute;left:-1px;top:-1px;bottom:-1px;width:calc(100% + 2px);border-radius:16px;background:#e5ecff;z-index:-1;animation:tswPill .42s cubic-bezier(.22,1,.36,1) both}
@keyframes tswGhost{from{transform:none;opacity:1}55%{opacity:.7}to{transform:translateY(-12px) scale(.965);opacity:0}}
@keyframes tswIn{from{transform:translateY(-12px) scale(.965)}to{transform:none}}
@keyframes tswFade{from{opacity:0}to{opacity:1}}
@keyframes tswBar{from{transform:translateX(var(--tsw-dx,0)) scaleX(var(--tsw-sx,1))}to{transform:none}}
@keyframes tswPill{from{transform:translateX(var(--tsw-dx,0));width:var(--tsw-w0,100%)}to{transform:none;width:calc(100% + 2px)}}
@media (prefers-reduced-motion:reduce){.kc main.kc-main.tsw::before{display:none}.kc main.kc-main.tsw-a>nav.tcl-tabs~*,.kc main.kc-main.tsw-b>nav.ia-tabs~*,.kc main.kc-main.tsw-a>nav.tcl-tabs>a.on::after,.kc main.kc-main.tsw-b>nav.ia-tabs>a.on::before{animation:none!important}}
'''

JS = r'''  /* tsw-v1 页签切换：点页签时记下当前页签位置，新页面挂载后从那里滑过来 */
  _tsw() {
    const W = window, D = document;
    if (!W.__tswOn) {
      W.__tswOn = 1;
      D.addEventListener('click', (e) => {
        const a = e.target && e.target.closest ? e.target.closest('main.kc-main > nav.tcl-tabs > a, main.kc-main > nav.ia-tabs > a') : null;
        if (!a || a.classList.contains('on')) return;
        const nav = a.parentNode, on = nav.querySelector(':scope > a.on'); if (!on) return;
        const nr = nav.getBoundingClientRect(), r = on.getBoundingClientRect();
        const v = { l: nav.classList.contains('tcl-tabs') ? 'a' : 'b', x: r.left - nr.left, w: r.width, t: Date.now() };
        W.__tswV = v; try { sessionStorage.setItem('tsw', JSON.stringify(v)); } catch (_) {}
      }, true);
    }
    let v = W.__tswV; if (!v) { try { v = JSON.parse(sessionStorage.getItem('tsw') || 'null'); } catch (_) {} }
    W.__tswV = null; try { sessionStorage.removeItem('tsw'); } catch (_) {}
    if (!v || Date.now() - v.t > 5000) return;
    const m = D.querySelector('main.kc-main'); if (!m) return;
    const nav = m.querySelector(v.l === 'a' ? ':scope > nav.tcl-tabs' : ':scope > nav.ia-tabs'); if (!nav) return;
    const on = nav.querySelector(':scope > a.on'); if (!on) return;
    const nr = nav.getBoundingClientRect(), r = on.getBoundingClientRect(), mr = m.getBoundingClientRect();
    on.style.setProperty('--tsw-dx', (v.x - (r.left - nr.left)).toFixed(1) + 'px');
    on.style.setProperty('--tsw-sx', (v.w / (r.width || 1)).toFixed(3));
    on.style.setProperty('--tsw-w0', v.w.toFixed(1) + 'px');
    const top = nr.bottom - mr.top + (v.l === 'a' ? 20 : 16);
    m.style.setProperty('--tsw-top', top + 'px');
    m.style.setProperty('--tsw-h', Math.max(240, Math.min(720, mr.height - top - 24)) + 'px');
    m.classList.add('tsw', 'tsw-' + v.l);
    setTimeout(() => { m.classList.remove('tsw', 'tsw-a', 'tsw-b'); }, 900);
  }
'''

HOOK = "componentDidMount() { if (document.querySelectorAll('.kc-top').length !== 1) return;"

for p in sys.argv[1:]:
    name = os.path.basename(p)
    s = open(p, encoding='utf-8').read()
    if 'tsw-v1' in s:
        print('skip', name); continue
    if 'class="tcl-tabs' not in s or s.count(HOOK) != 1:
        print('NOT APPLICABLE', name); continue
    k = s.index(HOOK)
    ls = s.rfind('\n', 0, k) + 1
    s = s[:ls] + JS + s[ls:]
    s = s.replace(HOOK, HOOK + ' this._tsw();', 1)
    i = s.index('<x-dc>'); j = s.index('</style>', i)
    s = s[:j] + CSS + s[j:]
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', name)
