# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'batch_download_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QProgressBar, QPushButton,
    QSizePolicy, QTextEdit, QVBoxLayout, QWidget)

class Ui_Dialog_batch_download(object):
    def setupUi(self, Dialog_batch_download):
        if not Dialog_batch_download.objectName():
            Dialog_batch_download.setObjectName(u"Dialog_batch_download")
        Dialog_batch_download.resize(800, 600)
        Dialog_batch_download.setMinimumSize(QSize(800, 600))
        
        # 主布局
        self.verticalLayout_main = QVBoxLayout(Dialog_batch_download)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        
        # 文件选择组
        self.groupBox_file = QGroupBox(Dialog_batch_download)
        self.groupBox_file.setObjectName(u"groupBox_file")
        self.groupBox_file.setTitle("配置文件")
        self.groupBox_file.setMaximumSize(QSize(16777215, 80))
        
        self.horizontalLayout_file = QHBoxLayout(self.groupBox_file)
        self.horizontalLayout_file.setObjectName(u"horizontalLayout_file")
        
        self.label_file = QLabel(self.groupBox_file)
        self.label_file.setObjectName(u"label_file")
        self.label_file.setText("文件路径:")
        self.label_file.setMaximumSize(QSize(60, 16777215))
        self.horizontalLayout_file.addWidget(self.label_file)
        
        self.lineEdit_file_path = QLineEdit(self.groupBox_file)
        self.lineEdit_file_path.setObjectName(u"lineEdit_file_path")
        self.lineEdit_file_path.setReadOnly(True)
        self.horizontalLayout_file.addWidget(self.lineEdit_file_path)
        
        self.pushButton_select_file = QPushButton(self.groupBox_file)
        self.pushButton_select_file.setObjectName(u"pushButton_select_file")
        self.pushButton_select_file.setText("浏览")
        self.pushButton_select_file.setMaximumSize(QSize(80, 16777215))
        self.horizontalLayout_file.addWidget(self.pushButton_select_file)
        
        self.verticalLayout_main.addWidget(self.groupBox_file)
        
        # URL列表组
        self.groupBox_urls = QGroupBox(Dialog_batch_download)
        self.groupBox_urls.setObjectName(u"groupBox_urls")
        self.groupBox_urls.setTitle("视频地址列表")
        self.groupBox_urls.setMaximumSize(QSize(16777215, 200))
        
        self.verticalLayout_urls = QVBoxLayout(self.groupBox_urls)
        self.verticalLayout_urls.setObjectName(u"verticalLayout_urls")
        
        self.label_count = QLabel(self.groupBox_urls)
        self.label_count.setObjectName(u"label_count")
        self.label_count.setText("共找到 0 个有效视频地址")
        self.verticalLayout_urls.addWidget(self.label_count)
        
        self.textEdit_urls = QTextEdit(self.groupBox_urls)
        self.textEdit_urls.setObjectName(u"textEdit_urls")
        self.textEdit_urls.setReadOnly(True)
        self.textEdit_urls.setMaximumHeight(150)
        self.verticalLayout_urls.addWidget(self.textEdit_urls)
        
        self.verticalLayout_main.addWidget(self.groupBox_urls)
        
        # 进度组
        self.groupBox_progress = QGroupBox(Dialog_batch_download)
        self.groupBox_progress.setObjectName(u"groupBox_progress")
        self.groupBox_progress.setTitle("下载进度")
        self.groupBox_progress.setMaximumSize(QSize(16777215, 120))
        
        self.verticalLayout_progress = QVBoxLayout(self.groupBox_progress)
        self.verticalLayout_progress.setObjectName(u"verticalLayout_progress")
        
        self.label_progress = QLabel(self.groupBox_progress)
        self.label_progress.setObjectName(u"label_progress")
        self.label_progress.setText("进度: 0/0 (0%)")
        self.verticalLayout_progress.addWidget(self.label_progress)
        
        self.progressBar = QProgressBar(self.groupBox_progress)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.verticalLayout_progress.addWidget(self.progressBar)
        
        self.label_current_url = QLabel(self.groupBox_progress)
        self.label_current_url.setObjectName(u"label_current_url")
        self.label_current_url.setText("当前: 无")
        self.label_current_url.setWordWrap(True)
        self.verticalLayout_progress.addWidget(self.label_current_url)
        
        self.verticalLayout_main.addWidget(self.groupBox_progress)
        
        # 日志组
        self.groupBox_log = QGroupBox(Dialog_batch_download)
        self.groupBox_log.setObjectName(u"groupBox_log")
        self.groupBox_log.setTitle("下载日志")
        
        self.verticalLayout_log = QVBoxLayout(self.groupBox_log)
        self.verticalLayout_log.setObjectName(u"verticalLayout_log")
        
        self.textEdit_log = QTextEdit(self.groupBox_log)
        self.textEdit_log.setObjectName(u"textEdit_log")
        self.textEdit_log.setReadOnly(True)
        font = QFont()
        font.setFamilies([u"Consolas", u"Monaco", u"monospace"])
        font.setPointSize(9)
        self.textEdit_log.setFont(font)
        self.verticalLayout_log.addWidget(self.textEdit_log)
        
        self.verticalLayout_main.addWidget(self.groupBox_log)
        
        # 按钮组
        self.horizontalLayout_buttons = QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName(u"horizontalLayout_buttons")
        
        # 添加弹性空间
        from PySide6.QtWidgets import QSpacerItem, QSizePolicy
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_buttons.addItem(spacer)
        
        self.pushButton_start = QPushButton(Dialog_batch_download)
        self.pushButton_start.setObjectName(u"pushButton_start")
        self.pushButton_start.setText("开始下载")
        self.pushButton_start.setMinimumSize(QSize(100, 30))
        self.horizontalLayout_buttons.addWidget(self.pushButton_start)
        
        self.pushButton_stop = QPushButton(Dialog_batch_download)
        self.pushButton_stop.setObjectName(u"pushButton_stop")
        self.pushButton_stop.setText("停止下载")
        self.pushButton_stop.setMinimumSize(QSize(100, 30))
        self.horizontalLayout_buttons.addWidget(self.pushButton_stop)
        
        self.pushButton_close = QPushButton(Dialog_batch_download)
        self.pushButton_close.setObjectName(u"pushButton_close")
        self.pushButton_close.setText("关闭")
        self.pushButton_close.setMinimumSize(QSize(100, 30))
        self.horizontalLayout_buttons.addWidget(self.pushButton_close)
        
        self.verticalLayout_main.addLayout(self.horizontalLayout_buttons)
        
        # 设置窗口标题
        self.retranslateUi(Dialog_batch_download)
        QMetaObject.connectSlotsByName(Dialog_batch_download)

    def retranslateUi(self, Dialog_batch_download):
        Dialog_batch_download.setWindowTitle(QCoreApplication.translate("Dialog_batch_download", u"批量下载", None))
        self.groupBox_file.setTitle(QCoreApplication.translate("Dialog_batch_download", u"配置文件", None))
        self.label_file.setText(QCoreApplication.translate("Dialog_batch_download", u"文件路径:", None))
        self.pushButton_select_file.setText(QCoreApplication.translate("Dialog_batch_download", u"浏览", None))
        self.groupBox_urls.setTitle(QCoreApplication.translate("Dialog_batch_download", u"视频地址列表", None))
        self.label_count.setText(QCoreApplication.translate("Dialog_batch_download", u"共找到 0 个有效视频地址", None))
        self.groupBox_progress.setTitle(QCoreApplication.translate("Dialog_batch_download", u"下载进度", None))
        self.label_progress.setText(QCoreApplication.translate("Dialog_batch_download", u"进度: 0/0 (0%)", None))
        self.label_current_url.setText(QCoreApplication.translate("Dialog_batch_download", u"当前: 无", None))
        self.groupBox_log.setTitle(QCoreApplication.translate("Dialog_batch_download", u"下载日志", None))
        self.pushButton_start.setText(QCoreApplication.translate("Dialog_batch_download", u"开始下载", None))
        self.pushButton_stop.setText(QCoreApplication.translate("Dialog_batch_download", u"停止下载", None))
        self.pushButton_close.setText(QCoreApplication.translate("Dialog_batch_download", u"关闭", None))