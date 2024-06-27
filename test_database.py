import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTimeEdit, QPushButton
from PyQt6.QtCore import QTime

class TimePickerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.timeEdit = QTimeEdit(self)
        self.timeEdit.setTime(QTime.currentTime())
        self.layout.addWidget(self.timeEdit)

        self.btn = QPushButton('Hiển thị Thời gian', self)
        self.btn.clicked.connect(self.showTime)
        self.layout.addWidget(self.btn)

        self.setLayout(self.layout)
        self.setWindowTitle('Chọn Thời gian')
        self.show()

    def showTime(self):
        selected_time = self.timeEdit.time()
        print(f'Thời gian đã chọn: {selected_time.toString()}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TimePickerWidget()
    sys.exit(app.exec())
