from src.start_menu import Process, gui_main
import src.network as network

if __name__ == "__main__":
    app_gui = None
    network_process = Process(target=network.main)
    app_gui = Process(target=gui_main)
    app_gui.start()
    network_process.start()
    while (app_gui.is_alive()):
        pass

    network_process.terminate()