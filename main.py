# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file:main.py
@time:2020/4/15 18:48
"""

import sys
import sip

from PyQt5.QtWidgets import QApplication

from MainWindow import MainWindow

def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()