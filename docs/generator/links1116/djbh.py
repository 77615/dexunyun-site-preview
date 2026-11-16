# -*- coding: utf-8 -*-
"""2026-11-16 官网「等保合规咨询」独立页 ServiceDJBH（原来 7 处入口都只跳安全服务页 #djbh 锚点）。
用 boss1112/pages.py 的外壳和渲染器生成；价格与方案内容来自现有 Services.dc.html#djbh（官网 32,000 / 41,000 / 73,000 元/年）。
然后把官网和控制台里指向 Services.dc.html#djbh 的链接改到新页。用法：python3 djbh.py <repo>
"""
import sys, os, re, glob
ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'boss1112'))
sys.argv = [sys.argv[0], ROOT]
import pages as G
from pages_data import svc, CONTACT

p = svc('ServiceDJBH.dc.html', '等保合规咨询', '等保 2.0 合规咨询',
 '与专业咨询机构、测评机构通力合作，从定级、备案、建设整改到等保测评全程陪跑，快速省心过等保。', [
 dict(t='cards', id='why', nav='为什么要做', title='为什么要做等保', min=280, icons=['doc', 'shield', 'users'], items=[
  ('法律要求', '《网络安全法》规定网络运营者应当按照网络安全等级保护制度履行安全保护义务。'),
  ('行业要求', '政务、金融、教育、医疗、能源等行业主管部门要求信息系统通过等级保护测评。'),
  ('业务需要', '招投标、上线审批和客户审核常常要求提供等保备案证明和测评报告。')]),
 dict(t='steps', id='flow', nav='服务流程', title='五步过等保', bg='#FFFFFF', items=[
  ('定级', '确定系统安全等级，准备定级报告'), ('备案', '准备备案材料，到当地公安网监递交备案'),
  ('建设整改', '按等保技术与管理要求建设整改'), ('等保测评', '准备和接受测评机构的测评'), ('监督检查', '接受公安网监定期检查，每年定期测评')]),
 dict(t='table', id='plans', nav='方案与价格', title='方案与价格', sub='官网默认组合价，可按实际系统增减产品。等保套餐需选购 2 个或以上付费产品。', bg='#F7F8FA',
  head=['', '等保二级方案', '等保三级方案（基础）· 推荐', '等保三级方案（增强）'],
  rows=[['适合', '一般信息系统', '重要信息系统', '更完整的纵深防御'],
        ['安全通信网络', '云防火墙、SSL 证书', '云防火墙、SSL 证书', '云防火墙、SSL 证书'],
        ['安全区域边界', 'DDoS 高防、Web 应用防火墙', 'DDoS 高防、Web 应用防火墙', 'DDoS 高防、Web 应用防火墙'],
        ['安全计算环境', '主机安全、漏洞扫描', '主机安全、漏洞扫描、审计', '主机安全、漏洞扫描、审计'],
        ['安全管理中心', '安全运营与专家服务', '安全运营与专家服务', '安全运营与专家服务'],
        ['价格', '¥32,000 元 / 年', '¥41,000 元 / 年', '¥73,000 元 / 年']],
  btns=[('咨询', CONTACT), ('咨询', CONTACT), ('咨询', CONTACT)]),
 dict(t='deep', id='adv', nav='我们的优势', title='我们的优势', items=[
  ('01', '联合测评机构', '与各地测评机构、咨询机构合作，减少反复沟通。'), ('02', '产品覆盖测评项', '高防、WAF、主机安全、漏洞扫描等自有产品直接对应技术要求。'),
  ('03', '全程陪跑', '从定级材料到整改清单，专人跟进到拿到测评报告。')]),
 ], faq=[('等保二级和三级怎么选？', '按系统受破坏后对社会秩序、公共利益的影响程度定级。一般企业官网、内部系统多为二级；涉及大量个人信息、交易或政务服务的多为三级。我们会在定级阶段协助判断。'),
         ('从开始到拿到测评报告要多久？', '通常 1 到 3 个月，取决于整改工作量和测评机构排期。'),
         ('已经有部分安全产品，还要全部重新买吗？', '不需要。方案价是官网默认组合，可以按已有产品增减，咨询时告诉我们现状即可。')],
 related=[('漏洞扫描 VSS', 'Web 与系统漏洞检测', 'ProductVSS.dc.html'), ('风险评估', '系统评估资产风险', 'ServiceRisk.dc.html'), ('德迅卫士', '主机安全', 'ProductHost.dc.html')])
s, h = G.build(p)
open(os.path.join(ROOT, p['file']), 'w', encoding='utf-8').write(s)

n = 0
for f in glob.glob(os.path.join(ROOT, '*.dc.html')) + glob.glob(os.path.join(ROOT, 'console', '*.dc.html')):
    t = open(f, encoding='utf-8').read(); o = t
    t = t.replace('href="Services.dc.html#djbh"', 'href="ServiceDJBH.dc.html"').replace("'../Services.dc.html#djbh'", "'../ServiceDJBH.dc.html'").replace('"../Services.dc.html#djbh"', '"../ServiceDJBH.dc.html"')
    if t != o: open(f, 'w', encoding='utf-8').write(t); n += 1
print('ServiceDJBH', h, 'relinked', n)
