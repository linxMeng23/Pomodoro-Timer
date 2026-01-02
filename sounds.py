"""
内置铃声生成模块
================
使用纯 Python 生成简单的提示音，无需外部音频文件。

功能：
- 生成不同类型的提示音（ding, bell, alarm）
- 使用 wave 模块生成 WAV 格式音频
- 支持 pygame 播放
"""

import os
import math
import wave
import struct
import tempfile


class SoundGenerator:
    """音频生成器类"""
    
    # 音频参数
    SAMPLE_RATE = 44100  # 采样率
    CHANNELS = 1         # 单声道
    SAMPLE_WIDTH = 2     # 16位
    
    def __init__(self):
        """初始化音频生成器"""
        self.sounds_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")
        self._ensure_sounds_dir()
        self._generated_files = {}
    
    def _ensure_sounds_dir(self):
        """确保 sounds 目录存在"""
        if not os.path.exists(self.sounds_dir):
            os.makedirs(self.sounds_dir)
    
    def _generate_sine_wave(self, frequency, duration, volume=0.8):
        """生成正弦波音频数据"""
        num_samples = int(self.SAMPLE_RATE * duration)
        samples = []
        
        for i in range(num_samples):
            t = i / self.SAMPLE_RATE
            # 添加淡入淡出效果
            fade_samples = int(0.01 * self.SAMPLE_RATE)  # 10ms 淡入淡出
            if i < fade_samples:
                fade = i / fade_samples
            elif i > num_samples - fade_samples:
                fade = (num_samples - i) / fade_samples
            else:
                fade = 1.0
            
            value = volume * fade * math.sin(2 * math.pi * frequency * t)
            samples.append(int(value * 32767))
        
        return samples
    
    def _generate_decay_tone(self, frequency, duration, volume=0.8, decay=3.0):
        """生成带衰减的音调"""
        num_samples = int(self.SAMPLE_RATE * duration)
        samples = []
        
        for i in range(num_samples):
            t = i / self.SAMPLE_RATE
            # 指数衰减
            envelope = math.exp(-decay * t)
            value = volume * envelope * math.sin(2 * math.pi * frequency * t)
            samples.append(int(value * 32767))
        
        return samples
    
    def _save_wav(self, samples, filename):
        """保存为 WAV 文件"""
        filepath = os.path.join(self.sounds_dir, filename)
        
        with wave.open(filepath, 'w') as wav_file:
            wav_file.setnchannels(self.CHANNELS)
            wav_file.setsampwidth(self.SAMPLE_WIDTH)
            wav_file.setframerate(self.SAMPLE_RATE)
            
            for sample in samples:
                packed = struct.pack('<h', max(-32768, min(32767, sample)))
                wav_file.writeframes(packed)
        
        return filepath
    
    def generate_ding(self):
        """
        生成清脆的 "叮" 提示音
        用于间隔提醒
        """
        filename = "ding.wav"
        filepath = os.path.join(self.sounds_dir, filename)
        
        if os.path.exists(filepath):
            return filepath
        
        # 高频短促的叮声
        samples = self._generate_decay_tone(
            frequency=1200,  # 1200Hz - 清脆的高音
            duration=0.3,    # 0.3秒
            volume=0.7,
            decay=8.0        # 快速衰减
        )
        
        return self._save_wav(samples, filename)
    
    def generate_bell(self):
        """
        生成悦耳的钟声
        用作结束提示音
        """
        filename = "bell.wav"
        filepath = os.path.join(self.sounds_dir, filename)
        
        if os.path.exists(filepath):
            return filepath
        
        samples = []
        
        # 混合多个频率模拟钟声
        frequencies = [523, 659, 784]  # C5, E5, G5 和弦
        duration = 1.5
        num_samples = int(self.SAMPLE_RATE * duration)
        
        for i in range(num_samples):
            t = i / self.SAMPLE_RATE
            envelope = math.exp(-2.0 * t)
            
            value = 0
            for freq in frequencies:
                value += 0.3 * envelope * math.sin(2 * math.pi * freq * t)
            
            samples.append(int(value * 32767))
        
        return self._save_wav(samples, filename)
    
    def generate_alarm(self):
        """
        生成响亮的闹钟声
        用作番茄钟结束的主提示音
        """
        filename = "alarm.wav"
        filepath = os.path.join(self.sounds_dir, filename)
        
        if os.path.exists(filepath):
            return filepath
        
        samples = []
        duration = 2.0
        num_samples = int(self.SAMPLE_RATE * duration)
        
        # 双音交替的闹钟声
        freq1, freq2 = 800, 1000
        switch_interval = 0.15  # 每0.15秒切换一次
        
        for i in range(num_samples):
            t = i / self.SAMPLE_RATE
            
            # 整体衰减
            envelope = 1.0 if t < 1.5 else math.exp(-3 * (t - 1.5))
            
            # 频率切换
            if int(t / switch_interval) % 2 == 0:
                freq = freq1
            else:
                freq = freq2
            
            value = 0.6 * envelope * math.sin(2 * math.pi * freq * t)
            samples.append(int(value * 32767))
        
        return self._save_wav(samples, filename)
    
    def generate_soft_chime(self):
        """
        生成柔和的风铃声
        适合作为轻柔的提示音
        """
        filename = "chime.wav"
        filepath = os.path.join(self.sounds_dir, filename)
        
        if os.path.exists(filepath):
            return filepath
        
        samples = []
        duration = 1.0
        num_samples = int(self.SAMPLE_RATE * duration)
        
        # 递降的三连音
        notes = [
            (880, 0.0, 0.3),   # A5
            (784, 0.15, 0.3),  # G5
            (659, 0.30, 0.4),  # E5
        ]
        
        for i in range(num_samples):
            t = i / self.SAMPLE_RATE
            value = 0
            
            for freq, start, note_duration in notes:
                if t >= start:
                    note_t = t - start
                    if note_t < note_duration:
                        envelope = math.exp(-5 * note_t)
                        value += 0.4 * envelope * math.sin(2 * math.pi * freq * note_t)
            
            samples.append(int(value * 32767))
        
        return self._save_wav(samples, filename)
    
    def generate_double_beep(self):
        """
        生成双声提示音
        用于重要提醒
        """
        filename = "double_beep.wav"
        filepath = os.path.join(self.sounds_dir, filename)
        
        if os.path.exists(filepath):
            return filepath
        
        samples = []
        duration = 0.6
        num_samples = int(self.SAMPLE_RATE * duration)
        
        freq = 1000
        beep_duration = 0.1
        gap = 0.1
        
        for i in range(num_samples):
            t = i / self.SAMPLE_RATE
            value = 0
            
            # 第一声
            if 0 <= t < beep_duration:
                envelope = math.exp(-10 * t)
                value = 0.6 * envelope * math.sin(2 * math.pi * freq * t)
            # 第二声
            elif beep_duration + gap <= t < beep_duration * 2 + gap:
                t2 = t - beep_duration - gap
                envelope = math.exp(-10 * t2)
                value = 0.6 * envelope * math.sin(2 * math.pi * freq * t2)
            
            samples.append(int(value * 32767))
        
        return self._save_wav(samples, filename)
    
    def generate_all_sounds(self):
        """生成所有内置铃声"""
        sounds = {
            "ding": self.generate_ding(),
            "bell": self.generate_bell(),
            "alarm": self.generate_alarm(),
            "chime": self.generate_soft_chime(),
            "double_beep": self.generate_double_beep()
        }
        return sounds
    
    def get_builtin_sounds(self):
        """
        获取所有内置铃声的信息
        返回格式: [(显示名称, 文件路径), ...]
        """
        # 确保所有铃声都已生成
        self.generate_all_sounds()
        
        return [
            ("🔔 叮 (Ding)", os.path.join(self.sounds_dir, "ding.wav")),
            ("🔔 钟声 (Bell)", os.path.join(self.sounds_dir, "bell.wav")),
            ("⏰ 闹钟 (Alarm)", os.path.join(self.sounds_dir, "alarm.wav")),
            ("🎐 风铃 (Chime)", os.path.join(self.sounds_dir, "chime.wav")),
            ("📢 双响 (Double Beep)", os.path.join(self.sounds_dir, "double_beep.wav")),
        ]


# 便捷函数
_generator = None

def get_sound_generator():
    """获取音频生成器单例"""
    global _generator
    if _generator is None:
        _generator = SoundGenerator()
    return _generator

def get_builtin_sounds():
    """获取内置铃声列表"""
    return get_sound_generator().get_builtin_sounds()

def get_ding_sound():
    """获取叮声路径"""
    return get_sound_generator().generate_ding()

def get_alarm_sound():
    """获取闹钟声路径"""
    return get_sound_generator().generate_alarm()


if __name__ == "__main__":
    # 测试生成铃声
    generator = SoundGenerator()
    sounds = generator.generate_all_sounds()
    print("已生成以下铃声:")
    for name, path in sounds.items():
        print(f"  - {name}: {path}")
