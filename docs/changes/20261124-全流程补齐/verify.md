# 校验：主流程与异常流程补齐

实施日期 2026-11-24。脚本：scripts/pur3.py、subs3.py、ddos3.py、auth3.py（幂等，第二次运行输出 already）。

## 规范一致
- [x] 颜色只用 token 或已有色值（#FFECE8 / #CB2634 同 kc 危险色），组件沿用 kc-btn / kc-tag / ac-al / fl-seg / fl-row
- [x] 逻辑脚本全部过 node --check（画布副本和仓库副本）
- [x] 术语：卫士「宽限期」，其他产品「保留期」「已释放」，没有混用

## 不重复
- [x] 购买入口：卫士授权和按规格产品共用 AcctPurchase，不恢复产品下拉
- [x] 通用状态只在 StateSpec 定义一次；LoadSpec 继续管加载与骨架屏

## 能点通（Playwright 本地渲染，仓库副本）
- [x] `console/AcctPurchase.dc.html?p=ddos&v=2` 显示 DDoS 企业型 ¥3,999.00；不带参数仍是卫士授权新购
- [x] `console/AcctSubs.dc.html?ft=hold` 列出高防-005、SCDN-002、web-old-01
- [x] DdosInstances 出现高防-005，无报错
- [x] Login 点「已锁定」、Forgot 点「与旧密码相同」显示对应报错（Forgot 自动切到第 2 步）
- [x] StateSpec 渲染无报错，高 3040

## 发布
- 账号与费用 E1uu v237、DDoS RL3X v42、官网 JTat v124（2026-11-24）

## 未做 / 待确认
| 项 | 原因 |
| --- | --- |
| 游戏盾 / SCDN / 云眼控制台内的到期态 | 等研发确认各产品保留期表现 |
| 登录页左侧「注册并完成认证，即可默认开通 SCDN、游戏盾、DDoS 高防 IP 基础版」 | 与「注册即送卫士 3 台」不一致，文案沿用现网，需 77 确认是否改 |
