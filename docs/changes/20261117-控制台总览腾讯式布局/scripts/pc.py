#!/usr/bin/env python3
"""我的产品 · 卡片版对比稿（参考 Agent Inbox Board 的组织方式）。
从 AcctProducts.dc.html 生成 AcctProductsCards.dc.html：
- 按「需处理 / 正常运行 / 已结束」分组的产品卡片，筛选胶囊带数量
- 卡片 / 列表切换；点卡片右侧抽屉看状态、操作和最近动态
用法: pc.py AcctProducts.dc.html AcctProductsCards.dc.html
"""
import re, sys

src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()

ICB = '<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3 3h8v8H3V3zm2 2v4h4V5H5zm8-2h8v8h-8V3zm2 2v4h4V5h-4zM3 13h8v8H3v-8zm2 2v4h4v-4H5zm8-2h8v8h-8v-8zm2 2v4h4v-4h-4z"/></svg>'
ICL = '<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 4h13v2H8V4zM3 3.5h3v3H3v-3zm0 7h3v3H3v-3zm0 7h3v3H3v-3zM8 11h13v2H8v-2zm0 7h13v2H8v-2z"/></svg>'

HTML = f'''<section class="pc">
        <nav class="pc-tabs" aria-label="我的产品"><a class="on" aria-current="page" href="AcctProductsCards.dc.html">按产品</a><a href="AcctSubs.dc.html">按资源</a></nav>
        <div class="pc-in">
        <div class="pc-bar">
          <div class="pc-sc" role="tablist" aria-label="按状态筛选"><sc-for list="{{{{pcScopes}}}}" as="s" hint-placeholder-count="4"><button type="button" role="tab" class="{{{{s.cls}}}}" aria-selected="{{{{s.on}}}}" onClick="{{{{s.go}}}}">{{{{s.n}}}}<em class="pc-n">{{{{s.c}}}}</em></button></sc-for></div>
          <div class="pc-tools"><div class="pc-vw" role="radiogroup" aria-label="视图"><button type="button" role="radio" title="卡片" aria-label="卡片" class="{{{{pcVbC}}}}" aria-checked="{{{{pcVbOn}}}}" onClick="{{{{pcToB}}}}">{ICB}</button><button type="button" role="radio" title="列表" aria-label="列表" class="{{{{pcVlC}}}}" aria-checked="{{{{pcVlOn}}}}" onClick="{{{{pcToL}}}}">{ICL}</button></div><a class="kc-btn pri" href="AcctPurchase.dc.html">购买产品</a></div>
        </div>
        <sc-if value="{{{{pcBoard}}}}" hint-placeholder-val="{{{{true}}}}"><div class="pc-wall"><sc-for list="{{{{pcLanes}}}}" as="l" hint-placeholder-count="3"><div class="pc-lane"><header class="pc-lh"><i class="{{{{l.mk}}}}"></i><b>{{{{l.n}}}}</b><span>{{{{l.c}}}}</span></header>
          <ul class="pc-grid"><sc-for list="{{{{l.items}}}}" as="p" hint-placeholder-count="3"><li class="{{{{p.cls}}}}"><button type="button" class="pc-cm" onClick="{{{{p.open}}}}">
            <span class="pc-tt"><span class="pc-ico"><i class="{{{{p.di}}}}"></i></span><span class="pc-nm"><b>{{{{p.n}}}}</b><small>{{{{p.plan}}}}</small></span><span class="{{{{p.chip}}}}"><i class="{{{{p.mk}}}}"></i>{{{{p.sw}}}}</span></span>
            <span class="pc-tx">{{{{p.text}}}}</span>
            <span class="{{{{p.uCls}}}}"><span class="pc-ub"><i class="{{{{p.uc}}}}" style="{{{{p.uw}}}}"></i></span><em>{{{{p.ut}}}}</em></span>
            <span class="pc-meta"><span class="{{{{p.exC}}}}">{{{{p.exp}}}}</span></span>
          </button><div class="pc-ft"><sc-for list="{{{{p.acts}}}}" as="a" hint-placeholder-count="2"><a class="{{{{a.cls}}}}" href="{{{{a.href}}}}">{{{{a.t}}}}</a></sc-for><a class="pc-con" href="{{{{p.con}}}}">{{{{p.conT}}}}<svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.17 12 8.22 7.05l1.42-1.41L16 12l-6.36 6.36-1.42-1.41z"/></svg></a></div></li></sc-for></ul></div></sc-for></div></sc-if>
        <sc-if value="{{{{pcList}}}}" hint-placeholder-val="{{{{false}}}}"><div class="pc-lst"><sc-for list="{{{{pcLanes}}}}" as="l" hint-placeholder-count="3"><div class="pc-lg"><header class="pc-lh"><i class="{{{{l.mk}}}}"></i><b>{{{{l.n}}}}</b><span>{{{{l.c}}}}</span></header>
          <ul><sc-for list="{{{{l.items}}}}" as="p" hint-placeholder-count="3"><li class="{{{{p.cls}}}}"><button type="button" class="pc-rw" onClick="{{{{p.open}}}}"><span class="pc-rn"><span class="pc-ico sm"><i class="{{{{p.di}}}}"></i></span><b>{{{{p.n}}}}</b></span><span class="pc-rp">{{{{p.plan}}}}</span><span class="pc-rt">{{{{p.text}}}}</span><span class="pc-st"><i class="{{{{p.mk}}}}"></i>{{{{p.sw}}}}</span><span class="{{{{p.exC}}}}">{{{{p.exp}}}}</span></button></li></sc-for></ul></div></sc-for></div></sc-if>
        </div>
      </section>
      <sc-if value="{{{{pcDOn}}}}" hint-placeholder-val="{{{{false}}}}"><div class="kc-dmask" onClick="{{{{pcClose}}}}"></div><aside class="kc-dw pc-dw" role="dialog" aria-label="产品详情"><div class="kc-dwh"><span>产品详情</span><button type="button" class="pc-x" aria-label="关闭" onClick="{{{{pcClose}}}}">×</button></div>
        <div class="kc-dwb"><div class="pc-dh"><span class="pc-ico"><i class="{{{{pcD.di}}}}"></i></span><div><h3>{{{{pcD.n}}}}</h3><p><span class="{{{{pcD.tag}}}}">{{{{pcD.sw}}}}</span><small>{{{{pcD.plan}}}}</small></p></div></div>
          <p class="pc-dd">{{{{pcD.text}}}}</p>
          <div class="pc-da"><sc-for list="{{{{pcD.acts}}}}" as="a" hint-placeholder-count="2"><a class="{{{{a.cls}}}}" href="{{{{a.href}}}}">{{{{a.t}}}}</a></sc-for></div>
          <dl class="pc-kv"><sc-for list="{{{{pcD.kv}}}}" as="k" hint-placeholder-count="4"><dt>{{{{k.k}}}}</dt><dd>{{{{k.v}}}}</dd></sc-for></dl>
          <h4>最近动态</h4><ol class="pc-steps"><sc-for list="{{{{pcD.steps}}}}" as="x" hint-placeholder-count="3"><li class="{{{{x.cls}}}}"><span>{{{{x.t}}}}</span><time>{{{{x.d}}}}</time></li></sc-for></ol></div>
        <div class="kc-dwf"><a class="kc-btn" href="{{{{pcD.con}}}}">进入控制台</a></div></aside></sc-if>'''

CSS = '''
/* pc-v1 我的产品 · 卡片版 */
.kc .kc-main>.pc{margin-top:0!important}
.kc main.kc-main>.kc-dmask,.kc main.kc-main>.kc-dw{margin:0!important}
.kc .kc-main>.pc{display:block!important;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.05)}
.pc-tabs{display:flex;gap:8px;padding:16px 20px;border-bottom:1px solid #f0f2f5}
.pc-tabs>a{display:inline-flex;align-items:center;height:32px;padding:0 16px;border:1px solid #e6e9ef;border-radius:16px;background:#fff;font-size:13px;color:rgba(0,0,0,.7);text-decoration:none;transition:color .15s,border-color .15s}
.pc-tabs>a:hover{color:#1664ff;border-color:#c6d8ff}
.pc-tabs>a.on{background:#e5ecff;border-color:#e5ecff;color:#1664ff;font-weight:500}
.kc .kc-main .pc>.pc-in{margin:0!important;padding:16px 20px 20px}
.pc-bar{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:0 0 16px}
.pc-sc{display:inline-flex;padding:2px;background:#f2f3f5}
.pc-sc button{display:inline-flex;align-items:center;gap:6px;height:28px;padding:0 14px;border:0;background:transparent;font:inherit;font-size:13px;color:rgba(0,0,0,.6);cursor:pointer;transition:background-color .14s,color .14s}
.pc-sc button:hover{color:rgba(0,0,0,.9)}
.pc-sc button.on{background:#fff;color:rgba(0,0,0,.9);font-weight:500;box-shadow:0 1px 2px rgba(0,0,0,.08)}
.pc-sc button>.pc-n{font-style:normal;font-size:12px;font-weight:400;color:rgba(0,0,0,.4);font-variant-numeric:tabular-nums}
.pc-tools{display:flex;align-items:center;gap:12px}
.pc-vw{display:inline-flex;gap:2px;padding:2px;background:#f2f3f5}
.pc-vw button{display:grid;place-items:center;width:28px;height:28px;border:0;background:transparent;color:rgba(0,0,0,.5);cursor:pointer}
.pc-vw button:hover{color:rgba(0,0,0,.9)}
.pc-vw button.on{background:#fff;color:#1664ff;box-shadow:0 1px 2px rgba(0,0,0,.06)}
.pc-lane+.pc-lane{margin-top:24px}
.pc-lh{display:flex;align-items:center;gap:8px;height:24px;margin:0 0 12px;font-size:13px}
.pc-lh b{font-weight:500;color:rgba(0,0,0,.9)}
.pc-lh>span{min-width:20px;padding:0 6px;background:#e5e8ef;font-size:12px;line-height:18px;text-align:center;color:rgba(0,0,0,.6);font-variant-numeric:tabular-nums}
.pc-mk{display:inline-block;flex:none;width:14px;height:14px;box-sizing:border-box;border-radius:50%}
.pc-mk.err{width:14px;height:14px;border:0;border-radius:0;background:#f53f3f;-webkit-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18z'/%3E%3Cpath d='M12 8v4.5'/%3E%3Cpath d='M12 16h.01'/%3E%3C/svg%3E") center/contain no-repeat;mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18z'/%3E%3Cpath d='M12 8v4.5'/%3E%3Cpath d='M12 16h.01'/%3E%3C/svg%3E") center/contain no-repeat}
.pc-mk.warn{width:14px;height:14px;border-radius:0;background:#ff7d00;-webkit-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z'/%3E%3Cpath d='M12 9v4'/%3E%3Cpath d='M12 17h.01'/%3E%3C/svg%3E") center/contain no-repeat;mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z'/%3E%3Cpath d='M12 9v4'/%3E%3Cpath d='M12 17h.01'/%3E%3C/svg%3E") center/contain no-repeat}
.pc-mk.ok{width:14px;height:14px;border:0;border-radius:0;background:#00b42a;-webkit-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18z'/%3E%3Cpath d='m8.5 12.2 2.4 2.4 4.6-4.8'/%3E%3C/svg%3E") center/contain no-repeat;mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18z'/%3E%3Cpath d='m8.5 12.2 2.4 2.4 4.6-4.8'/%3E%3C/svg%3E") center/contain no-repeat}
.pc-mk.mut{width:14px;height:14px;border:0;border-radius:0;background:#86909c;-webkit-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18z'/%3E%3Cpath d='M8.5 12h7'/%3E%3C/svg%3E") center/contain no-repeat;mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18z'/%3E%3Cpath d='M8.5 12h7'/%3E%3C/svg%3E") center/contain no-repeat}
.pc-ico .dt{width:20px!important;height:20px!important;flex-basis:20px!important;filter:none!important;opacity:1!important;vertical-align:0}
.pc-ico.sm{width:28px;height:28px}
.pc-ico.sm .dt{width:16px!important;height:16px!important;flex-basis:16px!important}
.pc-wall{padding:20px;background:#f5f6f8}
.pc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px;margin:0;padding:0;list-style:none}
.pc-c:hover{box-shadow:0 0 0 1px rgba(22,100,255,.18),0 8px 24px -8px rgba(15,23,42,.14)}
.pc-c.cur{box-shadow:0 0 0 1px #1664ff,0 8px 24px -8px rgba(22,100,255,.25)}
.pc-tt{display:flex;align-items:flex-start;gap:12px;min-width:0}
.pc-ico{display:grid;flex:none;place-items:center;width:40px;height:40px;border-radius:2px;background:linear-gradient(145deg,#eef4ff,#e1eaff)}
.pc-nm{display:grid;flex:1;min-width:0;padding-top:1px}
.pc-nm b{overflow:hidden;font-size:14px;font-weight:600;line-height:22px;white-space:nowrap;text-overflow:ellipsis;color:rgba(0,0,0,.9)}
.pc-nm small{font-size:12px;line-height:18px;color:rgba(0,0,0,.45)}
.pc-chip{display:inline-flex;flex:none;align-items:center;gap:4px;height:22px;padding:0 8px 0 6px;border-radius:11px;font-size:12px;font-weight:500;white-space:nowrap}
.pc-chip .pc-mk{width:12px;height:12px}
.pc-chip.err{background:#fff0f0;color:#cb2634}
.pc-chip.warn{background:#fff5e8;color:#c2570a}
.pc-chip.ok{background:#ebf9ef;color:#0e8a3a}
.pc-chip.mut{background:#f2f3f5;color:#4e5969}
.pc-tx{display:-webkit-box;height:40px;margin-top:14px;overflow:hidden;-webkit-line-clamp:2;-webkit-box-orient:vertical;font-size:13px;line-height:20px;color:rgba(0,0,0,.6)}
.pc-u{display:flex;align-items:center;gap:12px;height:16px;margin-top:14px}
.pc-ub{position:relative;flex:1;height:4px;border-radius:2px;background:#eef0f4;overflow:hidden}
.pc-ub i{position:absolute;left:0;top:0;bottom:0;border-radius:2px;background:linear-gradient(90deg,#4e8dff,#1664ff)}
.pc-ub i.o{background:linear-gradient(90deg,#ffb35c,#ff7d00)}
.pc-ub i.r{background:linear-gradient(90deg,#ff7a7a,#f53f3f)}
.pc-u em{flex:none;font-style:normal;font-size:12px;color:rgba(0,0,0,.5);font-variant-numeric:tabular-nums}
.pc-ex{overflow:hidden;white-space:nowrap;text-overflow:ellipsis;color:rgba(0,0,0,.5);font-variant-numeric:tabular-nums}
.pc-ex.o{color:#c2570a}
.pc-ex.r{color:#cb2634}
.pc-c{position:relative;display:flex;flex-direction:column;background:#fff;border-radius:2px;box-shadow:0 0 0 1px rgba(15,23,42,.04),0 1px 2px rgba(15,23,42,.04);transition:box-shadow .2s}
.pc-cm{display:flex;flex:1;flex-direction:column;gap:0;width:100%;padding:20px 20px 16px;border:0;background:none;font:inherit;text-align:left;cursor:pointer}
.pc-meta{display:flex;align-items:center;height:18px;margin-top:12px;font-size:12px}
.pc-ft{display:flex;align-items:center;gap:20px;height:44px;padding:0 20px;background:#fafbfc;border-top:1px solid #f2f3f5;font-size:13px}
.pc-act{color:rgba(0,0,0,.7);text-decoration:none;transition:color .15s}
.pc-act:hover{color:#1664ff}
.pc-act.pri{color:#1664ff;font-weight:500}
.pc-act.pri:hover{color:#4080ff}
.pc-con{display:inline-flex;align-items:center;gap:2px;margin-left:auto;color:rgba(0,0,0,.7);text-decoration:none;transition:color .15s}
.pc-con svg{transition:transform .2s}
.pc-con:hover{color:#1664ff}
.pc-con:hover svg{transform:translateX(2px)}
.pc-u.no{visibility:hidden}
.pc-st{display:inline-flex;align-items:center;gap:6px;white-space:nowrap;color:rgba(0,0,0,.9)}
.pc-lst{border:1px solid #f0f2f5}
.pc-lg .pc-lh{margin:0!important}
.pc-lg .pc-lh{height:40px;margin:0;padding:0 20px;background:#f7f8fa}
.pc-lg+.pc-lg{margin-top:8px}
.pc-lg ul{margin:0;padding:0;list-style:none}
.pc-rw{display:grid;grid-template-columns:200px 150px minmax(0,1fr) 110px 190px;align-items:center;gap:16px;width:100%;height:56px;padding:0 20px;border:0;background:none;font:inherit;font-size:13px;text-align:left;cursor:pointer}
.kc .pc-lg li{margin:0;border:0!important;border-bottom:1px solid #f0f2f5!important}
.kc .pc-lg li:last-child{border-bottom:0!important}
.pc-rw:hover,.pc-c.cur .pc-rw{background:#f5f8ff}
.pc-rn{display:flex;align-items:center;gap:10px;min-width:0}
.pc-rn b{overflow:hidden;font-weight:500;white-space:nowrap;text-overflow:ellipsis;color:rgba(0,0,0,.9)}
.pc-rp{color:rgba(0,0,0,.55);white-space:nowrap}
.pc-rt{overflow:hidden;white-space:nowrap;text-overflow:ellipsis;color:rgba(0,0,0,.65)}
.pc-rw .pc-ex{text-align:right}
.pc-lst .pc-c{background:none;box-shadow:none}
.pc-x{width:28px;height:28px;border:0;background:none;font-size:20px;line-height:1;color:rgba(0,0,0,.5);cursor:pointer}
.pc-x:hover{color:rgba(0,0,0,.9)}
.pc-dh{display:flex;align-items:center;gap:14px}
.pc-dh .pc-ico{width:48px;height:48px}
.pc-dh h3{margin:0;font-size:18px;line-height:26px;font-weight:600;color:rgba(0,0,0,.9)}
.pc-dh p{display:flex;align-items:center;gap:8px;margin:4px 0 0}
.pc-dh small{font-size:12px;color:rgba(0,0,0,.5)}
.pc-dd{margin:16px 0 0;font-size:13px;line-height:22px;color:rgba(0,0,0,.75)}
.pc-da{display:flex;gap:8px;margin-top:16px}
.pc-kv{display:grid;grid-template-columns:88px minmax(0,1fr);row-gap:12px;margin:24px 0 0;padding:16px 0 0;border-top:1px solid #f0f2f5;font-size:13px}
.pc-kv dt{color:rgba(0,0,0,.5)}
.pc-kv dd{margin:0;color:rgba(0,0,0,.9);font-variant-numeric:tabular-nums}
.pc-dw .kc-dwb h4{margin:24px 0 12px;font-size:13px;font-weight:500;color:rgba(0,0,0,.9)}
.pc-steps{position:relative;display:grid;gap:12px;margin:0;padding:14px 16px 14px 32px;list-style:none;background:#f7f8fa}
.pc-steps li{position:relative;display:flex;justify-content:space-between;gap:12px;font-size:13px;line-height:20px;color:rgba(0,0,0,.75)}
.pc-steps li::before{content:"";position:absolute;top:7px;left:-16px;width:6px;height:6px;border-radius:50%;background:#c2c7d0}
.pc-steps li:not(:last-child)::after{content:"";position:absolute;top:17px;bottom:-11px;left:-14px;width:1px;background:#e5e8ef}
.pc-steps li.now::before{background:#1664ff}
.pc-steps time{flex:none;color:rgba(0,0,0,.4);font-variant-numeric:tabular-nums}
'''

JS = r'''  /* pc-v1 我的产品 · 卡片版 */
  _pc() {
    const st = this.state || {}; const sc = st.pcS || 'all'; const vw = st.pcV || 'board'; const op = st.pcO || '';
    const DDOS = 'https://claude.ai/artifact/RL3XvNLs2o41CLGG3mLqe9#play-d1c5e98bff1b', ATK = 'https://claude.ai/artifact/RL3XvNLs2o41CLGG3mLqe9#play-5b7ed2d4829c';
    const HOST = 'https://claude.ai/artifact/LE5cNnQWZjPMjXvXCC4MG7#play-de5201e8a0c7', GAME = 'https://claude.ai/artifact/9WQ1i2DeBHUULxBDB2KQ6p#play-ef67b4d479f4';
    const SCDN = 'https://claude.ai/artifact/SfY2uSBB9Y6d1vwU1sb1cD#play-15dd8cd198dd', EYE = 'https://claude.ai/artifact/9WQ1i2DeBHUULxBDB2KQ6p#play-1f4762e5e343';
    const IDC = 'https://claude.ai/artifact/N8Yuj4E7xMtsnFAbT8om5A#play-e1a7a42a37df', BUY = 'BillConfirm.dc.html';
    // key, name, plan, category, text, state word, tone, expiry, expiry tone, usage [text, pct, tone] | null, actions, console, kv extra, steps
    const P = [
      ['ddos', 'DDoS 高防 IP', '4 个实例', '云安全', '高防-002 正在被 UDP Flood 攻击，峰值 86 Gbps，已自动清洗。最早一个实例 13 天后到期。', '攻击中', 'err', '最早 11-09 到期 · 剩 13 天', 'o', null,
        [['查看攻击', ATK, 1], ['续费', BUY]], DDOS, [['实例', '4 个'], ['保底防护', '100 Gbps']], [['攻击峰值 86 Gbps，清洗中', '今天 10:24'], ['高防-002 开始被攻击，已自动清洗', '今天 10:06'], ['高防-001 续费成功', '10-27']]],
      ['host', '德迅安全卫士', '企业版 · 50 台', '主机安全', '授权已到期，数据保留到 11 月 8 日。目前接入 68 台主机，超出授权 18 台。', '已到期', 'err', '10-25 已到期 · 保留至 11-08', 'r', ['68 / 50 台', 100, 'r'],
        [['续费', BUY, 1], ['扩容授权', BUY]], HOST, [['授权', '50 台'], ['已接入', '68 台']], [['新接入 web-new-03、web-new-04，超出授权的主机不做检测', '11-01'], ['授权到期，进入保留期', '10-25']]],
      ['game', '游戏盾', '专业版 · 2,000 并发', '云安全', '并发已用 85%，晚高峰可能超过上限，超出部分会被限流。', '接近上限', 'warn', '2027-01-12 到期 · 剩 77 天', '', ['1,700 / 2,000 并发', 85, 'o'],
        [['升级', BUY, 1], ['续费', BUY]], GAME, [['并发上限', '2,000'], ['当前并发', '1,700']], [['并发峰值 1,700', '昨天 21:52'], ['并发超过 80%', '昨天 21:40']]],
      ['ssl', 'SSL 证书', 'DV × 3 张', '云安全', 'www.example.com 的证书 8 天后到期，到期后浏览器会提示网站不安全。', '即将到期', 'warn', '最早 11-04 到期 · 剩 8 天', 'o', null,
        [['续费', BUY, 1]], 'AcctSubs.dc.html', [['证书', '3 张']], [['到期提醒已发送', '10-27'], ['m.example.com 证书签发', '09-12']]],
      ['idc', '服务器租用', '独享型 · 3 台', 'IDC 服务', '3 台服务器运行中，最早一台 24 天后到期。', '即将到期', 'warn', '最早 11-20 到期 · 剩 24 天', 'o', null,
        [['续费', BUY, 1], ['升级配置', BUY]], IDC, [['服务器', '3 台']], [['到期提醒已发送', '10-27'], ['web-prod-01 重启完成', '10-26']]],
      ['scdn', 'SCDN', '企业版 · 10 域名', '云安全', '已接入 6 个域名，还可以再接入 4 个。', '运行中', 'ok', '2027-03-18 到期 · 剩 142 天', '', ['6 / 10 域名', 60, ''],
        [['续费', BUY], ['升级', BUY]], SCDN, [['域名', '6 / 10']], [['CC 防护改为严格模式', '今天 10:41'], ['shop.example.com 接入完成', '10-21']]],
      ['eye', '德迅云眼', '标准版 · 20 资产', '安全运营', '正在监测 12 个资产，还可以再添加 8 个。', '运行中', 'ok', '2027-05-02 到期 · 剩 187 天', '', ['12 / 20 资产', 60, ''],
        [['续费', BUY], ['扩容', BUY]], EYE, [['资产', '12 / 20']], [['完成一次全量监测', '今天 03:00'], ['新增资产 m.example.com', '10-26']]],
      ['vss', '漏洞扫描 VSS', '基础版 · 5 站点', '安全运营', '已添加 2 个站点，还可以再添加 3 个。', '运行中', 'ok', '2027-02-20 到期 · 剩 116 天', '', ['2 / 5 站点', 40, ''],
        [['续费', BUY], ['升级', BUY]], 'AcctSubs.dc.html', [['站点', '2 / 5']], [['www.example.com 扫描完成', '10-28']]],
      ['dj', '等保咨询', '二级 · 一次性服务', '安全服务', '服务已在 8 月 30 日完成，可以下载服务报告。', '已完成', 'mut', '2026-08-30 完成', '', null,
        [['服务报告', 'SupDocs.dc.html', 1]], 'SupDocs.dc.html', [], [['服务报告已上传', '08-30'], ['现场测评完成', '08-22']]]
    ];
    const lane = (t) => (t === 'err' || t === 'warn' ? 'need' : t === 'ok' ? 'ok' : 'end');
    const LN = [['need', '需处理', 'warn'], ['ok', '正常运行', 'ok'], ['end', '已结束', 'mut']];
    const TAG = { err: 'kc-tag err', warn: 'kc-tag warn', ok: 'kc-tag ok', mut: 'kc-tag mut' };
    const cnt = (k) => P.filter((p) => lane(p[6]) === k).length;
    const pcScopes = [['all', '全部', P.length]].concat(LN.map((l) => [l[0], l[1], cnt(l[0])])).map(([k, n, c]) => ({ n, c, on: k === sc ? 'true' : 'false', cls: k === sc ? 'on' : '', go: () => this.setState({ pcS: k }) }));
    const item = (p) => ({ acts: p[10].map((x) => ({ t: x[0], href: x[1], cls: x[2] ? 'pc-act pri' : 'pc-act' })), con: p[11], conT: p[0] === 'dj' ? '查看服务' : '进入控制台', chip: 'pc-chip ' + p[6], n: p[1], plan: p[2], text: p[4], sw: p[5], mk: 'pc-mk ' + p[6], exp: p[7], exC: 'pc-ex' + (p[8] ? ' ' + p[8] : ''), di: this.__di(p[1]) || 'dt dt-db',
      uCls: p[9] ? 'pc-u' : 'pc-u no', ut: p[9] ? p[9][0] : '', uw: 'width:' + (p[9] ? p[9][1] : 0) + '%', uc: p[9] ? p[9][2] : '',
      cls: 'pc-c' + (op === p[0] ? ' cur' : ''), open: () => this.setState({ pcO: p[0] }) });
    const pcLanes = LN.filter((l) => sc === 'all' || sc === l[0]).map((l) => { const items = P.filter((p) => lane(p[6]) === l[0]).map(item); return { n: l[1], c: items.length, mk: 'pc-mk ' + l[2], items }; }).filter((l) => l.items.length);
    const D = P.find((p) => p[0] === op);
    const pcD = D ? { n: D[1], plan: D[2], text: D[4], sw: D[5], tag: TAG[D[6]], di: this.__di(D[1]) || 'dt dt-db', con: D[11],
      acts: D[10].map((a) => ({ t: a[0], href: a[1], cls: a[2] ? 'kc-btn pri' : 'kc-btn' })),
      kv: [{ k: '状态', v: D[5] }, { k: '分类', v: D[3] }, { k: '套餐', v: D[2] }].concat(D[9] ? [{ k: '用量', v: D[9][0] }] : []).concat(D[12].map((x) => ({ k: x[0], v: x[1] }))).concat([{ k: '到期', v: D[7] }]),
      steps: D[13].map((x, i) => ({ t: x[0], d: x[1], cls: i === 0 ? 'now' : '' })) } : { n: '', plan: '', text: '', sw: '', tag: '', di: '', con: '#', acts: [], kv: [], steps: [] };
    return { pcScopes, pcLanes, pcBoard: vw === 'board', pcList: vw === 'list',
      pcVbC: vw === 'board' ? 'on' : '', pcVlC: vw === 'list' ? 'on' : '', pcVbOn: vw === 'board' ? 'true' : 'false', pcVlOn: vw === 'list' ? 'true' : 'false',
      pcToB: () => this.setState({ pcV: 'board' }), pcToL: () => this.setState({ pcV: 'list' }),
      pcDOn: !!D, pcD, pcClose: () => this.setState({ pcO: '' }) };
  }
'''

if 'pc-v1' in s:
    sys.exit('already')
s, n = re.subn(r'<section class="kc-card">\s*<div class="kc-tabs" role="tablist">.*?</section>', lambda m: HTML, s, count=1, flags=re.S)
assert n == 1, 'card'
s = s.replace('<nav class="ia-tabs" aria-label="我的产品"><a class="on" aria-current="page" href="AcctProducts.dc.html">按产品</a><a href="AcctSubs.dc.html">按资源</a></nav>', '', 1)
s = s.replace('data-pg="AcctProducts"', 'data-pg="AcctProductsCards"')
s = s.replace('const o = this._rv(); o.hd', 'const o = Object.assign(this._rv(), this._pc()); o.hd', 1)
assert 'this._pc()' in s
k = s.index('  _rv() {')
s = s[:k] + JS + s[k:]
i = s.index('<x-dc>'); j = s.index('</style>', i)
s = s[:j] + CSS + s[j:]
s = s.replace('<title>', '<title>', 1)
open(out, 'w', encoding='utf-8').write(s)
print('ok')
