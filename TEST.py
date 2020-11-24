import os
import sys

from PyQt5 import QtWidgets, QtGui,QtCore,Qt
from PyQt5.QtWidgets import QMessageBox, QApplication,QTableWidget,QTableWidgetItem,QAbstractItemView

import Window_Catia as wc
import globals_var as gvar
from untitled import Ui_MainWindow, creat, about
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    # 在這裏的是系統開啟會重新re過一次的動作
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_setup.clicked.connect(self.open)
        self.ui.pushButton_start.clicked.connect(self.create_window)
        self.ui.label.setPixmap(QtGui.QPixmap(BASE_DIR + "\\test.jpg"))
        self.ui.label.setScaledContents(True)
        self.setWindowIcon(QtGui.QIcon(BASE_DIR + "\\icon.ico"))
        self.ui.pushButton_route.clicked.connect(self.save_file_root)
        self.ui.pushButton_catiastart.clicked.connect(wc.start_CATIA)
        self.ui.pushButton_about.clicked.connect(self.open_about)
        self.ui.pushButton_close_all.clicked.connect(self.Close)
        self.route = ''

    # 關閉量測介面
    def Close(self):
        self.close()


    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.reply = QMessageBox.question(self, "警示", "確定離開本系統?\nAre you sure you want to close?", QMessageBox.Yes,
                                          QMessageBox.No)
        if self.reply == QMessageBox.Yes:
            self.close()
        elif self.reply == QMessageBox.No:
            self.window = MainWindow()
            self.window.show()

    # 關閉全系統(強制關閉)
    def onButtonClick(self):
        '''按鈕槽函式封裝'''
        # 獲取訊號傳送物件
        sender = self.sender()
        # 列印訊號傳送物件的文字+列印輸出
        print(sender.text() + '被按下了')
        # 建立QApplication物件並呼叫quit方法
        qApp = QApplication.instance()
        qApp.quit()

    # 儲存路徑
    def save_file_root(self):
        # directory 變數名稱
        self.route = QtWidgets.QFileDialog.getExistingDirectory(None, "選取資料夾")
        self.ui.lineEdit_file_root.setText(self.route)

    # catia執行檔
    def create_window(self):
        print(gvar.width, gvar.height)
        self.env = wc.set_CATIA_workbench_env()
        self.env.Generative_Sheetmetal_Design()
        wc.part_open("following", system_root + "\\big_window")
        wc.Sideplate_param_change("width", gvar.width)
        wc.part_open("left", system_root + "\\big_window")
        wc.Sideplate_param_change("height", gvar.height)
        wc.part_open("right", system_root + "\\big_window")
        wc.Sideplate_param_change("height", gvar.height)
        wc.part_open("top", system_root + "\\big_window")
        wc.Sideplate_param_change("width", gvar.width)
        print(self.route)
        if self.route == '':
            gvar.full_save_dir = wc.save_dir(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
        else:
            gvar.full_save_dir = wc.save_dir(self.route)
        self.full_save_dir = gvar.full_save_dir
        print("%s" % self.full_save_dir)
        self.catia_save = ['top', 'right', 'following', 'left']
        self.small_catia_save = ['small_top', 'small_left', 'small_right', 'small_following', 'wheel_1', 'wheel_2']
        self.small2_catia_save = ['small2_following', 'small2_left', 'small2_top', 'small2_right', 'wheel_3',
                                  'wheel_4']  # ,'wheel_1','wheel_2']
        self.AL_Window = ['Product', 'Product1', 'Product2']
        for item in self.catia_save:
            wc.saveas_close(self.full_save_dir, item, '.CATPart')
        wc.open_assembly()
        wc.assembly_open_file(self.full_save_dir, "following", 0)
        wc.assembly_open_file(self.full_save_dir, "left", 0)
        wc.assembly_open_file(self.full_save_dir, "right", 0)
        wc.assembly_open_file(self.full_save_dir, "top", 0)
        wc.saveas_specify_target(self.full_save_dir, "following", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "left", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "right", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "top", 'CATPart')
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
        # wc.saveas(self.full_save_dir, 'Product', '.CATProduct')
        # print('Saved as CATProduct...')

        # -------------------------------------------------------------------------------------------------------2

        wc.part_open("small_top", system_root + "\\smalll_window")
        wc.Sideplate_param_change("height", gvar.small_height / 2)  # 172.5
        wc.part_open("small_left", system_root + "\\smalll_window")
        wc.Sideplate_param_change("width", gvar.small_width / 2)  # 255
        wc.part_open("small_right", system_root + "\\smalll_window")
        wc.Sideplate_param_change("width", gvar.small_width / 2)  # 255
        wc.part_open("small_following", system_root + "\\smalll_window")
        wc.Sideplate_param_change("height", gvar.small_height / 2)  # 172.5
        wc.part_open("wheel_1", system_root + "\\smalll_window")
        wc.part_open("wheel_2", system_root + "\\smalll_window")
        print("%s" % self.full_save_dir)
        for item in self.small_catia_save:
            wc.saveas_close(self.full_save_dir, item, '.CATPart')
        wc.open_assembly()
        wc.assembly_open_file(self.full_save_dir, "small_top", 0)
        wc.assembly_open_file(self.full_save_dir, "small_left", 0)
        wc.assembly_open_file(self.full_save_dir, "small_right", 0)
        wc.assembly_open_file(self.full_save_dir, "small_following", 0)
        wc.assembly_open_file(self.full_save_dir, "wheel_1", 0)
        wc.assembly_open_file(self.full_save_dir, "wheel_2", 0)
        wc.saveas_specify_target(self.full_save_dir, "small_top", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "small_left", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "small_right", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "small_following", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "wheel_1", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "wheel_2", 'CATPart')
        wc.show("small_top.1")  # small_top
        wc.show("small_left.1")  # small_left
        wc.show("small_right.1")  # small_right
        wc.show("small_following.1")  # small_following
        wc.show("wheel_1.1")
        wc.show("wheel_2.1")
        wc.add_offset_assembly("small_top", "small_left", 0,
                               "last_plane")  # 偏移組合(零件一,零件二,距離,元素)
        wc.add_offset_assembly("small_top", "small_following", 0, "yz plane")
        wc.add_offset_assembly("small_top", "small_following", 0, "zx plane")
        wc.add_offset_assembly("small_following", "small_left", gvar.small_height / 2 - 20.8, "yz plane")  # 變數.一半的h
        wc.add_offset_assembly("small_following", "small_left", 0, "xy plane1")  # 變數.w-12.69
        wc.add_offset_assembly("small_following", "small_left", 0, "zx plane")
        wc.add_offset_assembly("small_left", "small_right", -gvar.small_height + 20.8, "yz plane")  # 變數
        wc.add_offset_assembly("small_left", "small_right", 0, "xy plane")
        wc.add_offset_assembly("small_left", "small_right", 0, "zx plane")
        wc.add_offset_assembly('wheel_1', 'small_following', 0, 'top_Point2')
        wc.add_offset_assembly('wheel_1', 'small_following', 0, 'Plane_wheel_B')
        wc.add_offset_assembly('wheel_2', 'small_following', 0, 'top_Point3')
        wc.add_offset_assembly('wheel_2', 'small_following', 0, 'Plane_wheel_B')
        # wc.saveas(self.full_save_dir, 'Product1', '.CATProduct')
        # print('Saved as CATProduct...')

        # -------------------------------------------------------------------------------------------------------3

        wc.part_open("small2_following", system_root + "\\small2_window")
        wc.Sideplate_param_change("height", gvar.small_height / 2)  # height343
        wc.part_open("small2_left", system_root + "\\small2_window")
        wc.Sideplate_param_change("width", gvar.small2_width / 2)  # width267.5
        wc.part_open("small2_top", system_root + "\\small2_window")
        wc.Sideplate_param_change("height", gvar.small_height / 2)  # height343
        wc.part_open("small2_right", system_root + "\\small2_window")
        wc.Sideplate_param_change("width", gvar.small2_width / 2)  # width267.5
        wc.part_open("wheel_3", system_root + "\\small2_window")
        wc.part_open("wheel_4", system_root + "\\small2_window")
        print("%s" % self.full_save_dir)
        for item in self.small2_catia_save:
            wc.saveas_close(self.full_save_dir, item, '.CATPart')
        wc.open_assembly()
        wc.assembly_open_file(self.full_save_dir, "small2_following", 0)
        wc.assembly_open_file(self.full_save_dir, "small2_left", 0)
        wc.assembly_open_file(self.full_save_dir, "small2_top", 0)
        wc.assembly_open_file(self.full_save_dir, "small2_right", 0)
        wc.assembly_open_file(self.full_save_dir, "wheel_3", 0)
        wc.assembly_open_file(self.full_save_dir, "wheel_4", 0)
        wc.saveas_specify_target(self.full_save_dir, "small2_following", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "small2_left", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "small2_top", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "small2_right", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "wheel_3", 'CATPart')
        wc.saveas_specify_target(self.full_save_dir, "wheel_4", 'CATPart')
        wc.show("small2_following.1")  # small2_following
        wc.show("small2_left.1")  # small2_left
        wc.show("small2_top.1")  # small2_top
        wc.show("small2_right.1")  # small2_right
        wc.show("wheel_3.1")
        wc.show("wheel_4.1")
        wc.add_offset_assembly("small2_top", "small2_following", -gvar.small2_width + 48, "xy plane")  # 變數.
        wc.add_offset_assembly("small2_following", "small2_top", 0, "yz plane")
        wc.add_offset_assembly("small2_following", "small2_top", 0, "zx plane")
        wc.add_offset_assembly("small2_left", "small2_following", gvar.small_height / 2, "yz plane")  # 變數.
        wc.add_offset_assembly("small2_left", "small2_following", -gvar.small2_width / 2, "xy plane")  # 變數.
        wc.add_offset_assembly("small2_left", "small2_following", 0, "zx plane")
        wc.add_offset_assembly("small2_right", "small2_following", -gvar.small_height / 2, "yz plane")  # 變數.
        wc.add_offset_assembly("small2_right", "small2_following", -gvar.small2_width / 2, "xy plane")
        wc.add_offset_assembly("small2_right", "small2_following", 0, "zx plane")
        wc.add_offset_assembly('wheel_3', 'small2_following', 0, 'top_Point2')
        wc.add_offset_assembly('wheel_3', 'small2_following', 0, 'Plane_wheel_A')
        wc.add_offset_assembly('wheel_4', 'small2_following', 0, 'top_Point3')
        wc.add_offset_assembly('wheel_4', 'small2_following', 0, 'Plane_wheel_A')
        # wc.saveas(self.full_save_dir, 'Product2', '.CATProduct')
        # print('Saved as CATProduct...')

        for item in self.AL_Window:
            wc.saveas_close(self.full_save_dir, item, '.CATProduct')
        # -------------------------------------------------------------------------------------------------------組合

        wc.open_assembly()
        wc.assembly_open_file(self.full_save_dir, "Product", 1)
        wc.assembly_open_file(self.full_save_dir, "Product1", 1)
        wc.assembly_open_file(self.full_save_dir, "Product2", 1)
        wc.show_p("Product1.1", "following.1")
        wc.show_p('Product1.1', 'left.1')
        wc.show_p('Product1.1', 'right.1')
        wc.show_p('Product1.1', 'top.1')
        wc.show_p('Product2.1', 'small_top.1')
        wc.show_p('Product2.1', 'small_left.1')
        wc.show_p('Product2.1', 'small_right.1')
        wc.show_p('Product2.1', 'small_following.1')
        wc.show_p('Product2.1', 'wheel_1.1')
        wc.show_p('Product2.1', 'wheel_2.1')
        wc.show_p('Product3.1', 'small2_top.1')
        wc.show_p('Product3.1', 'small2_left.1')
        wc.show_p('Product3.1', 'small2_right.1')
        wc.show_p('Product3.1', 'small2_following.1')
        wc.show_p('Product3.1', 'wheel_3.1')
        wc.show_p('Product3.1', 'wheel_4.1')

        wc.test_2('Product3', 'small2_left', 'Product2', 'small_left', 'Plane_Product_ZY')
        wc.test_2('Product1', 'top', 'Product3', 'small2_following', 'Plane_wheel_A')
        wc.test_2('Product2', 'small_following', 'Product1', 'top', 'Plane_wheel_B')
        wc.test_2('Product1', 'top', 'Product2', 'wheel_1', 'Plane_end_B')
        wc.test_2('Product1', 'top', 'Product3', 'wheel_3', 'Plane_end_A')
        wc.test_2('Product1', 'left', 'Product2', 'small_right', 'Plane_set_end')
        wc.saveas(self.full_save_dir, 'AL_Window', '.CATProduct')
        print('Saved as CATProduct...END')

    # 開啟關於設定參數介面
    def open(self):
        self.hide()  # 隱藏
        self.window = Create()
        self.window.show()

    # 開啟關於
    def open_about(self):
        self.hide()  # 隱藏
        self.window = About()
        self.window.show()


class Create(QtWidgets.QMainWindow, creat):

    # 在這裏的是系統開啟會重新re過一次的動作
    def __init__(self):
        super(Create, self).__init__()  # 繼承
        self.ui = creat()
        self.ui.setupUi(self)
        self.ui.pushButton_set_up.clicked.connect(self.set_ok)
        # --------------圖片
        self.ui.label_window_pic.setPixmap(QtGui.QPixmap(BASE_DIR + '\\window_test_image'))
        # --------------根據框框大小縮放圖片
        self.ui.label_window_pic.setScaledContents(True)

        # self.ui.pushButton_setup.clicked.connect(self.set_ok)
        self.ui.pushButton_re.clicked.connect(self.reset)
        self.ui.pushButton_cancel.clicked.connect(self.close)
        self.ui.pushButton_set.clicked.connect(self.insert_table)
        self.ui.pushButton_delete.clicked.connect(self.dele)
        self.setWindowIcon(QtGui.QIcon(BASE_DIR + "\\icon.ico"))
        #不能改寫
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #選定一行
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.number = 0#設定表格參數'number'=0(初始化)
        self.ui.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        # 將右鍵菜單綁定到槽函數generateMenu
        self.ui.tableWidget.customContextMenuRequested.connect(self.generateMenu)
        # self.setLayout(Create)

    def insert_table(self):
        h = self.ui.lineEdit_H.text()
        w = self.ui.lineEdit_W.text()
        q = self.ui.lineEdit_Quantity.text()
        type = self.ui.comboBox_type.currentText()
        print(type,w,h,q)#設定參數tape,w,h,q,
        #抓取參數寫入表格(number,0123)
        # if self.number >=0:
        #     self.qwe == True
        # else:
        #     qwe == False
        if self.number >=0:
            self.ui.tableWidget.setItem(self.number, 0, QTableWidgetItem(type))
            self.ui.tableWidget.setItem(self.number, 1, QTableWidgetItem(h))
            self.ui.tableWidget.setItem(self.number, 2, QTableWidgetItem(w))
            self.ui.tableWidget.setItem(self.number, 3, QTableWidgetItem(q))
            # 設定輸入文字置中以及上下置中
            self.ui.tableWidget.item(self.number, 0).setTextAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.ui.tableWidget.item(self.number, 1).setTextAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.ui.tableWidget.item(self.number, 2).setTextAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.ui.tableWidget.item(self.number, 3).setTextAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            # 設定1時候參數+1
            self.number += 1
            if self.number >= 0:
                self.ui.tableWidget.setRowCount(self.number + 1)
        else:
            self.number = 0
            pass

    def generateMenu(self, pos):
        # 計算有多少條數據，默認-1,self.number

        for i in self.ui.tableWidget.selectionModel().selection().indexes():
            self.number = i.row()

        # 表格中只有兩條有效數據，所以只在前兩行支持右鍵彈出菜單
        if self.number < 80:
            menu = QMenu()
            item1 = menu.addAction(u'刪除')
            item2 = menu.addAction(u'設定')
            item3 = menu.addAction(u'我不知道他要幹嘛')
            action = menu.exec_(self.ui.tableWidget.mapToGlobal(pos))
            # 顯示選中行的數據文本
            if action == item1:
                print('你選了選項一，當前行文字內容是：', self.ui.tableWidget.item(self.number, 0).text(),
                      self.ui.tableWidget.item(self.number, 1).text(),
                      self.ui.tableWidget.item(self.number, 2).text())
                self.row = self.ui.tableWidget.currentRow()
                self.ui.tableWidget.removeRow(self.row)
                self.number -= 1
            if action == item2:
                print( self.ui.tableWidget.item(self.number, 0).text(),
                      self.ui.tableWidget.item(self.number, 1).text(),
                      self.ui.tableWidget.item(self.number, 2).text())
                self.ui.tableWidget.setEditTriggers(QAbstractItemView.CurrentChanged)


            if action == item3:
                print( self.ui.tableWidget.item(self.number, 0).text(),
                      self.ui.tableWidget.item(self.number, 1).text(),
                      self.ui.tableWidget.item(self.number, 2).text())

        else:
            self.number = 0
            pass

    def dele(self):
        self.row = self.ui.tableWidget.currentRow()
        print(self.row)
        self.ui.tableWidget.removeRow(self.row)
        self.number-= 1

    # 設定設定完成提示框(yes or no)
    def set_ok(self):
       pass

    def close(self):
        self.hide()
        self.window = MainWindow()
        self.window.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.hide()
        self.window = MainWindow()
        self.window.show()

    def reset(self):
        self.ui.lineEdit_H.setText('')
        self.ui.lineEdit_W.setText('')
        self.ui.comboBox_type.setCurrentIndex(0)
        print(self.ui.comboBox_type.currentText())

# about介面
class About(QtWidgets.QMainWindow, about):
    def __init__(self):
        super(About, self).__init__()  # 繼承
        self.ui = about()
        self.ui.setupUi(self)


# 執行
if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    system_root = os.path.dirname(os.path.realpath(__file__))
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
