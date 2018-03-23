from windows import Start_Menu, Game_Window
from PyQt5 import QtWidgets, uic, QtGui

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtGui import *

class Main_Controler():
    username = ""
    def __init__(self):
        self.show_start_menu()

    def show_start_menu(self):
        self.start_wnd = Start_Menu.Start_Menu()
        self.start_wnd.show()
        self.start_wnd.user_name.connect(self.set_username)
        self.start_wnd.start_game.connect(self.start_offline_game)

    def set_username(self, name):
        self.username = name

    def start_offline_game(self):
        game_menu = Game_Window.Game_Window(self.username)
        game_menu.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main_Controler()
    sys.exit(app.exec_())


