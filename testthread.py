# Form implementation generated from reading ui file 'display.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import socket

import time
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QCoreApplication
# from bluetooth import Protocols
import bluetooth
import sys
from time import sleep

from PyQt6.QtCore import QObject, QThread, pyqtSignal

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def run(self):
        """Long-running task."""
        print("Đang tìm kiếm các thiết bị Bluetooth xung quanh...")
        nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True)
        print("Các thiết bị Bluetooth xung quanh:")
        for addr, name in nearby_devices:
            # self.device_list.addItem(f"{addr} - {name}")
            self.progress.emit(f"{addr} - {name}")
            print(f"{addr} - {name}")
        self.finished.emit()
    def connect(self,id):
        option = id
        device_address = option[:17]
        port = 1  # RFCOMM port number
        # try:
        print(f"Đang kết nối đến thiết bị có địa chỉ {device_address}...")
        sock = bluetooth.BluetoothSocket(socket.BTPROTO_RFCOMM)
        sock.connect((device_address, port))
        while(1):
            pass
        self.finished.emit()
        # except Exception as e:
        #     print("Kết nối thất bại")
        #     return None


class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        # Tạo luồng và worker một lần duy nhất trong hàm __init__
        self.thread = {}

    def start_worker_1(self):
        self.thread[1] = ThreadClass(index=1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.my_function)
    def my_function(self, counter):
        m = counter
        i = self.MainWindow.sender().index
        self.image_label.setText(str(i))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(823, 537)
        self.MainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.image_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.image_label.setObjectName("image_label")
        self.horizontalLayout.addWidget(self.image_label)
        self.textEdit = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)
        self.horizontalLayout.setStretch(0, 6)
        self.horizontalLayout.setStretch(1, 4)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 3, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.connect_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.connect_button.setMinimumSize(QtCore.QSize(0, 40))
        self.connect_button.setObjectName("connect_button")
        self.horizontalLayout_2.addWidget(self.connect_button)
        self.device_list = QtWidgets.QComboBox(parent=self.centralwidget)
        self.device_list.setMinimumSize(QtCore.QSize(0, 40))
        self.device_list.setCurrentText("")
        self.device_list.setObjectName("device_list")
        self.horizontalLayout_2.addWidget(self.device_list)
        self.accept_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.accept_button.setMinimumSize(QtCore.QSize(0, 40))
        self.accept_button.setObjectName("accept_button")
        self.horizontalLayout_2.addWidget(self.accept_button)
        self.deny_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.deny_button.setMinimumSize(QtCore.QSize(0, 40))
        self.deny_button.setObjectName("deny_button")
        self.horizontalLayout_2.addWidget(self.deny_button)
        self.horizontalLayout_2.setStretch(0, 4)
        self.horizontalLayout_2.setStretch(1, 2)
        self.horizontalLayout_2.setStretch(2, 2)
        self.horizontalLayout_2.setStretch(3, 2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 823, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.image_label.setText(_translate("MainWindow", "                                     Hình ảnh sẽ được hiển thị tại đây"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Ten: Doan Quang Liu</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Loai phuong tien: O to</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Bien kiem soat: 51B-25121</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Toc do vi pham: 71km/h</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Toc do quy dinh: 50km/h</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Thoi diem ghi nhan: 15/11/2019 R:35</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Vi tri ghi nhan: Vi do 11,49</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">          Kinh do 109,46</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">          Vi tri Km480-900</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">          QL1A-Ha Tinh</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Thiet bi: 015737 Kiem dinh den 10_2020</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Don vi van hanh: Phong Canh sat Giao thong Cong an tinh Ha Tinh</span></p></body></html>"))
        self.connect_button.setText(_translate("MainWindow", "Bật Bluetooth"))
        self.accept_button.setText(_translate("MainWindow", "Đồng ý"))
        self.deny_button.setText(_translate("MainWindow", "Từ chối"))
        # self.connect_button.clicked.connect(self.connect)
        self.device_list.setPlaceholderText(_translate("MainWindow", "Danh sách thiết bị Bluetooth"))
        self.device_list.activated.connect(self.device_list_select)
        self.device_list.addItem("00:E1:33:13:D4:CE")
        # self.device_list.setDisabled(1)
        # self.accept_button.setDisabled(1)
        # self.deny_button.setDisabled(1)
        self.connect_button.clicked.connect(self.start_worker_1)

        
    def reportProgress(self, n):
        self.device_list.addItem(n)

    def connect(self):
        self.connect_button.setStyleSheet("background-color: #6495ED; color: white;")
        self.connect_button.setText("Đang chờ kết nối ...")
        QCoreApplication.processEvents()
        self.device_list.clear() 

        # Kiểm tra xem luồng tồn tại và đang chạy hay không
        if self.thread is not None and self.thread.isRunning():
            # Ngắt kết nối tín hiệu đã được kết nối trong __init__
            self.thread.started.disconnect()
            self.thread.started.connect(lambda: self.worker.connect(self.device_list.currentText()))

        self.connect_button.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.connect_button.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.connect_button.setStyleSheet("background-color: #66CDAA; color: white;")
        )
        self.thread.finished.connect(
            lambda: self.connect_button.setText("Đã bật Bluetooth!")
        )

    def device_list_select(self, text):
        if self.thread is not None and self.thread.isRunning():
            self.thread.started.disconnect()  # Ngắt kết nối tín hiệu đã được kết nối trong __init__
            self.thread.started.connect(lambda: self.worker.connect(self.device_list.currentText()))
        else:
            print("Luồng không tồn tại hoặc không đang chạy.")


class ThreadClass(QtCore.QThread):
    signal = pyqtSignal(int)

    def __init__(self, index=0):
        super().__init__()
        self.index = index

    def run(self):
        print('Starting thread...', self.index)
        counter = 0
        while True:
            
            client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            client.connect(("10:63:C8:75:7D:8A", 4))

            print(f"Connected!")

            try:
                while True:
                    message = input("Enter message: ")
                    client.send(message.encode('utf-8'))
                    data = client.recv(1024)
                    if not data:
                        break
                    print(f"Received: {data.decode('utf-8')}")

            except OSError:
                pass

            print("Disconnected")

            client.close()
            counter += 1
            print(counter)
            time.sleep(1)
            if counter == 5:
                counter = 0
            self.signal.emit(counter)

    def stop(self):
        print('Stopping thread...', self.index)
        self.terminate()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(w)
    w.show()
    sys.exit(app.exec())