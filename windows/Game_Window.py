# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, uic, QtGui

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtGui
import materials as resources
from PyQt5.QtGui import *
from submodules.windows_settings import setMoveWindow
from submodules.Incremental_Thread import  MyThread
rel_materials_path = "" # Ко всем материалам образаться rel_materials_path + путь к материалы

class Game_Window(QtWidgets.QMainWindow):

    clicks = 0
    boost_increment = 0.2
    boost_cost = 10
    boost_count = 0
    thread = None
    mutex = QtCore.QMutex()

    def __init__(self, username=None, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        setMoveWindow(self)


        self.MainWindow = uic.loadUi(rel_materials_path + resources.Game_Window_Resources.form, self)

        self.user_name.setStyleSheet("color: #fff;");
        self.user_name.setText(username)


        self.MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        self.MainWindow.setAttribute(Qt.WA_NoSystemBackground, True)
        self.MainWindow.setAttribute(Qt.WA_TranslucentBackground, True)

        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.num_of_clicks.setStyleSheet("color: rgb(255, 255, 255);")
        self.num_of_clicks.setText("0")
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_5.setText("Boost Cost")
        self.cost_of_boost.setStyleSheet("color: rgb(255, 255, 255);")
        self.cost_of_boost.setText(str(self.boost_cost))
        self.pushButton.setStyleSheet("color: rgb(100, 100, 100);")
        self.pushButton.setEnabled(False)

        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(rel_materials_path + resources.Game_Window_Resources.reset_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reset.setIcon(icon3)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(rel_materials_path + resources.Game_Window_Resources.statistic_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stat.setIcon(icon)

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(rel_materials_path + resources.Game_Window_Resources.info_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.info.setIcon(icon1)

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(rel_materials_path + resources.Game_Window_Resources.close_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exit.setIcon(icon2)
        self.exit.setIconSize(QtCore.QSize(32, 32))

        self.label.setPixmap(QtGui.QPixmap(rel_materials_path + resources.Game_Window_Resources.game_menu_gif))
        self.m = QMovie(rel_materials_path + resources.Game_Window_Resources.game_menu_gif)
        self.m.setSpeed(990)
        self.m.start()
        self.m.setPaused(True)
        self.label.setMovie(self.m)
        self.label.mousePressEvent = self.mouse_pressed
        self.m.frameChanged.connect(self.finish)
        self.exit.clicked.connect(self.closeIt)

        self.pushButton.clicked.connect(self.boost)

    def mouse_pressed(self, event):
        try:
            if self.m.state() != 2:
                self.m.start()
            self.user_clicks()
        except Exception as e:
            print(e)

    def user_clicks(self):
        self.mutex.lock()
        self.clicks = self.clicks + 1
        self.clicks = round(self.clicks, 1)
        self.mutex.unlock()
        self.update_clicks()


    def increment_clicks(self,inc):
        self.mutex.lock()
        self.clicks = self.clicks + inc
        self.clicks = round(self.clicks, 1)
        self.mutex.unlock()
        self.update_clicks()


    def update_clicks(self):
        self.num_of_clicks.setText(str(self.clicks))
        self.check_boost_cond()

    def finish(self, event):
        if self.m.currentFrameNumber() == (self.m.frameCount()-1):
            self.m.stop()

    def check_boost_cond(self):
        if self.boost_cost <= self.clicks:
            self.pushButton.setStyleSheet("color: rgb(255, 255, 255);")
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setStyleSheet("color: rgb(100, 100, 100);")
            self.pushButton.setEnabled(False)

    def boost(self):

        self.clicks = round(self.clicks - self.boost_cost,1)

        self.update_clicks()
        self.boost_count +=1
        self.boost_cost = self.form_new_boost_cost()
        self.update_boost_cost()
        self.start_thread()
        self.boost_increment += 0.2

    def update_boost_cost(self):
        self.cost_of_boost.setText(str(self.boost_cost))

    def start_thread(self):
        self.thread = MyThread(self.boost_increment)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.thread.increment)
        self.thread.increment_signal.connect(self.increment_clicks)
        self.timer.start(1000)
        self.thread.start()

        # if self.thread != None:
        #     if (self.thread.isRunning() == False):
        #         self.thread = MyThread(self.boost_increment)
        #         self.timer = QtCore.QTimer()
        #         self.timer.timeout.connect(self.thread.increment)
        #         self.thread.increment_signal.connect(self.increment_clicks)
        #         self.timer.start(1000)
        #         self.thread.start()
        #     else:
        #         self.thread.terminate()
        #         self.start_thread()
        # else:
        #     self.thread = MyThread(self.boost_increment)
        #     self.timer = QtCore.QTimer()
        #     self.timer.timeout.connect(self.thread.increment)
        #     self.thread.increment_signal.connect(self.increment_clicks)
        #     self.timer.start(1000)
        #     self.thread.start()


    def form_new_boost_cost(self):
        return round((self.boost_cost * 1.07**(self.boost_count+1)),1)

    def closeIt(self):
        self.close()

if __name__ == "__main__":
    import sys

    rel_materials_path = "..//"
    app = QtWidgets.QApplication(sys.argv)
    window = Game_Window()
    setMoveWindow(window)
    window.show()
    sys.exit(app.exec_())
