import piexif
from PIL import Image

image = Image.open("test.jpg")
exif_data = image.info.get("exif", piexif.dump({}))

exif_dict = piexif.load(exif_data)

# Sử dụng UTF-8 để mã hóa
new_comment = """Tên: Đoàn Văn Hoàn
Loại phương tiện: Đi bộ
Biển kiểm soát: 51B-050196
Tốc độ vi phạm: 41km/h
Tốc độ quy định: 50km/h
Thời điểm ghi nhận: 17/11/2023 R:35
Vị trí ghi nhận: Vĩ độ 11,49
	      Kinh độ 109,46
	      Vị trí Km480-900
	      QL1A-Hà Tĩnh
Thiết bị: 05050 Kiểm định đến 10_2020
Đơn vị vân hành: Phòng Cảnh sát Giao thông Công an tỉnh Hà Nội
""".encode("utf-8")

exif_dict['0th'][piexif.ImageIFD.ImageDescription] = new_comment

exif_bytes = piexif.dump(exif_dict)
image.save("test.jpg", "jpeg", exif=exif_bytes)
