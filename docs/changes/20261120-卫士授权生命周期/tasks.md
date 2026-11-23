# 任务：德迅安全卫士授权生命周期

| # | 画布 | 画板 | 动作 | 组件 / 交互规则 | 脚本 | 完成 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 卫士 LE5c | SecHosts、SecHome、SecAgent、SecLicense（共用主机数据） | 加「未受保护 · 授权已到期」原因与「更换保留主机」；宽限、排队、删除、卸载文案 | kc-tag warn、ac-al | scripts/t_sec2.py | [x] |
| 2 | 卫士 LE5c | 全部 Sec*（共用脚本） | 去掉插件授权文案 | — | scripts/t_sec2.py | [x] |
| 3 | 账号与费用 E1uu | AcctPurchase | 新购 / 扩容两态，折算说明 | 现有表单 | scripts/t_acct2.py | [~] 文案已改，表单交互未做 |
| 4 | 账号与费用 E1uu | AcctSubs、AcctProductDetail | 扩容改链、示例数对齐、去转移权益和旧概览 | kc-tiles | scripts/t_acct2.py | [x] |
| 5 | 账号与费用 E1uu | BillConfirm | 恢复文案；卫士续费可改台数 | 数量步进器 | scripts/t_acct2.py | [~] 文案已改，表单交互未做 |
| 6 | 账号与费用 E1uu | BillOrders、BillBalance、AcctProductDetail、SupTicketNew | 合入 kyno3x 3903f36 逆向修改，逐页对照 11-17 后的版式 | — | 手工合并 | [ ] 推迟 |
| 7 | 服务器 N8Yuj | IdcServerDetail | 卸载弹窗文案 | kc-modal | scripts/t_srv_site.py | [x] |
| 8 | 官网 JTat | Register | 注册即送 3 台 | — | scripts/t_srv_site.py | [x] |
| 9 | 仓库 | specs/德迅安全卫士-授权.md、decisions.md | 写入新规则；台账加两条（11-20 #1、#2） | — | — | [x] |
| 10 | 卫士 LE5c | SecHosts、SecLicense | 恢复顺序、数据保留日期、更换保留主机权限 | kc-tag、ac-al | scripts/t_sec2.py | [x] |
| 11 | 卫士 LE5c / 账号 E1uu | SecNotify、Notifications | 宽限期结束通知 | 现有通知行 | scripts/t_sec2.py、t_acct.py | [x] |
| 12 | 账号与费用 E1uu | AcctPurchase | 临近到期 / 宽限期扩容限制 | ac-al | scripts/t_acct2.py | [~] 文案已改，表单交互未做 |

实施前：重读线上画布，把 77 在画布里的改动合并进来。
