import sys
import json
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QLabel, QLineEdit
)
from PyQt5.QtCore import QThread, pyqtSignal

SERVER_URL = "http://localhost:5000"

class FetchInventoryThread(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def run(self):
        try:
            # For simplicity, assume there's an endpoint that returns the full inventory.
            # We can simulate it by directly querying the database if needed.
            # Here, we'll assume our server does not have a GET endpoint for inventory,
            # so we simulate it by reading from a local file or embedding a query.
            # For demonstration, we use the SQLite DB directly.
            import sqlite3
            conn = sqlite3.connect("inventory.db")
            c = conn.cursor()
            c.execute("SELECT name, quantity FROM inventory")
            items = c.fetchall()
            conn.close()
            self.finished.emit(items)
        except Exception as e:
            self.error.emit(str(e))

class UpdateInventoryThread(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, endpoint, payload):
        super().__init__()
        self.endpoint = endpoint
        self.payload = payload

    def run(self):
        try:
            response = requests.post(f"{SERVER_URL}{self.endpoint}", json=self.payload)
            if response.status_code != 200:
                self.error.emit(f"Error: {response.status_code} {response.text}")
            else:
                self.finished.emit(response.json())
        except Exception as e:
            self.error.emit(str(e))

class InventoryUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Table to display inventory
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Item Name", "Quantity"])
        self.layout.addWidget(self.table)
        
        # Controls to simulate purchase/return actions
        control_layout = QHBoxLayout()
        self.item_input = QLineEdit()
        self.item_input.setPlaceholderText("Item Name")
        control_layout.addWidget(self.item_input)
        
        self.purchase_button = QPushButton("Purchase")
        self.purchase_button.clicked.connect(self.purchase_item)
        control_layout.addWidget(self.purchase_button)
        
        self.return_button = QPushButton("Return")
        self.return_button.clicked.connect(self.return_item)
        control_layout.addWidget(self.return_button)
        
        self.layout.addLayout(control_layout)
        
        # Status label
        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)
        
        # Refresh inventory display initially
        self.refresh_inventory()
    def refresh_inventory(self):
        self.status_label.setText("Refreshing inventory...")
        self.fetch_thread = FetchInventoryThread()
        self.fetch_thread.finished.connect(self.update_table)
        self.fetch_thread.error.connect(self.show_error)
        self.fetch_thread.start()
    
    def update_table(self, items):
        self.table.setRowCount(0)
        for row_idx, (name, quantity) in enumerate(items):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(name))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(quantity)))
        self.status_label.setText("Inventory updated.")
    
    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)
        self.status_label.setText("Error occurred.")
    
    def purchase_item(self):
        # Purchase: decrement quantity by 1
        item_name = self.item_input.text().strip()
        if not item_name:
            QMessageBox.warning(self, "Input Error", "Please enter an item name.")
            return
        # First, get current quantity from the table
        current_quantity = None
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).text() == item_name:
                current_quantity = int(self.table.item(row, 1).text())
                break
        if current_quantity is None:
            QMessageBox.warning(self, "Item Not Found", "Item does not exist in inventory.")
            return
        new_quantity = max(0, current_quantity - 1)
        payload = {"name": item_name, "quantity": new_quantity}
        self.status_label.setText("Processing purchase...")
        self.update_thread = UpdateInventoryThread("/update-quantity", payload)
        self.update_thread.finished.connect(lambda res: self.on_update_success("Purchase", res))
        self.update_thread.error.connect(self.show_error)
        self.update_thread.start()
    
    def return_item(self):
        # Return: increment quantity by 1
        item_name = self.item_input.text().strip()
        if not item_name:
            QMessageBox.warning(self, "Input Error", "Please enter an item name.")
            return
        # First, get current quantity from the table (if exists)
        current_quantity = 0
        found = False
        for row in range(self.table.rowCount()):
             if self.table.item(row, 0).text() == item_name:
                current_quantity = int(self.table.item(row, 1).text())
                found = True
                break
        new_quantity = current_quantity + 1
        payload = {"name": item_name, "quantity": new_quantity}
        # If item does not exist, add it using /add-item
        if not found:
            endpoint = "/add-item"
        else:
            endpoint = "/update-quantity"
        self.status_label.setText("Processing return...")
        self.update_thread = UpdateInventoryThread(endpoint, payload)
        self.update_thread.finished.connect(lambda res: self.on_update_success("Return", res))
        self.update_thread.error.connect(self.show_error)
        self.update_thread.start()
    
    def on_update_success(self, action, response):
        self.status_label.setText(f"{action} processed successfully.")
        self.refresh_inventory()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryUI()
    window.show()
    sys.exit(app.exec_())




