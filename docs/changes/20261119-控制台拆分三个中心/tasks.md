# 任务

| 编号 | 页面 | 动作 | 内容 | 脚本 | 状态 |
| --- | --- | --- | --- | --- | --- |
| T1 | Bill* 13 页、NoAccess | 修改 | 费用中心左侧菜单；去掉顶部 tab、问候语和二级分段，页头改菜单名，分段里的按钮移到页头；面包屑「费用中心」 | scripts/centers.py | 完成 |
| T2 | Org* 6 页 | 修改 | 企业中心左侧菜单，同上；面包屑「企业中心」 | scripts/centers.py | 完成 |
| T3 | SupTickets、SupTicketNew、SupTicketDetail、SupDocs、Notifications | 修改 | 支持中心左侧菜单；消息页顶栏名「消息中心」改「支持中心」 | scripts/centers.py | 完成 |
| T4 | 总览、我的产品等其余 12 页 | 修改 | 顶部 tab 只留「总览 / 我的产品」 | scripts/centers.py | 完成 |
| T5 | canvas.json | 修改 | 费用概览、企业信息、我的工单画板标题和分区标题改成中心说法 | 手工 | 完成 |

用法：`python3 scripts/centers.py <放账号与费用画板的目录>`（标记 ctr-v1，幂等；在 20261117 那一轮的全部脚本之后跑）。画布 E1uu v105（版本号 188）。
