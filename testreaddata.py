import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import QCoreApplication
import sys
import piexif
from PIL import Image, ExifTags
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
import exifread

# Gọi lớp giao diện từ file .ui (sử dụng pyuic6)
from testnew import Ui_MainWindow  # Thay thế "testnew_ui" bằng tên đúng của file ui đã chuyển đổi

# Tạo ứng dụng PyQt6
app = QApplication(sys.argv)

# Tạo cửa sổ chính và thiết lập giao diện
main_window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(main_window)

def get_exif_info(image_path):
    # Mở tệp hình ảnh ở chế độ binary
    with open(image_path, "rb") as image_file:
        # Đọc dữ liệu EXIF
        exif_data = exifread.process_file(image_file, details=False)

    readable_exif = {}  # Từ điển để chứa dữ liệu EXIF dễ đọc

    # Lặp qua các thẻ EXIF và thêm vào từ điển readable_exif
    for tag in exif_data.keys():
        readable_exif[tag] = str(exif_data[tag])

    return readable_exif  # Trả về dữ liệu EXIF

# Kết nối sự kiện cho nút nhấn
def on_button_clicked():
    image_path = "test_with_metadata.jpg"  # Thay bằng đường dẫn hình ảnh của bạn
    # Đọc thông tin EXIF
    exif_info = get_exif_info(image_path)
    exif_str=str(exif_info)
    # exif_str = "\n".join([f"{tag}: {value}" for tag, value in exif_info.items()])
    ui.textEdit.setText(exif_str)


ui.pushButton.clicked.connect(on_button_clicked)

# Hiển thị cửa sổ chính
main_window.show()

# Khởi động ứng dụng PyQt6
sys.exit(app.exec())
