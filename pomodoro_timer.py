"""
番茄钟应用 (Pomodoro Timer)
=========================
一个简洁的个人番茄钟应用，支持自定义倒计时时间和提示铃声。

功能：
- 自定义倒计时时间（分钟）
- 开始/暂停/重置功能
- 倒计时结束后播放自定义铃声
- 每隔指定时间播放提示音
- 内置多种铃声可选
- 保存用户设置

作者：Antigravity AI
日期：2026-01-02
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import os
import sys
import json

# 导入内置铃声模块
from sounds import get_builtin_sounds, get_ding_sound, get_alarm_sound, get_sound_generator

# 尝试导入 pygame 用于音频播放
try:
    import pygame
    pygame.mixer.init()
    AUDIO_BACKEND = "pygame"
except ImportError:
    try:
        from playsound import playsound
        AUDIO_BACKEND = "playsound"
    except ImportError:
        AUDIO_BACKEND = None


def get_resource_path(relative_path):
    """获取资源文件的路径（支持 PyInstaller 打包）"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后的临时目录
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


def get_config_path():
    """获取配置文件路径（始终使用exe所在目录）"""
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后
        return os.path.join(os.path.dirname(sys.executable), "pomodoro_config.json")
    else:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "pomodoro_config.json")


class PomodoroTimer:
    """番茄钟主应用类"""
    
    # 默认设置
    DEFAULT_MINUTES = 25
    DEFAULT_SOUND_PATH = ""
    DEFAULT_INTERVAL_MINUTES = 3
    DEFAULT_INTERVAL_ENABLED = True
    
    def __init__(self, root):
        """初始化番茄钟应用"""
        self.root = root
        self.root.title("🍅 番茄钟 - Pomodoro Timer")
        self.root.geometry("480x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#2C3E50")
        
        # 计时器状态
        self.is_running = False
        self.is_paused = False
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.timer_thread = None
        self.stop_event = threading.Event()
        self.last_interval_time = 0
        
        # 生成内置铃声
        self.sound_generator = get_sound_generator()
        self.builtin_sounds = get_builtin_sounds()
        
        # 加载配置
        self.config = self.load_config()
        
        # 创建界面
        self.create_widgets()
        
        # 设置窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 让窗口居中显示
        self.center_window()
    
    def center_window(self):
        """将窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def load_config(self):
        """加载用户配置"""
        default_config = {
            "default_minutes": self.DEFAULT_MINUTES,
            "sound_path": self.DEFAULT_SOUND_PATH,
            "interval_minutes": self.DEFAULT_INTERVAL_MINUTES,
            "interval_enabled": self.DEFAULT_INTERVAL_ENABLED,
            "selected_builtin_sound": 3
        }
        
        try:
            config_path = get_config_path()
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
        
        return default_config
    
    def save_config(self):
        """保存用户配置"""
        try:
            config_path = get_config_path()
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def create_widgets(self):
        """创建界面组件"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # ========== 标题区域 ==========
        title_frame = tk.Frame(self.root, bg="#2C3E50")
        title_frame.pack(pady=15)
        
        title_label = tk.Label(
            title_frame,
            text="🍅 番茄钟",
            font=("微软雅黑", 28, "bold"),
            fg="#ECF0F1",
            bg="#2C3E50"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="专注工作，高效生活",
            font=("微软雅黑", 11),
            fg="#BDC3C7",
            bg="#2C3E50"
        )
        subtitle_label.pack()
        
        # ========== 时间显示区域 ==========
        timer_frame = tk.Frame(self.root, bg="#34495E", padx=40, pady=25)
        timer_frame.pack(pady=15, padx=30, fill="x")
        
        self.timer_label = tk.Label(
            timer_frame,
            text="25:00",
            font=("Consolas", 64, "bold"),
            fg="#E74C3C",
            bg="#34495E"
        )
        self.timer_label.pack()
        
        self.status_label = tk.Label(
            timer_frame,
            text="准备就绪",
            font=("微软雅黑", 13),
            fg="#95A5A6",
            bg="#34495E"
        )
        self.status_label.pack(pady=(5, 0))
        
        # 进度条
        self.progress = ttk.Progressbar(
            timer_frame,
            length=350,
            mode="determinate",
            maximum=100
        )
        self.progress.pack(pady=(10, 0))
        
        # ========== 时间设置区域 ==========
        settings_frame = tk.Frame(self.root, bg="#2C3E50")
        settings_frame.pack(pady=10, padx=30, fill="x")
        
        time_frame = tk.Frame(settings_frame, bg="#2C3E50")
        time_frame.pack(fill="x", pady=5)
        
        time_label = tk.Label(
            time_frame,
            text="⏱️ 设置时间（分钟）：",
            font=("微软雅黑", 11),
            fg="#ECF0F1",
            bg="#2C3E50"
        )
        time_label.pack(side="left")
        
        vcmd = (self.root.register(self.validate_time_input), '%P')
        
        self.time_entry = tk.Entry(
            time_frame,
            font=("Consolas", 14),
            width=6,
            justify="center",
            validate='key',
            validatecommand=vcmd
        )
        self.time_entry.pack(side="left", padx=10)
        self.time_entry.insert(0, str(self.config.get("default_minutes", 25)))
        
        # 快捷时间按钮
        quick_frame = tk.Frame(settings_frame, bg="#2C3E50")
        quick_frame.pack(fill="x", pady=8)
        
        quick_times = [15, 20, 25, 30, 45, 60]
        for minutes in quick_times:
            btn = tk.Button(
                quick_frame,
                text=f"{minutes}分",
                font=("微软雅黑", 9),
                width=5,
                bg="#3498DB",
                fg="white",
                relief="flat",
                cursor="hand2",
                command=lambda m=minutes: self.set_quick_time(m)
            )
            btn.pack(side="left", padx=3)
        
        # ========== 间隔提醒设置 ==========
        interval_frame = tk.Frame(self.root, bg="#2C3E50")
        interval_frame.pack(pady=8, padx=30, fill="x")
        
        self.interval_enabled_var = tk.BooleanVar(value=self.config.get("interval_enabled", True))
        
        interval_check = tk.Checkbutton(
            interval_frame,
            text="🔔 启用间隔提醒",
            font=("微软雅黑", 11),
            fg="#ECF0F1",
            bg="#2C3E50",
            selectcolor="#34495E",
            activebackground="#2C3E50",
            activeforeground="#ECF0F1",
            variable=self.interval_enabled_var,
            command=self.on_interval_toggle
        )
        interval_check.pack(side="left")
        
        interval_label = tk.Label(
            interval_frame,
            text="  每",
            font=("微软雅黑", 11),
            fg="#ECF0F1",
            bg="#2C3E50"
        )
        interval_label.pack(side="left")
        
        self.interval_entry = tk.Entry(
            interval_frame,
            font=("Consolas", 12),
            width=4,
            justify="center",
            validate='key',
            validatecommand=vcmd
        )
        self.interval_entry.pack(side="left", padx=5)
        self.interval_entry.insert(0, str(self.config.get("interval_minutes", 3)))
        
        interval_unit = tk.Label(
            interval_frame,
            text="分钟提醒一次",
            font=("微软雅黑", 11),
            fg="#ECF0F1",
            bg="#2C3E50"
        )
        interval_unit.pack(side="left")
        
        # ========== 铃声设置区域 ==========
        sound_section = tk.LabelFrame(
            self.root,
            text=" 🔊 铃声设置 ",
            font=("微软雅黑", 11, "bold"),
            fg="#ECF0F1",
            bg="#2C3E50",
            padx=10,
            pady=10
        )
        sound_section.pack(pady=10, padx=30, fill="x")
        
        builtin_frame = tk.Frame(sound_section, bg="#2C3E50")
        builtin_frame.pack(fill="x", pady=5)
        
        builtin_label = tk.Label(
            builtin_frame,
            text="结束铃声：",
            font=("微软雅黑", 10),
            fg="#BDC3C7",
            bg="#2C3E50"
        )
        builtin_label.pack(side="left")
        
        self.sound_choices = ["自定义..."] + [name for name, _ in self.builtin_sounds]
        self.selected_sound_var = tk.StringVar()
        
        selected_idx = self.config.get("selected_builtin_sound", 3)
        if self.config.get("sound_path") and selected_idx == 0:
            self.selected_sound_var.set("自定义...")
        else:
            if 0 < selected_idx <= len(self.builtin_sounds):
                self.selected_sound_var.set(self.builtin_sounds[selected_idx - 1][0])
            else:
                self.selected_sound_var.set(self.builtin_sounds[2][0] if len(self.builtin_sounds) > 2 else self.builtin_sounds[0][0])
        
        self.sound_dropdown = ttk.Combobox(
            builtin_frame,
            textvariable=self.selected_sound_var,
            values=self.sound_choices,
            state="readonly",
            width=20,
            font=("微软雅黑", 10)
        )
        self.sound_dropdown.pack(side="left", padx=10)
        self.sound_dropdown.bind("<<ComboboxSelected>>", self.on_sound_selected)
        
        preview_btn = tk.Button(
            builtin_frame,
            text="▶ 试听",
            font=("微软雅黑", 9),
            bg="#9B59B6",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.preview_sound
        )
        preview_btn.pack(side="left", padx=5)
        
        self.custom_sound_frame = tk.Frame(sound_section, bg="#2C3E50")
        self.custom_sound_frame.pack(fill="x", pady=5)
        
        self.sound_path_var = tk.StringVar(value=self.config.get("sound_path", ""))
        
        custom_label = tk.Label(
            self.custom_sound_frame,
            text="自定义文件：",
            font=("微软雅黑", 10),
            fg="#BDC3C7",
            bg="#2C3E50"
        )
        custom_label.pack(side="left")
        
        self.sound_entry = tk.Entry(
            self.custom_sound_frame,
            font=("微软雅黑", 9),
            textvariable=self.sound_path_var,
            width=22,
            state="readonly"
        )
        self.sound_entry.pack(side="left", padx=5)
        
        browse_btn = tk.Button(
            self.custom_sound_frame,
            text="浏览",
            font=("微软雅黑", 9),
            bg="#7F8C8D",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.browse_sound_file
        )
        browse_btn.pack(side="left", padx=5)
        
        if self.sound_path_var.get():
            sound_name = os.path.basename(self.sound_path_var.get())
            self.sound_entry.config(state="normal")
            self.sound_entry.delete(0, tk.END)
            self.sound_entry.insert(0, sound_name)
            self.sound_entry.config(state="readonly")
        
        if self.selected_sound_var.get() != "自定义...":
            self.custom_sound_frame.pack_forget()
        
        # ========== 控制按钮区域 ==========
        button_frame = tk.Frame(self.root, bg="#2C3E50")
        button_frame.pack(pady=20)
        
        self.start_btn = tk.Button(
            button_frame,
            text="▶ 开始",
            font=("微软雅黑", 14, "bold"),
            width=10,
            height=2,
            bg="#27AE60",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.start_timer
        )
        self.start_btn.pack(side="left", padx=10)
        
        self.reset_btn = tk.Button(
            button_frame,
            text="⟲ 重置",
            font=("微软雅黑", 14, "bold"),
            width=10,
            height=2,
            bg="#E74C3C",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.reset_timer
        )
        self.reset_btn.pack(side="left", padx=10)
        
        # ========== 音频后端状态 ==========
        if AUDIO_BACKEND:
            backend_text = f"音频引擎: {AUDIO_BACKEND}"
            backend_color = "#27AE60"
        else:
            backend_text = "⚠ 未安装音频库 (pygame/playsound)"
            backend_color = "#E74C3C"
        
        backend_label = tk.Label(
            self.root,
            text=backend_text,
            font=("微软雅黑", 9),
            fg=backend_color,
            bg="#2C3E50"
        )
        backend_label.pack(side="bottom", pady=10)
    
    def validate_time_input(self, new_value):
        """验证时间输入"""
        if new_value == "":
            return True
        try:
            value = int(new_value)
            return 0 <= value <= 999
        except ValueError:
            return False
    
    def set_quick_time(self, minutes):
        """设置快捷时间"""
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, str(minutes))
        self.update_timer_display(minutes * 60)
    
    def on_interval_toggle(self):
        """间隔提醒开关切换"""
        self.config["interval_enabled"] = self.interval_enabled_var.get()
        self.save_config()
    
    def on_sound_selected(self, event=None):
        """铃声选择变更"""
        selected = self.selected_sound_var.get()
        
        if selected == "自定义...":
            self.custom_sound_frame.pack(fill="x", pady=5)
            self.config["selected_builtin_sound"] = 0
        else:
            self.custom_sound_frame.pack_forget()
            for i, (name, _) in enumerate(self.builtin_sounds):
                if name == selected:
                    self.config["selected_builtin_sound"] = i + 1
                    break
        
        self.save_config()
    
    def get_current_end_sound_path(self):
        """获取当前结束铃声路径"""
        selected = self.selected_sound_var.get()
        
        if selected == "自定义...":
            return self.sound_path_var.get()
        else:
            for name, path in self.builtin_sounds:
                if name == selected:
                    return path
        
        return get_alarm_sound()
    
    def preview_sound(self):
        """试听当前选择的铃声"""
        sound_path = self.get_current_end_sound_path()
        
        if sound_path and os.path.exists(sound_path):
            threading.Thread(target=self._play_sound, args=(sound_path,), daemon=True).start()
        else:
            self.fallback_system_sound()
    
    def browse_sound_file(self):
        """浏览并选择铃声文件"""
        filetypes = [
            ("音频文件", "*.mp3 *.wav *.ogg *.flac"),
            ("MP3文件", "*.mp3"),
            ("WAV文件", "*.wav"),
            ("所有文件", "*.*")
        ]
        
        filepath = filedialog.askopenfilename(
            title="选择提示铃声",
            filetypes=filetypes,
            initialdir=os.path.expanduser("~\\Music")
        )
        
        if filepath:
            self.sound_path_var.set(filepath)
            self.config["sound_path"] = filepath
            self.save_config()
            
            sound_name = os.path.basename(filepath)
            self.sound_entry.config(state="normal")
            self.sound_entry.delete(0, tk.END)
            self.sound_entry.insert(0, sound_name)
            self.sound_entry.config(state="readonly")
    
    def update_timer_display(self, seconds):
        """更新计时器显示"""
        minutes = seconds // 60
        secs = seconds % 60
        self.timer_label.config(text=f"{minutes:02d}:{secs:02d}")
        
        if self.total_seconds > 0:
            progress = ((self.total_seconds - seconds) / self.total_seconds) * 100
            self.progress["value"] = progress
    
    def start_timer(self):
        """开始或暂停计时器"""
        if not self.is_running:
            try:
                minutes = int(self.time_entry.get())
                if minutes <= 0:
                    messagebox.showwarning("输入错误", "请输入大于0的分钟数！")
                    return
                
                self.config["default_minutes"] = minutes
                try:
                    interval = int(self.interval_entry.get())
                    self.config["interval_minutes"] = interval
                except ValueError:
                    pass
                self.save_config()
                
                self.remaining_seconds = minutes * 60
                self.total_seconds = minutes * 60
                self.last_interval_time = self.total_seconds
                self.is_running = True
                self.is_paused = False
                self.stop_event.clear()
                
                self.start_btn.config(text="⏸ 暂停", bg="#F39C12")
                self.status_label.config(text="计时中...", fg="#E74C3C")
                self.time_entry.config(state="disabled")
                self.interval_entry.config(state="disabled")
                
                self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
                self.timer_thread.start()
                
            except ValueError:
                messagebox.showwarning("输入错误", "请输入有效的分钟数！")
        
        elif self.is_paused:
            self.is_paused = False
            self.start_btn.config(text="⏸ 暂停", bg="#F39C12")
            self.status_label.config(text="计时中...", fg="#E74C3C")
        
        else:
            self.is_paused = True
            self.start_btn.config(text="▶ 继续", bg="#27AE60")
            self.status_label.config(text="已暂停", fg="#F39C12")
    
    def run_timer(self):
        """计时器线程函数"""
        while self.remaining_seconds > 0 and not self.stop_event.is_set():
            if not self.is_paused:
                time.sleep(1)
                if self.stop_event.is_set():
                    break
                if not self.is_paused:
                    self.remaining_seconds -= 1
                    self.root.after(0, self.update_timer_display, self.remaining_seconds)
                    
                    if self.interval_enabled_var.get():
                        self.check_interval_reminder()
            else:
                time.sleep(0.1)
        
        if self.remaining_seconds <= 0 and not self.stop_event.is_set():
            self.root.after(0, self.timer_complete)
    
    def check_interval_reminder(self):
        """检查并播放间隔提醒"""
        try:
            interval_minutes = int(self.interval_entry.get())
            if interval_minutes <= 0:
                return
            
            interval_seconds = interval_minutes * 60
            elapsed_since_last = self.last_interval_time - self.remaining_seconds
            
            if elapsed_since_last >= interval_seconds and self.remaining_seconds > 0:
                ding_path = get_ding_sound()
                threading.Thread(target=self._play_sound, args=(ding_path,), daemon=True).start()
                self.last_interval_time = self.remaining_seconds
                
                elapsed_total = self.total_seconds - self.remaining_seconds
                elapsed_min = elapsed_total // 60
                self.root.after(0, lambda: self.status_label.config(
                    text=f"已专注 {elapsed_min} 分钟 🔔", 
                    fg="#3498DB"
                ))
                self.root.after(1500, lambda: self.status_label.config(
                    text="计时中...", 
                    fg="#E74C3C"
                ) if self.is_running and not self.is_paused else None)
                
        except ValueError:
            pass
    
    def timer_complete(self):
        """计时完成处理"""
        self.is_running = False
        self.is_paused = False
        
        self.start_btn.config(text="▶ 开始", bg="#27AE60")
        self.status_label.config(text="🎉 时间到！", fg="#27AE60")
        self.time_entry.config(state="normal")
        self.interval_entry.config(state="normal")
        self.progress["value"] = 100
        
        self.play_notification_sound()
        messagebox.showinfo("番茄钟", "🍅 时间到！\n\n休息一下吧！")
    
    def _play_sound(self, sound_path):
        """播放音频文件"""
        if not sound_path or not os.path.exists(sound_path):
            return
        
        if AUDIO_BACKEND == "pygame":
            try:
                sound = pygame.mixer.Sound(sound_path)
                sound.play()
            except Exception as e:
                print(f"pygame播放失败: {e}")
        
        elif AUDIO_BACKEND == "playsound":
            try:
                playsound(sound_path)
            except Exception as e:
                print(f"playsound播放失败: {e}")
    
    def play_notification_sound(self):
        """播放结束提示铃声"""
        sound_path = self.get_current_end_sound_path()
        
        if sound_path and os.path.exists(sound_path):
            threading.Thread(target=self._play_sound, args=(sound_path,), daemon=True).start()
        else:
            self.fallback_system_sound()
    
    def fallback_system_sound(self):
        """使用Windows系统提示音"""
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except Exception as e:
            print(f"系统提示音播放失败: {e}")
    
    def reset_timer(self):
        """重置计时器"""
        self.stop_event.set()
        self.is_running = False
        self.is_paused = False
        
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=1)
        
        try:
            minutes = int(self.time_entry.get()) if self.time_entry.get() else self.config.get("default_minutes", 25)
        except ValueError:
            minutes = self.config.get("default_minutes", 25)
        
        self.remaining_seconds = minutes * 60
        self.total_seconds = minutes * 60
        self.update_timer_display(self.remaining_seconds)
        
        self.start_btn.config(text="▶ 开始", bg="#27AE60")
        self.status_label.config(text="准备就绪", fg="#95A5A6")
        self.time_entry.config(state="normal")
        self.interval_entry.config(state="normal")
        self.progress["value"] = 0
    
    def on_closing(self):
        """窗口关闭处理"""
        self.stop_event.set()
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=1)
        
        try:
            minutes = int(self.time_entry.get())
            self.config["default_minutes"] = minutes
        except ValueError:
            pass
        
        try:
            interval = int(self.interval_entry.get())
            self.config["interval_minutes"] = interval
        except ValueError:
            pass
        
        self.config["interval_enabled"] = self.interval_enabled_var.get()
        self.save_config()
        
        self.root.destroy()


def main():
    """主函数"""
    root = tk.Tk()
    
    # 设置DPI感知
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    
    app = PomodoroTimer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
