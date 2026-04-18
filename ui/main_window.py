from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit
)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QColor

from core.system_monitor import get_cpu_usage, get_memory_usage, get_processes
from widgets.cpu_graph import LiveGraph


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Process Monitor")
        self.resize(1000, 600)

        self.init_ui()
        self.start_timer()

    def init_ui(self):
        central = QWidget()
        layout = QVBoxLayout()

        # Graphs
        graph_layout = QHBoxLayout()

        self.cpu_graph = LiveGraph("CPU Usage")
        self.mem_graph = LiveGraph("Memory Usage")

        graph_layout.addWidget(self.cpu_graph)
        graph_layout.addWidget(self.mem_graph)

        layout.addLayout(graph_layout)

        # Search bar
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search process...")
        layout.addWidget(self.search)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["PID", "Name", "CPU %", "Memory %", "Action"]
        )
        self.table.setSortingEnabled(True)

        layout.addWidget(self.table)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(2000)

    def update_ui(self):
        cpu = get_cpu_usage()
        mem = get_memory_usage()

        self.cpu_graph.update_graph(cpu)
        self.mem_graph.update_graph(mem)

        self.update_table()

    def update_table(self):
        processes = get_processes()

        search_text = self.search.text().lower()

        # Filter first
        processes = [
            p for p in processes
            if search_text in (p['name'] or "").lower()
        ]

        # Sort
        processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)

        # Limit
        processes = processes[:20]

        self.table.setRowCount(len(processes))

        for row, p in enumerate(processes):
            self.table.setItem(row, 0, QTableWidgetItem(str(p['pid'])))
            self.table.setItem(row, 1, QTableWidgetItem(p['name'] or ""))

            # CPU column with highlight
            cpu_item = QTableWidgetItem(str(p['cpu_percent']))
            if p['cpu_percent'] > 50:
                cpu_item.setBackground(QColor(255, 100, 100))
            self.table.setItem(row, 2, cpu_item)

            # Memory column
            self.table.setItem(row, 3, QTableWidgetItem(str(round(p['memory_percent'], 2))))

            # Kill button
            btn = QPushButton("Kill")
            btn.clicked.connect(lambda _, pid=p['pid']: self.kill_process(pid))
            self.table.setCellWidget(row, 4, btn)

    def kill_process(self, pid):
        import psutil
        try:
            psutil.Process(pid).terminate()
        except Exception as e:
            print("Error:", e)