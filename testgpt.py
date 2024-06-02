import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QTableWidget, QTableWidgetItem, QInputDialog, QDialog, QHBoxLayout,
    QCheckBox, QHeaderView, QLabel, QLineEdit
)
import mysql.connector

class DeviceDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bluetooth Devices")
        self.setGeometry(100, 100, 700, 400)
        
        self.db = mysql.connector.connect(
            user='mobeo2002',
            password='doanquangluu',
            host='localhost',
            database='speed_gun'
        )
        
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "MAC Address", "Description", "Delete"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        self.load_devices()
        
        button_layout = QHBoxLayout()
        
        add_button = QPushButton("Add Device")
        add_button.clicked.connect(self.add_device)
        button_layout.addWidget(add_button)
        
        delete_button = QPushButton("Delete Selected Device")
        delete_button.clicked.connect(self.delete_device)
        button_layout.addWidget(delete_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def load_devices(self):
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
        dialog.setWindowTitle("Add Device")
        dialog.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()
        
        name_input = QLineEdit()
        name_input.setPlaceholderText("Enter Device Name")
        layout.addWidget(name_input)
        
        mac_input = QLineEdit()
        mac_input.setPlaceholderText("Enter MAC Address")
        layout.addWidget(mac_input)
        
        describe_input = QLineEdit()
        describe_input.setPlaceholderText("Enter Description")
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
                error_label.setText("Name and MAC Address cannot be empty.")
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
        
        cancel_button = QPushButton("Cancel")
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 300, 200)
        
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        self.list_device_saved_button = QPushButton("Danh sách thiết bị Bluetooth đã lưu")
        self.list_device_saved_button.clicked.connect(self.show_device_dialog)
        layout.addWidget(self.list_device_saved_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    def show_device_dialog(self):
        dialog = DeviceDialog()
        dialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
