# Pomodoro Timer

A clean, modern Pomodoro desktop app built with Python + Tkinter, designed for Windows 11.

![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%2011-0078D6.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## Features

- Custom countdown time (1-999 minutes)
- Quick buttons for 15/20/25/30/45/60 minutes
- Start/pause and reset
- Built-in notification sounds (ding, bell, alarm, chime, double beep)
- Interval reminders with a configurable interval (default 3 minutes)
- Custom end sound (MP3/WAV/OGG/FLAC)
- Progress bar display
- Auto-save user settings (time, sounds, interval reminders)
- Modern dark UI

---

## Project Structure

```
Pomodoro Timer/
├── pomodoro_timer.py    # Main app
├── sounds.py            # Built-in sound generator
├── sounds/              # Generated built-in sounds
│   ├── ding.wav         # Interval reminder sound
│   ├── bell.wav         # Bell
│   ├── alarm.wav        # Alarm
│   ├── chime.wav        # Chime
│   └── double_beep.wav  # Double beep
├── requirements.txt     # Python dependencies
├── pomodoro_config.json # User config (auto-generated)
└── README.md            # Chinese README
```

### Files

| File | Purpose |
| --- | --- |
| `pomodoro_timer.py` | Main app: UI, timer logic, audio playback |
| `sounds.py` | Built-in sound generator (pure Python WAV) |
| `sounds/` | Auto-generated built-in sounds |
| `requirements.txt` | Dependency list |
| `pomodoro_config.json` | Stores defaults and reminder settings |

---

## Requirements

- Python 3.8+ (recommended 3.10+)
- Windows 10 / Windows 11

### Audio Libraries

| Library | Usage | Required |
| --- | --- | --- |
| `tkinter` | GUI | Yes (bundled with Python) |
| `pygame` | Audio playback (recommended) | Optional |
| `playsound` | Audio playback (lightweight) | Optional |

Note: `tkinter` ships with Python on Windows.

---

## Install and Run

1) Install Python from https://www.python.org/downloads/ (check "Add Python to PATH").

2) Install one audio library:

```bash
pip install pygame
# or
pip install playsound
```

3) Run:

```bash
python pomodoro_timer.py
```

---

## Usage

1) Set time in minutes or click a quick button.
2) Choose end sound (built-in or custom file).
3) Start/pause with the main button.
4) Reset any time.
5) When the timer finishes, a notification sound plays and a message box appears.

---

## Configuration

The app writes `pomodoro_config.json` in the project directory:

```json
{
  "default_minutes": 25,
  "sound_path": "C:\\Users\\User\\Music\\alarm.mp3",
  "interval_minutes": 3,
  "interval_enabled": true,
  "selected_builtin_sound": 2
}
```

| Key | Description |
| --- | --- |
| `default_minutes` | Default countdown time |
| `sound_path` | Custom sound file path |
| `interval_minutes` | Interval reminder minutes |
| `interval_enabled` | Enable interval reminders |
| `selected_builtin_sound` | Built-in sound index (1-5) |

---

## Audio Support

Supported formats: MP3, WAV, OGG, FLAC.

If no audio library is installed or the file cannot be played, the app falls back to the Windows system sound.

---

## FAQ

Q: The app fails to start with a tkinter error.
A: Reinstall Python and ensure "tcl/tk and IDLE" is selected.

Q: The sound does not play.
A: Install `pygame` or `playsound`, move the audio file to a path with ASCII characters only, and try MP3/WAV.

Q: The UI looks blurry on high-DPI screens.
A: The app enables DPI awareness. If it is still blurry, set High DPI override in the Python executable properties.

---

## Technical Notes

- UI: Tkinter
- Timer thread: `threading`
- Config: JSON
- Audio: `pygame` or `playsound`
- Windows DPI awareness enabled

---

## License

For personal learning and use.

---

## Pomodoro Technique

1. Choose a task
2. Work for 25 minutes
3. Take a 5-minute break
4. After 4 sessions, take a 15-30 minute break

Stay focused and work efficiently.
