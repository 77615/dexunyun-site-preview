# 任务：控制台总览改成腾讯式布局

| # | 画板 | 动作 | 说明 | 脚本 | 状态 |
| --- | --- | --- | --- | --- | --- |
| T1 | ConsoleHome | 修改 | 去掉左侧菜单和折叠按钮 | scripts/tcl.py | 完成 |
| T2 | ConsoleHome | 新增 | 欢迎语下方页签 .tcl-tabs（总览 / 我的产品 / 费用 / 企业） | scripts/tcl.py | 完成 |
| T3 | ConsoleHome | 修改 | 账号条 + 费用信息合并成右上账户卡 .tcl-acct（内容不删） | scripts/tcl.py | 完成 |
| T4 | ConsoleHome | 修改 | 企业卡三格一行，右栏 440px、不吸顶 | scripts/tcl.py | 完成 |
| T5 | canvas.json | 修改 | ConsoleHome 高度 1300，标题改 v6 | 手工 | 完成 |

脚本幂等（标记 tcl-v1）；输入里有 data-annotation-id 时，新账户卡带上 home-account / home-fees。
用法：`python3 scripts/tcl.py console/ConsoleHome.dc.html`
