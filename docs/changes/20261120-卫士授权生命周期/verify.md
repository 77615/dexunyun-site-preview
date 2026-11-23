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
- [ ] 「更换保留主机」只有文字说明和链接，没有做选择主机的交互
- [ ] 没有处于「授权已到期」状态的示例主机（演示数据仍在宽限期内）

## 发布
- 卫士 LE5c v327、账号与费用 E1uu v206、服务器 N8Yuj v10、官网 JTat v122（2026-11-23）

## 不通过项
| 项 | 原因 | 处理 |
| --- | --- | --- |
| BillBalance「续费优先从余额扣」(P7) | 和 kyno3x 3903f36 的逆向修改一起处理 | 任务 6，推迟 |
| kyno3x 3903f36 合入（开通失败、核验超时、到期不续、退款） | 要逐页对照 11-17 之后的账号页版式 | 任务 6，推迟 |
| AcctPurchase 新购 / 扩容两态、BillConfirm 台数步进器 | 本次只改了提示文案 | 任务 3、5、12 部分完成 |
