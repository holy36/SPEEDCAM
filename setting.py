# Form implementation generated from reading ui file 'setting.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1115, 824)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(110, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.bground = QtWidgets.QPushButton(parent=self.centralwidget)
        self.bground.setEnabled(False)
        self.bground.setMinimumSize(QtCore.QSize(40, 30))
        self.bground.setText("")
        self.bground.setObjectName("bground")
        self.horizontalLayout_3.addWidget(self.bground)
        self.information_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.information_button.setMinimumSize(QtCore.QSize(40, 30))
        self.information_button.setText("")
        self.information_button.setObjectName("information_button")
        self.horizontalLayout_3.addWidget(self.information_button)
        self.horizontalLayout_3.setStretch(1, 25)
        self.horizontalLayout_3.setStretch(2, 2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.set_infor = QtWidgets.QLabel(parent=self.centralwidget)
        self.set_infor.setText("")
        self.set_infor.setObjectName("set_infor")
        self.verticalLayout.addWidget(self.set_infor)
        self.bground_setting = QtWidgets.QPushButton(parent=self.centralwidget)
        self.bground_setting.setEnabled(True)
        self.bground_setting.setMinimumSize(QtCore.QSize(0, 50))
        self.bground_setting.setObjectName("bground_setting")
        self.verticalLayout.addWidget(self.bground_setting)
        self.time_set = QtWidgets.QPushButton(parent=self.centralwidget)
        self.time_set.setMinimumSize(QtCore.QSize(0, 35))
        self.time_set.setObjectName("time_set")
        self.verticalLayout.addWidget(self.time_set)
        self.check_set = QtWidgets.QPushButton(parent=self.centralwidget)
        self.check_set.setMinimumSize(QtCore.QSize(0, 35))
        self.check_set.setObjectName("check_set")
        self.verticalLayout.addWidget(self.check_set)
        self.auto_connecT_setting = QtWidgets.QPushButton(parent=self.centralwidget)
        self.auto_connecT_setting.setMinimumSize(QtCore.QSize(0, 50))
        self.auto_connecT_setting.setObjectName("auto_connecT_setting")
        self.verticalLayout.addWidget(self.auto_connecT_setting)
        self.auto_connect = QtWidgets.QPushButton(parent=self.centralwidget)
        self.auto_connect.setObjectName("auto_connect")
        self.verticalLayout.addWidget(self.auto_connect)
        self.fixed_set = QtWidgets.QPushButton(parent=self.centralwidget)
        self.fixed_set.setMinimumSize(QtCore.QSize(0, 50))
        self.fixed_set.setObjectName("fixed_set")
        self.verticalLayout.addWidget(self.fixed_set)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.time_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.time_label.setText("")
        self.time_label.setObjectName("time_label")
        self.horizontalLayout_2.addWidget(self.time_label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 16)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_2.setStretch(1, 18)
        self.gridLayout.addLayout(self.verticalLayout_2, 2, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.bground_setting.setText(_translate("MainWindow", "Cài đặt tự động xác nhận bản tin"))
        self.time_set.setText(_translate("MainWindow", "Thời gian chờ tự động xác nhận"))
        self.check_set.setText(_translate("MainWindow", "Lựa chọn tự động xác nhận"))
        self.auto_connecT_setting.setText(_translate("MainWindow", "Cài đặt tự động kết nối thiết bị Bluetooth"))
        self.auto_connect.setText(_translate("MainWindow", "Đổi địa chỉ MAC thiết bị muốn kết nối"))
        self.fixed_set.setText(_translate("MainWindow", "Đặt lại cài đặt"))
