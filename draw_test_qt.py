from PyQt5 import QtWidgets, QtGui ,QtCore
from PyQt5.QtWidgets import QMessageBox, QAbstractItemView, QTableWidgetItem
from draw_test import Ui_MainWindow
import sys, re, time, serial.tools.list_ports
import toolconnect, sql_connect, measure
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtWidgets, QtGui
from draw_test import Ui_MainWindow
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
#         self.plot_()
#         self.measure_value = measure_thread()
#         self.measure_value.measure_value.connect(self.setmeasurevalue)
#
#         self.tb = self.addToolBar("open")
#         self.new = QtWidgets.QAction(QtGui.QIcon(BASE_DIR + "\\po.png"), "UP project", self)
#         self.tb.addAction(self.new)
#         self.new = QtWidgets.QAction(QtGui.QIcon(BASE_DIR + "\\project_item.png"), "project_item", self)
#         self.tb.addAction(self.new)
#         self.new = QtWidgets.QAction(QtGui.QIcon(BASE_DIR + "\\measure_choose.png"), "project_choose", self)
#         self.tb.addAction(self.new)
#     def plot_(self):
#         ax = self.ui.figure.add_axes([0.125, 0.125, 0.8, 0.8])
#         ax.plot([0.002, 0.0012, 0.003, 0.002, 0.002], marker='.', mfc='w', label="量測數值") #ro = 定義點狀
#         ax.plot([0.003, 0.003, 0.003, 0.003, 0.003], label="上限")
#         plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  #設置中文字 不然打不出來
#         plt.xlabel("量測次數")
#         plt.ylabel("量測數值")
#         plt.legend()
#         # self.ui.canvas.draw()
#     def setmeasurevalue(self,value):
#         print(value)
# class measure_thread(QThread):
#     measure_value = pyqtSignal(str)
#     measure_tool_name = pyqtSignal(str)
#     measure_unit = pyqtSignal(str)
#     def __init__(self, parent=None):
#         super(measure_thread, self).__init__(parent)
#         self.is_on = True
#     def set_port(self, port):
#         self.set_port = port
#     def run(self):
#         while self.is_on:
#             returenlist = self.serial_test(self.set_port)
#             if self.is_on == False:
#                 break
#             self.measure_value.emit(str(returenlist[0]))
#             self.measure_tool_name.emit(str(returenlist[1]))
#             self.measure_unit.emit(str(returenlist[2]))
#
#     def serial_test(self,comnumber):
#         COM_PORT = ("COM%s" % comnumber)  # 指定通訊埠名稱
#         BAUD_RATES = 57600  # 設定傳輸速率
#         BYTE_SIZE = 8
#         PARITY = 'N'
#         STOP_BITS = 1
#         ser = serial.Serial(COM_PORT, BAUD_RATES, BYTE_SIZE, PARITY, STOP_BITS, timeout=None)
#         string_slice_start = 8
#         string_slice_period = 12
#         try:
#             while True:
#                 if self.is_on==False:
#                     ser.close()
#                     break
#                 while ser.in_waiting:  # 若收到序列資料…
#                     data_raw = ser.read_until(b'\r')
#                     data = data_raw.decode()  # 用預設的UTF-8解碼
#                     equipment_ID = data[:string_slice_start - 1]
#                     altered_string = data[string_slice_start:string_slice_start + string_slice_period - 1]
#                     altered_int = float(altered_string)
#                     # print('接收到的原始資料：', data_raw)
#                     # print('接收到的資料：', data)
#                     # print('Measurement Data From : ', equipment_ID)
#                     # print('Altered Data : ', altered_string)
#                     # print('Altered Float : ', altered_int)
#                     unit = list(data)
#                     # I = ("I")
#                     # if unit[-2] == I:
#                     #     altered_int = ("%sin" % altered_int)
#                     # else:
#                     #     altered_int = ("%smm" % altered_int)
#                     I = ("I")
#                     if unit[-2] == I:
#                         altered_unit = ("in" )
#                     else:
#                         altered_unit = ("mm")
#                     a = []
#                     a.append(altered_int)
#                     a.append(equipment_ID)
#                     a.append(altered_unit)
#                     ser.close()
#                     return a
#         except:pass

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())






