import sys
import os
sys.path.append(os.path.dirname(__file__))

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

app = QApplication(sys.argv)

# Dark theme
app.setStyleSheet("""
QMainWindow {
    background-color: #121212;
}
QTableWidget {
    background-color: #1e1e1e;
    color: white;
    gridline-color: #444;
}
QHeaderView::section {
    background-color: #2c2c2c;
    color: white;
    padding: 5px;
}
QPushButton {
    background-color: #ff4d4d;
    color: white;
    border-radius: 5px;
    padding: 5px;
}
QPushButton:hover {
    background-color: #ff1a1a;
}
QLineEdit {
    background-color: #1e1e1e;
    color: white;
    padding: 5px;
}
""")

window = MainWindow()
window.show()

sys.exit(app.exec())