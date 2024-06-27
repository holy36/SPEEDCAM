import socket
import shutil
import psutil
import time
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QCoreApplication
import bluetooth
import sys
from time import sleep
from PyQt6.QtWidgets import QMenuBar, QCheckBox, QHeaderView, QHBoxLayout, QVBoxLayout, QTableWidget, QApplication, QMainWindow, QSizePolicy, QVBoxLayout, QWidget, QPinchGesture, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QMessageBox, QDialog, QInputDialog, QTableWidgetItem, QTextEdit
from PyQt6.QtGui import QPixmap, QPainter,QFont, QAction, QPalette, QColor
from PyQt6.QtCore import QObject, QThread, pyqtSignal, Qt,QEvent, QPoint, QPointF  
import display,search
from PyQt6.QtWidgets import (
    QDateTimeEdit,QSpinBox, QLineEdit,QVBoxLayout, QComboBox, QTimeEdit, QDialogButtonBox,QLabel, QPushButton, QCalendarWidget)
from PyQt6.QtCore import QDateTime, Qt
import base64
import os
import struct
import re
import datetime
import exifread
import mysql.connector

# 10:63:c8:75:7d:8a


def des_scrollbar_table(table):
        scrollbar_style = """
            QScrollBar:vertical {
                border: none;
                background: #f1f1f1;
                width: 25px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #34ebe5;  /* Blue color */
                min-height: 20px;
            }
            QScrollBar::add-line:vertical {
                background: #f1f1f1;
                height: 20px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                background: #f1f1f1;
                height: 20px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar:horizontal {
                border: none;
                background: #f1f1f1;
                height: 25px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:horizontal {
                background: #34ebe5;  /* Blue color */
                min-width: 20px;
            }
            QScrollBar::add-line:horizontal {
                background: #f1f1f1;
                width: 20px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:horizontal {
                background: #f1f1f1;
                width: 20px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }
        """

        table.verticalScrollBar().setStyleSheet(scrollbar_style)
        table.horizontalScrollBar().setStyleSheet(scrollbar_style)

class DeviceDialog(QDialog):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window  # Đây là cách chính xác để truyền tham chiếu của MainWindow vào DeviceDialog

        self.setWindowTitle("Danh sách các Thiết bị Bluetooth đã lưu trữ")
        self.setGeometry(100, 100, 1000, 600)
        
        self.db = mysql.connector.connect(
            user='mobeo2002',
            password='doanquangluu',
            host='localhost',
            database='speed_gun'
        )
        
        self.initUI()
        self.initMenuBar()

        
    def initUI(self):
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Tên", "Địa chỉ MAC", "Mô tả", "Xóa"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        self.table.setRowHeight(0, 50)  # Thiết lập chiều cao cho hàng đầu tiên là 50 pixel
        self.table.setRowHeight(1, 40)  # Thiết lập chiều cao cho hàng thứ hai là 40 pixel
        # Tiếp tục thiết lập cho các hàng khác nếu cần
        
        # Thiết lập chiều rộng cho mỗi cột
        self.table.setColumnWidth(0, 200)  # Thiết lập kích thước cho cột "Tên" là 200 pixel
        self.table.setColumnWidth(1, 200)  # Thiết lập kích thước cho cột "Địa chỉ MAC" là 200 pixel
        self.table.setColumnWidth(2, 300)  # Thiết lập kích thước cho cột "Mô tả" là 300 pixel
        self.table.setColumnWidth(3, 100)  # Thiết lập kích thước cho cột "Xóa" là 100 pixel
        des_scrollbar_table(self.table)
        self.load_devices()
        
        button_layout = QHBoxLayout()

        list_connect = QPushButton("Kết nối")
        list_connect.clicked.connect(self.connect_device)
        button_layout.addWidget(list_connect)
        list_connect.setFixedSize(200,100)
        
        add_button = QPushButton("Thêm thiết bị")
        add_button.clicked.connect(self.add_device)
        button_layout.addWidget(add_button)
        add_button.setFixedSize(200,100)

        edit_button = QPushButton("Sửa thông tin")
        edit_button.clicked.connect(self.edit_device)
        button_layout.addWidget(edit_button)
        layout.addLayout(button_layout)
        edit_button.setFixedSize(200,100)

        delete_button = QPushButton("Xóa thiết bị")
        delete_button.clicked.connect(self.delete_device)
        button_layout.addWidget(delete_button)
        delete_button.setFixedSize(200,100)
        
        quit_button = QPushButton("Đóng cửa sổ")
        icon = QtGui.QIcon()  # Tạo một đối tượng QIcon
        pixmap = QtGui.QPixmap(resource_path("icon/quit.png"))  # Tạo QPixmap từ đường dẫn hình ảnh
        icon.addPixmap(pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)  # Thêm pixmap vào icon
        quit_button.setIcon(icon)  # Đặt icon cho phần tử giao diện
        quit_button.setIconSize(QtCore.QSize(30,30))  # Đặt kích thước icon
        quit_button.clicked.connect(self.quit_dialog)
        button_layout.addWidget(quit_button)
        quit_button.setFixedSize(200,100)

        self.setLayout(layout)

    def quit_dialog(self):
        self.accept()
    def initMenuBar(self):
        menu_bar = QMenuBar(self)
        help_menu = menu_bar.addMenu("[Hướng dẫn]")
        menu_bar.setFixedSize(1100,50)
        menu_bar.setStyleSheet("background: qlineargradient(x1:0 y1:0, x2:1 y2:0, stop:0 white, stop:1 #42ddf5); color: black; font-size: 20pt; ")
        help_action = QAction("Hiển thị hướng dẫn sử dụng", self)
        help_action.triggered.connect(self.show_help)
        
        help_menu.addAction(help_action)
     
        # Check if layout exists and set the menu bar
        if self.layout():
            self.layout().setMenuBar(menu_bar)
        else:
            layout = QVBoxLayout()
            self.setLayout(layout)
            layout.setMenuBar(menu_bar)
    def show_help(self):
# Tạo thông báo với hướng dẫn
        instructions = (
            "Mục đích: Để thuận tiện cho việc kết nối mà không cần nhập địa chỉ MAC hay đợi quét thiết bị xung quanh, người sử dụng có thể lưu các thiết bị Bluetooth mong muốn để thuận tiện cho việc kết nối trong tương lai.\n\n"
            "Chức năng:\n"
            "*   Kết nối: Người dùng có thể chọn trực tiếp vào ô chứa tên hoặc địa chỉ MAC của thiết bị muốn kết nối và nhấn nút \"Kết nối\". Sau đó, Thiết bị 2 sẽ cố gắng kết nối tới thiết bị chỉ định và tự động đóng cửa sổ danh sách.\n"
            "*   Thêm thiết bị: Người dùng có thể thêm thiết bị mong muốn lưu bằng cách nhập tên và địa chỉ MAC của thiết bị (bắt buộc) và có thể thêm mô tả về thiết bị nếu muốn (không bắt buộc).\n"
            "*   Sửa thông tin thiết bị: Người dùng có thể chọn trực tiếp vào ô chứa tên hoặc địa chỉ MAC của thiết bị muốn sửa thông tin và nhấn nút \"Sửa thông tin\". Tại đây, người dùng có thể thay đổi cả ba thông tin. Tuy nhiên, lưu ý rằng nếu tên và địa chỉ MAC được thay đổi trùng với thiết bị đã được lưu, thì đối tượng được sửa mặc định là thiết bị đã được lưu.\n"
            "*   Xóa thiết bị: Người dùng có thể chọn các thiết bị bằng cách sử dụng ô checkbox ở cột cuối, sau đó nhấn nút \"Xóa thiết bị\". Thông tin về các thiết bị này sẽ bị xóa khỏi cơ sở dữ liệu."
        )


        dialog = QDialog(self)
        dialog.setWindowTitle("Hướng dẫn sử dụng chức năng Danh sách lưu Thiết bị Bluetooth")
        dialog.resize(800, 500)  # Đặt kích thước của QDialog

        text_edit = QTextEdit()
        text_edit.setText(instructions)
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("font-size: 16px;")  # Điều chỉnh cỡ chữ ở đây

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(dialog.accept)

        # Thiết lập kích thước nút Ok
        ok_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_button.setFixedSize(200, 80)  # Đặt kích thước nút Ok

        layout = QVBoxLayout()
        layout.addWidget(text_edit)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec()   
    def connect_device(self):
        selected_device = None
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).isSelected() or self.table.item(row, 1).isSelected():
                selected_device = (self.table.item(row, 0).text(), self.table.item(row, 1).text())
                break
        if selected_device:
            # self.thread = {}
            self.main_window.thread[2] = ThreadClass(index=1, mac_id=selected_device[1])
            self.main_window.thread[2].start()
            self.main_window.thread[2].signal.connect(self.main_window.my_function)
            self.main_window.thread[2].connect_status.connect(self.main_window.status_change)
            self.accept()
        else:
            QMessageBox.warning(self, "Cảnh báo", "Hãy chọn 1 thiết bị để kết nối!!!")

    def edit_device(self):
        selected_device = None
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).isSelected() or self.table.item(row, 1).isSelected():
                selected_device = (self.table.item(row, 0).text(), self.table.item(row, 1).text(), self.table.item(row, 2).text())
                break
        if selected_device:
            dialog = QDialog(self)
            dialog.setWindowTitle("Sửa thông tin thiết bị")
            dialog.setGeometry(100, 100, 300, 200)

            layout = QVBoxLayout()

            name_label = QLabel("Nhập tên thiết bị:")
            layout.addWidget(name_label)

            name_input = QLineEdit()
            name_input.setText(selected_device[0])
            layout.addWidget(name_input)

            mac_label = QLabel("Nhập địa chỉ MAC:")
            layout.addWidget(mac_label)

            mac_input = QLineEdit()
            mac_input.setText(selected_device[1])
            layout.addWidget(mac_input)

            describe_label = QLabel("Nhập mô tả (Không bắt buộc):")
            layout.addWidget(describe_label)

            describe_input = QLineEdit()
            describe_input.setText(selected_device[2])
            layout.addWidget(describe_input)

            error_label = QLabel("")
            error_label.setStyleSheet("color: red")
            layout.addWidget(error_label)

            button_layout = QHBoxLayout()

            ok_button = QPushButton("OK")
            def on_ok():
                name = name_input.text()
                mac_address = mac_input.text()
                describe = describe_input.text() if describe_input.text() else "No description"

                if not name or not mac_address:
                    error_label.setText("Tên thiết bị và địa chỉ MAC không thể để trống")
                    return

                cursor = self.db.cursor()
                cursor.execute("UPDATE device_mac_address SET name = %s, `describe` = %s WHERE mac_address = %s",
                            (name, describe, mac_address))
                self.db.commit()  # Đảm bảo lưu các thay đổi vào cơ sở dữ liệu
                cursor.close()
                dialog.accept()

                # Sau khi người dùng chỉnh sửa và nhấn OK, ta cần tải lại danh sách thiết bị để cập nhật giao diện
                self.load_devices()

            ok_button.clicked.connect(on_ok)  # Kích hoạt hàm on_ok() khi nút OK được nhấn
            button_layout.addWidget(ok_button)

            cancel_button = QPushButton("Hủy")
            cancel_button.clicked.connect(dialog.reject)
            button_layout.addWidget(cancel_button)

            layout.addLayout(button_layout)
            dialog.setLayout(layout)
            dialog.exec()
                                
    def load_devices(self):
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        cursor = self.db.cursor()
        cursor.execute("SELECT name, mac_address, `describe` FROM device_mac_address")
        devices = cursor.fetchall()
        self.table.setRowCount(len(devices))
        for row_num, device in enumerate(devices):
            self.table.setItem(row_num, 0, QTableWidgetItem(device[0]))
            self.table.setItem(row_num, 1, QTableWidgetItem(device[1]))
            self.table.setItem(row_num, 2, QTableWidgetItem(device[2]))
            checkbox = QCheckBox()
            checkbox.setStyleSheet("QCheckBox::indicator { width:30px; height: 30px;} QCheckBox{margin-left: 100px;} ")
            self.table.setCellWidget(row_num, 3, checkbox)
        cursor.close()

    def add_device(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Thêm thiết bị Bluetooth muốn lưu trữ")
        dialog.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()
        
        name_label = QLabel("Nhập tên thiết bị:")
        layout.addWidget(name_label)

        name_input = QLineEdit()
        name_input.setPlaceholderText("Nhập tên thiết bị")
        layout.addWidget(name_input)

        mac_label = QLabel("Nhập địa chỉ MAC:")
        layout.addWidget(mac_label)

        mac_input = QLineEdit()
        mac_input.setPlaceholderText("Nhập địa chỉ MAC")
        layout.addWidget(mac_input)

        describe_label = QLabel("Nhập mô tả:")
        layout.addWidget(describe_label)

        describe_input = QLineEdit()
        describe_input.setPlaceholderText("Nhập mô tả")
        layout.addWidget(describe_input)
        
        error_label = QLabel("")
        error_label.setStyleSheet("color: red")
        layout.addWidget(error_label)
        
        button_layout = QHBoxLayout()
        
        ok_button = QPushButton("OK")
        def on_ok():
            name = name_input.text()
            mac_address = mac_input.text()
            describe = describe_input.text() if describe_input.text() else "Không có mô tả"
            
            if not name or not mac_address:
                error_label.setText("Tên thiết bị và địa chỉ không thể để trống !!!")
                return

            cursor = self.db.cursor()
            cursor.execute("INSERT INTO device_mac_address (name, mac_address, `describe`) VALUES (%s, %s, %s)",
                           (name, mac_address, describe))
            self.db.commit()
            cursor.close()
            self.load_devices()
            dialog.accept()

        ok_button.clicked.connect(on_ok)
        button_layout.addWidget(ok_button)
        
        cancel_button = QPushButton("Hủy")
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec()
        
    def delete_device(self):
        cursor = self.db.cursor()
        for row in range(self.table.rowCount()):
            widget = self.table.cellWidget(row, 3)
            if isinstance(widget, QCheckBox) and widget.isChecked():
                mac_address = self.table.item(row, 1).text()
                cursor.execute("DELETE FROM device_mac_address WHERE mac_address = %s", (mac_address,))
        self.db.commit()
        cursor.close()
        self.load_devices()

class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPointF)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self.shown = False
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.grabGesture(Qt.GestureType.PinchGesture)
        self.setScene(self._scene)
        self.setTransformationAnchor(
            QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(
            QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

    def event(self,event):
        if event.type() == QEvent.Type.Gesture:
            gesture = event.gesture(Qt.GestureType.PinchGesture)
            # print(gesture)
            if gesture:
                self.handle_pinch(gesture)
                return True
        return super().event(event)

    def handle_pinch(self, gesture):
        scale_factor = gesture.scaleFactor()
        if(scale_factor>1):
            self._zoom +=(scale_factor-1)
        else:
            self._zoom -=(1-scale_factor)
        if self._zoom > 0:
            self.scale(scale_factor,scale_factor)
        else:
            self.fitInView()
        print(scale_factor)

    def hasPhoto(self):
        return not self._empty

    def showEvent(self, event):
        super().showEvent(event)
        if not self.shown:
            self.shown = True
    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                print(viewrect)
                print(scenerect)
                print(unity)
                self.scale(factor, factor)
                pass
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom <= 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.DragMode.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.position().toPoint()))
        super(PhotoViewer, self).mousePressEvent(event)

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def run(self):
        print("Đang tìm kiếm các thiết bị Bluetooth xung quanh...")
        nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True)
        print("Các thiết bị Bluetooth xung quanh:")
        for addr, name in nearby_devices:
            self.progress.emit(f"{addr} - {name}")
            print(f"{addr} - {name}")
        self.finished.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = display.Ui_MainWindow()
        self.uic.setupUi(self)
        self.viewer = PhotoViewer(self)
        self.searchUiDef = SearchUI()
        self.uic.image_layout.addWidget(self.viewer)
        self.viewer.setPhoto(QtGui.QPixmap(resource_path(resource_path('no_photo.png'))))
        self.thread = {}
        self.grabGesture(Qt.GestureType.PinchGesture)
        self.uic.connect_button.clicked.connect(self.connect)
        self.uic.connect_button.setStyleSheet("font-size: 13pt;")
        self.uic.cancel_button.clicked.connect(self.cancel_connection)
        self.uic.device_list.setPlaceholderText( "Danh sách thiết bị Bluetooth")
        self.uic.device_list.setStyleSheet("font-size: 13pt;")
        self.uic.device_list.activated.connect(self.device_list_select)
        self.uic.cancel_button.setStyleSheet("background-color: #66CDAA; color: white;")
        self.uic.quitbutton.clicked.connect(self.exit)
        self.uic.minbutton.clicked.connect(self.minimize_window)
        self.uic.maxbutton.clicked.connect(self.maximize_window)
        self.uic.search_button.clicked.connect(self.search_information)
        self.uic.search_button.setStyleSheet("font-size: 13pt;")
        self.uic.information_button.clicked.connect(self.show_information)
        self.uic.bground.setStyleSheet("background-color: #949084; color: white;")
        self.uic.bground.setText("Thiết bị truy cập trực tiếp máy bắn - SPR Lab")
        self.uic.bground.setStyleSheet("font-size: 13pt;")
        self.uic.connect_with_mac.setText("Kết nối bằng địa chỉ MAC")
        self.uic.list_device_saved.setText("Thiết bị Bluetooth đã lưu")
        self.uic.list_device_saved.setStyleSheet("font-size: 13pt;")
        self.uic.connect_with_mac.setStyleSheet("font-size: 13pt;")
        self.uic.list_device_saved.clicked.connect(self.show_device_dialog)
        self.uic.accept_button.setText("Gửi lên Server")
        self.uic.deny_button.setText("Chụp lại ảnh mới")
        self.uic.device_list.setMaximumWidth(0)
        self.uic.accept_button.setStyleSheet(
    "* {color: black; font-size: 15pt;"
    "background-color: #95f5b7;}"
)
        self.uic.deny_button.setStyleSheet(
            "* {color: black; font-size: 15pt;"
    "background-color: #d99886;}"
)    
        self.uic.instruction_text.setText("Sau khi nhận được bản tin, người sử dụng có hai lựa chọn:\n- Nhấn nút 'Gửi lên Server' (nút màu xanh) nếu chấp nhận bản tin đạt chuẩn và muốn gửi lên Server.\n- Nhấn nút 'Chụp lại ảnh mới' (nút màu đỏ) nếu hình ảnh chưa đạt chuẩn và yêu cầu Máy bắn tốc độ chụp lại ảnh mới.")
        self.uic.instruction_text.setStyleSheet("font-size: 13pt;")
        self.uic.instruction_text.setDisabled(1)
        self.uic.bground_2.setStyleSheet("background-color: #596063; color: white; font-size: 16pt;")
        self.uic.textEdit.clear()
        self.uic.connect_with_mac.clicked.connect(self.connect_with_address)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.showMaximized()
        self.viewer.fitInView()
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) 
        self.uic.bground.setDisabled(True)
        self.uic.bground.mousePressEvent = self.mousePressEvent
        self.clickPosition = QPoint()
        self.setWindowTitle("Hệ thống xử lý vi phạm tốc độ")
        self.setWindowIcon(QtGui.QIcon(resource_path("icon/csgt.png")))
        self.setIcon(resource_path("icon/min2.png"), self.uic.minbutton)
        self.setIcon(resource_path("icon/connect_with_mac.png"), self.uic.connect_with_mac, icon_size=(30, 35))  # Kích thước tùy chỉnh
        self.setIcon(resource_path("icon/quit.png"), self.uic.quitbutton, icon_size=(30, 35))  # Kích thước tùy chỉnh
        self.setIcon(resource_path("icon/min.png"), self.uic.maxbutton, icon_size=(30, 35))
        self.setIcon(resource_path("icon/search.png"), self.uic.search_button, icon_size=(30, 35))
        self.setIcon(resource_path("icon/accept.jpg"), self.uic.accept_button)
        self.setIcon(resource_path("icon/deny.png"), self.uic.deny_button)
        self.setIcon(resource_path("icon/bluetooth.png"), self.uic.connect_button)
        self.setIcon(resource_path("icon/in4.png"), self.uic.information_button,icon_size=(30, 35))
        self.setIcon(resource_path("icon/list.png"), self.uic.list_device_saved,icon_size=(30, 35))

        self.uic.device_list.setDisabled(1)
        self.uic.accept_button.setDisabled(1)
        self.uic.accept_button.clicked.connect(self.accept_information)
        self.uic.deny_button.clicked.connect(self.deny_information)
        self.uic.deny_button.setDisabled(1)

        disk_usage = psutil.disk_usage('/')
        available_disk_percentage = disk_usage.free * 100 / disk_usage.total
        # available_disk_percentage=4
        available_disk_gb = disk_usage.free / (1024 ** 3)  # Convert bytes to gigabytes
        if available_disk_percentage < 5:
            messenger_memory = QMessageBox()
            messenger_memory.setIcon(QMessageBox.Icon.Warning)
            messenger_memory.setWindowTitle("Cảnh báo")
            messenger_memory.setStyleSheet("QPushButton { min-width: 100px; min-height: 40px; }" 
                                "QLabel { color: red; font-size: 16pt;}")
            messenger_memory.setText("Bộ nhớ lưu trữ khả dụng quá thấp (dưới 5%). \n\nChương trình sẽ tự động ngắt bởi bộ nhớ lưu trữ còn lại quá thấp!!!\nVui lòng giải phóng bộ nhớ.")
            messenger_memory.exec()
            self.searchUiDef.showMaximized()
            
            self.close()
        elif available_disk_percentage < 10:
            messenger_memory = QMessageBox()
            messenger_memory.setIcon(QMessageBox.Icon.Warning)
            messenger_memory.setWindowTitle("Cảnh báo")
            messenger_memory.setStyleSheet("QPushButton { min-width: 100px; min-height: 40px; }" 
                                "QLabel { color: red; font-size: 16pt; font-size: 15pt;}")
            messenger_memory.setText(
                f"Bộ nhớ lưu trữ khả dụng: {available_disk_percentage:.2f}%\n"
                f"Bộ nhớ lưu trữ còn lại: {available_disk_gb:.2f} GB\n"
            )
            messenger_memory.setInformativeText("Bộ nhớ lưu trữ đang ở mức nguy hiểm (dưới 10%).\n\nLưu ý: Chương trình sẽ không hoạt động nếu bộ nhớ lưu trữ còn lại dưới 5%!!!\n\nLưu ý: Để giải phóng bộ nhớ cần xóa bản tin tại giao diện Tìm kiếm và xóa hình ảnh ở thư mục có đường dẫn sau: ")
            messenger_memory.setStandardButtons(QMessageBox.StandardButton.Ok)
            messenger_memory.exec()
        else:
            pass


    def show_device_dialog(self,status):
        dialog = DeviceDialog(self)  # Truyền tham chiếu của MainWindow vào DeviceDialog
        dialog.exec()
        # Gắn kết sự kiện device_list_select của MainWindow với phương thức connect_device của DeviceDialog


    def show_info_in_text_edit(self,info):
        html_content = self.format_text_with_colors(info)
        
        self.uic.textEdit.setHtml(html_content)
        self.uic.textEdit.setStyleSheet("font-size: 16pt;")
        self.uic.textEdit.setReadOnly(True)

    def format_text_with_colors(self,text):
        lines = text.split('\n')
        formatted_lines = []
        headers = [
        "Tên người vi phạm", "Loại phương tiện", "Biển kiểm soát", "Tốc độ vi phạm",
        "Giới hạn tốc độ quy định", "Thời điểm ghi nhận", "Vị trí ghi nhận", "QL1A-Hà Nội", "Thiết bị", "Đơn vị vận hành"
        ]
        for line in lines:
            stripped_line = line.strip()
            if ":" in stripped_line:
                key, value = map(str.strip, stripped_line.split(":", 1))
                if key in headers:
                    if key == "Biển kiểm soát" or key == "Tốc độ vi phạm":
                        formatted_lines.append(f'<p><strong>{key}:</strong> <span style="color:red;">{value}</span></p>')
                    elif key == "Thiết bị" or key == "Đơn vị vận hành":
                        formatted_lines.append(f'<p><strong>{key}:</strong> <span style="color:blue;">{value}</span></p>')
                    else:
                        formatted_lines.append(f'<p><strong>{key}:</strong> {value}</p>')
                else:
                    formatted_lines.append(f'<p>{stripped_line}</p>')
            elif any(header in stripped_line for header in headers):
                formatted_lines.append(f'<p style="color:blue;">{stripped_line}</p>')
            else:
                formatted_lines.append(f'<p>{stripped_line}</p>')
        
        return '\n'.join(formatted_lines)

    def show_information(self):
        # Tạo thông báo với hướng dẫn
        instructions = (
            "1. Nhấn nút 'Bật Bluetooth' để bắt đầu quét các thiết bị Bluetooth xung quanh. Sau khi quá trình quét hoàn tất, "
            "các thiết bị Bluetooth nhận diện được sẽ hiển thị trong 'Danh sách thiết bị Bluetooth'. Nếu thiết bị mong muốn "
            "không xuất hiện trong danh sách, người sử dụng có thể kết nối trực tiếp bằng cách nhập địa chỉ MAC của thiết bị và nhấn nút 'Kết nối bằng địa chỉ MAC'.\n\n"
            "2. Trong trường hợp kết nối thất bại, hãy thử kết nối lại. Khi kết nối thành công, chờ thiết bị Máy bắn tốc độ gửi bản tin.\n\n"
            "3. Sau khi nhận được bản tin, người sử dụng có hai lựa chọn:\n"
            "   - Nhấn nút 'Gửi lên Server' (nút màu xanh) nếu chấp nhận bản tin đạt chuẩn và muốn gửi lên Server.\n"
            "   - Nhấn nút 'Chụp lại ảnh mới' (nút màu đỏ) nếu hình ảnh chưa đạt chuẩn và yêu cầu Máy bắn tốc độ chụp lại ảnh mới.\n\n"
            "(*) Ngoài ra, người dùng có thể nhấn nút 'Tìm kiếm' để tìm kiếm và xem lại các bản tin đã được xác nhận."
        )

        dialog = QDialog(self)
        dialog.setWindowTitle("Hướng dẫn sử dụng")
        dialog.resize(600, 500)  # Đặt kích thước của QDialog

        text_edit = QTextEdit()
        text_edit.setText(instructions)
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("font-size: 16px;")  # Điều chỉnh cỡ chữ ở đây

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(dialog.accept)

        # Thiết lập kích thước nút Ok
        ok_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_button.setFixedSize(150, 50)  # Đặt kích thước nút Ok

        layout = QVBoxLayout()
        layout.addWidget(text_edit)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec()

    def setIcon(self, icon_path, ui_element, icon_size=(25, 30)):
                icon = QtGui.QIcon()  # Tạo một đối tượng QIcon
                pixmap = QtGui.QPixmap(icon_path)  # Tạo QPixmap từ đường dẫn hình ảnh
                icon.addPixmap(pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)  # Thêm pixmap vào icon
                ui_element.setIcon(icon)  # Đặt icon cho phần tử giao diện
                ui_element.setIconSize(QtCore.QSize(*icon_size))  # Đặt kích thước icon

    def dialog_config(self, dialog, dialog_text, callback_function):
        dialog.setWindowTitle(dialog_text)
        dialog.resize(300, 50)  # Đặt kích thước cho cửa sổ pop-up
        # Thêm một QLineEdit để nhập giá trị tên vào dialog
        line_edit = QLineEdit(dialog)
        # Thêm một QPushButton vào dialog
        btn_ok = QPushButton('OK', dialog)
        # Bố trí các thành phần trong dialog bằng QVBoxLayout
        layout = QVBoxLayout()
        layout.addWidget(QLabel(dialog_text))
        layout.addWidget(line_edit)
        layout.addWidget(btn_ok)
        # Xử lý sự kiện khi nhấn nút "OK"
        def showValue():
            value = line_edit.text()
            callback_function(value)
            self.uic.connect_with_mac.setDisabled(1)
            dialog.close()
        btn_ok.clicked.connect(showValue)
        dialog.setLayout(layout)


    def connect_with_address(self):
        # Tạo một QDialog để hiển thị pop-up
        dialog = QDialog(self)
        def callback_function(device_address):
            self.thread[2] = ThreadClass(index=1,mac_id=device_address)
            self.thread[2].start()
            self.thread[2].signal.connect(self.my_function)
            self.thread[2].connect_status.connect(self.status_change)
        self.dialog_config(dialog, "Nhập địa chỉ MAC của thiết bị bạn muốn kết nối Bluetooth", callback_function)
        # Hiển thị dialog
        dialog.exec()

    def parse_date(self,date_str):
        # Loại bỏ khoảng trắng hoặc ký tự không mong đợi
        date_str_clean = date_str.strip()  # Xóa khoảng trắng ở đầu/cuối
        # Nếu có ký tự lạ, bạn có thể sử dụng biểu thức chính quy để chỉ lấy các ký tự số và /
        date_str_clean = re.sub(r"[^\d/]", "", date_str_clean)  # Chỉ giữ số và dấu /
        # Định dạng ngày mong đợi
        date_format = "%d/%m/%Y"
        try:
            date_obj = datetime.datetime.strptime(date_str_clean, date_format).date()  # Chuyển đổi sang kiểu date
            return date_obj
        except ValueError as ve:
            print(f"Lỗi chuyển đổi ngày: {ve}")
            return None  # Hoặc giá trị mặc định nếu cần
    
    def process_information(self, status, mess):
        # Lấy văn bản từ textEdit
        header_text = self.uic.textEdit.toPlainText()
        # Trích xuất thông tin ngày từ văn bản
        date_str = header_text.split("Thời điểm ghi nhận: ")[1].split(" ")[0]  # Lấy giá trị ngày
        # Chuyển đổi từ chuỗi sang kiểu datetime.date
        date_format = "%d/%m/%Y"  # Định dạng của chuỗi ngày
        date_obj = self.parse_date(date_str)  # Chuyển đổi sang kiểu date
        # Trích xuất các thông tin khác
        speed_match = re.search(r"Tốc độ vi phạm: (\d+)km/h", header_text)
        speed = speed_match.group(1) if speed_match else "0"
        name_match = re.search(r"Tên người vi phạm: (.+?)(\n|$)", header_text)
        if name_match:
            name = name_match.group(1).strip()  # Lấy kết quả đầu tiên và loại bỏ khoảng trắng thừa
        else:
            name = ""  # Nếu không tìm thấy, xử lý theo cách khác    vehicle = header_text.split("Loại phương tiện: ")[1].split("\n")[0]
        vehicle = header_text.split("Loại phương tiện: ")[1].split("\n")[0]
        plate = header_text.split("Biển kiểm soát: ")[1].split("\n")[0]
        location = header_text.split("Đơn vị vận hành: Phòng Cảnh sát Giao thông Công an tỉnh ")[1].strip()
        print(location)
        device = header_text.split("Thiết bị: ")[1].split(" ")[0]
        # Kết nối với cơ sở dữ liệu MySQL và chèn dữ liệu vào
        db = mysql.connector.connect(
            user='mobeo2002',
            password='doanquangluu',
            host='localhost',
            database='speed_gun'
        )
        cursor = db.cursor()  # Tạo cursor
        insert_query = "INSERT INTO image (name, status, vehicle, plate, speed, date, location, device) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = ( name, status, vehicle, plate, speed, date_obj, location, device)  # Dùng date_obj
        cursor.execute(insert_query, data)
        select_query = """
        SELECT id 
        FROM image
        WHERE 
            name = %s AND 
            status = %s AND 
            vehicle = %s AND 
            plate = %s AND 
            speed = %s AND 
            date = %s AND 
            location = %s AND 
            device = %s
        """
        data = ( name, status, vehicle, plate, speed, date_obj, location, device)
        cursor.execute(select_query, data)
        # Lấy kết quả
        result = cursor.fetchone()
        # Sao chép và đổi tên hình ảnh
        current_folder = "/home/pi/SPEEDCAMPI"
        database_folder = os.path.join(current_folder,"database_folder")
        if not os.path.exists(database_folder):
            os.makedirs(database_folder)
        source_image=resource_path("receive.jpg")
        destination_image=f"{result}.jpg"
        destination_path=os.path.join(database_folder,destination_image)
        shutil.copy(source_image, destination_path)
        # Cập nhật cột `image` với tên tệp mới
        update_query = "UPDATE image SET image = %s WHERE id = %s"
        cursor.execute(update_query, (destination_path, result[0]))  # Chỉ lấy giá trị đầu tiên từ tuple
        db.commit()  # Xác nhận thay đổi
        notice=QMessageBox()
        notice.setWindowTitle("Thông báo")
        notice.setText(mess)
        notice.setIcon(QMessageBox.Icon.Information)
        notice.setStyleSheet(
            "QLabel { margin-left: 5px; font-size: 20px; } QPushButton{ width:100px; font-size: 15px; }" 
        )
        notice.exec()
        ui.viewer.setPhoto(QtGui.QPixmap(resource_path('no_photo.png')))
        # Xóa nội dung trong textEdit sau khi chèn
        ui.uic.textEdit.clear()
        ui.uic.deny_button.setDisabled(1)
        ui.uic.accept_button.setDisabled(1)
        self.uic.accept_button.setStyleSheet(
    "* {color: black; font-size: 15pt;"
    "background-color: #95f5b7;}"
)
        self.uic.deny_button.setStyleSheet(
                "* {color: black; font-size: 15pt;"
        "background-color: #d99886;}"
    )  

    def deny_information(self):
        messenger="Đã yêu cầu Máy bắn tốc độ chụp lại ảnh mới"
        self.process_information(0,messenger)
    def accept_information(self):
        messenger="Đã gửi bản tin lên Server"
        self.process_information(1,messenger)
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPosition()
        event.accept()

    def exit(self):
        # Thực hiện các hành động bạn muốn khi thoát ứng dụng
        QtWidgets.QApplication.quit()

    def minimize_window(self):
        # Minimize cửa sổ
        self.showMinimized()

    def maximize_window(self):
        # Maximize hoặc phục hồi cửa sổ
        if self.isMaximized():
            self.setIcon(resource_path("icon/max2.png"), self.uic.maxbutton, icon_size=(30, 35))
            self.resize(800, 600)
        else:
            self.setIcon(resource_path("icon/min.png"), self.uic.maxbutton, icon_size=(30, 35))
            self.showMaximized()

    def device_list_select(self):   
        option = self.uic.device_list.currentText()
        device_address = option[:17]
        self.thread[2] = ThreadClass(index=1,mac_id=device_address)
        self.thread[2].start()
        self.thread[2].signal.connect(self.my_function)
        self.thread[2].connect_status.connect(self.status_change)

    def my_function(self, msg):
        print('msg')
        # i = self.uic.MainWindow.sender().index
        # Bổ sung các ký tự padding '=' nếu cần thiết
        padded_msg = msg + '=' * ((4 - len(msg) % 4) % 4)
        # Giải mã chuỗi base64 đã được bổ sung padding
        image_data = base64.b64decode(padded_msg)
        # Lưu dữ liệu ảnh vào file
        file_name = resource_path("receive.jpg")
        with open(file_name, "wb") as f:
            f.write(image_data)
        self.viewer.setPhoto(QtGui.QPixmap(resource_path('receive.jpg')))
        # Đọc thông tin EXIF
        image_path = resource_path("receive.jpg")  # Thay bằng đường dẫn hình ảnh của bạn
        exif_info = self.get_exif_info(image_path)
        formatted_header = self.format_exif(exif_info)
        font=QFont()
        font.setPointSize(17)
        ui.uic.textEdit.setFont(font)
        ui.uic.textEdit.setText(formatted_header)
        self.show_info_in_text_edit(formatted_header)
        self.uic.accept_button.setDisabled(0)
        self.uic.deny_button.setDisabled(0)
        self.uic.accept_button.setStyleSheet(
    "* {color: black; font-size: 15pt;"
    "background-color: #03fc5a;}"
)
        self.uic.deny_button.setStyleSheet(
                "* {color: black; font-size: 15pt;"
        "background-color: #d6441c;}"
    )   

    def cancel_connection(self):
        self.thread[2].connect_status.emit(-1)
        self.thread[2].stop()
        self.uic.connect_button.setMaximumWidth(9999999)
        self.uic.cancel_button.setMaximumWidth(0)

    def get_exif_info(self,image_path):
        with open(image_path, "rb") as image_file:
            exif_data = exifread.process_file(image_file, details=False)
        readable_exif = {}  # Từ điển để chứa dữ liệu EXIF
        # Lặp qua các thẻ EXIF và thêm vào từ điển readable_exif
        for tag in exif_data.keys():
            readable_exif[tag] = str(exif_data[tag])  # Chuyển đổi thành chuỗi
        return readable_exif

    def format_exif(self,exif_info):
        # Kiểm tra xem ImageDescription có trong EXIF hay không
        description = exif_info.get("Image ImageDescription", "")
        # Thay thế các ký tự điều khiển nếu cần
        description = description.replace("\r", "").replace("\t", "    ")  # Thay thế tab bằng 4 khoảng trắng
        # Trả về mô tả đã được định dạng
        return description

    def status_change(self,status):
        self.uic.connect_button.setDisabled(0)
        self.uic.device_list.setDisabled(0)
        # Trang thai dang ket noi
        if status>3:
            self.uic.connect_button.setDisabled(1)
            self.uic.device_list.setDisabled(1)
            self.uic.connect_button.setMaximumWidth(9999999)
            self.uic.cancel_button.setMaximumWidth(0)
            self.uic.connect_button.setStyleSheet("background-color: #f7f57c; color: black; font-size: 13pt;")
            self.uic.connect_button.setText("Đang kết nối tới thiết bị")
        # Trang thai ket noi thanh cong
        if status==1:
            self.uic.connect_button.setMaximumWidth(0)
            self.uic.device_list.setMaximumWidth(0)
            self.uic.cancel_button.setMaximumWidth(9999999)
            self.uic.connect_with_mac.setDisabled(1)
            self.uic.list_device_saved.setDisabled(1)
        # 
        if status==0:
            self.uic.connect_button.setMaximumWidth(9999999)
            self.uic.cancel_button.setMaximumWidth(0)
            self.uic.connect_with_mac.setDisabled(0)
            self.uic.list_device_saved.setDisabled(0)
            self.uic.device_list.setMaximumWidth(0)
        # Trang thai ket noi that bai
        if status==3:
            self.uic.connect_button.setStyleSheet("background-color: #f7917c; color: white; font-size: 13pt;")
            self.uic.connect_button.setText("Kết nối thất bại! Nhấn quét lại!")
            self.uic.connect_with_mac.setDisabled(0)
            self.uic.list_device_saved.setDisabled(0)
            self.uic.device_list.setMaximumWidth(0)
        # Trang thai co ban
        if status==-1:
            self.uic.connect_button.setDisabled(0)
            self.uic.device_list.setDisabled(0)
            self.uic.connect_button.setMaximumWidth(9999999)
            self.uic.cancel_button.setMaximumWidth(0)
            self.uic.connect_button.setStyleSheet("background-color: white; color: black; font-size: 13pt;")
            self.uic.connect_button.setText("Bật Bluetooth")
        pass

    def reportProgress(self, n):
        self.uic.device_list.addItem(n)

    def update_device_list_placeholder(self):  
        self.uic.connect_with_mac.setDisabled(0)
        self.uic.list_device_saved.setDisabled(0)     
        if self.uic.device_list.count() == 0:
            self.uic.device_list.setPlaceholderText("Không có thiết bị Bluetooth")
        else:
            self.uic.device_list.setPlaceholderText("Danh sách thiết bị Bluetooth")

    def connect(self):
        # Thiết lập màu của nút thành màu xanh
        self.uic.connect_with_mac.setDisabled(1)
        self.uic.list_device_saved.setDisabled(1)
        self.uic.connect_button.setStyleSheet("background-color: #f7f57c; color: black; font-size: 13pt;")
        self.uic.connect_button.setText("Đang quét thiết bị xung quanh...")
        self.uic.device_list.setMaximumWidth(0)
        self.uic.connect_button.setDisabled(1)
        QCoreApplication.processEvents()  # Cập nhật giao diện người dùng
        self.uic.device_list.clear() 
        

        # Step 2: Create a QThread object
        self.thread[1] = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread[1])
        # Step 5: Connect signals and slots
        self.thread[1].started.connect(self.worker.run)
        self.worker.finished.connect(self.thread[1].quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread[1].finished.connect(self.thread[1].deleteLater)
        self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread[1].start()

        # Final resets
        self.uic.connect_button.setEnabled(False)
        self.thread[1].finished.connect(
            lambda: self.uic.connect_button.setEnabled(True)
        )
        self.thread[1].finished.connect(
            lambda: self.uic.connect_button.setStyleSheet("background-color: #6495ED; color: white; font-size: 13pt;")
        )
        self.thread[1].finished.connect(
            lambda: self.uic.connect_button.setText("Đã bật Bluetooth! Nhấn để quét Bluetooth lại!")
        )
        self.thread[1].finished.connect(
            lambda:  self.uic.device_list.setDisabled(0)
        )
        self.thread[1].finished.connect(
            lambda:  self.uic.device_list.setMaximumWidth(999999)
        )
        self.thread[1].finished.connect(
            lambda: self.uic.connect_button.setDisabled(0)
        )
        self.thread[1].finished.connect(self.update_device_list_placeholder)
        # Sau khi tìm thấy các thiết bị, cập nhật lại màu của nút thành màu xanh lá cây
        
    def search_information(self):
        searchUiDef.showMaximized()



class ThreadClass(QtCore.QThread):
    signal = pyqtSignal(str)
    connect_status = pyqtSignal(int)

    def __init__(self, index=0, mac_id = ""):
        super().__init__()
        self.index = index
        self.mac_id = mac_id

    def run(self):
        # print('Starting thread...', self.index,self.mac_id)
        self.connect_status.emit(4)
        counter = 0
        try:
            self.connect_status.emit(5)
            client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            client.connect((self.mac_id, 4))
            self.connect_status.emit(1)
            while True:
                # message = input("Enter message: ")
                # client.send(message.encode('utf-8'))
                data = self.recv_msg(client)
                if not data:
                    break
                self.signal.emit(f"{data.decode('utf-8')}")
        except OSError:
            self.connect_status.emit(3)
            pass
        self.connect_status.emit(0)
        client.close()

    def stop(self):
        print('Stopping thread...', self.index)
        self.connect_status.emit(0)
        self.terminate()

    def recv_msg(self,sock):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(sock, msglen)

    def recvall(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

class SearchUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = search.Ui_MainWindow()
        self.uic.setupUi(self)
        self.uic.quitbuttonsearch.clicked.connect(self.exit)
        self.uic.minbuttonsearch.clicked.connect(self.minimize_window)
        self.uic.maxbuttonsearch.clicked.connect(self.maximize_window)
        self.setWindowTitle("Cơ sở dữ liệu hệ thống")
        self.setWindowIcon(QtGui.QIcon(resource_path("icon/csgt.png")))
        self.uic.byname.clicked.connect(self.searchbyname)
        self.uic.bydate.clicked.connect(self.searchbydate)
        self.uic.bydevice.clicked.connect(self.searchbydevice)
        self.uic.bylocation.clicked.connect(self.searchbylocation)
        self.uic.byplate.clicked.connect(self.searchbyplate)
        self.uic.byspeed.clicked.connect(self.searchbyspeed)
        self.uic.byvehicle.clicked.connect(self.searchbyvehicle)
        self.uic.byid.clicked.connect(self.searchbyid)
        self.uic.showall.clicked.connect(self.showalldatabase)
        self.uic.bystatus.clicked.connect(self.searchbystatus)
        self.uic.instruction_button_search.clicked.connect(self.show_information)
        self.uic.delete_extend.clicked.connect(self.show_delete_dialog)
        self.uic.check_memory.clicked.connect(self.show_memory)
        self.uic.byname.setStyleSheet("font-size: 15pt;")
        self.uic.bydate.setStyleSheet("font-size: 15pt;")
        self.uic.bydevice.setStyleSheet("font-size: 15pt;")
        self.uic.bylocation.setStyleSheet("font-size: 15pt;")
        self.uic.byplate.setStyleSheet("font-size: 15pt;")
        self.uic.byspeed.setStyleSheet("font-size: 15pt;")
        self.uic.byvehicle.setStyleSheet("font-size: 15pt;")
        self.uic.byid.setStyleSheet("font-size: 15pt;")
        self.uic.bystatus.setStyleSheet("font-size: 15pt;")
        self.uic.showall.setStyleSheet("font-size: 15pt;")
        self.uic.instruction_button_search.setStyleSheet("font-size: 15pt;")
        self.uic.bgroundsearch.setStyleSheet("font-size: 15pt;")
        self.uic.check_memory.setStyleSheet("font-size: 15pt;")
        self.uic.delete_extend.setStyleSheet("background-color: #f7a6a6; color: black; font-size: 20pt;")
        self.uic.bgroundsearchby.setStyleSheet("background-color: #a6f7d8; color: black; font-size: 20pt;")
        self.uic.bgroundsearch.setText("Cơ sở dữ liệu Thiết bị truy cập trực tiếp máy bắn - SPR Lab")

        disk_usage = psutil.disk_usage('/')
        available_disk_percentage = disk_usage.free * 100 / disk_usage.total
        # available_disk_percentage=4
        if available_disk_percentage < 5:
            self.uic.check_memory.setStyleSheet("background-color: #eb3434;")
        elif available_disk_percentage < 10:
            self.uic.check_memory.setStyleSheet("background-color: #f7a6a6; font-size: 15pt;")
        else:
            self.uic.check_memory.setStyleSheet("background-color: #a6f7d8; color: black; font-size: 15pt;")


        self.setIcon(resource_path("icon/min2.png"), self.uic.minbuttonsearch, icon_size=(30, 35))
        self.setIcon(resource_path("icon/quit.png"), self.uic.quitbuttonsearch, icon_size=(30, 35))  # Kích thước tùy chỉnh
        self.setIcon(resource_path("icon/min.png"), self.uic.maxbuttonsearch, icon_size=(30, 35))
        self.setIcon(resource_path("icon/database.png"), self.uic.showall, icon_size=(30, 35))
        self.setIcon(resource_path("icon/search.png"), self.uic.bgroundsearchby, icon_size=(50, 70))
        self.setIcon(resource_path("icon/memory.png"), self.uic.check_memory, icon_size=(30, 35))
        self.setIcon(resource_path("icon/delete.png"), self.uic.delete_extend, icon_size=(30, 35))
        self.uic.showall.setText("Hiển thị toàn bộ")
        self.uic.byid.setText("Theo Mã sự vụ")
        self.uic.check_memory.setText("Kiểm tra bộ nhớ Thiết bị")
        self.uic.check_memory.setFixedSize(300,40)
        self.setIcon(resource_path("icon/in4.png"), self.uic.instruction_button_search,icon_size=(30, 35))
        self.uic.databasetable.setColumnCount(self.uic.databasetable.columnCount() + 1)  # Tăng số cột
        self.showalldatabase()


    
    def delete_checked_rows(self, index):
        if index == self.uic.databasetable.columnCount() - 1:  # Kiểm tra nếu là cột "Xóa dữ liệu"
            msg_box = QMessageBox()
            # Thiết lập tiêu đề và nội dung
            msg_box.setWindowTitle('Xác nhận xóa dữ liệu')
            msg_box.setText('Bạn có chắc chắn muốn xóa dữ liệu đã chọn?')
            # Thiết lập các nút và giá trị mặc định
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg_box.button(QMessageBox.StandardButton.Yes).setText('Có')
            msg_box.button(QMessageBox.StandardButton.No).setText('Không')
            msg_box.button(QMessageBox.StandardButton.No).setFixedSize(100, 50)
            msg_box.button(QMessageBox.StandardButton.Yes).setFixedSize(100, 50)
            # Thiết lập kích thước của hộp thoại
            msg_box.setStyleSheet("QLabel{min-width: 400px; font-size: 16px; min-height: 60px}")  # Thiết lập kích thước tối thiểu của label
            # Hiển thị hộp thoại và chờ cho đến khi người dùng chọn một nút
            reply = msg_box.exec()
            # Xử lý phản hồi từ người dùng
            if reply == QMessageBox.StandardButton.Yes:
                db = mysql.connector.connect(
                    user='mobeo2002',
                    password='doanquangluu',
                    host='localhost',
                    database='speed_gun'
                )
                cursor = db.cursor()
                rows_to_delete = []
                for row in range(self.uic.databasetable.rowCount()):
                    # Lấy checkbox từ ô trong cột "Xóa dữ liệu"
                    checkbox = self.uic.databasetable.cellWidget(row, self.uic.databasetable.columnCount() - 1)
                    print(checkbox)
                    if checkbox and checkbox.isChecked():  # Đảm bảo checkbox không phải là `None`
                        id_to_delete = self.uic.databasetable.item(row, 0).text()  # Ví dụ: Lấy ID từ ô đầu tiên
                        rows_to_delete.append(id_to_delete)

                # Duyệt qua các ID cần xóa
                for id_to_delete in rows_to_delete:
                    # Truy vấn để lấy đường dẫn hình ảnh
                    cursor.execute("SELECT image FROM image WHERE id = %s", (id_to_delete,))
                    image_path = cursor.fetchone()

                    if image_path is not None:
                        # Lấy giá trị từ tuple
                        image_path_string = image_path[0]

                        # In ra để kiểm tra
                        print(f"Image Path: {image_path_string}")
                        print(type(image_path_string))

                        # Kiểm tra sự tồn tại của đường dẫn
                        if os.path.exists(image_path_string):
                            print("File exists.")
                            print(image_path_string)
                            print(type(image_path_string))

                            # Xóa tệp
                            os.remove(image_path_string)
                            print("File has been removed.")
                        else:
                            print("File does not exist.")
                            print(image_path_string)
                            print(type(image_path_string))
                    else:
                        print("No image path found for the given ID.")

                    # Xóa bản ghi khỏi cơ sở dữ liệu
                    cursor.execute("DELETE FROM image WHERE id = %s", (id_to_delete,))

                db.commit()  # Lưu các thay đổi
                cursor.close()  # Đóng cursor
                db.close()  # Đóng kết nối
                # Cập nhật lại bảng sau khi xóa
                self.showalldatabase()  # Gọi hàm để cập nhật lại bảng
            if reply == QMessageBox.StandardButton.No:
                pass

    def show_memory(self):
        disk_usage = psutil.disk_usage('/')
        available_disk_percentage = disk_usage.free * 100 / disk_usage.total
        available_disk_gb = disk_usage.free / (1024 ** 3)  # Convert bytes to gigabytes
        messenger_memory = QMessageBox()
        messenger_memory.setIcon(QMessageBox.Icon.Information)
        messenger_memory.setWindowTitle("Thông tin bộ nhớ Thiết bị")
        font = QFont()
        image_count = available_disk_gb * 1000000 / 340
        if  available_disk_percentage < 10:
            # Hiển thị cảnh báo nhưng vẫn mở giao diện
            messenger_memory = QMessageBox()
            messenger_memory.setIcon(QMessageBox.Icon.Warning)
            messenger_memory.setWindowTitle("Cảnh báo")
            font.setPointSize(16)  # Đặt kích thước chữ là 14 nếu dưới 10%
            text_color = QColor("red")  # Đặt màu chữ là đỏ nếu dưới 10%
            messenger_memory.setStyleSheet("QPushButton { min-width: 100px; min-height: 40px; }" 
                                "QLabel { color: red; }")
            messenger_memory.setText(
                f"Bộ nhớ lưu trữ khả dụng: {available_disk_percentage:.2f}%\n"
                f"Bộ nhớ lưu trữ còn lại: {available_disk_gb:.0f} GB\n"
                f"Bạn có thể lưu thêm {image_count:.0f} bản tin nữa."
            )
            messenger_memory.setInformativeText("Bộ nhớ lưu trữ đang ở mức nguy hiểm (dưới 10%).")
        else:
            # Hiển thị thông tin như thông báo ban đầu
            font.setPointSize(16)  # Đặt kích thước chữ là 14 nếu dưới 10%
            text_color = QColor("green")  # Đặt màu chữ là đỏ nếu dưới 10%
            messenger_memory.setStyleSheet("QPushButton { min-width: 100px; min-height: 40px; }" 
                                "QLabel { color: green; }")
            messenger_memory.setText(
                f"Bộ nhớ lưu trữ khả dụng: {available_disk_percentage:.2f}%\n"
                f"Bộ nhớ lưu trữ còn lại: {available_disk_gb:.0f} GB\n"
                f"Bạn có thể lưu thêm {image_count:,.0f}".replace(",", " ") + " bản tin nữa."
            )
            messenger_memory.setInformativeText(
                "Vui lòng tiếp tục quản lý bộ nhớ để đảm bảo hoạt động ổn định."
            )

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Text, text_color)

        messenger_memory.setFont(font)
        messenger_memory.setPalette(palette)
        messenger_memory.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        messenger_memory.exec()

    def show_information(self):
        # Tạo thông báo với hướng dẫn
        instructions = (
            "1) Nhấn nút 'Hiển thị toàn bộ' để hiển thị lại toàn bộ bản tin đã được xác nhận \n\n"
            "2) Ở cột 'Tìm kiếm theo', người dùng có thể lựa chọn các tiêu chí để tìm kiếm theo thông tin mong muốn.\n\n"
            "3) Trong bảng hiển thị danh sách bản tin đã được xác nhận, ở cột cuối cùng có cột 'Xóa', để xóa bản tin người dùng không muốn lưu trữ trong cơ sở dữ liệu nữa.\n"
            "Để sử dụng, người dùng nhấn ô tick (Có chữ 'V' là đã lựa chọn bản tin), sau khi chọn các bản tin, người dùng nhấn nút 'Xóa' (ở phần tiêu đề cột) để xóa các bản tin đã chọn."
        )

        dialog = QDialog(self)
        dialog.setWindowTitle("Hướng dẫn sử dụng")
        dialog.resize(600, 500)  # Đặt kích thước của QDialog

        text_edit = QTextEdit()
        text_edit.setText(instructions)
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("font-size: 16px;")  # Điều chỉnh cỡ chữ ở đây

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(dialog.accept)

        # Thiết lập kích thước nút Ok
        ok_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_button.setFixedSize(150, 50)  # Đặt kích thước nút Ok

        layout = QVBoxLayout()
        layout.addWidget(text_edit)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec()
    
    def setIcon(self, icon_path, ui_element, icon_size=(25, 30)):
                icon = QtGui.QIcon()  # Tạo một đối tượng QIcon
                pixmap = QtGui.QPixmap(icon_path)  # Tạo QPixmap từ đường dẫn hình ảnh
                icon.addPixmap(pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)  # Thêm pixmap vào icon
                ui_element.setIcon(icon)  # Đặt icon cho phần tử giao diện
                ui_element.setIconSize(QtCore.QSize(*icon_size))  # Đặt kích thước icon

    def getImageLabel(self,image):
        imageLabel = QtWidgets.QLabel()
        imageLabel.setText("")
        imageLabel.setScaledContents(True)
        pixmap = QtGui.QPixmap(image)
        imageLabel.setPixmap(pixmap)
        return imageLabel
    
    def showalldatabase(self):
        self.uic.databasetable.clear()
        db = mysql.connector.connect(
            user='mobeo2002',
            password='doanquangluu',
            host='localhost',
            database='speed_gun'
        )
        cursor = db.cursor()
        cursor.execute("SELECT id, cast(image as char), status, name, vehicle, plate, speed, date, location, device FROM image")  # Select all columns from your table
        rows = cursor.fetchall()
        db.close()
        self.uic.databasetable.setRowCount(len(rows))
        self.uic.databasetable.setStyleSheet("QTableWidget::item { border-bottom: 74px}")
        des_scrollbar_table(self.uic.databasetable)
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                if(j==1):
                    item=self.getImageLabel(value)
                    self.uic.databasetable.setCellWidget(i,j,item)
                elif j == 2:
                    if value == 0:
                        self.uic.databasetable.setItem(i, j, QTableWidgetItem("Chụp ảnh mới"))
                    else:
                        self.uic.databasetable.setItem(i, j, QTableWidgetItem("Gửi lên Server"))
                else:
                    self.uic.databasetable.setItem(i, j, QTableWidgetItem(str(value)))
        self.uic.databasetable.setHorizontalHeaderLabels([
            "Mã sự vụ","Hình ảnh","Trạng thái","Tên", "Loại phương tiện", "Biển số", "Tốc độ", "Ngày", "Địa điểm", "Thiết bị",  "Xóa dữ liệu"
        ])
        # Thêm checkbox vào mỗi ô trong cột "Xóa dữ liệu"
        for row in range(self.uic.databasetable.rowCount()):
            checkbox = QtWidgets.QCheckBox()  # Tạo QCheckBox
            checkbox.setStyleSheet("QCheckBox::indicator { width:30px; height: 30px;} QCheckBox{margin-left: 35px;} ")
            self.uic.databasetable.setCellWidget(row, self.uic.databasetable.columnCount() - 1, checkbox)  # Thêm checkbox vào ô
        # Xử lý sự kiện khi nhấn vào tiêu đề "Xóa dữ liệu"
        header = self.uic.databasetable.horizontalHeader()  # Lấy tiêu đề
        header.sectionClicked.connect(self.delete_checked_rows)  # Kết nối với hàm để xóa dữ liệu  

    def exit(self):
        # Thực hiện các hành động bạn muốn khi thoát ứng dụng
        self.close()

    def minimize_window(self):
        # Minimize cửa sổ
        self.showMinimized()

    def maximize_window(self):
        # Maximize hoặc phục hồi cửa sổ
        if self.isMaximized():
            self.setIcon(resource_path("icon/max2.png"), self.uic.maxbuttonsearch, icon_size=(30, 35))
            self.resize(800, 600)
        else:
            self.setIcon(resource_path("icon/min.png"), self.uic.maxbuttonsearch, icon_size=(30, 35))
            self.showMaximized()

    def dialog_config(self, dialog, dialog_text, callback_function):
        dialog.setWindowTitle(dialog_text)
        dialog.resize(300, 100)  # Đặt kích thước cho cửa sổ pop-up
        dialog.setStyleSheet("font-size: 15pt;")
        # Thêm một QLineEdit để nhập giá trị tên vào dialog
        line_edit = QLineEdit(dialog)
        # Thêm một QPushButton vào dialog
        btn_ok = QPushButton('OK', dialog)
        btn_ok.setFixedSize(300,50)
        # Bố trí các thành phần trong dialog bằng QVBoxLayout
        layout = QVBoxLayout()
        layout.addWidget(QLabel(dialog_text))
        layout.addWidget(line_edit)
        layout.addWidget(btn_ok)
        
        # Xử lý sự kiện khi nhấn nút "OK"
        def showValue():
            value = line_edit.text()
            callback_function(value)
            dialog.close()
        btn_ok.clicked.connect(showValue)
        dialog.setLayout(layout)

    def searchbyname(self):
        # Tạo một QDialog để hiển thị pop-up
        dialog = QDialog(self)
        def callback_function(name_value):
            self.databaseshow_partial_column('name', name_value)
        self.dialog_config(dialog, "Nhập tên người vi phạm:", callback_function)
        # Hiển thị dialog
        dialog.exec()

    def searchbydate(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Chọn khoảng ngày tháng")
        dialog.resize(800, 600)

        # Calendar widget for selecting the start date
        start_calendar = QCalendarWidget(dialog)
        start_calendar.setGridVisible(True)

        # Calendar widget for selecting the end date
        end_calendar = QCalendarWidget(dialog)
        end_calendar.setGridVisible(True)

        btn_ok = QPushButton('OK', dialog)
        btn_ok.setFixedSize(800, 50)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Chọn ngày bắt đầu:"))
        layout.addWidget(start_calendar)
        layout.addWidget(QLabel("Chọn ngày kết thúc:"))
        layout.addWidget(end_calendar)
        layout.addWidget(btn_ok)
        dialog.setLayout(layout)

        def showSelectedDates():
            start_date = start_calendar.selectedDate().toString('yyyy-MM-dd')
            end_date = end_calendar.selectedDate().toString('yyyy-MM-dd')
            self.databaseshow_partial_column('date', (start_date, end_date))
            dialog.close()

        btn_ok.clicked.connect(showSelectedDates)
        dialog.exec()

    def searchbyplate(self):
        # Tạo một QDialog để hiển thị pop-up
        dialog = QDialog(self)
        def callback_function(plate_value):
            self.databaseshow_partial_column('plate', plate_value)
        self.dialog_config(dialog, "Nhập biển số xe:", callback_function)
        # Hiển thị dialog
        dialog.exec()

    def searchbylocation(self):
        # Tạo một QDialog để hiển thị pop-up
        dialog = QDialog(self)
        def callback_function(location_value):
            self.databaseshow_partial_column('location', location_value)
        self.dialog_config(dialog, "Nhập vị trí ghi hình:", callback_function)
        # Hiển thị dialog
        dialog.exec()

    def searchbyspeed(self):
        self.search_by_number_range('speed',"Tìm kiếm theo tốc độ", "Nhập tốc độ",60,100)

    def search_by_number_range(self, column_name, dialog_title, dialog_label,min_value,max_value):
        dialog = QDialog(self)
        dialog.setWindowTitle(dialog_title)

        # SpinBox để nhập giá trị tốc độ tối thiểu
        min_value_spinbox = QSpinBox(dialog)
        min_value_spinbox.setMinimum(0)
        min_value_spinbox.setMaximum(200)
        min_value_spinbox.setValue(min_value)
        min_value_spinbox.setFixedSize(300, 50)

        # SpinBox để nhập giá trị tốc độ tối đa
        max_value_spinbox = QSpinBox(dialog)
        max_value_spinbox.setMinimum(0)
        max_value_spinbox.setMaximum(200)
        max_value_spinbox.setValue(max_value)
        max_value_spinbox.setFixedSize(300, 50)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"{dialog_label} tối thiểu:"))
        layout.addWidget(min_value_spinbox)
        layout.addWidget(QLabel(f"{dialog_label} tối đa:"))
        layout.addWidget(max_value_spinbox)

        btn_ok = QPushButton('OK', dialog)
        layout.addWidget(btn_ok)
        btn_ok.setFixedSize(300, 50)

        def showNumber():
            min_number_value = min_value_spinbox.value()
            max_number_value = max_value_spinbox.value()
            self.databaseshow_partial_column(column_name, (min_number_value, max_number_value))
            dialog.close()

        btn_ok.clicked.connect(showNumber)
        dialog.setLayout(layout)
        dialog.exec()

    def searchbyid(self):
        self.search_by_number_range('id',"Tìm kiếm theo Mã sự vụ", "Nhập Mã sự vụ",0,30)

    def searchbystatus(self):
        # Tạo một QDialog để chọn trạng thái
        dialog = QDialog(self)
        dialog.setWindowTitle("Chọn trạng thái")
        dialog.resize(300, 50)  # Đặt kích cỡ dialog là 300x300
        layout = QVBoxLayout()
        # Tạo nút "Đồng ý"
        btn_agree = QPushButton("Gửi lên Server", dialog)
        btn_agree.setFixedSize(300,50)
        layout.addWidget(btn_agree)
        # Tạo nút "Từ chối"
        btn_decline = QPushButton("Chụp ảnh mới", dialog)
        btn_decline.setFixedSize(300,50)       
        layout.addWidget(btn_decline)
        # Xử lý sự kiện khi nhấn nút "Đồng ý"
        def showAcceptedStatus():
            dialog.close()
            self.databaseshow_partial_column('status', 1)
        btn_agree.clicked.connect(showAcceptedStatus)
        # Xử lý sự kiện khi nhấn nút "Từ chối"
        def showDeclinedStatus():
            dialog.close()
            self.databaseshow_partial_column('status', 0)
        btn_decline.clicked.connect(showDeclinedStatus)
        dialog.setLayout(layout)
        # Hiển thị dialog
        dialog.exec()

    def searchbydevice(self):
        # Sử dụng hàm chung với tên cột và tiêu đề thích hợp
        self.search_by_attribute("device", "Tìm kiếm theo thiết bị")

    def searchbyvehicle(self):
        # Sử dụng hàm chung với tên cột và tiêu đề thích hợp
        self.search_by_attribute("vehicle", "Tìm kiếm theo loại phương tiện")

    def search_by_attribute(self, column_name, dialog_title):
        # Kết nối tới cơ sở dữ liệu và truy vấn các giá trị độc nhất
        db = mysql.connector.connect(
            user='mobeo2002',
            password='doanquangluu',
            host='localhost',
            database='speed_gun'
        )
        cursor = db.cursor()
        query = f"SELECT DISTINCT {column_name} FROM image"
        cursor.execute(query)
        distinct_values = [row[0] for row in cursor.fetchall()]
        db.close()
        # Tạo QDialog để kiểm soát kích thước và giao diện
        custom_dialog = QDialog(self)
        custom_dialog.setWindowTitle(dialog_title)  # Tiêu đề dialog
        custom_dialog.resize(300, 100)  # Kích thước mặc định
        layout = QVBoxLayout(custom_dialog)
        # Tạo QComboBox với các giá trị độc nhất
        combo_box = QComboBox()
        combo_box.addItems(distinct_values)
        combo_box.setFixedSize(300, 50)  # Đặt chiều rộng và chiều cao cố định
        # Áp dụng kiểu CSS để tăng kích thước và cỡ chữ
        combo_box.setStyleSheet("""
            QComboBox {
                font-size: 16pt;  # Tăng cỡ chữ
                padding: 10px;  # Thêm khoảng cách
            }
            QComboBox::down-arrow {
                width: 20px;  # Tăng kích thước mũi tên
                height: 20px;
            }
        """)
        layout.addWidget(combo_box)
        # Tạo nút OK và thêm vào bố cục
        ok_button = QPushButton("OK")
        ok_button.setFixedSize(300,50)
        layout.addWidget(ok_button)
        # Kết nối sự kiện cho nút OK
        ok_button.clicked.connect(lambda: custom_dialog.accept())  # Khi nhấn OK
        # Hiển thị dialog
        custom_dialog.exec()
        selected_value = combo_box.currentText()  # Lấy giá trị đã chọn
        if selected_value:
            # Thực hiện hành động dựa trên lựa chọn
            self.databaseshow_partial_column(column_name, selected_value)

    def databaseshow_partial_column(self, column_name, show_value):            
        db = mysql.connector.connect(
            user='mobeo2002',
            password='doanquangluu',
            host='localhost',
            database='speed_gun'
        )
        cursor = db.cursor()

        # Kiểm tra nếu show_value là một tuple để xác định khoảng giá trị
        if isinstance(show_value, tuple) and len(show_value) == 2:
            min_value, max_value = show_value
            query = f"SELECT id, cast(image as char), status, name, vehicle, plate, speed, date, location, device FROM image WHERE {column_name} BETWEEN %s AND %s"
            cursor.execute(query, (min_value, max_value))
        else:
            # Trường hợp show_value không phải là tuple, mặc định kiểm tra giá trị đơn
            if isinstance(show_value, str):  # Nếu show_value là một chuỗi
                query = f"SELECT id, cast(image as char), status, name, vehicle, plate, speed, date, location, device FROM image WHERE {column_name} LIKE %s"
                cursor.execute(query, ("%" + show_value + "%",))
            else:  # Nếu show_value là một số nguyên
                query = f"SELECT id, cast(image as char), status, name, vehicle, plate, speed, date, location, device FROM image WHERE {column_name} = %s"
                cursor.execute(query, (show_value,))
        
        rows = cursor.fetchall()
        db.close()
        des_scrollbar_table(self.uic.databasetable)
        # Cập nhật table widget với các dòng được trả về từ cơ sở dữ liệu
        self.uic.databasetable.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                if j == 1:  # Nếu đây là cột hình ảnh
                    item = self.getImageLabel(value)
                    self.uic.databasetable.setCellWidget(i, j, item)
                elif j == 2:
                    if value == 0:
                        self.uic.databasetable.setItem(i, j, QTableWidgetItem("Chụp ảnh mới"))
                    else:
                        self.uic.databasetable.setItem(i, j, QTableWidgetItem("Gửi lên Server"))
                else:
                    self.uic.databasetable.setItem(i, j, QTableWidgetItem(str(value)))
        
        self.uic.databasetable.setHorizontalHeaderLabels([
            "Mã sự vụ","Hình ảnh","Trạng thái","Tên", "Loại phương tiện", "Biển số", "Tốc độ", "Ngày", "Địa điểm", "Thiết bị",  "Xóa dữ liệu"
        ])
        
        # Thêm checkbox vào mỗi ô trong cột "Xóa dữ liệu"
        for row in range(self.uic.databasetable.rowCount()):
            checkbox = QtWidgets.QCheckBox()  # Tạo QCheckBox
            checkbox.setStyleSheet("QCheckBox::indicator { width:30px; height: 30px;} QCheckBox{margin-left: 35px;} ")
            self.uic.databasetable.setCellWidget(row, self.uic.databasetable.columnCount() - 1, checkbox)  # Thêm checkbox vào ô
        
        # Xử lý sự kiện khi nhấn vào tiêu đề "Xóa dữ liệu"
        header = self.uic.databasetable.horizontalHeader()  # Lấy tiêu đề
        header.sectionClicked.connect(self.delete_checked_rows)  # Kết nối với hàm để xóa dữ liệu  
        
        return show_value
    
    def show_delete_dialog(self):
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Xóa theo thông tin")
        self.dialog.setFixedSize(600, 500)

        layout = QVBoxLayout(self.dialog)
        
        label = QLabel("Chọn phương thức xóa:", self.dialog)
        layout.addWidget(label)

        button_speed = QPushButton("Xóa bản tin theo khoảng tốc độ", self.dialog)
        button_speed.clicked.connect(self.delete_by_speed_range)
        layout.addWidget(button_speed)

        button_time = QPushButton("Xóa bản tin theo khoảng thời gian", self.dialog)
        button_time.clicked.connect(self.delete_by_time_range)
        layout.addWidget(button_time)

        button_plate = QPushButton("Xóa bản tin theo biển số xe", self.dialog)
        button_plate.clicked.connect(self.delete_by_plate)
        layout.addWidget(button_plate)

        button_id = QPushButton("Xóa bản tin theo khoảng Mã sự vụ", self.dialog)
        button_id.clicked.connect(self.delete_by_id_range)
        layout.addWidget(button_id)

        button_location = QPushButton("Xóa bản tin theo vị trí ghi hình", self.dialog)
        button_location.clicked.connect(self.delete_by_recording_location)
        layout.addWidget(button_location)

        button_device = QPushButton("Xóa bản tin theo thiết bị ghi hình", self.dialog)
        button_device.clicked.connect(self.delete_by_recording_device)
        layout.addWidget(button_device)

        button_vehicle = QPushButton("Xóa bản tin theo phương tiện vi phạm", self.dialog)
        button_vehicle.clicked.connect(self.delete_by_violating_vehicle)
        layout.addWidget(button_vehicle)

        button_status = QPushButton("Xóa bản tin theo trạng thái xác nhận", self.dialog)
        button_status.clicked.connect(self.delete_by_confirmation_status)
        layout.addWidget(button_status)

        button_name = QPushButton("Xóa bản tin theo tên người vi phạm", self.dialog)
        button_name.clicked.connect(self.delete_by_name)
        layout.addWidget(button_name)

        button_speed.setFixedSize(600, 40)
        button_time.setFixedSize(600, 40)
        button_id.setFixedSize(600, 40)
        button_location.setFixedSize(600, 40)
        button_device.setFixedSize(600, 40)
        button_vehicle.setFixedSize(600, 40)
        button_status.setFixedSize(600, 40)
        button_plate.setFixedSize(600, 40)
        button_name.setFixedSize(600, 40)

        cancel_button = QPushButton("Hủy", self.dialog)
        self.setIcon(resource_path("icon/quit.png"), cancel_button,icon_size=(30, 35))
        cancel_button.setFixedSize(200, 50)
        cancel_button.clicked.connect(self.dialog.reject)

        insstruct_button = QPushButton("Hướng dẫn", self.dialog)
        self.setIcon(resource_path("icon/in4.png"), insstruct_button,icon_size=(30, 35))
        insstruct_button.setFixedSize(200, 50)
        insstruct_button.clicked.connect(self.instruct_delete)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(insstruct_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.dialog.setLayout(layout)

        self.dialog.exec()
    def instruct_delete(self):
        # Tạo thông báo với hướng dẫn
        instructions = (
            "Ngoài chức năng xóa bằng cách chọn bản tin như thông thường, để thuận tiện cho việc lựa chọn xóa, người dùng có thể chọn cách xóa theo trường thông tin mong muốn."
        )

        dialog = QDialog(self)
        dialog.setWindowTitle("Hướng dẫn sử dụng")
        dialog.resize(600, 400)  # Đặt kích thước của QDialog

        text_edit = QTextEdit()
        text_edit.setText(instructions)
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("font-size: 16px;")  # Điều chỉnh cỡ chữ ở đây

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(dialog.accept)

        # Thiết lập kích thước nút Ok
        ok_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_button.setFixedSize(100, 50)  # Đặt kích thước nút Ok

        layout = QVBoxLayout()
        layout.addWidget(text_edit)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec()

    def delete_by_speed_range(self):
        delete_value=(60,100)
        self.delete_by_number_range('speed',"Tốc độ", delete_value)

    def delete_by_number_range(self,column_name, dialog_label, delete_value):
        self.dialog.accept()
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Xóa bản tin theo khoảng {dialog_label}")
        min_value, max_value = delete_value
        min_number_spinbox = QSpinBox(dialog)
        min_number_spinbox.setMinimum(0)
        min_number_spinbox.setMaximum(200)
        min_number_spinbox.setValue(min_value)
        min_number_spinbox.setFixedSize(300, 50)

        max_number_spinbox = QSpinBox(dialog)
        max_number_spinbox.setMinimum(0)
        max_number_spinbox.setMaximum(200)
        max_number_spinbox.setValue(max_value)
        max_number_spinbox.setFixedSize(300, 50)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Nhập {dialog_label} tối thiểu:"))
        layout.addWidget(min_number_spinbox)
        layout.addWidget(QLabel(f"Nhập {dialog_label} tối đa:"))
        layout.addWidget(max_number_spinbox)

        btn_ok = QPushButton('Xóa', dialog)
        layout.addWidget(btn_ok)        
        btn_ok.setFixedSize(300, 50)
        cancel_button = QPushButton("Hủy", self.dialog)
        cancel_button.setFixedSize(300, 50)
        cancel_button.clicked.connect(dialog.close)
        layout.addWidget(cancel_button)        
        def deleteNumber():
            min_number_value = min_number_spinbox.value()
            max_number_value = max_number_spinbox.value()
            number_range=(min_number_value,max_number_value)
            # Gọi hàm delete_by_speed_range với min_speed_value và max_speed_value
            self.delete_partial_column(column_name,number_range)
            dialog.close()
        btn_ok.clicked.connect(deleteNumber)
        dialog.setLayout(layout)
        dialog.exec()

    def delete_partial_column(self, column_name, delete_value):
        db = mysql.connector.connect(
            user='mobeo2002',
            password='doanquangluu',
            host='localhost',
            database='speed_gun'
        )
        cursor = db.cursor()
        if isinstance(delete_value, tuple) and len(delete_value) == 2:
            min_value, max_value = delete_value
            query = f"SELECT image FROM image WHERE {column_name} BETWEEN %s AND %s"
            cursor.execute(query, (min_value, max_value))
        else:
            # Nếu delete_value không phải là tuple, xử lý như trước (chỉ trong trường hợp đặc biệt)
            query = f"SELECT image FROM image WHERE {column_name} = %s"
            cursor.execute(query, (delete_value,))
        
        # Lấy tất cả các đường dẫn tệp hình ảnh
        image_paths = cursor.fetchall()
        
        # Xóa các tệp hình ảnh nếu tồn tại
        for image_path in image_paths:
            image_path_string = image_path[0]
            if os.path.exists(image_path_string):
                os.remove(image_path_string)

        # Kiểm tra nếu delete_value là tuple (khoảng giá trị)
        if isinstance(delete_value, tuple) and len(delete_value) == 2:
            min_value, max_value = delete_value
            query = f"DELETE FROM image WHERE {column_name} BETWEEN %s AND %s"
            cursor.execute(query, (min_value, max_value))
        else:
            # Nếu delete_value không phải là tuple, xử lý như trước (chỉ trong trường hợp đặc biệt)
            query = f"DELETE FROM image WHERE {column_name} = %s"
            cursor.execute(query, (delete_value,))
    
        db.commit()
        cursor.close()
        db.close()
        self.dialog.accept()
        self.showalldatabase()
    
    def delete_by_time_range(self):
        self.dialog.accept()
        dialog = QDialog(self)
        dialog.setWindowTitle("Xóa bản tin theo khoảng thời gian")
        dialog.resize(800, 600)

        layout = QVBoxLayout()

        label_start = QLabel("Chọn ngày bắt đầu:")
        calendar_start = QCalendarWidget(dialog)
        label_end = QLabel("Chọn ngày kết thúc:")
        calendar_end = QCalendarWidget(dialog)

        btn_ok = QPushButton('Xóa', dialog)
        btn_ok.setFixedSize(800, 50)

        cancel_button = QPushButton("Hủy", self.dialog)
        cancel_button.setFixedSize(800, 50)
        cancel_button.clicked.connect(dialog.close)
        
        layout.addWidget(label_start)
        layout.addWidget(calendar_start)
        layout.addWidget(label_end)
        layout.addWidget(calendar_end)
        layout.addWidget(btn_ok)
        layout.addWidget(cancel_button)
        dialog.setLayout(layout)

        def deleteSelectedDateRange():
            start_date = calendar_start.selectedDate().toString('yyyy-MM-dd')
            end_date = calendar_end.selectedDate().toString('yyyy-MM-dd')
            self.delete_partial_column('date', (start_date, end_date))
            dialog.close()

        btn_ok.clicked.connect(deleteSelectedDateRange)
        dialog.exec()

    def delete_by_id_range(self):
        delete_value=(0,100)
        self.delete_by_number_range('id',"Mã sự vụ", delete_value)

    def delete_by_recording_location(self):
        self.dialog.accept()
        self.delete_by_input_text("location", "Nhập vị trí ghi hình:")

    def delete_by_plate(self):
        self.dialog.accept()
        self.delete_by_input_text("plate", "Nhập biển số xe vi phạm:")

    def delete_by_name(self):
        self.dialog.accept()
        self.delete_by_input_text("name", "Nhập tên người vi phạm:")

    def delete_by_input_text(self, column_name, dialog_title):
        # Tạo QDialog để nhập thông tin
        dialog = QDialog(self)
        dialog.setWindowTitle(dialog_title)
        dialog.resize(300,200)
        dialog.setStyleSheet("font-size: 14pt;")
        dialog_layout = QVBoxLayout(dialog)
        if(column_name=="name"):
            column_name_label = "Tên người vi phạm"
        if(column_name=="plate"):
            column_name_label = "Biển số xe vi phạm"
        if(column_name=="location"):
            column_name_label = "Vị trí ghi hình"    
        # Thêm các trường nhập thông tin
        input_field = QLineEdit()
        input_field.setPlaceholderText(f"Nhập {column_name_label}")
        dialog_layout.addWidget(input_field)

        # Thêm nút OK
        ok_button = QPushButton("OK", dialog)
        dialog_layout.addWidget(ok_button)
        ok_button.setFixedSize(300, 50)
        cancel_button = QPushButton("Hủy", self.dialog)
        cancel_button.setFixedSize(300, 50)
        cancel_button.clicked.connect(dialog.close)
        
        dialog_layout.addWidget(cancel_button)
        # Xử lý sự kiện khi nhấn nút OK
        def delete_by_input():
            input_text = input_field.text()
            if input_text:
                self.delete_partial_column(column_name, input_text)
            dialog.close()

        ok_button.clicked.connect(delete_by_input)

        # Hiển thị dialog
        dialog.exec()

    def delete_by_recording_device(self):
        self.dialog.accept()
        self.delete_by_attribute("device", "Xóa theo thiết bị")

    def delete_by_violating_vehicle(self):
        self.dialog.accept()
        self.delete_by_attribute("vehicle", "Xóa theo loại phương tiện")

    def delete_by_confirmation_status(self):
        self.dialog.accept()
        dialog = QDialog(self)
        dialog.setWindowTitle("Xóa theo trạng thái xác nhận")
        dialog.resize(300, 100)  # Đặt kích cỡ dialog là 300x300
        layout = QVBoxLayout()
        btn_agree = QPushButton("Gửi lên Server", dialog)#
        btn_agree.setFixedSize(300,50)
        layout.addWidget(btn_agree)
        btn_decline = QPushButton("Chụp lại ảnh mới", dialog)
        btn_decline.setFixedSize(300,50)
        layout.addWidget(btn_decline)
        def deleteAcceptedStatus():
            dialog.close()
            self.delete_partial_column('status', 1)
        btn_agree.clicked.connect(deleteAcceptedStatus)
        def deleteDeclinedStatus():
            dialog.close()
            self.delete_partial_column('status', 0)
        btn_decline.clicked.connect(deleteDeclinedStatus)
        cancel_button = QPushButton("Hủy", self.dialog)
        cancel_button.setFixedSize(300, 50)
        cancel_button.clicked.connect(dialog.close)
        
        layout.addWidget(cancel_button)
        dialog.setLayout(layout)
        # Hiển thị dialog
        dialog.exec()

    def delete_by_attribute(self, column_name, dialog_title):
        # Kết nối tới cơ sở dữ liệu và truy vấn các giá trị độc nhất
        db = mysql.connector.connect(
            user='mobeo2002',
            password='doanquangluu',
            host='localhost',
            database='speed_gun'
        )
        cursor = db.cursor()

        query = f"SELECT DISTINCT {column_name} FROM image"
        cursor.execute(query)
        distinct_values = [row[0] for row in cursor.fetchall()]

        db.close()

        # Tạo QDialog để kiểm soát kích thước và giao diện
        custom_dialog = QDialog(self)
        custom_dialog.setWindowTitle(dialog_title)  # Tiêu đề dialog
        custom_dialog.resize(300, 150)  # Kích thước mặc định

        layout = QVBoxLayout(custom_dialog)

        # Tạo QComboBox với các giá trị độc nhất
        combo_box = QComboBox()
        combo_box.addItems(distinct_values)
        combo_box.setFixedSize(300, 50)  # Đặt chiều rộng và chiều cao cố định

        # Áp dụng kiểu CSS để tăng kích thước và cỡ chữ
        combo_box.setStyleSheet("""
            QComboBox {
                font-size: 16pt;  /* Tăng cỡ chữ */
                padding: 10px;  /* Thêm khoảng cách */
            }
            QComboBox::down-arrow {
                width: 20px;  /* Tăng kích thước mũi tên */
                height: 20px;
            }
        """)

        layout.addWidget(combo_box)

        # Tạo nút OK và thêm vào bố cục
        ok_button = QPushButton("OK")
        ok_button.setFixedSize(300,50)
        layout.addWidget(ok_button)
        ok_button.clicked.connect(custom_dialog.accept)
        
        cancel_button = QPushButton("Hủy", self.dialog)
        cancel_button.setFixedSize(300, 50)
        cancel_button.clicked.connect(custom_dialog.close)
        
        layout.addWidget(cancel_button)

        # Kết nối sự kiện cho nút "X"
        def quit_dialog():
            custom_dialog.close()  # Chỉ đóng dialog mà không đóng toàn bộ chương trình

        # Kết nối sự kiện cho nút "X"
        custom_dialog.rejected.connect(quit_dialog)
        # Hiển thị dialog
        if custom_dialog.exec() == QDialog.DialogCode.Accepted:
            selected_value = combo_box.currentText()  # Lấy giá trị đã chọn
            if selected_value:
                # Thực hiện hành động dựa trên lựa chọn
                self.delete_partial_column(column_name, selected_value)

    
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    import sys
    app =QApplication(sys.argv)
    w = QtWidgets.QMainWindow()
    ui = MainWindow()
    searchUiDef = SearchUI()
    sys.exit(app.exec())
