import os
import sys
import subprocess
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
from PySide6.QtCore import Qt

from UI.main_ui import Ui_MainWindow
from about import DialogAbout
from output import DialogOutput
from set_up import Window
from login import Login
from batch_download import BatchDownloadDialog
from tools import workdir, save_config, load_config, read_config, config_path, system
from UI import icon


# 主界面
class MainWindow(Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.parent = QMainWindow()
        self.setupUi(self.parent)
        self.parent.setWindowTitle('BBDownG - 1.2.1')

        flag = 0
        # 判断是否有配置文件
        if not os.path.isfile(config_path):
            self.lineEdit_dir.setText(os.path.join(workdir, 'Download'))  # 设置默认下载路径
            save_config(self)
            flag = 1
        else:
            load_config(self)  # 加载配置文件

        self.setup_window = Window(flag=flag)

        # 在窗体左下角添加登录状态标签（状态栏）
        self.label_login_status = QLabel(self.parent)
        self.label_login_status.setStyleSheet("color: #0084ff; font-size: 9pt; padding: 5px;")
        self.label_login_status.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # 将标签添加到状态栏左侧（非permanent，显示在左边）
        self.parent.statusBar().addWidget(self.label_login_status)

        self.pushButton_save_dir.clicked.connect(self.down_path)  # 下载路径
        self.pushButton_text.clicked.connect(self.open_url_text)  # 选择文本文件
        self.action_set_up.triggered.connect(self.open_setup)  # 打开设置界面
        self.action_about.triggered.connect(self.open_about)  # 打开关于界面
        self.pushButton_download.clicked.connect(self.download)  # 开始下载
        self.pushButton_login.clicked.connect(lambda x: self.open_login('login'))
        self.pushButton_logintv.clicked.connect(lambda x: self.open_login('logintv'))
        
        # 添加批量下载按钮连接（如果存在的话）
        if hasattr(self, 'pushButton_batch_download'):
            self.pushButton_batch_download.clicked.connect(lambda: self.open_batch_download())
        
        # 检查并显示登录状态
        self.update_login_status()

    # 设置下载保存路径
    def down_path(self):
        down_dir = QFileDialog.getExistingDirectory(None, '选择保存路径')
        if down_dir:
            self.lineEdit_dir.setText(down_dir)

    # 设置选择需要下载的url的文本文件
    def open_url_text(self):
        url_text = QFileDialog.getOpenFileName(None, '选择文件', '', '*.txt *.ini')[0]
        if url_text:
            self.lineEdit_url.setText(url_text)

    # 打开登录界面
    def open_login(self, arg):
        login = Login(arg)
        login.exec()
        self.close_process(str(login.cmd.pid))
        # 登录后更新状态
        self.update_login_status()

    # 打开设置界面
    def open_setup(self):
        self.setup_window.exec()

    # 当下载界面或登录界面关闭时候调用
    def close_process(self, pid):
        if system == 'Windows':
            subprocess.run(['taskkill', '/F', '/T', '/PID', pid], shell=True)
        else:
            subprocess.run(['kill', '-9', pid])

    # 开始下载
    def download(self):
        try:
            save_config(self)  # 保存配置
            args = self.arg()

            # 如果用户填写的下载地址是一个文本就根据文本内容下载
            if os.path.isfile(self.lineEdit_url.text()):
                # 使用批量下载功能
                self.open_batch_download(self.lineEdit_url.text())
            else:
                # 将参数传递到下载界面
                output_window = DialogOutput(args)
                output_window.exec()
                if hasattr(output_window, 'thread') and hasattr(output_window.thread, 'p'):
                    self.close_process(str(output_window.thread.p.pid))
        except Exception as e:
            print(f"下载出错: {e}")
            import traceback
            traceback.print_exc()

    # 下载参数
    def arg(self):
        args = ''

        # 读取配置文件
        config = read_config()

        # BBDown路径
        args += f'"{config["lineEdit_bbdown"]}"' if system == 'Windows' else f'{config["lineEdit_bbdown"]}'

        # 视频下载地址
        args += f' "{self.lineEdit_url.text()}" ' if system == 'Windows' else f' {self.lineEdit_url.text()} '

        # 画质选择
        if self.radioButton_dfn_priority.isChecked():
            pass
        elif self.radioButton_dfn_1080P.isChecked():
            args += ' --dfn-priority "1080P 高清" '
        elif self.radioButton_dfn_720P.isChecked():
            args += ' --dfn-priority "720P 高清" '
        elif self.radioButton_dfn_480P.isChecked():
            args += ' --dfn-priority "480P 清晰" '
        elif self.radioButton_dfn_360P.isChecked():
            args += ' --dfn-priority "360P 流畅" '
        elif self.radioButton_dfn_more.isChecked():  # 更多选项
            if self.comboBox_dfn_more.currentIndex() != 0:
                dfn = self.comboBox_dfn_more.itemText(self.comboBox_dfn_more.currentIndex())
                args += f' --dfn-priority "{dfn}"'

        # 下载源选择
        choice = ['--use-tv-api', '', '--use-app-api', '--use-intl-api']
        if choice[self.comboBox_source.currentIndex()]:
            args += ' ' + choice[self.comboBox_source.currentIndex()] + ' '

        # 下载视频编码选择
        if self.comboBox_encoding.currentIndex() != 0:
            choice = ['', 'avc', 'av1', 'hevc']
            args += ' --encoding-priority ' + choice[self.comboBox_encoding.currentIndex()] + ' '

        # 指定FFmpeg路径
        if config['checkBox_ffmpeg']:
            args += f' --ffmpeg-path "{config["lineEdit_ffmpeg"]}" '

        # 下载分P选项
        if self.radioButton_p_current.isChecked():
            pass
        elif self.radioButton_p_all.isChecked():
            args += ' --select-page ALL '

        # 下载选项
        if config['checkBox_audio_only']:  # 仅下载音频
            args += ' --audio-only '
        if config['checkBox_video_only']:  # 仅下载视频
            args += ' --video-only '
        if config['checkBox_sub_only']:  # 仅下载字幕
            args += ' --sub-only '
        if config['checkBox_danmaku']:  # 下载弹幕
            args += ' --download-danmaku '
        if config.get('checkBox_danmaku_only'):  # 仅下载弹幕
            args += ' --danmaku-only '
        
        # 新增下载选项
        if config.get('checkBox_cover_only'):  # 仅下载封面
            args += ' --cover-only '
        if config.get('checkBox_danmaku_formats') and config.get('lineEdit_danmaku_formats'):  # 弹幕格式
            args += f' --download-danmaku-formats "{config["lineEdit_danmaku_formats"]}" '

        # 交互选项
        if config['checkBox_ia']:  # 交互式选择清晰度
            args += ' --interactive '
        if config['checkBox_info']:  # 仅解析而不进行下载
            args += ' --only-show-info '
        if config['checkBox_hs']:  # 不显示所有音视频流
            args += ' --hide-streams '
        if config['checkBox_debug']:  # 输出调试日志
            args += ' --debug '

        # Cookies
        if config['checkBox_token']:  # 单独设置access_token
            args += f' --access-token "{config["lineEdit_token"]}" '
        if config['checkBox_c']:  # 单独设置cookie
            args += f' --cookie "{config["lineEdit_c"]}" '

        # 跳过选项
        if config['checkBox_skip_subtitle']:  # 跳过字幕下载
            args += ' --skip-subtitle '
        if config['checkBox_skip_cover']:  # 跳过封面下载
            args += ' --skip-cover '
        if config['checkBox_skip_mux']:  # 跳过混流步骤
            args += ' --skip-mux '
        if config['checkBox_skip_ai']:  # 跳过AI字幕下载
            args += ' --skip-ai true '
        else:
            args += ' --skip-ai false '

        # MP4box
        if config['checkBox_mp4box']:  # 使用MP4Box来混流
            args += ' --use-mp4box '
        if config['checkBox_mp4box_path']:  # 设置MP4Box的路径
            args += f' --mp4box-path "{config["lineEdit_mp4box_path"]}" '

        # 其他
        if config['checkBox_mt']:  # 使用多线程下载
            args += ' --multi-thread '
        if config['checkBox_force_http']:  # 使用HTTP替换HTTPS
            args += ' --force-http '
        if config['checkBox_language']:  # 设置混流的音频语言代码
            args += f' --language {config["lineEdit_language"]} '
        
        # 新增其他选项
        if config.get('checkBox_simply_mux'):  # 精简混流
            args += ' --simply-mux '
        if config.get('checkBox_video_ascending'):  # 视频升序
            args += ' --video-ascending '
        if config.get('checkBox_audio_ascending'):  # 音频升序
            args += ' --audio-ascending '
        if config.get('checkBox_force_replace_host'):  # 强制替换主机
            args += ' --force-replace-host '
        if config.get('checkBox_allow_pcdn'):  # 允许PCDN
            args += ' --allow-pcdn '
        if config.get('checkBox_show_all'):  # 显示所有分P
            args += ' --show-all '

        # 分P
        if config['checkBox_p']:  # 指定分p范围
            args += f' --select-page {config["lineEdit_p"]} '
        if config['checkBox_p_delay']:  # 分p下载间隔
            args += f' --delay-per-page {config["lineEdit_p_delay"]} '

        # aria2c
        if config['checkBox_use_aria2c']:  # 使用aria2c
            args += ' --use-aria2c '
            if config['checkBox_aria2c_path']:  # 文件路径
                args += f' --aria2c-path "{config["lineEdit_aria2c_path"]}" '
            if config['checkBox_aria2c_proxy']:  # 代理地址
                args += f' --aria2c-proxy {config["lineEdit_aria2c_proxy"]} '
            if config['checkBox_aria2c_args']:  # 附加参数
                args += f' --aria2c-args "{config["lineEdit_aria2c_args"]}" '

        # 文件名选项
        if config['checkBox_F']:  # 单分P
            args += f' --file-pattern "{config["lineEdit_F"]}" '
        if config['checkBox_M']:  # 多分P
            args += f' --multi-file-pattern "{config["lineEdit_M"]}" '

        # 代理
        if config['checkBox_enable_proxy']:  # 启用代理
            if config['checkBox_host']:  # 代理地址
                args += f' --host {config["lineEdit_host"]} '
            if config['checkBox_ep_host']:  # 番剧代理
                args += f' --ep-host {config["lineEdit_ep_host"]} '
            if config['checkBox_area']:  # 地区指定
                args += f' --area {config["lineEdit_area"]} '
        
        # 新增主机设置
        if config.get('checkBox_upos_host') and config.get('lineEdit_upos_host'):  # UPOS主机
            args += f' --upos-host {config["lineEdit_upos_host"]} '
        if config.get('checkBox_tv_host') and config.get('lineEdit_tv_host'):  # TV主机
            args += f' --tv-host {config["lineEdit_tv_host"]} '

        # ua设置
        if config['checkBox_ua']:
            args += f' --user-agent "{config["lineEdit_ua"]}"'

        # 是否记录已经下载视频，以便后续跳过
        if config['checkBox_archives']:
            args += f' --save-archives-to-file'

        # 下载路径
        args += f' --work-dir "{self.lineEdit_dir.text()}" ' if system == 'Windows' else f' --work-dir {self.lineEdit_dir.text()} '

        return args

    # 启动关于界面
    def open_about(self):
        about_window = DialogAbout()
        about_window.exec()
    
    # 打开批量下载界面
    def open_batch_download(self, file_path=None):
        save_config(self)  # 保存配置
        base_args = self.arg_for_batch()  # 获取批量下载参数
        
        batch_window = BatchDownloadDialog(base_args, self.lineEdit_dir.text())
        
        # 如果提供了文件路径，自动加载
        if file_path:
            batch_window.lineEdit_file_path.setText(file_path)
            batch_window.load_urls_from_file(file_path)
        
        batch_window.exec()
    
    # 为批量下载生成参数（不包含具体URL）
    def arg_for_batch(self):
        args = ''

        # 读取配置文件
        config = read_config()

        # BBDown路径
        args += f'"{config["lineEdit_bbdown"]}"' if system == 'Windows' else f'{config["lineEdit_bbdown"]}'

        # 视频下载地址占位符
        args += ' "视频地址占位符" '

        # 画质选择
        if self.radioButton_dfn_priority.isChecked():
            pass
        elif self.radioButton_dfn_1080P.isChecked():
            args += ' --dfn-priority "1080P 高清" '
        elif self.radioButton_dfn_720P.isChecked():
            args += ' --dfn-priority "720P 高清" '
        elif self.radioButton_dfn_480P.isChecked():
            args += ' --dfn-priority "480P 清晰" '
        elif self.radioButton_dfn_360P.isChecked():
            args += ' --dfn-priority "360P 流畅" '
        elif self.radioButton_dfn_more.isChecked():  # 更多选项
            if self.comboBox_dfn_more.currentIndex() != 0:
                dfn = self.comboBox_dfn_more.itemText(self.comboBox_dfn_more.currentIndex())
                args += f' --dfn-priority "{dfn}"'

        # 下载源选择
        choice = ['--use-tv-api', '', '--use-app-api', '--use-intl-api']
        if choice[self.comboBox_source.currentIndex()]:
            args += ' ' + choice[self.comboBox_source.currentIndex()] + ' '

        # 下载视频编码选择
        if self.comboBox_encoding.currentIndex() != 0:
            choice = ['', 'avc', 'av1', 'hevc']
            args += ' --encoding-priority ' + choice[self.comboBox_encoding.currentIndex()] + ' '

        # 指定FFmpeg路径
        if config['checkBox_ffmpeg']:
            args += f' --ffmpeg-path "{config["lineEdit_ffmpeg"]}" '

        # 下载分P选项
        if self.radioButton_p_current.isChecked():
            pass
        elif self.radioButton_p_all.isChecked():
            args += ' --select-page ALL '

        # 下载选项
        if config['checkBox_audio_only']:  # 仅下载音频
            args += ' --audio-only '
        if config['checkBox_video_only']:  # 仅下载视频
            args += ' --video-only '
        if config['checkBox_sub_only']:  # 仅下载字幕
            args += ' --sub-only '
        if config['checkBox_danmaku']:  # 下载弹幕
            args += ' --download-danmaku '
        if config.get('checkBox_danmaku_only'):  # 仅下载弹幕
            args += ' --danmaku-only '
        
        # 新增下载选项
        if config.get('checkBox_cover_only'):  # 仅下载封面
            args += ' --cover-only '
        if config.get('checkBox_danmaku_formats') and config.get('lineEdit_danmaku_formats'):  # 弹幕格式
            args += f' --download-danmaku-formats "{config["lineEdit_danmaku_formats"]}" '

        # 交互选项
        if config['checkBox_ia']:  # 交互式选择清晰度
            args += ' --interactive '
        if config['checkBox_info']:  # 仅解析而不进行下载
            args += ' --only-show-info '
        if config['checkBox_hs']:  # 不显示所有音视频流
            args += ' --hide-streams '
        if config['checkBox_debug']:  # 输出调试日志
            args += ' --debug '

        # Cookies
        if config['checkBox_token']:  # 单独设置access_token
            args += f' --access-token "{config["lineEdit_token"]}" '
        if config['checkBox_c']:  # 单独设置cookie
            args += f' --cookie "{config["lineEdit_c"]}" '

        # 跳过选项
        if config['checkBox_skip_subtitle']:  # 跳过字幕下载
            args += ' --skip-subtitle '
        if config['checkBox_skip_cover']:  # 跳过封面下载
            args += ' --skip-cover '
        if config['checkBox_skip_mux']:  # 跳过混流步骤
            args += ' --skip-mux '
        if config['checkBox_skip_ai']:  # 跳过AI字幕下载
            args += ' --skip-ai true '
        else:
            args += ' --skip-ai false '

        # MP4box
        if config['checkBox_mp4box']:  # 使用MP4Box来混流
            args += ' --use-mp4box '
        if config['checkBox_mp4box_path']:  # 设置MP4Box的路径
            args += f' --mp4box-path "{config["lineEdit_mp4box_path"]}" '

        # 其他
        if config['checkBox_mt']:  # 使用多线程下载
            args += ' --multi-thread '
        if config['checkBox_force_http']:  # 使用HTTP替换HTTPS
            args += ' --force-http '
        if config['checkBox_language']:  # 设置混流的音频语言代码
            args += f' --language {config["lineEdit_language"]} '
        
        # 新增其他选项
        if config.get('checkBox_simply_mux'):  # 精简混流
            args += ' --simply-mux '
        if config.get('checkBox_video_ascending'):  # 视频升序
            args += ' --video-ascending '
        if config.get('checkBox_audio_ascending'):  # 音频升序
            args += ' --audio-ascending '
        if config.get('checkBox_force_replace_host'):  # 强制替换主机
            args += ' --force-replace-host '
        if config.get('checkBox_allow_pcdn'):  # 允许PCDN
            args += ' --allow-pcdn '
        if config.get('checkBox_show_all'):  # 显示所有分P
            args += ' --show-all '

        # 分P
        if config['checkBox_p']:  # 指定分p范围
            args += f' --select-page {config["lineEdit_p"]} '
        if config['checkBox_p_delay']:  # 分p下载间隔
            args += f' --delay-per-page {config["lineEdit_p_delay"]} '

        # aria2c
        if config['checkBox_use_aria2c']:  # 使用aria2c
            args += ' --use-aria2c '
            if config['checkBox_aria2c_path']:  # 文件路径
                args += f' --aria2c-path "{config["lineEdit_aria2c_path"]}" '
            if config['checkBox_aria2c_proxy']:  # 代理地址
                args += f' --aria2c-proxy {config["lineEdit_aria2c_proxy"]} '
            if config['checkBox_aria2c_args']:  # 附加参数
                args += f' --aria2c-args "{config["lineEdit_aria2c_args"]}" '

        # 文件名选项
        if config['checkBox_F']:  # 单分P
            args += f' --file-pattern "{config["lineEdit_F"]}" '
        if config['checkBox_M']:  # 多分P
            args += f' --multi-file-pattern "{config["lineEdit_M"]}" '

        # 代理
        if config['checkBox_enable_proxy']:  # 启用代理
            if config['checkBox_host']:  # 代理地址
                args += f' --host {config["lineEdit_host"]} '
            if config['checkBox_ep_host']:  # 番剧代理
                args += f' --ep-host {config["lineEdit_ep_host"]} '
            if config['checkBox_area']:  # 地区指定
                args += f' --area {config["lineEdit_area"]} '
        
        # 新增主机设置
        if config.get('checkBox_upos_host') and config.get('lineEdit_upos_host'):  # UPOS主机
            args += f' --upos-host {config["lineEdit_upos_host"]} '
        if config.get('checkBox_tv_host') and config.get('lineEdit_tv_host'):  # TV主机
            args += f' --tv-host {config["lineEdit_tv_host"]} '

        # ua设置
        if config['checkBox_ua']:
            args += f' --user-agent "{config["lineEdit_ua"]}"'

        # 是否记录已经下载视频，以便后续跳过
        if config['checkBox_archives']:
            args += f' --save-archives-to-file'

        # 下载路径
        args += f' --work-dir "{self.lineEdit_dir.text()}" ' if system == 'Windows' else f' --work-dir {self.lineEdit_dir.text()} '

        return args
    
    # 启动关于界面
    def open_about(self):
        about_window = DialogAbout()
        about_window.exec()
    
    # 获取用户信息
    def get_user_info(self, login_type='login'):
        """从Bilibili API获取用户信息"""
        try:
            import json
            import urllib.request
            import socket
            
            data_file = os.path.join(workdir, 'BBDown.data' if login_type == 'login' else 'BBDownTV.data')
            if not os.path.exists(data_file):
                return None
            
            with open(data_file, 'r', encoding='utf-8') as f:
                data = f.read().strip()
            
            if login_type == 'login':
                # 解析Cookie获取SESSDATA
                cookies = {}
                for item in data.split(';'):
                    if '=' in item:
                        key, value = item.split('=', 1)
                        cookies[key.strip()] = value.strip()
                
                if 'SESSDATA' not in cookies:
                    return None
                
                # 调用Bilibili API获取用户信息（设置短超时避免阻塞）
                url = 'https://api.bilibili.com/x/web-interface/nav'
                req = urllib.request.Request(url)
                req.add_header('Cookie', f'SESSDATA={cookies["SESSDATA"]}')
                req.add_header('User-Agent', 'Mozilla/5.0')
                
                with urllib.request.urlopen(req, timeout=2) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    if result.get('code') == 0 and 'data' in result:
                        return result['data'].get('uname', None)
            else:
                # TV登录暂时无法获取用户名
                return 'TV用户'
                
        except (urllib.error.URLError, socket.timeout, Exception) as e:
            # 网络错误不影响程序运行，静默失败
            return None
    
    # 更新登录状态显示
    def update_login_status(self):
        """更新登录状态显示"""
        try:
            status_parts = []
            
            # 检查普通登录
            username = self.get_user_info('login')
            if username:
                # 如果用户名太长，截断显示
                if len(username) > 15:
                    display_name = username[:15] + "..."
                else:
                    display_name = username
                status_parts.append(f"✓ {display_name}")
            
            # 检查TV登录
            username_tv = self.get_user_info('logintv')
            if username_tv:
                status_parts.append("✓ TV")
            
            # 更新状态栏显示
            if status_parts:
                self.label_login_status.setText("  |  ".join(status_parts))
            else:
                self.label_login_status.setText("")
                
        except Exception as e:
            # 如果更新失败，不影响程序运行
            print(f"更新登录状态失败: {e}")
            self.label_login_status.setText("")


# 启动主界面
def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(':icon/icon.ico'))  # 设置图标
    window = MainWindow()
    window.parent.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
