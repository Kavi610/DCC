# DCC Integration Project

DCC Assignment - Python Developer Task

### Project Structure:
1. **blender_plugin.py** - Blender plugin to manipulate and send object transforms.
2. **server.py** - Flask-based API server.
3. **database.py** - SQLite setup for inventory management.
4. **inventory_ui.py** - PyQt5-based UI to display inventory.
5. **README.txt** - Instructions to run the project.

### Setup and Execution:
1. Install required packages:
   ```bash
   pip install flask requests PyQt5
   ```
2. Setup the database:
   ```bash
   python database.py
   ```
3. Start the Flask server:
   ```bash
   python server.py
   ```
4. Install the Blender plugin:
   - Open Blender → Edit → Preferences → Add-ons.
   - Click Install, select `blender_plugin.py`, and enable the add-on.
5. Run the PyQt UI:
   ```bash
   python inventory_ui.py
   ```

### Notes:
- The server introduces a 10-second delay as per requirements.
- Logs all received requests in the terminal.
