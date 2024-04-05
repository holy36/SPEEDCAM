
# Form implementation generated from reading ui file 'display.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import socket

import time
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QCoreApplication
# from bluetooth import Protocols
import bluetooth
import sys
from time import sleep
from PyQt6.QtWidgets import QApplication, QMainWindow, QSizePolicy, QVBoxLayout, QWidget, QPinchGesture, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QObject, QThread, pyqtSignal, Qt,QEvent
import display


class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPointF)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.grabGesture(Qt.GestureType.PinchGesture)
        self.setScene(self._scene)
        self.setTransformationAnchor(
            QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(
            QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

    def event(self,event):
        if event.type() == QEvent.Type.Gesture:
            gesture = event.gesture(Qt.GestureType.PinchGesture)
            # print(gesture)
            if gesture:
                self.handle_pinch(gesture)
                return True
        return super().event(event)

    def handle_pinch(self, gesture):
        scale_factor = gesture.scaleFactor()
        if(scale_factor>1):
            self._zoom +=(scale_factor-1)
        else:
            self._zoom -=(1-scale_factor)
        if self._zoom > 0:
            self.scale(scale_factor,scale_factor)
        else:
            self.fitInView()
        print(scale_factor)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                print(viewrect)
                print(scenerect)
                self.scale(factor, factor)
                pass
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom <= 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.DragMode.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.position().toPoint()))
        super(PhotoViewer, self).mousePressEvent(event)

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def run(self):
        """Long-running task."""
        print("Đang tìm kiếm các thiết bị Bluetooth xung quanh...")
        nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True)
        print("Các thiết bị Bluetooth xung quanh:")
        for addr, name in nearby_devices:
            # self.device_list.addItem(f"{addr} - {name}")
            self.progress.emit(f"{addr} - {name}")
            print(f"{addr} - {name}")
        self.finished.emit()
    def connect(self,id):
        option = id
        device_address = option[:17]
        port = 1  # RFCOMM port number
        # try:
        print(f"Đang kết nối đến thiết bị có địa chỉ {device_address}...")
        sock = bluetooth.BluetoothSocket(socket.BTPROTO_RFCOMM)
        sock.connect((device_address, port))
        while(1):
            pass
        self.finished.emit()
        # except Exception as e:
        #     print("Kết nối thất bại")
        #     return None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = display.Ui_MainWindow()
        self.uic.setupUi(self)
        self.viewer = PhotoViewer(self)
        self.uic.image_layout.addWidget(self.viewer)
        self.viewer.setPhoto(QtGui.QPixmap('test.jpg'))
        self.thread = {}
        self.grabGesture(Qt.GestureType.PinchGesture)
        self.showMaximized()
        self.uic.connect_button.clicked.connect(self.connect)
        self.uic.cancel_button.clicked.connect(self.cancel_connection)
        self.uic.device_list.setPlaceholderText( "Danh sách thiết bị Bluetooth")
        self.uic.device_list.activated.connect(self.device_list_select)
        self.uic.cancel_button.setStyleSheet("background-color: #66CDAA; color: white;")
        self.uic.quitbutton.clicked.connect(self.exit)
        self.uic.minbutton.clicked.connect(self.minimize_window)
        self.uic.maxbutton.clicked.connect(self.maximize_window)
        self.uic.bground.setStyleSheet("background-color: #949084; color: white;")
        self.uic.bground.setText("Thiết bị truy cập trực tiếp máy bắn tốc độ - SPR Lab")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)



        

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/window-minimize.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.uic.minbutton.setIcon(icon)
        self.uic.minbutton.setIconSize(QtCore.QSize(25, 30))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon/png-clipart-computer-icons-derosa-music-bluetooth-bluetooth-text-trademark-thumbnail.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.uic.connect_button.setIcon(icon2)
        self.uic.connect_button.setIconSize(QtCore.QSize(25, 30))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icon/pngtree-chek-mark-rounded-icon-tick-box-vector-png-image_17766700.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.uic.accept_button.setIcon(icon3)
        self.uic.accept_button.setIconSize(QtCore.QSize(25, 30))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icon/473-4730000_deny-comments-saturation-icon-png.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.uic.deny_button.setIcon(icon4)
        self.uic.deny_button.setIconSize(QtCore.QSize(25, 30))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icon/2017609-200.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.uic.quitbutton.setIcon(icon5)
        self.uic.quitbutton.setIconSize(QtCore.QSize(25, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon/54860.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.uic.maxbutton.setIcon(icon1)
        self.uic.maxbutton.setIconSize(QtCore.QSize(25, 30))


        
    
        self.image = QPixmap("test.jpg")
        self.uic.image_label.setPixmap(self.image)
        self.uic.image_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.uic.image_label.setScaledContents(True)

        self.uic.device_list.setDisabled(1)
        self.uic.accept_button.setDisabled(1)
        self.uic.deny_button.setDisabled(1)
        self.viewer.fitInView()
    
    def exit(self):
        # Thực hiện các hành động bạn muốn khi thoát ứng dụng
        QtWidgets.QApplication.quit()

    def minimize_window(self):
        # Minimize cửa sổ
        self.showMinimized()

    def maximize_window(self):
        # Maximize hoặc phục hồi cửa sổ
        if self.isMaximized():
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap("icon/maximize-icon-512x512-ari7tfdx.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.uic.maxbutton.setIcon(icon1)
            self.uic.maxbutton.setIconSize(QtCore.QSize(25, 30))
            self.showNormal()

        else:
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap("icon/54860.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.uic.maxbutton.setIcon(icon1)
            self.uic.maxbutton.setIconSize(QtCore.QSize(25, 30))
            self.showMaximized()

        

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:  # Phóng to khi cuộn lên
            self.zoom(1.1)
        else:  # Thu nhỏ khi cuộn xuống
            self.zoom(0.9)

    def zoom(self, factor):
        self.image = self.image.scaled(self.image.size() * factor)
        pixmap = self.image.scaled(self.image.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.uic.image_label.setPixmap(pixmap)


    def device_list_select(self):
        option = self.uic.device_list.currentText()
        device_address = option[:17]
        self.thread[2] = ThreadClass(index=1,mac_id=device_address)
        self.thread[2].start()
        self.thread[2].signal.connect(self.my_function)
        self.thread[2].connect_status.connect(self.status_change)
    def my_function(self, msg):
        i = self.uic.MainWindow.sender().index
        self.uic.image_label.setText(msg)

    def cancel_connection(self):
        self.thread[2].stop()
        self.uic.connect_button.setMaximumWidth(9999999)
        self.uic.cancel_button.setMaximumWidth(0)

    def status_change(self,status):
        self.uic.connect_button.setDisabled(0)
        self.uic.device_list.setDisabled(0)
        if status>3:
            self.uic.connect_button.setDisabled(1)
            self.uic.device_list.setDisabled(1)
            self.uic.connect_button.setMaximumWidth(9999999)
            self.uic.cancel_button.setMaximumWidth(0)
            self.uic.connect_button.setStyleSheet("background-color: #f7f57c; color: black;")
            self.uic.connect_button.setText("Đang kết nối tới thiết bị")
        if status==1:
            self.uic.connect_button.setMaximumWidth(0)
            self.uic.cancel_button.setMaximumWidth(9999999)
        if status==0:
            self.uic.connect_button.setMaximumWidth(9999999)
            self.uic.cancel_button.setMaximumWidth(0)
        if status==3:
            self.uic.connect_button.setStyleSheet("background-color: #f7917c; color: white;")
            self.uic.connect_button.setText("Kết nối thất bại! Nhấn kết nối lại!")
        # self.thread[2].connect_status.emit(3)

        pass

    def reportProgress(self, n):
        self.uic.device_list.addItem(n)

    def connect(self):
        # Thiết lập màu của nút thành màu xanh
        self.uic.connect_button.setStyleSheet("background-color: #f7f57c; color: black;")
        self.uic.connect_button.setText("Đang quét thiết bị xung quanh...")
        self.uic.connect_button.setDisabled(1)
        QCoreApplication.processEvents()  # Cập nhật giao diện người dùng
        self.uic.device_list.clear() 

        # Step 2: Create a QThread object
        self.thread[1] = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread[1])
        # Step 5: Connect signals and slots
        self.thread[1].started.connect(self.worker.run)
        self.worker.finished.connect(self.thread[1].quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread[1].finished.connect(self.thread[1].deleteLater)
        self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread[1].start()

        # Final resets
        self.uic.connect_button.setEnabled(False)
        self.thread[1].finished.connect(
            lambda: self.uic.connect_button.setEnabled(True)
        )
        self.thread[1].finished.connect(
            lambda: self.uic.connect_button.setStyleSheet("background-color: #6495ED; color: white;")
        )
        self.thread[1].finished.connect(
            lambda: self.uic.connect_button.setText("Đã bật Bluetooth! Nhấn để quét Bluetooth lại!")
        )
        self.thread[1].finished.connect(
            lambda:  self.uic.device_list.setDisabled(0)
        )
        self.thread[1].finished.connect(
            lambda: self.uic.connect_button.setDisabled(0)
        )
        # Sau khi tìm thấy các thiết bị, cập nhật lại màu của nút thành màu xanh lá cây
        



class ThreadClass(QtCore.QThread):
    signal = pyqtSignal(str)
    connect_status = pyqtSignal(int)

    def __init__(self, index=0, mac_id = ""):
        super().__init__()
        self.index = index
        self.mac_id = mac_id

    def run(self):
        # print('Starting thread...', self.index,self.mac_id)
        self.connect_status.emit(4)
        counter = 0
            
        try:
            self.connect_status.emit(5)
            client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            client.connect((self.mac_id, 4))

            # print(f"Connected!")

            self.connect_status.emit(1)
            while True:
                # message = input("Enter message: ")
                # client.send(message.encode('utf-8'))
                data = client.recv(1024)
                if not data:
                    break
                # print(f"Received: {data.decode('utf-8')}")
                # print(self.connect_status)
                self.signal.emit(f"{data.decode('utf-8')}")

        except OSError:
            self.connect_status.emit(3)
            pass

        # print("Disconnected")
        self.connect_status.emit(0)

        client.close()

    def stop(self):
        print('Stopping thread...', self.index)
        self.connect_status.emit(0)
        self.terminate()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())