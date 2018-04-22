from windows import Start_Menu, Game_Window
from PyQt5 import QtWidgets, uic, QtGui

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
from multiprocessing import Process, Pipe
from multiplayer import Network_manager, Client_manager
# import sys
# sys.path.append('C:\\Program Files (x86)\\Nmap')
import os
os.environ['PATH'] = os.environ['PATH'] + ';C:\\Program Files (x86)\\Nmap;'
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
        game_menu = Game_Window.Game_Window(20, self.username)
        game_menu.show()
        game_menu.multiplayer_game_start.connect(self.start_online_game)


    def start_online_game(self):
        try:
            net_pipe, gui_pipe = Pipe()
            network_process = Process(target=Network_manager.main, args=(net_pipe,))
            app_gui = Process(target=Client_manager.main, args=(gui_pipe, self.username,))
            app_gui.start()
            network_process.start()
            app_gui.join()
            network_process.terminate()
        except Exception as e:
            print(e.__str__())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main_Controler()
    sys.exit(app.exec_())


