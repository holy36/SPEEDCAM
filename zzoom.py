import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class View(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grabGesture(Qt.PinchGesture)
        self.grabGesture(Qt.SwipeGesture)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-5000, -5000, 10000, 10000)
        self.scene.addRect(0, 0, 100, 100, QPen(Qt.NoPen), QBrush(Qt.green))

        self.setScene(self.scene)

    def event(self, event):
        if isinstance(event, QNativeGestureEvent) and event.gestureType() == Qt.NativeGestureType.ZoomNativeGesture:
            return self.zoomNativeEvent(event)
        return super().event(event)

    def zoomNativeEvent(self, event: QNativeGestureEvent):
        print(f"Pinch Gesture Event: pos{event.pos().x(), event.pos().y()} value({event.value()})")
        return super().event(event)

    def gestureEvent(self, event):
        print("Gesture event")

        if event.gesture(Qt.PinchGesture):
            print("Pinch gesture")
            self.pinchTriggered(QPinchGesture(event.gesture(Qt.PinchGesture)))
        if event.gesture(Qt.SwipeGesture):
            print("Swipe gesture")
            self.swipeTriggered(QSwipeGesture(event.gesture(Qt.SwipeGesture)))

        print()
        return True

    def pinchTriggered(self, gesture):
        changeFlags = gesture.changeFlags()
        
        if changeFlags & QPinchGesture.ScaleFactorChanged:
            print("Scale factor changed", gesture.scaleFactor(), gesture.totalScaleFactor(), gesture.lastScaleFactor())

    def swipeTriggered(self, gesture):
        pass

app = QApplication([sys.argv])

view = View()
view.show()

app.exec()