# 2026-11-17 77 选「安全组放在服务器控制台」：德迅服务器的安全组规则只在服务器控制台（IdcSecGroup）维护；
# 卫士 网络防火墙 / 网络访问防护 的安全组页签里，德迅服务器的规则只读，带「去服务器控制台修改」，非德迅主机仍在卫士里改。
import os, re, sys
C = os.path.join(os.path.dirname(__file__), '../../../console')
def rw(f, pairs):
    p = os.path.join(C, f); s = open(p, encoding='utf-8').read()
    for a, b in pairs:
        if b in s and a not in s: continue
        assert s.count(a) == 1, (f, a[:80], s.count(a)); s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)
# --- SecFirewall：表格加「管理位置」，德迅服务器的安全组只给「去服务器控制台修改」
rw('SecFirewall.dc.html', [
 ('["安全组", {"q": "搜索安全组", "add": "新建安全组", "cols": ["安全组", "规则", "关联主机", "入站默认", "更新时间"], "ops": ["编辑", "删除"], "rows": [["web-default", "6 条", "24 台", "拒绝", "10-28 11:20"], ["db-strict", "3 条", "6 台", "拒绝", "10-30 16:05"], ["ops-jump", "2 条", "2 台", "拒绝", "10-12 09:40"]]}]',
  '["安全组", {"q": "搜索安全组", "add": "新建安全组（非德迅主机）", "cols": ["安全组", "规则", "关联主机", "管理位置", "入站默认", "更新时间"], "ops": ["编辑", "删除"], "rows": [["web-default", "6 条", "24 台", {"t": "服务器控制台", "s": "德迅服务器，这里只能查看"}, "拒绝", "10-28 11:20"], ["db-strict", "3 条", "6 台", {"t": "服务器控制台", "s": "德迅服务器，这里只能查看"}, "拒绝", "10-30 16:05"], ["ops-jump", "2 条", "2 台", {"t": "服务器控制台", "s": "德迅服务器，这里只能查看"}, "拒绝", "10-12 09:40"], ["office-hosts", "4 条", "5 台", {"t": "德迅安全卫士", "s": "非德迅主机，在这里修改"}, "拒绝", "11-02 14:10"]]}]'),
 ("ops: T.ops.filter((n) => !((n === '加白'", "ops: r.some((c) => /^服务器控制台/.test(tx(c))) ? [{ n: '去服务器控制台修改', h: 'IdcSecGroup.dc.html', c: 'sl-op', go: () => {} }] : T.ops.filter((n) => !((n === '加白'"),
 ("return { n: nn, c: /删除|移除/.test(nn) ? 'sl-op fx-d' : 'sl-op', go: ev(() => act(nn, r, i)) }; }) }));",
  "return { n: nn, h: '#', c: /删除|移除/.test(nn) ? 'sl-op fx-d' : 'sl-op', go: ev(() => act(nn, r, i)) }; }) }));"),
 ('<a class="{{p.c}}" href="#" onClick="{{p.go}}">{{p.n}}</a></sc-for></td></tr></sc-if><sc-if value="{{r.ed}}"',
  '<a class="{{p.c}}" href="{{p.h}}" onClick="{{p.go}}">{{p.n}}</a></sc-for></td></tr></sc-if><sc-if value="{{r.ed}}"'),
])
# --- SecNetGuard（方案示例）：安全组规则加「管理位置」列，德迅服务器的规则只读
s = open(os.path.join(C, 'SecNetGuard.dc.html'), encoding='utf-8').read()
i = s.find('"k": "sg"'); j = s.find('{"k": "log"', i); seg = s[i:j]; seg0 = seg
if '"mg"' not in seg:
    seg = seg.replace('["生效主机", 170, "sc", ""], ["备注", 0, "n", ""]', '["生效主机", 170, "sc", ""], ["管理位置", 120, "mg", ""], ["备注", 0, "n", ""]', 1)
    seg = seg.replace('"add": "添加安全组规则"', '"add": "添加规则（非德迅主机）"', 1)
    seg = re.sub(r'\{"id": "s(\d)", ', lambda m: '{"id": "s%s", "mg": "服务器控制台", "pgH": "IdcSecGroup.dc.html", "pgN": "去服务器控制台修改", ' % m.group(1), seg)
    seg = seg.replace('"sc": "全部主机", "n": "默认放行出站", "sw": true}]', '"sc": "全部主机", "n": "默认放行出站", "sw": true}, {"id": "s9", "mg": "德迅安全卫士", "pri": "30", "dir": "入方向", "proto": "TCP", "port": "3389", "peer": "192.168.10.0/24", "pol": "允许", "sc": "office-pc（非德迅主机）", "n": "办公网远程桌面", "sw": true}]', 1)
    assert seg != seg0 and seg.count('"mg"') == 10, seg.count('"mg"')
    s = s[:i] + seg + s[j:]
pairs = [("if (r.src === '系统') L = L.filter((x) => x !== 'edit' && x !== 'del');", "if (r.src === '系统' || r.mg === '服务器控制台') L = L.filter((x) => x !== 'edit' && x !== 'del');"),
 ("if (r.pgH && !inDw) out.push({ t: '进入',", "if (r.pgH && !inDw) out.push({ t: r.pgN || '进入',"),
 ("c.swGo = ev(() => { if (RO) return toast(ROM);", "c.swGo = ev(() => { if (RO) return toast(ROM); if (r.mg === '服务器控制台') return toast('德迅服务器的安全组在服务器控制台修改', 'info');")]
for a, b in pairs:
    if b in s: continue
    assert s.count(a) == 1, a; s = s.replace(a, b)
open(os.path.join(C, 'SecNetGuard.dc.html'), 'w', encoding='utf-8').write(s)
print('ok')
rw('IdcSecGroup.dc.html', [('一台服务器可以关联多个安全组，规则修改后立即生效。</p>', '一台服务器可以关联多个安全组，规则修改后立即生效。德迅服务器的安全组只在这里修改，德迅安全卫士里只能查看。</p>')])
