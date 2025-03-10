import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QDialog
from addEditCoffeeForm import AddEditCoffeeForm


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.load_data()

        # Кнопки
        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)

    def load_data(self):
        """Загрузка данных из базы в таблицу."""
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        data = cur.execute("SELECT * FROM coffee").fetchall()
        con.close()

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))

        for i, row in enumerate(data):
            for j, value in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))

    def add_coffee(self):
        """Открытие формы добавления кофе."""
        dialog = AddEditCoffeeForm(self)
        if dialog.exec():
            self.load_data()

    def edit_coffee(self):
        """Открытие формы редактирования выбранной записи."""
        selected = self.tableWidget.currentRow()
        if selected == -1:
            return
        coffee_id = self.tableWidget.item(selected, 0).text()
        dialog = AddEditCoffeeForm(self, coffee_id)
        if dialog.exec():
            self.load_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
