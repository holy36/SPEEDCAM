
from PyQt6 import QtCore, QtGui, QtWidgets
import display

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QMainWindow()
    ui = display.Ui_MainWindow()
    ui.setupUi(w)
    w.show()
    sys.exit(app.exec())