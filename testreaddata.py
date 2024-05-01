import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import QCoreApplication
import sys
import piexif
from PIL import Image, ExifTags
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
import exifread
import mysql.connector
# Gọi lớp giao diện từ file .ui (sử dụng pyuic6)
from testnew import Ui_MainWindow  # Thay thế "testnew_ui" bằng tên đúng của file ui đã chuyển đổi
import re
import datetime
import shutil
import os

# Tạo ứng dụng PyQt6
app = QApplication(sys.argv)

# Tạo cửa sổ chính và thiết lập giao diện
main_window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(main_window)

db = mysql.connector.connect(
    user='mobeo2002',
    password='doanquangluu',
    host='localhost',
    database='speed_gun'
)

def get_exif_info(image_path):
    with open(image_path, "rb") as image_file:
        exif_data = exifread.process_file(image_file, details=False)

    readable_exif = {}  # Từ điển để chứa dữ liệu EXIF

    # Lặp qua các thẻ EXIF và thêm vào từ điển readable_exif
    for tag in exif_data.keys():
        readable_exif[tag] = str(exif_data[tag])  # Chuyển đổi thành chuỗi

    return readable_exif

def format_exif(exif_info):
    # Kiểm tra xem ImageDescription có trong EXIF hay không
    description = exif_info.get("Image ImageDescription", "")

    # Thay thế các ký tự điều khiển nếu cần
    description = description.replace("\r", "").replace("\t", "    ")  # Thay thế tab bằng 4 khoảng trắng

    # Trả về mô tả đã được định dạng
    return description

# Kết nối sự kiện cho nút nhấn
def on_button_clicked():
    image_path = "test.jpg"  # Thay bằng đường dẫn hình ảnh của bạn
    # Đọc thông tin EXIF
    exif_info = get_exif_info(image_path)
    exif_str=str(exif_info)
    formatted_header = format_exif(exif_info)
    # exif_str = "\n".join([f"{tag}: {value}" for tag, value in exif_info.items()])
    ui.textEdit.setText(formatted_header)

def parse_date(date_str):
    # Loại bỏ khoảng trắng hoặc ký tự không mong đợi
    date_str_clean = date_str.strip()  # Xóa khoảng trắng ở đầu/cuối
    # Nếu có ký tự lạ, bạn có thể sử dụng biểu thức chính quy để chỉ lấy các ký tự số và /
    date_str_clean = re.sub(r"[^\d/]", "", date_str_clean)  # Chỉ giữ số và dấu /

    # Định dạng ngày mong đợi
    date_format = "%d/%m/%Y"

    try:
        date_obj = datetime.datetime.strptime(date_str_clean, date_format).date()  # Chuyển đổi sang kiểu date
        return date_obj
    except ValueError as ve:
        print(f"Lỗi chuyển đổi ngày: {ve}")
        return None  # Hoặc giá trị mặc định nếu cần

def on_clear_button_clicked():
    # Lấy văn bản từ textEdit
    header_text = ui.textEdit.toPlainText()

    # Trích xuất thông tin ngày từ văn bản
    date_str = header_text.split("Thời điểm ghi nhận: ")[1].split(" ")[0]  # Lấy giá trị ngày

    # Chuyển đổi từ chuỗi sang kiểu datetime.date
    date_format = "%d/%m/%Y"  # Định dạng của chuỗi ngày
    date_obj = parse_date(date_str)  # Chuyển đổi sang kiểu date

    # Trích xuất các thông tin khác
    speed_match = re.search(r"Tốc độ vi phạm: (\d+)km/h", header_text)
    speed = speed_match.group(1) if speed_match else "0"

    name_match = re.search(r"Tên: (.+?)(\n|$)", header_text)

    if name_match:
        name = name_match.group(1).strip()  # Lấy kết quả đầu tiên và loại bỏ khoảng trắng thừa
    else:
        name = ""  # Nếu không tìm thấy, xử lý theo cách khác    vehicle = header_text.split("Loại phương tiện: ")[1].split("\n")[0]
    vehicle = header_text.split("Loại phương tiện: ")[1].split("\n")[0]
    plate = header_text.split("Biển kiểm soát: ")[1].split("\n")[0]
    location = header_text.split("Đơn vị vân hành: Phòng Cảnh sát Giao thông Công an tỉnh ")[1].strip()
    print(location)
    device = header_text.split("Thiết bị: ")[1].split(" ")[0]
    
    status=1
    with open("image_send.jpg", "rb") as file:
        image_data = file.read()  # Đọc dữ liệu nhị phân từ tệp

    # Kết nối với cơ sở dữ liệu MySQL và chèn dữ liệu vào
    db = mysql.connector.connect(
        user='mobeo2002',
        password='doanquangluu',
        host='localhost',
        database='speed_gun'
    )

    cursor = db.cursor()  # Tạo cursor
    insert_query = "INSERT INTO image (name, status, vehicle, plate, speed, date, location, device) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    data = ( name, status, vehicle, plate, speed, date_obj, location, device)  # Dùng date_obj

    cursor.execute(insert_query, data)
    select_query = """
    SELECT id 
    FROM image
    WHERE 
        name = %s AND 
        status = %s AND 
        vehicle = %s AND 
        plate = %s AND 
        speed = %s AND 
        date = %s AND 
        location = %s AND 
        device = %s
    """
    data = ( name, status, vehicle, plate, speed, date_obj, location, device)
    cursor.execute(select_query, data)

    # Lấy kết quả
    result = cursor.fetchone()
    # Sao chép và đổi tên hình ảnh
    current_folder = os.path.dirname(__file__)

# Tạo đường dẫn đến thư mục "database"
    database_folder = os.path.join(current_folder, "database")

    # Đảm bảo thư mục "database" tồn tại, nếu không thì tạo nó
    if not os.path.exists(database_folder):
        os.makedirs(database_folder)

    # Đường dẫn đến tệp gốc
    source_image = "test.jpg"

    # Tên tệp mới (dựa trên giá trị kết quả)
    destination_image = f"{result[0]}.jpg"

    # Đường dẫn đầy đủ đến thư mục "database" để sao chép tệp
    destination_path = os.path.join(database_folder, destination_image)

    # Sao chép tệp vào thư mục "database"
    shutil.copy(source_image, destination_path)

    # Cập nhật cột `image` với tên tệp mới
    update_query = "UPDATE image SET image = %s WHERE id = %s"
    cursor.execute(update_query, (destination_path, result[0]))  # Chỉ lấy giá trị đầu tiên từ tuple
    db.commit()  # Xác nhận thay đổi

    # Xóa nội dung trong textEdit sau khi chèn
    ui.textEdit.clear()



ui.pushButton.clicked.connect(on_button_clicked)
ui.clearButton.clicked.connect(on_clear_button_clicked)

# Hiển thị cửa sổ chính
main_window.show()

# Khởi động ứng dụng PyQt6
sys.exit(app.exec())
