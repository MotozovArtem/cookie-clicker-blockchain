# -*- coding: utf-8 -*-

import sys

from PyQt5.QtGui import QMovie
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtGui
from multiplayer.models.Blockchain import Blockchain
from multiplayer.models.Miner import Miner
from multiplayer.models.Client import Client

from multiplayer.Multiplayer_window import Game_Window
from submodules.windows_settings import setMoveWindow
from submodules.sys_dialogs import UserDialog
from multiprocessing import Process
import traceback
from multiplayer import Network_manager






def main(pipe, user_nickname):
    app = QtWidgets.QApplication(sys.argv)
    try:
        author = str(user_nickname)
        # TODO: отсюда и до window.show() почему-то очень долго думает
        blockchain = Blockchain(author)
        client = Client(blockchain, pipe)
        miner = Miner(blockchain, client)
        window = Game_Window(10,miner, client)
        setMoveWindow(window)
        window.show()
    except Exception:
        print(traceback.format_exc())
    app.exec_()


