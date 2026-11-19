# 卫士授权三台免费：卫士画布 Sec* 页面补丁（幂等）。用法：python3 t_sec.py <目录>
import sys, glob, os, json, re
D = sys.argv[1]
UCBUY = 'https://claude.ai/artifact/E1uuQ8QtSKdrmFcHHxSRR9#play-8b7e5ba1733c'
P = [
 # 页头
 ('<span>企业版 · 68 台主机</span>', '<span>68 台主机 · 授权 57/57</span>'),
 # 能力列表：AI 研判对所有人开放
 ("['AI 研判', '企业版', 'on',", "['AI 研判', '基础', 'on',"),
 # 顶部通知
 ("'企业版授权 11-01 已到期，保留至 11-08；1 台主机（app-07）超出授权上限', '续费并扩容'",
  "'已购授权 11-01 已到期，保留至 11-08；授权已用满，app-07 没能加入', '续费或购买授权'"),
 ("'企业版授权 11-01 已到期，宽限期还剩 4 天：11-08 后停止检测并清理数据；另有 1 台主机（app-07）超出授权', '去续费'",
  "'已购的 54 台授权 11-01 已到期，宽限期还剩 4 天：11-08 后这部分主机停止检测；另外授权已用满，app-07 没能加入', '去续费'"),
 # 未受保护原因：未授权 → 授权已用满
 ("'未授权 · 授权已用完，这台没有绑定'", "'授权已用满 · 客户端已装好，授权用满没能加入'"),
 ("能装的直接装，离线先排查，未授权去绑定。", "能装的直接装，离线先排查，授权已用满的删掉不用的主机或购买授权。"),
 ("'未授权', 'kc-tag warn', '绑定授权', () => toast('跳转到「授权管理」', 'info')",
  "'授权已用满', 'kc-tag warn', '购买授权', () => toast('跳转到「授权管理」：删除不用的主机或购买授权后，app-07 会自动加入', 'info')"),
 ("['app-07', '10.0.2.27', '未授权']", "['app-07', '10.0.2.27', '授权已用满']"),
 ("'检测过期', '未授权']", "'检测过期', '授权已用满']"),
 ("'检测过期', '未授权'].", "'检测过期', '授权已用满']."),
 ("/^未授权/", "/^授权已用满/"),
 ("（未安装、已卸载、部署失败、离线、检测过期、未授权）", "（未安装、已卸载、部署失败、离线、检测过期、授权已用满）"),
 ("'未授权': '授权已用完，绑定授权后才会检测'", "'授权已用满': '客户端已装好，但授权用满没能加入；删除不用的主机或购买授权后自动加入'"),
 ("检测过期可立即检测；未授权去绑定授权", "检测过期可立即检测；授权已用满的删掉不用的主机或购买授权"),
 ("（离线、检测过期或未授权）", "（离线、检测过期或授权已用满）"),
 ("rsn === '未授权'", "rsn === '授权已用满'"),
 ("ops.push({ n: '绑定授权', go: GO('SecLicense', {}) })", "ops.push({ n: '购买授权', go: GO('SecLicense', {}) })"),
 ("1 台主机（app-07）没有绑定授权只告警不防护", "授权已用满，1 台主机（app-07）没能加入"),
 # 操作审计示例
 ("'关闭新主机自动绑定授权', '授权管理', '企业版 64 台'", "'删除主机 old-web-02，释放 1 个授权', '授权管理', '授权 57 台'"),
 ("{ df: [['新主机自动绑定授权', '开启', '关闭']] }", "{ df: [['已用授权', '57 / 57', '56 / 57']] }"),
 # 资产列表删除确认
 ("？客户端会停止上报，授权释放。", "？客户端会停止上报，立刻空出 1 个授权，可以加入新主机。"),
 # 总览优先处置提示
 ('title="企业版：AI 根据风险等级、可利用性和影响范围排序"', 'title="AI 根据风险等级、可利用性和影响范围排序"'),
 # 客户端管理里插件授权文案
 ("需要先在授权管理购买插件授权。", "默认开启。"),
 # 设置项说明
 ("st: k === '企业版' ? '企业版' : '已开启', tc: k === '企业版' ? 'sh-ent' : 'sh-on'", "st: '已开启', tc: 'sh-on'"),
 ("'德迅云新开服务器预装客户端；是否自动绑定授权见「授权管理」'", "'德迅云新开服务器预装客户端，随服务器赠送，不占授权'"),
]
# SecLicense 页
LIC_OLD_JS = re.compile(r"o\.tiles = \[\['授权台数'.*?\n    \}\n    if \(PG === 'SecAgent'\)", re.S)
LIC_NEW_JS = """o.tiles = [['授权台数', '57', ' 台', '免费 3 + 已购 54', '', 'b'], ['已用', '57', ' / 57', '剩余 0 台，新主机无法加入', 'o', 'b'], ['没能加入', '1', ' 台', 'app-07 · 删除不用的主机或购买授权', 'o', 'h'], ['宽限期剩余', '4', ' 天', '已购授权 11-08 后失效', 'r', 'b']]
        .map(([n, v, u, s2, c, g]) => ({ n, v, u, s: s2, c, go: g === 'h' ? ev(() => toast('跳转到「资产列表」，筛选「授权已用满」的主机', 'info')) : ev(() => {}) }));
      o.sws = [];
      const lk = (n) => ({ n, href: UC, go: undefined });
      o.lics = [['FREE-100014655316', '免费额度', '注册赠送', '3 台', '长期有效', '生效中', 'sl-st', '', []],
        ['LIC-20251026-0031', '购买授权', '在线购买', '54 台', '2025-11-02 至 2026-11-01', '宽限期', 'sl-st r', '数据保留至 11-08', [lk('续费')]],
        ['7 台德迅云服务器', '随服务器赠送', '德迅云服务器', '7 台 · 不占授权', '跟随服务器到期', '生效中', 'sl-st', '', [{ n: '查看服务器', href: 'https://claude.ai/artifact/N8Yuj4E7xMtsnFAbT8om5A#play-e1a7a42a37df', go: undefined }]]]
        .map(([id, n, ed, use, t, s2, sc, why, ops]) => ({ id, n, ed, use, t, st: s2, sc, why, ops }));
    }
    if (PG === 'SecAgent')"""
H = [
 ('<p class="kc-desc">查看授权用量和到期时间。购买、续费、扩容在用户中心完成，按对公转账付款。</p>',
  '<p class="kc-desc">每个账号免费 3 台，超出按台购买。授权只数台数，不绑定 IP 和设备。购买、续费在用户中心完成，按对公转账付款。</p>'),
 ('<span>企业版授权已于 11-01 到期，现在处于宽限期：检测和告警照常，自动处置已暂停，数据保留到 11-08（到期后统一保留 7 天）。续费并核验到账后恢复。另有 1 台主机（app-07）没有绑定授权，只告警不防护。</span></div>',
  '<span>已购的 54 台授权 11-01 到期，现在处于宽限期：检测和告警照常，自动处置已暂停，数据保留到 11-08。续费并核验到账后恢复。</span></div>\n        <div class="ac-al i" style="margin:0 20px 16px"><i>i</i><span>授权已用满，新主机无法加入（app-07 已被拒绝）。换机器时在资产列表删除旧主机，会立刻空出名额；德迅云服务器随服务器赠送，不占授权。</span></div>'),
 ('<th>授权</th><th>版本</th><th>已绑定 / 台数</th>', '<th>授权</th><th>来源</th><th>台数</th>'),
]
HOME_JS = re.compile(r"lic: \(\(\) => \{ const ed = \(this\.state \|\| \{\}\)\.ed \|\| '企业版';.*?\}; \}\)\(\),", re.S)
HOME_NEW = "lic: { ed: '授权 57 台', ent: false, cls: 'base', tag: '免费 3 + 已购 54', pb: '购买授权', flip: undefined },"
HOME_H = [
 ('<b onClick="{{sx.lic.flip}}" title="设计预览：点击切换基础版 / 企业版样式">{{sx.lic.ed}}</b>', '<b>{{sx.lic.ed}}</b>'),
 ('<b>65</b><em>/ 64 台</em>', '<b>57</b><em>/ 57 台</em>'),
 ('<p class="sh-lic-ov">已超额 1 台（app-07），这台只告警不防护</p>', '<p class="sh-lic-ov">已用满，app-07 没能加入；删除不用的主机会立刻空出名额</p>'),
 ('<div class="sh-lic-row"><span>到期</span><em>11-01 · 数据保留至 11-08</em></div>',
  '<div class="sh-lic-row"><span>已购授权到期</span><em>11-01 · 数据保留至 11-08</em></div><div class="sh-lic-row"><span>德迅云服务器</span><em>7 台 · 随服务器赠送</em></div>'),
]
# 防护策略：AI 研判不再是企业版能力
POL = [
 ("['企业版', 'AI 研判', '企业版 · 告警自动研判与处置建议', 'ent']", "['AI 研判', 'AI 研判', '告警自动研判与处置建议', '']"),
 ("const ENT = false; // 企业版未开通", "const ENT = true; // 2026-11-19 不分版本，AI 研判所有账号都有"),
 ("'企业版能力', '给出研判结论和处置建议', '未开通', 'kc-tag mut', '去开通'", "'默认开启', '给出研判结论和处置建议', '已开启', 'kc-tag ok', '查看'"),
 ("d: lock ? '企业版能力，当前未开通' : d", "d: d"),
 ("tt: lock ? '需开通企业版' : !adm", "tt: !adm"),
 ("lk: '开通企业版', href: 'SecLicense.dc.html'", "lk: '', href: 'SecLicense.dc.html'"),
 ('<h5 class="pl-gh">企业版</h5>', '<h5 class="pl-gh">AI 研判</h5>'),
]
AGENT = [
 ('<span class="sl-n">德迅服务器开通时已默认安装，这里用于其他机房的主机</span></div>\n          <h4 class="st-h">',
  '<span class="sl-n">德迅服务器开通时已默认安装，随服务器赠送，不占授权；这里用于其他机房的主机</span></div>\n          <div class="ac-al" style="margin:0 0 16px"><i>!</i><span>授权已用满（57 / 57），新装的主机不会加入。先在资产列表删除不用的主机，或<a href="https://claude.ai/artifact/E1uuQ8QtSKdrmFcHHxSRR9#play-8b7e5ba1733c">购买授权</a>；有空余名额后，已装好客户端的主机会自动加入。</span></div>\n          <h4 class="st-h">'),
 ("        ['cache-01', '10.0.3.31', '安装命令 · 其他机房', '11-06 14:20',",
  "        ['app-07', '10.0.2.27', '安装命令 · 其他机房', '11-03 11:20', P3('ok', 'ok', 'err', '上线'), '没能加入', 'sl-st r', '授权已用满（57 / 57），客户端已装好但没有加入；删除不用的主机或购买授权后自动加入', '购买授权', () => toast('跳转到「授权管理」', 'info')],\n        ['cache-01', '10.0.3.31', '安装命令 · 其他机房', '11-06 14:20',"),
 ("o.accs.filter((r) => r.st === '接入中' || r.st === '部署失败')", "o.accs.filter((r) => r.st === '接入中' || r.st === '部署失败' || r.st === '没能加入')"),
]
hits = {}
for f in sorted(glob.glob(os.path.join(D, '*.dc.html'))):
    t0 = t = open(f, encoding='utf8').read(); b = os.path.basename(f)
    for o, n in P + (H if b == 'SecLicense.dc.html' else []) + (HOME_H if b == 'SecHome.dc.html' else []) + (POL if b == 'SecPolicy.dc.html' else []) + (AGENT if b == 'SecAgent.dc.html' else []):
        if o in t: t = t.replace(o, n); hits[o[:40]] = hits.get(o[:40], 0) + 1
    if "if (PG === 'SecLicense')" in t and "['已绑定'" in t:
        t, k = LIC_OLD_JS.subn(LIC_NEW_JS, t, count=1); hits['LICJS'] = hits.get('LICJS', 0) + k
    if b == 'SecHome.dc.html':
        t, k = HOME_JS.subn(HOME_NEW, t, count=1); hits['HOMEJS'] = k
    if t != t0: open(f, 'w', encoding='utf8').write(t)
cj = os.path.join(D, 'canvas.json')
if os.path.exists(cj):
    c = json.load(open(cj, encoding='utf8'))
    c['boards']['SecLicense.dc.html']['title'] = '授权管理（2026-11-19：免费 3 台 + 按台购买，只数台数不绑机器；用满新主机无法加入，删旧主机即释放；德迅云服务器随服务器赠送不占授权）'
    json.dump(c, open(cj, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
for k, v in hits.items(): print(v, k)
