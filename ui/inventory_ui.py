import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QLineEdit

SERVER_URL = "http://localhost:5000"

class InventoryUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Item Name", "Quantity"])
        self.layout.addWidget(self.table)

        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        self.refresh_inventory()

    def refresh_inventory(self):
        self.status_label.setText("Refreshing inventory...")
        try:
            response = requests.get(f"{SERVER_URL}/inventory")
            if response.status_code == 200:
                items = response.json().get("items", [])
                self.update_table(items)
        except Exception as e:
            self.status_label.setText("Error fetching inventory")

    def update_table(self, items):
        self.table.setRowCount(0)
        for row_idx, (name, quantity) in enumerate(items):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(name))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(quantity)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryUI()
    window.show()
    sys.exit(app.exec_())
