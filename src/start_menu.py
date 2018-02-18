# -*- coding: utf-8 -*-


import sys
from uuid import uuid4

from PyQt5.QtGui import QMovie
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtGui
from blockchain_menu import StartWindow
from submodules.windows_settings import setMoveWindow
from Blockchain import Blockchain
from Miner import Miner
from Client import Client
import asyncore

from blockchain_menu import StartWindow
from submodules.windows_settings import setMoveWindow
from submodules.sys_dialogs import UserDialog
from multiprocessing import Process
import traceback
class Start_Menu(QtWidgets.QMainWindow):

    def __init__(self, parent=None, *args, **kwargs):
        super(QtWidgets.QMainWindow, self).__init__(parent=parent)
        self.setupUi(self)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")

        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        MainWindow.setAttribute(Qt.WA_NoSystemBackground, True)
        MainWindow.setAttribute(Qt.WA_TranslucentBackground, True)

        self.MainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 10, -1)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(1000, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("materials/icons/Close Window_96px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(32, 32))
        self.pushButton.setShortcut("")
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")

        self.pushButton.clicked.connect(self.closeIt)
        self.horizontalLayout.addWidget(self.pushButton, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.main_btn = QtWidgets.QLabel(self.centralwidget)
        self.main_btn.setText("")
        self.main_btn.setAlignment(QtCore.Qt.AlignCenter)
        self.main_btn.setObjectName("main_btn")

        self.main_btn.setPixmap(QtGui.QPixmap("materials/gifs/start_menu.gif"))
        self.main_btn.setObjectName("label")
        self.m = QMovie("materials/gifs/start_menu.gif")
        self.m.setSpeed(100)
        self.m.start()
        self.main_btn.setMovie(self.m)
        self.main_btn.mousePressEvent = self.mouse_pressed

        self.verticalLayout.addWidget(self.main_btn)
        self.footer = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.footer.sizePolicy().hasHeightForWidth())
        self.footer.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS PGothic")
        font.setPointSize(12)
        self.footer.setFont(font)
        self.footer.setStyleSheet("color: rgb(255, 255, 255);\n")
        self.footer.setAlignment(QtCore.Qt.AlignCenter)
        self.footer.setObjectName("footer")
        self.verticalLayout.addWidget(self.footer)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 9)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.footer.setText(_translate("MainWindow", "@Created_by"))

    def mouse_pressed(self, event):
        try:
            # window = StartWindow(self, self.miner)
            while True:
                nick = UserDialog(self).get_answer("Sign up", "Your Nickname:")
                if nick == None or nick == "":
                    continue
                else:
                    self.user_nickname = nick
                    break
            self.author = str(self.user_nickname)  # При перезапуске проги он перегенится. Критично ли это?
            self.blockchain = Blockchain(self.author)

            self.client = Client(self.blockchain)
            print("OOP000")
            self.miner = Miner(self.blockchain, self.client)
            # self.process = Process(target=self.client.main_run)
            # self.process.daemon = True
            # self.process.start()
            # self.process.join()
            # process.join() ??
            print("OOP")
            window = StartWindow(self, self.miner, self.client)
            print("1")
            setMoveWindow(window)
            self.hide()
            window.show()
            # asyncore.loop(600)
        except Exception:
            print(traceback.format_exc())

    def closeIt(self):
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    try:
        window = Start_Menu()
        setMoveWindow(window)
        window.show()
    except Exception as e:
        print(e)
    sys.exit(app.exec_())
