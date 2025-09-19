#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BBDownG 标准化发布构建器

遵循GitHub主流软件发布规范：
- 语义化版本号 (v1.2.3)
- 平台标识 (win64/macos/linux)
- 构建类型标记 (stable/beta/rc)
"""

import os
import sys
import shutil
import subprocess
import zipfile
import platform
from datetime import datetime
import json

# 版本配置
VERSION_MAJOR = 1
VERSION_MINOR = 2
VERSION_PATCH = 0
BUILD_TYPE = "stable"  # stable, beta, rc, alpha

# 平台检测
def get_platform_info():
    """获取平台信息"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        if machine in ["amd64", "x86_64"]:
            return "win64"
        else:
            return "win32"
    elif system == "darwin":
        if machine == "arm64":
            return "macos-arm64"
        else:
            return "macos-x64"
    elif system == "linux":
        if machine in ["amd64", "x86_64"]:
            return "linux-x64"
        elif machine in ["arm64", "aarch64"]:
            return "linux-arm64"
        else:
            return "linux-x86"
    else:
        return f"{system}-{machine}"

def get_version_string():
    """生成版本字符串"""
    version = f"v{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"
    if BUILD_TYPE != "stable":
        version += f"-{BUILD_TYPE}"
    return version

def get_release_name():
    """生成发布文件名"""
    version = get_version_string()
    platform_id = get_platform_info()
    return f"BBDownG-{version}-{platform_id}"

def check_dependencies():
    """检查构建依赖"""
    print("🔍 检查构建依赖...")
    
    try:
        import PySide6
        print(f"✅ PySide6: {PySide6.__version__}")
    except ImportError:
        print("❌ PySide6 未安装")
        print("请运行: pip install PySide6")
        return False
    
    try:
        result = subprocess.run(['pyinstaller', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ PyInstaller: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PyInstaller 未安装")
        print("请运行: pip install pyinstaller")
        return False
    
    return True

def clean_build_dirs():
    """清理构建目录"""
    print("🧹 清理构建目录...")
    
    dirs_to_clean = ['dist', 'build', 'releases']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  删除: {dir_name}")
    
    # 删除spec文件
    spec_files = [f for f in os.listdir('.') if f.endswith('.spec')]
    for spec_file in spec_files:
        os.remove(spec_file)
        print(f"  删除: {spec_file}")

def build_executable():
    """构建可执行文件"""
    print("🔨 构建可执行文件...")
    
    release_name = get_release_name()
    platform_id = get_platform_info()
    
    # 根据平台选择扩展名
    if platform_id.startswith('win'):
        exe_name = f"{release_name}.exe"
    else:
        exe_name = release_name
    
    # PyInstaller命令
    cmd = [
        'pyinstaller',
        '--onefile',           # 单文件模式
        '--windowed',          # 无控制台窗口
        f'--name={exe_name}',  # 输出文件名
        '--icon=UI/icon.ico',  # 图标文件
        '--clean',             # 清理缓存
        '--noconfirm',         # 不询问覆盖
        'main.py'              # 主程序文件
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 构建成功")
        return exe_name
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        print(f"错误输出: {e.stderr}")
        return None

def create_release_info():
    """创建发布信息文件"""
    version = get_version_string()
    platform_id = get_platform_info()
    
    release_info = {
        "version": version,
        "platform": platform_id,
        "build_type": BUILD_TYPE,
        "build_date": datetime.now().isoformat(),
        "python_version": sys.version,
        "system_info": {
            "system": platform.system(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "architecture": platform.architecture()[0]
        },
        "dependencies": {
            "PySide6": "6.9.2",
            "PyInstaller": "6.15.0"
        },
        "features": {
            "bbdown_compatibility": "Latest (1.4.9+)",
            "new_parameters": 11,
            "new_features": 10,
            "ui_framework": "PySide6"
        }
    }
    
    return release_info

def create_release_notes():
    """创建发布说明"""
    version = get_version_string()
    
    release_notes = f"""# BBDownG {version} 发布说明

## 📦 发布信息

- **版本**: {version}
- **平台**: {get_platform_info()}
- **构建类型**: {BUILD_TYPE}
- **发布日期**: {datetime.now().strftime('%Y-%m-%d')}

## ✨ 主要特性

### 🆕 新增功能 (10个)
- 弹幕格式选择 (`--download-danmaku-formats`)
- 精简混流选项 (`--simply-mux`)
- 视频/音频升序选项 (`--video-ascending`, `--audio-ascending`)
- 强制替换主机 (`--force-replace-host`)
- UPOS/TV主机设置 (`--upos-host`, `--tv-host`)
- 仅下载封面 (`--cover-only`)
- 允许PCDN (`--allow-pcdn`)
- 显示所有分P (`--show-all`)

### 🔧 参数更新 (11个)
- 完全同步BBDown最新版本参数格式
- 所有旧参数已更新为新格式 (如 `-dd` → `--download-danmaku`)
- 修复参数兼容性问题

### 🛠️ 技术改进
- 完全兼容BBDown 1.4.9+
- 改进错误处理和用户体验
- 自动配置升级功能
- 优化参数生成逻辑

## 💻 系统要求

### Windows
- Windows 7/10/11 (64位推荐)
- 内存: 至少 512MB
- 存储: 至少 100MB 可用空间

### macOS
- macOS 10.14+ (Mojave或更高版本)
- Intel或Apple Silicon处理器
- 内存: 至少 512MB

### Linux
- 大多数现代Linux发行版
- glibc 2.17+ (CentOS 7+, Ubuntu 16.04+)
- 内存: 至少 512MB

## 📋 依赖要求

### BBDown
- **推荐版本**: BBDown 1.4.9+
- **最低版本**: BBDown 1.4.0
- **下载地址**: https://github.com/nilaoda/BBDown/releases

### 可选工具
- **FFmpeg**: 用于视频处理 (推荐)
- **aria2c**: 用于多线程下载 (可选)

## 🚀 快速开始

1. **下载发布包**
   - 选择适合您系统的版本
   - 解压到任意目录

2. **准备BBDown**
   - 下载BBDown最新版本
   - 将BBDown.exe放在同一目录或设置路径

3. **运行程序**
   - 双击可执行文件启动
   - 首次运行会自动创建配置文件

4. **开始使用**
   - 输入B站视频链接
   - 选择下载选项
   - 开始下载

## 🔄 从旧版本升级

### 自动升级
- 程序会自动检测并升级配置文件
- 保持向后兼容性

### 手动升级
如遇问题，可以：
1. 备份现有配置文件
2. 删除旧配置文件
3. 重新运行程序生成新配置

## 🐛 已知问题

- 部分旧版本BBDown可能不兼容新参数
- 建议使用BBDown 1.4.9+以获得最佳体验

## 📞 技术支持

- **GitHub**: https://github.com/albert-huan/BBDownG
- **问题反馈**: 请在GitHub提交Issue
- **BBDown官方**: https://github.com/nilaoda/BBDown

## 🙏 致谢

感谢以下项目和开发者：
- BBDown - 核心下载引擎
- BBDown-GUI - UI设计参考
- BBDownG原项目 - 项目基础

---

**下载链接**: 请从GitHub Releases页面下载对应平台的版本
"""
    
    return release_notes

def create_release_package(exe_name):
    """创建发布包"""
    print("📦 创建发布包...")
    
    release_name = get_release_name()
    release_dir = f"releases/{release_name}"
    
    # 创建发布目录
    os.makedirs(release_dir, exist_ok=True)
    
    # 复制可执行文件
    exe_source = f"dist/{exe_name}"
    exe_dest = f"{release_dir}/{exe_name}"
    
    if os.path.exists(exe_source):
        shutil.copy2(exe_source, exe_dest)
        print(f"✅ 复制可执行文件: {exe_dest}")
    else:
        print(f"❌ 可执行文件未找到: {exe_source}")
        return False
    
    # 复制BBDown.exe（如果存在）
    if os.path.exists('BBDown.exe'):
        shutil.copy2('BBDown.exe', f"{release_dir}/BBDown.exe")
        print("  复制: BBDown.exe")
    
    # 创建发布信息文件
    release_info = create_release_info()
    with open(f"{release_dir}/release-info.json", 'w', encoding='utf-8') as f:
        json.dump(release_info, f, indent=2, ensure_ascii=False)
    print("  创建: release-info.json")
    
    # 创建发布说明
    release_notes = create_release_notes()
    with open(f"{release_dir}/RELEASE_NOTES.md", 'w', encoding='utf-8') as f:
        f.write(release_notes)
    print("  创建: RELEASE_NOTES.md")
    
    # 创建简化的README
    create_simple_readme(release_dir)
    
    return release_dir

def create_simple_readme(release_dir):
    """创建简化的README"""
    version = get_version_string()
    platform_id = get_platform_info()
    
    readme_content = f"""# BBDownG {version}

哔哩哔哩视频下载器 - 图形化界面版本

## 快速开始

1. 确保已下载BBDown.exe (https://github.com/nilaoda/BBDown/releases)
2. 双击运行BBDownG可执行文件
3. 在设置中配置BBDown路径（如果不在同一目录）
4. 输入B站视频链接开始下载

## 系统要求

- **平台**: {platform_id}
- **BBDown**: 1.4.0+ (推荐1.4.9+)
- **内存**: 512MB+
- **存储**: 100MB+

## 新功能

- ✅ 完全兼容BBDown最新版本
- ✅ 10个新下载选项
- ✅ 11个参数更新
- ✅ 改进的用户体验

## 技术支持

- GitHub: https://github.com/albert-huan/BBDownG
- 详细说明: 查看 RELEASE_NOTES.md

---
构建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open(f"{release_dir}/README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("  创建: README.md")

def create_archive(release_dir):
    """创建压缩包"""
    print("🗜️ 创建压缩包...")
    
    release_name = get_release_name()
    archive_name = f"{release_name}.zip"
    archive_path = f"releases/{archive_name}"
    
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, release_dir)
                zipf.write(file_path, arc_name)
                print(f"  添加: {arc_name}")
    
    print(f"✅ 创建压缩包: {archive_path}")
    return archive_path

def get_file_size(file_path):
    """获取文件大小"""
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def main():
    """主构建流程"""
    version = get_version_string()
    platform_id = get_platform_info()
    release_name = get_release_name()
    
    print("🚀 BBDownG 标准化发布构建")
    print("=" * 60)
    print(f"版本: {version}")
    print(f"平台: {platform_id}")
    print(f"构建类型: {BUILD_TYPE}")
    print(f"发布名称: {release_name}")
    print("=" * 60)
    
    # 检查依赖
    if not check_dependencies():
        print("❌ 依赖检查失败，请安装必要的包")
        return False
    
    # 清理构建目录
    clean_build_dirs()
    
    # 构建可执行文件
    exe_name = build_executable()
    if not exe_name:
        print("❌ 构建失败")
        return False
    
    # 创建发布包
    release_dir = create_release_package(exe_name)
    if not release_dir:
        print("❌ 发布包创建失败")
        return False
    
    # 创建压缩包
    archive_path = create_archive(release_dir)
    
    # 显示结果
    print("\n" + "=" * 60)
    print("🎉 构建完成！")
    print("=" * 60)
    
    exe_path = f"{release_dir}/{exe_name}"
    if os.path.exists(exe_path):
        print(f"📁 可执行文件: {exe_path}")
        print(f"📏 文件大小: {get_file_size(exe_path)}")
    
    if os.path.exists(archive_path):
        print(f"📦 发布包: {archive_path}")
        print(f"📏 压缩包大小: {get_file_size(archive_path)}")
    
    print(f"\n📋 发布信息:")
    print(f"- 版本: {version}")
    print(f"- 平台: {platform_id}")
    print(f"- 构建类型: {BUILD_TYPE}")
    print(f"- 发布名称: {release_name}")
    print(f"- 构建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\n📁 发布目录结构:")
    for root, dirs, files in os.walk(release_dir):
        level = root.replace(release_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")
    
    print(f"\n🎯 GitHub发布建议:")
    print(f"- Tag: {version}")
    print(f"- Release Title: BBDownG {version}")
    print(f"- 上传文件: {os.path.basename(archive_path)}")
    print(f"- 发布说明: 使用 RELEASE_NOTES.md 内容")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 标准化发布构建成功！")
        print("可以上传到GitHub Releases了！")
    else:
        print("\n❌ 发布构建失败，请检查错误信息")
    
    input("\n按回车键退出...")
    sys.exit(0 if success else 1)