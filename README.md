# 🍅 番茄钟应用 (Pomodoro Timer)

一个简洁美观的个人番茄钟桌面应用，基于 Python + Tkinter 开发，专为 Windows 11 设计。

![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%2011-0078D6.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## ✨ 功能特性

- 🕐 **自定义时间**：支持自定义倒计时时间（分钟），范围 1-999 分钟
- ⚡ **快捷按钮**：提供 15/20/25/30/45/60 分钟快捷设置按钮
- ▶️ **开始/暂停**：一键开始或暂停计时
- 🔄 **重置功能**：随时重置计时器
- 🔊 **内置铃声**：提供 5 种内置提示音（叮声、钟声、闹钟、风铃、双响），无需额外下载
- 🔔 **间隔提醒**：每隔 N 分钟播放"叮"声提醒，帮助保持专注（默认每 3 分钟）
- 🎵 **自定义铃声**：支持选择本地音频文件作为结束提示铃声（MP3/WAV/OGG/FLAC）
- 📊 **进度条显示**：直观显示倒计时进度
- 💾 **配置保存**：自动保存用户设置（时间、铃声、间隔提醒）
- 🎨 **现代界面**：美观的深色主题界面设计

---

## 📁 项目结构

```
Pomodoro Timer/
├── pomodoro_timer.py    # 主程序文件
├── sounds.py            # 内置铃声生成模块
├── sounds/              # 内置铃声文件夹（运行后自动生成）
│   ├── ding.wav         # 叮声（间隔提醒用）
│   ├── bell.wav         # 钟声
│   ├── alarm.wav        # 闹钟声
│   ├── chime.wav        # 风铃声
│   └── double_beep.wav  # 双响声
├── build.bat            # 一键打包脚本
├── pomodoro.spec        # PyInstaller 配置文件
├── requirements.txt     # Python 依赖库列表
├── pomodoro_config.json # 用户配置文件（运行后自动生成）
├── README.md            # 中文说明文档（本文件）
└── README_EN.md         # 英文说明文档
```

### 文件说明

| 文件                   | 作用                                                |
| ---------------------- | --------------------------------------------------- |
| `pomodoro_timer.py`    | 主程序文件，包含完整的番茄钟应用代码                |
| `sounds.py`            | 内置铃声生成模块，使用纯 Python 生成 WAV 格式提示音 |
| `sounds/`              | 内置铃声文件夹，首次运行时自动生成                  |
| `build.bat`            | Windows 一键打包脚本                                |
| `pomodoro.spec`        | PyInstaller 打包配置文件                            |
| `requirements.txt`     | 依赖列表                                            |
| `pomodoro_config.json` | 用户配置文件                                        |

---

## 🔧 环境要求

### Python 版本

- **Python 3.8+**（推荐 Python 3.10 或更高版本）
- 可以在命令行输入 `python --version` 查看当前版本

### 操作系统

- **Windows 10 / Windows 11**

### 依赖库

| 库名        | 用途             | 是否必需               |
| ----------- | ---------------- | ---------------------- |
| `tkinter`   | GUI 图形界面     | ✅ 必需（Python 自带） |
| `pygame`    | 音频播放（推荐） | ⭕ 二选一              |
| `playsound` | 音频播放（轻量） | ⭕ 二选一              |

> **注意**：`tkinter` 是 Python 标准库的一部分，在 Windows 上默认已安装。

---

## 🚀 安装与运行

### 步骤 1：安装 Python

如果尚未安装 Python，请从官网下载安装：

- 官网地址：https://www.python.org/downloads/
- 安装时勾选 **"Add Python to PATH"** 选项

### 步骤 2：安装依赖库

打开命令提示符（CMD）或 PowerShell，运行以下命令：

```bash
# 安装 pygame（推荐）
pip install pygame

# 或者安装 playsound（更轻量）
pip install playsound
```

### 步骤 3：运行程序

```bash
cd "f:\CodeResp\Pomodoro Timer"
python pomodoro_timer.py
```

或者直接双击 `pomodoro_timer.py` 文件运行。

---

## 📖 使用说明

### 基本操作

1. **设置时间**：

   - 在输入框中输入倒计时分钟数
   - 或点击快捷按钮（15 分/20 分/25 分等）快速设置

2. **设置铃声**：

   - 从下拉菜单选择内置铃声
   - 或选择"自定义..."并浏览本地音频文件
   - 点击「▶ 试听」预听铃声

3. **间隔提醒**：

   - 勾选「🔔 启用间隔提醒」
   - 设置提醒间隔（默认 3 分钟）

4. **开始计时**：

   - 点击「▶ 开始」按钮开始倒计时
   - 计时过程中可点击「⏸ 暂停」暂停
   - 暂停后点击「▶ 继续」继续计时

5. **重置计时**：

   - 点击「⟲ 重置」按钮重置计时器

6. **计时完成**：
   - 倒计时结束后会自动播放提示铃声
   - 并弹出提示框通知用户

---

## ⚙️ 配置文件

程序会在同目录下生成 `pomodoro_config.json` 配置文件：

```json
{
  "default_minutes": 25,
  "sound_path": "C:\\Users\\用户名\\Music\\alarm.mp3",
  "interval_minutes": 3,
  "interval_enabled": true,
  "selected_builtin_sound": 3
}
```

| 配置项                   | 说明                     |
| ------------------------ | ------------------------ |
| `default_minutes`        | 默认倒计时分钟数         |
| `sound_path`             | 自定义铃声文件的完整路径 |
| `interval_minutes`       | 间隔提醒分钟数           |
| `interval_enabled`       | 是否启用间隔提醒         |
| `selected_builtin_sound` | 内置铃声序号（1-5）      |

---

## 🔊 音频支持

### 支持的音频格式

- MP3 (`.mp3`)
- WAV (`.wav`)
- OGG (`.ogg`)
- FLAC (`.flac`)

### 音频库选择

| 库          | 优点                 | 缺点                 |
| ----------- | -------------------- | -------------------- |
| `pygame`    | 功能强大，支持格式多 | 体积较大（约 10MB）  |
| `playsound` | 轻量简单             | 部分版本有兼容性问题 |

> **推荐**：使用 `pygame`，稳定性和兼容性更好。

### 备用方案

如果未安装任何音频库，或音频文件无法播放，程序会自动使用 Windows 系统提示音。

---

## 📦 打包成 EXE 文件

### 方法一：使用一键打包脚本（推荐）

双击运行项目目录下的 `build.bat` 文件即可自动完成打包。

### 方法二：手动打包

#### 步骤 1：安装 PyInstaller

```bash
pip install pyinstaller
```

#### 步骤 2：执行打包命令

```bash
cd "f:\CodeResp\Pomodoro Timer"

# 使用命令行参数打包
pyinstaller --onefile --windowed --name "PomodoroTimer" --add-data "sounds.py;." pomodoro_timer.py
```

#### 步骤 3：获取打包结果

打包完成后，可执行文件位于：

```
dist\PomodoroTimer.exe
```

### 打包参数说明

| 参数         | 说明                                           |
| ------------ | ---------------------------------------------- |
| `--onefile`  | 打包成单个 exe 文件                            |
| `--windowed` | 不显示控制台窗口（GUI 程序必须）               |
| `--name`     | 指定输出的 exe 文件名                          |
| `--icon`     | 指定程序图标（可选，如 `--icon=pomodoro.ico`） |
| `--clean`    | 清理临时文件后重新打包                         |

### 打包后的使用说明

1. **首次运行**：程序会自动在 exe 所在目录创建 `sounds/` 文件夹和配置文件
2. **分发给他人**：只需复制 `PomodoroTimer.exe` 即可，无需安装 Python
3. **文件大小**：打包后约 30 MB（包含 pygame 库）

---

## ❓ 常见问题

### Q1: 程序无法启动，提示找不到 tkinter

**解决方法**：重新安装 Python，确保勾选了 "tcl/tk and IDLE" 选项。

### Q2: 铃声无法播放

**可能原因**：

1. 未安装 `pygame` 或 `playsound`
2. 音频文件路径包含中文或特殊字符
3. 音频文件格式不支持

**解决方法**：

1. 运行 `pip install pygame` 安装音频库
2. 将音频文件移动到纯英文路径
3. 使用 MP3 或 WAV 格式的音频文件

### Q3: 界面模糊（高 DPI 屏幕）

程序已内置 DPI 感知设置。如仍模糊：右键 Python 程序 → 属性 → 兼容性 → 更改高 DPI 设置 → 勾选"替代高 DPI 缩放行为"。

### Q4: 打包后运行闪退

**解决方法**：使用命令行运行 exe 查看错误信息：

```bash
cd dist
PomodoroTimer.exe
```

### Q5: 杀毒软件误报

这是 PyInstaller 打包的常见问题。**解决方法**：

- 将 exe 添加到杀毒软件白名单
- 或使用代码签名证书签名 exe

---

## 📝 技术细节

- **GUI 框架**：Tkinter（Python 标准库）
- **多线程**：使用 `threading` 模块进行计时，避免阻塞 UI
- **配置存储**：JSON 格式本地存储
- **音频播放**：支持 `pygame` 和 `playsound` 两种后端
- **铃声生成**：纯 Python 合成 WAV 音频
- **系统集成**：支持 Windows DPI 感知

---

## 📜 许可证

本项目仅供个人学习和使用。

---

## 🎯 番茄工作法简介

番茄工作法是一种时间管理方法，核心是：

1. 选择一个待完成的任务
2. 设置 25 分钟的番茄钟
3. 专注工作直到番茄钟响铃
4. 短暂休息 5 分钟
5. 每完成 4 个番茄钟，休息 15-30 分钟

使用本应用，让你的工作更高效！🍅
