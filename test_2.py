import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5 import QtCore, QtGui, QtWidgets

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Table(QWidget):
    def __init__(self):
        super(Table, self).__init__()
        self.initUI()

    def initUI(self):
        # 設置標題與初始大小
        self.setWindowTitle('QTableWidget demo')
        self.resize(500, 300)

        # 水平佈局，初始表格5*3，添加到佈局
        layout = QHBoxLayout()
        self.tableWidget = QTableWidget(5, 5)
        layout.addWidget(self.tableWidget)

        # 設置表格水平方向的頭標籤
        self.tableWidget.setHorizontalHeaderLabels([ '長', '寬', '高' ])

        # 設置水平方向自動伸縮填滿窗口
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 添加數據到指定行列
        newItem = QTableWidgetItem("888")
        self.tableWidget.setItem(0, 0, newItem)

        newItem = QTableWidgetItem("777")
        self.tableWidget.setItem(0, 1, newItem)

        newItem = QTableWidgetItem("160")
        self.tableWidget.setItem(0, 2, newItem)

        newItem = QTableWidgetItem("5000")
        self.tableWidget.setItem(1, 0, newItem)

        newItem = QTableWidgetItem("500")
        self.tableWidget.setItem(1, 1, newItem)

        newItem = QTableWidgetItem("120")
        self.tableWidget.setItem(1, 2, newItem)

        # 允許右鍵產生菜單
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        # 將右鍵菜單綁定到槽函數generateMenu
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)

        self.setLayout(layout)

    def generateMenu(self, pos):
        # 計算有多少條數據，默認-1,
        row_num = -1
        for i in self.tableWidget.selectionModel().selection().indexes():
            row_num = i.row()

        # 表格中只有兩條有效數據，所以只在前兩行支持右鍵彈出菜單
        if row_num < 2:
            menu = QMenu()
            item1 = menu.addAction(u'刪除')
            item2 = menu.addAction(u'設定')
            item3 = menu.addAction(u'我不知道他要幹嘛')
            action = menu.exec_(self.tableWidget.mapToGlobal(pos))
            # 顯示選中行的數據文本
            if action == item1:
                print('你選了選項一，當前行文字內容是：', self.tableWidget.item(row_num, 0).text(),
                      self.tableWidget.item(row_num, 1).text(),
                      self.tableWidget.item(row_num, 2).text())
            if action == item2:
                print('你選了選項二，當前行文字內容是：', self.tableWidget.item(row_num, 0).text(),
                      self.tableWidget.item(row_num, 1).text(),
                      self.tableWidget.item(row_num, 2).text())
            if action == item3:
                print('你選了選項三，當前行文字內容是：', self.tableWidget.item(row_num, 0).text(),
                      self.tableWidget.item(row_num, 1).text(),
                      self.tableWidget.item(row_num, 2).text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = Table()
    example.show()
    sys.exit(app.exec_())


# import sys, os
# from PyQt5.QtGui import QCursor, QIcon
# from PyQt5.QtWidgets import QApplication, QWidget, QMenu, QAction
# from PyQt5 import QtCore
# from PyQt5.QtCore import QSettings, QDateTime, Qt
# from testui import Ui_Form  # 引用UI文件，根据调用类型选择继承窗口类型：QMainWindow,QWidget,QDialog
#
# from PyQt5 import QtCore, QtGui, QtWidgets
#
#
# class Ui_Form(object):
#     def setupUi(self, Form):
#         Form.setObjectName("Form")
#         Form.resize(362, 310)
#         self.groupBox = QtWidgets.QGroupBox(Form)
#         self.groupBox.setGeometry(QtCore.QRect(50, 40, 241, 211))
#         self.groupBox.setObjectName("groupBox")
#         self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
#         self.lineEdit.setGeometry(QtCore.QRect(60, 70, 113, 20))
#         self.lineEdit.setObjectName("lineEdit")
#         self.pushButton = QtWidgets.QPushButton(self.groupBox)
#         self.pushButton.setGeometry(QtCore.QRect(30, 140, 75, 23))
#         self.pushButton.setObjectName("pushButton")
#         self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
#         self.pushButton_2.setGeometry(QtCore.QRect(140, 140, 75, 23))
#         self.pushButton_2.setObjectName("pushButton_2")
#
#         self.retranslateUi(Form)
#         QtCore.QMetaObject.connectSlotsByName(Form)
#
#     def retranslateUi(self, Form):
#         _translate = QtCore.QCoreApplication.translate
#         Form.setWindowTitle(_translate("Form", "Form"))
#         self.groupBox.setTitle(_translate("Form", "GroupBox"))
#         self.pushButton.setText(_translate("Form", "保存数据"))
#         self.pushButton_2.setText(_translate("Form", "删除数据"))
#
# class MyMainWindow(QWidget, Ui_Form):  # Widget界面时>>（QWidget,UI_。。），MainWindow类似
#     def __init__(self, parent=None):
#         super(MyMainWindow, self).__init__(parent)
#         self.setupUi(self)
#
#         # 按钮信号连接对象
#         self.pushButton.clicked.connect(self.button)
#         self.pushButton_2.clicked.connect(self.button_2)
#
#         # 声明在groupBox创建右键菜单
#         self.groupBox.setContextMenuPolicy(Qt.CustomContextMenu)
#         self.groupBox.customContextMenuRequested.connect(self.create_rightmenu)  # 连接到菜单显示函数
#
#     def button(self):
#         # 按钮1槽函数，进行数据保存
#         print('保存数据')
#
#     def button_2(self):
#         # 按钮2槽函数，删除数据
#         print('删除数据')
#
#     # 创建右键菜单函数
#     def create_rightmenu(self):
#         # 菜单对象
#         self.groupBox_menu = QMenu(self)
#
#         self.actionA = QAction(QIcon('image/保存.png'), u'保存数据',
#                                self)  # self.actionA = self.contextMenu.addAction(QIcon("images/0.png"),u'|  动作A')
#         self.actionA.setShortcut('Ctrl+S')  # 设置快捷键
#         self.groupBox_menu.addAction(self.actionA)  # 把动作A选项添加到菜单
#
#         self.actionB = QAction(QIcon('image/删除.png'), u'删除数据', self)
#         self.groupBox_menu.addAction(self.actionB)
#
#         self.actionA.triggered.connect(self.button)  # 将动作A触发时连接到槽函数 button
#         self.actionB.triggered.connect(self.button_2)
#
#         self.groupBox_menu.popup(QCursor.pos())  # 声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，
#
#
# if __name__ == "__main__":
#     # 适配2k高分辨率屏幕
#     QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
#     app = QApplication(sys.argv)
#     myWin = MyMainWindow()
#     myWin.show()
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QTableWidget,QPushButton,QApplication,QVBoxLayout,QTableWidgetItem,QCheckBox,QAbstractItemView,QHeaderView,QLabel,QFrame
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont,QColor
from faker import Factory
import random
import sys
class ui(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.id = 1
        self.lines = []
        self.editable = True
        self.des_sort = True
        self.faker = Factory.create()
        self.btn_add.clicked.connect(self.add_line)
        self.btn_del.clicked.connect(self.del_line)
        self.btn_modify.clicked.connect(self.modify_line)
        self.btn_select_line.clicked.connect(self.select_line)
        self.btn_select_single.clicked.connect(self.deny_muti_line)
        self.btn_sort.clicked.connect(self.sortItem)
        self.btn_set_header.clicked.connect(self.setheader)
        self.btn_set_middle.clicked.connect(self.middle)
        self.table.cellChanged.connect(self.cellchange)
        self.btn_noframe.clicked.connect(self.noframe)
#     # Sess = sessionmaker(bind = engine)
    def setupUI(self):
        self.setWindowTitle('欢迎加入微信公众号:python玩转网络 ')
        self.resize(640,480)
        self.table = QTableWidget(self)
        self.btn_add = QPushButton('增加')
        self.btn_del = QPushButton('删除')
        self.btn_modify = QPushButton('可以编辑')
        self.btn_select_line = QPushButton('选择整行')
        self.btn_select_single = QPushButton('禁止选多行')
        self.btn_sort = QPushButton('以分数排序')
        self.btn_set_header = QPushButton('标头设置')
        self.btn_set_middle = QPushButton('文字居中加颜色')
        self.btn_noframe = QPushButton('取消边框颜色交替')
        self.spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.btn_add)
        self.vbox.addWidget(self.btn_del)
        self.vbox.addWidget(self.btn_modify)
        self.vbox.addWidget(self.btn_select_line)
        self.vbox.addWidget(self.btn_select_single)
        self.vbox.addWidget(self.btn_sort)
        self.vbox.addWidget(self.btn_set_header)
        self.vbox.addWidget(self.btn_set_middle)
        self.vbox.addWidget(self.btn_noframe)
        self.vbox.addSpacerItem(self.spacerItem)  #可以用addItem也可以用addSpacerItem方法添加，没看出哪里不一样
        self.txt = QLabel()
        self.txt.setMinimumHeight(50)
        self.vbox2 = QVBoxLayout()
        self.vbox2.addWidget(self.table)
        self.vbox2.addWidget(self.txt)
        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.vbox2)
        self.hbox.addLayout(self.vbox)
        self.setLayout(self.hbox)
        self.table.setColumnCount(4)   ##设置列数
        self.headers = ['id','选择','姓名','成绩','住址']
        self.table.setHorizontalHeaderLabels(self.headers)
        self.show()
    def add_line(self):
        self.table.cellChanged.disconnect()
        row = self.table.rowCount()
        self.table.setRowCount(row + 1)
        id = str(self.id)
        ck = QCheckBox()
        h = QHBoxLayout()
        h.setAlignment(Qt.AlignCenter)
        h.addWidget(ck)
        w = QWidget()
        w.setLayout(h)
        name = self.faker.name()
        score = str(random.randint(50,99))
        add = self.faker.address()
        self.table.setItem(row,0,QTableWidgetItem(id))
        self.table.setCellWidget(row,1,w)
        self.table.setItem(row,2,QTableWidgetItem(name))
        self.table.setItem(row,3,QTableWidgetItem(score))
        self.table.setItem(row,4,QTableWidgetItem(add))
        self.id += 1
        self.lines.append([id,ck,name,score,add])
        self.settext('自动生成随机一行数据！,checkbox设置为居中显示')
        self.table.cellChanged.connect(self.cellchange)
    def del_line(self):
        removeline = []
        for line in self.lines:
            if line[1].isChecked():
                row = self.table.rowCount()
                for x in range(row,0,-1):
                    if line[0] == self.table.item(x - 1,0).text():
                        self.table.removeRow(x - 1)
                        removeline.append(line)
        for line in removeline:
            self.lines.remove(line)
        self.settext('删除在左边checkbox中选中的行，使用了一个笨办法取得行号\n，不知道有没有其他可以直接取得行号的方法！')
    def modify_line(self):
        if self.editable == True:
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.btn_modify.setText('禁止编辑')
            self.editable = False
        else:
            self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
            self.btn_modify.setText('可以编辑')
            self.editable = True
        self.settext('设置，是否可以编辑整个表格')
    def select_line(self):
        if self.table.selectionBehavior() == 0:
            self.table.setSelectionBehavior(1)
            self.btn_select_line.setStyleSheet('background-color:lightblue')
        else:
            self.table.setSelectionBehavior(0)
            self.btn_select_line.setStyleSheet('')
        self.settext('默认时，点击单元格，只可选择一个格，此处设置为可选择整行')

    def deny_muti_line(self):
        if self.table.selectionMode() in [2,3]:
            self.table.setSelectionMode(QAbstractItemView.SingleSelection)
            self.btn_select_single.setStyleSheet('background-color:lightblue')
        else:
            self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
            self.btn_select_single.setStyleSheet('')
        self.settext('点击时会轮换以多行或单行选择，默认是可以同时选择多行')
    def sortItem(self):
        if self.des_sort == True:
            self.table.sortItems(3,Qt.DescendingOrder)
            self.des_sort = False
            self.btn_sort.setStyleSheet('background-color:lightblue')
            self.table.setSortingEnabled(True)  # 设置表头可以自动排序
        else:
            self.table.sortItems(3,Qt.AscendingOrder)
            self.des_sort = True
            self.btn_sort.setStyleSheet('background-color:lightblue')
            self.table.setSortingEnabled(False)
        self.settext('点击时会轮换以升序降序排列，但排序时，会使自动列宽失效！')
    def setheader(self):
        font = QFont('微软雅黑', 12)
        font.setBold(True)
        self.table.horizontalHeader().setFont(font)  # 设置表头字体
        self.table.setColumnWidth(0,50)
        self.table.setColumnWidth(1,50)
        self.table.setColumnWidth(3,100)
        self.table.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
        self.table.horizontalHeader().setStyleSheet('QHeaderView::section{background:gray}')
        self.table.horizontalHeader().setFixedHeight(50)
        self.table.setColumnHidden(0,True)
        self.btn_set_header.setStyleSheet('background-color:lightblue')
        self.settext('设置标头字体及字号，隐藏ID列，设置标头除姓名外全部为固定宽度\n，设置姓名列自动扩展宽度，设置标头行高，设置标头背景色')
    def middle(self):
        self.btn_set_middle.setStyleSheet('background-color:lightblue')
        self.table.setStyleSheet('color:green;')
        row = self.table.rowCount()
        for x in range(row):
            for y in range(4):
                if y != 1:
                    item = self.table.item(x,y)
                    item.setTextAlignment(Qt.AlignCenter)
                else:
                    pass
        self.btn_set_middle.setStyleSheet('background-color:lightblue')
        self.settext('将文字居中显示,设置文字颜色')
    def cellchange(self,row,col):
        item = self.table.item(row,col)
        txt = item.text()
        self.settext('第%s行，第%s列 , 数据改变为:%s'%(row,col,txt))
    def noframe(self):
        self.table.setAlternatingRowColors(True)
        self.table.setFrameStyle(QFrame.NoFrame)
        self.table.setStyleSheet('color:green;'
                                 'gridline-color:white;'
                                 'border:0px solid gray')
        self.settext('取消表的框线,\n 取消表格内框')

    def settext(self,txt):
        font = QFont('微软雅黑',10)
        self.txt.setFont(font)
        self.txt.setText(txt)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = ui()
    sys.exit(app.exec_())