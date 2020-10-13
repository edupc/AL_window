from untitled import Ui_MainWindow, creat
import os, sys
from PyQt5 import QtWidgets, QtGui#視窗類型,圖片
import globals_var as gvar
import AL_Window_GUI



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.open)

    def open(self):
        self.hide()#隱藏
        self.window = Create()
        self.window.show()
        print("test")

class Create(QtWidgets.QMainWindow, creat):
    def __init__(self):
        super(Create, self).__init__()#繼承
        self.ui = creat()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.set_ok)
    def set_ok(self):
        gvar.width = self.ui.lineEdit_2.text()
        gvar.height =self.ui.lineEdit_3.text()
        print(gvar.width,gvar.height)
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.window = MainWindow()
        self.window.show()
# class test123(QtWidgets.QMainWindow, creat):
#     def __init__(self):
#         super(test123, self).__init__()#繼承
#         self.ui = creat()
#         self.ui.setupUi(self)
#         self.ui.pushButton.clicked.connect(self.good)
#     def good(self):
#         gvar.width = self.ui.lineEdit_3.text()
#         print(gvar.width)
#     def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
#         self.window = MainWindow()
#         self.window.show()


if __name__ == '__main__' :
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
