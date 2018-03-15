import sys
sys.path.append("./")

from src.start_menu import gui_main
from multiprocessing import Process, Pipe
import src.network as network

if __name__ == "__main__":
    app_gui = None
    net_pipe, gui_pipe = Pipe()
    network_process = Process(target=network.main, args=(net_pipe,))
    app_gui = Process(target=gui_main, args=(gui_pipe,))
    app_gui.start()
    network_process.start()
    while app_gui.is_alive():
        pass

    network_process.terminate()
