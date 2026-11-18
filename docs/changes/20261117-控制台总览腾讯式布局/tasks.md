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
| T5 | canvas.json | 修改 | ConsoleHome 高度 1300，标题改 v6 | 手工 | 完成 |

脚本幂等（标记 tcl-v1）；输入里有 data-annotation-id 时，新账户卡带上 home-account / home-fees。
用法：`python3 scripts/tcl.py console/ConsoleHome.dc.html`

第二轮：`python3 scripts/tcl2.py console/*.dc.html`（只改带账号侧 4 项菜单的页面，标记 tcl2-v1）。
