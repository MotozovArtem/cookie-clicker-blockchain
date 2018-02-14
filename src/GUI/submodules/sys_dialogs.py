from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets



class ExceptionDialog(QtWidgets.QDialog):

    def __init__(self,parent,comment_to_error, error_text):
        QtWidgets.QDialog.__init__(parent)

        message_box = QtWidgets.QMessageBox()
        message_box.setIcon(QtWidgets.QMessageBox.Critical)
        message_box.setWindowTitle("Error")
        message_box.setText(comment_to_error)
        message_box.setDetailedText(str(error_text))
        message_box.exec_()


class InfoDialog(QtWidgets.QDialog):

    def __init__(self, parent, info_comment):
        QtWidgets.QDialog.__init__(parent)

        message_box = QtWidgets.QMessageBox()
        message_box.setIcon(QtWidgets.QMessageBox.Information)
        message_box.setWindowTitle("Info")
        message_box.setText(info_comment)
        message_box.addButton(QMessageBox.Ok)
        message_box.exec_()
