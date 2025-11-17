import os
import re
import configparser
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QDialog, QMessageBox
from UI.batch_download_ui import Ui_Dialog_batch_download
from tools import log, system
import subprocess
from time import sleep


class BatchDownloadThread(QThread):
    """批量下载线程"""
    progress_signal = Signal(int, int, str)  # 当前进度, 总数, 当前URL
    log_signal = Signal(str)  # 日志信息
    finished_signal = Signal(dict)  # 完成信号，传递统计信息
    
    def __init__(self, urls, base_args, download_dir):
        super().__init__()
        self.urls = urls
        self.base_args = base_args
        self.download_dir = download_dir
        self.is_stopped = False
        self.stats = {
            'total': len(urls),
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'failed_urls': []
        }
    
    def stop(self):
        """停止下载"""
        self.is_stopped = True
    
    def run(self):
        """执行批量下载"""
        self.log_signal.emit(f"{log()} 开始批量下载，共 {len(self.urls)} 个视频")
        
        for i, url in enumerate(self.urls):
            if self.is_stopped:
                self.log_signal.emit(f"{log()} 用户停止了批量下载")
                break
                
            # 发送进度信号
            self.progress_signal.emit(i + 1, len(self.urls), url)
            self.log_signal.emit(f"{log()} 正在下载第 {i+1}/{len(self.urls)} 个视频: {url}")
            
            # 构建下载命令
            args = self.base_args.replace('"视频地址占位符"', f'"{url}"')
            
            try:
                # 执行下载，设置环境变量和编码
                env = os.environ.copy()
                if system == 'Windows':
                    # Windows下强制使用UTF-8
                    process = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, 
                                             stderr=subprocess.STDOUT, cwd=self.download_dir,
                                             env=env, encoding='utf-8', errors='replace')
                else:
                    process = subprocess.Popen(args.split(), stdout=subprocess.PIPE, 
                                             stderr=subprocess.STDOUT, cwd=self.download_dir,
                                             encoding='utf-8', errors='replace')
                
                # 读取输出
                success = True
                while True:
                    if self.is_stopped:
                        process.terminate()
                        break
                        
                    output = process.stdout.readline()  # 已经是字符串，不需要decode
                    if output == '':
                        break
                    
                    try:
                        line = output.strip()
                        if line:
                            self.log_signal.emit(line)
                            # 检查是否有错误信息
                            if any(keyword in line.lower() for keyword in ['error', '错误', 'failed', '失败']):
                                success = False
                    except Exception:
                        continue
                
                # 等待进程结束
                process.wait()
                
                if self.is_stopped:
                    break
                
                # 检查返回码
                if process.returncode == 0 and success:
                    self.stats['success'] += 1
                    self.log_signal.emit(f"{log()} ✓ 第 {i+1} 个视频下载成功")
                else:
                    self.stats['failed'] += 1
                    self.stats['failed_urls'].append(url)
                    self.log_signal.emit(f"{log()} ✗ 第 {i+1} 个视频下载失败")
                    
            except Exception as e:
                self.stats['failed'] += 1
                self.stats['failed_urls'].append(url)
                self.log_signal.emit(f"{log()} ✗ 第 {i+1} 个视频下载异常: {str(e)}")
            
            # 短暂延迟，避免请求过于频繁
            if not self.is_stopped and i < len(self.urls) - 1:
                sleep(1)
        
        # 发送完成信号
        self.finished_signal.emit(self.stats)


class BatchDownloadDialog(QDialog, Ui_Dialog_batch_download):
    """批量下载对话框"""
    
    def __init__(self, base_args, download_dir):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('BBDownG - 批量下载')
        
        self.base_args = base_args
        self.download_dir = download_dir
        self.urls = []
        self.download_thread = None
        
        # 连接信号
        self.pushButton_select_file.clicked.connect(self.select_file)
        self.pushButton_start.clicked.connect(self.start_download)
        self.pushButton_stop.clicked.connect(self.stop_download)
        self.pushButton_close.clicked.connect(self.close)
        
        # 初始状态
        self.pushButton_start.setEnabled(False)
        self.pushButton_stop.setEnabled(False)
    
    def select_file(self):
        """选择配置文件"""
        from PySide6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择配置文件', '', 
            'Text Files (*.txt);;INI Files (*.ini);;All Files (*)'
        )
        
        if file_path:
            self.lineEdit_file_path.setText(file_path)
            self.load_urls_from_file(file_path)
    
    def load_urls_from_file(self, file_path):
        """从文件加载URL列表"""
        try:
            self.urls = []
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.ini':
                # 解析INI文件
                config = configparser.ConfigParser()
                config.read(file_path, encoding='utf-8')
                
                for section in config.sections():
                    for key, value in config.items(section):
                        if self.is_valid_url(value):
                            self.urls.append(value.strip())
                        elif self.is_valid_url(key):
                            self.urls.append(key.strip())
            
            else:
                # 解析TXT文件
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#') and self.is_valid_url(line):
                        self.urls.append(line)
            
            # 去重
            self.urls = list(dict.fromkeys(self.urls))
            
            # 更新UI
            self.textEdit_urls.clear()
            for i, url in enumerate(self.urls, 1):
                self.textEdit_urls.append(f"{i}. {url}")
            
            self.label_count.setText(f"共找到 {len(self.urls)} 个有效视频地址")
            self.pushButton_start.setEnabled(len(self.urls) > 0)
            
            if len(self.urls) == 0:
                QMessageBox.warning(self, '警告', '未找到有效的视频地址！')
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'读取文件失败：{str(e)}')
    
    def is_valid_url(self, url):
        """检查是否为有效的B站视频URL"""
        if not url:
            return False
        
        # B站视频URL模式
        patterns = [
            r'https?://www\.bilibili\.com/video/[Bb][Vv]\w+',
            r'https?://b23\.tv/\w+',
            r'https?://www\.bilibili\.com/bangumi/play/[Ee][Pp]\d+',
            r'https?://www\.bilibili\.com/bangumi/play/ss\d+',
            r'[Bb][Vv]\w+',
            r'[Ee][Pp]\d+',
            r'ss\d+'
        ]
        
        return any(re.match(pattern, url.strip()) for pattern in patterns)
    
    def start_download(self):
        """开始批量下载"""
        if not self.urls:
            QMessageBox.warning(self, '警告', '没有可下载的视频地址！')
            return
        
        # 创建下载线程
        self.download_thread = BatchDownloadThread(self.urls, self.base_args, self.download_dir)
        
        # 连接信号
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.log_signal.connect(self.append_log)
        self.download_thread.finished_signal.connect(self.download_finished)
        
        # 更新UI状态
        self.pushButton_start.setEnabled(False)
        self.pushButton_stop.setEnabled(True)
        self.pushButton_select_file.setEnabled(False)
        
        # 清空日志
        self.textEdit_log.clear()
        
        # 启动下载
        self.download_thread.start()
    
    def stop_download(self):
        """停止下载"""
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.stop()
            self.append_log(f"{log()} 正在停止下载...")
            self.pushButton_stop.setEnabled(False)
    
    def update_progress(self, current, total, url):
        """更新进度"""
        progress = int((current / total) * 100)
        self.progressBar.setValue(progress)
        self.label_progress.setText(f"进度: {current}/{total} ({progress}%)")
        self.label_current_url.setText(f"当前: {url}")
    
    def append_log(self, message):
        """添加日志"""
        self.textEdit_log.append(message)
        # 自动滚动到底部
        scrollbar = self.textEdit_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def download_finished(self, stats):
        """下载完成"""
        # 更新UI状态
        self.pushButton_start.setEnabled(True)
        self.pushButton_stop.setEnabled(False)
        self.pushButton_select_file.setEnabled(True)
        
        # 显示统计信息
        self.append_log(f"\n{log()} ==================== 下载完成 ====================")
        self.append_log(f"{log()} 总计: {stats['total']} 个视频")
        self.append_log(f"{log()} 成功: {stats['success']} 个")
        self.append_log(f"{log()} 失败: {stats['failed']} 个")
        self.append_log(f"{log()} 跳过: {stats['skipped']} 个")
        
        if stats['failed_urls']:
            self.append_log(f"{log()} 失败的视频地址:")
            for url in stats['failed_urls']:
                self.append_log(f"  - {url}")
        
        self.append_log(f"{log()} ================================================")
        
        # 显示完成对话框
        success_rate = (stats['success'] / stats['total']) * 100 if stats['total'] > 0 else 0
        QMessageBox.information(
            self, '下载完成', 
            f"批量下载已完成！\n\n"
            f"总计: {stats['total']} 个视频\n"
            f"成功: {stats['success']} 个\n"
            f"失败: {stats['failed']} 个\n"
            f"成功率: {success_rate:.1f}%"
        )
    
    def closeEvent(self, event):
        """关闭事件"""
        if self.download_thread and self.download_thread.isRunning():
            reply = QMessageBox.question(
                self, '确认', '下载正在进行中，确定要关闭吗？',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.download_thread.stop()
                self.download_thread.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()