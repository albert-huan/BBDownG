# BBDownG - 哔哩哔哩视频下载器 v1.2

BBDownG是BBDown的图形化跨平台版本，支持从哔哩哔哩(B站)下载视频、音频和字幕。它能够根据用户提供的URL循环下载视频，操作简单，支持多平台使用。

## 🎉 v1.2 重大更新

BBDownG v1.2 已完全同步BBDown最新版本的所有功能，提供了更好的兼容性和更多的下载选项。

### ✨ 新增功能 (10个)

1. **弹幕格式选择** (`--download-danmaku-formats`)
   - 支持指定下载的弹幕格式 (xml, ass, protobuf)

2. **精简混流选项** (`--simply-mux`)
   - 精简混流，不增加描述、作者等信息

3. **视频/音频升序选项**
   - 视频升序 (最小体积优先): `--video-ascending`
   - 音频升序 (最小体积优先): `--audio-ascending`

4. **主机设置选项**
   - UPOS服务器设置: `--upos-host`
   - TV端接口主机: `--tv-host`
   - 强制替换主机: `--force-replace-host`

5. **其他新功能**
   - 仅下载封面: `--cover-only`
   - 允许PCDN: `--allow-pcdn`
   - 显示所有分P: `--show-all`

### 🔧 参数更新 (11个)

| 旧参数 | 新参数 | 说明 |
|--------|--------|------|
| `-dd` | `--download-danmaku` | 下载弹幕 |
| `-ia` | `--interactive` | 交互式选择清晰度 |
| `-info` | `--only-show-info` | 仅解析不下载 |
| `-hs` | `--hide-streams` | 隐藏音视频流 |
| `-token` | `--access-token` | 访问令牌 |
| `-c` | `--cookie` | Cookie设置 |
| `-mt` | `--multi-thread` | 多线程下载 |
| `-p` | `--select-page` | 选择分P |
| `-F` | `--file-pattern` | 单分P文件名 |
| `-M` | `--multi-file-pattern` | 多分P文件名 |
| `-ua` | `--user-agent` | 用户代理 |

## 🚀 快速开始

### 1. 运行程序
双击 `BBDownG_v1.2.exe` 启动程序

### 2. 首次设置
- 如果没有BBDown.exe，请从 [BBDown官方](https://github.com/nilaoda/BBDown/releases) 下载
- 在设置中指定BBDown.exe的路径
- 配置下载目录和其他选项

### 3. 开始下载
- 输入B站视频链接
- 选择下载选项
- 点击开始下载

## 💡 特性

- **跨平台支持**：BBDownG可以在Windows、Linux等平台上运行，提供图形化用户界面，方便用户操作。
- **多种下载功能**：支持视频、音频和字幕下载，满足不同需求。
- **易于使用**：用户只需提供视频的URL，程序会自动处理下载任务。
- **完全兼容**：与BBDown最新版本完全兼容，支持所有最新功能。

## 📖 使用方法

### 基本使用

1. **准备工作**：
   - 将 `BBDownG_v1.2.exe`、`BBDown.exe` 放在同一目录下，或者在程序设置中指定它们的路径。
   
2. **Linux用户**：
   - 如果你在Linux系统下，且已经安装了 `ffmpeg` 等工具，可以在设置中取消勾选相应的路径，程序会自动识别系统环境变量。

### 新功能使用说明

#### 弹幕格式选择
在设置界面中启用"弹幕格式"选项，可以指定下载的弹幕格式：
- `xml`: 原始XML格式弹幕
- `ass`: ASS字幕格式
- `protobuf`: Protobuf格式弹幕

#### 文件名自定义
使用新的文件名模式变量：
```
<videoTitle>: 视频主标题
<pageNumber>: 视频分P序号
<pageNumberWithZero>: 视频分P序号(前缀补零)
<pageTitle>: 视频分P标题
<bvid>: 视频BV号
<aid>: 视频aid
<cid>: 视频cid
<dfn>: 视频清晰度
<res>: 视频分辨率
<fps>: 视频帧率
<videoCodecs>: 视频编码
<videoBandwidth>: 视频码率
<audioCodecs>: 音频编码
<audioBandwidth>: 音频码率
<ownerName>: 上传者名称
<ownerMid>: 上传者mid
<publishDate>: 发布时间
<videoDate>: 视频发布时间
<apiType>: API类型(TV/APP/INTL/WEB)
```

#### 代理和主机设置
新增了更多的代理和主机设置选项：
- **UPOS主机**: 自定义upos服务器
- **TV主机**: 自定义TV端接口请求主机
- **强制替换主机**: 强制替换下载服务器host

## 🔧 兼容性说明

### BBDown版本要求
- **推荐版本**: BBDown 1.4.9 或更高版本
- **最低版本**: BBDown 1.4.0
- **不支持**: BBDown 1.3.x 及以下版本

### 向后兼容性
- ✅ 现有配置文件将自动升级
- ✅ 旧的参数格式已更新为新格式
- ✅ 默认设置保持不变

### 系统要求
- Windows 7/10/11 (x64)
- 或 Linux (需要Python环境)
- 内存: 至少 512MB
- 存储: 至少 100MB 可用空间

## 🛠️ 故障排除

### 常见问题

1. **BBDown程序未找到**
   - 确保BBDown.exe在程序目录中
   - 或在设置中指定正确的BBDown路径

2. **参数不被识别**
   - 确保使用的是BBDown最新版本
   - 检查BBDown版本: `BBDown --version`

3. **配置文件错误**
   - 删除config.json文件重新生成
   - 或运行更新器重新初始化

### 获取帮助
如果遇到问题，请：
1. 检查BBDown版本兼容性
2. 查看BBDown官方文档
3. 提交Issue到项目仓库

## 📋 发布包内容

本发布包包含以下文件：
- **BBDownG_v1.2.exe** - 主程序（完全兼容BBDown最新版本）
- **BBDown.exe** - BBDown核心程序
- **使用说明.txt** - 快速使用指南
- **bbdown_updater.py** - 配置更新工具
- **test_update.py** - 功能测试脚本

## 📊 测试结果

```
配置文件更新: ✅ 通过
参数生成: ✅ 通过  
BBDown兼容性: ✅ 通过
构建测试: ✅ 通过
```

## 📝 更新日志

### v1.2 (2025-09-19)
- ✅ 完全同步BBDown最新版本
- ✅ 更新所有命令行参数 (11个参数更新)
- ✅ 添加10个新功能选项
- ✅ 修复兼容性问题
- ✅ 改进用户体验
- ✅ 自动配置升级
- ✅ 改进错误处理

### 技术规格
- **构建时间**: 2025-09-19 15:26:26
- **Python版本**: 3.12.10
- **PySide6版本**: 6.9.2
- **PyInstaller版本**: 6.15.0
- **支持系统**: Windows (x64)

## 🎯 未来计划

1. **UI界面优化** - 为新功能添加专门的UI控件
2. **批量下载增强** - 改进批量下载体验
3. **配置管理** - 添加配置导入/导出功能
4. **自动更新** - 实现BBDown版本自动检测更新

## 📞 技术支持

- **GitHub仓库**: [https://github.com/albert-huan/BBDownG](https://github.com/albert-huan/BBDownG)
- **BBDown官方**: [https://github.com/nilaoda/BBDown](https://github.com/nilaoda/BBDown)
- **问题反馈**: 请在GitHub仓库提交Issue

## 🙏 致谢

感谢以下开源项目和开发者的支持：

- **[BBDown](https://github.com/nilaoda/BBDown)** - 核心下载引擎
- **[BBDown - GUI](https://github.com/1299172402/BBDown_GUI)** - UI设计参考
- **[BBDownG 原项目](https://github.com/7lumen/BBDownG)** - 项目基础版本
- **[aria2c](https://github.com/aria2/aria2)** - 下载工具
- **[FFmpeg](https://github.com/FFmpeg/FFmpeg)** - 媒体处理

## 📄 许可协议

本项目遵循相关开源项目的许可协议。软件图标来源于网络，如有版权问题，请联系作者删除。

---

**🎉 BBDownG v1.2 - 完全兼容BBDown最新版本，享受最新功能和最佳体验！**