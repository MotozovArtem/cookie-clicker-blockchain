
from PyQt5 import QtCore

class MyThread(QtCore.QThread):
    increment_signal = QtCore.pyqtSignal(float)

    def __init__(self, inc, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.inc = inc

    def run(self):
        pass

    def increment(self):
        self.increment_signal.emit(self.inc)




if __name__ == "__main__":
    def test(ar):
        print("Num - ", ar)
    from PyQt5 import QtCore, QtWidgets
    import time
    import sys
    th = MyThread(0.5)
    app = QtWidgets.QApplication(th)

    th.increment_signal.connect(test)
    th.start()
    sys.exit(app.exec_())

    # while True:
    #     time.sleep(3)
    #     print("Work")
