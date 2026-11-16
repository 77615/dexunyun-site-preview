# boss #10 (2026-11-12): 威胁狩猎 告警时间线 on wide screens: text was centred with a big gap before the process chip.
# Now a left-aligned log grid: time | level dot | event + ATT&CK | command | process | status; stacks under 1500px.
import sys
CSS='''
/* ---- boss 2026-11-12：告警时间线宽屏排版 ---- */
.sl .hu-tlb .hu-tr1{grid-template-columns:64px 10px minmax(0,1fr) 140px 56px !important;align-items:start !important;text-align:left !important}
.sl .hu-tlb .hu-tm{display:flex !important;flex-direction:column !important;align-items:flex-start !important;justify-content:flex-start !important;gap:2px !important;text-align:left !important}
.sl .hu-tlb .hu-tmh{justify-content:flex-start !important}
.sl .hu-tlb .hu-tm code{display:block;max-width:100%;text-align:left !important}
.sl .hu-tlb .hu-tp{justify-self:start;border:0 !important;background:none !important;padding:0 !important;height:auto !important;line-height:20px !important;font:12px/20px Menlo,Monaco,Consolas,monospace !important;color:#86909c;text-align:left !important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}
.sl .hu-tlb .hu-ast{justify-self:end;line-height:20px}
@media (min-width:1500px){
  .sl .hu-tlb .hu-tr1{grid-template-columns:72px 10px minmax(220px,300px) minmax(0,1fr) 150px 64px !important;align-items:center !important;padding:10px 12px !important}
  .sl .hu-tlb .hu-tm{display:contents !important}
  .sl .hu-tlb .hu-tmh{flex-direction:column;align-items:flex-start !important;gap:0 !important;min-width:0}
  .sl .hu-tlb .hu-tmh small{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}
  .sl .hu-tlb .hu-tm code{padding:4px 10px;background:#f7f8fa;border-radius:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .sl .hu-tlb .hu-tr1 .hu-ld{margin-top:0 !important}
}
'''
f=sys.argv[1]; s=open(f).read()
if '告警时间线宽屏排版' in s: sys.exit('already')
k=s.rfind('</style>'); s=s[:k]+CSS+s[k:]; open(f,'w').write(s); print('ok')
