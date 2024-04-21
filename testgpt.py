import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
import mysql.connector

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Database Table")
        self.setGeometry(100, 100, 600, 400)

        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)

        self.populateTable()

    def populateTable(self):
        db = mysql.connector.connect(
            user='mobeo2002',
            password='doanquangluu',
            host='localhost',
            database='speed_gun'
        )
        cursor = db.cursor()
        cursor.execute("SELECT * FROM image")  # Select all columns from your table
        rows = cursor.fetchall()

        # Set table size
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(len(rows[0])+2)  # Assuming all rows have the same number of columns

        # Set table headers
        headers = [desc[2] for desc in cursor.description]
        self.tableWidget.setHorizontalHeaderLabels(headers)

        # Populate table with data
        for i, row in enumerate(rows):
            for j, value in enumerate(row, start=0):
                self.tableWidget.setItem(i, j+2, QTableWidgetItem(str(value)))

        db.close()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
