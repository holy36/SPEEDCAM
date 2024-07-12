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
from PyQt6.QtCore import QObject, QThread, pyqtSignal, Qt,QEvent, QPoint, QPointF 
import new_display,new_search
from PyQt6.QtWidgets import (
    QDateTimeEdit,QSpinBox, QLineEdit, QTimeEdit,QVBoxLayout,QMessageBox, QComboBox, QDialogButtonBox,QLabel, QPushButton, QCalendarWidget)
from PyQt6.QtCore import QDateTime, Qt, QTimer, QLocale
import mysql.connector

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

        self.uic.bydate.clicked.connect(self.searchbydate)
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


    def searchbydate(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Chọn khoảng ngày tháng")
        dialog.resize(800, 500)
        
        layout = QVBoxLayout()
        
        label_start = QLabel("Chọn ngày bắt đầu:")
        calendar_start = QCalendarWidget(dialog)
        label_end = QLabel("Chọn ngày kết thúc:")
        calendar_end = QCalendarWidget(dialog)
        
        btn_ok = QPushButton('OK', dialog)
        
        layout.addWidget(label_start)
        layout.addWidget(calendar_start)
        layout.addWidget(label_end)
        layout.addWidget(calendar_end)
        layout.addWidget(btn_ok)
        dialog.setLayout(layout)

        def showSelectedDateRange():
            start_date = calendar_start.selectedDate().toString('yyyy-MM-dd')
            end_date = calendar_end.selectedDate().toString('yyyy-MM-dd')
            self.databaseshow_partial_column('date', (start_date, end_date))
            dialog.close()
        btn_ok.clicked.connect(showSelectedDateRange)
        dialog.exec()
        

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
