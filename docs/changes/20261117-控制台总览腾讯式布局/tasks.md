# 任务：控制台总览改成腾讯式布局

| # | 画板 | 动作 | 说明 | 脚本 | 状态 |
| --- | --- | --- | --- | --- | --- |
| T1 | ConsoleHome | 修改 | 去掉左侧菜单和折叠按钮 | scripts/tcl.py | 完成 |
| T2 | ConsoleHome | 新增 | 欢迎语下方页签 .tcl-tabs（总览 / 我的产品 / 费用 / 企业） | scripts/tcl.py | 完成 |
| T3 | ConsoleHome | 修改 | 账号条 + 费用信息合并成右上账户卡 .tcl-acct（内容不删） | scripts/tcl.py | 完成 |
| T4 | ConsoleHome | 修改 | 企业卡三格一行，右栏 440px、不吸顶 | scripts/tcl.py | 完成 |
| T6 | 账号与费用 37 页 | 修改 | 去左侧菜单，加一级页签 .tcl-tabs（分组页替换标题行） | scripts/tcl2.py | 完成 |
| T7 | ConsoleHome | 修改 | 去掉 Axhub 标注 script 和 data-annotation-id；页签 16px | 手工 | 完成 |
| T8 | 12 个分组页 | 修改 | 首页同款头部 + 胶囊二级页签 + 卡片样式 | scripts/tcl3.py | 完成 |
| T9 | AcctProducts | 修改 | 表格换成卡片版（状态分栏、卡片 / 列表切换、卡片操作栏、详情抽屉、胶囊容器页签、分段状态筛选） | scripts/pc.py | 完成 |
| T10 | 11 个分组页 | 修改 | 二级胶囊页签放进白色容器顶部、连到首张卡片；卡片内状态页签改灰底分段筛选 | scripts/hier.py | 完成 |
| T11 | 11 个分组页 | 修改 | 胶囊页签条和下面整块内容包进同一容器 div.hier-box（白底细边框）> 胶囊条 + 浅灰内底 div.hier-in，卡片放在内底里 | scripts/hier2.py | 完成 |
| T12 | AcctProducts | 修改 | 保留 77 画板里的微调（页签条灰底、白色卡片区、直角标签）；按腾讯语义色分三档状态、产品图标块三种淡彩、直角纯色进度条、黑色透明度文字、卡片悬停只加阴影、需处理计数红色 | scripts/pcsem.py | 完成 |
| T13 | AcctProducts | 修改 | 状态分组改成浅灰容器、标题在容器里；卡片 4px 圆角极浅阴影；底部去掉灰底条，左「进入控制台 ›」，右文字按钮 + 白底描边主按钮 | scripts/pcboard.py | 完成 |
| T14 | AcctProducts | 修改 | 筛选合成一行：左状态安静页签，右按产品/按资源分段、卡片/列表、搜索、购买产品；搜索过滤和无结果状态；加载中占位；无产品空状态；原型状态切换 | scripts/pcfiles.py | 完成 |
| T15 | AcctSubs | 修改 | 去掉容器顶部胶囊条；卡片顶部一行：左状态安静页签，右按产品/按资源分段 + 权益转移、到期提醒设置；容器白底，筛选栏与表格左右对齐 20 | scripts/subsuni.py | 完成 |
| T5 | canvas.json | 修改 | ConsoleHome 高度 1300，标题改 v6 | 手工 | 完成 |

脚本幂等（标记 tcl-v1）；输入里有 data-annotation-id 时，新账户卡带上 home-account / home-fees。
用法：`python3 scripts/tcl.py console/ConsoleHome.dc.html`

第二轮：`python3 scripts/tcl2.py console/*.dc.html`（只改带账号侧 4 项菜单的页面，标记 tcl2-v1）。

第四轮：`python3 scripts/pc.py console/AcctProducts.dc.html out.html`，再把 title 改成「我的产品」、data-pg 和「按产品」链接改回 AcctProducts；`python3 scripts/hier.py console/{AcctSubs,Bill*,Org*}.dc.html`（只改分组页，标记 hier-v1）。画布 E1uu v96。
第五轮：`python3 scripts/hier2.py console/{AcctSubs,Bill*,Org*}.dc.html`（需先跑 hier.py，标记 hier-v2）。画布 E1uu v97。
第六轮：`python3 scripts/pcsem.py console/AcctProducts.dc.html`（在 pc.py 之后，标记 pcsem-v1）。画布 E1uu v98（版本号 162）。
第七轮：`python3 scripts/pcboard.py console/AcctProducts.dc.html`（在 pcsem.py 之后，标记 pcb-v1）。
第八轮：`python3 scripts/pcfiles.py console/AcctProducts.dc.html`（在 pcboard.py 之后，标记 pcf-v1）。
第九轮：`python3 scripts/subsuni.py console/AcctSubs.dc.html`（在 hier2.py 之后，标记 sbu-v1）。
