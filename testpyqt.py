import sys
from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog, QLabel, QHBoxLayout, QLineEdit, QFormLayout

class MemoryMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Memory Monitor")
        self.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()
        
        self.check_button = QPushButton("Check Memory", self)
        self.check_button.clicked.connect(self.show_custom_dialog)
        layout.addWidget(self.check_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_custom_dialog(self):
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Delete Options")

        layout = QVBoxLayout(self.dialog)
        
        label = QLabel("Select the delete criteria:", self.dialog)
        layout.addWidget(label)

        button_speed = QPushButton("Delete by speed range", self.dialog)
        button_speed.clicked.connect(lambda: self.delete_by_criteria("speed range"))
        layout.addWidget(button_speed)

        button_time = QPushButton("Delete by time range", self.dialog)
        button_time.clicked.connect(lambda: self.delete_by_criteria("time range"))
        layout.addWidget(button_time)

        button_id = QPushButton("Delete by ID range", self.dialog)
        button_id.clicked.connect(lambda: self.delete_by_criteria("ID range"))
        layout.addWidget(button_id)

        button_location = QPushButton("Delete by recording location", self.dialog)
        button_location.clicked.connect(lambda: self.delete_by_criteria("recording location"))
        layout.addWidget(button_location)

        button_device = QPushButton("Delete by recording device", self.dialog)
        button_device.clicked.connect(lambda: self.delete_by_criteria("recording device"))
        layout.addWidget(button_device)

        button_vehicle = QPushButton("Delete by violating vehicle", self.dialog)
        button_vehicle.clicked.connect(lambda: self.delete_by_criteria("violating vehicle"))
        layout.addWidget(button_vehicle)

        button_status = QPushButton("Delete by confirmation status", self.dialog)
        button_status.clicked.connect(lambda: self.delete_by_criteria("confirmation status"))
        layout.addWidget(button_status)

        cancel_button = QPushButton("Cancel", self.dialog)
        cancel_button.setFixedSize(100, 30)  # Sửa kích cỡ nút "Cancel"
        cancel_button.clicked.connect(self.dialog.reject)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.dialog.setLayout(layout)
        self.dialog.exec()

    def delete_by_criteria(self, criteria):
        self.dialog.accept()  # Đóng dialog hiện tại

        input_dialog = QDialog(self)
        input_dialog.setWindowTitle(f"Delete by {criteria}")

        form_layout = QFormLayout(input_dialog)

        if criteria == "speed range":
            min_speed_label = QLabel("Minimum Speed:", input_dialog)
            self.min_speed_input = QLineEdit(input_dialog)
            form_layout.addRow(min_speed_label, self.min_speed_input)

            max_speed_label = QLabel("Maximum Speed:", input_dialog)
            self.max_speed_input = QLineEdit(input_dialog)
            form_layout.addRow(max_speed_label, self.max_speed_input)

        # Add more inputs based on the criteria if needed.

        delete_button = QPushButton("Delete", input_dialog)
        delete_button.clicked.connect(lambda: self.delete_records(criteria, input_dialog))
        form_layout.addWidget(delete_button)

        cancel_button = QPushButton("Cancel", input_dialog)
        cancel_button.clicked.connect(input_dialog.reject)
        form_layout.addWidget(cancel_button)

        input_dialog.setLayout(form_layout)
        input_dialog.exec()

    def delete_records(self, criteria, dialog):
        if criteria == "speed range":
            min_speed = self.min_speed_input.text()
            max_speed = self.max_speed_input.text()
            # Here you would add code to delete records from the database based on speed range.
            QMessageBox.information(self, "Info", f"Deleted records with speed range: {min_speed} - {max_speed}")
        
        # Add more delete logic based on the criteria if needed.

        dialog.accept()  # Close the input dialog after deletion.

def main():
    app = QApplication(sys.argv)
    window = MemoryMonitor()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
