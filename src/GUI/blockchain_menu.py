# -*- coding: utf-8 -*-

import sys
from PyQt5.QtGui import QMovie
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtGui

from src.GUI.blockchain_stat import Ui_Form
from src.GUI.submodules.windows_settings import setMoveWindow
from src.GUI.submodules.sys_dialogs import ExceptionDialog, InfoDialog
from src.GUI.submodules.sys_dialogs import UserDialog


from src.Miner import Miner, SuccessException
import threading

class StartWindow(QtWidgets.QMainWindow):

    def __init__(self, parent, miner, client):
        QtWidgets.QMainWindow.__init__(self)
        self.parent = parent
        self.setupUi(self)
        self.miner = miner
        self.client = client
        self.thread = threading.Thread(target=self.show_warning())
        self.thread.daemon = True
        self.thread.start()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setStyleSheet("background-color: rgb(8, 24, 33);")

        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        MainWindow.setAttribute(Qt.WA_NoSystemBackground, True)
        MainWindow.setAttribute(Qt.WA_TranslucentBackground, True)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, 10, 0, -1)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.stat = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stat.sizePolicy().hasHeightForWidth())
        self.stat.setSizePolicy(sizePolicy)
        self.stat.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("materials/icons/Statistics_100px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stat.setIcon(icon)
        self.stat.setIconSize(QtCore.QSize(32, 32))
        self.stat.setFlat(True)
        self.stat.setObjectName("stat")
        self.stat.clicked.connect(self.show_stat)
        self.horizontalLayout_7.addWidget(self.stat)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.info = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info.sizePolicy().hasHeightForWidth())
        self.info.setSizePolicy(sizePolicy)
        self.info.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("materials/icons/Info_100px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.info.setIcon(icon1)
        self.info.setIconSize(QtCore.QSize(32, 32))
        self.info.setFlat(True)
        self.info.clicked.connect(self.show_info)
        self.info.setObjectName("info")
        self.horizontalLayout_7.addWidget(self.info)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem2)
        self.exit = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exit.sizePolicy().hasHeightForWidth())
        self.exit.setSizePolicy(sizePolicy)
        self.exit.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("materials/icons/Close Window_96px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exit.setIcon(icon2)
        self.exit.setIconSize(QtCore.QSize(32, 32))
        self.exit.setFlat(True)
        self.exit.setObjectName("exit")
        self.exit.clicked.connect(self.closeIt)
        self.horizontalLayout_7.addWidget(self.exit)
        self.horizontalLayout_7.setStretch(1, 1)
        self.horizontalLayout_7.setStretch(3, 1)
        self.horizontalLayout_7.setStretch(4, 12)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setGeometry(QtCore.QRect(130, 20, 601, 531))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("materials/gifs/mining.gif"))
        self.label.setObjectName("label")

        self.m = QMovie("materials/gifs/mining.gif")
        self.m.setSpeed(990)
        self.m.start()
        self.m.setPaused(True)
        self.label.setMovie(self.m)
        self.label.mousePressEvent = self.mouse_pressed
        self.m.frameChanged.connect(self.finish)

        self.horizontalLayout_12.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setContentsMargins(-1, -1, -1, 30)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem3 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem3)
        self.reset = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reset.sizePolicy().hasHeightForWidth())
        self.reset.setSizePolicy(sizePolicy)
        self.reset.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("materials/icons/Reset_104px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reset.setIcon(icon3)
        self.reset.setIconSize(QtCore.QSize(20, 20))
        self.reset.setFlat(True)
        self.reset.setObjectName("reset")
        self.horizontalLayout_11.addWidget(self.reset)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem4)
        self.horizontalLayout_11.setStretch(1, 1)
        self.horizontalLayout_11.setStretch(2, 19)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 7)
        self.verticalLayout.setStretch(2, 2)
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

    def show_stat(self):
        window = Ui_Form(self, self.miner.blockchain.chain)  # отсюда вызываю функция получения статистики по блокчейну
        setMoveWindow(window)  # в blockchain_stat в функции get_block_desc показано как я представляю структуру блока
        self.hide()
        window.show()

    def show_info(self):
        dialog = InfoDialog(self.label, "Info",
                            "A blockchain - a continuously growing list of records, called blocks, which are linked and secured using cryptography.")
        dialog.show()

    def ask_for_comment(self):  # User`ve made block and we ask for comment
        self.client.send_notifi()
        comment = UserDialog(self).get_answer("Proved!!!",
                                              "Congratulations!\nYou mined the block.\n Please enter your comment:")
        # self.client.handle_write()
        if comment:
            self.miner.update(comment)
        else:
            self.miner.update("Default comment")
        # TODO: Нужно ещё проверить на пустой комментарий

    def show_warning(self):  # Show user that someone else has mined the block
        while True:
            if self.client.notifi_flag == True:
                dialog = InfoDialog(self.label, "Warning", "Your opponents have already mined the block!!!")
                dialog.show()



    def mouse_pressed(self, *args):
        """Здесь фиксируется клик пользователя"""
        if self.m.state() != 2:
            self.m.start()
        try:
            self.miner.click()
        except SuccessException:
            self.ask_for_comment()

    def finish(self, *args):
        if self.m.currentFrameNumber() == (self.m.frameCount() - 1):
            self.m.stop()

    def closeIt(self):
        self.parent.show()
        self.close()
