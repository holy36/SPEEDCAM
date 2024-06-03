import sys
import psutil
from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer

class MemoryMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Memory Monitor")
        self.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()
        
        self.check_button = QPushButton("Check Disk Space Now", self)
        self.check_button.clicked.connect(self.show_disk_info)
        layout.addWidget(self.check_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_disk_info(self):
        disk_usage = psutil.disk_usage('/')
        available_disk_percentage = disk_usage.free * 100 / disk_usage.total
        available_disk_gb = disk_usage.free / (1024 ** 3)  # Convert bytes to gigabytes
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Disk Space Information")
        msg.setText(
            f"Available disk space: {available_disk_percentage:.2f}%\n"
            f"Remaining disk space: {available_disk_gb:.2f} GB"
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

def main():
    app = QApplication(sys.argv)
    window = MemoryMonitor()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
