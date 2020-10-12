from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QAbstractItemView, QTableWidgetItem
from qt5 import Ui_MainWindow, Ui_Form, Ui_toolcheck, Ui_widget_projectcheck , Ui_check
import sys, re, time, serial.tools.list_ports
import toolconnect, sql_connect, measure
from PyQt5.QtCore import QThread, pyqtSignal
import os
import shutil
import matplotlib.pyplot as plt
import global_var as gvar


# GLOBAL VARIABLES
selected_com_port = ''
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, project_name, measure_item_data, work_order_data, measurer):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(BASE_DIR + "\\ico.ico"))
        # self.plot_()
        self.sql = sql_connect.sql_connect()
        self.measure_value_data = [] #所有量測數值
        self.measure_yield = [] #計算量測次數串列
        self.drawing_data = []
        self.number = 0 #自動跳行
        self.row = int()
        self.column = int()


        self.measure_value = measure_thread()
        self.measure_value.measure_value.connect(self.setmeasurevalue)
        self.com_name = gvar.system_com_name
        self.project_name = project_name
        self.measurer = measurer
        self.measure_item_data = []
        self.work_order_data = work_order_data
        print("專案名稱:%s"%self.project_name)
        print("工單設定:%s"%self.work_order_data)
        print("量測項目%s"%self.measure_item_data)
        self.measure_project_time = time.strftime("%Y-%m-%d", time.localtime())#量測日期
        self.measure_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())#量測數值日期

        # self.ui.tableWidget_measure.itemClicked.connect(self.get_measure_item)
        self.ui.tableWidget_measure.itemSelectionChanged.connect(self.get_blank_form)

        self.measure_tool_start()

        self.tb = self.addToolBar("open")
        self.new = QtWidgets.QAction(QtGui.QIcon(BASE_DIR + "\\po.png"), "UP project", self)
        self.tb.addAction(self.new)
        self.new = QtWidgets.QAction(QtGui.QIcon(BASE_DIR + "\\project_item.png"), "project_item", self)
        self.tb.addAction(self.new)
        self.new = QtWidgets.QAction(QtGui.QIcon(BASE_DIR + "\\measure_choose.png"), "project_choose", self)
        self.tb.addAction(self.new)
        self.ui.label_gonogo.setPixmap(QtGui.QPixmap(BASE_DIR + "\\GO.png"))
        self.ui.label_gonogo.setScaledContents(True)
        self.ui.label_project_name.setText("專案名稱：%s" % project_name)
        self.ui.label_project_item_name_2.setText("量測人員：%s" % self.measurer)

        self.project_item = ["量測部位", "量測日期", "量測次數", "良數", "不良數", "總數", "GO/NOGO"]
        self.ui.tableWidget_project_item.setRowCount(len(self.project_item))
        self.ui.tableWidget_project_item.setColumnCount(1)
        self.ui.tableWidget_project_item.horizontalHeader().setVisible(False)
        self.ui.tableWidget_project_item.setVerticalHeaderLabels(self.project_item)
        self.ui.tableWidget_project_item.setItem(0, 0, QTableWidgetItem("未選擇量測部位"))
        self.ui.tableWidget_project_item.setItem(0, 1, QTableWidgetItem(self.measure_time))
        self.ui.tableWidget_project_item.resizeColumnsToContents()

        self.measure_item = ["量測項目名稱", "量測數值上限", "量測數值下限", "量測數值中心",
                             "量測小數點位數", "量測單位", "量測次數", "量具名稱"]
        measure_item_data_old = measure_item_data
        # self.measure_item_data.clear()
        for item in measure_item_data_old:
            item.pop(0)
            if int(item[7]) > 0:
                number = int(item[6])
                print("量測點數:%s" % number)
                for i in range(1, number+1):
                    self.item = item[:]
                    self.item.insert(0, "%s - %s" % (item[0], i))
                    self.item.pop(1)
                    self.item.pop(-3)
                    self.measure_item_data.append(self.item)
        print(self.measure_item_data)
        self.ui.tableWidget_measure.setRowCount(len(self.measure_item))
        self.ui.tableWidget_measure.setColumnCount(len(self.measure_item_data))
        self.ui.tableWidget_measure.setVerticalHeaderLabels(self.measure_item)
        self.ui.tableWidget_measure.horizontalHeader().setVisible(False)
        for i in range(0, len(self.measure_item)):
            for i_2 in range(0, len(self.measure_item_data)):
                data = QTableWidgetItem(str(self.measure_item_data[i_2][i]))
                data.setTextAlignment(QtCore.Qt.AlignHCenter)
                self.ui.tableWidget_measure.setItem(i, i_2, data)
        self.ui.tableWidget_measure.setEditTriggers(QtWidgets.QTableWidget.DoubleClicked)#不可編輯


        self.ui.tableWidget_measure.setRowCount(len(self.measure_item) + int(self.measure_item_data[0][6]))#量測次數行數
        if int(self.measure_item_data[0][6]) > 1:
            self.measure_number_list = list()
            for i in range(int(self.measure_item_data[0][6])):
                measure_number = ("1 - %s" % (i+1))
                self.measure_number_list.append(measure_number)
            print(self.measure_number_list)
            # self.ui.tableWidget_project.resizeRowsToContents()  # 調整欄位大小
        self.ui.tableWidget_measure.resizeRowsToContents() #調整欄位大小 (垂直縮小)
        self.ui.tableWidget_measure.setVerticalHeaderLabels(self.measure_item + self.measure_number_list)#量測1-1設定


        # self.ui.tableWidget_measure.setColumnCount(len(self.measure_item_data))
        # self.measure_item_set = list()
        # for item in self.measure_item_data:
        #     self.measure_item_set.append(item[1])
        # print(self.measure_item_set)
        # self.ui.tableWidget_measure.setHorizontalHeaderLabels(self.measure_item_set)


        #量測部位圖片
        self.measure_image_item = self.sql.sql_all_image_item(self.project_name)
        self.ui.label_item_image.setPixmap(QtGui.QPixmap(BASE_DIR + "\\measure_item_image\\%s\\%s"%(self.project_name, self.measure_image_item[0])))
        self.ui.label_item_image.setScaledContents(True)

        self.ui.tableWidget_measure.doubleClicked.connect(self.double_clicked)
        self.ui.tableWidget_measure.cellChanged.connect(self.value_insert) #輸入量測資料

    def double_clicked(self):
        self.row = self.ui.tableWidget_measure.currentRow()
        self.column = self.ui.tableWidget_measure.currentColumn()
        print(self.row, self.column)
        print("double_clicked R:%s C:%s"%(self.row, self.column))

    def value_insert(self):
        pass
    #     try:
    #             self.measure_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())  # 量測數值日期
    #             self.row = self.ui.tableWidget_measure.currentRow()
    #             self.colunm = self.ui.tableWidget_measure.currentColumn()
    #             self.insert_value = self.ui.tableWidget_measure.item(self.row, self.colunm).text()
    #             # print(self.ui.tableWidget_measure.item(self.row, self.colunm).text())
    #             print(self.row, self.colunm)
    #             self.gonogo = measure.measure_go_nogo_calculate(
    #                 float(self.ui.tableWidget_measure.item(2, self.column).text()),
    #                 float(self.ui.tableWidget_measure.item(3, self.column).text()),
    #                 float(self.insert_value)
    #             )
    #
    #             self.ui.tableWidget_project_item.setItem(0, 0, QTableWidgetItem(
    #                 str(self.ui.tableWidget_measure.item(1, self.column).text())))
    #             if self.gonogo == True:
    #                 self.ui.label_gonogo.setPixmap(QtGui.QPixmap(BASE_DIR + "\\GO.PNG"))
    #                 self.ui.tableWidget_project_item.setItem(0, 6, QTableWidgetItem("GO"))
    #
    #             elif self.gonogo == False:
    #                 self.ui.label_gonogo.setPixmap(QtGui.QPixmap(BASE_DIR + "\\NOGO.PNG"))
    #                 self.ui.tableWidget_project_item.setItem(0, 6, QTableWidgetItem("NOGO"))
    #
    #             self.ui.tableWidget_project_item.setItem(0, 1, QTableWidgetItem(self.measure_time))
    #             self.measure_value_new_data = [self.insert_value,
    #                                            self.ui.tableWidget_measure.item(6, self.column).text(),  # 單位
    #                                            self.measure_time,  # 量測日期
    #                                            self.ui.tableWidget_measure.item(2, self.column).text(),  # 上限
    #                                            self.ui.tableWidget_measure.item(3, self.column).text(),  # 下限
    #                                            self.ui.tableWidget_measure.item(7, self.column).text(),  # 量測次數
    #                                            self.ui.tableWidget_measure.item(1, self.column).text(),  # 量測部位
    #                                            self.measure_number_list[int(self.row - 9)]  # 量測次數
    #                                            ]
    #             if len(self.measure_value_data) > 0:
    #                 for item in self.measure_value_data:
    #                     if item[7] == self.measure_value_new_data[7] and item[6] == self.measure_value_new_data[6]:
    #                         self.measure_value_data.remove(item)
    #                         print("清除資料")
    #             self.measure_value_data.append(self.measure_value_new_data)
    #             print("new data :%s" % self.measure_value_new_data)
    #             print("all_data :%s" % self.measure_value_data)
    #             if len(self.measure_number_list) == len(self.measure_value_data):
    #                 number = int((self.row - 8) / 3)  # 計算要增加幾項
    #                 for i in range(int(self.measure_item_data[0][7])):
    #                     measure_number = ("%s - %s" % (number + 1, i + 1))
    #                     self.measure_number_list.append(measure_number)
    #                     self.ui.tableWidget_measure.setRowCount(
    #                         int(len(self.measure_item)) + int(len(self.measure_number_list)))
    #                     self.ui.tableWidget_measure.setVerticalHeaderLabels(
    #                         self.measure_item + self.measure_number_list)
    #             for item in self.measure_value_data:
    #                 if item[6] == self.ui.tableWidget_measure.item(1, self.column).text():
    #                     self.measure_yield.append(item[0])
    #             (value_excellent, value_inferior, all) = measure.measure_Yield(
    #                 float(self.ui.tableWidget_measure.item(2, self.column).text()),
    #                 float(self.ui.tableWidget_measure.item(3, self.column).text()),
    #                 self.measure_yield)
    #             self.ui.tableWidget_project_item.setItem(0, 3, QTableWidgetItem(str(value_excellent)))
    #             self.ui.tableWidget_project_item.setItem(0, 4, QTableWidgetItem(str(value_inferior)))
    #             self.ui.tableWidget_project_item.setItem(0, 5, QTableWidgetItem(str(all)))
    #             self.measure_yield.clear()
    #             for item in self.measure_value_data:
    #                 if item[6] == self.ui.tableWidget_measure.item(1, self.column).text():
    #                     self.drawing_data.append(item)
    #             print(self.drawing_data)
    #             (measure_data, upper_data, lower_data) = measure.draw_measure(self.drawing_data)
    #             self.drawing_data.clear()
    #             print(self.drawing_data)
    #             print(measure_data, upper_data, lower_data)
    #             self.plot_(upper_data, lower_data, measure_data)
    #     except:
    #         print("輸入量測資料空白")

    def keyPressEvent(self, e): #擷取信號
            if e.key() == QtCore.Qt.Key_Enter:
                print("enter")

    def plot_(self, upper_data, lower_data, measure_data):
        self.ui.figure.clf()
        ax = self.ui.figure.add_axes([0.125, 0.125, 0.8, 0.8])
        ax.plot(measure_data, marker='o', mfc='w', label="量測數值", linewidth=2.5) #ro = 定義點狀
        ax.plot(upper_data, label="上限", mfc='w', linestyle='dashed')
        ax.plot(lower_data, label="下限", mfc='w', linestyle='dashed')
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  #設置中文字 不然打不出來
        plt.xlabel("量測次數")
        plt.ylabel("量測數值")
        plt.legend()
        self.ui.canvas.draw()

    def setmeasurevalue(self, value): #量具輸入
        self.value = value
        if self.row != self.ui.tableWidget_measure.currentRow() or self.row is None:
            self.number = 0
        elif self.column != self.ui.tableWidget_measure.currentColumn() or self.column is None:
            self.number = 0
        self.row = self.ui.tableWidget_measure.currentRow()
        self.column = self.ui.tableWidget_measure.currentColumn()
        self.ui.tableWidget_measure.setItem(self.row + self.number, self.column, QTableWidgetItem(str(self.value)))
        self.gonogo = measure.measure_go_nogo_calculate(
            float(self.ui.tableWidget_measure.item(2, self.column).text()),
            float(self.ui.tableWidget_measure.item(3, self.column).text()),
            float(self.value))
        self.ui.tableWidget_project_item.setItem(0, 0, QTableWidgetItem(str(self.ui.tableWidget_measure.item(0, self.column).text())))
        if self.gonogo == True:
            self.ui.label_gonogo.setPixmap(QtGui.QPixmap(BASE_DIR + "\\GO.PNG"))
            self.ui.tableWidget_project_item.setItem(0, 6, QTableWidgetItem("GO"))
            self.ui.tableWidget_measure.item(self.row + self.number, self.column).setTextAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)  # 設定輸入文字置中以及上下置中

        elif self.gonogo == False:
            self.ui.label_gonogo.setPixmap(QtGui.QPixmap(BASE_DIR + "\\NOGO.PNG"))
            self.ui.tableWidget_project_item.setItem(0, 6, QTableWidgetItem("NOGO"))
            self.ui.tableWidget_measure.item(self.row + self.number, self.column).setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))#設置文字為紅色
            self.ui.tableWidget_measure.item(self.row + self.number, self.column).setTextAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)  # 設定輸入文字置中以及上下置中

        self.measure_value_new_data = [self.value,
                                       self.ui.tableWidget_measure.item(6, self.column).text(),  # 單位
                                       self.measure_time,  # 量測日期
                                       self.ui.tableWidget_measure.item(2, self.column).text(),  # 上限
                                       self.ui.tableWidget_measure.item(3, self.column).text(),  # 下限
                                       self.ui.tableWidget_measure.item(7, self.column).text(),  # 量測次數
                                       self.ui.tableWidget_measure.item(0, self.column).text(),  # 量測部位
                                       self.measure_number_list[(self.row + self.number) - 8]  # 量測次數
                                       ]
        if len(self.measure_value_data) > 0:
            self.delet_data = []
            for item in self.measure_value_data:
                if item[7] == self.measure_value_new_data[7] and item[6] == self.measure_value_new_data[6]:
                    # print(self.measure_value_data.index(item))
                    # data_position = self.measure_value_data.index(item)
                    self.delet_data = item[:]
                    self.measure_value_data_check = False
                    # self.measure_value_data.insert(data_position, self.measure_value_new_data)# 新增new_data
                elif item[7] != self.measure_value_new_data[7] or item[6] != self.measure_value_new_data[6]:
                    self.measure_value_data_check = True

            #檢查旗標
            if self.measure_value_data_check is False:
                dele_number = self.measure_value_data.index(self.delet_data) #位置
                self.measure_value_data.remove(self.delet_data)
                self.measure_value_data.insert(dele_number, self.measure_value_new_data)
                # self.measure_value_data.append(self.measure_value_new_data)
                print("清除資料:%s" % self.delet_data)
            if self.delet_data != [] and self.measure_value_data_check == True:
                dele_number = self.measure_value_data.index(self.delet_data)
                self.measure_value_data.remove(self.delet_data)
                # self.measure_value_data.append(self.measure_value_new_data)
                self.measure_value_data.insert(dele_number, self.measure_value_new_data)
                print("清除資料:%s" % self.delet_data)
            elif self.measure_value_data_check is True:
                self.find_number_check = False
                # self.find_item = []
                # for item in self.measure_value_data: #抓出量測次數
                #     if self.measure_value_new_data[-2] == item[-2]:
                #         find_number = list(item[7])[-1]
                #         if find_number > list(self.measure_value_new_data[-1])[-1]:
                #             self.find_number_check = True
                #             self.find_item.append(item[-1][:])
                if self.find_number_check is True:
                    print("Ture")
                    pass
                elif self.find_number_check is False:
                    self.measure_value_data.append(self.measure_value_new_data)
                print("新增資料:%s" % self.measure_value_new_data)


        elif len(self.measure_value_data) == 0:
            self.measure_value_data.append(self.measure_value_new_data)
        self.number = self.number + 1

        for item in self.measure_value_data:
            if item[6] == self.ui.tableWidget_measure.item(0, self.column).text():
                self.measure_yield.append(item[0])

        #計算良數
        (value_excellent, value_inferior, all) = measure.measure_Yield(
            float(self.ui.tableWidget_measure.item(2, self.column).text()),
            float(self.ui.tableWidget_measure.item(3, self.column).text()),
            self.measure_yield)

        #人機介面數值
        self.ui.tableWidget_project_item.setItem(0, 3, QTableWidgetItem(str(value_excellent)))
        self.ui.tableWidget_project_item.setItem(0, 4, QTableWidgetItem(str(value_inferior)))
        self.ui.tableWidget_project_item.setItem(0, 5, QTableWidgetItem(str(all)))
        self.ui.tableWidget_project_item.setItem(0, 2, QTableWidgetItem(str(self.ui.tableWidget_measure.item(6, self.column).text())))

        if len(self.measure_yield)+1 > len(self.measure_number_list):
            number = int(len(self.measure_number_list) / 3)  # 計算要增加幾項
            print(number)
            for i in range(int(self.ui.tableWidget_measure.item(6, self.column).text())):
                measure_number = ("%s - %s" % (number + 1, i + 1))
                self.measure_number_list.append(measure_number)
                self.ui.tableWidget_measure.setRowCount(int(len(self.measure_item)) + int(len(self.measure_number_list)))
                self.ui.tableWidget_measure.setVerticalHeaderLabels(self.measure_item + self.measure_number_list)
        #清除數值串列
        self.measure_yield.clear()


    def measure_tool_start(self):
        self.measure_value.is_on = True
        self.measure_value.set_port(gvar.system_com_name)
        self.measure_value.start()

    # def get_measure_item(self):
    #     column = self.ui.tableWidget_measure.currentColumn()
    #     row = self.ui.tableWidget_measure.currentRow()
    #     self.ui.label_item_image.setPixmap(QtGui.QPixmap(BASE_DIR + "\\measure_item_image\\%s\\%s" % (self.project_name, self.measure_image_item[column])))
    #     self.ui.label_item_image.setScaledContents(True)
    #     self.ui.label_project_item_name.setText("量測項目：%s"%self.measure_image_item[column])
    #     # self.ui.tableWidget_project_item.setItem(0, 2, QTableWidgetItem(self.ui.tableWidget_measure.item(self.row, 7).text()))
    #     print(row)

    def closeEvent(self, QCloseEvent):
        self.reply = QMessageBox.question(self, "警示", "確定離開量測頁面?", QMessageBox.Yes, QMessageBox.No)
        if self.reply == QMessageBox.Yes:
            self.hide()
            self.window = TOOLWindow()
            self.window.show()
        elif self.reply == QMessageBox.No:
            QCloseEvent.ignore()
    def get_blank_form(self): #選擇查看
        column = self.ui.tableWidget_measure.currentColumn()
        row = self.ui.tableWidget_measure.currentRow()
        # try: #找尋text
        #     self.value = float(self.ui.tableWidget_measure.item(row, column).text())
        #     value_check = True
        # except:
        #     value_check = False
        #     pass
        #
        # self.ui.label_item_image.setPixmap(QtGui.QPixmap(
        #     BASE_DIR + "\\measure_item_image\\%s\\%s" % (self.project_name, self.measure_image_item[column])))
        # self.ui.label_item_image.setScaledContents(True)
        # self.ui.label_project_item_name.setText("量測項目：%s" % self.measure_image_item[column])
        # self.ui.tableWidget_project_item.setItem(0, 2, QTableWidgetItem(self.ui.tableWidget_measure.item(7, column).text()))
        # for item in self.measure_value_data:
        #     if item[6] == self.ui.tableWidget_measure.item(1, column).text():
        #         self.measure_yield.append(item[0])
        # (value_excellent, value_inferior, all) = measure.measure_Yield(
        #     float(self.ui.tableWidget_measure.item(2, column).text()),
        #     float(self.ui.tableWidget_measure.item(3, column).text()),
        #     self.measure_yield)
        # self.measure_yield.clear()
        #
        # self.ui.tableWidget_project_item.setItem(0, 3, QTableWidgetItem(str(value_excellent)))
        # self.ui.tableWidget_project_item.setItem(0, 4, QTableWidgetItem(str(value_inferior)))
        # self.ui.tableWidget_project_item.setItem(0, 5, QTableWidgetItem(str(all)))
        #
        # if value_check is True and self.value is not str:
        #     self.gonogo = measure.measure_go_nogo_calculate(
        #         float(self.ui.tableWidget_measure.item(2, self.column).text()),
        #         float(self.ui.tableWidget_measure.item(3, self.column).text()),
        #         float(self.value)
        #     )
        #     if self.gonogo == True:
        #         self.ui.label_gonogo.setPixmap(QtGui.QPixmap(BASE_DIR + "\\GO.PNG"))
        #         self.ui.tableWidget_project_item.setItem(0, 6, QTableWidgetItem("GO"))
        #     elif self.gonogo == False:
        #         self.ui.label_gonogo.setPixmap(QtGui.QPixmap(BASE_DIR + "\\NOGO.PNG"))
        #         self.ui.tableWidget_project_item.setItem(0, 6, QTableWidgetItem("NOGO"))

        # for item in self.measure_value_data:
        #     if item[6] == self.ui.tableWidget_measure.item(1, column).text():
        #         self.drawing_data.append(item)
        # (measure_data, upper_data, lower_data) = measure.draw_measure(self.drawing_data)
        # print(measure_data, upper_data, lower_data)
        # self.plot_(measure_data, upper_data, lower_data)

class tool_measure_choose(QtWidgets.QWidget, Ui_check):
    measure_mode = pyqtSignal(str)
    def __init__(self):
        super(tool_measure_choose, self).__init__()
        self.ui = Ui_check()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(BASE_DIR + '\\ico.ico'))
        self.ui.pushButton_exit.clicked.connect(self.close)
        self.ui.radioButton.clicked.connect(self.mode_show)
        self.ui.radioButton_2.clicked.connect(self.mode_show)
        self.ui.pushButton_setup.clicked.connect(self.mode_set_ok)
    def mode_show(self):
        rad = self.sender()
        if rad.text() == "依照零件部位":
            self.mode = "零件部位"
        elif rad.text() == "依照件數":
            self.mode = "依照件數"
        print("子視窗%s" % self.mode)
    def mode_set_ok(self):
        mode = self.mode
        self.measure_mode.emit(mode)
        self.close()
    def close(self):
        self.hide()

class project_check_window(QtWidgets.QWidget,Ui_widget_projectcheck):
    def __init__(self, data_all, tool_ok_com):
        super(project_check_window, self).__init__()
        self.project_name = str()
        self.tool_com = tool_ok_com
        self.sql_project_data = data_all
        self.ui = Ui_widget_projectcheck()
        self.sql = sql_connect.sql_connect()
        self.setWindowIcon(QtGui.QIcon('D:/GitHub/pythonProject/ico.ico'))
        self.ui.setupUi(self)
        self.ui.pushButton_close.clicked.connect(self.close)
        self.ui.pushButton_cinfirm_project.clicked.connect(self.open_start_measure_window)
        self.ui.pushButton_rest_project.clicked.connect(self.resst_project)
        self.measure_check = False

        #匯入量測專案資料
        self.project_name_item = ["專案名稱", "建立日期", "建立人", "備註"]
        self.ui.tableWidget_project.setRowCount(len(self.sql_project_data))
        self.ui.tableWidget_project.setColumnCount(len(self.project_name_item))
        self.ui.tableWidget_project.setHorizontalHeaderLabels(self.project_name_item)
        for i in range(len(self.sql_project_data)):
            for i_2 in range(0,len(self.sql_project_data[i])):
                self.ui.tableWidget_project.setItem(i, i_2, QTableWidgetItem(str(self.sql_project_data[i][i_2])))
        self.ui.tableWidget_project.setEditTriggers(QAbstractItemView.DoubleClicked)#不可編輯
        self.ui.tableWidget_project.resizeColumnsToContents()#調整欄位大小
        self.ui.tableWidget_project.resizeRowsToContents()#調整欄位大小
        self.ui.tableWidget_project.setSelectionBehavior(self.ui.tableWidget_project.SelectRows)
        self.ui.tableWidget_project.itemClicked.connect(self.set_work_order_measure_item)

        #匯入量測部位圖片
        DIRT_TEMP = create_temp()
        self.measure_image_project = self.sql.sql_image_all_project_name()
        for name in self.measure_image_project:
            measure_item = self.sql.sql_all_image_item("%s" % name)
            os.makedirs(BASE_DIR + "\\measure_item_image\\%s"%name)
            for item in measure_item:
                data = self.sql.sql_image_base64data(item)
                sql_connect.save("measure_item_image/%s/%s" % (name, item), data, "jpg")
                print("load image ok")

    def set_work_order_measure_item(self, item):
        print("選擇專案名稱:%s" % self.sql_project_data[item.row()][0])#專案名稱
        porject_name = self.sql_project_data[item.row()][0]
        self.ui.lineEdit_now_project_name.setText(self.sql_project_data[item.row()][0])
        #匯入工單表單內容
        self.work_order_item = ["專案名稱", "工單", "件號", "件數", "材料", "機台名稱", "批號", "班別", "量測人員", "備註"]
        sql = sql_connect.sql_connect()
        self.work_order_data = sql.sql_find_work_order(str(self.sql_project_data[item.row()][0]))
        self.project_name = self.ui.lineEdit_now_project_name.text()#名稱定義
        self.ui.tableWidget_work_order.setRowCount(len(self.work_order_data))
        self.ui.tableWidget_work_order.setColumnCount(len(self.work_order_item))
        self.ui.tableWidget_work_order.setHorizontalHeaderLabels(self.work_order_item)
        self.ui.tableWidget_work_order.verticalHeader().setVisible(False)
        for i in range(len(self.work_order_data)):
            for i_2 in range(0, len(self.work_order_data[i])):
                self.ui.tableWidget_work_order.setItem(i, i_2, QTableWidgetItem(str(self.work_order_data[i][i_2])))
        self.ui.tableWidget_work_order.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget_work_order.resizeColumnsToContents()
        self.ui.tableWidget_work_order.resizeRowsToContents()
        self.ui.tableWidget_work_order.setSelectionBehavior(self.ui.tableWidget_work_order.SelectRows)

        #匯入量測item
        self.measure_item = ["量測專案名稱", "量測項目名稱", "量測數值上限", "量測數值下限", "量測數值中心", "量測小數點位數", "量測單位", "量測點數", "量測次數", "量具名稱", "量測部位圖"]
        self.measure_item_data = sql.sql_find_measure_item(self.sql_project_data[item.row()][0])
        print(self.measure_item_data)
        self.ui.tableWidget_measureitem.setRowCount(len(self.measure_item_data))
        self.ui.tableWidget_measureitem.setColumnCount(len(self.measure_item))
        self.ui.tableWidget_measureitem.setHorizontalHeaderLabels(self.measure_item)

        for i in range(len(self.measure_item_data)):
            for i_2 in range(len(self.measure_item_data[i])):
                self.ui.tableWidget_measureitem.setItem(i, i_2, QTableWidgetItem(str(self.measure_item_data[i][i_2])))
                self.ui.tableWidget_measureitem.item(i, i_2).setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget_measureitem.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget_measureitem.resizeColumnsToContents()
        self.ui.tableWidget_measureitem.resizeRowsToContents()
        self.ui.tableWidget_measureitem.setSelectionBehavior(self.ui.tableWidget_measureitem.SelectRows)

        self.image_item = []
        for item in self.measure_item_data:
            self.image_item.append(item[1])
        for item in self.image_item:
            icon = QTableWidgetItem(QtGui.QIcon(BASE_DIR + "\\measure_item_image\\%s\\%s.jpg"%(str(porject_name), str(item))), "")
            print(self.image_item.index(item))
            self.ui.tableWidget_measureitem.setItem(self.image_item.index(item), 10, icon)
            self.ui.tableWidget_measureitem.setIconSize(QtCore.QSize(300, 300))
            self.ui.tableWidget_measureitem.setColumnWidth(10, 300)
            self.ui.tableWidget_measureitem.setRowHeight(self.image_item.index(item), 300)


        # icon = QTableWidgetItem(QtGui.QIcon(BASE_DIR + "\\measure_item_image\\%s\\%s.jpg"%(str(porject_name), "2")),'')
        # self.ui.tableWidget_measureitem.setItem(0, 10, icon)
        # self.ui.tableWidget_measureitem.setIconSize(QtCore.QSize(300, 300))
        # self.ui.tableWidget_measureitem.setColumnWidth(10, 350)
        # self.ui.tableWidget_measureitem.setRowHeight(0, 350)
        try:
            if len(self.measure_item_data) == 0:
                self.measure_check = False
            else:
                self.measure_check = True
        except:
            pass
        self.measure_image_project = self.sql.sql_image_all_project_name()


    def resst_project(self):
        self.ui.tableWidget_project.clear()
        self.ui.tableWidget_project.setEditTriggers(QAbstractItemView.CurrentChanged)
        sql = sql_connect.sql_connect()
        self.sql_project_data = sql.sql_all_date("mysite_project")
        self.ui.tableWidget_project.setRowCount(len(self.sql_project_data))
        self.ui.tableWidget_project.setColumnCount(len(self.project_name_item))
        self.ui.tableWidget_project.setHorizontalHeaderLabels(self.project_name_item)
        for i in range(len(self.sql_project_data)):
            for i_2 in range(0, len(self.sql_project_data[i])):
                self.ui.tableWidget_project.setItem(i, i_2, QTableWidgetItem(str(self.sql_project_data[i][i_2])))
        self.ui.tableWidget_project.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget_project.resizeColumnsToContents()
        self.ui.tableWidget_project.resizeRowsToContents()
        self.ui.tableWidget_project.setSelectionBehavior(self.ui.tableWidget_measureitem.SelectRows)

    def close(self):
        self.hide()
        self.window = TOOLWindow()
        self.window.show()

    def closeEvent(self, QCloseEvent):
        self.hide()
        self.window = TOOLWindow()
        self.window.show()

    def open_start_measure_window(self, QCloseEvent):
        self.measurer = self.ui.lineEdit_measure_staff.text()
        if self.measure_check == True:
            if self.measurer is not "":
                self.hide()
                print(self.ui.lineEdit_now_project_name.text())
                sql = sql_connect.sql_connect()
                self.window = MainWindow(self.project_name, self.measure_item_data, self.work_order_data, self.measurer)
                self.window.show()
            elif self.measurer is "":
                self.reply = QMessageBox.question(self, 'Message', "量測人員名稱未設定", QMessageBox.Yes)
        elif self.measure_check == False:
            self.reply = QMessageBox.question(self, 'Message', "量測專案沒有工單以及量測設定", QMessageBox.Yes)

class TOOLWindow(QtWidgets.QWidget, Ui_Form):
    com_signal = pyqtSignal(str)
    def __init__(self):
        super(TOOLWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(BASE_DIR + '\\ico.ico'))
        # self.ui.start_measure.clicked.connect(self.open_main_measure_window)
        self.ui.tool_test.clicked.connect(self.open_tool_test)
        self.ui.start_measure.clicked.connect(self.open_porject_check_window)
        # self.ui.excit.clicked.connect(self.close)
        self.main_window_center()
        self.set_ok_con = None

    def main_window_center(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height() - size.height())/2)

    def open_porject_check_window(self):
        # check network connections before show window
        from urllib import request, error
        def internet_on():
            try:
                request.urlopen('http://www.google.com', timeout=1)
                return True
            except error.URLError as err:
                return False
        get_internet_stat = internet_on()

        self.set_ok_con = True

        if self.set_ok_con is None:
            self.reply = QMessageBox.question(self, '警示', "量測量具還未設定", QMessageBox.Yes)
        if get_internet_stat is False:
            self.reply = QMessageBox.warning(self, '警示', "沒有網路連線", QMessageBox.Yes)
        elif self.set_ok_con is not None and get_internet_stat is True:
            self.hide()
            sql = sql_connect.sql_connect()
            self.window = project_check_window(sql.sql_all_date("mysite_project"), self.set_ok_con)
            self.window.show()

    def send_com_signal(self):
        com = self.set_ok_con
        self.com_signal.emit(com)

    def open_tool_test(self):
        self.window = tool_test(toolconnect.com2())
        self.window.mysignal.connect(self.get_signal)
        self.window.show()

    def closeEvent(self, QCloseEvent):
        self.reply = QMessageBox.question(self, '警示',"確定離開量測系統?", QMessageBox.Yes, QMessageBox.No)
        if self.reply == QMessageBox.Yes:
            QCloseEvent.accept()
            # delet() 刪除資料夾
        else:
            QCloseEvent.ignore()
    def get_signal(self, con):
        self.set_ok_con = con
        print(self.set_ok_con)

# 多線程失敗
# class Backendthread(QThread):
#     update_date = pyqtSignal(str)
#     def run(self):
#         while True:
#             date = QDateTime.currentDateTime()
#             currtime = date.toString('yyyy-MM-dd hh:mm:ss')
#             self.update_date.emit( str(currtime) )
#             print(date)
#             time.sleep(1)
# def iniUi(self):
    #     self.backend = Backendthread()
    #     self.backend.start()
    #
    # def hand(self, data):
    #     self.lineEdit_toolvalue.setText(data)

class tool_test(QtWidgets.QWidget,Ui_toolcheck):
    mysignal = pyqtSignal(str)
    def __init__(self, tool_com_all):
        self.tool_com_all = tool_com_all
        super(tool_test, self).__init__()
        self.ui = Ui_toolcheck()
        self.ui.setupUi(self)
        self.main_window_center()
        self.setWindowIcon(QtGui.QIcon(BASE_DIR + '\\ico_1.ico'))
        for com_obj in self.tool_com_all:
            self.ui.comboBox_comname.addItem(com_obj)
        self.measure_value = measure_thread()
        self.measure_value.measure_value.connect(self.setmeasurevalue)
        self.measure_value.measure_tool_name.connect(self.setmeasuretoolname)
        self.ui.Button_tool_connect.clicked.connect(self.measure_tooltest_start)

        self.ui.Button_tool_connect_rest.clicked.connect(self.tool_rest)
        self.ui.pushButton_9.clicked.connect(self.close)
        self.ui.pushButton_10.clicked.connect(self.tool_set_ok)

        self.chick_tool_ok = False

    def tool_set_ok(self):
        if self.chick_tool_ok == False :
            self.reply = QMessageBox.question(self, 'Message', "量測量具還未設定", QMessageBox.Yes)
        elif self.chick_tool_ok == True:
            self.measure_value.is_on = False
            self.con = self.set_con[0]
            gvar.system_com_name = self.set_con[0]
            self.mysignal.emit(self.con)
            self.hide()

    def tool_rest(self):
        self.chick_tool_ok = False
        self.ui.comboBox_comname.clear()
        rest_com_choose = toolconnect.com2()
        for com_obj in rest_com_choose:
            self.ui.comboBox_comname.addItem(com_obj)
        self.ui.lineEdit_toolname.setText(' ')
        self.ui.lineEdit_toolvalue.setText(' ')
        self.measure_value.is_on = False
        self.measure_value = measure_thread()
        self.measure_value.measure_value.connect(self.setmeasurevalue)
        self.measure_value.measure_tool_name.connect(self.setmeasuretoolname)
        print('self.measure_value.is_on=%s' % self.measure_value.is_on)

    def setmeasurevalue(self, value):
        self.ui.lineEdit_toolvalue.setText(value)

    def setmeasuretoolname(self, name):
        self.ui.lineEdit_toolname.setText(name)

    def closeEvent(self, QCloseEvent):
        self.measure_value.is_on = False
        print('self.measure_value.is_on=%s'%self.measure_value.is_on)
        # self.window = TOOLWindow()
        # self.window.show()

    def main_window_center(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height() - size.height())/2)

    def measure_tooltest_start(self):
        self.chick_tool_ok = True
        self.set_con = re.findall(r"\d",self.ui.comboBox_comname.currentText())
        print('self.set_con=%s'%self.set_con[0])
        self.measure_value.is_on = True
        self.measure_value.set_port(self.set_con[0])
        self.measure_value.start()

    def close(self):
        self.hide()
        self.measure_value.is_on = False
        print('self.measure_value.is_on=%s' % self.measure_value.is_on)
        # self.window = TOOLWindow()
        # self.window.show()

class measure_thread(QThread):
    measure_value = pyqtSignal(str)
    measure_tool_name = pyqtSignal(str)
    measure_unit = pyqtSignal(str)
    def __init__(self, parent=None):
        super(measure_thread, self).__init__(parent)
        self.is_on = True
    def set_port(self, port):
        self.set_port = port
    def run(self):
        # pass
        while self.is_on:
            returenlist = self.serial_test(self.set_port)
            if self.is_on == False:
                break
            self.measure_value.emit(str(returenlist[0]))
            self.measure_tool_name.emit(str(returenlist[1]))
            self.measure_unit.emit(str(returenlist[2]))

    def serial_test(self,comnumber):
        COM_PORT = ("COM%s" % comnumber)  # 指定通訊埠名稱
        BAUD_RATES = 57600  # 設定傳輸速率
        BYTE_SIZE = 8
        PARITY = 'N'
        STOP_BITS = 1
        ser = serial.Serial(COM_PORT, BAUD_RATES, BYTE_SIZE, PARITY, STOP_BITS, timeout=None)
        string_slice_start = 8
        string_slice_period = 12
        try:
            while True:
                if self.is_on==False:
                    ser.close()
                    break
                while ser.in_waiting:  # 若收到序列資料…
                    data_raw = ser.read_until(b'\r')
                    data = data_raw.decode()  # 用預設的UTF-8解碼
                    equipment_ID = data[:string_slice_start - 1]
                    altered_string = data[string_slice_start:string_slice_start + string_slice_period - 1]
                    altered_int = float(altered_string)
                    # print('接收到的原始資料：', data_raw)
                    # print('接收到的資料：', data)
                    # print('Measurement Data From : ', equipment_ID)
                    # print('Altered Data : ', altered_string)
                    # print('Altered Float : ', altered_int)
                    unit = list(data)
                    # I = ("I")
                    # if unit[-2] == I:
                    #     altered_int = ("%sin" % altered_int)
                    # else:
                    #     altered_int = ("%smm" % altered_int)
                    I = ("I")
                    if unit[-2] == I:
                        altered_unit = ("in" )
                    else:
                        altered_unit = ("mm")
                    a = []
                    a.append(altered_int)
                    a.append(equipment_ID)
                    a.append(altered_unit)
                    ser.close()
                    return a
        except:pass

def create_temp():
    # import tempfile
    # tmp_dir = tempfile.TemporaryDirectory()
    # print(tmp_dir.name)
    folder = os.path.exists(BASE_DIR + "\\measure_iteem_image")
    try:
        os.makedirs(BASE_DIR + "\\measure_item_image")
        print("建立目錄")
    except:
        path = (BASE_DIR + "\\measure_item_image")
        try:
            shutil.rmtree(path)
            print("刪除資料夾")
        except:
            pass
        os.makedirs(BASE_DIR + "\\measure_item_image")
        print("建立目錄")

def delet():
    path = (BASE_DIR+"\\measure_item_image")
    try:
        shutil.rmtree(path)
    except OSError as e:
        print(e)
    else:
        print("刪除資料夾")

if __name__ == '__main__' :
    # app = QtWidgets.QApplication(sys.argv)
    # w = TOOLWindow()
    # Form = QtWidgets.QWidget()
    # w.setupUi(Form)
    # w.show()
    # sys.exit(app.exec_())
    # TEMP_DIR =

    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    DIRT_TEMP = create_temp()

    app = QtWidgets.QApplication([])
    window = TOOLWindow()
    window.show()
    sys.exit(app.exec_())

