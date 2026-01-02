# 🍅 Pomodoro Timer

A clean, modern Pomodoro desktop app built with Python + Tkinter, designed for Windows 11.

![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%2011-0078D6.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## ✨ Features

- 🕐 **Custom Time**: Set countdown from 1-999 minutes
- ⚡ **Quick Buttons**: 15/20/25/30/45/60 minute presets
- ▶️ **Start/Pause**: One-click control
- 🔄 **Reset**: Reset anytime
- 🔊 **Built-in Sounds**: 5 notification sounds (Ding, Bell, Alarm, Chime, Double Beep)
- 🔔 **Interval Reminders**: Play "ding" every N minutes (default: 3 min)
- 🎵 **Custom Sound**: Use your own MP3/WAV/OGG/FLAC files
- 📊 **Progress Bar**: Visual countdown progress
- 💾 **Auto-save Settings**: Remembers your preferences
- 🎨 **Modern Dark UI**: Beautiful dark theme design

---

## 📁 Project Structure

```
Pomodoro Timer/
├── pomodoro_timer.py    # Main application
├── sounds.py            # Built-in sound generator module
├── sounds/              # Auto-generated sound files
│   ├── ding.wav         # Interval reminder sound
│   ├── bell.wav         # Bell sound
│   ├── alarm.wav        # Alarm sound
│   ├── chime.wav        # Chime sound
│   └── double_beep.wav  # Double beep sound
├── build.bat            # One-click build script
├── pomodoro.spec        # PyInstaller config file
├── requirements.txt     # Python dependencies
├── pomodoro_config.json # User settings (auto-generated)
├── README.md            # Chinese documentation
└── README_EN.md         # English documentation (this file)
```

### File Descriptions

| File                   | Purpose                                                   |
| ---------------------- | --------------------------------------------------------- |
| `pomodoro_timer.py`    | Main app: GUI, timer logic, audio playback                |
| `sounds.py`            | Pure Python WAV sound generator, no external files needed |
| `sounds/`              | Auto-generated folder with 5 built-in notification sounds |
| `build.bat`            | Windows batch script for one-click PyInstaller packaging  |
| `pomodoro.spec`        | PyInstaller specification file                            |
| `requirements.txt`     | Python dependency list                                    |
| `pomodoro_config.json` | JSON config storing user preferences                      |

---

## 🔧 Requirements

### Python Version

- **Python 3.8+** (recommended: Python 3.10+)
- Check version: `python --version`

### Operating System

- Windows 10 / Windows 11

### Dependencies

| Library     | Purpose                      | Required                     |
| ----------- | ---------------------------- | ---------------------------- |
| `tkinter`   | GUI framework                | ✅ Yes (bundled with Python) |
| `pygame`    | Audio playback (recommended) | ⭕ One of these              |
| `playsound` | Audio playback (lightweight) | ⭕ One of these              |

> **Note**: `tkinter` is included with Python on Windows by default.

---

## 🚀 Installation & Running

### Step 1: Install Python

Download from https://www.python.org/downloads/

- ✅ Check "Add Python to PATH" during installation

### Step 2: Install Audio Library

```bash
# Recommended
pip install pygame

# OR lightweight alternative
pip install playsound
```

### Step 3: Run the App

```bash
cd "f:\CodeResp\Pomodoro Timer"
python pomodoro_timer.py
```

Or simply double-click `pomodoro_timer.py`.

---

## 📖 How to Use

1. **Set Time**: Enter minutes or click a quick button (15/20/25/30/45/60)
2. **Set Sound**: Choose from built-in sounds or select a custom file
3. **Enable Interval Reminder**: Check the box and set reminder interval (default: 3 min)
4. **Start**: Click "▶ 开始" (Start) button
5. **Pause/Resume**: Click "⏸ 暂停" (Pause) / "▶ 继续" (Continue)
6. **Reset**: Click "⟲ 重置" (Reset)
7. **Timer Complete**: Sound plays and notification appears

---

## ⚙️ Configuration

The app saves settings to `pomodoro_config.json`:

```json
{
  "default_minutes": 25,
  "sound_path": "C:\\Users\\User\\Music\\alarm.mp3",
  "interval_minutes": 3,
  "interval_enabled": true,
  "selected_builtin_sound": 3
}
```

| Setting                  | Description                        |
| ------------------------ | ---------------------------------- |
| `default_minutes`        | Default countdown time in minutes  |
| `sound_path`             | Path to custom sound file          |
| `interval_minutes`       | Minutes between interval reminders |
| `interval_enabled`       | Enable/disable interval reminders  |
| `selected_builtin_sound` | Built-in sound index (1-5)         |

---

## 🔊 Audio Support

### Supported Formats

- MP3 (`.mp3`)
- WAV (`.wav`)
- OGG (`.ogg`)
- FLAC (`.flac`)

### Audio Library Comparison

| Library     | Pros                   | Cons                      |
| ----------- | ---------------------- | ------------------------- |
| `pygame`    | Powerful, many formats | Larger size (~10MB)       |
| `playsound` | Lightweight, simple    | Some compatibility issues |

> **Recommendation**: Use `pygame` for better stability.

### Fallback

If no audio library is installed or playback fails, the app uses Windows system sounds.

---

## 📦 Build Standalone EXE

### Method 1: One-Click Build (Recommended)

Double-click `build.bat` to automatically build the executable.

### Method 2: Manual Build

#### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

#### Step 2: Build

```bash
cd "f:\CodeResp\Pomodoro Timer"

# Using spec file
pyinstaller pomodoro.spec --clean

# OR using command line
pyinstaller --onefile --windowed --name "PomodoroTimer" --add-data "sounds.py;." pomodoro_timer.py
```

#### Step 3: Get the Result

```
dist\PomodoroTimer.exe
```

### Build Parameters

| Parameter    | Description                                      |
| ------------ | ------------------------------------------------ |
| `--onefile`  | Bundle into single EXE                           |
| `--windowed` | No console window (required for GUI)             |
| `--name`     | Output filename                                  |
| `--icon`     | App icon (optional, e.g., `--icon=pomodoro.ico`) |
| `--clean`    | Clean temp files before build                    |

### After Building

1. **First Run**: Auto-creates `sounds/` folder and config file in EXE directory
2. **Distribution**: Just copy the EXE file, no Python needed
3. **File Size**: ~30 MB (includes pygame)

---

## ❓ Troubleshooting

### Q: App fails to start with tkinter error

**Solution**: Reinstall Python and ensure "tcl/tk and IDLE" is selected.

### Q: Sound doesn't play

**Possible causes**:

1. No audio library installed
2. File path contains non-ASCII characters
3. Unsupported audio format

**Solution**:

1. Run `pip install pygame`
2. Move audio file to ASCII-only path
3. Use MP3 or WAV format

### Q: UI looks blurry (high DPI)

The app enables DPI awareness. If still blurry: Right-click Python → Properties → Compatibility → High DPI settings → Override.

### Q: EXE crashes on startup

**Solution**: Run from command line to see error:

```bash
cd dist
PomodoroTimer.exe
```

### Q: Antivirus flags the EXE

This is common with PyInstaller. **Solution**: Add to whitelist or use code signing.

---

## 📝 Technical Details

- **GUI Framework**: Tkinter (Python standard library)
- **Threading**: `threading` module for non-blocking timer
- **Config Storage**: JSON format
- **Audio Playback**: `pygame` / `playsound` backends
- **Sound Generation**: Pure Python WAV synthesis
- **System Integration**: Windows DPI awareness

---

## 📜 License

For personal learning and use only.

---

## 🎯 About Pomodoro Technique

The Pomodoro Technique is a time management method:

1. Choose a task to work on
2. Set timer for 25 minutes
3. Work until the timer rings
4. Take a 5-minute break
5. After 4 pomodoros, take a 15-30 minute break

Stay focused and work efficiently! 🍅
