# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:SettingWidget.py
@time:2020/4/16 11:53
"""

import configparser

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFileDialog, \
    QPushButton, QScrollArea, QGridLayout, QSpinBox,QColorDialog

BTN_STYLE = """
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
        """

SCROLLAREA_STYLE = """
        QLabel{
            font-family:Microsoft Yahei;
            font-size:14px;
            color:dimgray;
            font-weight:bold;
        }

        QWidget{
            background:#FBFAFA;
        }

        QLineEdit{
            border:1px solid #B5ADAD;
            font-family:Microsoft Yahei;
            font-size:13px;
            color:gray;
        }
        QScrollArea{
            border:0px solid #B5ADAD;
        }
        QScrollBar:vertical  
        {
            border-radius:7px;  
            background:#f1f1f1; 
            padding-top:14px;  
            padding-bottom:14px;  
        }
        QScrollBar::handle:vertical
        {
            background:#C4CAD0; 
            border-radius:6px;  
            margin-left:2px;  
            margin-right:2px;  
        }
        QScrollBar::handle:vertical:hover  
        {
            background:gray;
            border-radius:6px;
        }
        QScrollBar::add-line:vertical  
        {
            height:14px;width:8px;  
            image:url('');  
        }
        QScrollBar::sub-line:vertical  
        {
            height:14px;width:8px;
            image:url('');  
        }
        QScrollBar::add-line:vertical:hover  
        {
            height:14px;width:8px;
            image:url('');
            subcontrol-position:bottom;
        }
        QScrollBar::sub-line:vertical:hover 
        {
            height:14px;width:8px;
            image:url('');  
            subcontrol-position:top;
        }
        QScrollBar::add-page:vertical  
        {
            background:#f1f1f1;
        }
        QScrollBar::sub-page:vertical  
        {
            background:#f1f1f1; 
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

        """


class SettingWidget(QWidget):

    def __init__(self, fWind):
        super().__init__()
        self.fWindow = fWind

        self.config = configparser.ConfigParser()
        self.config.read("init.ini",encoding="utf8")

        self.initUI()
        self.resetData()

    def initUI(self):

        """------------------图片标注设置------------------"""
        self.label_Img = QLabel('图片标注设置')
        self.label_Img.setFixedHeight(20)
        self.label_Img.setAlignment(Qt.AlignCenter)

        self.label_textformat = QLabel('标注文本模板:')
        self.label_textformat.setFixedSize(200, 20)
        self.label_textformat.setAlignment(Qt.AlignLeft)

        self.label_textformat_info = QLabel()
        self.label_textformat_info.setFixedHeight(90)
        self.label_textformat_info.setAlignment(Qt.AlignLeft)
        self.label_textformat_info.setStyleSheet("font-family:Microsoft Yahei;font-size:12px;color:gray;")
        self.label_textformat_info.setText("    请在模板中你想要的位置插入以下关键字，系统会自动替换为相应的数据：\n    图片创建的:\n\t年：{year}\t月：{month}\t日：{day}\n\t时：{hour}\t分：{minute}\t秒：{second}\n    图片的名称: {name}")

        self.lineedit_textformat = QLineEdit()
        self.lineedit_textformat.setFixedHeight(30)
        self.lineedit_textformat.textChanged.connect(self.on_textformat_changed)

        self.label_textformat_preview = QLabel('效果预览:')
        self.label_textformat_preview.setFixedHeight(20)
        self.label_textformat_preview.setAlignment(Qt.AlignLeft)
        self.label_textformat_preview.setStyleSheet("font-family:Microsoft Yahei;font-size:12px;color:gray;")

        layout_textformat = QVBoxLayout()
        layout_textformat.setContentsMargins(0, 5, 0, 0)
        layout_textformat.setSpacing(5)
        layout_textformat.addWidget(self.label_textformat)
        layout_textformat.addWidget(self.label_textformat_info)
        layout_textformat.addWidget(self.lineedit_textformat)
        layout_textformat.addWidget(self.label_textformat_preview)

        self.label_textsize = QLabel('文本大小:')
        self.label_textsize.setFixedSize(60, 30)
        self.label_textsize.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.spinbox_textsize = QSpinBox()
        self.spinbox_textsize.setFixedSize(50, 22)
        self.spinbox_textsize.setAlignment(Qt.AlignCenter)
        self.spinbox_textsize.setMinimum(1)
        self.spinbox_textsize.setMaximum(200)

        layout_textsize = QHBoxLayout()
        layout_textsize.setContentsMargins(0, 5, 0, 0)
        layout_textsize.setSpacing(5)
        layout_textsize.addWidget(self.label_textsize)
        layout_textsize.addWidget(self.spinbox_textsize)
        layout_textsize.addStretch()

        self.label_textoffset = QLabel('文本垂直偏移量:')
        self.label_textoffset.setFixedSize(100, 30)
        self.label_textoffset.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.spinbox_textoffset = QSpinBox()
        self.spinbox_textoffset.setFixedSize(50, 22)
        self.spinbox_textoffset.setAlignment(Qt.AlignCenter)
        self.spinbox_textoffset.setMinimum(-20)
        self.spinbox_textoffset.setMaximum(100)

        layout_textoffset = QHBoxLayout()
        layout_textoffset.setContentsMargins(0, 5, 0, 0)
        layout_textoffset.setSpacing(5)
        layout_textoffset.addWidget(self.label_textoffset)
        layout_textoffset.addWidget(self.spinbox_textoffset)
        layout_textoffset.addStretch()

        self.label_textcolor = QLabel('文本颜色:')
        self.label_textcolor.setFixedSize(60, 30)
        self.label_textcolor.setAlignment(Qt.AlignLeft | Qt.AlignCenter)

        self.label_textcolor_R = QLabel('R:')
        self.label_textcolor_R.setFixedSize(30, 30)
        self.label_textcolor_R.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.spinbox_textcolor_R = QSpinBox()
        self.spinbox_textcolor_R.setFixedSize(50, 22)
        self.spinbox_textcolor_R.setAlignment(Qt.AlignCenter)
        self.spinbox_textcolor_R.setMinimum(0)
        self.spinbox_textcolor_R.setMaximum(255)

        self.label_textcolor_G = QLabel('G:')
        self.label_textcolor_G.setFixedSize(30, 30)
        self.label_textcolor_G.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.spinbox_textcolor_G = QSpinBox()
        self.spinbox_textcolor_G.setFixedSize(50, 22)
        self.spinbox_textcolor_G.setAlignment(Qt.AlignCenter)
        self.spinbox_textcolor_G.setMinimum(0)
        self.spinbox_textcolor_G.setMaximum(255)

        self.label_textcolor_B = QLabel('B:')
        self.label_textcolor_B.setFixedSize(30, 30)
        self.label_textcolor_B.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.spinbox_textcolor_B = QSpinBox()
        self.spinbox_textcolor_B.setFixedSize(50, 22)
        self.spinbox_textcolor_B.setAlignment(Qt.AlignCenter)
        self.spinbox_textcolor_B.setMinimum(0)
        self.spinbox_textcolor_B.setMaximum(255)

        self.label_textcolor_example=QLabel()
        self.label_textcolor_example.setFixedSize(100,30)

        self.colorDialogBtn=QPushButton("选择颜色")
        self.colorDialogBtn.setFixedSize(60,30)
        self.colorDialogBtn.clicked.connect(self.on_colorDialogBtn_clicked)

        layout_textcolor = QHBoxLayout()
        layout_textcolor.setContentsMargins(0, 5, 0, 0)
        layout_textcolor.setSpacing(5)
        layout_textcolor.addWidget(self.label_textcolor)
        layout_textcolor.addWidget(self.label_textcolor_R)
        layout_textcolor.addWidget(self.spinbox_textcolor_R)
        layout_textcolor.addWidget(self.label_textcolor_G)
        layout_textcolor.addWidget(self.spinbox_textcolor_G)
        layout_textcolor.addWidget(self.label_textcolor_B)
        layout_textcolor.addWidget(self.spinbox_textcolor_B)
        layout_textcolor.addStretch()
        layout_textcolor.addWidget(self.label_textcolor_example)
        layout_textcolor.addStretch()
        layout_textcolor.addWidget(self.colorDialogBtn)

        self.label_OutPutPath = QLabel('结果保存路径:')
        self.label_OutPutPath.setFixedSize(200, 20)
        self.label_OutPutPath.setAlignment(Qt.AlignLeft)
        self.lineedit_OutPutPath = QLineEdit()
        self.lineedit_OutPutPath.setFixedHeight(30)
        self.btn_OutPutPath = QPushButton('...')
        self.btn_OutPutPath.setStyleSheet(BTN_STYLE)
        self.btn_OutPutPath.setFixedSize(30, 30)
        self.btn_OutPutPath.clicked.connect(self.on_btn_OutPutPath_clicked)

        layout_OutPutPath = QGridLayout()
        layout_OutPutPath.setContentsMargins(0, 5, 0, 0)
        layout_OutPutPath.setSpacing(5)
        layout_OutPutPath.addWidget(self.label_OutPutPath, 0, 0)
        layout_OutPutPath.addWidget(self.lineedit_OutPutPath, 1, 0)
        layout_OutPutPath.addWidget(self.btn_OutPutPath, 1, 1)

        layout_Img = QVBoxLayout()
        layout_Img.setContentsMargins(5, 10, 5, 0)
        layout_Img.setSpacing(10)
        layout_Img.addWidget(self.label_Img)
        layout_Img.addLayout(layout_textformat)
        layout_Img.addLayout(layout_textsize)
        layout_Img.addLayout(layout_textoffset)
        layout_Img.addLayout(layout_textcolor)
        layout_Img.addLayout(layout_OutPutPath)


        """------------------QScrollArea------------------"""
        sa_contentLayout = QVBoxLayout()
        sa_contentLayout.setContentsMargins(0, 0, 0, 0)
        sa_contentLayout.setSpacing(10)
        sa_contentLayout.addLayout(layout_Img)
        sa_contentLayout.addStretch()

        self.sa_contentWidget = QWidget()
        self.sa_contentWidget.setFixedSize(600, 450)
        self.sa_contentWidget.setLayout(sa_contentLayout)

        self.sa_Settings = QScrollArea()
        self.sa_Settings.setStyleSheet(SCROLLAREA_STYLE)
        self.sa_Settings.setWidget(self.sa_contentWidget)
        self.sa_Settings.setAlignment(Qt.AlignHCenter)

        # ------------------------------------------------------
        self.btn_defualt = QPushButton('默认')
        self.btn_defualt.setFixedSize(60, 30)
        self.btn_defualt.setStyleSheet(BTN_STYLE)
        self.btn_defualt.setStatusTip('恢复默认设置')
        self.btn_defualt.clicked.connect(self.on_btn_defualt_clicked)
        self.btn_cancel = QPushButton('取消')
        self.btn_cancel.setFixedSize(60, 30)
        self.btn_cancel.setStyleSheet(BTN_STYLE)
        self.btn_cancel.setStatusTip('取消未保存的修改')
        self.btn_cancel.clicked.connect(self.on_btn_cancel_clicked)
        self.btn_apply = QPushButton('应用')
        self.btn_apply.setFixedSize(60, 30)
        self.btn_apply.setStyleSheet(BTN_STYLE)
        self.btn_apply.setStatusTip('保存并应用修改')
        self.btn_apply.clicked.connect(self.on_btn_apply_clicked)

        layout_bottom = QHBoxLayout()
        layout_bottom.setContentsMargins(0, 0, 20, 0)
        layout_bottom.setSpacing(5)
        layout_bottom.addStretch(1)
        layout_bottom.addWidget(self.btn_defualt)
        layout_bottom.addWidget(self.btn_cancel)
        layout_bottom.addWidget(self.btn_apply)

        # -------------------------------------------------------
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(5, 0, 5, 5)
        mainLayout.setSpacing(3)
        mainLayout.addWidget(self.sa_Settings)
        mainLayout.addLayout(layout_bottom)

        self.setLayout(mainLayout)

    def resetData(self):
        self.lineedit_textformat.setText(self.config.get("IMG","textformat"))
        self.on_textformat_changed()

        self.spinbox_textsize.setValue(int(self.config.get("IMG","textsize")))

        self.spinbox_textoffset.setValue(int(self.config.get("IMG", "textoffset")))

        r,g,b=int(self.config.get("IMG","textcolorr")),int(self.config.get("IMG","textcolorg")),int(self.config.get("IMG","textcolorb"))
        self.spinbox_textcolor_R.setValue(r)
        self.spinbox_textcolor_G.setValue(g)
        self.spinbox_textcolor_B.setValue(b)
        self.label_textcolor_example.setStyleSheet("background-color:rgb({},{},{});border:1px solid #B5ADAD;".format(r,g,b))

        self.lineedit_OutPutPath.setText(self.config.get("IMG","imgsavepath"))

    def defualtData(self):
        self.config.read("./defualt.ini",encoding="utf8")
        self.resetData()
        self.config.write(open("./init.ini", "w",encoding="utf8"))

    def on_btn_OutPutPath_clicked(self):
        path = QFileDialog.getExistingDirectory(self, "设置图片标注结果保存路径", ".")
        if len(path) != 0:
            self.lineedit_OutPutPath.setText(path)

    def on_colorDialogBtn_clicked(self):
        col = QColorDialog.getColor()
        self.spinbox_textcolor_R.setValue(col.red())
        self.spinbox_textcolor_G.setValue(col.green())
        self.spinbox_textcolor_B.setValue(col.blue())
        self.label_textcolor_example.setStyleSheet(
            "background-color:rgb({},{},{});border:1px solid #B5ADAD;".format(col.red(), col.green(), col.blue()))

    def on_btn_defualt_clicked(self):
        self.defualtData()

    def on_btn_cancel_clicked(self):
        self.resetData()

    def on_btn_apply_clicked(self):
        self.saveConfig()

    def on_textformat_changed(self):
        format="效果预览:  "+self.lineedit_textformat.text()
        format =format.replace('{year}','2020')
        format =format.replace('{month}', '1')
        format =format.replace('{day}', '1')
        format =format.replace('{hour}', '8')
        format =format.replace('{minute}', '30')
        format =format.replace('{second}', '12')
        format =format.replace('{name}', '风景画')
        self.label_textformat_preview.setText(format)


    def show(self):
        self.resetData()
        super().show()

    def saveConfig(self):
        self.config.set("IMG","textformat",self.lineedit_textformat.text())
        self.config.set("IMG", "textsize", str(self.spinbox_textsize.value()))
        self.config.set("IMG", "textoffset", str(self.spinbox_textoffset.value()))
        self.config.set("IMG", "textcolorr", str(self.spinbox_textcolor_R.value()))
        self.config.set("IMG", "textcolorg", str(self.spinbox_textcolor_G.value()))
        self.config.set("IMG", "textcolorb", str(self.spinbox_textcolor_B.value()))
        self.config.set("IMG", "imgsavepath", str(self.lineedit_OutPutPath.text()))

        self.config.write(open("./init.ini", "w",encoding="utf8"))