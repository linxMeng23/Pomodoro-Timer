# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 打包配置文件
========================
用于将番茄钟应用打包成 Windows 可执行文件

使用方法：
    pyinstaller pomodoro.spec

或者直接运行 build.bat
"""

import os
import sys

# 项目根目录
project_dir = os.path.dirname(os.path.abspath(SPEC))

# 分析主程序
a = Analysis(
    ['pomodoro_timer.py'],
    pathex=[project_dir],
    binaries=[],
    datas=[
        # 包含 sounds.py 模块
        ('sounds.py', '.'),
    ],
    hiddenimports=[
        'pygame',
        'pygame.mixer',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='番茄钟',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # 可选：设置图标
    # icon='pomodoro.ico',
)
