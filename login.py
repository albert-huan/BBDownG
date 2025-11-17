import os.path
import time

from PySide6.QtWidgets import QDialog, QApplication
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QPixmap
import subprocess
from UI.qrcode_ui import Ui_Dialog
from tools import workdir, system, read_config


# 创建新线程
class WorkThread(QThread):
    s = Signal(str)

    def __init__(self, arg, process):
        super().__init__()
        self.arg = arg
        self.qr_found = False
        self.process = process

    def run(self):
        # 先等待二维码生成
        for i in range(10):  # 最多等待10秒
            time.sleep(1)
            if os.path.exists(os.path.join(os.getcwd(), 'qrcode.png')):
                self.qr_found = True
                self.s.emit('请扫描二维码')
                break
            else:
                self.s.emit('获取二维码中...')
        
        if not self.qr_found:
            self.s.emit('未获取到信息')
            return
            
        # 等待登录完成
        for i in range(171):  # 剩余171秒
            time.sleep(1)
            if ((self.arg == 'login') and (os.path.exists(os.path.join(workdir, 'BBDown.data')))) or (
                    (self.arg == "logintv") and (os.path.exists(os.path.join(workdir, "BBDownTV.data")))):
                # 获取用户名
                username = self.get_username()
                if username:
                    self.s.emit(f'登录成功！用户：{username}')
                else:
                    self.s.emit('登录成功')
                time.sleep(1)
                self.s.emit("关闭窗口")
                break
            elif os.path.exists(os.path.join(os.getcwd(), 'qrcode.png')):
                self.s.emit('请扫描二维码')
            else:
                self.s.emit('二维码已失效')
                break
    
    def get_username(self):
        """从BBDown.data文件中获取用户名"""
        try:
            import json
            data_file = os.path.join(workdir, 'BBDown.data' if self.arg == 'login' else 'BBDownTV.data')
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # BBDown.data中通常包含用户信息
                    if 'name' in data:
                        return data['name']
                    elif 'uname' in data:
                        return data['uname']
        except Exception as e:
            pass
        return None


# 显示登录二维码窗口
class Login(QDialog, Ui_Dialog):
    def __init__(self, arg):
        super(Login, self).__init__()
        self.setupUi(self)
        self.arg = arg
        self.setWindowTitle('BBdown - 登录')

        self.label_qr.setScaledContents(True)  # 设置图片自适应大小

        # 判断登录类型和是否有登录后的data文件
        if (arg == 'login') and (os.path.exists(os.path.join(workdir, 'BBDown.data'))):
            os.remove(os.path.join(workdir, 'BBDown.data'))
        if (arg == 'logintv') and (os.path.exists(os.path.join(workdir, 'BBDownTV.data'))):
            os.remove(os.path.join(workdir, 'BBDownTV.data'))

        # 获取BBDown程序路径
        config = read_config()['lineEdit_bbdown']

        # 调用BBdown获取二维码
        if system == 'Windows':
            self.cmd = subprocess.Popen([f'{config}', f'{self.arg}'], shell=True)
        else:
            self.cmd = subprocess.Popen([f'{config}', f'{self.arg}'])
        self.execute()

    # 调用新线程
    def execute(self):
        self.work = WorkThread(self.arg, self.cmd)
        self.work.start()
        self.work.s.connect(self.display)

    # 显示图片和信息
    def display(self, s):
        # 只有在二维码文件存在时才显示图片
        qr_path = os.path.join(os.getcwd(), 'qrcode.png')
        if os.path.exists(qr_path) and (s in ['请扫描二维码'] or s.startswith('登录成功')):
            self.label_qr.setPixmap(QPixmap(qr_path))
        
        self.label.setText(s)
        
        if s == '关闭窗口':
            try:
                if system == 'Linux':
                    subprocess.run(['kill', '-9', str(self.cmd.pid)])
                else:
                    subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.cmd.pid)], shell=True)
            except:
                pass  # 进程可能已经结束
            self.close()
