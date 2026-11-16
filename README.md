# 德迅云官网改版 · 高保真原型（静态预览）

由 Design 画布导出的静态站点，可直接用 GitHub Pages 预览。

- 入口：`index.html` → 首页 `Main.dc.html`
- 全部页面：`pages.html`
- `support.js` 为设计稿运行时（内含 React），每个 `*.dc.html` 页面独立运行
- 图片与视频在 `img/`；首页地球使用 jsDelivr 上的 cobe@0.6.3

本地预览：`python3 -m http.server` 后打开 http://localhost:8000 （直接双击 html 文件无法加载组件）。

_最近同步：2026-11-16 17:40，官网画布 + 5 个控制台画布（含新版控制台总览）。_
