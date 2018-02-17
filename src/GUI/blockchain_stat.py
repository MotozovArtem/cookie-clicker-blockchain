# -*- coding: utf-8 -*-



from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtGui
from graphviz import Digraph
from PyQt5.QtOpenGL import *
from PyQt5.QtGui import *
import os
import sys
import sys
"""
(Для Windows)Прежде чем запускать этот код вы должны установить библиотеку graphviz
через pip + graphviz-2.38.msi на сайте https://graphviz.gitlab.io/_pages/Download/Download_windows.html
и прописать путь к папке bin.

(Для Linux)Нуу либо тоже самое либо выплывайте сами...
"""

os.environ["PATH"] += os.pathsep + "C:\\Program Files (x86)\\Graphviz2.38\\bin\\"  #Волшебная строка после которая сама прописывает вам путь

class Ui_Form(QtWidgets.QWidget):

    def __init__(self, parent, blockchain):
        QtWidgets.QWidget.__init__(self)
        self.parent = parent
        self.setupUi(self)
        self.set_blockchain_graph(blockchain)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1200, 800)
        Form.setStyleSheet("background-color: rgb(0, 0, 0);")
        Form.setWindowFlags(Qt.FramelessWindowHint)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 10, 10, 10)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("materials/icons/Return_104px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.clicked.connect(self.closeIt)
        self.pushButton.setIconSize(QtCore.QSize(32, 32))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 30)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

    def get_block_desc(self, block): #так я вижу структура каждого блока (если вы нет - то измените её здесь или уведомьте меня)
        text = ("  Hash: {0};\n"
                "  Author: {1};\n"
                "  Comment: {2};\n"
                "  Proof: {3};\n"
                "  Date: {4};\n"
                "  Prev_block: {5};").format(block["hash"], block["author"],block["comment"],block["proof"],block["timestamp"],block["previous_hash"],)
        return text

    def set_blockchain_graph(self,blockchain):

        if len(blockchain) !=0:

            dot = Digraph(comment='Blockchain', format="jpg")
            dot.attr(rankdir='LR',size='1200, 800' )

            dot.node(blockchain[0]["hash"],
                     label=self.get_block_desc(blockchain[0]),
                     shape='rectangle')

            for i in range(1,len(blockchain)):
                dot.node(blockchain[i]["hash"],
                         label=self.get_block_desc(blockchain[i]),
                         shape='rectangle')
                dot.edge(blockchain[i-1]["hash"],blockchain[i]["hash"])

            dot.render('materials/graph/output')
            scene = QtWidgets.QGraphicsScene()
            scene.addPixmap(QPixmap("materials/graph/output.jpg"))
            self.graphicsView.setScene(scene)
        else:
            pass


    def closeIt(self):
        self.parent.show()
        self.close()

