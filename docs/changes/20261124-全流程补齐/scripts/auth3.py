#!/usr/bin/env python3
"""登录 / 注册 / 找回密码：补报错状态 + 演示切换。幂等。用法 auth3.py <file>"""
import sys, re, json, os
p = sys.argv[1]
s = open(p, encoding='utf8').read()
if 'auth3:' in s:
    print('already', p); sys.exit(0)
name = os.path.basename(p).split('.')[0]
CFG = {
 'Login': [
   ('账号或密码错误', '账号或密码错误，还可以再试 4 次；连续错误 5 次将锁定 15 分钟', None),
   ('已锁定', '密码连续错误 5 次，账号已锁定，14:32 后可以再试；也可以改用短信验证码登录，或找回密码', None),
   ('验证码错误', '短信验证码错误或已过期（5 分钟内有效），请重新获取', None),
   ('账号已冻结', '账号已被冻结，暂时不能登录，请联系客服 0577-26676666', None),
   ('登录过期', '登录已过期，请重新登录；登录后会回到刚才的页面', None)],
 'Register': [
   ('手机号已注册', '该手机号已注册，可以直接登录；忘记密码请找回密码', None),
   ('验证码错误', '短信验证码错误或已过期（5 分钟内有效），请重新获取', None),
   ('发送太频繁', '验证码发送太频繁，请 60 秒后再试；同一手机号每天最多发送 10 次', None),
   ('密码太弱', '密码至少 8 位，需要同时包含字母和数字', None),
   ('未同意协议', '请先阅读并同意《用户服务协议》和《隐私政策》', None)],
 'Forgot': [
   ('手机号未注册', '该手机号还没有注册，可以直接注册', 0),
   ('验证码错误', '短信验证码错误或已过期（5 分钟内有效），请重新获取', 0),
   ('两次密码不一致', '两次输入的新密码不一致', 1),
   ('与旧密码相同', '新密码不能与最近 3 次使用过的密码相同', 1),
   ('密码太弱', '密码至少 8 位，需要同时包含字母和数字', 1)],
}[name]
n = 0
def rep(a, b):
    global s, n
    assert s.count(a) == 1, (a[:90], s.count(a)); s = s.replace(a, b); n += 1
ALERT = lambda on, msg: ('<sc-if value="{{ %s }}" hint-placeholder-val="{{ false }}"><div role="alert" style="display:flex;gap:8px;align-items:flex-start;padding:10px 12px;border-radius:2px;background:#FFECE8;color:#CB2634;font-size:13px;line-height:20px"><span aria-hidden="true" style="font-weight:600">!</span><span>{{ %s }}</span></div></sc-if>' % (on, msg))
DEMO = ('<div style="display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:12px;color:#86909C"><span>演示报错</span>'
        '<sc-for list="{{ erDemo }}" as="d" hint-placeholder-count="5"><button type="button" style="{{ d.st }}" onClick="{{ d.go }}">{{ d.n }}</button></sc-for></div>')
h2 = re.search(r'<h2 style="margin:0;font-size:28px;line-height:36px;font-weight:600">[^<]*</h2>', s).group(0)
rep(h2, h2 + '\n' + DEMO)
if name == 'Forgot':
    rep('<button class="btn btn-p" style="width:100%" onClick="{{ stP1 }}">下一步</button>', ALERT('erOn1', 'erMsg') + '<button class="btn btn-p" style="width:100%" onClick="{{ stP1 }}">下一步</button>')
    rep('<button class="btn btn-p" style="width:100%" onClick="{{ stP2 }}">确认修改</button>', ALERT('erOn2', 'erMsg') + '<button class="btn btn-p" style="width:100%" onClick="{{ stP2 }}">确认修改</button>')
else:
    btn = re.search(r'<a href="[^"]*"[^>]*class="btn btn-p" style="width:100%">(登录|注册)</a>', s).group(0)
    rep(btn, ALERT('erOn', 'erMsg') + btn)
js = ("/* auth3: 报错演示 */\n"
      "const ER = [['正常', '', null]].concat(" + json.dumps([list(x) for x in CFG], ensure_ascii=False) + ");\n"
      "const er = s.er || 0;\n"
      "const erBase = 'height:24px;padding:0 8px;font-size:12px;border-radius:2px;cursor:pointer;background:#fff;';\n"
      "o.erDemo = ER.map(([n, m, stp], i) => ({ n, st: erBase + (i === er ? 'border:1px solid #165DFF;color:#165DFF' : 'border:1px solid #E5E6EB;color:#4E5969'), go: () => this.setState(stp === null ? { er: i } : { er: i, st: stp }) }));\n"
      "o.erOn = er > 0; o.erMsg = ER[er][1]; o.erOn1 = er > 0 && ER[er][2] === 0; o.erOn2 = er > 0 && ER[er][2] === 1;\n")
i = s.rindex('\nreturn o;')
s = s[:i] + '\n' + js + s[i:]; n += 1
open(p, 'w', encoding='utf8').write(s)
print('ok', p, n)
