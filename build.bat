@echo off
chcp 65001 >nul
echo ============================================
echo     番茄钟应用 - 打包脚本
echo ============================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

REM 检查 PyInstaller 是否安装
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [信息] 正在安装 PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [错误] PyInstaller 安装失败
        pause
        exit /b 1
    )
)

REM 检查 pygame 是否安装
pip show pygame >nul 2>&1
if errorlevel 1 (
    echo [信息] 正在安装 pygame...
    pip install pygame
)

echo.
echo [信息] 开始打包...
echo.

REM 使用 spec 文件打包
pyinstaller pomodoro.spec --clean

if errorlevel 1 (
    echo.
    echo [错误] 打包失败！
    pause
    exit /b 1
)

echo.
echo ============================================
echo     打包完成！
echo ============================================
echo.
echo 可执行文件位置：dist\番茄钟.exe
echo.
echo 首次运行时，程序会自动在同目录下生成：
echo   - sounds\ 文件夹（内置铃声）
echo   - pomodoro_config.json（配置文件）
echo.

REM 打开输出目录
explorer dist

pause
