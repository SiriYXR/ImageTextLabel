# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:MainWindow.py
@time:2020/4/15 18:58
"""
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget,QVBoxLayout,QPushButton,QHBoxLayout

from ImgProcessWidget import ImgProcessWidget
from SettingWidget import SettingWidget

MAIN_STYLE = """
        *{
            font-family:Microsoft Yahei;
            font-size:12px;
            color:dimgray;
            background-color:#fff;
        }

        QPushButton
        {
            font-family:Microsoft Yahei;
            font-size:14px;
            color:dimgray;
            background-color:#fff;
            border:1px solid #B5ADAD;
            border-radius:2px;
        }
        QPushButton:hover
        {
            color:#fff;
            background-color:dimgray;
        }
        QPushButton:pressed
        {
            color:#fff;
            background-color:dimgray;
            padding-left:3px;
            padding-top:3px;
        }

        QComboBox{
            font-family:Microsoft YaHei;
            border:1px solid #B5ADAD;
            border-radius:2px;
            background: #fff;
            font:12px;
            color:dimgray;
        }
        QComboBox QAbstractItemView{
            border: 0px;
            outline:0px;
            selection-background-color: #2C2A28;
            height:100px;
            background: #fff;
            font-size:12px
        }
        QComboBox QAbstractItemView::item {
            height:30px;
        }
        QComboBox QAbstractItemView::item:selected{
            background-color: #f1f1f1;
        }
        QComboBox::down-arrow{
            background: #fff;
            color:dimgray;
        }
        QComboBox::drop-down{
            border:0px;
        }


        QSpinBox{
            border:1px solid #B5ADAD;
            height: 21px;
        }
        /*spinbox 抬起样式*/
        QTimeEdit::up-button,QDoubleSpinBox::up-button,QSpinBox::up-button {subcontrol-origin:border;
            subcontrol-position:right;
            image: url(./GUI2/img/spinbox_up_right.png);
            width: 12px;
            height: 20px;       
        }
        QTimeEdit::down-button,QDoubleSpinBox::down-button,QSpinBox::down-button {subcontrol-origin:border;
            subcontrol-position:left;
            border-image: url(./GUI2/img/spinbox_up_left.png);
            width: 12px;
            height: 20px;
        }
        /*按钮按下样式*/
        QTimeEdit::up-button:pressed,QDoubleSpinBox::up-button:pressed,QSpinBox::up-button:pressed{subcontrol-origin:border;
            subcontrol-position:right;
            image: url(./GUI2/img/spinbox_down_right.png);
            width: 12px;
            height: 20px;       
        }
        QTimeEdit::down-button:pressed,QDoubleSpinBox::down-button:pressed,QSpinBox::down-button:pressed,QSpinBox::down-button:pressed{
            subcontrol-position:left;
            image: url(./GUI2/img/spinbox_down_left.png);
            width: 12px;
            height: 20px;
        }
        """

TOP_BTN_ON_STYLE="""
        QPushButton
        {
            font-family:Microsoft Yahei;
            font-size:14px;
            color:#27a2f1;
            background-color:#f1f1f1;
            border:0px solid #f1f1f1;
            border-radius:0px;
        }

        QPushButton:hover
        {
            background-color:#f1f1f1;
        }

        QPushButton:pressed
        {
            background-color:#f1f1f1;
            padding-left:3px;
            padding-top:3px;
        }
        """

TOP_BTN_OFF_STYLE="""
        QPushButton
        {
            font-family:Microsoft Yahei;
            font-size:14px;
            color:#8e8e8e;
            background-color:#f1f1f1;
            border:0px solid #f1f1f1;
            border-radius:0px;
        }

        QPushButton:hover
        {
            background-color:#f1f1f1;
        }

        QPushButton:pressed
        {
            background-color:#f1f1f1;
            padding-left:3px;
            padding-top:3px;
        }
        """

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        self.setMinimumSize(800, 600)
        self.setStyleSheet(MAIN_STYLE)
        self.setWindowIcon(QIcon('./pictures.png'))
        self.move(int((QApplication.desktop().width() - self.width()) / 2),
                  int((QApplication.desktop().height() - self.height()) / 2))
        self.setWindowTitle('图片标注')
        self.statusBar().showMessage('欢迎使用！')

        self.imgProcessBtn = QPushButton('图片标注')
        self.imgProcessBtn.setFixedHeight(30)
        self.imgProcessBtn.setStyleSheet(TOP_BTN_ON_STYLE)
        self.imgProcessBtn.setStatusTip('图片标注')
        self.imgProcessBtn.clicked.connect(self.on_imgProcessBtn_clicked)

        self.settingBtn = QPushButton('系统设置')
        self.settingBtn.setFixedHeight(30)
        self.settingBtn.setStyleSheet(TOP_BTN_OFF_STYLE)
        self.settingBtn.setStatusTip('系统设置')
        self.settingBtn.clicked.connect(self.on_settingBtn_clicked)

        topLayout = QHBoxLayout()
        topLayout.setContentsMargins(0, 0, 0, 0)
        topLayout.setSpacing(0)
        topLayout.addWidget(self.imgProcessBtn)
        topLayout.addWidget(self.settingBtn)

        self.imgProcessWidget=ImgProcessWidget(self)

        self.settingWidget=SettingWidget(self)
        self.settingWidget.hide()

        bottomLayout = QVBoxLayout()
        bottomLayout.addWidget(self.imgProcessWidget)
        bottomLayout.addWidget(self.settingWidget)

        mainWdiget=QWidget()

        layout=QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addLayout(topLayout)
        layout.addLayout(bottomLayout)

        mainWdiget.setLayout(layout)
        self.setCentralWidget(mainWdiget)

    def on_imgProcessBtn_clicked(self):
        self.imgProcessWidget.setHidden(False)
        self.settingWidget.setHidden(True)

        self.imgProcessBtn.setStyleSheet(TOP_BTN_ON_STYLE)
        self.settingBtn.setStyleSheet(TOP_BTN_OFF_STYLE)

    def on_settingBtn_clicked(self):
        self.imgProcessWidget.setHidden(True)
        self.settingWidget.setHidden(False)

        self.imgProcessBtn.setStyleSheet(TOP_BTN_OFF_STYLE)
        self.settingBtn.setStyleSheet(TOP_BTN_ON_STYLE)