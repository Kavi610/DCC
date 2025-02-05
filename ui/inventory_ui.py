import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

SERVER_URL = "http://127.0.0.1:5000"

class InventoryUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("Inventory Items:")
        layout.addWidget(self.label)
        self.refresh_inventory()
        self.setLayout(layout)

    def refresh_inventory(self):
        response = requests.get(f"{SERVER_URL}/get-items")
        items = response.json()
        self.label.setText(f"Inventory:\n" + "\n".join([f"{item['name']} - {item['quantity']}" for item in items]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryUI()
    window.show()
    sys.exit(app.exec_())
