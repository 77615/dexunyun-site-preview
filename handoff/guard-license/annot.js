/* 德迅安全卫士授权调整 · 标注版原型加载器
 * 加载 @axhub/annotation browser bundle 和 source.js，按文字给改动点元素打 data-annotation-id，
 * 再交给 Axhub 运行时渲染编号、气泡和侧边栏文档。标注 UI 全部来自 Axhub，这里只做定位和切页。 */
(function () {
  var BASE = (document.currentScript && document.currentScript.src || '').replace(/annot\.js.*$/, '');
  var PAGE = (location.pathname.split('/').pop() || '').replace(/\.dc\.html$/, '');
  function load(src) { return new Promise(function (ok, no) { var s = document.createElement('script'); s.src = src; s.onload = ok; s.onerror = no; document.head.appendChild(s); }); }

  function norm(s) { return (s || '').replace(/\s+/g, ' ').trim(); }
  function findByText(spec) {
    var texts = spec.t || [], nth = spec.nth || 0;
    var root = document.getElementById('dc-root') || document.querySelector('x-dc') || document.body;
    for (var k = 0; k < texts.length; k++) {
      var want = texts[k], hits = [];
      var all = root.querySelectorAll('*');
      for (var i = 0; i < all.length; i++) {
        var el = all[i];
        if (el.closest('[data-axhub-annotation-root],.axhub-annotation-root')) continue;
        var tx = norm(el.textContent);
        if (tx.indexOf(want) < 0) continue;
        var deeper = false;
        for (var j = 0; j < el.children.length; j++) { if (norm(el.children[j].textContent).indexOf(want) >= 0) { deeper = true; break; } }
        if (deeper) continue;
        var r = el.getBoundingClientRect();
        if (!r.width && !r.height) continue;
        hits.push(el);
      }
      if (hits.length) return spec.last ? hits[hits.length - 1] : hits[Math.min(nth, hits.length - 1)];
    }
    if (spec.sel) { var e = root.querySelector(spec.sel); if (e) return e; }
    return null;
  }

  var SRC = null;
  function tag() {
    if (!SRC) return false;
    var changed = false;
    SRC.data.nodes.forEach(function (n) {
      if (n.pageId !== PAGE) return;
      var spec = {}; try { spec = JSON.parse(n.locator.fingerprint); } catch (e) {}
      var cur = document.querySelector('[data-annotation-id="' + n.id + '"]');
      var el = findByText(spec);
      if (cur && cur === el) return;
      if (cur) cur.removeAttribute('data-annotation-id');
      if (el) el.setAttribute('data-annotation-id', n.id);
      changed = true;
    });
    return changed;
  }

  /* 快照里没有的页面：改去仓库里的完整预览 */
  function fixLinks(pages) {
    document.addEventListener('click', function (ev) {
      var a = ev.target.closest && ev.target.closest('a[href]');
      if (!a) return;
      var h = a.getAttribute('href') || '';
      var m = h.match(/^(?:\.\/)?([A-Za-z0-9-]+\.dc\.html)(.*)$/);
      if (!m || pages.indexOf(m[1]) >= 0) return;
      ev.preventDefault(); ev.stopPropagation();
      var site = /^(Main|Login|Legal|Docs|Register|Forgot|Product|Solution|Service|About|Contact|News|Trust|Faq)/.test(m[1]);
      location.href = BASE + (site ? '../../' : '../../console/') + m[1] + m[2];
    }, true);
  }

  Promise.all([load(BASE + 'vendor/axhub-annotation.global.js'), load(BASE + 'source.js'), load(BASE + 'pages.js')]).then(function () {
    SRC = window.__GL_ANNOT_SOURCE__;
    fixLinks(window.__GL_PAGES__ || []);
    var viewer = window.AxhubAnnotation.createAnnotationViewer({
      source: function () { return SRC; },
      resolveElement: function (loc) { return document.querySelector(loc.selectors[0]); },
      options: {
        getCurrentPageId: function () { return PAGE; },
        defaultMarkerIndexVisible: true,
        toolbarEdge: 'right',
        showBrandLink: false,
        emptyWhenNoData: true,
        onDirectoryRoute: function (node) { if (node.route && node.route !== PAGE) location.href = node.route + '.dc.html'; }
      }
    });
    window.__GL_VIEWER__ = viewer;
    var t = null;
    function retag() { clearTimeout(t); t = setTimeout(function () { if (tag()) viewer.refresh(); }, 250); }
    var tries = 0;
    (function wait() {
      tag();
      if (document.querySelector('[data-annotation-id]') || tries++ > 40) {
        viewer.start().then(function () { viewer.refresh(); });
        new MutationObserver(function (ms) {
          for (var i = 0; i < ms.length; i++) { var x = ms[i].target; if (x.nodeType === 3) x = x.parentElement; if (x && x.closest && x.closest('#dc-root, x-dc')) { retag(); return; } }
        }).observe(document.body, { childList: true, subtree: true, characterData: true });
      } else setTimeout(wait, 150);
    })();
  }).catch(function (e) { console.error('[标注] 加载失败', e); });
})();
