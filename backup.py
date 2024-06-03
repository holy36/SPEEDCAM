from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QLabel, QApplication, QVBoxLayout, QWidget, QScrollBar
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtCore import Qt, QRect
import sys

class CustomScrollBar(QScrollBar):
    def __init__(self, orientation, placeholder_text, parent=None):
        super().__init__(orientation, parent)
        self.placeholder_text = placeholder_text

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QColor("#888"))
        painter.setFont(QFont("Arial", 10))

        if self.orientation() == Qt.Orientation.Vertical:
            rect = QRect(0, 0, self.width(), self.height())
            painter.rotate(90)
            painter.translate(0, -self.width())
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.placeholder_text)
        else:
            rect = QRect(0, 0, self.width(), self.height())
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.placeholder_text)

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.databasetable = QTableWidget()
        self.databasetable.setColumnCount(3)
        self.databasetable.setHorizontalScrollBar(CustomScrollBar(Qt.Orientation.Horizontal, "Thanh cuộn ngang", self))
        self.databasetable.setVerticalScrollBar(CustomScrollBar(Qt.Orientation.Vertical, "Thanh cuộn dọc", self))
        self.des_scrollbar_table(self.databasetable)

        layout = QVBoxLayout()
        layout.addWidget(self.databasetable)
        self.setLayout(layout)

    def des_scrollbar_table(self, table):
        scrollbar_style = """
            QScrollBar:vertical {
                border: none;
                background: #f1f1f1;
                width: 25px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #0000FF;  /* Blue color */
                min-height: 20px;
            }
            QScrollBar::add-line:vertical {
                background: #f1f1f1;
                height: 20px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                background: #f1f1f1;
                height: 20px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar:horizontal {
                border: none;
                background: #f1f1f1;
                height: 25px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:horizontal {
                background: #0000FF;  /* Blue color */
                min-width: 20px;
            }
            QScrollBar::add-line:horizontal {
                background: #f1f1f1;
                width: 20px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:horizontal {
                background: #f1f1f1;
                width: 20px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }
        """
        table.verticalScrollBar().setStyleSheet(scrollbar_style)
        table.horizontalScrollBar().setStyleSheet(scrollbar_style)

    def populateTable(self, rows):
        self.databasetable.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                if j == 1:
                    item = self.getImageLabel(value)
                    self.databasetable.setCellWidget(i, j, item)
                elif j == 2:
                    if value == 0:
                        self.databasetable.setItem(i, j, QTableWidgetItem("Từ chối"))
                    else:
                        self.databasetable.setItem(i, j, QTableWidgetItem("Đồng ý"))
                else:
                    self.databasetable.setItem(i, j, QTableWidgetItem(str(value)))

    def getImageLabel(self, value):
        # Placeholder for the actual implementation of getImageLabel
        label = QLabel()
        pixmap = QPixmap(value)  # Assuming value is the path to the image
        label.setPixmap(pixmap)
        return label

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MyApp()
    
    # Example data
    rows = [
        [1, 'image1.png', 0],
        [2, 'image2.png', 1],
        [3, 'image3.png', 0]
    ]
    mainWin.populateTable(rows)
    
    mainWin.show()
    sys.exit(app.exec())
