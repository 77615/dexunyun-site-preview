# 任务：德迅安全卫士授权改为「三台免费、按台购买」

77 已确认（2026-11-19）：德迅服务器不占名额；其余按推荐项。已全部完成，见 verify.md。
与提案的差别：app-07 没有移出资产列表，改为「未受保护 · 授权已用满」并在接入记录显示「没能加入」，这样用户装了客户端能看到原因，减少咨询。
实施前：重读线上画布，把 77 在画布里的改动合并进来。

| # | 画布 | 画板 | 动作 | 组件 / 交互规则 | 脚本 | 完成 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 卫士 | SecLicense | 修改：概况 4 格「授权台数 64（免费 3 + 已购 61）/ 已用 64 / 剩余 0 / 到期」；去「已绑定」「新主机自动绑定授权」；明细表行 = 免费额度（永久）+ 购买记录；用满 kc-alert warn「新主机无法加入…删除主机 / 购买授权」 | kc-stat-tiles、kc-table、kc-alert | scripts/t1_license.py | [x] |
| 2 | 卫士 | 全部 Sec*（约 31 页） | 修改：页头「企业版 · 68 台主机」→「68 台主机 · 授权 64/64」 | kc-hd | scripts/t2_header.py | [x] |
| 3 | 卫士 | SecHome | 修改：授权卡去版本切换和「升级企业版」，按钮「购买授权」；待办里的「企业版授权到期」改「授权到期」；去掉 app-07「未授权」 | kc-card | scripts/t3_home.py | [x] |
| 4 | 卫士 | SecHosts、SecHostDetail、SecHunt | 修改：未受保护原因 6 → 5（去「未授权」）；删除主机弹窗加「释放 1 个授权」；示例数据 68 台中 app-07 移出资产列表 | kc-modal、kc-tag | scripts/t4_hosts.py | [x] |
| 5 | 卫士 | SecAgent | 修改：安装客户端抽屉顶部显示「剩余授权 N 台」，用满时 kc-alert 说明新主机会被拒；接入记录新增一条「app-07 接入被拒 · 授权已用满」；能力列表 AI 研判去「企业版」 | kc-drawer、kc-alert | scripts/t5_agent.py | [x] |
| 6 | 卫士 | SecNotify、SecReport、SecAudit | 修改：通知项「授权到期」保留、加「授权用满」；报表和审计里的「企业版 64 台」「新主机自动绑定授权」示例改掉 | kc-table | scripts/t6_misc.py | [x] |
| 7 | 账号与费用 | AcctPurchase | 修改：卫士只选台数 + 时长；删版本选择和「版本功能对比」弹窗（归档） | kc-input、kc-select | scripts/t7_purchase.py | [x] |
| 8 | 账号与费用 | AcctProducts、AcctProductDetail、AcctUsage、AcctSubs、BillOrders、BillInvoice、BillContractApply、ConsoleHome* | 修改：去「企业版」，统一叫「授权」；ConsoleHome 待处理去掉 app-07「未授权」 | — | scripts/t8_acct.py | [x] |
| 9 | 服务器 | IdcServerDetail | 修改：安全页签里「企业版」字样去掉；写明德迅服务器随单赠送、不占授权 | — | scripts/t9_idc.py | [x] |
| 10 | 官网 | ProductHost | 修改：企业版区块改名为能力介绍；新增「怎么收费」4 格（3 台免费 / 按台购买 / 不绑机器 / 换机删旧加新）+ 价格待定；CTA「免费注册使用」「购买更多授权」 | 官网 tcx 样式 | scripts/t10_host.py | [x] |
| 11 | 官网 | HostFeature-*（8）、Main、Products、MegaMenu | 修改：CTA 与价格文案 | — | scripts/t11_site.py | [x] |
| 12 | 仓库 | docs/specs/德迅安全卫士-授权.md、decisions.md | 新建 spec；台账加 #N | — | — | [x] |
| 13 | 全部 | — | 用 redesign-verify-sync 校验（残留「企业版 / 个人版 / 未授权 / 绑定授权」应为 0）、同步画布、提交 | — | — | [x] |
