# 画布 → 预览站同步

控制台页面的源头是 6 个 Design 画布（账号与费用 E1uu、卫士 LE5c、DDoS RL3X、SCDN SfY2、游戏盾/云眼 9WQ1、服务器 N8Yu）。画布里跨画板的链接是 `https://claude.ai/artifact/<画布>#play-<id>`，预览站要换成 `console/` 下的相对路径。

1. 用 Artifact 工具把各画布的 `project/*.dc.html` 读到本目录：`<画布简称>/project/X.dc.html`（已在 .gitignore）。
2. `python3 convert.py`：按 `playmap.json` 换链接，去掉已删除的「产品详情中转页」兜底映射；仓库里同一行带 `?tab=` 等参数的保留仓库写法。结果在 `out/`。
3. 对比 `out/` 和 `console/`，确认只差画布上的新改动后复制过去，渲染检查后提交。
4. 出现新的 play 链接时 convert.py 会打印 MISS：先跑 `python3 learn.py`（按仓库现有页面反推映射），或手工补进 `playmap.json`。
