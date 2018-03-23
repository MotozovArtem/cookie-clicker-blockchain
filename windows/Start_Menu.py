# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, uic, QtGui

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtGui
import materials as resources
from PyQt5.QtGui import *
from submodules.sys_dialogs import UserDialog
from submodules.windows_settings import setMoveWindow
rel_materials_path = "" # Ко всем материалам образаться rel_materials_path + путь к материалы

class Start_Menu(QtWidgets.QMainWindow):

    user_name = QtCore.pyqtSignal(str)
    start_game = QtCore.pyqtSignal()


    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        setMoveWindow(self)
        self.MainWindow = uic.loadUi(rel_materials_path + resources.Start_Menu_Resources.form, self)

        self.MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        self.MainWindow.setAttribute(Qt.WA_NoSystemBackground, True)
        self.MainWindow.setAttribute(Qt.WA_TranslucentBackground, True)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(rel_materials_path + resources.Start_Menu_Resources.close_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)

        self.main_btn.setPixmap(QtGui.QPixmap(rel_materials_path + resources.Start_Menu_Resources.start_menu_gif))
        self.m = QMovie(rel_materials_path + resources.Start_Menu_Resources.start_menu_gif)
        self.m.setSpeed(100)
        self.m.start()
        self.main_btn.setMovie(self.m)


        self.main_btn.mousePressEvent = self.mouse_pressed
        self.pushButton.clicked.connect(self.closeIt)

    def mouse_pressed(self, event):
        while True:
            nick = UserDialog(self).get_answer("Sign up", "Your Nickname:")
            if nick == None or nick == "":
                continue
            else:
                self.user_name.emit(nick)
                self.start_game.emit()
                self.closeIt()
                break

    def closeIt(self):
        self.MainWindow.close()

if __name__ == "__main__":
    import sys

    rel_materials_path = "..//"
    app = QtWidgets.QApplication(sys.argv)
    window = Start_Menu()
    window.show()
    sys.exit(app.exec_())

