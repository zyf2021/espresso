import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem
from UI.main_ui import Ui_MainWindow
from UI.addEditCoffeeForm_ui import Ui_Dialog


class CoffeeDatabase:
    def __init__(self, db_path="data/coffee.sqlite"):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def get_coffee(self):
        return self.cursor.execute("SELECT * FROM coffee").fetchall()

    def add_coffee(self, name, roast, coffee_type, taste, price, size):
        self.cursor.execute(
            "INSERT INTO coffee (name, roast_level, type, taste, price, package_size) VALUES (?, ?, ?, ?, ?, ?)",
            (name, roast, coffee_type, taste, price, size),
        )
        self.connection.commit()

    def update_coffee(self, coffee_id, name, roast, coffee_type, taste, price, size):
        self.cursor.execute(
            "UPDATE coffee SET name=?, roast_level=?, type=?, taste=?, price=?, package_size=? WHERE id=?",
            (name, roast, coffee_type, taste, price, size, coffee_id),
        )
        self.connection.commit()


class CoffeeApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = CoffeeDatabase()
        self.load_coffee()
        self.addButton.clicked.connect(self.open_add_dialog)
        self.editButton.clicked.connect(self.open_edit_dialog)

    def load_coffee(self):
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        data = self.db.get_coffee()
        print(data)

        for row_data in data:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            for col, data in enumerate(row_data):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(data)))

    def open_add_dialog(self):
        dialog = CoffeeDialog(self.db, parent=self)
        dialog.exec()
        self.load_coffee()

    def open_edit_dialog(self):
        selected = self.tableWidget.currentRow()
        if selected >= 0:
            coffee_id = int(self.tableWidget.item(selected, 0).text())
            name = self.tableWidget.item(selected, 1).text()
            roast = self.tableWidget.item(selected, 2).text()
            coffee_type = self.tableWidget.item(selected, 3).text()
            taste = self.tableWidget.item(selected, 4).text()
            price = self.tableWidget.item(selected, 5).text()
            size = self.tableWidget.item(selected, 6).text()

            dialog = CoffeeDialog(self.db, coffee_id, name, roast, coffee_type, taste, price, size, self)
            dialog.exec()
            self.load_coffee()


class CoffeeDialog(QDialog, Ui_Dialog):
    def __init__(self, db, coffee_id=None, name="", roast="", coffee_type="", taste="", price="", size="", parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.db = db
        self.coffee_id = coffee_id

        self.nameEdit.setText(name)
        self.roastLevelEdit.setText(roast)
        self.typeEdit.setText(coffee_type)
        self.tasteEdit.setText(taste)
        self.priceEdit.setText(price)
        self.packageSizeEdit.setText(size)

        self.saveButton.clicked.connect(self.save_data)

    def save_data(self):
        name = self.nameEdit.text()
        roast = self.roastLevelEdit.text()
        coffee_type = self.typeEdit.text()
        taste = self.tasteEdit.text()
        price = self.priceEdit.text()
        size = self.packageSizeEdit.text()

        if self.coffee_id:
            self.db.update_coffee(self.coffee_id, name, roast, coffee_type, taste, price, size)
        else:
            self.db.add_coffee(name, roast, coffee_type, taste, price, size)

        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CoffeeApp()
    main_window.show()
    sys.exit(app.exec())


#
