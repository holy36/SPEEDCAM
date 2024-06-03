import sys
import psutil
from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer

class MemoryMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        self.check_memory()

    def initUI(self):
        self.setWindowTitle("Memory Monitor")
        self.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()
        
        self.check_button = QPushButton("Check Memory Now", self)
        self.check_button.clicked.connect(self.show_memory_info)
        layout.addWidget(self.check_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_memory)
        self.timer.start(60000)  # Check every 60 seconds

    def check_memory(self):
        memory = psutil.virtual_memory()
        available_memory_percentage = memory.available * 100 / memory.total

        if available_memory_percentage < 10:
            self.show_warning(available_memory_percentage, memory.available)

    def show_memory_info(self):
        memory = psutil.virtual_memory()
        available_memory_percentage = memory.available * 100 / memory.total
        available_memory_mb = memory.available / (1024 ** 2)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Memory Information")
        msg.setText(
            f"Available memory: {available_memory_percentage:.2f}%\n"
            f"Remaining memory: {available_memory_mb:.2f} MB"
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def show_warning(self, available_memory_percentage, available_memory):
        available_memory_mb = available_memory / (1024 ** 2)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Memory Warning")
        msg.setText(
            f"Available memory is below 10%: {available_memory_percentage:.2f}%\n"
            f"Remaining memory: {available_memory_mb:.2f} MB"
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
