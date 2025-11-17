# 更新日志

所有重要的项目变更都会记录在此文件中。

---

## [1.2.1] - 2025-11-14

### ✨ 新增功能

- **登录状态显示** - 登录成功后在状态栏显示用户名
  - 支持普通登录和 TV 登录状态显示
  - 格式：`✓ 用户名 | ✓ TV`
  - 自动从 BBDown.data 读取用户信息

- **下载完成提示** - 下载完成后自动显示提示信息
  - 在状态栏显示"下载已完成"
  - 改进用户体验，明确下载状态

- **自动路径配置** - 首次运行自动配置工具路径
  - 自动检测并配置 BBDown.exe
  - 自动检测并配置 FFmpeg
  - 自动检测并配置 aria2c
  - 无需手动设置，开箱即用

### 🐛 修复问题

- **编码问题修复** - 完美支持中文，无乱码
  - 修复批量下载中文文件名乱码
  - 修复日志输出中文乱码
  - 统一使用 UTF-8 编码处理
  - 修复 Windows 控制台编码问题

- **配置文件处理** - 改进配置文件读取
  - 支持配置文件缺失时使用默认值
  - 添加配置文件自动升级功能
  - 改进错误处理和日志输出

### 🔧 优化改进

- **批量下载优化**
  - 改进批量下载的错误处理
  - 优化下载进度显示
  - 支持更多 URL 格式

- **界面优化**
  - 优化界面布局
  - 改进状态栏信息显示
  - 提升用户体验

- **打包优化**
  - 优化 PyInstaller 打包配置
  - 排除不必要的 PySide6 模块
  - 打包体积优化至约 50MB

### 📦 构建改进

- **自动化构建** - 改进 GitHub Actions 工作流
  - 自动从 GitHub 下载最新 BBDown
  - 自动下载 aria2 和 ffmpeg
  - 生成 7z 和 ZIP 两种压缩格式
  - 自动发布到 GitHub Releases

---

## [1.2.0] - 2025-09-19

### ✨ 新增功能

- **完全同步 BBDown 最新版本** - 支持所有最新功能
  
- **10 个新功能选项**
  - 弹幕格式选择 (`--download-danmaku-formats`)
  - 精简混流选项 (`--simply-mux`)
  - 视频升序选项 (`--video-ascending`)
  - 音频升序选项 (`--audio-ascending`)
  - 主机设置选项 (`--upos-host`)
  - TV 主机选项 (`--tv-host`)
  - 强制替换主机 (`--force-replace-host`)
  - 仅下载封面 (`--cover-only`)
  - 允许 PCDN (`--allow-pcdn`)
  - 显示所有分P (`--show-all`)

### 🔄 变更

- **命令行参数格式更新** - 与 BBDown 最新版本保持一致
  - `-dd` → `--download-danmaku` (下载弹幕)
  - `-ia` → `--interactive` (交互模式)
  - `-info` → `--only-show-info` (仅显示信息)
  - `-hs` → `--hide-streams` (隐藏流信息)
  - `-token` → `--access-token` (访问令牌)
  - `-c` → `--cookie` (Cookie)
  - `-mt` → `--multi-thread` (多线程)
  - `-p` → `--select-page` (选择分P)
  - `-F` → `--file-pattern` (文件命名模式)
  - `-M` → `--multi-file-pattern` (多文件命名模式)
  - `-ua` → `--user-agent` (用户代理)

### 🐛 修复问题

- 修复与 BBDown 最新版本的兼容性问题
- 改进配置文件自动升级功能
- 修复部分参数传递错误

### 🔧 优化改进

- 优化界面布局和用户体验
- 改进错误处理和日志输出
- 提升程序稳定性

---

## [1.2] - 初始版本

### ✨ 核心功能

- **图形化界面** - 基于 PySide6 的现代化 GUI
- **视频下载** - 支持 B 站视频、番剧、课程等
- **画质选择** - 支持 8K/4K/1080P/720P 等多种画质
- **登录功能** - 扫码登录，下载高画质视频
- **批量下载** - 从文本文件批量下载多个视频
- **字幕弹幕** - 支持下载字幕和弹幕
- **音频下载** - 支持仅下载音频
- **断点续传** - 支持下载中断后继续
- **多线程下载** - 使用 aria2c 加速下载
- **代理支持** - 支持 HTTP/SOCKS5 代理

### 🛠️ 技术栈

- Python 3.7+
- PySide6 6.9.2+
- PyInstaller 6.15.0+
- BBDown (核心下载引擎)
- FFmpeg (视频处理)
- aria2 (多线程下载)

---

## 版本说明

### 版本号格式

遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范：

- **主版本号 (Major)**: 重大功能更新或不兼容的 API 变更
- **次版本号 (Minor)**: 向后兼容的功能性新增
- **修订号 (Patch)**: 向后兼容的问题修正

### 发布类型

- **stable**: 稳定版本，推荐使用
- **beta**: 测试版本，可能存在问题
- **rc**: 候选版本，即将发布
- **alpha**: 早期版本，仅供测试

### 更新图例

- ✨ 新增功能
- 🐛 修复问题
- 🔧 优化改进
- 🔄 变更
- 📦 构建相关
- 📝 文档更新
- ⚠️ 废弃功能
- 🗑️ 移除功能

---

## 相关链接

- **项目主页**: https://github.com/albert-huan/BBDownG
- **发布页面**: https://github.com/albert-huan/BBDownG/releases
- **问题反馈**: https://github.com/albert-huan/BBDownG/issues
- **BBDown 官方**: https://github.com/nilaoda/BBDown

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

如果你发现了 bug 或有新功能建议，请：

1. 在 [Issues](https://github.com/albert-huan/BBDownG/issues) 中搜索是否已有相关问题
2. 如果没有，创建新的 Issue 并详细描述问题或建议
3. 如果你想贡献代码，请先 Fork 项目并创建 Pull Request

---

<div align="center">

**感谢使用 BBDownG！**

Made with ❤️ by [albert-huan](https://github.com/albert-huan)

</div>
