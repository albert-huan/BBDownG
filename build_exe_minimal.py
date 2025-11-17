#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess

# Fix encoding issues on Windows - MUST be at the very top
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

"""
BBDownG Minimal Build Script
Minimize exe file size as much as possible
"""

def clean():
    """清理构建目录"""
    print("清理旧文件...")
    dirs = ['dist', 'build']
    for d in dirs:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"  删除: {d}")
    
    # 删除spec文件
    for f in os.listdir('.'):
        if f.endswith('.spec'):
            os.remove(f)
            print(f"  删除: {f}")

def build():
    """构建exe（最小化版本）"""
    print("\n开始构建最小化版本...")
    
    cmd = [
        'pyinstaller',
        '--onefile',                            # 单文件
        '--windowed',                           # 无控制台
        '--name=BBDownG',                       # 程序名
        '--icon=UI/icon.ico',                   # 图标
        '--add-data=UI;UI',                     # 添加UI文件夹
        
        # 只导入必需的模块
        '--hidden-import=PySide6.QtCore',
        '--hidden-import=PySide6.QtGui',
        '--hidden-import=PySide6.QtWidgets',
        
        # 排除所有不需要的PySide6模块
        '--exclude-module=PySide6.Qt3DAnimation',
        '--exclude-module=PySide6.Qt3DCore',
        '--exclude-module=PySide6.Qt3DExtras',
        '--exclude-module=PySide6.Qt3DInput',
        '--exclude-module=PySide6.Qt3DLogic',
        '--exclude-module=PySide6.Qt3DRender',
        '--exclude-module=PySide6.QtAxContainer',
        '--exclude-module=PySide6.QtBluetooth',
        '--exclude-module=PySide6.QtCharts',
        '--exclude-module=PySide6.QtConcurrent',
        '--exclude-module=PySide6.QtDataVisualization',
        '--exclude-module=PySide6.QtDBus',
        '--exclude-module=PySide6.QtDesigner',
        '--exclude-module=PySide6.QtGraphs',
        '--exclude-module=PySide6.QtGraphsWidgets',
        '--exclude-module=PySide6.QtHelp',
        '--exclude-module=PySide6.QtHttpServer',
        '--exclude-module=PySide6.QtLocation',
        '--exclude-module=PySide6.QtMultimedia',
        '--exclude-module=PySide6.QtMultimediaWidgets',
        '--exclude-module=PySide6.QtNetworkAuth',
        '--exclude-module=PySide6.QtNfc',
        '--exclude-module=PySide6.QtOpenGL',
        '--exclude-module=PySide6.QtOpenGLWidgets',
        '--exclude-module=PySide6.QtPdf',
        '--exclude-module=PySide6.QtPdfWidgets',
        '--exclude-module=PySide6.QtPositioning',
        '--exclude-module=PySide6.QtPrintSupport',
        '--exclude-module=PySide6.QtQml',
        '--exclude-module=PySide6.QtQuick',
        '--exclude-module=PySide6.QtQuick3D',
        '--exclude-module=PySide6.QtQuickControls2',
        '--exclude-module=PySide6.QtQuickWidgets',
        '--exclude-module=PySide6.QtRemoteObjects',
        '--exclude-module=PySide6.QtScxml',
        '--exclude-module=PySide6.QtSensors',
        '--exclude-module=PySide6.QtSerialBus',
        '--exclude-module=PySide6.QtSerialPort',
        '--exclude-module=PySide6.QtSpatialAudio',
        '--exclude-module=PySide6.QtSql',
        '--exclude-module=PySide6.QtStateMachine',
        '--exclude-module=PySide6.QtSvg',
        '--exclude-module=PySide6.QtSvgWidgets',
        '--exclude-module=PySide6.QtTest',
        '--exclude-module=PySide6.QtTextToSpeech',
        '--exclude-module=PySide6.QtUiTools',
        '--exclude-module=PySide6.QtWebChannel',
        '--exclude-module=PySide6.QtWebEngine',
        '--exclude-module=PySide6.QtWebEngineCore',
        '--exclude-module=PySide6.QtWebEngineQuick',
        '--exclude-module=PySide6.QtWebEngineWidgets',
        '--exclude-module=PySide6.QtWebSockets',
        '--exclude-module=PySide6.QtXml',
        
        # 排除其他不需要的模块
        '--exclude-module=matplotlib',
        '--exclude-module=numpy',
        '--exclude-module=pandas',
        '--exclude-module=PIL',
        '--exclude-module=tkinter',
        
        '--clean',
        '--noconfirm',
        'main.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("构建成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False

def create_release():
    """创建发布包"""
    print("\n创建发布包...")
    
    release_dir = "BBDownG-Release"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # 复制exe
    if os.path.exists('dist/BBDownG.exe'):
        shutil.copy2('dist/BBDownG.exe', f'{release_dir}/BBDownG.exe')
        print("  [OK] BBDownG.exe")
    
    # 复制BBDown
    if os.path.exists('BBDown.exe'):
        shutil.copy2('BBDown.exe', f'{release_dir}/BBDown.exe')
        print("  [OK] BBDown.exe")
    
    # 复制ffmpeg
    if os.path.exists('ffmpeg'):
        shutil.copytree('ffmpeg', f'{release_dir}/ffmpeg')
        print("  [OK] ffmpeg/")
    
    # 复制aria2
    if os.path.exists('aria2'):
        shutil.copytree('aria2', f'{release_dir}/aria2')
        print("  [OK] aria2/")
    
    # 复制使用说明
    if os.path.exists('使用说明.txt'):
        shutil.copy2('使用说明.txt', f'{release_dir}/使用说明.txt')
        print("  [OK] 使用说明.txt")
    
    print(f"\n[OK] 发布包已创建: {release_dir}/")
    
    # 显示文件大小
    exe_path = f'{release_dir}/BBDownG.exe'
    if os.path.exists(exe_path):
        size = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"   BBDownG.exe 大小: {size:.1f} MB")

def main():
    print("=" * 60)
    print("BBDownG 最小化打包工具")
    print("=" * 60)
    
    # 检查PyInstaller
    try:
        subprocess.run(['pyinstaller', '--version'], 
                      capture_output=True, check=True)
    except:
        print("[ERROR] PyInstaller 未安装")
        print("请运行: pip install pyinstaller")
        return False
    
    # 清理
    clean()
    
    # 构建
    if not build():
        return False
    
    # 创建发布包
    create_release()
    
    print("\n" + "=" * 60)
    print("[SUCCESS] 最小化打包完成！")
    print("=" * 60)
    print(f"发布包位置: BBDownG-Release/")
    print("文件大小已优化，应该在 50MB 左右")
    
    return True

if __name__ == "__main__":
    success = main()
    
    # Only wait for input in interactive mode
    if sys.stdin.isatty():
        try:
            input("\n按回车键退出...")
        except (EOFError, KeyboardInterrupt):
            pass
    
    sys.exit(0 if success else 1)
