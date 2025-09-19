from PySide6.QtWidgets import QDialog, QFileDialog
from UI.setup_ui import Ui_Dialog_SetUp
from tools import save_config, load_config, read_config, bbdown_path
import os


class Window(QDialog, Ui_Dialog_SetUp):
    def __init__(self, flag=0):
        super(Window, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('BBDownG - 设置')
        
        # 如果是第一次运行，设置默认值
        if flag == 1:
            self.lineEdit_bbdown.setText(bbdown_path)
        else:
            # 加载配置
            try:
                load_config(self)
            except:
                # 如果加载失败，设置默认值
                self.lineEdit_bbdown.setText(bbdown_path)
        
        # 连接信号
        self.pushButton_bbdown.clicked.connect(self.select_bbdown)
        self.pushButton_ffmpeg.clicked.connect(self.select_ffmpeg)
        
        # 保存按钮
        self.pushButton_save.clicked.connect(self.save_settings)
    
    def select_bbdown(self):
        file_path = QFileDialog.getOpenFileName(self, '选择BBDown程序', '', 'BBDown (BBDown.exe);;All Files (*)')[0]
        if file_path:
            self.lineEdit_bbdown.setText(file_path)
    
    def select_ffmpeg(self):
        file_path = QFileDialog.getOpenFileName(self, '选择FFmpeg程序', '', 'FFmpeg (ffmpeg.exe);;All Files (*)')[0]
        if file_path:
            self.lineEdit_ffmpeg.setText(file_path)
    

    
    def save_settings(self):
        save_config(self)
        self.accept()  # 关闭对话框并返回接受状态