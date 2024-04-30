from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        
        # Central Widget
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Existing Push Button
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 110, 251, 341))
        self.pushButton.setObjectName("pushButton")
        
        # Existing TextEdit
        self.textEdit = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(330, 30, 461, 511))
        self.textEdit.setObjectName("textEdit")
        
        # New Clear Button
        self.clearButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.clearButton.setGeometry(QtCore.QRect(40, 460, 251, 50))  # Định vị mới
        self.clearButton.setObjectName("clearButton")  # Đặt tên mới

        # Set the central widget
        MainWindow.setCentralWidget(self.centralwidget)

        # Menu Bar and Status Bar
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
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
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.clearButton.setText(_translate("MainWindow", "Xóa Chữ"))  # Văn bản trên nút mới
