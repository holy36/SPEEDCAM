from PyQt6 import QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QtWidgets.QVBoxLayout(self)
        
        # Tạo QGraphicsView để hiển thị hình ảnh
        self.graphics_view = QtWidgets.QGraphicsView(self)
        layout.addWidget(self.graphics_view)
        
        # Tạo QGraphicsScene và thiết lập nó cho QGraphicsView
        self.scene = QtWidgets.QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        
        # Load hình ảnh từ tệp hoặc pixmap
        pixmap = QtGui.QPixmap("test.jpg")
        
        # Tính toán tỉ lệ giữa chiều rộng và chiều cao của pixmap so với layout
        layout_ratio = self.graphics_view.width() / self.graphics_view.height()
        pixmap_ratio = pixmap.width() / pixmap.height()
        
        # Thay đổi kích thước của pixmap sao cho phù hợp với layout
        if layout_ratio > pixmap_ratio:
            pixmap = pixmap.scaledToWidth(self.graphics_view.width())
        else:
            pixmap = pixmap.scaledToHeight(self.graphics_view.height())
        
        # Tạo QGraphicsPixmapItem và thêm vào QGraphicsScene
        self._photo = QtWidgets.QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self._photo)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())
