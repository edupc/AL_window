import sys
from PyQt5.QtWidgets import QMainWindow,QHBoxLayout,QPushButton,QApplication,QWidget

'''
主視窗:關閉主視窗
'''

class MainWin(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        #標題設定
        self.setWindowTitle('關閉主視窗例子')
        #按鈕
        self.button1=QPushButton('關閉主視窗')
        self.button1.clicked.connect(self.onButtonClick)
        #佈局--水平佈局
        layout=QHBoxLayout()
        layout.addWidget(self.button1)
        #視窗中心控制元件
        main_frame=QWidget()
        main_frame.setLayout(layout)
        self.setCentralWidget(main_frame)

    def onButtonClick(self):
        '''按鈕槽函式封裝'''
        #獲取訊號傳送物件
        sender=self.sender()
        #列印訊號傳送物件的文字+列印輸出
        print(sender.text()+'被按下了')
        #建立QApplication物件並呼叫quit方法
        qApp=QApplication.instance()
        qApp.quit()

if __name__=="__main__":
    app=QApplication(sys.argv)
    myMainWin=MainWin()
    myMainWin.show()
    sys.exit(app.exec_())