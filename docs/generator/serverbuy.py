# -*- coding: utf-8 -*-
"""服务器租用直达购买页 ServerBuy.dc.html (2026-11-09).
Data = live www.dexunyun.com/placeOrder (6 types, regions, DDoS tiers, configs, prices, OS list), read 2026-11-09.
usage: python3 serverbuy.py <base.css (Legal helmet <style> without closing tag)> <qnav.html> <out.dc.html>
"""
import json, sys

C = ["CPU:E5-2697V2*2(48线程)/内存:64G", "CPU:Gold-6138*2(80线程)/内存:128G", "CPU:E5-2696V4*2(88线程)/内存:128G",
     "CPU:E5-2670*2(32线程)/内存:32G", "CPU:Gold-6138*2(80线程)/内存:128G/硬盘:1T固态",
     "CPU:I9-9900K/内存:64G(DDR4 3200Hz)/硬盘:M.2 512G固态", "CPU:I9-14900K/内存:128G(DDR4 3200Hz)/硬盘:M.2 1T固态",
     "CPU:R9-9950X/内存:128G(DDR5 5600Hz)/硬盘:M.2 1T固态", "CPU:I9-10900K/内存:64G(DDR4 3200Hz)/硬盘:M.2 1T固态",
     "CPU:I9-14900K/内存:128G(DDR4 3200Hz)/硬盘:U.2 1T固态", "CPU:R9-9950X/内存:192G(DDR5 5600Mhz)/硬盘:U.2 1T固态"]
B = [["1 个 · BGP", "50Mbps"], ["1 个 · BGP", "100Mbps"], ["1 个 · BGP", "30Mbps"], ["1 个 · BGP", "150Mbps"], ["1 个 · BGP", "200Mbps"],
     ["1 个", "30Mbps"], ["1 个", "50Mbps"], ["1 个", "100Mbps"],
     ["1 个 · 电信", "30Mbps"], ["1 个 · 电信", "50Mbps"], ["1 个 · 电信", "100Mbps"], ["1 个 · 电信", "200Mbps"],
     ["1 个 · BGP", "300M 峰值（100M 独享）"], ["1 个 · BGP", "500M 峰值（200M 独享）"], ["1 个 · BGP", "100M 峰值（50M 独享）"],
     ["1 个", "300M 峰值（100M 独享）"], ["1 个", "500M 峰值（200M 独享）"]]

HP = "针对高性能计算应用领域，单核心计算性能达到传统服务器的1.5倍，适合高负载应用。"
HPU = "针对高性能计算应用领域，单核心计算性能达到传统服务器的1.5倍，适合高负载UDP应用。"
KS = "攻击打不死，专接扛不住。承诺打死按天退款。"
A = {
 "杭州BGP": (0, KS, [["200G", [[0,0,1399],[1,0,1499,1],[2,0,1599],[0,1,1999],[1,1,2099,1],[2,1,2199]]], ["300G", [[0,1,2999],[1,1,3099,1],[2,1,3199]]], ["400G", [[0,1,4500],[1,1,4600,1],[2,1,4700]]], ["500G", [[0,1,9800],[1,1,9900,1],[2,1,10000]]], ["600G", [[0,1,19800],[1,1,19900,1],[2,1,20000]]]]),
 "温州BGP": (1, "浙江省核心骨干网，线路极优质，网络稳定性高达99.9%。", [["200G", [[3,0,899],[0,0,999],[1,0,1099,1],[3,1,1299],[2,0,1299],[0,1,1399],[1,1,1499,1],[2,1,1699]]], ["300G", [[3,1,1999],[0,1,2099],[1,1,2199,1],[2,1,2399]]], ["400G", [[3,1,2999],[0,1,3099],[1,1,3199,1],[2,1,3399]]]]),
 "宁波BGP": (0, "浙江省星级数据中心，网络稳定性高达99.9%。", [["120G", [[3,0,899],[0,0,949],[1,0,999,1],[2,0,1299]]], ["200G", [[3,1,1299],[0,1,1349],[1,1,1399,1],[2,1,1699]]], ["300G", [[3,1,1999],[0,1,2099],[1,1,2199,1],[2,1,2399]]]]),
 "龙港BGP": (0, "BGP线路质量安全稳定，辐射整个东南区域。", [["100G", [[3,2,599],[0,2,699],[1,2,799,1],[2,2,999]]], ["200G", [[3,0,899],[0,0,999],[1,0,1099,1],[2,0,1299]]]]),
 "襄阳BGP": (0, "国家骨干网，优化互联互通，T级集群联动，UDP业务专享。", [["200G", [[3,0,599],[1,0,699]]], ["300G", [[3,1,1199],[1,1,1299]]], ["400G", [[3,3,2199],[1,3,2299]]]]),
 "山东BGP": (0, "省骨干直连，网络高速稳定，适合高负载UDP应用。", [["100G", [[3,0,599],[4,0,799],[3,1,999],[4,1,1099]]], ["200G", [[3,1,1099],[4,1,1299]]], ["300G", [[3,1,2099],[4,1,2299]]]]),
 "杭州BGP 高性能": (0, KS, [["200G", [[5,0,1500],[6,0,1999],[7,0,1999],[5,1,2200],[6,1,2699],[7,1,2699]]], ["300G", [[5,1,3200],[6,1,3699],[7,1,3699]]], ["400G", [[5,1,4700],[6,1,5200],[7,1,5200]]], ["500G", [[5,1,10000],[6,1,10500],[7,1,10500]]], ["600G", [[5,1,20000],[6,1,20500],[7,1,20500]]]]),
 "温州BGP 高性能": (1, HP, [["200G", [[5,0,1200],[5,1,1500],[6,0,1699],[7,0,1699],[6,1,1999],[7,1,1999]]], ["300G", [[5,1,2500],[6,1,2999],[7,1,2999]]], ["400G", [[5,1,3500],[6,1,3999],[7,1,3999]]]]),
 "宁波BGP 高性能": (0, HP, [["200G", [[8,0,1200],[8,1,1500],[6,0,1599],[7,0,1599],[6,1,1899],[7,1,1899]]], ["300G", [[8,1,2500],[6,1,2699],[7,1,2699]]]]),
 "龙港BGP 高性能": (0, HP, [["100G", [[5,0,999],[5,1,1299],[6,0,1500],[7,0,1500],[6,1,1799],[7,1,1799]]], ["200G", [[5,0,1200],[5,1,1500],[6,0,1799],[7,0,1799],[6,1,1999],[7,1,1999]]]]),
 "襄阳BGP 高性能": (0, HPU, [["200G", [[6,1,1500],[7,1,1500]]], ["300G", [[6,3,2500],[7,3,2500]]], ["400G", [[6,4,3500],[7,4,3500]]]]),
 "山东BGP 高性能": (0, HPU, [["200G", [[9,0,1499],[9,1,1799],[10,0,1799],[10,1,1999]]], ["300G", [[9,1,2799],[10,1,2999]]], ["400G", [[9,1,3799],[10,1,3999]]]]),
 "杭州电信": (0, "T级集群联动，阻断海外恶意流量，国家级骨干直连点，网络稳定性高达99.99%。", [["200G", [[3,5,399],[3,6,499],[1,6,599]]], ["300G", [[3,5,499],[3,6,599],[1,6,699]]], ["400G", [[3,5,699],[3,6,799],[1,6,899]]], ["500G", [[3,5,1299],[3,6,1399],[1,6,1499]]]]),
 "宁波电信": (0, "国家骨干网，优化互联互通，网络稳定性高达99.99%。", [["100G", [[3,5,399],[0,5,449],[3,6,499],[0,6,549],[1,6,599,1],[3,7,699],[0,7,749],[1,7,799,1]]]]),
 "襄阳电信": (0, "国家骨干网，优化互联互通，T级集群联动，UDP业务专享。", [["200G", [[3,6,399]]], ["300G", [[3,6,599],[1,6,699,1],[3,7,799],[1,7,899,1]]], ["400G", [[3,6,1299],[1,6,1399,1],[3,7,1499],[1,7,1599,1]]]]),
 "宁波电信 高性能": (0, HP, [["100G", [[5,8,599],[5,9,699],[5,10,899],[6,8,1099],[6,9,1299],[7,9,1299],[6,10,1499],[7,10,1499],[6,11,1999]]]]),
 "温州BGP（核心骨干）": (0, "浙江省核心骨干网，线路极优质，网络稳定性高达99.9%。", [["100G", [[3,14,899],[0,14,999],[3,12,1099],[0,12,1199],[3,13,1799],[0,13,1899]]]]),
 "宁波BGP（核心骨干）": (0, "浙江省核心骨干网，BGP线路质量安全稳定。", [["100G", [[3,12,1099],[0,12,1199],[3,13,1799],[0,13,1899]]]]),
 "襄阳电信（核心骨干）": (1, "华中骨干网，优化互联互通，T级集群联动，UDP业务专享。", [["200G", [[3,15,799],[3,16,1599]]]]),
 "宁波电信（国干直联）": (0, "国家骨干网，优化互联互通，网络稳定性高达99.99%。", [["100G", [[3,15,799],[0,15,899],[3,16,1599],[0,16,1699]]]]),
 "UDP高防（BGP）": (0, KS, [["200G", [[3,1,1199],[1,1,1299],[3,4,1899],[1,4,1999]]], ["300G", [[3,1,1699],[1,1,1799],[3,4,2499],[1,4,2599]]], ["400G", [[3,1,2199],[1,1,2299],[3,4,2999],[1,4,3099]]]]),
 "UDP高防（电信）": (0, KS, [["300G", [[3,7,1399],[0,7,1499]]], ["400G", [[3,7,1999],[0,7,2099]]], ["500G", [[3,7,2999],[0,7,3099]]], ["600G", [[3,7,4999],[0,7,5099]]]]),
}
HPR = ["杭州BGP 高性能", "温州BGP 高性能", "宁波BGP 高性能", "龙港BGP 高性能", "襄阳BGP 高性能", "山东BGP 高性能"]
T = [
 ["BGP 服务器", "多线智能选路，12 个机房", "ic-hfserver", ["杭州BGP", "温州BGP", "宁波BGP", "龙港BGP", "襄阳BGP", "山东BGP"] + HPR],
 ["电信服务器", "骨干直连，¥399/月起", "ic-ecs", ["杭州电信", "宁波电信", "襄阳电信", "宁波电信 高性能"]],
 ["高性能服务器", "单核性能约 1.5 倍", "ic-baremetal", [r for r in HPR if r != "山东BGP 高性能"] + ["宁波电信 高性能"]],
 ["大带宽服务器", "骨干网独享大带宽", "ic-accel", ["温州BGP（核心骨干）", "宁波BGP（核心骨干）", "襄阳电信（核心骨干）", "宁波电信（国干直联）"]],
 ["UDP 高防专区", "游戏与实时应用首选", "ic-ddos", ["UDP高防（BGP）", "UDP高防（电信）"]],
 ["抗 D 弹性计费", "按需调整，以报价为准", "ic-wall", ["杭州BGP", "杭州BGP 高性能", "UDP高防（BGP）"]],
]
OS = [
 ["Windows", ["Windows Server 2025 64位", "Windows Server 2022 64位", "Windows Server 2019 64位", "Windows Server 2016 64位", "Windows Server 2012 R2 64位", "Windows Server 2008 R2 64位", "Windows 10 64位", "Windows 7 64位"]],
 ["CentOS", ["CentOS 7.9 64位", "CentOS 7.6 64位", "CentOS 8.5 64位", "CentOS 8 Stream 64位", "CentOS 9 Stream 64位", "CentOS 6.9 64位"]],
 ["Ubuntu", ["Ubuntu 22.04 64位", "Ubuntu 20.04 64位", "Ubuntu 18.04 64位", "Ubuntu 16.04 64位"]],
 ["Debian", ["Debian 11.6 64位", "Debian 11.3 64位", "Debian 10.1 64位", "Debian 9.4 64位"]],
 ["Rocky", ["Rocky Linux 10", "Rocky Linux 9.6", "Rocky Linux 9.5", "Rocky Linux 8.9"]],
 ["Fedora", ["Fedora 35.0", "Fedora 34.0"]],
 ["FreeBSD", ["FreeBSD 15.0", "FreeBSD 14.3", "FreeBSD 13.5", "FreeBSD 12.1"]],
]
M = [[1, "1 个月"], [2, "2 个月"], [3, "3 个月"], [6, "6 个月"], [12, "1 年"], [24, "2 年"], [36, "3 年"]]

def cfg_split(s):
    parts = s.replace("CPU:", "").split("/")
    cpu = parts[0]
    rest = [p.replace("内存:", "内存 ").replace("硬盘:", "硬盘 ") for p in parts[1:]]
    return cpu, " · ".join(rest)

regions = {}
for name, (tj, desc, fh) in A.items():
    regions[name] = {"tj": tj, "d": desc, "fh": [[f[0], [[*cfg_split(C[c[0]]), B[c[1]][0], B[c[1]][1], c[2], 1 if len(c) > 3 else 0] for c in f[1]]] for f in fh]}
DATA = {"T": [[t[0], t[1], t[2], t[3]] for t in T], "R": regions, "OS": OS, "M": M}

CSS = r"""
/* ---- 服务器租用直达购买页（.sb 作用域） ---- */
.sb{background:#F7F8FA}
.sb-top{background:#FFFFFF;border-bottom:1px solid #E5E6EB}
.sb-gift{display:flex;flex-wrap:wrap;gap:8px 28px;font-size:13px;color:#4E5969}
.sb-gift span{display:inline-flex;align-items:center;gap:6px}
.sb-gift i{font-style:normal;display:inline-flex;align-items:center;justify-content:center;height:18px;padding:0 6px;font-size:12px;color:#165DFF;background:#E8F3FF;border-radius:2px}
.sb-main{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:20px;align-items:start;padding-top:20px;padding-bottom:64px}
.sb-blk{background:#FFFFFF;border:1px solid #E5E6EB;border-radius:2px;padding:24px 24px;margin-bottom:16px}
.sb-blk h2{margin:0 0 20px;font-size:18px;line-height:26px;font-weight:600;color:#1D2129;display:flex;align-items:center;gap:12px}
.sb-blk h2 small{font-size:13px;font-weight:400;color:#86909C}
.sb-row{display:grid;grid-template-columns:84px minmax(0,1fr);gap:16px;align-items:start}
.sb-row+.sb-row{margin-top:20px}
.sb-lb{font-size:14px;color:#4E5969;line-height:40px}
.sb-types{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.sb-type{position:relative;display:flex;gap:12px;align-items:center;padding:14px 16px;border:1px solid #E5E6EB;border-radius:2px;background:#FFFFFF;cursor:pointer;text-align:left;font-family:inherit;transition:border-color .2s,background .2s;overflow:hidden}
.sb-type:hover{border-color:#94BFFF}
.sb-type img{width:40px;height:40px;object-fit:contain;flex:none}
.sb-type b{display:block;font-size:15px;font-weight:600;color:#1D2129}
.sb-type span{display:block;font-size:12px;line-height:18px;color:#86909C;margin-top:2px}
.sb-on{border-color:#165DFF !important;background:#F2F7FF !important}
.sb-on::after{content:"";position:absolute;right:0;top:0;border-style:solid;border-width:0 22px 22px 0;border-color:transparent #165DFF transparent transparent}
.sb-on::before{content:"";position:absolute;right:3px;top:3px;width:7px;height:4px;border-left:1.5px solid #FFFFFF;border-bottom:1.5px solid #FFFFFF;transform:rotate(-45deg);z-index:1}
.sb-opts{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.sb-opts.f6{grid-template-columns:repeat(6,minmax(0,1fr))}
.sb-opts.f7{grid-template-columns:repeat(7,minmax(0,1fr))}
.sb-opts.fx{display:flex;flex-wrap:wrap}.sb-opts.fx{gap:8px}.sb-opts.fx .sb-opt{min-width:0;padding:0 14px}
.sb-opt.has-tj{padding-right:34px}
.sb-opt{position:relative;height:40px;padding:0 10px;border:1px solid #E5E6EB;border-radius:2px;background:#FFFFFF;font-size:14px;color:#1D2129;cursor:pointer;font-family:inherit;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;transition:border-color .2s,color .2s,background .2s}
.sb-opt:hover{border-color:#94BFFF;color:#165DFF}
.sb-opt.sb-on{color:#165DFF;font-weight:500}
.sb-opt em{position:absolute;right:-1px;top:-1px;font-style:normal;font-size:11px;line-height:16px;padding:0 5px;background:#FF7D00;color:#FFFFFF;border-radius:0 2px 0 2px}
.sb-note{margin-top:10px;display:flex;gap:6px;align-items:flex-start;font-size:13px;line-height:20px;color:#86909C}
.sb-tbl{width:100%;border-collapse:collapse;font-size:14px}
.sb-tbl th{text-align:left;font-weight:500;color:#4E5969;background:#F7F8FA;height:40px;padding:0 12px;border-bottom:1px solid #E5E6EB}
.sb-tbl td{padding:12px;border-bottom:1px solid #F2F3F5;vertical-align:middle}
.sb-tbl tr.sb-tr{cursor:pointer;transition:background .15s}
.sb-tbl tr.sb-tr:hover{background:#F7F9FC}
.sb-tbl tr.sb-tr-on,.sb-tbl tr.sb-tr-on:hover{background:#F2F7FF}
.sb-rd{width:16px;height:16px;border-radius:50%;border:1px solid #C9CDD4;box-sizing:border-box;display:inline-block;vertical-align:middle;transition:border .15s}
.sb-tr-on .sb-rd{border:5px solid #165DFF}
.sb-cpu{font-weight:500;color:#1D2129;white-space:nowrap}
.sb-mem{font-size:12px;color:#86909C;margin-top:2px}
.sb-pr{color:#F53F3F;font-weight:600;font-family:"DIN Alternate",Bahnschrift,Inter,Arial,sans-serif;font-size:18px;white-space:nowrap}
.sb-pr small{font-size:12px;color:#86909C;font-weight:400;margin-left:2px;font-family:inherit}
.sb-hot{display:inline-flex;align-items:center;height:18px;padding:0 6px;margin-left:8px;font-size:11px;color:#F53F3F;border:1px solid #FDCDC5;background:#FFF2EE;border-radius:2px;vertical-align:2px}
.sb-sel{height:40px;min-width:280px;padding:0 36px 0 12px;border:1px solid #E5E6EB;border-radius:2px;background:#FFFFFF url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2386909C' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E") no-repeat right 12px center;font-size:14px;color:#1D2129;font-family:inherit;-webkit-appearance:none;appearance:none;margin-top:10px}
.sb-sel:focus{outline:none;border-color:#165DFF}
.sb-step{display:inline-flex;height:40px;border:1px solid #E5E6EB;border-radius:2px;overflow:hidden}
.sb-step button{width:40px;border:0;background:#F7F8FA;font-size:18px;color:#4E5969;cursor:pointer;font-family:inherit}
.sb-step button:hover{color:#165DFF}
.sb-step span{width:56px;display:flex;align-items:center;justify-content:center;font-size:14px;border-left:1px solid #E5E6EB;border-right:1px solid #E5E6EB}
.sb-ck{display:inline-flex;align-items:center;gap:8px;font-size:14px;color:#4E5969;cursor:pointer;background:none;border:0;padding:0;font-family:inherit}
.sb-ck i{width:16px;height:16px;border:1px solid #C9CDD4;border-radius:2px;box-sizing:border-box;display:inline-flex;align-items:center;justify-content:center}
.sb-ck-on i{background:#165DFF;border-color:#165DFF}
.sb-ck-on i::after{content:"";width:7px;height:4px;border-left:1.5px solid #FFFFFF;border-bottom:1.5px solid #FFFFFF;transform:translateY(-1px) rotate(-45deg)}
.sb-ta{width:100%;box-sizing:border-box;min-height:84px;padding:10px 12px;border:1px solid #E5E6EB;border-radius:2px;font-size:14px;font-family:inherit;resize:vertical;color:#1D2129}
.sb-ta:focus{outline:none;border-color:#165DFF}
.sb-side{position:sticky;top:80px}
.sb-sum{background:#FFFFFF;border:1px solid #E5E6EB;border-radius:2px}
.sb-sum h3{margin:0;padding:18px 24px;font-size:16px;font-weight:600;border-bottom:1px solid #F2F3F5}
.sb-dl{margin:0;padding:16px 24px;display:grid;grid-template-columns:72px minmax(0,1fr);gap:10px 12px;font-size:13px;line-height:20px}
.sb-dl dt{color:#86909C}.sb-dl dd{margin:0;color:#1D2129;word-break:break-all}
.sb-tot{padding:16px 24px 24px;border-top:1px solid #F2F3F5}
.sb-calc{font-size:12px;color:#86909C}
.sb-big{display:flex;align-items:baseline;gap:4px;margin:8px 0 16px;color:#F53F3F;font-family:"DIN Alternate",Bahnschrift,Inter,Arial,sans-serif;font-weight:700}
.sb-big small{font-size:18px}.sb-big b{font-size:34px;line-height:40px;letter-spacing:-.01em}
.sb-buy{width:100%;height:44px;border:0;border-radius:2px;background:#165DFF;color:#FFFFFF;font-size:16px;font-weight:500;cursor:pointer;font-family:inherit;transition:background .15s}
.sb-buy:hover{background:#0E42D2}
.sb-sub{margin-top:12px;display:flex;justify-content:space-between;font-size:13px;color:#4E5969}
.sb-mini{margin-top:12px;font-size:12px;line-height:18px;color:#86909C}
.sb-help{margin-top:16px;background:#FFFFFF;border:1px solid #E5E6EB;border-radius:2px;padding:16px 24px;font-size:13px;line-height:22px;color:#4E5969}
.sb-faq{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.sb-faq div{background:#FFFFFF;border:1px solid #E5E6EB;border-radius:2px;padding:20px}
.sb-faq b{display:block;font-size:15px;font-weight:600;margin-bottom:8px}
.sb-faq p{margin:0;font-size:13px;line-height:22px;color:#4E5969}
.sb-mask{position:fixed;inset:0;z-index:50;background:rgba(29,33,41,0.45);display:flex;align-items:center;justify-content:center}
.sb-dlg{width:560px;max-width:calc(100vw - 32px);background:#FFFFFF;border-radius:2px;box-shadow:0 12px 40px rgba(0,0,0,0.18)}
.sb-dlg header{display:flex;justify-content:space-between;align-items:center;padding:18px 24px;border-bottom:1px solid #F2F3F5;font-size:16px;font-weight:600}
.sb-x{width:28px;height:28px;border:0;background:none;font-size:20px;color:#86909C;cursor:pointer}
.sb-x:hover{color:#1D2129}
.sb-dlg .sb-dl{grid-template-columns:96px minmax(0,1fr)}
.sb-pay{margin:0 24px;padding:12px 16px;background:#F2F7FF;border-radius:2px;font-size:13px;line-height:22px;color:#4E5969}
.sb-ft{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:16px 24px;border-top:1px solid #F2F3F5;margin-top:16px}
.sb-ft .sb-buy{width:auto;padding:0 28px;height:40px;font-size:14px}
.sb-buy[disabled]{background:#94BFFF;cursor:not-allowed}
.sb-ok{padding:36px 24px 8px;text-align:center}
.sb-ok i{display:inline-flex;width:48px;height:48px;border-radius:50%;background:#E8FFEA;align-items:center;justify-content:center}
.sb-ok h4{margin:16px 0 8px;font-size:18px}
.sb-ok p{margin:0;font-size:14px;line-height:22px;color:#4E5969}
@media (max-width:1100px){.sb-main{grid-template-columns:1fr}.sb-side{position:static}.sb-types{grid-template-columns:repeat(2,minmax(0,1fr))}.sb-opts,.sb-opts.f6,.sb-opts.f7{grid-template-columns:repeat(3,minmax(0,1fr))}.sb-faq{grid-template-columns:repeat(2,minmax(0,1fr))}}
"""

CHECK = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#86909C" stroke-width="2" aria-hidden="true" style="flex:none;margin-top:3px"><circle cx="12" cy="12" r="9"></circle><path d="M12 8v5M12 16h.01"></path></svg>'

BODY = """
<div class="tcx sb" data-pg="ServerBuy" style="min-width:0">
<div style="position:sticky;top:0;z-index:5"><dc-import name="Header" active="products" hint-size="100%,60px"></dc-import></div>
<section class="sb-top">
  <div class="wrap" style="padding-top:20px;padding-bottom:20px;display:flex;flex-direction:column;gap:12px">
    <nav aria-label="面包屑" class="crumb" style="display:flex;gap:8px;flex-wrap:wrap"><a href="Main.dc.html">首页</a> <span aria-hidden="true">/</span> <a href="Products.dc.html">产品与服务</a> <span aria-hidden="true">/</span> <span style="color:#1D2129">服务器租用</span></nav>
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap">
      <div><h1 style="margin:0;font-size:28px;line-height:38px;font-weight:600;color:#1D2129">服务器租用</h1>
      <p style="margin:6px 0 0;font-size:14px;line-height:22px;color:#4E5969">T 级数据中心，BGP 多线与电信骨干直连，自带 DDoS 原生防护，选好配置即可下单。</p></div>
      <div class="sb-gift"><span><i>赠</i>自主化管理平台</span><span><i>赠</i><a href="ProductHost.dc.html" style="color:inherit">德迅安全卫士</a></span><span><i>赠</i>Web 云防护</span><span><i>赠</i>1V1 专家 7×24 支撑</span></div>
    </div>
  </div>
</section>
<section>
<div class="wrap sb-main">
  <div style="min-width:0">
    <div class="sb-blk">
      <h2>类型与机房</h2>
      <div class="sb-row"><div class="sb-lb">类型</div>
        <div class="sb-types">TYPES_STATIC</div>
      </div>
      <div class="sb-row"><div class="sb-lb">地区</div>
        <div><div class="sb-opts"><sc-for list="{{ regs }}" as="o" hint-placeholder-count="8"><button type="button" class="sb-opt {{ o.cls }} {{ o.tjc }}" onClick="{{ o.go }}" title="{{ o.n }}">{{ o.n }}<sc-if value="{{ o.tj }}" hint-placeholder-val="{{ false }}"><em>推荐</em></sc-if></button></sc-for></div>
        <div class="sb-note">""" + CHECK + """<span>{{ regDesc }}</span></div></div>
      </div>
      <div class="sb-row"><div class="sb-lb">DDoS 防护</div>
        <div class="sb-opts f6"><sc-for list="{{ fhs }}" as="o" hint-placeholder-count="5"><button type="button" class="sb-opt {{ o.cls }}" onClick="{{ o.go }}">{{ o.n }}</button></sc-for></div>
      </div>
    </div>
    <div class="sb-blk">
      <h2>配置选择<small>以下为该机房当前在售机型，价格为每台每月</small></h2>
      <table class="sb-tbl">
        <thead><tr><th style="width:44px"></th><th>配置</th><th style="width:96px">IP 数</th><th style="width:150px">带宽</th><th style="width:110px;text-align:right">价格</th></tr></thead>
        <tbody><sc-for list="{{ cfgs }}" as="o" hint-placeholder-count="6"><tr class="sb-tr {{ o.cls }}" onClick="{{ o.go }}"><td><span class="sb-rd"></span></td><td><div class="sb-cpu">{{ o.cpu }}<sc-if value="{{ o.hot }}" hint-placeholder-val="{{ false }}"><span class="sb-hot">爆款</span></sc-if></div><div class="sb-mem">{{ o.mem }}</div></td><td>{{ o.ip }}</td><td>{{ o.bw }}</td><td style="text-align:right"><span class="sb-pr">¥{{ o.p }}<small>/月</small></span></td></tr></sc-for></tbody>
      </table>
    </div>
    <div class="sb-blk">
      <h2>系统与购买量</h2>
      <div class="sb-row"><div class="sb-lb">操作系统</div>
        <div><div class="sb-opts fx"><sc-for list="{{ osf }}" as="o" hint-placeholder-count="7"><button type="button" class="sb-opt {{ o.cls }}" onClick="{{ o.go }}">{{ o.n }}</button></sc-for></div>
        <select class="sb-sel" value="{{ osV }}" onChange="{{ osPick }}" aria-label="系统版本"><sc-for list="{{ osvs }}" as="v" hint-placeholder-count="4"><option value="{{ v.n }}">{{ v.n }}</option></sc-for></select></div>
      </div>
      <div class="sb-row"><div class="sb-lb">购买时长</div>
        <div class="sb-opts f7"><sc-for list="{{ months }}" as="o" hint-placeholder-count="7"><button type="button" class="sb-opt {{ o.cls }}" onClick="{{ o.go }}">{{ o.n }}</button></sc-for></div>
      </div>
      <div class="sb-row"><div class="sb-lb">购买数量</div>
        <div style="display:flex;align-items:center;gap:24px;flex-wrap:wrap"><div class="sb-step"><button type="button" onClick="{{ qDec }}" aria-label="减少">−</button><span>{{ q }}</span><button type="button" onClick="{{ qInc }}" aria-label="增加">+</button></div><span style="font-size:13px;color:#86909C">台，单次最多 20 台</span></div>
      </div>
      <div class="sb-row"><div class="sb-lb">特殊要求</div>
        <div><textarea class="sb-ta" placeholder="如需定制分区、额外 IP、指定上架时间等，请在此说明，工程师会在交付前与您确认"></textarea></div>
      </div>
    </div>
  </div>
  <aside class="sb-side">
    <div class="sb-sum">
      <h3>当前配置</h3>
      <dl class="sb-dl"><dt>类型</dt><dd>{{ sType }}</dd><dt>机房</dt><dd>{{ sReg }}</dd><dt>DDoS 防护</dt><dd>{{ sFh }}</dd><dt>CPU</dt><dd>{{ sCpu }}</dd><dt>内存/硬盘</dt><dd>{{ sMem }}</dd><dt>IP / 带宽</dt><dd>{{ sIp }} / {{ sBw }}</dd><dt>操作系统</dt><dd>{{ osV }}</dd><dt>时长 × 数量</dt><dd>{{ sM }} × {{ q }} 台</dd></dl>
      <div class="sb-tot">
        <div class="sb-calc">¥{{ sP }}/月 × {{ sMn }} 个月 × {{ q }} 台</div>
        <div class="sb-big"><small>¥</small><b>{{ total }}</b></div>
        <button type="button" class="sb-buy" onClick="{{ openDlg }}">立即购买</button>
        <div class="sb-sub"><a href="Contact.dc.html">咨询售前</a><span>热线 0577-26676666</span></div>
        <div class="sb-mini">购买即表示同意《SLA 服务等级协议》《信息安全协议》</div>
      </div>
    </div>
    <div class="sb-help"><b style="color:#1D2129">付款与交付</b><br>下单后通过对公转账付款，财务核验到账后安排交付，进度可在控制台「我的订单」查看。</div>
  </aside>
</div>
</section>
<section style="padding:0 0 72px">
  <div class="wrap">
    <h2 style="margin:0 0 20px;font-size:20px;font-weight:600">购买须知</h2>
    <div class="sb-faq">
      <div><b>防护承诺</b><p>标注「承诺打死按天退款」的机房，在防护峰值内被攻击打死，按天退还服务费。</p></div>
      <div><b>付款方式</b><p>目前支持对公转账。提交订单后在控制台付款页查看收款账户，到账核验后开通。</p></div>
      <div><b>赠送服务</b><p>每台服务器赠送自主化管理平台、德迅安全卫士、Web 云防护和 1V1 专家支撑。</p></div>
      <div><b>配置与升级</b><p>如需更高防护、更大带宽或其他机型，可在特殊要求中说明，或联系售前定制。</p></div>
    </div>
  </div>
</section>
<dc-import name="Footer" hint-size="100%,480px"></dc-import>
""" + "QNAV" + """
<sc-if value="{{ dlg1 }}" hint-placeholder-val="{{ false }}"><div class="sb-mask" onClick="{{ closeDlg }}"><div class="sb-dlg" role="dialog" aria-modal="true" aria-label="确认订单" onClick="{{ stop }}">
  <header>确认订单<button type="button" class="sb-x" onClick="{{ closeDlg }}" aria-label="关闭">×</button></header>
  <dl class="sb-dl"><dt>产品</dt><dd>{{ sType }} · {{ sReg }}</dd><dt>DDoS 防护</dt><dd>{{ sFh }}</dd><dt>配置</dt><dd>{{ sCpu }} · {{ sMem }}</dd><dt>IP / 带宽</dt><dd>{{ sIp }} / {{ sBw }}</dd><dt>操作系统</dt><dd>{{ osV }}</dd><dt>时长 × 数量</dt><dd>{{ sM }} × {{ q }} 台</dd><dt>应付金额</dt><dd><span class="sb-pr">¥{{ total }}</span></dd></dl>
  <div class="sb-pay">付款方式：对公转账。提交后在控制台付款页查看收款账户，财务核验到账后安排交付。未登录时会先进入登录页。</div>
  <div class="sb-ft"><button type="button" class="sb-ck {{ agCls }}" onClick="{{ agTog }}"><i></i>我已阅读并同意《SLA 服务等级协议》《信息安全协议》</button><button type="button" class="sb-buy" disabled="{{ noAg }}" onClick="{{ submit }}">提交订单</button></div>
</div></div></sc-if>
<sc-if value="{{ dlg2 }}" hint-placeholder-val="{{ false }}"><div class="sb-mask" onClick="{{ closeDlg }}"><div class="sb-dlg" role="dialog" aria-modal="true" aria-label="订单已提交" onClick="{{ stop }}">
  <div class="sb-ok"><i><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="#00B42A" stroke-width="2.4" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"></path></svg></i><h4>订单已提交</h4><p>订单号 DX20261109{{ ordNo }} · 应付 ¥{{ total }}<br>请在控制台完成对公转账，到账核验后安排交付。</p></div>
  <div class="sb-ft" style="justify-content:flex-end"><button type="button" class="btn btn-s btn-sm" onClick="{{ closeDlg }}">继续选购</button><a class="btn btn-p btn-sm" href="CONSOLE_PAY">前往控制台付款</a></div>
</div></div></sc-if>
</div>
"""

LOGIC = r"""
<script type="text/x-dc" data-dc-script data-props='{"$preview":{"width":1440,"height":2200}}'>
class Component extends DCLogic {
componentDidMount() {
  try { const m = /[?&]t=(\d)/.exec(window.location.search || ''); if (m) this.setState({ t: +m[1] }); } catch (e) {}
}
renderVals() {
const D = __DATA__;
const s = this.state || {};
const set = (o) => this.setState(o);
const t = s.t ?? 0, T = D.T[t] || D.T[0];
const rNames = T[3], ri = Math.min(s.r ?? 0, rNames.length - 1), rn = rNames[ri], R = D.R[rn];
const fi = Math.min(s.f ?? 0, R.fh.length - 1), F = R.fh[fi];
const ci = Math.min(s.c ?? 0, F[1].length - 1), Cf = F[1][ci];
const osF = s.osF ?? 0, OSF = D.OS[osF], osV = s.osV && OSF[1].indexOf(s.osV) > -1 ? s.osV : OSF[1][0];
const mi = s.m ?? 0, Mo = D.M[mi], q = s.q ?? 1, ar = !!s.ar, ag = !!s.ag;
const fmt = (n) => n.toLocaleString('en-US');
const total = Cf[4] * Mo[0] * q;
const o = {
  regs: rNames.map((n, i) => ({ n, tj: !!D.R[n].tj, tjc: D.R[n].tj ? 'has-tj' : '', cls: i === ri ? 'sb-on' : '', go: () => set({ r: i, f: 0, c: 0 }) })),
  regDesc: R.d,
  fhs: R.fh.map((x, i) => ({ n: x[0] + ' 防御', cls: i === fi ? 'sb-on' : '', go: () => set({ f: i, c: 0 }) })),
  cfgs: F[1].map((x, i) => ({ cpu: x[0], mem: x[1], ip: x[2], bw: x[3], p: fmt(x[4]), hot: !!x[5], cls: i === ci ? 'sb-tr-on' : '', go: () => set({ c: i }) })),
  osf: D.OS.map((x, i) => ({ n: x[0], cls: i === osF ? 'sb-on' : '', go: () => set({ osF: i, osV: null }) })),
  osvs: OSF[1].map((n) => ({ n })),
  osV, osPick: (e) => set({ osV: e.target.value }),
  months: D.M.map((x, i) => ({ n: x[1], cls: i === mi ? 'sb-on' : '', go: () => set({ m: i }) })),
  q, qDec: () => set({ q: Math.max(1, q - 1) }), qInc: () => set({ q: Math.min(20, q + 1) }),
  sType: T[0], sReg: rn, sFh: F[0] + ' 防御', sCpu: Cf[0], sMem: Cf[1], sIp: Cf[2], sBw: Cf[3],
  sP: fmt(Cf[4]), sM: Mo[1], sMn: Mo[0], total: fmt(total),
  dlg1: s.dlg === 1, dlg2: s.dlg === 2,
  openDlg: () => set({ dlg: 1 }), closeDlg: () => set({ dlg: 0 }), stop: (e) => e && e.stopPropagation && e.stopPropagation(),
  agCls: ag ? 'sb-ck-on' : '', agTog: () => set({ ag: !ag }), noAg: !ag,
  submit: () => { if (ag) set({ dlg: 2, ord: String(Math.floor(100000 + Math.random() * 899999)) }); },
  ordNo: s.ord || '000000',
};
D.T.forEach((x, i) => { o['tyC' + i] = i === t ? 'sb-on' : ''; o['tyP' + i] = () => set({ t: i, r: 0, f: 0, c: 0 }); });
return o;
}
}
</script>
"""

def types_static():
    return ''.join('<button type="button" class="sb-type {{ tyC%d }}" onClick="{{ tyP%d }}"><img src="img/%s.webp" alt="" aria-hidden="true"><div><b>%s</b><span>%s</span></div></button>' % (i, i, t[2], t[0], t[1]) for i, t in enumerate(T))

def build(base_css, qnav, console_pay):
    head = '<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n<title>服务器租用</title>\n<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n'
    body = BODY.replace("TYPES_STATIC", types_static()).replace("QNAV", qnav.strip()).replace("CONSOLE_PAY", console_pay)
    logic = LOGIC.replace("__DATA__", json.dumps(DATA, ensure_ascii=False))
    return head + base_css.rstrip() + "\n" + CSS + "</style>\n</helmet>\n" + body + "</x-dc>\n" + logic + "</body>\n</html>\n"

if __name__ == "__main__":
    base, qn, out = sys.argv[1:4]
    pay = sys.argv[4] if len(sys.argv) > 4 else "console/BillPayment.dc.html"
    open(out, "w").write(build(open(base).read(), open(qn).read(), pay))
    print("wrote", out)
