# 德迅云改版 · Spec 工作流

完整说明（含流程图）：https://claude.ai/artifact/7B2stPnzD646RQqi4PJnTN

每条改动（老板口述、77 的意见、客户反馈）都走同一条线：

| 阶段 | 产出 | 检查点 |
| --- | --- | --- |
| 0 收集反馈 | `changes/<日期>-<名称>/feedback.md` | 拿到原话；每条映射到画板页面 |
| 1 现状盘点 | 业务逻辑分析 + 现状问题（写进 proposal.md 的「现状」） | 事实 / 推断 / 待定分开；列出碰到的历史决策 |
| 2 变更提案 | `proposal.md` | **77 确认**（决策卡） |
| 3 设计与任务 | `tasks.md` | 不自造组件 |
| 4 实施 | `scripts/` 幂等补丁 + 改后的 .dc.html | 先重读线上画布；`node --check` |
| 5 校验 | `verify.md` | 校验清单全过或写明原因 |
| 6 同步归档 | 画布发布、仓库提交、更新 `specs/` 与 `decisions.md`、变更移入 `changes/archive/` | 画布、仓库、specs 三处一致 |

快车道：只改颜色、间距、文案（不动菜单、不增删页面、不碰业务规则）时跳过 1–3。

## 目录

- `specs/<模块>.md`：当前真相。模块 = 官网、账号与费用、SCDN、DDoS、游戏盾与云眼、服务器与德迅安全卫士。
- `changes/<YYYYMMDD>-<名称>/`：一次变更的全部材料。
- `changes/archive/`：已完成的变更。
- `decisions.md`：决策台账。
- `templates/`：空模板，新变更时复制。
