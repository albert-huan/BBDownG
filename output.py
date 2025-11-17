import os
import signal
import subprocess
from time import sleep

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QDialog

from UI.output_ui import Ui_Dialog_output
from tools import log, system


# 创建新线程
class NewThreads(QThread):
    output_signal = Signal(str)
    info_signal = Signal(bool)

    def __init__(self, args):
        """
        :param args: 命令行参数
        """
        super().__init__()
        # 导入workdir
        from tools import workdir
        # 运行命令，设置工作目录为BBDown所在目录，以便读取BBDown.data
        # 设置环境变量强制UTF-8输出
        env = os.environ.copy()
        if system == 'Windows':
            # Windows下强制使用UTF-8
            self.p = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, 
                                     stderr=subprocess.STDOUT, cwd=workdir, env=env,
                                     encoding='utf-8', errors='replace')
        
        else:
            self.p = subprocess.Popen(args.split(), stdout=subprocess.PIPE, 
                                     stderr=subprocess.STDOUT, cwd=workdir,
                                     encoding='utf-8', errors='replace')

    def run(self):
        try:
            while True:
                out = self.p.stdout.readline()  # 获取输出内容（已经是字符串）
                if out == '':
                    # 等待进程结束并获取返回码
                    returncode = self.p.wait()
                    self.info_signal.emit(True)
                    break
                # 传递内容
                self.output_signal.emit(out)
        except Exception as e:
            self.output_signal.emit(f'\n错误: {str(e)}\n')
            self.info_signal.emit(True)


# 窗体
class DialogOutput(QDialog, Ui_Dialog_output):
    def __init__(self, args, flag=False):
        super().__init__()
        self.setupUi(self)
        self.flag = flag
        self.args = args
        self.setWindowTitle('BBDownG - 下载')

        # 显示下载参数
        self.lineEdit_cmd.setText(self.args)
        self.lineEdit_cmd.setCursorPosition(0)
        self.pushButton_stop.clicked.connect(self.stop)  # 暂停下载
        self.flage_stop = False
        self.stat_down()  # 开始下载

    # 创建线程，开始下载
    def stat_down(self):
        self.thread = NewThreads(self.args)
        self.thread.start()
        self.thread.output_signal.connect(self.display)
        self.thread.info_signal.connect(self.close_down_window)

    # 将信息显示出来
    def display(self, m):
        self.textEdit_output.setText(self.textEdit_output.toPlainText() + m.strip() + '\n')
        self.textEdit_output.verticalScrollBar().setValue(self.textEdit_output.verticalScrollBar().maximum())

    # 暂停下载
    def stop(self):
        if self.flage_stop:
            return
        # 调用命令，暂停下载
        if system == 'Windows':
            subprocess.Popen(['taskkill', '/F', '/T', '/PID', str(self.thread.p.pid)], shell=True)
        else:
            subprocess.Popen(['kill', '-9', str(self.thread.p.pid)])

        self.display('')
        self.display('')
        self.display(log() + ' 下载已停止')
        self.flage_stop = True

    # 关闭下载窗口
    def close_down_window(self, finished):
        if finished:
            self.display('')
            self.display(log() + ' 下载已完成')
            self.pushButton_stop.setText('关闭')
            self.pushButton_stop.clicked.disconnect()
            self.pushButton_stop.clicked.connect(self.close)
        if self.flag:
            sleep(3)  # 休眠3秒
            self.close()  # 关闭窗口
