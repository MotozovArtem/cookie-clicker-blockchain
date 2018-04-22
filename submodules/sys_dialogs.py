from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from .windows_settings import setMoveWindow


class ExceptionDialog(QtWidgets.QMessageBox):

    def __init__(self,parent,comment_to_error, error_text):
        super(QtWidgets.QMessageBox, self).__init__(parent)
        self.setIconPixmap("materials/icons/Exception_32px.png")
        self.setStyleSheet("background-color:RGB(0,0,0); color:#FF0000")
        self.setWindowTitle("Error")
        self.setText(comment_to_error)
        self.setDetailedText(str(error_text))
        self.addButton(QMessageBox.Ok)


class InfoDialog(QtWidgets.QMessageBox):

    def __init__(self, parent, title, info_comment):
        super(QtWidgets.QMessageBox, self).__init__(parent)
        self.setStyleSheet("background-color:RGB(0,0,0); color:#FFF")
        self.setWindowModality(1)
        self.setIconPixmap(QtGui.QPixmap("materials/icons/Info_32px.png"))
        self.setWindowTitle(title)
        self.setText(info_comment)
        self.addButton(QMessageBox.Ok)



class WarningDialog(QtWidgets.QMessageBox):

    def __init__(self, parent, title, info_comment):
        super(QtWidgets.QMessageBox, self).__init__(parent)
        self.setStyleSheet("background-color:RGB(0,0,0); color:#FFFF00")
        self.setWindowModality(1)
        self.setIconPixmap(QtGui.QPixmap("materials/icons/Warning_32px.png"))
        self.setWindowTitle(title)
        self.setText(info_comment)
        self.addButton(QMessageBox.Ok)


class UserDialog(QtWidgets.QInputDialog):

    def __init__(self,  parent):
        super(QtWidgets.QDialog, self).__init__(parent)
        self.parent = parent
        self.setStyleSheet("background-color:RGB(0,0,0); color:#FF0000;")
        self.setWindowModality(1)


    def get_answer(self,title, question):
        self.parent.setStyleSheet("background-color:RGB(0,0,0); color:#FF0000")
        # self.setStyleSheet("background-color:RGB(0,0,0); color:#FF0000")
        text, ok = self.getText(self.parent, title,question)
        if ok:
            return text
        else:
            return None

    # icon = UserDialog().get_answer("Question", "Nick:")

