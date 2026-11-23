# 德迅安全卫士授权调整 · 开发交付包

| 文件 | 内容 |
| --- | --- |
| `docs/01-变更说明.md` | 授权规则 R01–R25、对象与状态流转、改动点 C01–C36、异常场景 E01–E16、待确认 Q1–Q6 |
| `docs/02-开发任务清单.md` | 数据 DA、后端 BE、前端 FE 任务，每条带规则编号和验收标准 |
| `index.html` | 标注版原型入口（GitHub Pages：`/handoff/guard-license/`） |
| `proto/` | 2026-11-23 画布快照（卫士 LE5c、账号与费用 E1uu、服务器详情、官网注册），每页末尾挂了 `../annot.js` |
| `annot.js` | 加载 Axhub 标注运行时，按文字定位改动点，处理切页；快照里没有的页面跳到仓库完整预览 |
| `source.js`、`pages.js` | 由 `build.py` 生成的标注数据，不要手改 |
| `vendor/` | `@axhub/annotation` 1.0.22 browser bundle（MIT） |

## 更新

1. 改文档：直接改 `docs/*.md`，改动点表格（`| Cxx | 页面 | 类型 | 说明 | 规则 |`）就是标注气泡的内容。
2. 改锚点：`build.py` 里的 `M` 列表，`text` 是页面上能看到的文字（可以给候选列表，适合多状态页面）。
3. 运行 `python3 handoff/guard-license/build.py`，重新生成 `source.js`、`pages.js`、`index.html`，并给新快照页面挂脚本（可重复运行）。
4. 画布更新后要刷新快照：用最新画布的 `.dc.html` 覆盖 `proto/` 里同名文件，再跑第 3 步。

编号规则：标注上的圆形数字按 `M` 的顺序生成，所以 `M` 的顺序必须和 C 编号一致。
