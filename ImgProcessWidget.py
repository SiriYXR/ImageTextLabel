# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:ImgProcessWidget.py
@time:2020/4/15 19:07
"""

import os
import time
import cv2
import numpy
import configparser
import exifread
import datetime
from PIL import ImageQt,Image

from PyQt5.QtCore import Qt,QRect
from PyQt5.QtGui import QImage,QPixmap,QPainter,QColor,QFont,qRed, qGreen, qBlue
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QFileDialog, QLineEdit, \
    QSpinBox, QColorDialog

MAIN_STYLE = """
        *{
            font-family:Microsoft Yahei;
            font-size:12px;
            color:dimgray;
        }
        
        QLineEdit{
            background-color:#fff;
            border:1px solid #B5ADAD;
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

SCROLLAREA_STYLE = """
        QLabel{
            font-family:Microsoft Yahei;
            font-size:14px;
            color:dimgray;
            font-weight:bold;
        }
        QWidget{
            background:#fff;
        }
        QLineEdit{
            border:1px solid #B5ADAD;
            font-family:Microsoft Yahei;
            font-size:13px;
            color:gray;
        }
        QScrollArea{
            border:1px solid #B5ADAD;
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

        QScrollBar:horizontal
        {
            border-radius:7px;  
            background:#f1f1f1; 
            padding-left:14px;  
            padding-right:14px;  
        }
        QScrollBar::handle:horizontal
        {
            background:#C4CAD0; 
            border-radius:6px;  
            margin-top:2px;  
            margin-bottom:2px;  
        }
        QScrollBar::handle:horizontal:hover
        {
            background:gray;
            border-radius:6px;
        }
        QScrollBar::add-line:horizontal
        {
            height:14px;width:8px;  
            image:url('');  
        }
        QScrollBar::sub-line:horizontal
        {
            height:14px;width:8px;
            image:url('');  
        }
        QScrollBar::add-line:horizontal:hover
        {
            height:14px;width:8px;
            image:url('');
            subcontrol-position:right;
        }
        QScrollBar::sub-line:horizontal:hover
        {
            height:14px;width:8px;
            image:url('');  
            subcontrol-position:left;
        }
        QScrollBar::add-page:horizontal
        {
            background:#f1f1f1;
        }
        QScrollBar::sub-page:horizontal
        {
            background:#f1f1f1; 
        }
        """

class ImgObject(object):

    def __init__(self,path):
        self.filepath=path
        self.filename=os.path.basename(self.filepath)

        config = configparser.ConfigParser()
        config.read("init.ini", encoding="utf8")

        f= open(self.filepath, 'rb')
        tags = exifread.process_file(f)

        timeinfo=None

        if 'EXIF DateTimeOriginal' in tags.keys():
            timestr=tags['EXIF DateTimeOriginal'].printable
            imgctime=time.strptime(tags['EXIF DateTimeOriginal'].printable, "%Y:%m:%d %H:%M:%S")
            timeinfo =[imgctime.tm_year,imgctime.tm_mon,imgctime.tm_mday,imgctime.tm_hour,imgctime.tm_min,imgctime.tm_sec]
        else:
            creatTimeStamp = os.path.getctime(self.filepath)
            timeStruct = time.localtime(creatTimeStamp)
            timeinfo = time.strftime('%Y %m %d %H %M %S', timeStruct).split(' ')
        format = config.get("IMG","textformat")
        format = format.replace('{year}', str(timeinfo[0]))
        format = format.replace('{month}', str(timeinfo[1]))
        format = format.replace('{day}', str(timeinfo[2]))
        format = format.replace('{hour}', str(timeinfo[3]))
        format = format.replace('{minute}', str(timeinfo[4]))
        format = format.replace('{second}', str(timeinfo[5]))
        format = format.replace('{name}', self.filename.split('.')[0])
        self.text=format
        self.textsize = int(config.get("IMG", "textsize"))
        self.textoffset = int(config.get("IMG", "textoffset"))

        self.colorr = int(config.get("IMG", "textcolorr"))
        self.colorg = int(config.get("IMG", "textcolorg"))
        self.colorb = int(config.get("IMG", "textcolorb"))

class ImgProcessWidget(QWidget):

    def __init__(self,fWindow):
        super().__init__()
        self.fWindow=fWindow

        self.initData()

        self.initUI()

    def initData(self):
        self.filelist = []
        self.fileindex=-1

    def initUI(self):
        self.setStyleSheet(MAIN_STYLE)

        self.imgLabel=QLabel()
        self.imgLabel.resize(200,200)
        self.imgLabel.setText("请导入图片")
        self.imgLabel.setAlignment(Qt.AlignCenter)

        self.sa_img = QScrollArea()
        self.sa_img.setStyleSheet(SCROLLAREA_STYLE)
        self.sa_img.setWidget(self.imgLabel)
        self.sa_img.setAlignment(Qt.AlignCenter)

        self.currentFilePathLabel = QLabel()
        self.currentFilePathLabel.setAlignment(Qt.AlignCenter)
        self.currentFilePathLabel.setFixedHeight(30)

        self.btn_last_img = QPushButton("<")
        self.btn_last_img.setFixedSize(30, 30)
        self.btn_last_img.setStatusTip('加载上一张图片')
        self.btn_last_img.clicked.connect(self.on_btn_last_img_clicked)

        self.btn_next_img = QPushButton(">")
        self.btn_next_img.setFixedSize(30, 30)
        self.btn_next_img.setStatusTip('加载下一张图片')
        self.btn_next_img.clicked.connect(self.on_btn_next_img_clicked)

        currentFilePathLayout = QHBoxLayout()
        currentFilePathLayout.setContentsMargins(0, 2, 0, 0)
        currentFilePathLayout.setSpacing(5)
        currentFilePathLayout.addWidget(self.btn_last_img)
        currentFilePathLayout.addWidget(self.currentFilePathLabel)
        currentFilePathLayout.addWidget(self.btn_next_img)

        self.label_textinfo = QLabel('标注文本:')
        self.label_textinfo.setFixedSize(60, 20)
        self.label_textinfo.setAlignment(Qt.AlignLeft)

        self.lineedit_textinfo = QLineEdit()
        self.lineedit_textinfo.setFixedHeight(30)
        self.lineedit_textinfo.textChanged.connect(self.on_textinfo_changed)

        layout_textinfo = QHBoxLayout()
        layout_textinfo.setContentsMargins(0, 5, 0, 0)
        layout_textinfo.setSpacing(5)
        layout_textinfo.addWidget(self.label_textinfo)
        layout_textinfo.addWidget(self.lineedit_textinfo)

        self.label_textsize = QLabel('文本大小:')
        self.label_textsize.setFixedSize(60, 30)
        self.label_textsize.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.spinbox_textsize = QSpinBox()
        self.spinbox_textsize.setFixedSize(50, 22)
        self.spinbox_textsize.setAlignment(Qt.AlignCenter)
        self.spinbox_textsize.setMinimum(1)
        self.spinbox_textsize.setMaximum(200)
        self.spinbox_textsize.valueChanged.connect(self.on_spinbox_textsize_changed)

        self.label_textoffset = QLabel('文本垂直偏移量:')
        self.label_textoffset.setFixedSize(100, 30)
        self.label_textoffset.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.spinbox_textoffset = QSpinBox()
        self.spinbox_textoffset.setFixedSize(50, 22)
        self.spinbox_textoffset.setAlignment(Qt.AlignCenter)
        self.spinbox_textoffset.setMinimum(-20)
        self.spinbox_textoffset.setMaximum(100)
        self.spinbox_textoffset.valueChanged.connect(self.on_spinbox_textoffset_changed)

        self.label_textcolor = QLabel('文本颜色:')
        self.label_textcolor.setFixedSize(60, 30)
        self.label_textcolor.setAlignment(Qt.AlignLeft | Qt.AlignCenter)

        self.label_textcolor_example = QLabel()
        self.label_textcolor_example.setFixedSize(100, 30)
        self.label_textcolor_example.setStyleSheet(
            "background-color:#fff;border:1px solid #B5ADAD;")

        self.colorDialogBtn = QPushButton("选择颜色")
        self.colorDialogBtn.setFixedSize(60, 30)
        self.colorDialogBtn.clicked.connect(self.on_colorDialogBtn_clicked)

        layout_textsetting = QHBoxLayout()
        layout_textsetting.setContentsMargins(0, 5, 0, 0)
        layout_textsetting.setSpacing(5)
        layout_textsetting.addWidget(self.label_textsize)
        layout_textsetting.addWidget(self.spinbox_textsize)
        layout_textsetting.addWidget(self.label_textoffset)
        layout_textsetting.addWidget(self.spinbox_textoffset)
        layout_textsetting.addWidget(self.label_textcolor)
        layout_textsetting.addWidget(self.label_textcolor_example)
        layout_textsetting.addWidget(self.colorDialogBtn)
        layout_textsetting.addStretch()

        self.btn_inport_img = QPushButton("导入图片")
        self.btn_inport_img.setFixedHeight(30)
        self.btn_inport_img.clicked.connect(self.on_btn_inport_clicked)

        self.btn_outport_img = QPushButton("保存图片")
        self.btn_outport_img.setFixedHeight(30)
        self.btn_outport_img.clicked.connect(self.on_btn_outport_clicked)

        inoutPortLayout = QHBoxLayout()
        inoutPortLayout.setContentsMargins(0, 2, 0, 0)
        inoutPortLayout.setSpacing(5)
        inoutPortLayout.addWidget(self.btn_inport_img)
        inoutPortLayout.addWidget(self.btn_outport_img)

        layout=QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.sa_img)
        layout.addLayout(currentFilePathLayout)
        layout.addLayout(layout_textinfo)
        layout.addLayout(layout_textsetting)
        layout.addLayout(inoutPortLayout)

        self.setLayout(layout)

    def on_btn_last_img_clicked(self):
        if self.fileindex == -1:
            self.fWindow.statusBar().showMessage('请先导入图片!')
            return
        if self.fileindex == 0:
            self.fWindow.statusBar().showMessage('这是第一张图片!')
            return

        self.fileindex -= 1
        self.showImageFile()

    def on_btn_next_img_clicked(self):
        if self.fileindex == -1:
            self.fWindow.statusBar().showMessage('请先导入图片!')
            return
        if self.fileindex == len(self.filelist) - 1:
            self.fWindow.statusBar().showMessage('这是最后一张图片!')
            return

        self.fileindex += 1
        self.showImageFile()

    def on_btn_inport_clicked(self):
        pathlist = QFileDialog.getOpenFileNames(self, "打开文件", "./",
                                                "图片文件(*.jpg *.jpeg *.png)")[0]
        if len(pathlist)>0:
            self.fWindow.statusBar().showMessage('成功添加{}张图片。'.format(len(pathlist)))
            self.fileindex=0
            self.filelist.clear()
            for i in pathlist:
                self.filelist.append(ImgObject(i))
            self.showImageFile()

    def on_btn_outport_clicked(self):
        if len(self.filelist)==0:
            self.fWindow.statusBar().showMessage('请先导入图片!')
            return

        self.fWindow.statusBar().showMessage('开始保存!')

        config = configparser.ConfigParser()
        config.read("init.ini", encoding="utf8")
        outportPath=config.get("IMG",'imgsavepath')
        
        if not os.path.exists(outportPath):
            os.makedirs(outportPath)

        for i in self.filelist:
            # img=QImage(i)
            cvimg = self.cv_imread(i.filepath,1)
            img = self.CVMat2QImage(cvimg)
            img = self.drawImage(img, i.text,i.textsize,i.textoffset,
                           i.colorr,i.colorg,i.colorb)
            #img.save(outportPath+'/'+i.filename.split('.')[0]+'.png')
            pimg=ImageQt.fromqimage(img)
            pimg.save(outportPath+'/'+i.filename)

        self.fWindow.statusBar().showMessage('保存结束!')

    def on_textinfo_changed(self):
        if(self.fileindex>=0):
            self.filelist[self.fileindex].text=self.lineedit_textinfo.text()
            self.showImageFile()

    def on_colorDialogBtn_clicked(self):
        if (self.fileindex < 0):
            return
        col = QColorDialog.getColor()
        self.filelist[self.fileindex].colorr = col.red()
        self.filelist[self.fileindex].colorg = col.green()
        self.filelist[self.fileindex].colorb = col.blue()
        self.label_textcolor_example.setStyleSheet(
            "background-color:rgb({},{},{});border:1px solid #B5ADAD;".format(col.red(), col.green(), col.blue()))
        self.showImageFile()

    def on_spinbox_textsize_changed(self):
        if (self.fileindex < 0):
            return
        self.filelist[self.fileindex].textsize=self.spinbox_textsize.value()
        self.showImageFile()

    def on_spinbox_textoffset_changed(self):
        if (self.fileindex < 0):
            return
        self.filelist[self.fileindex].textoffset=self.spinbox_textoffset.value()
        self.showImageFile()

    def showImageFile(self):
        self.currentFilePathLabel.setText("{} ({}/{})".format(self.filelist[self.fileindex].filename,self.fileindex+1,len(self.filelist)))
        self.lineedit_textinfo.setText(self.filelist[self.fileindex].text)
        self.label_textcolor_example.setStyleSheet(
            "background-color:rgb({},{},{});border:1px solid #B5ADAD;".format(self.filelist[self.fileindex].colorr, self.filelist[self.fileindex].colorg, self.filelist[self.fileindex].colorb))
        self.spinbox_textsize.setValue(self.filelist[self.fileindex].textsize)
        self.spinbox_textoffset.setValue(self.filelist[self.fileindex].textoffset)
        #img=QImage(self.filelist[self.fileindex].filepath)
        cvimg=self.cv_imread(self.filelist[self.fileindex].filepath,1)
        img=self.CVMat2QImage(cvimg)
        img=self.drawImage(img,self.filelist[self.fileindex].text,self.filelist[self.fileindex].textsize,self.filelist[self.fileindex].textoffset,
                           self.filelist[self.fileindex].colorr,self.filelist[self.fileindex].colorg,self.filelist[self.fileindex].colorb)
        self.imgLabel.resize(img.size())
        self.imgLabel.setPixmap(QPixmap(img))

    def drawImage(self,img,info,fontsize,offset,r,g,b):
        w, h = img.width(), img.height()
        painter=QPainter()
        painter.begin(img)
        painter.setPen(QColor(r,g,b))
        painter.setFont(QFont('SimSun',fontsize))
        painter.drawText(QRect(0,h*0.8-h*offset/100,w,h*0.2),Qt.AlignCenter,info)
        painter.end()
        return img

    def cv_imread(self,filePath="", flags=-1):
        cv_img = cv2.imdecode(numpy.fromfile(filePath, dtype=numpy.uint8), flags)
        return cv_img

    def cv_imwrite(self,cvimg,filepath):
        ext='.'+filepath.split('.')[-1]
        cv2.imencode(ext, cvimg)[1].tofile(filepath)

    def CVMat2QImage(self,cv_image):
        height, width, bytesPerComponent = cv_image.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB, cv_image)
        qimg = QImage(cv_image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        return qimg

    def QImage2CVMat(self,qimg):
        tmp = qimg

        # 使用numpy创建空的图象
        cv_image = numpy.zeros((tmp.height(), tmp.width(), 3), dtype=numpy.uint8)

        for row in range(0, tmp.height()):
            for col in range(0, tmp.width()):
                r = qRed(tmp.pixel(col, row))
                g = qGreen(tmp.pixel(col, row))
                b = qBlue(tmp.pixel(col, row))
                cv_image[row, col, 0] = r
                cv_image[row, col, 1] = g
                cv_image[row, col, 2] = b
        return cv_image