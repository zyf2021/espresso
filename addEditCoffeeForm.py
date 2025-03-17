from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QMessageBox
import sqlite3

class AddEditCoffeeForm(QDialog):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.coffee_id = coffee_id
        if self.coffee_id:
            self.load_coffee()

        self.saveButton.clicked.connect(self.save_data)

    def load_coffee(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        data = cur.execute("SELECT * FROM coffee WHERE id=?", (self.coffee_id,)).fetchone()
        con.close()

        if data:
            self.nameEdit.setText(data[1])
            self.roastLevelEdit.setText(data[2])
            self.typeEdit.setText(data[3])
            self.tasteEdit.setText(data[4])
            self.priceEdit.setText(str(data[5]))
            self.packageSizeEdit.setText(str(data[6]))

    def save_data(self):
        name = self.nameEdit.text()
        roast_level = self.roastLevelEdit.text()
        coffee_type = self.typeEdit.text()
        taste = self.tasteEdit.text()
        price = self.priceEdit.text()
        package_size = self.packageSizeEdit.text()

        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()

        if self.coffee_id:
            cur.execute("""
                UPDATE coffee SET name=?, roast_level=?, type=?, taste=?, price=?, package_size=?
                WHERE id=?
            """, (name, roast_level, coffee_type, taste, price, package_size, self.coffee_id))
        else:
            cur.execute("""
                INSERT INTO coffee (name, roast_level, type, taste, price, package_size) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, roast_level, coffee_type, taste, price, package_size))

        con.commit()
        con.close()
        self.accept()
