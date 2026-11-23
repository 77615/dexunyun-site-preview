# 校验：德迅安全卫士授权生命周期

实施日期 2026-11-23。脚本：scripts/t_sec2.py（30 个 Sec* 页）、t_acct2.py（5 页）、t_srv_site.py（2 页），可重复运行（第二次运行改动 0 处）。

## 规范一致
- [x] 颜色只用 token，没有新增裸色值
- [x] 组件沿用 kc-tag / ac-al / kc-tiles，不新增
- [x] 逻辑脚本全部过 node --check（画布副本和仓库副本）
- [x] 术语：「授权已到期」「没能加入 · 授权已用满」「随服务器赠送，不占授权台数」与 spec 一致；去掉「转移权益」「插件授权」「释放授权、绑定」

## 不重复
- [x] 扩容入口只剩 AcctPurchase；AcctProductDetail 去掉 dx-guard-02，只留一批 54 台、同一到期日
- [x] 同一批授权在 SecLicense / SecHome / AcctSubs / AcctProductDetail / Notifications 说法一致：2026-11-01 到期，宽限至 11-08，11-08 后 54 台停止检测

## 能点通
- [x] 宽限提示里「资产列表」链到 SecHosts；AcctPurchase 提示里「续费」链到 BillConfirm
- [x] 「更换保留主机」：授权管理里的抽屉，最多选 3 台，默认最早接入的 3 台（第二轮）
- [ ] 没有处于「授权已到期」状态的示例主机：演示数据在宽限期内（11-04），加了会自相矛盾；抽屉里用「11-08 后停止检测」表达

## 发布
- 卫士 LE5c v327、账号与费用 E1uu v206、服务器 N8Yuj v10、官网 JTat v122（2026-11-23）

## 第二轮（2026-11-23，77：做完未完成的；选购页对齐费用中心）
- AcctPurchase 按 BillConfirm 结构重建，三态用页头「演示」切换；BillConfirm 加卫士台数步进器（只能减，减量核验到账后生效）
- kyno3x 3903f36 合入：AcctSubs、AcctTransfer、AcctTransferDetail（卫士转移那句画布已无对应文案，跳过）、BillBalance（余额只展示，退款原路退回）、BillOrders（用量账单、核验超时、开通失败、申请退款、已退款页签）、BillPayment（实名提示；保留现行「7 天未付自动取消」）、SupTicketDetail（问题未解决）、SupTicketNew（关联订单 / 退款 / 复制工单）、DdosInstances、ScdnPlan
- 发布：E1uu v207、LE5c v328、DDoS RL3X v41、SCDN SfY2 v44
- 仓库 console/ 仍是 11-17 前的账号页版式（费用中心左侧菜单版在 r7hjqo 分支未合入），仓库里的 AcctPurchase 按仓库现有的 BillConfirm 重建
- 未做渲染截图（环境不允许本地起浏览器渲染），逻辑脚本全部过 node --check

## 不通过项
| 项 | 原因 | 处理 |
| --- | --- | --- |
| 到期不续开关（kyno 放在 AcctProductDetail） | 该画板已取消，没有新位置 | 待定：放到我的产品卡片「更多」里 |

## 第三轮（2026-11-23，77「补上」）
- AcctPurchase 加三种状态：不足 30 天（拦住扩容，去续费）、已过宽限期（重新购买，从到账日起算，到账后按最早接入恢复被停主机，买几台恢复几台）、有待付款单（同一授权只能 1 笔待付款，按钮变「去付款」）。演示切换共 6 个
- 「购买产品」下拉改为固定「德迅安全卫士 · 主机授权」，其他产品引导到服务器选购页或官网产品页，不在这里重复下单
- 发布 E1uu v208；scripts/pur2.py
