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
import new_display,new_search, setting
from PyQt6.QtWidgets import (
    QDateTimeEdit,QSpinBox, QLineEdit, QTimeEdit,QVBoxLayout,QMessageBox, QComboBox, QDialogButtonBox,QLabel, QPushButton, QCalendarWidget)
from PyQt6.QtCore import QDateTime, Qt, QTimer, QLocale
import mysql.connector

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
                f"- Thời gian tự động xác nhận: {time_set}\n"
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

                QMessageBox.information(dialog, 'Thành công', 'Cập nhật thành công.')
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

                if value == 1:
                    QMessageBox.information(dialog, 'Thành công', 'Cập nhật tựu động thao tác (Gửi lên Server) thành công.')
                    self.show_set_infor()
                else:
                    QMessageBox.information(dialog, 'Thành công', 'Cập nhật tự động thao tác (Chụp lại ảnh mới) thành công.')
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

                QMessageBox.information(dialog, 'Thành công', f'Cập nhật thành công: {formatted_text}')
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
