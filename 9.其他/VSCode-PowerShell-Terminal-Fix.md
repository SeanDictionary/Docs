# VSCode PowerShell 终端乱码问题完整解决方案

## 📋 目录
- [本地配置](#本地配置)
- [问题现象](#问题现象)
- [问题分析](#问题分析)
- [根本原因](#根本原因)
- [解决方案](#解决方案)
- [技术细节](#技术细节)

---
## 本地配置

- 操作系统：Windows 10 Pro 22H2 (19045.6093)
- VSCode 版本：1.106.3
- PowerShell 版本：7.5.2

---

## 问题现象

### 具体表现
在 VSCode 中使用集成终端使用 F5 运行 Python 调试或执行长命令时，终端会显示一串乱码文本，例如：

```powershell
PS C:\Users\SeanL\Desktop> c:; cd 'c:\Users\SeanL\Desktop'; & 'd:\Miniconda3\envs\test\python.exe' 'c:\Users\SeanL\.vscode\extensions\ms-python.debugpy-2025.16.0-win32-x64\bundled\libs\debugpy\launcher' '3729' '--' 'C:\Users\SeanL\Desktop\a.py'

launcher' '3729' '--' 'C:\x5cUsers\x5cSeanL\x5cDesktop\x5ca.py'
Traceback (most recent call last):
  ...
```

注意第二行的乱码输出：`launcher' '3729' '--' 'C:\x5cUsers\x5cSeanL\x5cDesktop\x5ca.py'` 该行乱码不会影响脚本的输出，脚本输出是覆盖在乱码上的，但是影响阅读和调试。

此外并非每次运行相同的文件能成功复现。

### 特征识别
- ✅ 乱码内容是命令行的一部分（命令尾部）
- ✅ 反斜杠 `\` 被转义为 `\x5c`
- ✅ 只在 VSCode 集成终端中出现
- ✅ 只在执行较长命令时出现
- ✅ 使用 `-NoProfile` 启动 PowerShell 时不会出现
- ✅ 但使用 `-NoProfile` 会导致 Conda 环境和其他功能失效

---

## 问题分析

### 触发条件
1. **环境要求：**
   - 使用 VSCode 集成终端
   - PowerShell 作为默认 shell
   - 启用了 Shell Integration（VSCode 默认启用）
   - 加载了 PowerShell Profile

2. **命令特征：**
   - 命令长度较长（通常 > 100 字符）
   - 包含路径参数（如 Python 调试器路径）
   - 命令中包含特殊字符（如反斜杠、引号）

### 为什么只在 VSCode 中出现？
VSCode 的 Shell Integration 功能会自动注入一个脚本 `shellIntegration.ps1`，用于增强终端体验（命令追踪、输出捕获、智能导航等）。这个脚本通过 OSC（Operating System Command）转义序列与 VSCode 通信。

其他终端（Windows Terminal、ConEmu 等）不会注入这个脚本，因此不会出现此问题。

---

## 根本原因

### 技术原理

**OSC 633 控制序列**
VSCode Shell Integration 使用 OSC 633 系列序列来追踪命令执行：

- **OSC 633;A** - 提示符开始
- **OSC 633;B** - 提示符结束 / 命令输入开始
- **OSC 633;C** - 命令执行开始
- **OSC 633;D** - 命令执行结束（带退出码）
- **OSC 633;E** - 命令行内容（用于历史追踪）⚠️ **问题根源**

### 问题详解

在 `shellIntegration.ps1` 的 `PSConsoleHostReadLine` 函数中（第 195-222 行），有如下代码：

```powershell
function Global:PSConsoleHostReadLine {
    $CommandLine = $Global:__VSCodeState.OriginalPSConsoleHostReadLine.Invoke()
    $Global:__VSCodeState.IsInExecution = $true

    # 构造 OSC 633;E 序列
    $Result = "$([char]0x1b)]633;E;"
    $Result += $(__VSCode-Escape-Value $CommandLine)  # ⚠️ 转义命令行
    # ...
    $Result += "`a"

    # 发送到终端
    [Console]::Write($Result)
    
    $CommandLine  # 返回原始命令供 PowerShell 执行
}
```

**问题链条：**

1. **命令拦截：** `PSConsoleHostReadLine` 拦截用户输入的命令
2. **内容转义：** `__VSCode-Escape-Value` 将命令中的特殊字符转义
   - 反斜杠 `\` → `\x5c`
   - 换行符 `\n` → `\x0a`
   - 分号 `;` → `\x3b`
3. **序列发送：** 转义后的命令通过 OSC 633;E 序列发送
4. **渲染 Bug：** VSCode 终端在处理长命令时，渲染引擎存在竞态条件
5. **乱码显示：** 本应隐藏的转义后的命令字符串被错误地显示到屏幕

### 为什么 `-NoProfile` 有效？

使用 `-NoProfile` 后：
- PowerShell Profile 不会被加载
- VSCode 的 Shell Integration 脚本也不会被自动注入
- 没有 OSC 633 序列发送
- 因此不会出现乱码

**但代价是：**
- ❌ Conda 环境激活失败
- ❌ 失去自定义的 PowerShell 配置
- ❌ 失去 VSCode Shell Integration 的所有功能

---

## 解决方案

### 方案概述
直接修改 VSCode 的 Shell Integration 脚本，禁用导致问题的 OSC 633;E 序列发送。

### 详细步骤

#### 1. 定位文件
Shell Integration 脚本路径：
```
C:\Users\<YourUsername>\AppData\Local\Programs\Microsoft VS Code\resources\app\out\vs\workbench\contrib\terminal\common\scripts\shellIntegration.ps1
```

快速获取路径的方法：
```powershell
code --locate-shell-integration-path pwsh
```

#### 2. 备份原文件（重要！）
```powershell
Copy-Item "C:\Users\SeanL\AppData\Local\Programs\Microsoft VS Code\resources\app\out\vs\workbench\contrib\terminal\common\scripts\shellIntegration.ps1" "C:\Users\SeanL\Desktop\shellIntegration.ps1.backup"
```

#### 3. 修改文件

使用管理员权限打开 VSCode：
```powershell
# 右键以管理员身份运行 VSCode，然后打开文件
code "C:\Users\SeanL\AppData\Local\Programs\Microsoft VS Code\resources\app\out\vs\workbench\contrib\terminal\common\scripts\shellIntegration.ps1"
```

找到 `PSConsoleHostReadLine` 函数（约第 197 行），将以下代码：

**修改前：**
```powershell
function Global:PSConsoleHostReadLine {
    $CommandLine = $Global:__VSCodeState.OriginalPSConsoleHostReadLine.Invoke()
    $Global:__VSCodeState.IsInExecution = $true

    # Command line
    # OSC 633 ; E [; <CommandLine> [; <Nonce>]] ST
    $Result = "$([char]0x1b)]633;E;"
    $Result += $(__VSCode-Escape-Value $CommandLine)
    # Only send the nonce if the OS is not Windows 10 as it seems to echo to the terminal
    # sometimes
    if ($Global:__VSCodeState.IsWindows10 -eq $false) {
        $Result += ";$($Global:__VSCodeState.Nonce)"
    }
    $Result += "`a"

    # Command executed
    # OSC 633 ; C ST
    $Result += "$([char]0x1b)]633;C`a"

    # Write command executed sequence directly to Console to avoid the new line from Write-Host
    [Console]::Write($Result)

    $CommandLine
}
```

**修改后：**
```powershell
function Global:PSConsoleHostReadLine {
    $CommandLine = $Global:__VSCodeState.OriginalPSConsoleHostReadLine.Invoke()
    $Global:__VSCodeState.IsInExecution = $true

    # Command line - DISABLED to prevent display issues with long commands
    # The OSC 633;E sequence was causing escaped command text to appear in terminal
    # OSC 633 ; E [; <CommandLine> [; <Nonce>]] ST
    # $Result = "$([char]0x1b)]633;E;"
    # $Result += $(__VSCode-Escape-Value $CommandLine)
    # if ($Global:__VSCodeState.IsWindows10 -eq $false) {
    #     $Result += ";$($Global:__VSCodeState.Nonce)"
    # }
    # $Result += "`a"

    # Command executed
    # OSC 633 ; C ST
    $Result = "$([char]0x1b)]633;C`a"

    # Write command executed sequence directly to Console to avoid the new line from Write-Host
    [Console]::Write($Result)

    $CommandLine
}
```

#### 4. 保存并重启
- 保存文件（Ctrl+S）
- 完全关闭 VSCode（不是窗口，是整个应用）
- 重新启动 VSCode
- 测试运行 Python 调试命令

### 验证修复
运行之前出现乱码的命令，不再显示转义后的字符串。


