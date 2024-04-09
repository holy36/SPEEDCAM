import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kiểm tra nội dung file văn bản")
        self.setGeometry(100, 100, 600, 400)

        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        self.check_file_contents()

    def check_file_contents(self):
        try:

        except FileNotFoundError:
            self.text_edit.setPlainText("Không tìm thấy tệp văn bản 'text.txt'")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
