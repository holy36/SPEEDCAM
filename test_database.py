import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QTextEdit, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QPainter, QFont, QFontMetrics
from PyQt6.QtCore import Qt, QRect

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Thêm nội dung text vào hình ảnh")

        # Tạo các widgets
        self.image_label = QLabel()
        self.merge_text_edit = QTextEdit()
        with open('test.txt', 'r') as file:
            merge_text = file.read()
            if "Phong Canh sat" in merge_text:
                merge_text = merge_text.replace("Phong Canh sat Giao thong", "Phong Canh sat Giao thong\n")
                self.merge_text_edit.setText(merge_text)
            else:
                self.merge_text_edit.setText(merge_text)
        self.generate_button = QPushButton("Thêm Text và Lưu")
        self.generate_button.clicked.connect(self.add_text_to_image)

        # Tạo layout chính
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.merge_text_edit)
        main_layout.addWidget(self.generate_button)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def add_text_to_image(self):
        with open('test.txt', 'r') as file:
            merge_text = file.read()
            if "Phong Canh sat" in merge_text:
                merge_text = merge_text.replace("Phong Canh sat Giao thong", "Phong Canh sat Giao thong\n")
                self.merge_text_edit.setText(merge_text)
            else:
                self.merge_text_edit.setText(merge_text)
        # Đọc hình ảnh và thêm khoảng trắng bên phải
        image = QPixmap("test.jpg")
        width = image.width()
        height = image.height()
        new_width = int(width * 1.5)  # Tăng chiều rộng lên 50%
        new_image = QPixmap(new_width, height)
        new_image.fill(Qt.GlobalColor.white)  # Tạo nền trắng mới

        # Vẽ hình ảnh gốc lên hình mới
        painter = QPainter(new_image)
        painter.drawPixmap(0, 0, image)
        painter.end()

        # Chèn văn bản vào phần trắng bên phải
        painter = QPainter(new_image)
        painter.setFont(QFont("Arial", 40))
        painter.drawText(image.width(), 0, new_width - image.width(), height, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, merge_text)
        painter.end()

        # Lưu hình ảnh với text vào file mới
        save_path = "merge.png"
        if save_path:
            new_image.save(save_path)
            QMessageBox.information(self, "LoginOutput", "Update thanh cong")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
