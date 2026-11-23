# 生成标注数据 source.js，并给 proto/ 里的快照页面注入标注脚本（幂等）。
# 用法：python3 handoff/guard-license/build.py
# 改动点说明取自 docs/01-变更说明.md 第 4 节的表格（按 C 编号），前端任务取自 docs/02-开发任务清单.md。
import json, os, re, glob, time

H = os.path.dirname(os.path.abspath(__file__))
DOC1 = open(os.path.join(H, 'docs/01-变更说明.md'), encoding='utf-8').read()
DOC2 = open(os.path.join(H, 'docs/02-开发任务清单.md'), encoding='utf-8').read()

COLOR = {'新增': '#00B42A', '修改': '#165DFF', '删除': '#F53F3F', '待确认': '#FF7D00'}

# 页面 → 标注锚点。text 可以是字符串或候选列表（多状态页面，命中哪个用哪个）；sel 为兜底选择器；nth 为第几个匹配
M = [
 ('SecHosts', 'C01', {'text': '未受保护', 'nth': 0}),
 ('SecHosts', 'C02', {'text': '更多', 'nth': 0}),
 ('SecHosts', 'C03', {'text': '已卸载 · 10-29 由 root 卸载'}),
 ('SecLicense', 'C04', {'text': '11-08 后 54 台停止检测'}),
 ('SecLicense', 'C05', {'text': '现在处于宽限期（到 11-08）'}),
 ('SecLicense', 'C06', {'text': '名额空出后先恢复被停的主机'}),
 ('SecLicense', 'C07', {'text': '更换保留主机', 'nth': 0}),
 ('SecLicense', 'C08', {'text': '宽限至 11-08'}),
 ('SecHome', 'C09', {'text': '宽限期还剩 4 天'}),
 ('SecHome', 'C10', {'text': '11-01 到期 · 宽限至 11-08'}),
 ('SecAgent', 'C11', {'text': '按尝试接入的先后自动加入'}),
 ('SecNotify', 'C12', {'text': '宽限期结束主机停止检测'}),
 ('SecAgent', 'C13', {'text': '客户端负责在主机上采集和执行防护'}),
 ('AcctPurchase', 'C14', {'text': '购买资源'}),
 ('AcctPurchase', 'C15', {'text': '有待付款单', 'nth': 0}),
 ('AcctPurchase', 'C16', {'text': '德迅安全卫士 · 主机授权'}),
 ('AcctPurchase', 'C17', {'text': '购买方式'}),
 ('AcctPurchase', 'C18', {'text': '服务期限', 'nth': 1}),
 ('AcctPurchase', 'C19', {'text': ['宽限期内不能扩容，请先续费；过了宽限期', '剩余不足 30 天不能扩容', '同一份授权同时只能有 1 笔待付款订单', '宽限期已过，54 台主机已停止检测']}),
 ('AcctPurchase', 'C20', {'text': ['到账后恢复', '购买后共']}),
 ('AcctPurchase', 'C21', {'text': ['去付款', '提交订单'], 'last': True}),
 ('AcctPurchase', 'C22', {'text': '每个账号免费 3 台，当前已用'}),
 ('BillConfirm', 'C23', {'text': '卫士授权台数'}),
 ('BillConfirm', 'C24', {'text': '德迅安全卫士授权续费时可以减少台数'}),
 ('BillConfirm', 'C25', {'text': '+ 卫士授权（价格待定）'}),
 ('AcctSubs', 'C26', {'text': '德迅安全卫士 · 授权'}),
 ('AcctProducts', 'C27', {'text': '更多', 'nth': 1}),
 ('AcctProducts', 'C28', {'text': '11-01 到期 · 宽限至 11-08'}),
 ('Notifications', 'C29', {'text': '德迅安全卫士已购授权 11-01 到期'}),
 ('BillOrders', 'C30', {'text': '付款核验中 · 已超 2 个工作日'}),
 ('BillBalance', 'C31', {'text': '目前只做展示'}),
 ('BillPayment', 'C32', {'text': '付款前需完成个人实名认证'}),
 ('SupTicketNew', 'C33', {'text': ['退款申请', '提交工单'], 'last': True}),
 ('AcctSubs', 'C34', {'text': '授权预警', 'nth': 0}),
 ('IdcServerDetail', 'C35', {'text': ['卸载客户端', '随服务器赠送德迅安全卫士', '安全配置']}),
 ('Register', 'C36', {'text': '注册即送德迅安全卫士 3 台'}),
]

PAGE_T = {'SecHosts': '卫士 · 资产列表', 'SecLicense': '卫士 · 授权管理', 'SecHome': '卫士 · 安全总览', 'SecAgent': '卫士 · 客户端管理',
          'SecNotify': '卫士 · 通知设置', 'SecHostDetail': '卫士 · 主机详情', 'AcctPurchase': '账号 · 选购产品（6 种状态）', 'BillConfirm': '账号 · 确认订单（续费）',
          'AcctSubs': '账号 · 我的产品 · 按资源', 'AcctProducts': '账号 · 我的产品 · 按产品', 'Notifications': '账号 · 消息', 'BillOrders': '费用 · 订单',
          'BillBalance': '费用 · 收支明细', 'BillPayment': '费用 · 对公转账付款', 'SupTicketNew': '支持 · 提交工单', 'IdcServerDetail': '服务器 · 服务器详情', 'Register': '官网 · 注册'}

# 解析 01 文档第 4 节表格：| C01 | 页面 | 类型 | 说明 | 规则 |
rows = {}
for m in re.finditer(r'^\| (C\d\d) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$', DOC1, re.M):
    rows[m.group(1)] = [x.strip() for x in m.groups()[1:]]
# 解析 02 文档前端任务：| FE-01 | 任务 | 改动点 | 规则 | 验收 | 优先级 |
fe = {}
for m in re.finditer(r'^\| (FE-\d\d) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$', DOC2, re.M):
    for c in re.findall(r'C\d\d', m.group(3)):
        fe.setdefault(c, []).append((m.group(1), m.group(2).strip(), m.group(5).strip()))
# 规则表：| R01 | 规则 | 边界 |
rules = {m.group(1): (m.group(2).strip(), m.group(3).strip()) for m in re.finditer(r'^\| (R\d\d) \| ([^|]+) \| ([^|]+) \|$', DOC1, re.M)}

now = int(time.time() * 1000)
nodes, md = [], {}
for i, (page, cid, loc) in enumerate(M):
    pg, typ, desc, rl = rows[cid]
    rids = re.findall(r'R\d\d', rl)
    # 「R04–R08」展开
    for a, b in re.findall(r'R(\d\d)–R(\d\d)', rl):
        rids += ['R%02d' % k for k in range(int(a), int(b) + 1)]
    rids = sorted(set(rids))
    body = ['# %s · %s' % (cid, typ), '', '**页面**：%s' % pg, '', '**改了什么**：%s' % desc, '']
    if rids:
        body += ['**依据规则**', ''] + ['- **%s** %s%s' % (r, rules[r][0], ('（' + rules[r][1] + '）') if rules[r][1] not in ('—', '') else '') for r in rids if r in rules] + ['']
    if cid in fe:
        body += ['**开发任务**', ''] + ['- **%s** %s；验收：%s' % t for t in fe[cid]] + ['']
    if cid == 'C15':
        sec = DOC1.split('### 4.5 多状态页面的切换条件', 1)[1].split('## 5.', 1)[0]
        body += ['**状态切换条件**（页头「演示」按钮在原型里切换这 6 种状态，开发按下表判断，不做切换控件）', '', sec.strip()]
    if typ == '待确认':
        q = re.search(r'^\| (Q\d) \| ([^|]*%s[^|]*) \| ([^|]+) \|' % cid, DOC1, re.M)
        qs = [m for m in re.finditer(r'^\| (Q\d) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$', DOC1, re.M) if cid in m.group(4)]
        for m in qs:
            body += ['**待确认 %s**：%s' % (m.group(1), m.group(2).strip()), '', '**建议**：%s' % m.group(3).strip(), '']
    md[cid.lower()] = '\n'.join(body)
    texts = loc['text'] if isinstance(loc['text'], list) else [loc['text']]
    fp = json.dumps({'t': texts, 'nth': loc.get('nth', 0), 'last': loc.get('last', False), 'sel': loc.get('sel', '')}, ensure_ascii=False)
    nodes.append({'id': cid.lower(), 'index': int(cid[1:]), 'title': '%s · %s · %s' % (cid, typ, desc[:28] + ('…' if len(desc) > 28 else '')),
                  'pageId': page, 'locator': {'selectors': ['[data-annotation-id="%s"]' % cid.lower()], 'fingerprint': fp, 'path': []},
                  'aiPrompt': '', 'annotationText': '', 'hasMarkdown': True, 'color': COLOR[typ], 'images': [], 'createdAt': now, 'updatedAt': now})

legend = '''# 标注说明

这是德迅安全卫士授权调整的**标注版原型**，页面是 2026-11-23 画布的快照（卫士 LE5c、账号与费用 E1uu、服务器、官网注册页）。

- 页面上的圆形编号 = 改动点编号（C01–C36），点开看改了什么、依据哪条规则、对应哪个开发任务
- 颜色：**绿色 新增**　**蓝色 修改**　**红色 删除**　**橙色 待确认**
- 删除的元素已经不在页面上，编号标在原位置附近
- 弹窗和抽屉里的改动（删除确认框、更换保留主机抽屉、卸载弹窗）编号标在打开它的按钮上
- 选购产品页的 6 种状态用页头「演示」按钮切换，切换后编号会跟着出现
- 规则（R）、异常场景（E）、待确认（Q）见左侧文档《变更说明》，任务见《开发任务清单》

## 页面目录

''' + '\n'.join('- [%s](%s.dc.html)：%s' % (PAGE_T[p], p, '、'.join(c for pp, c, _ in M if pp == p)) for p in dict.fromkeys(pp for pp, _, _ in M)) + '\n'

src = {
 'documentVersion': 1, 'format': 'axhub-annotation-source',
 'presentation': {'layerSelectors': ['.sh-dw', '.vf-dlg', '[role="dialog"]']},
 'data': {'version': 2, 'prototypeName': 'guard-license-handoff', 'pageId': 'SecLicense', 'nodes': nodes, 'updatedAt': now},
 'markdownMap': md,
 'directory': {'nodes': [{'type': 'folder', 'id': 'pages', 'title': '标注页面', 'defaultExpanded': True,
                          'children': [{'type': 'route', 'id': 'r-' + p, 'title': PAGE_T[p], 'route': p} for p in dict.fromkeys(pp for pp, _, _ in M)]}]},
 'documents': {'nodes': [
    {'type': 'markdown', 'id': 'doc-legend', 'title': '标注说明', 'markdown': legend},
    {'type': 'markdown', 'id': 'doc-change', 'title': '01 变更说明', 'markdownPath': '01-变更说明.md', 'markdown': DOC1},
    {'type': 'markdown', 'id': 'doc-tasks', 'title': '02 开发任务清单', 'markdownPath': '02-开发任务清单.md', 'markdown': DOC2}]},
}
open(os.path.join(H, 'source.js'), 'w', encoding='utf-8').write('window.__GL_ANNOT_SOURCE__ = ' + json.dumps(src, ensure_ascii=False) + ';\n')

TAG = '<script src="../annot.js" defer></script>'
pages = []
for f in sorted(glob.glob(os.path.join(H, 'proto/*.dc.html'))):
    t = open(f, encoding='utf-8').read()
    if TAG not in t:
        t = t.replace('</body>', TAG + '\n</body>', 1)
        open(f, 'w', encoding='utf-8').write(t)
    pages.append(os.path.basename(f))
open(os.path.join(H, 'pages.js'), 'w', encoding='utf-8').write('window.__GL_PAGES__ = ' + json.dumps(pages) + ';\n')
print(len(nodes), 'markers,', len(pages), 'pages')

# 入口页 index.html
CLS = {'新增': 'add', '修改': 'mod', '删除': 'del', '待确认': 'q'}
cards = []
for p in dict.fromkeys(pp for pp, _, _ in M):
    chips = ''.join('<span class="chip %s" title="%s">%s</span>' % (CLS[rows[c][1]], rows[c][2].replace('"', '&quot;'), c) for pp, c, _ in M if pp == p)
    cards.append('<a class="card" href="proto/%s.dc.html"><b>%s</b><small>%s.dc.html</small><div class="chips">%s</div></a>' % (p, PAGE_T[p], p, chips))
tpl = open(os.path.join(H, 'index.tpl.html'), encoding='utf-8').read()
out = tpl.replace('{{N_PAGES}}', str(len(cards))).replace('{{N_MARKS}}', str(len(M))).replace('{{CARDS}}', '\n'.join(cards))
open(os.path.join(H, 'index.html'), 'w', encoding='utf-8').write(out)
