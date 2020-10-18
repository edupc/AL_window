from untitled import Ui_MainWindow, creat
import sys , os
from PyQt5 import QtWidgets, QtGui#視窗類型,圖片
import globals_var as gvar
from PyQt5.QtWidgets import QMessageBox, QAbstractItemView, QTableWidgetItem
import Window_Catia as wc
import string,datetime
from datetime import datetime,timezone,timedelta
import win32com.client as win32


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_setup.clicked.connect(self.open)
        self.ui.pushButton_start.clicked.connect(self.create_window)
        self.ui.label.setPixmap(QtGui.QPixmap(BASE_DIR + "\\mprdc_logo.png"))
        self.ui.label.setScaledContents(True)
        self.setWindowIcon(QtGui.QIcon(BASE_DIR + "\\ico.ico"))
        self.ui.pushButton_route.clicked.connect(self.save_file_root)
        self.ui.pushButton_catiastart.clicked.connect(wc.start_CATIA)

    def save_file_root(self):
        #directory 變數名稱
        self.route = QtWidgets.QFileDialog.getExistingDirectory(None,
                                                                    "選取資料夾")
        self.ui.lineEdit_file_root.setText(self.route)
    def create_window(self):
        print(gvar.width, gvar.height)
        self.env = wc.set_CATIA_workbench_env()
        self.env.Generative_Sheetmetal_Design()
        wc.part_open("following", system_root+"\\big_window")
        wc.Sideplate_param_change("width", gvar.width)
        wc.part_open("left", system_root+"\\big_window")
        wc.Sideplate_param_change("height", gvar.height)
        wc.part_open("right", system_root+"\\big_window")
        wc.Sideplate_param_change("height", gvar.height)
        wc.part_open("top", system_root+"\\big_window")
        wc.Sideplate_param_change("width", gvar.width)
        if self.route == '':
            gvar.full_save_dir = wc.save_dir('C:\\Users\\PDAL-BM-1\\Desktop')
        else:
            gvar.full_save_dir = wc.save_dir(self.route)
        self.full_save_dir = gvar.full_save_dir
        print("%s" % self.full_save_dir)
        self.catia_save = ['top', 'right', 'following', 'left']
        self.small_catia_save = ['small_top', 'small_left', 'small_right', 'small_following']
        self.small2_catia_save = ['small2_following', 'small2_left', 'small2_top', 'small2_right']
        for item in self.catia_save:
            wc.saveas_close(self.full_save_dir, item, '.CATPart')
        wc.open_assembly()
        wc.assembly_open_file(self.full_save_dir, "following", 0)
        wc.assembly_open_file(self.full_save_dir, "left", 0)
        wc.assembly_open_file(self.full_save_dir, "right", 0)
        wc.assembly_open_file(self.full_save_dir, "top", 0)
        wc.saveas_specify_target(self.full_save_dir,"following",'CATPart')
        wc.saveas_specify_target(self.full_save_dir,"left",'CATPart')
        wc.saveas_specify_target(self.full_save_dir,"right",'CATPart')
        wc.saveas_specify_target(self.full_save_dir,"top",'CATPart')
        wc.show("following.1")
        wc.show("left.1")
        wc.show("right.1")
        wc.show("top.1")
        wc.add_offset_assembly("left", "top", gvar.width, "yz plane")  # 偏移組合(零件一,零件二,距離,元素)
        wc.add_offset_assembly("left", "top", -gvar.height + 300, "xy plane")
        wc.add_offset_assembly("left", "top", 0, "zx plane")
        wc.add_offset_assembly("right", "top", -gvar.width, "yz plane")
        wc.add_offset_assembly("right", "top", -gvar.height + 300, "xy plane")
        wc.add_offset_assembly("right", "top", 0, "zx plane")
        wc.add_offset_assembly("following", "top", 0, "yz plane")
        wc.add_offset_assembly("following", "top", (-2 * gvar.height) + 45, "xy plane")
        wc.add_offset_assembly("following", "top", 0, "zx plane")
        wc.saveas(self.full_save_dir, 'Product', '.CATProduct')
        print('Saved as CATProduct...')

        wc.part_open("small_top", system_root + "\\smalll_window")
        wc.Sideplate_param_change("height", gvar.small_height)  # 172.5
        wc.part_open("small_left", system_root + "\\smalll_window")
        wc.Sideplate_param_change("width", gvar.small_width)  # 255
        wc.part_open("small_right", system_root + "\\smalll_window")
        wc.Sideplate_param_change("width", gvar.small_width)  # 255
        wc.part_open("small_following", system_root + "\\smalll_window")
        wc.Sideplate_param_change("height", gvar.small_height)  # 172.5
        # wc.full_save_dir = self.save_dir('C:\\Users\\PDAL-BM-1\\Desktop')
        print("%s" % self.full_save_dir)
        for item in self.small_catia_save:
            wc.saveas_close(self.full_save_dir, item, '.CATPart')
        wc.open_assembly()
        wc.assembly_open_file(self.full_save_dir, "small_top", 0)
        wc.assembly_open_file(self.full_save_dir, "small_left", 0)
        wc.assembly_open_file(self.full_save_dir, "small_right", 0)
        wc.assembly_open_file(self.full_save_dir, "small_following", 0)
        wc.saveas_specify_target(self.full_save_dir, "small_top", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "small_left", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "small_right", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "small_following", 'CATPart')
        wc.show("Part3.1")
        wc.show("Part4.1")
        wc.show("Part8.1")
        wc.show("Part9.1")
        wc.add_offset_assembly("Part3", "Part9", (-gvar.small_width * 2) + 50.99 + 10.105,
                            "xy plane")  # 偏移組合(零件一,零件二,距離,元素)
        wc.add_offset_assembly("Part3", "Part9", 0, "yz plane")
        wc.add_offset_assembly("Part3", "Part9", 0, "zx plane")
        wc.add_offset_assembly("Part9", "Part4", gvar.small_height, "yz plane")  # 變數.一半的h
        wc.add_offset_assembly("Part9", "Part4", gvar.small_width - 12.69, "xy plane")  # 變數.w-12.69
        wc.add_offset_assembly("Part9", "Part4", 0, "zx plane")
        wc.add_offset_assembly("Part4", "Part8", -gvar.small_height * 2, "yz plane")  # 變數
        wc.add_offset_assembly("Part4", "Part8", 0, "xy plane")
        wc.add_offset_assembly("Part4", "Part8", 0, "zx plane")
        wc.saveas(self.full_save_dir, 'Product1', '.CATProduct')
        print('Saved as CATProduct...')

        wc.part_open("small2_following", system_root + "\\small2_window")
        wc.Sideplate_param_change("height", gvar.small_height)  # height343
        wc.part_open("small2_left", system_root + "\\small2_window")
        wc.Sideplate_param_change("width", gvar.small2_width)  # width267.5
        wc.part_open("small2_top", system_root + "\\small2_window")
        wc.Sideplate_param_change("height", gvar.small_height)  # height343
        wc.part_open("small2_right", system_root + "\\small2_window")
        wc.Sideplate_param_change("width", gvar.small2_width)  # width267.5
        # wc.full_save_dir = self.save_dir('C:\\Users\\PDAL-BM-1\\Desktop')
        print("%s" % self.full_save_dir)
        for item in self.small2_catia_save:
            wc.saveas_close(self.full_save_dir, item, '.CATPart')
        wc.open_assembly()
        wc.assembly_open_file(self.full_save_dir, "small2_following", 0)
        wc.assembly_open_file(self.full_save_dir, "small2_left", 0)
        wc.assembly_open_file(self.full_save_dir, "small2_top", 0)
        wc.assembly_open_file(self.full_save_dir, "small2_right", 0)
        wc.saveas_specify_target(self.full_save_dir, "small2_following", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "small2_left", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "small2_top", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "small2_right", 'CATPart')
        wc.show("Part1.1")  # 更訂patt名稱
        wc.show("Part2.1")  # 更訂patt名稱
        wc.show("Part3.1")  # 更訂patt名稱
        wc.show("Part5.1")  # 更訂patt名稱
        wc.add_offset_assembly("Part3", "Part1", -gvar.small2_width * 2 + 48, "xy plane")  # 變數.
        wc.add_offset_assembly("Part1", "Part3", 0, "yz plane")
        wc.add_offset_assembly("Part1", "Part3", 0, "zx plane")
        wc.add_offset_assembly("Part2", "Part1", gvar.small_height, "yz plane")  # 變數.
        wc.add_offset_assembly("Part2", "Part1", -gvar.small2_width, "xy plane")  # 變數.
        wc.add_offset_assembly("Part2", "Part1", 0, "zx plane")
        wc.add_offset_assembly("Part5", "Part1", -gvar.small_height, "yz plane")  # 變數.
        wc.add_offset_assembly("Part5", "Part1", -gvar.small2_width, "xy plane")
        wc.add_offset_assembly("Part5", "Part1", 0, "zx plane")
        wc.saveas(self.full_save_dir, 'Product2', '.CATProduct')
        print('Saved as CATProduct...')

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
        self.ui.pushButton_setup.clicked.connect(self.set_ok)
        #--------------圖片
        self.ui.label_image.setPixmap(QtGui.QPixmap(BASE_DIR+'\\window_test_image'))
        #--------------根據框框大小縮放圖片
        self.ui.label_image.setScaledContents(True)
        # self.ui.pushButton_setup.clicked.connect(self.set_ok)





    def set_ok(self):
        if self.ui.lineEdit_width.text() != '' and self.ui.lineEdit_height.text() != '':
            gvar.width = float(self.ui.lineEdit_width.text())
            gvar.height = float(self.ui.lineEdit_height.text())
            self.reply = QMessageBox.question(self, "提示", "設定完成", QMessageBox.Yes, QMessageBox.No)
            if self.reply == QMessageBox.Yes:
                self.hide()
                self.window = MainWindow()
                self.window.show()
            elif self.reply == QMessageBox.No:
                QtWidgets.QCloseEvent.ignore()
        else:
            print("err")
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
    system_root = os.path.dirname(os.path.realpath(__file__))
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

