# 反馈：德迅安全卫士授权 · 开通到到期的主流程、异常与逆向流程

- 来源：77 在项目线程提问（2026-11-20）；分析文档 https://claude.ai/artifact/2No7ckSQzFMoSCqjKsj5vA
- 前置：决策 #10（2026-11-19，三台免费、按台购买、只数台数）

| 编号 | 原话（逐字） | 类型 | 涉及页面 | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 主机安全的主要流程目前有调整，从开通服务到使用功能中，主要的流程比如第一次开通服务，购买额外的授权，再到购买的服务到期，中间的主要流程和异常流程以及逆向流程都有哪些 | 业务逻辑 | 卫士 SecLicense、SecHosts、SecAgent、SecHome；账号与费用 AcctPurchase、AcctSubs、AcctProductDetail、AcctUsage、BillConfirm、BillPayment、BillOrders、BillBalance；服务器 IdcServerDetail；官网 Register | 分析见文档 |
| F2 | （决策卡）已购授权到期或减少台数后，超出的主机怎么处理？→ 选「留在列表，超出几台停检测」 | 业务逻辑 | SecHosts、SecLicense、SecHome | 2026-11-20 |
| F3 | （文档评论）扩容「通常是怎么做的？哪种方式更简单」→ 回复推荐并入后：「好」 | 业务逻辑 | AcctPurchase、AcctSubs、AcctProductDetail、BillConfirm | 2026-11-20 |

快车道判断：涉及业务规则和购买入口 → 走完整流程。
