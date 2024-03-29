from PyQt6 import QtCore, QtGui,QtWidgets,uic
from PyQt6.QtWidgets import QDialog,QApplication,QMessageBox,QMainWindow,QListWidgetItem
from PyQt6.uic import loadUi
import sys
import mysql.connector
import datetime
import bluetooth
import display

class loginUi(display.Ui_MainWindow): #login window
    def __init__(self):
        super(loginUi,self).__init__()
        uic.loadUi('display.ui',self) #goi ui chuong trinh
        
        self.connect_button.clicked.connect(self.connect)


    def connect(self):
        print("Đang tìm kiếm các thiết bị Bluetooth xung quanh...")
        nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True)
        print("Các thiết bị Bluetooth xung quanh:")
        for addr, name in nearby_devices:
            print(f"{addr} - {name}")
        self.connect_button.setStyleSheet("background-color: green; color: white;")


app =QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
Login_f = loginUi()


widget.addWidget(Login_f)
widget.setCurrentIndex(0)
widget.setFixedHeight(602)
widget.setFixedWidth(804)
widget.show()
app.exec()