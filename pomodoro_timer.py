"""
番茄钟应用 (Pomodoro Timer)
=========================
一个简洁的个人番茄钟应用，支持自定义倒计时时间和提示铃声。

功能：
- 自定义倒计时时间（分钟）
- 开始/暂停/重置功能
- 倒计时结束后播放自定义铃声
- 保存用户设置（铃声路径）

作者：Antigravity AI
日期：2026-01-02
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import os
import json

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


class PomodoroTimer:
    """番茄钟主应用类"""
    
    # 配置文件路径
    CONFIG_FILE = "pomodoro_config.json"
    
    # 默认设置
    DEFAULT_MINUTES = 25
    DEFAULT_SOUND_PATH = ""
    
    def __init__(self, root):
        """初始化番茄钟应用"""
        self.root = root
        self.root.title("🍅 番茄钟 - Pomodoro Timer")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#2C3E50")
        
        # 计时器状态
        self.is_running = False
        self.is_paused = False
        self.remaining_seconds = 0
        self.timer_thread = None
        self.stop_event = threading.Event()
        
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
            "sound_path": self.DEFAULT_SOUND_PATH
        }
        
        try:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.CONFIG_FILE)
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # 合并默认配置和加载的配置
                    default_config.update(loaded_config)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
        
        return default_config
    
    def save_config(self):
        """保存用户配置"""
        try:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.CONFIG_FILE)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def create_widgets(self):
        """创建界面组件"""
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置按钮样式
        style.configure('Start.TButton', 
                       font=('微软雅黑', 12, 'bold'),
                       padding=10)
        style.configure('Stop.TButton', 
                       font=('微软雅黑', 12, 'bold'),
                       padding=10)
        style.configure('Reset.TButton', 
                       font=('微软雅黑', 12, 'bold'),
                       padding=10)
        
        # ========== 标题区域 ==========
        title_frame = tk.Frame(self.root, bg="#2C3E50")
        title_frame.pack(pady=20)
        
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
            font=("微软雅黑", 12),
            fg="#BDC3C7",
            bg="#2C3E50"
        )
        subtitle_label.pack()
        
        # ========== 时间显示区域 ==========
        timer_frame = tk.Frame(self.root, bg="#34495E", padx=40, pady=30)
        timer_frame.pack(pady=20, padx=30, fill="x")
        
        self.timer_label = tk.Label(
            timer_frame,
            text="25:00",
            font=("Consolas", 72, "bold"),
            fg="#E74C3C",
            bg="#34495E"
        )
        self.timer_label.pack()
        
        self.status_label = tk.Label(
            timer_frame,
            text="准备就绪",
            font=("微软雅黑", 14),
            fg="#95A5A6",
            bg="#34495E"
        )
        self.status_label.pack(pady=(10, 0))
        
        # ========== 时间设置区域 ==========
        settings_frame = tk.Frame(self.root, bg="#2C3E50")
        settings_frame.pack(pady=15, padx=30, fill="x")
        
        # 时间输入
        time_frame = tk.Frame(settings_frame, bg="#2C3E50")
        time_frame.pack(fill="x", pady=5)
        
        time_label = tk.Label(
            time_frame,
            text="⏱️ 设置时间（分钟）：",
            font=("微软雅黑", 12),
            fg="#ECF0F1",
            bg="#2C3E50"
        )
        time_label.pack(side="left")
        
        # 时间输入验证
        vcmd = (self.root.register(self.validate_time_input), '%P')
        
        self.time_entry = tk.Entry(
            time_frame,
            font=("Consolas", 14),
            width=8,
            justify="center",
            validate='key',
            validatecommand=vcmd
        )
        self.time_entry.pack(side="left", padx=10)
        self.time_entry.insert(0, str(self.config.get("default_minutes", 25)))
        
        # 快捷时间按钮
        quick_frame = tk.Frame(settings_frame, bg="#2C3E50")
        quick_frame.pack(fill="x", pady=10)
        
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
        
        # ========== 铃声设置区域 ==========
        sound_frame = tk.Frame(self.root, bg="#2C3E50")
        sound_frame.pack(pady=10, padx=30, fill="x")
        
        sound_label = tk.Label(
            sound_frame,
            text="🔔 提示铃声：",
            font=("微软雅黑", 12),
            fg="#ECF0F1",
            bg="#2C3E50"
        )
        sound_label.pack(side="left")
        
        self.sound_path_var = tk.StringVar(value=self.config.get("sound_path", ""))
        
        self.sound_entry = tk.Entry(
            sound_frame,
            font=("微软雅黑", 10),
            textvariable=self.sound_path_var,
            width=25,
            state="readonly"
        )
        self.sound_entry.pack(side="left", padx=5)
        
        browse_btn = tk.Button(
            sound_frame,
            text="选择",
            font=("微软雅黑", 10),
            bg="#9B59B6",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.browse_sound_file
        )
        browse_btn.pack(side="left", padx=5)
        
        # 显示铃声状态
        if self.sound_path_var.get():
            sound_name = os.path.basename(self.sound_path_var.get())
            self.sound_entry.config(state="normal")
            self.sound_entry.delete(0, tk.END)
            self.sound_entry.insert(0, sound_name)
            self.sound_entry.config(state="readonly")
        
        # ========== 控制按钮区域 ==========
        button_frame = tk.Frame(self.root, bg="#2C3E50")
        button_frame.pack(pady=25)
        
        # 开始/暂停按钮
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
        
        # 停止/重置按钮
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
        """验证时间输入，只允许数字"""
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
            
            # 更新显示
            sound_name = os.path.basename(filepath)
            self.sound_entry.config(state="normal")
            self.sound_entry.delete(0, tk.END)
            self.sound_entry.insert(0, sound_name)
            self.sound_entry.config(state="readonly")
            
            messagebox.showinfo("铃声设置", f"已选择铃声：\n{sound_name}")
    
    def update_timer_display(self, seconds):
        """更新计时器显示"""
        minutes = seconds // 60
        secs = seconds % 60
        self.timer_label.config(text=f"{minutes:02d}:{secs:02d}")
    
    def start_timer(self):
        """开始或暂停计时器"""
        if not self.is_running:
            # 开始计时
            try:
                minutes = int(self.time_entry.get())
                if minutes <= 0:
                    messagebox.showwarning("输入错误", "请输入大于0的分钟数！")
                    return
                
                # 保存默认时间设置
                self.config["default_minutes"] = minutes
                self.save_config()
                
                self.remaining_seconds = minutes * 60
                self.is_running = True
                self.is_paused = False
                self.stop_event.clear()
                
                # 更新按钮状态
                self.start_btn.config(text="⏸ 暂停", bg="#F39C12")
                self.status_label.config(text="计时中...", fg="#E74C3C")
                self.time_entry.config(state="disabled")
                
                # 启动计时线程
                self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
                self.timer_thread.start()
                
            except ValueError:
                messagebox.showwarning("输入错误", "请输入有效的分钟数！")
        
        elif self.is_paused:
            # 继续计时
            self.is_paused = False
            self.start_btn.config(text="⏸ 暂停", bg="#F39C12")
            self.status_label.config(text="计时中...", fg="#E74C3C")
        
        else:
            # 暂停计时
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
                    # 在主线程中更新UI
                    self.root.after(0, self.update_timer_display, self.remaining_seconds)
            else:
                time.sleep(0.1)
        
        if self.remaining_seconds <= 0 and not self.stop_event.is_set():
            # 计时结束
            self.root.after(0, self.timer_complete)
    
    def timer_complete(self):
        """计时完成处理"""
        self.is_running = False
        self.is_paused = False
        
        # 更新UI
        self.start_btn.config(text="▶ 开始", bg="#27AE60")
        self.status_label.config(text="🎉 时间到！", fg="#27AE60")
        self.time_entry.config(state="normal")
        
        # 播放提示音
        self.play_notification_sound()
        
        # 显示提示框
        messagebox.showinfo("番茄钟", "🍅 时间到！\n\n休息一下吧！")
    
    def play_notification_sound(self):
        """播放提示铃声"""
        sound_path = self.sound_path_var.get()
        
        if not sound_path or not os.path.exists(sound_path):
            # 如果没有设置铃声或文件不存在，使用系统提示音
            try:
                import winsound
                # 播放系统默认提示音
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            except Exception as e:
                print(f"播放系统提示音失败: {e}")
            return
        
        if AUDIO_BACKEND == "pygame":
            try:
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"pygame播放失败: {e}")
                self.fallback_system_sound()
        
        elif AUDIO_BACKEND == "playsound":
            try:
                # 在新线程中播放，避免阻塞UI
                threading.Thread(target=playsound, args=(sound_path,), daemon=True).start()
            except Exception as e:
                print(f"playsound播放失败: {e}")
                self.fallback_system_sound()
        
        else:
            self.fallback_system_sound()
    
    def fallback_system_sound(self):
        """使用Windows系统提示音作为备选"""
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
        
        # 等待线程结束
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=1)
        
        # 重置显示
        try:
            minutes = int(self.time_entry.get()) if self.time_entry.get() else self.config.get("default_minutes", 25)
        except ValueError:
            minutes = self.config.get("default_minutes", 25)
        
        self.remaining_seconds = minutes * 60
        self.update_timer_display(self.remaining_seconds)
        
        # 重置按钮和状态
        self.start_btn.config(text="▶ 开始", bg="#27AE60")
        self.status_label.config(text="准备就绪", fg="#95A5A6")
        self.time_entry.config(state="normal")
    
    def on_closing(self):
        """窗口关闭处理"""
        self.stop_event.set()
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=1)
        
        # 保存配置
        try:
            minutes = int(self.time_entry.get())
            self.config["default_minutes"] = minutes
            self.save_config()
        except ValueError:
            pass
        
        self.root.destroy()


def main():
    """主函数"""
    root = tk.Tk()
    
    # 设置DPI感知（Windows 10/11 高DPI支持）
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    
    # 设置图标（可选）
    try:
        # 如果有图标文件，可以设置
        # root.iconbitmap('pomodoro.ico')
        pass
    except Exception:
        pass
    
    app = PomodoroTimer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
