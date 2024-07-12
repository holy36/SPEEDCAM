
import socket
import time
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QCoreApplication
# from bluetooth import Protocols
import bluetooth
import sys
from time import sleep
from PyQt6.QtWidgets import QMenuBar, QMenu, QHeaderView, QHBoxLayout, QVBoxLayout, QTableWidget, QApplication,QCheckBox, QMainWindow, QSizePolicy, QVBoxLayout, QWidget, QPinchGesture, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QMessageBox, QDialog, QInputDialog, QTableWidgetItem, QTextEdit
from PyQt6.QtGui import QPixmap, QAction, QPainter,QFont
from PyQt6.QtCore import QObject, QThread, pyqtSignal, Qt,QEvent, QPoint, QPointF, QTime
import new_display,new_search, setting
from PyQt6.QtWidgets import (
    QDateTimeEdit,QSpinBox, QLineEdit, QTimeEdit,QVBoxLayout,QMessageBox, QComboBox, QDialogButtonBox,QLabel, QPushButton, QCalendarWidget)
from PyQt6.QtCore import QDateTime, Qt, QTimer, QLocale
import mysql.connector


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
        self.load_devices()
        
        button_layout = QHBoxLayout()

        list_connect = QPushButton("Kết nối")
        list_connect.clicked.connect(self.connect_device)
        button_layout.addWidget(list_connect)
        list_connect.setFixedSize(250,100)
        
        add_button = QPushButton("Thêm thiết bị")
        add_button.clicked.connect(self.add_device)
        button_layout.addWidget(add_button)
        add_button.setFixedSize(250,100)

        edit_button = QPushButton("Sửa thông tin")
        edit_button.clicked.connect(self.edit_device)
        button_layout.addWidget(edit_button)
        layout.addLayout(button_layout)
        edit_button.setFixedSize(250,100)

        delete_button = QPushButton("Xóa thiết bị")
        delete_button.clicked.connect(self.delete_device)
        button_layout.addWidget(delete_button)
        delete_button.setFixedSize(250,100)
        
        self.setLayout(layout)
        
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
        dialog.resize(600, 400)  # Đặt kích thước của QDialog

        text_edit = QTextEdit()
        text_edit.setText(instructions)
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("font-size: 16px;")  # Điều chỉnh cỡ chữ ở đây

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(dialog.accept)

        # Thiết lập kích thước nút Ok
        ok_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_button.setFixedSize(60, 30)  # Đặt kích thước nút Ok

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
            self.thread = [None, None, None]  # Khởi tạo self.thread là một danh sách chứa 3 phần tử None
            self.thread[2] = ThreadClass(index=1, mac_id=selected_device[1])
            self.thread[2].start()
            self.thread[2].signal.connect(self.main_window.my_function)
            self.thread[2].connect_status.connect(self.main_window.status_change)
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
            # self.fitInView()
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = new_display.Ui_MainWindow()
        self.uic.setupUi(self)
        self.viewer = PhotoViewer(self)
        self.searchUiDef = SearchUI()
        self.settingUiDef = SettingUI()
        self.uic.image_layout.addWidget(self.viewer)
        self.viewer.setPhoto(QtGui.QPixmap('test.jpg'))
        self.thread = {}
        self.grabGesture(Qt.GestureType.PinchGesture)
        self.uic.connect_button.clicked.connect(self.connect)
        self.uic.cancel_button.clicked.connect(self.cancel_connection)
        self.uic.device_list.setPlaceholderText( "Danh sách thiết bị Bluetooth")
        self.uic.device_list.activated.connect(self.device_list_select)
        self.uic.cancel_button.setStyleSheet("background-color: #66CDAA; color: white;")
        self.uic.quitbutton.clicked.connect(self.exit)
        self.uic.minbutton.clicked.connect(self.minimize_window)
        self.uic.maxbutton.clicked.connect(self.maximize_window)
        self.uic.bground.setStyleSheet("background-color: #949084; color: white;")
        self.uic.bground.setText("Thiết bị truy cập trực tiếp máy bắn tốc độ - SPR Lab")
        self.uic.connect_with_mac.setText("Kết nối tới địa chỉ")
        self.uic.connect_with_mac.clicked.connect(self.connect_with_address)
        self.uic.information_button.clicked.connect(self.show_information)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showMaximized()
        self.viewer.fitInView()
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) 
        self.uic.bground.setDisabled(True)
        self.uic.bground.mouseMoveEvent = self.MoveWindow
        self.uic.bground.mousePressEvent = self.mousePressEvent
        self.clickPosition = QPoint()
        self.setWindowTitle("Hệ thống xử lý vi phạm tốc độ")
        self.setWindowIcon(QtGui.QIcon("icon/csgt.png"))
        self.uic.list_device_saved.setText("Danh sách thiết bị Bluetooth đã lưu")
        self.uic.list_device_saved.clicked.connect(self.show_device_dialog)


        self.setIcon("icon/min2.png", self.uic.minbutton)
        self.setIcon("icon/connect_with_mac.png", self.uic.connect_with_mac, icon_size=(30, 35))  # Kích thước tùy chỉnh
        self.setIcon("icon/quit.png", self.uic.quitbutton, icon_size=(30, 35))  # Kích thước tùy chỉnh
        self.setIcon("icon/min.png", self.uic.maxbutton, icon_size=(30, 35))
        self.setIcon("icon/accept.png", self.uic.accept_button)
        self.setIcon("icon/deny.png", self.uic.deny_button)
        self.setIcon("icon/bluetooth.png", self.uic.connect_button)
        self.setIcon("icon/in4.png", self.uic.information_button,icon_size=(30, 35))
        self.setIcon("icon/list.png", self.uic.list_device_saved,icon_size=(30, 35))




        
    
        self.image = QPixmap("test.jpg")
        self.uic.image_label.setPixmap(self.image)
        self.uic.image_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.uic.image_label.setScaledContents(True)

        self.uic.device_list.setDisabled(1)
        self.uic.accept_button.setDisabled(0)
        self.uic.accept_button.clicked.connect(self.accept_information)

        self.searchUiDef.main_signal.connect(self.main_ui_show)
        self.searchUiDef.setting_signal.connect(self.setting_ui_show)
        self.settingUiDef.main_signal.connect(self.main_ui_show)
        self.settingUiDef.search_signal.connect(self.search_ui_show)

        self.uic.deny_button.setDisabled(1)
        # notice=QMessageBox()
        # notice.setWindowTitle("Thông báo")
        # notice.setText("Bạn đã từ chối bản tin")
        # notice.setIcon(QMessageBox.Icon.Information)
        # notice.setStyleSheet(
        #     "QLabel { margin-left: 5px; font-size: 20px; } QPushButton{ width:100px; font-size: 15px; }" 
        # )
        # notice.exec()
        self.uic.instruction_text.setText("Sau khi nhận được bản tin, người sử dụng có hai lựa chọn:\n- Nhấn nút 'Gửi lên Server' (nút màu xanh) nếu chấp nhận bản tin đạt chuẩn và muốn gửi lên Server.\n- Nhấn nút 'Chụp lại ảnh mới' (nút màu đỏ) nếu hình ảnh chưa đạt chuẩn và yêu cầu Máy bắn tốc độ chụp lại ảnh mới.\n\n")
        self.uic.instruction_text.setStyleSheet("font-size: 14pt;")
        self.uic.instruction_text.setDisabled(1)
        self.uic.bground_2.setStyleSheet("background-color: #596063; color: white; font-size: 16pt;")
        self.show_info_in_text_edit()

        self.uic.time_label.setStyleSheet("""
            font-size: 16px;
            color: #333;
            background-color: #afc9b6;
            border: 2px solid #ccc;
            border-radius: 10px;
            padding: 10px;
        """)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Cập nhật mỗi 1000ms (1 giây)

        # Cập nhật thời gian lần đầu
        self.update_time()
        self.uic.time_label.mousePressEvent = self.handle_label_click

    def handle_label_click(self, event):
        # Tạo và hiển thị cửa sổ lịch
        calendar_dialog = QDialog(self)
        calendar_dialog.setWindowTitle("Lịch")
        
        # Tạo nút đóng cửa sổ lớn
        close_button = QPushButton("X", calendar_dialog)
        close_button.setFixedSize(50, 50)
        close_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                font-weight: bold;
                color: white;
                background-color: #ff0000;  /* Màu đỏ */
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #cc0000;  /* Màu đỏ nhạt hơn khi hover */
            }
            QPushButton:pressed {
                background-color: #990000;  /* Màu đỏ đậm hơn khi nhấn */
            }
        """)
        close_button.clicked.connect(calendar_dialog.close)

        calendar_widget = QCalendarWidget(calendar_dialog)
        calendar_widget.setLocale(QLocale(QLocale.Language.Vietnamese))
        
        # Tăng kích cỡ cho QCalendarWidget
        calendar_widget.setFixedSize(600, 400)

        # Sử dụng stylesheet để tăng kích cỡ các nút điều hướng
        calendar_widget.setStyleSheet("""
            QCalendarWidget QToolButton {
                height: 40px;
                width: 100px;
                color: white;
                font-size: 18px;
                icon-size: 28px, 28px;
                background-color: #0078d7;  /* Màu xanh đậm */
                border: none;
                border-radius: 5px;
                margin: 5px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #005a9e;  /* Màu xanh nhạt hơn khi hover */
            }
            QCalendarWidget QToolButton:pressed {
                background-color: #003f7f;  /* Màu xanh đậm hơn khi nhấn */
            }
            QCalendarWidget QWidget {
                alternate-background-color: #f0f0f0;
            }
            QCalendarWidget QAbstractItemView:enabled {
                font-size: 16px;  /* Kích thước font cho các ngày */
                color: black;  /* Màu chữ cho các ngày */
                background-color: white;
                selection-background-color: #0078d7;  /* Màu nền khi chọn ngày */
                selection-color: white;  /* Màu chữ khi chọn ngày */
            }
        """)

        layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        header_layout.addWidget(close_button)
        
        layout.addLayout(header_layout)
        layout.addWidget(calendar_widget)
        calendar_dialog.setLayout(layout)
        
        calendar_dialog.exec()


    def update_time(self):
        # Lấy thời gian hiện tại
        current_datetime = QDateTime.currentDateTime()

        # Định dạng theo hh:mm:ss AP dd/MM/yyyy
        time_part = current_datetime.toString("hh:mm AP")
        date_part = current_datetime.toString("dd/MM/yyyy")
        current_time = f"{time_part} - {date_part}"
        # Cập nhật QLabel với thời gian đã định dạng
        self.uic.time_label.setText(current_time)

    def search_ui_show(self):
        self.searchUiDef.showMaximized()
        self.settingUiDef.close()
        self.close()

    def main_ui_show(self):
        self.searchUiDef.close()
        self.settingUiDef.close()
        self.showMaximized()
 
    def setting_ui_show(self):
        self.settingUiDef.showMaximized()
        self.close()
        self.searchUiDef.close()

    def show_device_dialog(self):
        dialog = DeviceDialog(self)  # Truyền tham chiếu của MainWindow vào DeviceDialog
        dialog.exec()
        # Gắn kết sự kiện device_list_select của MainWindow với phương thức connect_device của DeviceDialog

    def show_info_in_text_edit(self):
        info = """
        Tên người vi phạm: Phạm Quốc Huy
        Loại phương tiện: Ô tô
        Biển kiểm soát: 18B-22212
        Tốc độ vi phạm: 70km/h
        Giới hạn tốc độ quy định: 50km/h
        Thời điểm ghi nhận: 08/05/2024 R:35
        Vị trí ghi nhận: 
                  Vĩ độ: 11° 29' 24'' Bắc
                  Kinh độ: 109° 27' 36'' Đông
                  Vị trí Km480-900
                  QL1A-Hà Nội
        Thiết bị: 01012 Kiểm định đến 10_2020
        Đơn vị vận hành: Phòng Cảnh sát Giao thông Công an tỉnh Hà Nội
        """
        
        html_content = self.format_text_with_colors(info)
        
        self.uic.textEdit.setHtml(html_content)
        self.uic.textEdit.setStyleSheet("font-size: 16pt;")
        self.uic.textEdit.setReadOnly(True)

    def format_text_with_colors(self,text):
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            if "Biển kiểm soát:" in line:
                formatted_lines.append(f'<p><strong>Biển kiểm soát:</strong> <span style="color:red;">{line.split(":", 1)[1].strip()}</span></p>')
            elif "Tốc độ vi phạm:" in line:
                formatted_lines.append(f'<p><strong>Tốc độ vi phạm:</strong> <span style="color:red;">{line.split(":", 1)[1].strip()}</span></p>')
            elif "Vị trí ghi nhận:" in line:
                formatted_lines.append(f'<p><strong>Vị trí ghi nhận:</strong></p>')
            elif "Vĩ độ:" in line or "Kinh độ:" in line or "Vị trí" in line or "QL1A-Hà Nội" in line:
                formatted_lines.append(f'<p style="color:blue;">{line.strip()}</p>')
            elif "Thiết bị:" in line:
                formatted_lines.append(f'<p><strong>Thiết bị:</strong> <span style="color:blue;">{line.split(":", 1)[1].strip()}</span></p>')
            elif "Đơn vị vận hành:" in line:
                formatted_lines.append(f'<p><strong>Đơn vị vận hành:</strong> <span style="color:blue;">{line.split(":", 1)[1].strip()}</span></p>')
            else:
                formatted_lines.append(f'<p>{line.strip()}</p>')
        
        return '\n'.join(formatted_lines)

    def show_information(self):
        # Tạo thông báo với hướng dẫn
        instructions = (
            "1. Nhấn nút 'Bật Bluetooth' để bắt đầu quét các thiết bị Bluetooth xung quanh. Sau khi quá trình quét hoàn tất, "
            "các thiết bị Bluetooth nhận diện được sẽ hiển thị trong 'Danh sách thiết bị Bluetooth'. Nếu thiết bị mong muốn "
            "không xuất hiện trong danh sách, bạn có thể kết nối trực tiếp bằng cách nhập địa chỉ MAC của thiết bị và nhấn nút 'Kết nối bằng địa chỉ MAC'.\n\n"
            "2. Trong trường hợp kết nối thất bại, hãy thử kết nối lại. Khi kết nối thành công, chờ thiết bị Máy bắn tốc độ gửi bản tin.\n\n"
            "3. Sau khi nhận được bản tin, người sử dụng có hai lựa chọn:\n"
            "   - Nhấn nút 'Gửi lên Server' (nút màu xanh) nếu chấp nhận bản tin đạt chuẩn và muốn gửi lên Server.\n"
            "   - Nhấn nút 'Chụp lại ảnh mới' (nút màu đỏ) nếu hình ảnh chưa đạt chuẩn và yêu cầu Máy bắn tốc độ chụp lại ảnh mới.\n\n"
            "4. Ngoài ra, người dùng có thể nhấn nút 'Tìm kiếm' để tìm kiếm và xem lại các bản tin đã được xác nhận."
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
        ok_button.setFixedSize(60, 30)  # Đặt kích thước nút Ok

        layout = QVBoxLayout()
        layout.addWidget(text_edit)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec()


    def setIcon(self, icon_path, ui_element, icon_size=(25, 30)):
        """
        Đặt icon cho một phần tử giao diện PyQt6.

        :param icon_path: Đường dẫn tới tệp hình ảnh cho icon.
        :param ui_element: Phần tử giao diện (ví dụ, nút hoặc QLabel) cần đặt icon.
        :param icon_size: Kích thước của icon (rộng, cao). Mặc định là (25, 30).
        """
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

        self.dialog_config(dialog, "Nhập địa chỉ thiết bị bạn muốn kết nối", callback_function)
        # Hiển thị dialog
        dialog.exec()
        
    def accept_information(self):
        QMessageBox.information(self, "Tèn ten", "Ố dề")
        try:
            db = mysql.connector.connect(
                user='mobeo2002',
                password='doanquangluu',
                host='localhost',
                database='speed_gun'
            )
            cursor = db.cursor()
            query = "SELECT time_set, check_set FROM check_device WHERE idcheck_device = %s"
            cursor.execute(query, (1,))
            result = cursor.fetchone()
            if result:
                time_set, check_set = result
            else:
                time_set, check_set = None, None
        except mysql.connector.Error as err:
            QMessageBox.critical(self, 'Lỗi', f'Không thể lấy thông tin từ cơ sở dữ liệu: {err}')
            cursor.close()
            db.close()
            return

        cursor.close()
        db.close()

        check_set_text = "Gửi lên Server" if check_set == 1 else "Chụp lại ảnh mới"
        
        if time_set is not None:
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(lambda: QMessageBox.information(self, f'Thông báo', f'Hệ thống đã tự động {check_set_text}'))
            timer.start(time_set-1)  # Start timer with time_set milliseconds


    def MoveWindow(self, event):
        if not self.isMaximized():
            if event.buttons() & Qt.MouseButton.LeftButton:
                new_position = QPoint(int(event.globalPosition().x() - self.clickPosition.x()),
                                      int(event.globalPosition().y() - self.clickPosition.y()))
                self.move(self.pos() + new_position)
                self.clickPosition = event.globalPosition()
                event.accept()


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
            self.setIcon("icon/max2.png", self.uic.maxbutton, icon_size=(30, 35))
            self.resize(800, 600)
        else:
            self.setIcon("icon/min.png", self.uic.maxbutton, icon_size=(30, 35))
            self.showMaximized()

        

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:  # Phóng to khi cuộn lên
            self.zoom(1.1)
        else:  # Thu nhỏ khi cuộn xuống
            self.zoom(0.9)

    def zoom(self, factor):
        self.image = self.image.scaled(self.image.size() * factor)
        pixmap = self.image.scaled(self.image.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.uic.image_label.setPixmap(pixmap)


    def device_list_select(self):   
        option = self.uic.device_list.currentText()
        device_address = option[:17]
        self.thread[2] = ThreadClass(index=1,mac_id=device_address)
        self.thread[2].start()
        self.thread[2].signal.connect(self.my_function)
        self.thread[2].connect_status.connect(self.status_change)
    def my_function(self, msg):
        i = self.uic.MainWindow.sender().index
        self.uic.image_label.setText(msg)

    def cancel_connection(self):
        self.thread[2].stop()
        self.uic.connect_button.setMaximumWidth(9999999)
        self.uic.cancel_button.setMaximumWidth(0)

    def status_change(self,status):
        self.uic.connect_button.setDisabled(0)
        self.uic.device_list.setDisabled(0)
        if status>3:
            self.uic.connect_button.setDisabled(1)
            self.uic.device_list.setDisabled(1)
            self.uic.connect_button.setMaximumWidth(9999999)
            self.uic.cancel_button.setMaximumWidth(0)
            self.uic.connect_button.setStyleSheet("background-color: #f7f57c; color: black;")
            self.uic.connect_button.setText("Đang kết nối tới thiết bị")
        if status==1:
            self.uic.connect_button.setMaximumWidth(0)
            self.uic.cancel_button.setMaximumWidth(9999999)
        if status==0:
            self.uic.connect_button.setMaximumWidth(9999999)
            self.uic.cancel_button.setMaximumWidth(0)
        if status==3:
            self.uic.connect_button.setStyleSheet("background-color: #f7917c; color: white;")
            self.uic.connect_button.setText("Kết nối thất bại! Nhấn kết nối lại!")
        # self.thread[2].connect_status.emit(3)

        pass

    def reportProgress(self, n):
        self.uic.device_list.addItem(n)
    def update_device_list_placeholder(self):       
        if self.uic.device_list.count() == 0:
            self.uic.device_list.setPlaceholderText("Không có thiết bị Bluetooth")
        else:
            self.uic.device_list.setPlaceholderText("Danh sách thiết bị Bluetooth")

    def connect(self):
        # Thiết lập màu của nút thành màu xanh
        self.uic.connect_button.setStyleSheet("background-color: #f7f57c; color: black;")
        self.uic.connect_button.setText("Đang quét thiết bị xung quanh...")
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
            lambda: self.uic.connect_button.setStyleSheet("background-color: #6495ED; color: white;")
        )
        self.thread[1].finished.connect(
            lambda: self.uic.connect_button.setText("Đã bật Bluetooth! Nhấn để quét Bluetooth lại!")
        )
        self.thread[1].finished.connect(
            lambda:  self.uic.device_list.setDisabled(0)
        )
        self.thread[1].finished.connect(
            lambda: self.uic.connect_button.setDisabled(0)
        )
        self.thread[1].finished.connect(self.update_device_list_placeholder)
        # Sau khi tìm thấy các thiết bị, cập nhật lại màu của nút thành màu xanh lá cây

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

            # print(f"Connected!")

            self.connect_status.emit(1)
            while True:
                # message = input("Enter message: ")
                # client.send(message.encode('utf-8'))
                data = client.recv(1024)
                if not data:
                    break
                # print(f"Received: {data.decode('utf-8')}")
                # print(self.connect_status)
                self.signal.emit(f"{data.decode('utf-8')}")
        except OSError:
            self.connect_status.emit(3)
            pass
        # print("Disconnected")
        self.connect_status.emit(0)

        client.close()

    def stop(self):
        print('Stopping thread...', self.index)
        self.connect_status.emit(0)
        self.terminate()

class SearchUI(QMainWindow):
    main_signal = pyqtSignal()
    setting_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.uic = new_search.Ui_MainWindow()
        self.uic.setupUi(self)
        self.uic.quitbuttonsearch.clicked.connect(self.exit)
        self.uic.minbuttonsearch.clicked.connect(self.minimize_window)
        self.uic.maxbuttonsearch.clicked.connect(self.maximize_window)
        self.setWindowTitle("Cơ sở dữ liệu hệ thống")
        self.setWindowIcon(QtGui.QIcon("icon/Phu_hieu_canh_sat_giao_thong.png"))

        self.uic.bydate.clicked.connect(self.searchbydatetime)
        self.uic.byplate.clicked.connect(self.searchbyplate)
        self.uic.byspeed.clicked.connect(self.searchbyspeed)
        self.uic.showall.clicked.connect(self.showalldatabase)
        self.uic.delete_extend.clicked.connect(self.show_delete_dialog)
        self.uic.main_ui.clicked.connect(self.emit_main_ui)
        self.uic.setting_ui.clicked.connect(self.emit_setting_ui)
        self.uic.searchbyother.clicked.connect(self.show_search_extend_dialog)

        self.uic.bydate.setStyleSheet("font-size: 15pt;")
        self.uic.byplate.setStyleSheet("font-size: 15pt;")
        self.uic.byspeed.setStyleSheet("font-size: 15pt;")
        self.uic.main_ui.setStyleSheet("font-size: 15pt;")
        self.uic.setting_ui.setStyleSheet("font-size: 15pt;")
        self.uic.bgroundsearchby.setStyleSheet("font-size: 20pt;")
        self.uic.searchbyother.setStyleSheet("font-size: 20pt;")
        self.uic.delete_extend.setStyleSheet("font-size: 20pt;")
        self.uic.bground_ui.setStyleSheet("font-size: 20pt;")


        

        self.setIcon("icon/min2.png", self.uic.minbuttonsearch, icon_size=(30, 35))
        self.setIcon("icon/quit.png", self.uic.quitbuttonsearch, icon_size=(30, 35))  # Kích thước tùy chỉnh
        self.setIcon("icon/min.png", self.uic.maxbuttonsearch, icon_size=(30, 35))
        self.setIcon("icon/database.png", self.uic.showall, icon_size=(30, 35))
        self.setIcon("icon/search.png", self.uic.bgroundsearchby, icon_size=(30, 35))
        self.setIcon("icon/in4.png", self.uic.instruction_button_search, icon_size=(30, 35))
        self.setIcon("icon/memory.png", self.uic.check_memory, icon_size=(30, 35))
        self.setIcon("icon/delete.png", self.uic.delete_extend, icon_size=(30, 35))
        self.setIcon("icon/search.png", self.uic.searchbyother, icon_size=(30, 35))
        self.setIcon("icon/ui.png", self.uic.bground_ui, icon_size=(30, 35))
        self.setIcon("icon/setting.png", self.uic.setting_ui, icon_size=(30, 35))
        self.setIcon("icon/main_ui.png", self.uic.main_ui, icon_size=(30, 35))




        self.uic.showall.setText("Hiển thị toàn bộ")
        self.uic.showall.setStyleSheet("font-size: 15pt;")
        self.showalldatabase()

        self.uic.time_label_search.setStyleSheet("""
            font-size: 16px;
            color: #333;
            background-color: #afc9b6;
            border: 2px solid #ccc;
            border-radius: 10px;
            padding: 10px;
        """)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Cập nhật mỗi 1000ms (1 giây)

        # Cập nhật thời gian lần đầu
        self.update_time()
        self.uic.time_label_search.mousePressEvent = self.handle_label_click

    def handle_label_click(self, event):
        # Tạo và hiển thị cửa sổ lịch
        calendar_dialog = QDialog(self)
        calendar_dialog.setWindowTitle("Lịch")
        
        # Tạo nút đóng cửa sổ lớn
        close_button = QPushButton("X", calendar_dialog)
        close_button.setFixedSize(50, 50)
        close_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                font-weight: bold;
                color: white;
                background-color: #ff0000;  /* Màu đỏ */
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #cc0000;  /* Màu đỏ nhạt hơn khi hover */
            }
            QPushButton:pressed {
                background-color: #990000;  /* Màu đỏ đậm hơn khi nhấn */
            }
        """)
        close_button.clicked.connect(calendar_dialog.close)

        calendar_widget = QCalendarWidget(calendar_dialog)
        calendar_widget.setLocale(QLocale(QLocale.Language.Vietnamese))
        
        # Tăng kích cỡ cho QCalendarWidget
        calendar_widget.setFixedSize(600, 400)

        # Sử dụng stylesheet để tăng kích cỡ các nút điều hướng
        calendar_widget.setStyleSheet("""
            QCalendarWidget QToolButton {
                height: 40px;
                width: 100px;
                color: white;
                font-size: 18px;
                icon-size: 28px, 28px;
                background-color: #0078d7;  /* Màu xanh đậm */
                border: none;
                border-radius: 5px;
                margin: 5px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #005a9e;  /* Màu xanh nhạt hơn khi hover */
            }
            QCalendarWidget QToolButton:pressed {
                background-color: #003f7f;  /* Màu xanh đậm hơn khi nhấn */
            }
            QCalendarWidget QWidget {
                alternate-background-color: #f0f0f0;
            }
            QCalendarWidget QAbstractItemView:enabled {
                font-size: 16px;  /* Kích thước font cho các ngày */
                color: black;  /* Màu chữ cho các ngày */
                background-color: white;
                selection-background-color: #0078d7;  /* Màu nền khi chọn ngày */
                selection-color: white;  /* Màu chữ khi chọn ngày */
            }
        """)

        layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        header_layout.addWidget(close_button)
        
        layout.addLayout(header_layout)
        layout.addWidget(calendar_widget)
        calendar_dialog.setLayout(layout)
        
        calendar_dialog.exec()


    def update_time(self):
        # Lấy thời gian hiện tại
        current_datetime = QDateTime.currentDateTime()

        # Định dạng theo "Thời gian: hh:mm:ss AP \n dd/MM/yyyy"
        time_part = current_datetime.toString("hh:mm AP")
        date_part = current_datetime.toString("dd/MM/yyyy")
        current_time = f"Thời gian: {time_part}\nNgày: {date_part}"

        # Cập nhật QLabel với thời gian đã định dạng
        self.uic.time_label_search.setText(current_time)


    def emit_main_ui(self):
        self.main_signal.emit()
    
    def emit_setting_ui(self):
        self.setting_signal.emit()

    def setIcon(self, icon_path, ui_element, icon_size=(25, 30)):
            """
            Đặt icon cho một phần tử giao diện PyQt6.

            :param icon_path: Đường dẫn tới tệp hình ảnh cho icon.
            :param ui_element: Phần tử giao diện (ví dụ, nút hoặc QLabel) cần đặt icon.
            :param icon_size: Kích thước của icon (rộng, cao). Mặc định là (25, 30).
            """
            icon = QtGui.QIcon()  # Tạo một đối tượng QIcon
            pixmap = QtGui.QPixmap(icon_path)  # Tạo QPixmap từ đường dẫn hình ảnh
            icon.addPixmap(pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)  # Thêm pixmap vào icon

            ui_element.setIcon(icon)  # Đặt icon cho phần tử giao diện
            ui_element.setIconSize(QtCore.QSize(*icon_size))  # Đặt kích thước icon

    def getImageLabel(self,image):
        imageLabel = QtWidgets.QLabel()
        imageLabel.setText("")
        imageLabel.setScaledContents(True)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(image, 'jpg')
        imageLabel.setPixmap(pixmap)
        return imageLabel
    
    def showalldatabase(self):
        self.uic.databasetable.clearContents()
        db = mysql.connector.connect(
            user='mobeo2002',
            password='doanquangluu',
            host='localhost',
            database='speed_gun'
        )
        cursor = db.cursor()
        self.des_scrollbar_table(self.uic.databasetable)
        cursor.execute("SELECT * FROM image")  # Select all columns from your table
        rows = cursor.fetchall()
        db.close()
        self.uic.databasetable.setRowCount(len(rows))
        self.uic.databasetable.setStyleSheet("QTableWidget::item { border-bottom: 74px}")
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                if(j==1):
                    item=self.getImageLabel(value)
                    self.uic.databasetable.setCellWidget(i,j,item)
                elif j == 2:
                    if value == 0:
                        self.uic.databasetable.setItem(i, j, QTableWidgetItem("Chụp lại ảnh mới"))
                    else:
                        self.uic.databasetable.setItem(i, j, QTableWidgetItem("Gửi lên Server"))
                else:
                    self.uic.databasetable.setItem(i, j, QTableWidgetItem(str(value)))

    def exit(self):
        # Thực hiện các hành động bạn muốn khi thoát ứng dụng
        self.close()

    def minimize_window(self):
        # Minimize cửa sổ
        self.showMinimized()

    def maximize_window(self):
        # Maximize hoặc phục hồi cửa sổ
        if self.isMaximized():
            self.setIcon("icon/max2.png", self.uic.maxbuttonsearch, icon_size=(30, 35))
            self.resize(800, 600)
        else:
            self.setIcon("icon/min.png", self.uic.maxbuttonsearch, icon_size=(30, 35))
            self.showMaximized()

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
            dialog.close()

        btn_ok.clicked.connect(showValue)

        dialog.setLayout(layout)


    def searchbydatetime(self):
        self.showStartDateTimeDialog()

    def showStartDateTimeDialog(self):
        self.start_datetime_dialog = QDialog(self)
        self.start_datetime_dialog.setWindowTitle("Chọn ngày và thời gian bắt đầu")
        self.start_datetime_dialog.resize(700, 700)
        
        layout = QVBoxLayout()
        
        label_date = QLabel("Chọn ngày bắt đầu:", self.start_datetime_dialog)
        label_date.setStyleSheet("font-size: 20pt;")
        self.calendar_start = QCalendarWidget(self.start_datetime_dialog)
        self.calendar_start.setLocale(QLocale(QLocale.Language.Vietnamese))
        
        label_time = QLabel("Chọn thời gian bắt đầu:", self.start_datetime_dialog)
        label_time.setStyleSheet("font-size: 20pt;")

        
        time_layout = QHBoxLayout()
        label_hour = QLabel("                    Giờ:", self.start_datetime_dialog)
        self.hour_spinbox_start = QSpinBox(self.start_datetime_dialog)
        self.hour_spinbox_start.setRange(0, 23)
        self.hour_spinbox_start.setValue(QTime.currentTime().hour())

        label_minute = QLabel("                    Phút:", self.start_datetime_dialog)
        self.minute_spinbox_start = QSpinBox(self.start_datetime_dialog)
        self.minute_spinbox_start.setRange(0, 59)
        self.minute_spinbox_start.setValue(QTime.currentTime().minute())

        label_second = QLabel("                    Giây:", self.start_datetime_dialog)
        self.second_spinbox_start = QSpinBox(self.start_datetime_dialog)
        self.second_spinbox_start.setRange(0, 59)
        self.second_spinbox_start.setValue(QTime.currentTime().second())


        label_hour.setStyleSheet("font-size: 16pt;")
        label_minute.setStyleSheet("font-size: 16pt;")
        label_second.setStyleSheet("font-size: 16pt;")

        self.hour_spinbox_start.setFixedSize(90, 60)
        self.minute_spinbox_start.setFixedSize(90, 60)
        self.second_spinbox_start.setFixedSize(90, 60)
        # Đặt kích thước cho nút mũi tên tăng giảm của hour_spinbox_start
        self.hour_spinbox_start.setStyleSheet("QSpinBox::up-button { width: 40px; height: 30px; }"
                                      "QSpinBox::down-button { width: 40px; height: 30px; }"
                                      "QSpinBox { font-size: 18px; }")  # Đặt kích thước chữ

        self.minute_spinbox_start.setStyleSheet("QSpinBox::up-button { width: 40px; height: 30px; }"
                                                "QSpinBox::down-button { width: 40px; height: 30px; }"
                                                "QSpinBox { font-size: 18px; }")  # Đặt kích thước chữ

        self.second_spinbox_start.setStyleSheet("QSpinBox::up-button { width: 40px; height: 30px; }"
                                                "QSpinBox::down-button { width: 40px; height: 30px; }"
                                                "QSpinBox { font-size: 18px; }")  # Đặt kích thước chữ


        time_layout.addWidget(label_hour)
        time_layout.addWidget(self.hour_spinbox_start)
        time_layout.addWidget(label_minute)
        time_layout.addWidget(self.minute_spinbox_start)
        time_layout.addWidget(label_second)
        time_layout.addWidget(self.second_spinbox_start)

        btn_next = QPushButton('Tiếp tục', self.start_datetime_dialog)
        btn_next.setFixedHeight(50)
        
        layout.addWidget(label_date)
        layout.addWidget(self.calendar_start)
        layout.addWidget(label_time)
        layout.addLayout(time_layout)
        layout.addWidget(btn_next)
        self.start_datetime_dialog.setLayout(layout)

        btn_next.clicked.connect(self.showEndDateTimeDialog)
        self.start_datetime_dialog.exec()

    def showEndDateTimeDialog(self):
        self.start_datetime_dialog.close()
        
        self.end_datetime_dialog = QDialog(self)
        self.end_datetime_dialog.setWindowTitle("Chọn ngày và thời gian kết thúc")
        self.end_datetime_dialog.resize(700, 700)
        
        layout = QVBoxLayout()
        
        label_date = QLabel("Chọn ngày kết thúc:", self.end_datetime_dialog)
        label_date.setStyleSheet("font-size: 20pt;")
        self.calendar_end = QCalendarWidget(self.end_datetime_dialog)
        self.calendar_end.setLocale(QLocale(QLocale.Language.Vietnamese))
        
        label_time = QLabel("Chọn thời gian kết thúc:", self.end_datetime_dialog)
        label_time.setStyleSheet("font-size: 20pt;")
        
        time_layout = QHBoxLayout()
        label_hour = QLabel("Giờ:", self.end_datetime_dialog)
        self.hour_spinbox_end = QSpinBox(self.end_datetime_dialog)
        self.hour_spinbox_end.setRange(0, 23)
        self.hour_spinbox_end.setValue(QTime.currentTime().hour())

        label_minute = QLabel("Phút:", self.end_datetime_dialog)
        self.minute_spinbox_end = QSpinBox(self.end_datetime_dialog)
        self.minute_spinbox_end.setRange(0, 59)
        self.minute_spinbox_end.setValue(QTime.currentTime().minute())

        label_second = QLabel("Giây:", self.end_datetime_dialog)
        self.second_spinbox_end = QSpinBox(self.end_datetime_dialog)
        self.second_spinbox_end.setRange(0, 59)
        self.second_spinbox_end.setValue(QTime.currentTime().second())

        self.hour_spinbox_end.setFixedSize(90, 60)
        self.minute_spinbox_end.setFixedSize(90, 60)
        self.second_spinbox_end.setFixedSize(90, 60)
        
        label_hour.setStyleSheet("font-size: 16pt;")
        label_minute.setStyleSheet("font-size: 16pt;")
        label_second.setStyleSheet("font-size: 16pt;")

                # Tương tự cho các spinbox của dialog kết thúc
        self.hour_spinbox_end.setStyleSheet("QSpinBox::up-button { width: 40px; height: 30px; }"
                                            "QSpinBox::down-button { width: 40px; height: 30px; }"
                                            "QSpinBox { font-size: 16px; }")  # Đặt kích thước chữ

        self.minute_spinbox_end.setStyleSheet("QSpinBox::up-button { width: 40px; height: 30px; }"
                                            "QSpinBox::down-button { width: 40px; height: 30px; }"
                                            "QSpinBox { font-size: 16px; }")  # Đặt kích thước chữ

        self.second_spinbox_end.setStyleSheet("QSpinBox::up-button { width: 40px; height: 30px; }"
                                            "QSpinBox::down-button { width: 40px; height: 30px; }"
                                      "QSpinBox { font-size: 16px; }")  # Đặt kích thước chữ

        time_layout.addWidget(label_hour)
        time_layout.addWidget(self.hour_spinbox_end)
        time_layout.addWidget(label_minute)
        time_layout.addWidget(self.minute_spinbox_end)
        time_layout.addWidget(label_second)
        time_layout.addWidget(self.second_spinbox_end)

        btn_ok = QPushButton('OK', self.end_datetime_dialog)
        btn_ok.setFixedHeight(50)
        
        layout.addWidget(label_date)
        layout.addWidget(self.calendar_end)
        layout.addWidget(label_time)
        layout.addLayout(time_layout)
        layout.addWidget(btn_ok)
        self.end_datetime_dialog.setLayout(layout)

        btn_ok.clicked.connect(self.showSelectedDateTimeRange)
        self.end_datetime_dialog.exec()
    
    def showSelectedDateTimeRange(self):
        start_date = self.calendar_start.selectedDate().toString('yyyy-MM-dd')
        start_time = QTime(self.hour_spinbox_start.value(), 
                           self.minute_spinbox_start.value(), 
                           self.second_spinbox_start.value()).toString('HH:mm:ss')
        start_datetime = f"{start_date} {start_time}"

        end_date = self.calendar_end.selectedDate().toString('yyyy-MM-dd')
        end_time = QTime(self.hour_spinbox_end.value(), 
                         self.minute_spinbox_end.value(), 
                         self.second_spinbox_end.value()).toString('HH:mm:ss')
        end_datetime = f"{end_date} {end_time}"
        
        self.databaseshow_partial_column('date', (start_datetime, end_datetime))
        self.end_datetime_dialog.close()
        

    def searchbyplate(self):
        # Tạo một QDialog để hiển thị pop-up
        dialog = QDialog(self)
        def callback_function(plate_value):
            self.databaseshow_partial_column('plate', plate_value)
        self.dialog_config(dialog, "Tìm kiếm theo tên", callback_function)
        # Hiển thị dialog
        dialog.exec()

    def searchbyspeed(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Tìm kiếm theo khoảng tốc độ")

        # SpinBox để nhập giá trị tốc độ tối thiểu
        min_speed_spinbox = QSpinBox(dialog)
        min_speed_spinbox.setMinimum(0)
        min_speed_spinbox.setMaximum(200)
        min_speed_spinbox.setValue(60)
        min_speed_spinbox.setFixedSize(300, 50)

        # SpinBox để nhập giá trị tốc độ tối đa
        max_speed_spinbox = QSpinBox(dialog)
        max_speed_spinbox.setMinimum(0)
        max_speed_spinbox.setMaximum(200)
        max_speed_spinbox.setValue(100)
        max_speed_spinbox.setFixedSize(300, 50)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nhập tốc độ tối thiểu:"))
        layout.addWidget(min_speed_spinbox)
        layout.addWidget(QLabel("Nhập tốc độ tối đa:"))
        layout.addWidget(max_speed_spinbox)

        btn_ok = QPushButton('OK', dialog)
        layout.addWidget(btn_ok)

        def showSpeed():
            min_speed_value = min_speed_spinbox.value()
            max_speed_value = max_speed_spinbox.value()
            self.databaseshow_partial_column('speed', (min_speed_value, max_speed_value))
            dialog.close()

        btn_ok.clicked.connect(showSpeed)
        dialog.setLayout(layout)
        dialog.exec()

    def searchbyid(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Tìm kiếm theo khoảng ID")
        
        # SpinBox để nhập giá trị ID tối thiểu
        min_id_spinbox = QSpinBox(dialog)
        min_id_spinbox.setMinimum(0)
        min_id_spinbox.setValue(0)
        min_id_spinbox.setFixedSize(300, 50)
        
        # SpinBox để nhập giá trị ID tối đa
        max_id_spinbox = QSpinBox(dialog)
        max_id_spinbox.setMinimum(0)
        max_id_spinbox.setValue(100)
        max_id_spinbox.setFixedSize(300, 50)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nhập ID tối thiểu:"))
        layout.addWidget(min_id_spinbox)
        layout.addWidget(QLabel("Nhập ID tối đa:"))
        layout.addWidget(max_id_spinbox)
        
        btn_ok = QPushButton('OK', dialog)
        layout.addWidget(btn_ok)
        
        def showIdRange():
            min_id_value = min_id_spinbox.value()
            max_id_value = max_id_spinbox.value()
            self.databaseshow_partial_column('id', (min_id_value, max_id_value))
            dialog.close()
        
        btn_ok.clicked.connect(showIdRange)
        dialog.setLayout(layout)
        dialog.exec()

    def searchbystatus(self):
        # Tạo một QDialog để chọn trạng thái
        dialog = QDialog(self)
        dialog.setWindowTitle("Chọn trạng thái")
        dialog.resize(300, 50)  # Đặt kích cỡ dialog là 300x300
        layout = QVBoxLayout()
        # Tạo nút "Đồng ý"
        btn_agree = QPushButton("Đồng ý", dialog)
        layout.addWidget(btn_agree)
        # Tạo nút "Từ chối"
        btn_decline = QPushButton("Từ chối", dialog)
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
        layout.addWidget(ok_button)

        # Kết nối sự kiện cho nút OK
        ok_button.clicked.connect(lambda: custom_dialog.accept())  # Khi nhấn OK

        # Hiển thị dialog
        custom_dialog.exec()

        selected_value = combo_box.currentText()  # Lấy giá trị đã chọn

        if selected_value:
            # Thực hiện hành động dựa trên lựa chọn
            self.databaseshow_partial_column(column_name, selected_value)

    def des_scrollbar_table(self, table):
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


    def databaseshow_partial_column(self, column_name, show_value):
        db = mysql.connector.connect(
            user='mobeo2002',
            password='doanquangluu',
            host='localhost',
            database='speed_gun'
        )
        cursor = db.cursor()

        # Kiểm tra nếu show_value là tuple (khoảng giá trị)
        if isinstance(show_value, tuple) and len(show_value) == 2:
            min_value, max_value = show_value
            query = f"SELECT * FROM image WHERE {column_name} BETWEEN %s AND %s"
            cursor.execute(query, (min_value, max_value))
        else:
            # Nếu show_value không phải là tuple, xử lý như trước (chỉ trong trường hợp đặc biệt)
            if isinstance(show_value, str):
                query = f"SELECT * FROM image WHERE {column_name} LIKE %s"
                cursor.execute(query, ("%" + show_value + "%",))
            else:
                query = f"SELECT * FROM image WHERE {column_name} = %s"
                cursor.execute(query, (show_value,))

        rows = cursor.fetchall()
        db.close()
    # Cập nhật table widget với các dòng được trả về từ cơ sở dữ liệu
        self.des_scrollbar_table(self.uic.databasetable)
        self.uic.databasetable.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                if j == 1:
                    item = self.getImageLabel(value)
                    self.uic.databasetable.setCellWidget(i, j, item)
                elif j == 2:
                    if value == 0:
                        self.uic.databasetable.setItem(i, j, QTableWidgetItem("Từ chối"))
                    else:
                        self.uic.databasetable.setItem(i, j, QTableWidgetItem("Đồng ý"))
                else:
                    self.uic.databasetable.setItem(i, j, QTableWidgetItem(str(value)))

        return show_value


    def show_search_extend_dialog(self):
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Tìm kiếm theo thông tin")
        self.dialog.setFixedSize(600, 400)

        layout = QVBoxLayout(self.dialog)
        
        label = QLabel("Chọn phương thức tìm kiếm:", self.dialog)
        layout.addWidget(label)


        button_id = QPushButton("Tìm kiếm bản tin theo khoảng ID", self.dialog)
        button_id.clicked.connect(self.searchbyid)
        layout.addWidget(button_id)


        button_device = QPushButton("Tìm kiếm bản tin theo thiết bị ghi hình", self.dialog)
        button_device.clicked.connect(self.searchbydevice)
        layout.addWidget(button_device)

        button_vehicle = QPushButton("Tìm kiếm bản tin theo phương tiện vi phạm", self.dialog)
        button_vehicle.clicked.connect(self.searchbyvehicle)
        layout.addWidget(button_vehicle)

        button_status = QPushButton("Tìm kiếm bản tin theo trạng thái xác nhận", self.dialog)
        button_status.clicked.connect(self.searchbystatus)
        layout.addWidget(button_status)

        button_id.setFixedSize(600, 40)
        button_device.setFixedSize(600, 40)
        button_vehicle.setFixedSize(600, 40)
        button_status.setFixedSize(600, 40)

        cancel_button = QPushButton("Hủy", self.dialog)
        cancel_button.setFixedSize(200, 50)
        cancel_button.clicked.connect(self.dialog.reject)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.dialog.setLayout(layout)

        self.dialog.exec()

    def show_delete_dialog(self):
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Xóa theo thông tin")
        self.dialog.setFixedSize(600, 400)

        layout = QVBoxLayout(self.dialog)
        
        label = QLabel("Chọn phương thức xóa:", self.dialog)
        layout.addWidget(label)

        button_speed = QPushButton("Xóa bản tin theo khoảng tốc độ", self.dialog)
        button_speed.clicked.connect(self.delete_by_speed_range)
        layout.addWidget(button_speed)

        button_time = QPushButton("Xóa bản tin theo khoảng thời gian", self.dialog)
        button_time.clicked.connect(self.delete_by_time_range)
        layout.addWidget(button_time)

        button_id = QPushButton("Xóa bản tin theo khoảng ID", self.dialog)
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

        button_speed.setFixedSize(600, 40)
        button_time.setFixedSize(600, 40)
        button_id.setFixedSize(600, 40)
        button_location.setFixedSize(600, 40)
        button_device.setFixedSize(600, 40)
        button_vehicle.setFixedSize(600, 40)
        button_status.setFixedSize(600, 40)

        cancel_button = QPushButton("Hủy", self.dialog)
        cancel_button.setFixedSize(200, 50)
        cancel_button.clicked.connect(self.dialog.reject)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.dialog.setLayout(layout)

        self.dialog.exec()

    def delete_by_speed_range(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Xóa bản tin theo khoảng tốc độ")

        min_speed_spinbox = QSpinBox(dialog)
        min_speed_spinbox.setMinimum(0)
        min_speed_spinbox.setMaximum(200)
        min_speed_spinbox.setValue(60)
        min_speed_spinbox.setFixedSize(300, 50)

        max_speed_spinbox = QSpinBox(dialog)
        max_speed_spinbox.setMinimum(0)
        max_speed_spinbox.setMaximum(200)
        max_speed_spinbox.setValue(100)
        max_speed_spinbox.setFixedSize(300, 50)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nhập tốc độ tối thiểu:"))
        layout.addWidget(min_speed_spinbox)
        layout.addWidget(QLabel("Nhập tốc độ tối đa:"))
        layout.addWidget(max_speed_spinbox)

        btn_ok = QPushButton('Xóa', dialog)
        layout.addWidget(btn_ok)

        def deleteSpeed():
            min_speed_value = min_speed_spinbox.value()
            max_speed_value = max_speed_spinbox.value()
            speed_range=(min_speed_value,max_speed_value)
            # Gọi hàm delete_by_speed_range với min_speed_value và max_speed_value
            self.delete_by_number_range('speed',speed_range)
            dialog.close()
        btn_ok.clicked.connect(deleteSpeed)
        dialog.setLayout(layout)
        dialog.exec()
    
    def delete_by_number_range(self,column_name,number_range):
        db = mysql.connector.connect(
            user='mobeo2002',
            password='doanquangluu',
            host='localhost',
            database='speed_gun'
        )
        cursor = db.cursor()

        min_value, max_value = number_range

        query = f"DELETE FROM image WHERE {column_name} BETWEEN %s AND %s"
        cursor.execute(query, (min_value, max_value))

        db.commit()
        cursor.close()
        db.close()
        self.dialog.accept()
        self.showalldatabase()


    
    def delete_by_time_range(self):
        QMessageBox.information(self, "Info", "Delete by time range clicked")

    def delete_by_id_range(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Xóa bản tin theo khoảng ID")

        min_number_box = QSpinBox(dialog)
        min_number_box.setMinimum(0)
        min_number_box.setMaximum(1000)
        min_number_box.setValue(0)
        min_number_box.setFixedSize(300, 50)

        max_number_box = QSpinBox(dialog)
        max_number_box.setMinimum(0)
        max_number_box.setMaximum(1000)
        max_number_box.setValue(50)
        max_number_box.setFixedSize(300, 50)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nhập ID tối thiểu:"))
        layout.addWidget(min_number_box)
        layout.addWidget(QLabel("Nhập ID tối đa:"))
        layout.addWidget(max_number_box)

        btn_ok = QPushButton('Xóa', dialog)
        layout.addWidget(btn_ok)

        def deleteSpeed():
            min_id_value = min_number_box.value()
            max_id_value = max_number_box.value()
            id_range=(min_id_value,max_id_value)
            # Gọi hàm delete_by_id_range với min_id_value và max_id_value
            self.delete_by_number_range('id',id_range)
            dialog.close()
        btn_ok.clicked.connect(deleteSpeed)
        dialog.setLayout(layout)
        dialog.exec()

    def delete_by_recording_location(self):
        QMessageBox.information(self, "Info", "Delete by recording location clicked")

    def delete_by_recording_device(self):
        QMessageBox.information(self, "Info", "Delete by recording device clicked")

    def delete_by_violating_vehicle(self):
        QMessageBox.information(self, "Info", "Delete by violating vehicle clicked")

    def delete_by_confirmation_status(self):
        QMessageBox.information(self, "Info", "Delete by confirmation status clicked")

class SettingUI(QMainWindow):
    main_signal = pyqtSignal()
    search_signal = pyqtSignal()
    auto_check_status=0
    def __init__(self):
        super().__init__()
        self.uic = setting.Ui_MainWindow()
        self.uic.setupUi(self)
        self.setWindowTitle("Cơ sở dữ liệu hệ thống")
        self.setWindowIcon(QtGui.QIcon("icon/Phu_hieu_canh_sat_giao_thong.png"))
        self.uic.bground.setText("Cài đặt chương trình thiết bị - SPR Lab")
        self.uic.time_label.setStyleSheet("""
            font-size: 16px;
            color: #333;
            background-color: #afc9b6;
            border: 2px solid #ccc;
            border-radius: 10px;
            padding: 10px;
        """)

        self.uic.quitbutton.clicked.connect(self.exit)
        self.uic.minbutton.clicked.connect(self.minimize_window)
        self.uic.maxbutton.clicked.connect(self.maximize_window)
        self.uic.main_ui.clicked.connect(self.emit_main_ui)
        self.uic.search_ui.clicked.connect(self.emit_search_ui)
        self.uic.time_set.clicked.connect(self.show_time_set)
        self.uic.check_set.clicked.connect(self.show_check_set)
        self.uic.auto_connect.clicked.connect(self.auto_connect)
        self.uic.fixed_set.clicked.connect(self.setting_reset)
        self.uic.auto_connecT_setting.clicked.connect(self.auto_connect_on_off)
        self.uic.bground_setting.clicked.connect(self.auto_check_on_off)
        self.uic.time_set.setStyleSheet("font-size: 15pt;")

        self.uic.check_set.setStyleSheet("font-size: 15pt;")
        self.uic.auto_connect.setStyleSheet("font-size: 15pt;")
        self.uic.bground_setting.setStyleSheet("font-size: 20pt;")
        self.uic.bground_ui.setStyleSheet("font-size: 20pt;")
        self.uic.auto_connecT_setting.setStyleSheet("font-size: 20pt;")
        self.uic.fixed_set.setStyleSheet("font-size: 20pt;")
        self.uic.information_button.clicked.connect(self.show_information)

        self.uic.main_ui.setStyleSheet("font-size: 15pt;")
        self.uic.search_ui.setStyleSheet("font-size: 15pt;")


        self.setIcon("icon/in4.png", self.uic.information_button,icon_size=(30, 35))
        self.setIcon("icon/quit.png", self.uic.quitbutton, icon_size=(30, 35))  # Kích thước tùy chỉnh
        self.setIcon("icon/min.png", self.uic.maxbutton, icon_size=(30, 35))
        self.setIcon("icon/min2.png", self.uic.minbutton)
        self.setIcon("icon/main_ui.png", self.uic.main_ui, icon_size=(30, 35))
        self.setIcon("icon/search.png", self.uic.search_ui, icon_size=(30, 35))
        self.setIcon("icon/setting.png", self.uic.bground_setting, icon_size=(30, 35))
        self.setIcon("icon/setting.png", self.uic.fixed_set, icon_size=(30, 35))
        self.setIcon("icon/setting.png", self.uic.auto_connecT_setting, icon_size=(30, 35))
        self.setIcon("icon/ui.png", self.uic.bground_ui, icon_size=(30, 35))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Cập nhật mỗi 1000ms (1 giây)

        # Cập nhật thời gian lần đầu
        self.update_time()
        self.uic.time_label.mousePressEvent = self.handle_label_click
        self.show_set_infor()
    
    def auto_connect_on_off(self):
        current_state = self.uic.auto_connect.isEnabled()
        self.uic.auto_connect.setEnabled(not current_state)

        if self.uic.auto_connect.isEnabled():
            self.uic.auto_connecT_setting.setText('Cài đặt tự động kết nối thiết bị Bluetooth: Bật')
            self.auto_connect()
        else:
            self.uic.auto_connecT_setting.setText('Cài đặt tự động kết nối thiết bị Bluetooth: Tắt')
            self.cancel_auto('latest_device_connect_mac')

    def auto_check_on_off(self):
        current_state = self.uic.time_set.isEnabled()
        self.uic.time_set.setEnabled(not current_state)

        current_state = self.uic.check_set.isEnabled()
        self.uic.check_set.setEnabled(not current_state)

        if self.uic.time_set.isEnabled():
            self.uic.bground_setting.setText('Cài đặt tự động xác nhận bản tin: Bật')
            self.show_check_set()
            self.show_time_set()
            
        else:
            self.uic.bground_setting.setText('Cài đặt tự động xác nhận bản tin: Tắt')
            self.cancel_auto('check_set')
            self.cancel_auto('time_set')
            


    def show_set_infor(self):
        try:
            # Kết nối tới cơ sở dữ liệu
            db = mysql.connector.connect(
                user='mobeo2002',
                password='doanquangluu',
                host='localhost',
                database='speed_gun'
            )
            cursor = db.cursor()
            query = "SELECT time_set, check_set, latest_device_connect_mac FROM check_device WHERE idcheck_device = %s"
            cursor.execute(query, (1,))
            result = cursor.fetchone()
            if result:
                time_set, check_set, latest_device_connect_mac = result
            else:
                time_set, check_set, latest_device_connect_mac = None, None, None
            
            # Kiểm tra latest_device_connect_mac và cập nhật trạng thái của nút pushbutton
        except mysql.connector.Error as err:
            print(f"Lỗi kết nối đến cơ sở dữ liệu: {err}")
        
        finally:
            # Đóng kết nối tới cơ sở dữ liệu
            if db.is_connected():
                cursor.close()
                db.close()
        check_set_text = "Gửi lên Server" if check_set == 1 else "Chụp lại ảnh mới"
        auto_connect_text = latest_device_connect_mac if latest_device_connect_mac else 'Không'
        if time_set and check_set:             
            info_text = (
                "Thông tin cài đặt hiện tại:\n"
                f"- Thời gian tự động xác nhận: {time_set/1000} (s)\n"
                f"- Lựa chọn tự động xác nhận: {check_set_text}\n"
                f"- Tự động kết nối: {auto_connect_text}\n"
            )
        else:
            info_text = (
                "Thông tin cài đặt hiện tại:\n"
                "- Tự động xác nhận bản tin: Không\n"
                f"- Tự động kết nối: {auto_connect_text}\n"
            )
        self.uic.set_infor.setText(info_text)
        self.uic.set_infor.setStyleSheet("font-size: 16pt;")
        if auto_connect_text == "Không":
            self.uic.auto_connect.setEnabled(False)
            self.uic.auto_connecT_setting.setText('Cài đặt tự động kết nối thiết bị Bluetooth: Tắt')
        else:
            self.uic.auto_connect.setEnabled(True)
            self.uic.auto_connecT_setting.setText('Cài đặt tự động kết nối thiết bị Bluetooth: Bật') 

        if time_set and check_set:             
            self.uic.bground_setting.setText('Cài đặt tự động xác nhận bản tin: Bật')
            self.uic.time_set.setEnabled(True)
            self.uic.check_set.setEnabled(True)
        else:
            self.uic.bground_setting.setText('Cài đặt tự động xác nhận bản tin: Tắt')
            self.uic.time_set.setEnabled(False)
            self.uic.check_set.setEnabled(False)
    
    def setting_reset(self):
        try:
            db = mysql.connector.connect(
                user='mobeo2002',
                password='doanquangluu',
                host='localhost',
                database='speed_gun'
            )
            cursor = db.cursor()
            update_query = """
            UPDATE check_device 
            SET time_set = %s, check_set = %s, latest_device_connect_mac = %s 
            WHERE idcheck_device = %s
            """
            values = (3000, 1, '', 1)
            cursor.execute(update_query, values)
            db.commit()
            QMessageBox.information(self, "Cài đặt", "Đã đưa về cài đặt mặc định")
            self.show_set_infor()
        except mysql.connector.Error as err:
            QMessageBox.information(self, "Cài đặt", "Thất bại đưa về cài đặt mặc định")
        finally:
            cursor.close()
            db.close()



    def show_time_set(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Nhập Thời Gian Chờ Tự Động Xác Nhận (giây)')
        dialog.setGeometry(500, 100, 600, 400)

        layout = QVBoxLayout()

        # Label and SpinBox for time_set input
        time_set_label = QLabel("Thời gian chờ tự động xác nhận:", dialog)
        time_set_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(time_set_label)

        time_set_input = QSpinBox(dialog)
        time_set_input.setRange(0, 10000)
        time_set_input.setSingleStep(1)
        time_set_input.setStyleSheet("font-size: 18px; padding: 10px; min-width: 200px;")
        layout.addWidget(time_set_input)

        button_layout = QHBoxLayout()

        def update_time_set():
            time_set = time_set_input.value()
            time_set = time_set *1000
            try:
                db = mysql.connector.connect(
                    user='mobeo2002',
                    password='doanquangluu',
                    host='localhost',
                    database='speed_gun'
                )
                cursor = db.cursor()
                update_query = "UPDATE check_device SET time_set = %s WHERE idcheck_device = %s"
                values = (time_set, 1)
                cursor.execute(update_query, values)
                db.commit()

                self.show_set_infor()
            except mysql.connector.Error as err:
                QMessageBox.critical(dialog, 'Lỗi', f'Không thể cập nhật cơ sở dữ liệu: {err}')
            finally:
                cursor.close()
                db.close()
                dialog.accept()

        def set_default():
            try:
                db = mysql.connector.connect(
                    user='mobeo2002',
                    password='doanquangluu',
                    host='localhost',
                    database='speed_gun'
                )
                cursor = db.cursor()
                update_query = """
                UPDATE check_device 
                SET time_set = %s, check_set = %s, latest_device_connect_mac = %s 
                WHERE idcheck_device = %s
                """
                values = (3000, 1, 'aaaaaaa', 1)
                cursor.execute(update_query, values)
                db.commit()

                QMessageBox.information(dialog, 'Thành công', 'Cập nhật giá trị mặc định thành công.')
            except mysql.connector.Error as err:
                QMessageBox.critical(dialog, 'Lỗi', f'Không thể cập nhật cơ sở dữ liệu: {err}')
            finally:
                cursor.close()
                db.close()
                dialog.accept()

        ok_button = QPushButton('OK', dialog)
        ok_button.setStyleSheet("font-size: 18px; padding: 10px; min-width: 100px;")
        ok_button.clicked.connect(update_time_set)
        button_layout.addWidget(ok_button)

        default_button = QPushButton('Mặc định', dialog)
        default_button.setStyleSheet("font-size: 18px; padding: 10px; min-width: 100px;")
        default_button.clicked.connect(set_default)
        button_layout.addWidget(default_button)

        cancel_button = QPushButton('Hủy', dialog)
        cancel_button.setStyleSheet("font-size: 18px; padding: 10px; min-width: 100px;")
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.exec()

    def show_check_set(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Chọn Hành Động')
        dialog.setGeometry(500, 100, 400, 200)

        layout = QVBoxLayout()

        button_layout = QHBoxLayout()

        def update_check_set(value):
            try:
                db = mysql.connector.connect(
                    user='mobeo2002',
                    password='doanquangluu',
                    host='localhost',
                    database='speed_gun'
                )
                cursor = db.cursor()
                update_query = "UPDATE check_device SET check_set = %s WHERE idcheck_device = %s"
                values = (value, 1)
                cursor.execute(update_query, values)
                db.commit()
                self.show_set_infor()
            except mysql.connector.Error as err:
                QMessageBox.critical(dialog, 'Lỗi', f'Không thể cập nhật cơ sở dữ liệu: {err}')
            finally:
                cursor.close()
                db.close()
                dialog.accept()

        server_button = QPushButton('Gửi lên Server', dialog)
        server_button.setStyleSheet("font-size: 18px; padding: 10px; min-width: 150px;")
        server_button.clicked.connect(lambda: update_check_set(1))
        button_layout.addWidget(server_button)

        capture_button = QPushButton('Chụp lại ảnh mới', dialog)
        capture_button.setStyleSheet("font-size: 18px; padding: 10px; min-width: 150px;")
        capture_button.clicked.connect(lambda: update_check_set(-1))
        button_layout.addWidget(capture_button)

        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.exec()
    
    def auto_connect(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Nhập địa chỉ MAC thiết bị')
        dialog.setGeometry(500, 100, 500, 200)

        layout = QVBoxLayout()

        input_label = QLabel("Nhập địa chỉ MAC thiết bị:", dialog)
        input_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(input_label)

        input_line_edit = QLineEdit(dialog)
        input_line_edit.setPlaceholderText("Nhập địa chỉ MAC thiết bị")
        input_line_edit.setStyleSheet("font-size: 18px; padding: 10px;")
        layout.addWidget(input_line_edit)

        button_layout = QHBoxLayout()

        def save_to_db():
            input_text = input_line_edit.text()
            formatted_text = ':'.join(input_text[i:i+2] for i in range(0, len(input_text), 2))
            try:
                db = mysql.connector.connect(
                    user='mobeo2002',
                    password='doanquangluu',
                    host='localhost',
                    database='speed_gun'
                )
                cursor = db.cursor()
                update_query = "UPDATE check_device SET latest_device_connect_mac = %s WHERE idcheck_device = %s"
                values = (formatted_text, 1)
                cursor.execute(update_query, values)
                db.commit()
                self.show_set_infor()
            except mysql.connector.Error as err:
                QMessageBox.critical(dialog, 'Lỗi', f'Không thể cập nhật cơ sở dữ liệu: {err}')
            finally:
                cursor.close()
                db.close()
                dialog.accept()

        ok_button = QPushButton('OK', dialog)
        ok_button.setStyleSheet("font-size: 18px; padding: 10px; min-width: 100px;")
        ok_button.clicked.connect(save_to_db)
        button_layout.addWidget(ok_button)

        cancel_button = QPushButton('Không tự động', dialog)
        cancel_button.setStyleSheet("font-size: 18px; padding: 10px; min-width: 100px;")
        cancel_button.clicked.connect(lambda: self.cancel_auto('latest_device_connect_mac'))
        button_layout.addWidget(cancel_button)

        quit_button = QPushButton('Thoát', dialog)
        quit_button.setStyleSheet("font-size: 18px; padding: 10px; min-width: 100px;")
        quit_button.clicked.connect(dialog.reject)
        button_layout.addWidget(quit_button)


        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.exec()
        self.show_set_infor()
    def cancel_auto(self, value):
        try:
            # Kết nối tới cơ sở dữ liệu
            db = mysql.connector.connect(
                user='mobeo2002',
                password='doanquangluu',
                host='localhost',
                database='speed_gun'
            )
            # Tạo một cursor để tương tác với database
            cursor = db.cursor()
            # Câu lệnh SQL để xóa dữ liệu của cột value với id = 1
            sql = f"UPDATE check_device SET {value} = NULL WHERE idcheck_device = 1"
            # Thực thi câu lệnh SQL
            cursor.execute(sql)
            # Xác nhận thay đổi trong database
            db.commit()
        except mysql.connector.Error as err:
            pass
        finally:
            # Đóng kết nối tới cơ sở dữ liệu
            if db.is_connected():
                cursor.close()
                db.close()
        self.show_set_infor()

    def emit_main_ui(self):
        self.main_signal.emit()
    def emit_search_ui(self):
        self.search_signal.emit()

    def setIcon(self, icon_path, ui_element, icon_size=(25, 30)):
        """
        Đặt icon cho một phần tử giao diện PyQt6.

        :param icon_path: Đường dẫn tới tệp hình ảnh cho icon.
        :param ui_element: Phần tử giao diện (ví dụ, nút hoặc QLabel) cần đặt icon.
        :param icon_size: Kích thước của icon (rộng, cao). Mặc định là (25, 30).
        """
        icon = QtGui.QIcon()  # Tạo một đối tượng QIcon
        pixmap = QtGui.QPixmap(icon_path)  # Tạo QPixmap từ đường dẫn hình ảnh
        icon.addPixmap(pixmap, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)  # Thêm pixmap vào icon

        ui_element.setIcon(icon)  # Đặt icon cho phần tử giao diện
        ui_element.setIconSize(QtCore.QSize(*icon_size))  # Đặt kích thước icon

    def handle_label_click(self, event):
        # Tạo và hiển thị cửa sổ lịch
        calendar_dialog = QDialog(self)
        calendar_dialog.setWindowTitle("Lịch")
        
        # Tạo nút đóng cửa sổ lớn
        close_button = QPushButton("X", calendar_dialog)
        close_button.setFixedSize(50, 50)
        close_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                font-weight: bold;
                color: white;
                background-color: #ff0000;  /* Màu đỏ */
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #cc0000;  /* Màu đỏ nhạt hơn khi hover */
            }
            QPushButton:pressed {
                background-color: #990000;  /* Màu đỏ đậm hơn khi nhấn */
            }
        """)
        close_button.clicked.connect(calendar_dialog.close)

        calendar_widget = QCalendarWidget(calendar_dialog)
        calendar_widget.setLocale(QLocale(QLocale.Language.Vietnamese))
        
        # Tăng kích cỡ cho QCalendarWidget
        calendar_widget.setFixedSize(600, 400)

        # Sử dụng stylesheet để tăng kích cỡ các nút điều hướng
        calendar_widget.setStyleSheet("""
            QCalendarWidget QToolButton {
                height: 40px;
                width: 100px;
                color: white;
                font-size: 18px;
                icon-size: 28px, 28px;
                background-color: #0078d7;  /* Màu xanh đậm */
                border: none;
                border-radius: 5px;
                margin: 5px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #005a9e;  /* Màu xanh nhạt hơn khi hover */
            }
            QCalendarWidget QToolButton:pressed {
                background-color: #003f7f;  /* Màu xanh đậm hơn khi nhấn */
            }
            QCalendarWidget QWidget {
                alternate-background-color: #f0f0f0;
            }
            QCalendarWidget QAbstractItemView:enabled {
                font-size: 16px;  /* Kích thước font cho các ngày */
                color: black;  /* Màu chữ cho các ngày */
                background-color: white;
                selection-background-color: #0078d7;  /* Màu nền khi chọn ngày */
                selection-color: white;  /* Màu chữ khi chọn ngày */
            }
        """)

        layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        header_layout.addWidget(close_button)
        
        layout.addLayout(header_layout)
        layout.addWidget(calendar_widget)
        calendar_dialog.setLayout(layout)
        
        calendar_dialog.exec()


    def update_time(self):
        # Lấy thời gian hiện tại
        current_datetime = QDateTime.currentDateTime()

        # Định dạng theo hh:mm:ss AP dd/MM/yyyy
        time_part = current_datetime.toString("hh:mm AP")
        date_part = current_datetime.toString("dd/MM/yyyy")
        current_time = f"Thời gian: {time_part}\nNgày: {date_part}"
        # Cập nhật QLabel với thời gian đã định dạng
        self.uic.time_label.setText(current_time)
    def exit(self):
        # Thực hiện các hành động bạn muốn khi thoát ứng dụng
        QtWidgets.QApplication.quit()

    def minimize_window(self):
        # Minimize cửa sổ
        self.showMinimized()

    def maximize_window(self):
        # Maximize hoặc phục hồi cửa sổ
        if self.isMaximized():
            self.setIcon("icon/max2.png", self.uic.maxbutton, icon_size=(30, 35))
            self.resize(800, 600)
        else:
            self.setIcon("icon/min.png", self.uic.maxbutton, icon_size=(30, 35))
            self.showMaximized()
    def show_information(self):
        # Tạo thông báo với hướng dẫn
        instructions = (
    "Tại giao diện cài đặt, người dùng có thể lựa chọn bật chức năng tự động xác nhận bản tin khi không có thao tác bởi người dùng. "
    "Các thay đổi có thể bao gồm thời gian tự động xác nhận (nghĩa là cài đặt sau một khoảng thời gian nhất định kể từ khi nhận bản tin "
    "mà không có thao tác gì, bản tin sẽ tự động được xác nhận), và tùy chọn hành động xác nhận là 'Gửi lên Server' hoặc 'Chụp lại ảnh mới'.\n\n"
    "Ngoài ra, giao diện còn cung cấp chức năng kết nối tự động tới thiết bị, cho phép thiết bị tự động kết nối ngay khi khởi động chương trình "
    "bằng cách lưu trữ thông tin địa chỉ MAC của thiết bị mong muốn kết nối.\n\n"
    "Người dùng cũng có thể nhấn nút Cài đặt mặc định để đưa chương trình về cài đặt gốc, bao gồm:\n"
    "- Thời gian tự động xác nhận bản tin: 30 giây\n"
    "- Hành động xác nhận: Gửi lên Server\n"
    "- Tự động kết nối: Không"
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
        ok_button.setFixedSize(60, 30)  # Đặt kích thước nút Ok

        layout = QVBoxLayout()
        layout.addWidget(text_edit)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec()

if __name__ == "__main__":
    import sys
    app =QApplication(sys.argv)
    # app = QtWidgets.QApplication(sys.argv)
    # widget=QtWidgets.QStackedWidget()
    w = QtWidgets.QMainWindow()
    ui = MainWindow()
    # Login_f = MainWindow()
    searchUiDef = SearchUI()
    settingUiDef = SettingUI()


    # widget.addWidget(Login_f) 
    # widget.addWidget(search) 
    # widget.setCurrentIndex(0)
    # widget.show()
    # searchUiDef.show()
    sys.exit(app.exec())