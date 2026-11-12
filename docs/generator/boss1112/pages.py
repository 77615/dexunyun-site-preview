# 2026-11-12 (77): every menu link needs its own page. Builds new detail pages from the ProductSSL shell
# (same CSS, header, footer, CTA, floating bar, logic) with content sections taken from the live site dexun.com.
# usage: python3 pages.py <repo_dir>
import re, sys, os, html
sys.path.insert(0, os.path.dirname(__file__))
from pages_data import PAGES

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
SHELL = open(os.path.join(ROOT, 'ProductSSL.dc.html'), encoding='utf-8').read()

ICONS = {
 'shield': '<path d="M12 3l7 3v5c0 4.5-3 8.3-7 10-4-1.7-7-5.5-7-10V6z"></path><path d="M9 12l2 2 4-4"></path>',
 'lock': '<rect x="5" y="11" width="14" height="9" rx="1.5"></rect><path d="M8 11V8a4 4 0 0 1 8 0v3"></path>',
 'globe': '<circle cx="12" cy="12" r="9"></circle><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"></path>',
 'chart': '<path d="M4 20h16M7 16v-5M12 16V7M17 16v-8"></path>',
 'bolt': '<path d="M13 3L5 14h6l-1 7 8-11h-6z"></path>',
 'server': '<rect x="4" y="4" width="16" height="7" rx="1.5"></rect><rect x="4" y="13" width="16" height="7" rx="1.5"></rect><path d="M8 7.5h.01M8 16.5h.01"></path>',
 'eye': '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"></path><circle cx="12" cy="12" r="3"></circle>',
 'search': '<circle cx="11" cy="11" r="7"></circle><path d="M20 20l-3.5-3.5"></path>',
 'users': '<circle cx="9" cy="8" r="3.5"></circle><path d="M2.5 20c.8-3.5 3.4-5.5 6.5-5.5s5.7 2 6.5 5.5"></path><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14.5c2 .7 3.2 2.6 3.5 5.5"></path>',
 'doc': '<path d="M6 3h8l4 4v14H6z"></path><path d="M14 3v4h4M9 12h6M9 16h6"></path>',
 'alert': '<path d="M12 3l9.5 17h-19z"></path><path d="M12 10v4M12 17h.01"></path>',
 'cube': '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"></path><path d="M4 7.5l8 4.5 8-4.5M12 12v9"></path>',
 'grid': '<rect x="4" y="4" width="7" height="7"></rect><rect x="13" y="4" width="7" height="7"></rect><rect x="4" y="13" width="7" height="7"></rect><rect x="13" y="13" width="7" height="7"></rect>',
 'clock': '<circle cx="12" cy="12" r="9"></circle><path d="M12 7v5l3 2"></path>',
 'target': '<circle cx="12" cy="12" r="9"></circle><circle cx="12" cy="12" r="5"></circle><circle cx="12" cy="12" r="1"></circle>',
 'tool': '<path d="M14.5 5.5a4 4 0 0 0-5 5L4 16v4h4l5.5-5.5a4 4 0 0 0 5-5l-2.5 2.5-2.5-.5-.5-2.5z"></path>',
 'net': '<circle cx="12" cy="5" r="2"></circle><circle cx="5" cy="19" r="2"></circle><circle cx="19" cy="19" r="2"></circle><path d="M12 7v5M12 12l-6 5.5M12 12l6 5.5"></path>',
 'chat': '<path d="M4 5h16v11H9l-5 4z"></path>',
}
ICO_ORDER = ['shield', 'bolt', 'eye', 'chart', 'lock', 'globe', 'server', 'search', 'users', 'doc', 'cube', 'clock']
ARROW = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>'
SPOT = 'onMouseEnter="{{ spotIn }}" onMouseMove="{{ spot }}" onMouseLeave="{{ spotOut }}"'
SPOTIN = '<canvas class="spot-cv" aria-hidden="true"></canvas><div class="spot-glow" aria-hidden="true"></div>'
e = html.escape


def ico(name, size=22):
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def head(title, sub=None, light=False):
    c = ' style="color:#FFFFFF"' if light else ''
    s = f'<div style="display:flex;flex-direction:column;gap:16px"><h2 class="sec-t"{c}>{title}</h2>'
    if sub:
        sc = 'color:rgba(255,255,255,0.75)' if light else ''
        s += f'<p class="sec-d" style="margin:0;max-width:760px;{sc}">{sub}</p>'
    return s + '</div>'


def sec_open(sid, bg):
    style = 'padding:80px 0' + (f';background:{bg}' if bg else '')
    return f'<section id="{sid}" style="{style}">\n  <div class="wrap">'


def bullets(items, light=False):
    if not items:
        return ''
    col = 'rgba(255,255,255,0.78)' if light else '#4E5969'
    return ('<ul style="margin:4px 0 0;padding:0;list-style:none;display:flex;flex-direction:column;gap:6px;font-size:14px;color:%s">' % col
            + ''.join(f'<li class="chk">{x}</li>' for x in items) + '</ul>')


def r_intro(s):
    paras = ''.join(f'<p class="sec-d">{p}</p>' for p in s['paras'])
    side = ''
    if s.get('kv'):
        rows = ''.join(f'<tr><td style="width:34%;color:#4E5969">{k}</td><td>{v}</td></tr>' for k, v in s['kv'])
        side = f'<div style="overflow-x:auto;border:1px solid #EAEDF1"><table class="tbl"><tbody>{rows}</tbody></table></div>'
    elif s.get('list'):
        side = ('<div class="card" style="padding:28px;background:#F7F8FA;border-color:#EAEDF1;display:flex;flex-direction:column;gap:14px">'
                + (f'<div style="font-size:16px;font-weight:500">{s["list_t"]}</div>' if s.get('list_t') else '')
                + ''.join(f'<div style="display:flex;gap:12px;align-items:flex-start"><span style="flex:none;width:24px;height:24px;border-radius:2px;background:#E8F3FF;color:#165DFF;font-size:12px;font-weight:600;display:flex;align-items:center;justify-content:center">{i+1:02d}</span><div style="display:flex;flex-direction:column;gap:2px"><b style="font-size:15px;font-weight:500">{t}</b><span style="font-size:14px;line-height:22px;color:#4E5969">{d}</span></div></div>' for i, (t, d) in enumerate(s['list']))
                + '</div>')
    return (sec_open(s['id'], s.get('bg')).replace('<div class="wrap">', '<div class="wrap" style="display:flex;flex-wrap:wrap;gap:48px;align-items:center">')
            + f'\n    <div style="flex:1 1 440px;min-width:0;display:flex;flex-direction:column;gap:16px"><h2 class="sec-t">{s["title"]}</h2>{paras}</div>'
            + f'\n    <div style="flex:1 1 480px;min-width:0">{side}</div>\n  </div>\n</section>\n')


def r_cards(s):
    mn = s.get('min', 240)
    out = []
    for i, it in enumerate(s['items']):
        t, d = it[0], it[1]
        bl = it[2] if len(it) > 2 else None
        ic = s.get('icons', ICO_ORDER)[i % len(s.get('icons', ICO_ORDER))]
        out.append(f'<div class="card lift spot spot-l" style="padding:28px;display:flex;flex-direction:column;gap:12px" {SPOT}>{SPOTIN}'
                   f'<div class="ic">{ico(ic)}</div><div style="font-size:17px;font-weight:500">{t}</div>'
                   f'<div style="font-size:15px;line-height:22px;color:#4E5969">{d}</div>{bullets(bl)}</div>')
    return (sec_open(s['id'], s.get('bg')) + head(s['title'], s.get('sub'))
            + f'\n    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax({mn}px,1fr));gap:16px;margin-top:48px">'
            + ''.join(out) + '</div>\n  </div>\n</section>\n')


def r_grid(s):
    mn = s.get('min', 260)
    out = []
    for i, it in enumerate(s['items']):
        t, d = it[0], it[1]
        bl = it[2] if len(it) > 2 else None
        out.append(f'<div style="padding:28px 24px;border-right:1px solid #EAEDF1;border-bottom:1px solid #EAEDF1;background:#FFFFFF;display:flex;flex-direction:column;gap:10px">'
                   f'<span style="font-size:13px;color:#165DFF;font-weight:600;font-variant-numeric:tabular-nums">{i+1:02d}</span><div style="font-size:16px;font-weight:500">{t}</div>'
                   f'<div style="font-size:15px;line-height:22px;color:#4E5969">{d}</div>{bullets(bl)}</div>')
    return (sec_open(s['id'], s.get('bg', '#F7F8FA')) + head(s['title'], s.get('sub'))
            + f'\n    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax({mn}px,1fr));border-top:1px solid #EAEDF1;border-left:1px solid #EAEDF1;margin-top:48px">'
            + ''.join(out) + '</div>\n  </div>\n</section>\n')


def r_ed(s):
    n = len(s['items'])
    items = ''.join(f'<div class="ed-i"><div class="ic">{ico(s.get("icons", ICO_ORDER)[i % len(s.get("icons", ICO_ORDER))])}</div><b><i>{i+1:02d}</i>{t}</b><p>{d}</p></div>'
                    for i, (t, d) in enumerate(s['items']))
    return (f'<section id="{s["id"]}" style="padding:96px 0;background:{s.get("bg", "#FFFFFF")}"><div class="wrap"><div class="ed"><div class="ed-l">'
            f'<div class="ed-n">{n:02d}<small>{s.get("unit", "项核心能力")}</small></div><h2 class="sec-t">{s["title"]}</h2><p>{s.get("sub", "")}</p></div>'
            f'<div class="ed-r">{items}</div></div></div>\n</section>\n')


def r_steps(s):
    n = len(s['items'])
    lis = []
    for i, it in enumerate(s['items']):
        t, d = it
        on = i == 0
        lis.append(f'<li style="flex:1 1 150px;min-width:0;display:flex;flex-direction:column;gap:10px">\n'
                   f'  <div style="display:flex;align-items:center;gap:8px"><span class="num" style="width:32px;height:32px;border-radius:999px;background:{"#165DFF" if on else "#E8F3FF"};color:{"#FFFFFF" if on else "#165DFF"};display:flex;align-items:center;justify-content:center;font-weight:600;flex:none">{i+1}</span><span style="flex:1;height:1px;background:{"transparent" if i == n-1 else "#E5E6EB"}"></span></div>\n'
                   f'  <div style="font-size:15px;font-weight:500">{t}</div><div style="font-size:14px;line-height:20px;color:#4E5969">{d}</div></li>')
    return (sec_open(s['id'], s.get('bg', '#F7F8FA')) + head(s['title'], s.get('sub'))
            + '\n    <ol style="list-style:none;margin:48px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:24px">' + ''.join(lis) + '</ol>\n  </div>\n</section>\n')


def cell(v):
    if v == '✓':
        return '<td style="text-align:center"><span class="chk" aria-label="支持"></span></td>'
    if v in ('-', '—'):
        return '<td style="text-align:center;color:#C9CDD4">—</td>'
    return f'<td>{v}</td>'


def r_table(s):
    th = ''.join(f'<th>{h}</th>' for h in s['head'])
    rows = ''.join('<tr>' + f'<td style="color:#4E5969">{r[0]}</td>' + ''.join(cell(v) for v in r[1:]) + '</tr>' for r in s['rows'])
    foot = ''
    if s.get('btns'):
        foot = ('<tr><td></td>' + ''.join(f'<td><a href="{h}" class="btn btn-p btn-sm">{l}</a></td>' for l, h in s['btns']) + '</tr>')
    note = f'<p style="margin:16px 0 0;font-size:13px;color:#6B7380">{s["note"]}</p>' if s.get('note') else ''
    return (sec_open(s['id'], s.get('bg')) + head(s['title'], s.get('sub'))
            + f'\n    <div style="overflow-x:auto;border:1px solid #EAEDF1;margin-top:40px;background:#FFFFFF"><table class="tbl" style="min-width:640px"><thead><tr>{th}</tr></thead><tbody>{rows}{foot}</tbody></table></div>{note}\n  </div>\n</section>\n')


def r_deep(s):
    out = ''.join(f'<div class="deep-card" style="padding:28px;display:flex;flex-direction:column;gap:12px"><span class="num v88-big" style="font-size:42px;font-weight:600;color:#3C7EFF">{it[0]}</span>'
                  f'<div style="font-size:18px;font-weight:500">{it[1]}</div><div style="font-size:15px;line-height:22px;color:rgba(255,255,255,0.75)">{it[2]}</div></div>' for it in s['items'])
    return (f'<section id="{s["id"]}" class="deep" style="padding:80px 0;position:relative;overflow:hidden">\n  <div class="wrap" style="position:relative">'
            + head(s['title'], s.get('sub'), light=True)
            + f'\n    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax({s.get("min", 240)}px,1fr));gap:16px;margin-top:48px">' + out + '</div>\n  </div>\n</section>\n')


def r_links(s):
    out = ''.join(f'<a href="{h}" class="card lift spot spot-l" style="padding:20px 24px;display:flex;justify-content:space-between;align-items:center;gap:12px;color:#1D2129" {SPOT}>{SPOTIN}'
                  f'<div style="display:flex;flex-direction:column;gap:4px"><span class="t" style="font-size:16px;font-weight:500">{t}</span><span style="font-size:13px;color:#4E5969">{d}</span></div><span class="go">{ARROW}</span></a>'
                  for t, d, h in s['items'])
    return (sec_open(s['id'], s.get('bg')) + head(s['title'], s.get('sub'))
            + f'\n    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax({s.get("min", 260)}px,1fr));gap:16px;margin-top:48px">' + out + '</div>\n  </div>\n</section>\n')


def r_case(s):
    # left: background + steps; right: result
    left = ''.join(f'<div style="display:flex;flex-direction:column;gap:8px"><b style="font-size:15px;font-weight:500">{t}</b><p style="margin:0;font-size:15px;line-height:24px;color:#4E5969">{d}</p></div>' for t, d in s['blocks'])
    steps = ''.join(f'<li style="font-size:14px;line-height:22px;color:#4E5969">{x}</li>' for x in s.get('steps', []))
    right = (f'<div class="card" style="padding:28px;background:#F7F8FA;border-color:#EAEDF1;display:flex;flex-direction:column;gap:12px"><div style="font-size:16px;font-weight:500">{s.get("steps_t", "处置过程")}</div>'
             f'<ol style="margin:0;padding-left:20px;display:flex;flex-direction:column;gap:6px">{steps}</ol></div>') if steps else ''
    return (sec_open(s['id'], s.get('bg')) + head(s['title'], s.get('sub'))
            + f'\n    <div style="display:flex;flex-wrap:wrap;gap:40px;margin-top:40px"><div style="flex:1 1 420px;min-width:0;display:flex;flex-direction:column;gap:24px">{left}</div>'
            + f'<div style="flex:1 1 420px;min-width:0">{right}</div></div>\n  </div>\n</section>\n')


def r_faq(s):
    qs = ''.join(f'<details class="card" style="padding:16px 20px;background:#FFFFFF;border-color:#EAEDF1"{" open" if i == 0 else ""}><summary style="font-size:15px;font-weight:500;cursor:pointer">{q}</summary><p style="margin:12px 0 0;font-size:15px;line-height:22px;color:#4E5969">{a}</p></details>'
                 for i, (q, a) in enumerate(s['items']))
    rel = ''
    if s.get('related'):
        rel = ('<div style="flex:1 1 280px;min-width:0;display:flex;flex-direction:column;gap:12px"><h2 class="sec-t" style="margin-bottom:24px">%s</h2>' % s.get('related_t', '相关产品')
               + ''.join(f'<a href="{h}" class="card lift spot spot-l" style="padding:20px 24px;display:flex;flex-direction:column;gap:6px;color:#1D2129" {SPOT}>{SPOTIN}<span class="t" style="font-size:16px;font-weight:500">{t}</span><span style="font-size:14px;line-height:20px;color:#4E5969">{d}</span></a>' for t, d, h in s['related'])
               + '</div>')
    return (f'<section id="{s["id"]}" style="padding:80px 0;background:{s.get("bg", "#F7F8FA")}">\n  <div class="wrap" style="display:flex;flex-wrap:wrap;gap:48px">\n'
            f'    <div style="flex:2 1 520px;min-width:0;display:flex;flex-direction:column;gap:12px"><h2 class="sec-t" style="margin-bottom:24px">{s.get("title", "常见问题")}</h2>{qs}</div>\n    {rel}\n  </div>\n</section>\n')


def r_raw(s):
    return s['html']


R = {'intro': r_intro, 'cards': r_cards, 'grid': r_grid, 'ed': r_ed, 'steps': r_steps, 'table': r_table, 'deep': r_deep,
     'links': r_links, 'case': r_case, 'faq': r_faq, 'raw': r_raw}


def hero(p):
    crumb = '<a href="Main.dc.html">首页</a> <span aria-hidden="true">/</span> ' + ''.join(
        f'<a href="{h}">{n}</a> <span aria-hidden="true">/</span> ' for n, h in p['crumb']) + f'<span style="color:#1D2129">{p["name"]}</span>'
    btns = ''.join(f'<a href="{h}" class="btn {"btn-p" if i == 0 else "btn-s"}">{l}</a>' for i, (l, h) in enumerate(p['btns']))
    tags = ''
    if p.get('tags'):
        tags = ('<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">'
                + ''.join(f'<span class="tag" style="background:#FFFFFF;border:1px solid #E5E6EB">{t}</span>' for t in p['tags']) + '</div>')
    return (f'<section class="hero-bn hb93" style="background:#EEF1F6 url(img/{p.get("bg", "hbx-shield.webp")}) 72% center/cover no-repeat;position:relative;overflow:hidden">\n'
            '  <div class="wrap" style="position:relative;min-height:460px;box-sizing:border-box;padding-top:24px;padding-bottom:56px;display:flex;flex-direction:column">\n'
            f'    <nav aria-label="面包屑" class="crumb" style="display:flex;gap:8px;flex-wrap:wrap">{crumb}</nav>\n'
            '    <div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:20px;max-width:600px;margin-top:28px">\n'
            f'      <h1 style="margin:0;font-size:48px;line-height:58px;font-weight:600;text-wrap:balance;color:#1D2129">{p["h1"]}</h1>\n'
            f'      <p style="margin:0;font-size:17px;line-height:30px;color:#4E5969">{p["desc"]}</p>\n'
            f'      <div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:4px">{btns}</div>\n      {tags}\n    </div>\n  </div>\n</section>')


def tabnav(p):
    navs = [(s['id'], s['nav']) for s in p['sections'] if s.get('nav')]
    if len(navs) < 2:
        return ''
    a = ''.join(f'<a href="#{i}" class="tab{" tab-on" if k == 0 else ""}" style="display:inline-block">{n}</a>' for k, (i, n) in enumerate(navs))
    return f'<div style="background:rgba(255,255,255,0.92);border-bottom:1px solid #EAECF0;"><div class="wrap"><nav aria-label="页内导航" style="display:flex;gap:40px;flex-wrap:wrap">{a}</nav></div></div>\n'


def build(p):
    s = SHELL
    stem = p['file'].replace('.dc.html', '')
    a = s.index('<section class="hero-bn')
    cta_start = s.index('<section style="padding:0 0 96px;background:#FFFFFF">')
    body = hero(p) + tabnav(p) + ''.join(R[x['t']](x) for x in p['sections'])
    s = s[:a] + body + s[cta_start:]
    s = s.replace('<title>SSL 证书</title>', f'<title>{p["name"]}</title>', 1)
    s = s.replace('data-pg="ProductSSL"', f'data-pg="{stem}"').replace('[data-pg="ProductSSL"]', f'[data-pg="{stem}"]')
    s = s.replace('<dc-import name="Header" active="products"', f'<dc-import name="Header" active="{p.get("active", "products")}"', 1)
    s = s.replace('开始使用SSL 证书', p.get('cta') or ('开始使用 ' + p['name']))
    s = s.replace('安全专家 7×24 小时在线，工程师一对一协助接入。', p.get('cta_d', '安全专家 7×24 小时在线，工程师一对一协助接入。'))
    if p.get('cta_btn'):
        s = s.replace('<a href="Register.dc.html" class="btn btn-p">免费注册</a>', f'<a href="{p["cta_btn"][1]}" class="btn btn-p">{p["cta_btn"][0]}</a>', 1)
    s = s.replace('const G = {"sc": [1, 0, "tab-on", ""]};', 'const G = {};')
    h = 460 + 60 + 160 + sum(620 if x['t'] in ('table', 'faq', 'intro') else 560 for x in p['sections']) + 900
    s = re.sub(r'"\$preview":\{"width":1440,"height":\d+\}', '"$preview":{"width":1440,"height":%d}' % h, s)
    return s, h


if __name__ == '__main__':
    heights = {}
    for p in PAGES:
        s, h = build(p)
        open(os.path.join(ROOT, p['file']), 'w', encoding='utf-8').write(s)
        heights[p['file']] = h
        print('wrote', p['file'], h)
    import json
    json.dump(heights, open(os.path.join(os.path.dirname(__file__), 'pages_heights.json'), 'w'), ensure_ascii=False, indent=1)
