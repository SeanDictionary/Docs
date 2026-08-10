# VS Code Remote-SSH 权限修复记录

## 1. 背景信息
- 日期：2026-03-06
- 本机系统：Windows（`win32 x64`）
- VS Code：`1.110.0`
- Remote-SSH 扩展：`0.122.0`
- 目标主机：`WebServer-192.168.30.128`（`linux`）

## 2. 现象与报错
连接 Remote-SSH 时失败，核心报错如下：

```text
Bad permissions. Try removing permissions for user: SEAN-LEGION\CodexSandboxUsers ... on file C:/Users/SeanL/.ssh/config.
Bad owner or permissions on C:\\Users\\SeanL/.ssh/config
Failed to parse remote port from server output
```

附带出现：

```text
过程试图写入的管道不存在。
```

该报错是前面 SSH 权限校验失败导致的连带现象，不是根因。

## 3. 根因分析
`OpenSSH` 在读取本地 SSH 配置文件时，对 ACL 要求严格。  
`C:\Users\SeanL\.ssh\config` 和 `C:\Users\SeanL\.ssh` 存在不被接受的继承权限（尤其 `SEAN-LEGION\CodexSandboxUsers`），导致 SSH 直接拒绝使用该配置文件，Remote-SSH 随后无法完成远端 server 启动握手。

## 4. 修复目标
- 移除 `~/.ssh/config` 与 `~/.ssh` 上不必要的继承/多余主体权限。
- 保留最小必要主体：
  - 当前用户 `SEAN-LEGION\SeanL`
  - `NT AUTHORITY\SYSTEM`
  - `BUILTIN\Administrators`

## 5. 执行过程摘要
- 第一轮尝试：`icacls` 在 PowerShell 下发生参数/转义问题，命令未生效。
- 第二轮尝试：改为提权执行并逐条命令应用 ACL，成功。

## 6. 最终执行的关键命令（思路）
按顺序执行了以下 ACL 操作：

```powershell
icacls.exe $cfg /inheritance:r
icacls.exe $cfg /remove:g 'SEAN-LEGION\CodexSandboxUsers' 'Users' 'Authenticated Users' 'Everyone'
icacls.exe $cfg /grant:r 'SEAN-LEGION\SeanL:F' 'SYSTEM:F' 'Administrators:F'

icacls.exe $dir /inheritance:r
icacls.exe $dir /remove:g 'SEAN-LEGION\CodexSandboxUsers' 'Users' 'Authenticated Users' 'Everyone'
icacls.exe $dir /grant:r 'SEAN-LEGION\SeanL:(OI)(CI)F' 'SYSTEM:(OI)(CI)F' 'Administrators:(OI)(CI)F'
```

其中：
- `$cfg = C:\Users\SeanL\.ssh\config`
- `$dir = C:\Users\SeanL\.ssh`

## 7. 修复前后 ACL 对比
### 7.1 修复前（关键问题）
- `C:\Users\SeanL\.ssh\config` 存在：
  - `SEAN-LEGION\CodexSandboxUsers:(I)(M,DC)`（不符合 OpenSSH 要求）
- `C:\Users\SeanL\.ssh` 也存在同类继承权限。

### 7.2 修复后（最终状态）
`C:\Users\SeanL\.ssh\config`：

```text
BUILTIN\Administrators:(F)
NT AUTHORITY\SYSTEM:(F)
SEAN-LEGION\SeanL:(F)
```

`C:\Users\SeanL\.ssh`：

```text
BUILTIN\Administrators:(OI)(CI)(F)
NT AUTHORITY\SYSTEM:(OI)(CI)(F)
SEAN-LEGION\SeanL:(OI)(CI)(F)
```

## 8. 当前结论
本次根因（`Bad owner or permissions on ~/.ssh/config`）已修复。  
建议重新在 VS Code 中连接 `WebServer-192.168.30.128` 进行验证。

若仍失败，请提供新一轮 Remote-SSH 日志，重点关注是否还有：
- `Bad owner or permissions ...`
- 密钥路径/认证失败
- 远端 shell 初始化脚本报错

## 9. 备注
会话中还发现当前环境 `where ssh` 优先命中 `SageMath` 自带 `ssh.exe`，而非系统 OpenSSH。  
VS Code 本次连接日志显示其实际调用的是 `C:\WINDOWS\System32\OpenSSH\ssh.exe`，因此本次权限问题修复方向正确。
