"""
============================================================
  Real-Time Process Monitoring Dashboard
  CSE 316 - Operating Systems | Academic Task-2 (CA2)
  Author: LPU Student Project
  Description: A professional, cross-platform Task Manager
               built with Python and PySide6, compatible
               with both Windows and Ubuntu/Linux.
============================================================
"""

import sys
import os
import signal
import platform
import time
import math
from datetime import datetime
from collections import deque
from datetime import datetime, UTC
import shutil
import subprocess
# ── Third-party imports ────────────────────────────────────
import psutil
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QLabel, QPushButton, QLineEdit, QComboBox, QGroupBox,
    QSplitter, QFrame, QMessageBox, QProgressBar, QScrollArea,
    QSizePolicy, QMenu, QAbstractItemView, QToolBar, QStatusBar,
    QDialog, QDialogButtonBox, QSpinBox, QCheckBox, QTextEdit,
    QGridLayout, QSlider
)
from PySide6.QtCore import (
    Qt, QTimer, QThread, Signal, QObject, QSize, QRect, QPoint
)
from PySide6.QtGui import (
    QColor, QPainter, QPen, QBrush, QFont, QFontMetrics,
    QPalette, QLinearGradient, QAction, QIcon, QPixmap,
    QKeySequence, QCursor, QPainterPath, QRadialGradient,
    QPolygonF
)

# ─────────────────────────────────────────────────────────────
#  CONSTANTS & THEME
# ─────────────────────────────────────────────────────────────

APP_NAME    = "System Monitor"
APP_VERSION = "1.0.0"
IS_WINDOWS  = platform.system() == "Windows"
IS_LINUX    = platform.system() == "Linux"

# Dark-mode color palette
DARK_BG       = "#0d1117"   # window background
PANEL_BG      = "#161b22"   # card / panel background
BORDER_COL    = "#30363d"   # border lines
ACCENT_BLUE   = "#1f6feb"   # primary accent
ACCENT_GREEN  = "#3fb950"   # healthy / low usage
ACCENT_YELLOW = "#d29922"   # warning
ACCENT_RED    = "#f85149"   # critical / danger
ACCENT_PURPLE = "#8957e5"   # secondary accent
TEXT_PRIMARY  = "#e6edf3"   # main text
TEXT_MUTED    = "#7d8590"   # secondary / dim text
TEXT_HEADING  = "#ffffff"   # headings
HOVER_BG      = "#1c2128"   # row hover
SELECT_BG     = "#1f2d3d"   # selected row

STYLESHEET = f"""
/* ── Global ───────────────────────────────── */
QMainWindow, QWidget {{
    background-color: {DARK_BG};
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', 'Ubuntu', sans-serif;
    font-size: 13px;
}}

/* ── Tab Widget ────────────────────────────── */
QTabWidget::pane {{
    border: 1px solid {BORDER_COL};
    background-color: {PANEL_BG};
    border-radius: 6px;
}}
QTabBar::tab {{
    background-color: {DARK_BG};
    color: {TEXT_MUTED};
    padding: 10px 22px;
    border: 1px solid transparent;
    border-bottom: none;
    font-size: 13px;
    font-weight: 500;
    margin-right: 2px;
}}
QTabBar::tab:selected {{
    background-color: {PANEL_BG};
    color: {TEXT_HEADING};
    border-color: {BORDER_COL};
    border-bottom-color: {PANEL_BG};
}}
QTabBar::tab:hover:!selected {{
    background-color: {HOVER_BG};
    color: {TEXT_PRIMARY};
}}

/* ── Table ─────────────────────────────────── */
QTableWidget {{
    background-color: {DARK_BG};
    alternate-background-color: {PANEL_BG};
    color: {TEXT_PRIMARY};
    gridline-color: {BORDER_COL};
    border: none;
    selection-background-color: {SELECT_BG};
    selection-color: {TEXT_HEADING};
    font-size: 12px;
}}
QTableWidget::item {{
    padding: 6px 8px;
    border-bottom: 1px solid {BORDER_COL};
}}
QTableWidget::item:hover {{
    background-color: {HOVER_BG};
}}
QHeaderView::section {{
    background-color: {PANEL_BG};
    color: {TEXT_MUTED};
    padding: 8px;
    border: none;
    border-bottom: 2px solid {BORDER_COL};
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
QHeaderView::section:hover {{
    background-color: {HOVER_BG};
    color: {TEXT_PRIMARY};
}}

/* ── Buttons ───────────────────────────────── */
QPushButton {{
    background-color: {PANEL_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COL};
    border-radius: 5px;
    padding: 7px 16px;
    font-size: 13px;
    font-weight: 500;
}}
QPushButton:hover {{
    background-color: {HOVER_BG};
    border-color: {ACCENT_BLUE};
    color: {TEXT_HEADING};
}}
QPushButton:pressed {{
    background-color: {ACCENT_BLUE};
    color: white;
}}
QPushButton#dangerBtn {{
    background-color: #2d1a1a;
    border-color: {ACCENT_RED};
    color: {ACCENT_RED};
}}
QPushButton#dangerBtn:hover {{
    background-color: {ACCENT_RED};
    color: white;
}}
QPushButton#primaryBtn {{
    background-color: {ACCENT_BLUE};
    color: white;
    border-color: {ACCENT_BLUE};
}}
QPushButton#primaryBtn:hover {{
    background-color: #388bfd;
}}

/* ── Input / Search ─────────────────────────── */
QLineEdit {{
    background-color: {PANEL_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COL};
    border-radius: 5px;
    padding: 7px 10px;
    font-size: 13px;
}}
QLineEdit:focus {{
    border-color: {ACCENT_BLUE};
}}

/* ── ComboBox ───────────────────────────────── */
QComboBox {{
    background-color: {PANEL_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COL};
    border-radius: 5px;
    padding: 6px 10px;
    min-width: 120px;
}}
QComboBox:hover {{ border-color: {ACCENT_BLUE}; }}
QComboBox QAbstractItemView {{
    background-color: {PANEL_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COL};
    selection-background-color: {SELECT_BG};
}}

/* ── GroupBox ───────────────────────────────── */
QGroupBox {{
    border: 1px solid {BORDER_COL};
    border-radius: 6px;
    margin-top: 14px;
    padding-top: 6px;
    color: {TEXT_MUTED};
    font-weight: 600;
    font-size: 11px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    left: 10px;
}}

/* ── ProgressBar ─────────────────────────────── */
QProgressBar {{
    border: none;
    border-radius: 3px;
    background-color: #21262d;
    height: 6px;
    text-align: center;
    color: transparent;
}}
QProgressBar::chunk {{
    border-radius: 3px;
    background-color: {ACCENT_BLUE};
}}

/* ── ScrollBar ───────────────────────────────── */
QScrollBar:vertical {{
    background: {DARK_BG};
    width: 8px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {BORDER_COL};
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {TEXT_MUTED};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}

/* ── StatusBar ───────────────────────────────── */
QStatusBar {{
    background-color: {PANEL_BG};
    color: {TEXT_MUTED};
    border-top: 1px solid {BORDER_COL};
    font-size: 12px;
    padding: 2px 8px;
}}

/* ── ToolBar ─────────────────────────────────── */
QToolBar {{
    background-color: {PANEL_BG};
    border-bottom: 1px solid {BORDER_COL};
    spacing: 6px;
    padding: 4px 8px;
}}

/* ── Context Menu ────────────────────────────── */
QMenu {{
    background-color: {PANEL_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COL};
    border-radius: 6px;
    padding: 4px;
}}
QMenu::item {{
    padding: 8px 20px;
    border-radius: 4px;
}}
QMenu::item:selected {{
    background-color: {SELECT_BG};
    color: {TEXT_HEADING};
}}
QMenu::separator {{
    height: 1px;
    background-color: {BORDER_COL};
    margin: 4px 8px;
}}

/* ── Splitter ────────────────────────────────── */
QSplitter::handle {{
    background-color: {BORDER_COL};
    width: 1px;
    height: 1px;
}}

/* ── Label ───────────────────────────────────── */
QLabel {{ color: {TEXT_PRIMARY}; }}
QLabel#heading {{ color: {TEXT_HEADING}; font-size: 18px; font-weight: 700; }}
QLabel#subheading {{ color: {TEXT_MUTED}; font-size: 12px; }}
QLabel#value {{ color: {TEXT_HEADING}; font-size: 22px; font-weight: 700; }}
QLabel#metric {{ color: {TEXT_MUTED}; font-size: 11px; font-weight: 600; text-transform: uppercase; }}
"""


# ─────────────────────────────────────────────────────────────
#  HELPER: bytes → human-readable
# ─────────────────────────────────────────────────────────────

def human_bytes(n: int) -> str:
    """Convert bytes to a readable string (KB, MB, GB)."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < 1024.0:
            return f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} PB"


def cpu_color(pct: float) -> str:
    if pct < 50:   return ACCENT_GREEN
    if pct < 80:   return ACCENT_YELLOW
    return ACCENT_RED


def mem_color(pct: float) -> str:
    if pct < 60:   return ACCENT_BLUE
    if pct < 85:   return ACCENT_YELLOW
    return ACCENT_RED


# ─────────────────────────────────────────────────────────────
#  CUSTOM WIDGET: Mini Line Chart (sparkline)
# ─────────────────────────────────────────────────────────────

class SparklineChart(QWidget):
    """A lightweight animated sparkline that draws the last N data points."""

    def __init__(self, color: str = ACCENT_BLUE, max_points: int = 60, parent=None):
        super().__init__(parent)
        self.color = QColor(color)
        self.data: deque = deque([0.0] * max_points, maxlen=max_points)
        self.setMinimumHeight(80)
        self.setMinimumWidth(200)

    def push(self, value: float):
        self.data.append(max(0.0, min(100.0, value)))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        # Background
        painter.fillRect(self.rect(), QColor(DARK_BG))

        pts = list(self.data)
        n   = len(pts)
        if n < 2:
            return

        pad_x, pad_y = 8, 8
        chart_w = w - 2 * pad_x
        chart_h = h - 2 * pad_y

        step_x = chart_w / (n - 1)

        # Build path
        path = QPainterPath()
        fill = QPainterPath()
        for i, val in enumerate(pts):
            x = pad_x + i * step_x
            y = pad_y + chart_h - (val / 100.0) * chart_h
            if i == 0:
                path.moveTo(x, y)
                fill.moveTo(x, h - pad_y)
                fill.lineTo(x, y)
            else:
                path.lineTo(x, y)
                fill.lineTo(x, y)

        # Close fill path
        fill.lineTo(pad_x + (n - 1) * step_x, h - pad_y)
        fill.closeSubpath()

        # Draw gradient fill
        grad = QLinearGradient(0, 0, 0, h)
        c_top = QColor(self.color)
        c_top.setAlpha(80)
        c_bot = QColor(self.color)
        c_bot.setAlpha(5)
        grad.setColorAt(0, c_top)
        grad.setColorAt(1, c_bot)
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.NoPen)
        painter.drawPath(fill)

        # Draw line
        pen = QPen(self.color, 2)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

        # Current value text
        cur = pts[-1]
        painter.setPen(QColor(self.color))
        font = QFont("Segoe UI", 9, QFont.Bold)
        painter.setFont(font)
        painter.drawText(w - 46, 18, f"{cur:.1f}%")

        painter.end()


# ─────────────────────────────────────────────────────────────
#  CUSTOM WIDGET: Circular Gauge
# ─────────────────────────────────────────────────────────────

class CircularGauge(QWidget):
    """Animated circular progress gauge."""

    def __init__(self, label: str = "", color: str = ACCENT_BLUE, parent=None):
        super().__init__(parent)
        self.label  = label
        self.color  = color
        self._value = 0.0
        self.setFixedSize(130, 130)

    def set_value(self, v: float):
        self._value = max(0.0, min(100.0, v))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        r = min(w, h) // 2 - 12

        # Background arc
        bg_pen = QPen(QColor(BORDER_COL), 10, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(cx - r, cy - r, 2 * r, 2 * r, 225 * 16, -270 * 16)

        # Foreground arc
        angle_span = int(-270 * (self._value / 100.0) * 16)
        col = QColor(cpu_color(self._value) if "CPU" in self.label else mem_color(self._value))
        fg_pen = QPen(col, 10, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(fg_pen)
        painter.drawArc(cx - r, cy - r, 2 * r, 2 * r, 225 * 16, angle_span)

        # Center text – value
        painter.setPen(QColor(TEXT_HEADING))
        val_font = QFont("Segoe UI", 16, QFont.Bold)
        painter.setFont(val_font)
        val_str = f"{self._value:.0f}%"
        fm = QFontMetrics(val_font)
        painter.drawText(cx - fm.horizontalAdvance(val_str) // 2, cy + fm.ascent() // 2 - 8, val_str)

        # Label below
        painter.setPen(QColor(TEXT_MUTED))
        lbl_font = QFont("Segoe UI", 9)
        painter.setFont(lbl_font)
        lbl_fm = QFontMetrics(lbl_font)
        painter.drawText(cx - lbl_fm.horizontalAdvance(self.label) // 2, cy + 20, self.label)

        painter.end()


# ─────────────────────────────────────────────────────────────
#  CUSTOM WIDGET: Resource Card
# ─────────────────────────────────────────────────────────────

class ResourceCard(QFrame):
    """Card that shows a gauge + sparkline + stats for one resource."""

    def __init__(self, title: str, color: str, parent=None):
        super().__init__(parent)
        self.setObjectName("ResourceCard")
        self.setStyleSheet(f"""
            QFrame#ResourceCard {{
                background-color: {PANEL_BG};
                border: 1px solid {BORDER_COL};
                border-radius: 8px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        # Title
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px; font-weight: 600; letter-spacing: 1px;")
        layout.addWidget(title_lbl)

        # Gauge + stats row
        row = QHBoxLayout()
        row.setSpacing(16)
        self.gauge = CircularGauge(title, color)
        row.addWidget(self.gauge)

        stats_col = QVBoxLayout()
        stats_col.setSpacing(4)
        self.stat_labels: dict[str, QLabel] = {}
        for key in ("Usage", "Available", "Total"):
            k_lbl = QLabel(key)
            k_lbl.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px;")
            v_lbl = QLabel("—")
            v_lbl.setStyleSheet(f"color: {TEXT_HEADING}; font-size: 13px; font-weight: 600;")
            self.stat_labels[key] = v_lbl
            pair = QHBoxLayout()
            pair.addWidget(k_lbl)
            pair.addStretch()
            pair.addWidget(v_lbl)
            stats_col.addLayout(pair)

        stats_col.addStretch()
        row.addLayout(stats_col)
        layout.addLayout(row)

        # Sparkline
        self.sparkline = SparklineChart(color)
        layout.addWidget(self.sparkline)

    def update_data(self, pct: float, available: str, total: str):
        self.gauge.set_value(pct)
        self.sparkline.push(pct)
        self.stat_labels["Usage"].setText(f"{pct:.1f}%")
        self.stat_labels["Available"].setText(available)
        self.stat_labels["Total"].setText(total)


# ─────────────────────────────────────────────────────────────
#  BACKGROUND DATA COLLECTOR THREAD
# ─────────────────────────────────────────────────────────────

class SystemDataCollector(QObject):
    """Runs in a background QThread; emits signals with fresh data."""

    system_data_ready = Signal(dict)
    process_data_ready = Signal(list)

    def __init__(self, interval_ms: int = 1000):
        super().__init__()
        self.interval_ms = interval_ms
        self._running    = False
        self._timer      = None

    def start_collection(self):
        self._running = True
        self._timer   = QTimer()
        self._timer.setInterval(self.interval_ms)
        self._timer.timeout.connect(self._collect)
        self._timer.start()

    def stop_collection(self):
        self._running = False
        if self._timer:
            self._timer.stop()
            self._timer.deleteLater()
            self._timer = None
    
    def _collect(self):
        if not self._running:
            return
        # ── System-level stats ──────────────────────────
        cpu_pct  = psutil.cpu_percent(interval=None)
        cpu_freq = psutil.cpu_freq()
        cpu_per  = psutil.cpu_percent(percpu=True, interval=None)
        mem      = psutil.virtual_memory()
        swap     = psutil.swap_memory()
        disk     = psutil.disk_usage("/")
        net      = psutil.net_io_counters()
        boot_ts  = psutil.boot_time()
        uptime_s = time.time() - boot_ts
        uptime   = str(datetime.fromtimestamp(uptime_s, UTC).strftime("%Hh %Mm %Ss"))

        sys_data = {
            "cpu_pct":    cpu_pct,
            "cpu_freq":   cpu_freq,
            "cpu_per":    cpu_per,
            "cpu_count":  psutil.cpu_count(logical=True),
            "cpu_phys":   psutil.cpu_count(logical=False),
            "mem":        mem,
            "swap":       swap,
            "disk":       disk,
            "net":        net,
            "uptime":     uptime,
            "timestamp":  datetime.now().strftime("%H:%M:%S"),
        }
        self.system_data_ready.emit(sys_data)

        # ── Process list ────────────────────────────────
        procs = []
        for proc in psutil.process_iter([
            "pid", "name", "username", "status",
            "cpu_percent", "memory_info", "memory_percent",
            "num_threads", "create_time", "nice"
        ]):
            try:
                info = proc.info
                procs.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        self.process_data_ready.emit(procs)


# ─────────────────────────────────────────────────────────────
#  PROCESS TABLE TAB
# ─────────────────────────────────────────────────────────────

PROC_COLUMNS = [
    ("PID",      60,  Qt.AlignRight),
    ("Name",     200, Qt.AlignLeft),
    ("User",     120, Qt.AlignLeft),
    ("Status",   90,  Qt.AlignCenter),
    ("CPU %",    80,  Qt.AlignRight),
    ("Memory",   100, Qt.AlignRight),
    ("Mem %",    70,  Qt.AlignRight),
    ("Threads",  70,  Qt.AlignRight),
    ("PID (nice)", 80, Qt.AlignRight),
]


class ProcessTab(QWidget):
    """Full-featured process list with search, sort, kill, and signals."""

    kill_requested     = Signal(int, str)   # pid, name
    signal_requested   = Signal(int, int)   # pid, signal

    def __init__(self, parent=None):
        super().__init__(parent)
        self._all_procs: list = []
        self._filter_text: str = ""
        self._sort_col:  int = 4      # CPU % by default
        self._sort_desc: bool = True

        self._build_ui()

    # ── UI Construction ──────────────────────────────────────

    def _build_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        # ── Toolbar / filter row ────────────────────────
        toolbar = QFrame()
        toolbar.setStyleSheet(f"background-color: {PANEL_BG}; border-bottom: 1px solid {BORDER_COL};")
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(12, 8, 12, 8)
        tb_layout.setSpacing(8)

        search_icon = QLabel("🔍")
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search by name or PID…")
        self.search_box.setFixedWidth(260)
        self.search_box.textChanged.connect(self._on_search)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Processes", "Running", "Sleeping", "Stopped", "Zombie"])
        self.filter_combo.currentTextChanged.connect(self._on_search)

        self.proc_count_lbl = QLabel("0 processes")
        self.proc_count_lbl.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 12px;")

        self.refresh_btn  = QPushButton("⟳  Refresh")
        self.refresh_btn.setObjectName("primaryBtn")

        self.end_task_btn = QPushButton("✕  End Task")
        self.end_task_btn.setObjectName("dangerBtn")
        self.end_task_btn.setEnabled(False)
        self.end_task_btn.clicked.connect(self._on_end_task)

        tb_layout.addWidget(search_icon)
        tb_layout.addWidget(self.search_box)
        tb_layout.addWidget(self.filter_combo)
        tb_layout.addStretch()
        tb_layout.addWidget(self.proc_count_lbl)
        tb_layout.addWidget(self.refresh_btn)
        tb_layout.addWidget(self.end_task_btn)
        main.addWidget(toolbar)

        # ── Process table ───────────────────────────────
        self.table = QTableWidget(0, len(PROC_COLUMNS))
        self.table.setHorizontalHeaderLabels([c[0] for c in PROC_COLUMNS])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSortingEnabled(False)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.horizontalHeader().sectionClicked.connect(self._on_header_clicked)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setFocusPolicy(Qt.StrongFocus)

        for i, (_, width, _) in enumerate(PROC_COLUMNS):
            self.table.setColumnWidth(i, width)

        self.table.horizontalHeader().setStretchLastSection(True)
        main.addWidget(self.table)

    # ── Data update ──────────────────────────────────────────

    def update_processes(self, procs: list):
        self._all_procs = procs
        self._render_table()

    def _render_table(self):
        text = self._filter_text.lower()
        status_filter = self.filter_combo.currentText()

        # Filter
        filtered = []
        for p in self._all_procs:
            name = (p.get("name") or "").lower()
            pid  = str(p.get("pid") or "")
            st   = (p.get("status") or "").lower()

            if text and text not in name and text not in pid:
                continue
            if status_filter != "All Processes":
                if status_filter.lower() not in st:
                    continue
            filtered.append(p)

        # Sort
        col_map = {0: "pid", 1: "name", 2: "username", 3: "status",
                   4: "cpu_percent", 5: None, 6: "memory_percent",
                   7: "num_threads", 8: "nice"}
        sort_key = col_map.get(self._sort_col, "cpu_percent")

        def sort_fn(p):
            if sort_key is None:
                mi = p.get("memory_info")
                return mi.rss if mi else 0
            v = p.get(sort_key) or 0
            return v if isinstance(v, (int, float)) else str(v).lower()

        filtered.sort(key=sort_fn, reverse=self._sort_desc)

        # Render
        self.table.setUpdatesEnabled(False)
        self.table.setRowCount(len(filtered))

        for row, p in enumerate(filtered):
            self.table.setRowHeight(row, 28)
            pid   = p.get("pid") or 0
            name  = p.get("name") or ""
            user  = p.get("username") or ""
            status = p.get("status") or ""
            cpu_raw   = p.get("cpu_percent") or 0.0
            cpu = cpu_raw / psutil.cpu_count()
            mi    = p.get("memory_info")
            mem_b = mi.rss if mi else 0
            mem_p = p.get("memory_percent") or 0.0
            thrs  = p.get("num_threads") or 0
            nice  = p.get("nice") or 0

            values = [
                (str(pid),                          Qt.AlignRight | Qt.AlignVCenter),
                (name,                              Qt.AlignLeft  | Qt.AlignVCenter),
                (user.split("\\")[-1] if user else "", Qt.AlignLeft | Qt.AlignVCenter),
                (status,                            Qt.AlignCenter | Qt.AlignVCenter),
                (f"{cpu:.1f}",                      Qt.AlignRight | Qt.AlignVCenter),
                (human_bytes(mem_b),                Qt.AlignRight | Qt.AlignVCenter),
                (f"{mem_p:.1f}",                    Qt.AlignRight | Qt.AlignVCenter),
                (str(thrs),                         Qt.AlignRight | Qt.AlignVCenter),
                (str(nice),                         Qt.AlignRight | Qt.AlignVCenter),
            ]

            for col, (text_val, align) in enumerate(values):
                item = QTableWidgetItem(text_val)
                item.setTextAlignment(align)
                item.setData(Qt.UserRole, pid)

                # Color-code CPU column
                if col == 4:
                    c = QColor(cpu_color(cpu))
                    if cpu > 5:
                        item.setForeground(c)
                elif col == 6:
                    c = QColor(mem_color(mem_p))
                    if mem_p > 2:
                        item.setForeground(c)
                elif col == 3:
                    col_map_s = {
                        "running":  ACCENT_GREEN,
                        "sleeping": TEXT_MUTED,
                        "stopped":  ACCENT_YELLOW,
                        "zombie":   ACCENT_RED,
                    }
                    item.setForeground(QColor(col_map_s.get(status, TEXT_PRIMARY)))

                self.table.setItem(row, col, item)

        self.table.setUpdatesEnabled(True)
        self.proc_count_lbl.setText(f"{len(filtered)} processes")

    # ── Slots ────────────────────────────────────────────────

    def _on_search(self):
        self._filter_text = self.search_box.text()
        self._render_table()

    def _on_header_clicked(self, col: int):
        if self._sort_col == col:
            self._sort_desc = not self._sort_desc
        else:
            self._sort_col  = col
            self._sort_desc = True
        self._render_table()

    def _on_selection_changed(self):
        has_sel = bool(self.table.selectedItems())
        self.end_task_btn.setEnabled(has_sel)

    def _get_selected_pid(self) -> tuple[int, str] | None:
        rows = self.table.selectedItems()
        if not rows:
            return None
        row = self.table.currentRow()
        pid  = int(self.table.item(row, 0).text())
        name = self.table.item(row, 1).text()
        return pid, name

    def _on_end_task(self):
        sel = self._get_selected_pid()
        if sel:
            self.kill_requested.emit(sel[0], sel[1])

    def _show_context_menu(self, pos):
        sel = self._get_selected_pid()
        if not sel:
            return
        pid, name = sel

        menu = QMenu(self)
        menu.addAction(f"  PID {pid}  —  {name}").setEnabled(False)
        menu.addSeparator()

        kill_act = menu.addAction("✕  Kill Process  (SIGKILL)")
        term_act = menu.addAction("⚠  Terminate  (SIGTERM)")
        menu.addSeparator()
        stop_act = menu.addAction("⏸  Suspend  (SIGSTOP)")
        cont_act = menu.addAction("▶  Resume  (SIGCONT)")

        if not IS_WINDOWS:
            menu.addSeparator()
            hup_act  = menu.addAction("↺  Reload  (SIGHUP)")
        else:
            hup_act = None

        action = menu.exec(self.table.viewport().mapToGlobal(pos))

        if action == kill_act:
            self._do_kill(pid, name, signal.SIGKILL)
        elif action == term_act:
            self._do_kill(pid, name, signal.SIGTERM)
        elif action == stop_act and not IS_WINDOWS:
            self._send_signal(pid, signal.SIGSTOP)
        elif action == cont_act and not IS_WINDOWS:
            self._send_signal(pid, signal.SIGCONT)
        elif hup_act and action == hup_act:
            self._send_signal(pid, signal.SIGHUP)

    def _do_kill(self, pid: int, name: str, sig):
        """Kill process with confirmation dialog."""
        msg = QMessageBox(self)
        msg.setWindowTitle("Confirm Kill")
        msg.setIcon(QMessageBox.Warning)
        msg.setText(f"<b>Kill process?</b><br><br>"
                    f"PID: <b>{pid}</b><br>Name: <b>{name}</b><br><br>"
                    "This action cannot be undone.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setStyleSheet(STYLESHEET)
        if msg.exec() == QMessageBox.Yes:
            self._send_signal(pid, sig)



    def _send_signal(self, pid: int, sig):
        try:
            proc = psutil.Process(pid)

            if IS_WINDOWS:
                proc.kill()
                return

            # ✅ Try normal kill first
            try:
                proc.send_signal(sig)
                return
            except psutil.AccessDenied:
                pass

            # ✅ Map signal safely
            sig_num = int(sig)

            # ✅ Use full path for reliability
            pkexec_path = shutil.which("pkexec") or "/usr/bin/pkexec"

            cmd = [
                pkexec_path,
                "/bin/kill",
                f"-{sig_num}",
                str(pid)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                raise Exception(
                    result.stderr.strip() or result.stdout.strip() or "Unknown error"
                )

        except psutil.NoSuchProcess:
            QMessageBox.information(self, "Info", f"Process {pid} no longer exists.")

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to kill process {pid}\n\n{str(e)}"
            )


# ─────────────────────────────────────────────────────────────
#  PERFORMANCE TAB
# ─────────────────────────────────────────────────────────────

class PerformanceTab(QWidget):
    """Shows CPU, memory, disk, and network in real-time with charts."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        content = QWidget()
        scroll.setWidget(content)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        main = QVBoxLayout(content)
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(16)

        # ── Row 1: CPU + Memory gauges ──────────────────
        row1 = QHBoxLayout()
        row1.setSpacing(16)

        self.cpu_card = ResourceCard("CPU", ACCENT_BLUE)
        self.mem_card = ResourceCard("MEMORY", ACCENT_GREEN)
        row1.addWidget(self.cpu_card)
        row1.addWidget(self.mem_card)
        main.addLayout(row1)

        # ── Row 2: Per-core CPU bars ─────────────────────
        core_group = QGroupBox("Per-Core CPU Usage")
        core_group.setStyleSheet(f"""
            QGroupBox {{ background-color: {PANEL_BG}; border: 1px solid {BORDER_COL};
                         border-radius: 8px; margin-top: 14px; padding: 10px; }}
            QGroupBox::title {{ color: {TEXT_MUTED}; font-size: 11px; font-weight: 600;
                                subcontrol-origin: margin; left: 12px; padding: 0 6px; }}
        """)
        self.core_layout = QGridLayout(core_group)
        self.core_layout.setSpacing(8)
        self.core_bars:  list[QProgressBar] = []
        self.core_labels: list[QLabel]       = []
        main.addWidget(core_group)

        # ── Row 3: Disk + Network ────────────────────────
        row3 = QHBoxLayout()
        row3.setSpacing(16)

        # Disk stats card
        disk_card = QFrame()
        disk_card.setStyleSheet(f"background-color: {PANEL_BG}; border: 1px solid {BORDER_COL}; border-radius: 8px;")
        disk_lay = QVBoxLayout(disk_card)
        disk_lay.setContentsMargins(16, 12, 16, 12)
        disk_lbl = QLabel("DISK")
        disk_lbl.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px; font-weight: 600; letter-spacing: 1px;")
        disk_lay.addWidget(disk_lbl)
        self.disk_bar = QProgressBar()
        self.disk_bar.setTextVisible(False)
        self.disk_bar.setFixedHeight(8)
        disk_lay.addWidget(self.disk_bar)
        self.disk_stats: dict[str, QLabel] = {}
        for key in ("Total", "Used", "Free", "Usage %"):
            row = QHBoxLayout()
            k = QLabel(key); k.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 12px;")
            v = QLabel("—"); v.setStyleSheet(f"color: {TEXT_HEADING}; font-size: 12px; font-weight: 600;")
            self.disk_stats[key] = v
            row.addWidget(k); row.addStretch(); row.addWidget(v)
            disk_lay.addLayout(row)
        disk_lay.addStretch()
        row3.addWidget(disk_card)

        # Network card
        net_card = QFrame()
        net_card.setStyleSheet(f"background-color: {PANEL_BG}; border: 1px solid {BORDER_COL}; border-radius: 8px;")
        net_lay = QVBoxLayout(net_card)
        net_lay.setContentsMargins(16, 12, 16, 12)
        net_lbl = QLabel("NETWORK")
        net_lbl.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px; font-weight: 600; letter-spacing: 1px;")
        net_lay.addWidget(net_lbl)
        self.net_sparkline_up   = SparklineChart(ACCENT_GREEN, 60)
        self.net_sparkline_down = SparklineChart(ACCENT_BLUE, 60)
        net_lay.addWidget(QLabel("▲ Upload"))
        net_lay.addWidget(self.net_sparkline_up)
        net_lay.addWidget(QLabel("▼ Download"))
        net_lay.addWidget(self.net_sparkline_down)
        self.net_labels: dict[str, QLabel] = {}
        for key in ("Bytes Sent", "Bytes Recv", "Packets Sent", "Packets Recv"):
            row = QHBoxLayout()
            k = QLabel(key); k.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 12px;")
            v = QLabel("—"); v.setStyleSheet(f"color: {TEXT_HEADING}; font-size: 12px; font-weight: 600;")
            self.net_labels[key] = v
            row.addWidget(k); row.addStretch(); row.addWidget(v)
            net_lay.addLayout(row)
        net_lay.addStretch()
        row3.addWidget(net_card)
        main.addLayout(row3)

        # ── Row 4: Swap / System info ────────────────────
        row4 = QHBoxLayout()
        row4.setSpacing(16)

        swap_card = QFrame()
        swap_card.setStyleSheet(f"background-color: {PANEL_BG}; border: 1px solid {BORDER_COL}; border-radius: 8px;")
        swap_lay = QVBoxLayout(swap_card)
        swap_lay.setContentsMargins(16, 12, 16, 12)
        swap_lbl = QLabel("SWAP MEMORY")
        swap_lbl.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px; font-weight: 600; letter-spacing: 1px;")
        swap_lay.addWidget(swap_lbl)
        self.swap_bar = QProgressBar()
        self.swap_bar.setTextVisible(False)
        self.swap_bar.setFixedHeight(8)
        swap_lay.addWidget(self.swap_bar)
        self.swap_stats: dict[str, QLabel] = {}
        for key in ("Total", "Used", "Free", "Usage %"):
            row = QHBoxLayout()
            k = QLabel(key); k.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 12px;")
            v = QLabel("—"); v.setStyleSheet(f"color: {TEXT_HEADING}; font-size: 12px; font-weight: 600;")
            self.swap_stats[key] = v
            row.addWidget(k); row.addStretch(); row.addWidget(v)
            swap_lay.addLayout(row)
        swap_lay.addStretch()
        row4.addWidget(swap_card)

        sys_card = QFrame()
        sys_card.setStyleSheet(f"background-color: {PANEL_BG}; border: 1px solid {BORDER_COL}; border-radius: 8px;")
        sys_lay = QVBoxLayout(sys_card)
        sys_lay.setContentsMargins(16, 12, 16, 12)
        sys_lbl = QLabel("SYSTEM INFO")
        sys_lbl.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px; font-weight: 600; letter-spacing: 1px;")
        sys_lay.addWidget(sys_lbl)
        self.sys_labels: dict[str, QLabel] = {}
        for key in ("OS", "CPU Cores", "CPU Freq", "Uptime", "Last Update"):
            row = QHBoxLayout()
            k = QLabel(key); k.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 12px;")
            v = QLabel("—"); v.setStyleSheet(f"color: {TEXT_HEADING}; font-size: 12px; font-weight: 600;")
            self.sys_labels[key] = v
            row.addWidget(k); row.addStretch(); row.addWidget(v)
            sys_lay.addLayout(row)
        sys_lay.addStretch()
        row4.addWidget(sys_card)

        main.addLayout(row4)
        main.addStretch()

        # Net tracking
        self._prev_bytes_sent = 0
        self._prev_bytes_recv = 0

    def _ensure_core_bars(self, n: int):
        while len(self.core_bars) < n:
            idx  = len(self.core_bars)
            col  = idx % 8
            row  = idx // 8
            lbl  = QLabel(f"C{idx}")
            lbl.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px; min-width: 24px;")
            bar  = QProgressBar()
            bar.setTextVisible(False)
            bar.setFixedHeight(12)
            bar.setRange(0, 100)
            bar.setStyleSheet(f"""
                QProgressBar {{ background-color: #21262d; border-radius: 3px; }}
                QProgressBar::chunk {{ background-color: {ACCENT_BLUE}; border-radius: 3px; }}
            """)
            val  = QLabel("0%")
            val.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 10px; min-width: 30px;")
            self.core_layout.addWidget(lbl, row, col * 3)
            self.core_layout.addWidget(bar, row, col * 3 + 1)
            self.core_layout.addWidget(val, row, col * 3 + 2)
            self.core_bars.append(bar)
            self.core_labels.append(val)

    def update_data(self, data: dict):
        cpu_pct  = data["cpu_pct"]
        cpu_per  = data["cpu_per"]
        mem      = data["mem"]
        swap     = data["swap"]
        disk     = data["disk"]
        net      = data["net"]
        freq     = data["cpu_freq"]

        # CPU card
        self.cpu_card.update_data(
            cpu_pct,
            f"{100-cpu_pct:.1f}% idle",
            f"{data['cpu_count']} logical / {data['cpu_phys']} physical"
        )

        # Memory card
        self.mem_card.update_data(
            mem.percent,
            human_bytes(mem.available),
            human_bytes(mem.total)
        )

        # Per-core bars
        self._ensure_core_bars(len(cpu_per))
        for i, pct in enumerate(cpu_per):
            self.core_bars[i].setValue(int(pct))
            self.core_labels[i].setText(f"{pct:.0f}%")
            col = cpu_color(pct)
            self.core_bars[i].setStyleSheet(f"""
                QProgressBar {{ background-color: #21262d; border-radius: 3px; }}
                QProgressBar::chunk {{ background-color: {col}; border-radius: 3px; }}
            """)

        # Disk
        self.disk_bar.setValue(int(disk.percent))
        self.disk_stats["Total"].setText(human_bytes(disk.total))
        self.disk_stats["Used"].setText(human_bytes(disk.used))
        self.disk_stats["Free"].setText(human_bytes(disk.free))
        self.disk_stats["Usage %"].setText(f"{disk.percent:.1f}%")

        # Network
        sent = net.bytes_sent
        recv = net.bytes_recv
        delta_sent = max(0, sent - self._prev_bytes_sent)
        delta_recv = max(0, recv - self._prev_bytes_recv)
        self._prev_bytes_sent = sent
        self._prev_bytes_recv = recv
        max_val = max(delta_sent, delta_recv, 1)
        self.net_sparkline_up.push(min(100, delta_sent / max_val * 100))
        self.net_sparkline_down.push(min(100, delta_recv / max_val * 100))
        self.net_labels["Bytes Sent"].setText(human_bytes(sent))
        self.net_labels["Bytes Recv"].setText(human_bytes(recv))
        self.net_labels["Packets Sent"].setText(f"{net.packets_sent:,}")
        self.net_labels["Packets Recv"].setText(f"{net.packets_recv:,}")

        # Swap
        self.swap_bar.setValue(int(swap.percent))
        self.swap_stats["Total"].setText(human_bytes(swap.total))
        self.swap_stats["Used"].setText(human_bytes(swap.used))
        self.swap_stats["Free"].setText(human_bytes(swap.free))
        self.swap_stats["Usage %"].setText(f"{swap.percent:.1f}%")

        # System info
        freq_str = f"{freq.current:.0f} MHz" if freq else "N/A"
        self.sys_labels["OS"].setText(f"{platform.system()} {platform.release()}")
        self.sys_labels["CPU Cores"].setText(
            f"{data['cpu_phys']} Physical / {data['cpu_count']} Logical"
        )
        self.sys_labels["CPU Freq"].setText(freq_str)
        self.sys_labels["Uptime"].setText(data["uptime"])
        self.sys_labels["Last Update"].setText(data["timestamp"])


# ─────────────────────────────────────────────────────────────
#  USERS TAB
# ─────────────────────────────────────────────────────────────

class UsersTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 12, 12, 12)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Username", "Terminal", "Host", "Started"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)

        lay.addWidget(QLabel("Logged-in Users"))
        lay.addWidget(self.table)

    def refresh(self):
        users = psutil.users()
        self.table.setRowCount(len(users))
        for i, u in enumerate(users):
            started = datetime.fromtimestamp(u.started).strftime("%Y-%m-%d %H:%M")
            vals = [u.name, u.terminal or "—", u.host or "local", started]
            for j, v in enumerate(vals):
                item = QTableWidgetItem(v)
                item.setForeground(QColor(TEXT_PRIMARY))
                self.table.setItem(i, j, item)
            self.table.setRowHeight(i, 28)


# ─────────────────────────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME}  —  Real-Time Process Monitor  (v{APP_VERSION})")
        self.setMinimumSize(1100, 700)
        self.resize(1280, 800)
        self.setStyleSheet(STYLESHEET)
        self._build_ui()
        self._setup_data_thread()
        self._setup_timers()

    # ── UI ───────────────────────────────────────────────────

    def _build_ui(self):
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
        header = QFrame()
        header.setFixedHeight(56)
        header.setStyleSheet(f"background-color: {PANEL_BG}; border-bottom: 1px solid {BORDER_COL};")
        hdr_lay = QHBoxLayout(header)
        hdr_lay.setContentsMargins(16, 0, 16, 0)

        # Logo / title
        logo = QLabel("🖥️")
        logo.setStyleSheet("font-size: 22px;")
        title_lbl = QLabel(APP_NAME)
        title_lbl.setStyleSheet(f"color: {TEXT_HEADING}; font-size: 16px; font-weight: 700; letter-spacing: 1px;")
        sub_lbl = QLabel("Real-Time Process Monitor")
        sub_lbl.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 12px; margin-left: 8px;")

        self.cpu_badge  = QLabel("CPU 0%")
        self.mem_badge  = QLabel("MEM 0%")
        for badge in (self.cpu_badge, self.mem_badge):
            badge.setStyleSheet(f"""
                background-color: {DARK_BG};
                color: {TEXT_MUTED};
                border: 1px solid {BORDER_COL};
                border-radius: 12px;
                padding: 3px 12px;
                font-size: 12px;
                font-weight: 600;
            """)

        self.clock_lbl = QLabel("00:00:00")
        self.clock_lbl.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 12px; font-family: monospace;")

        hdr_lay.addWidget(logo)
        hdr_lay.addWidget(title_lbl)
        hdr_lay.addWidget(sub_lbl)
        hdr_lay.addStretch()
        hdr_lay.addWidget(self.cpu_badge)
        hdr_lay.addWidget(self.mem_badge)
        hdr_lay.addWidget(self.clock_lbl)
        root.addWidget(header)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        root.addWidget(self.tabs)

        self.perf_tab    = PerformanceTab()
        self.proc_tab    = ProcessTab()
        self.users_tab   = UsersTab()

        self.tabs.addTab(self.perf_tab,  "  📊  Performance  ")
        self.tabs.addTab(self.proc_tab,  "  🔧  Processes  ")
        self.tabs.addTab(self.users_tab, "  👤  Users  ")

        # Wire kill signals
        self.proc_tab.kill_requested.connect(self._on_kill)

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self._os_lbl    = QLabel(f"  {platform.system()} {platform.release()}  ")
        self._pid_lbl   = QLabel(f"  App PID: {os.getpid()}  ")
        self._py_lbl    = QLabel(f"  Python {sys.version.split()[0]}  ")
        for lbl in (self._os_lbl, self._pid_lbl, self._py_lbl):
            lbl.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px;")
            self.status.addPermanentWidget(lbl)

        self.status.showMessage("Initializing monitoring…")

    # ── Background thread ────────────────────────────────────

    def _setup_data_thread(self):
        self._thread    = QThread()
        self._collector = SystemDataCollector(interval_ms=1500)
        self._collector.moveToThread(self._thread)

        self._thread.started.connect(self._collector.start_collection)
        self._collector.system_data_ready.connect(self._on_system_data)
        self._collector.process_data_ready.connect(self._on_process_data)

        self._thread.start()

    def _setup_timers(self):
        # Clock timer
        self._clock_timer = QTimer(self)
        self._clock_timer.setInterval(1000)
        self._clock_timer.timeout.connect(self._tick_clock)
        self._clock_timer.start()

        # Users tab refresh (every 10 s)
        self._users_timer = QTimer(self)
        self._users_timer.setInterval(10_000)
        self._users_timer.timeout.connect(self.users_tab.refresh)
        self._users_timer.start()
        self.users_tab.refresh()

    # ── Slots ────────────────────────────────────────────────

    def _tick_clock(self):
        self.clock_lbl.setText(datetime.now().strftime("%H:%M:%S"))

    def _on_system_data(self, data: dict):
        self.perf_tab.update_data(data)

        cpu = data["cpu_pct"]
        mem = data["mem"].percent

        # Update badges
        cpu_col = cpu_color(cpu)
        mem_col = mem_color(mem)
        self.cpu_badge.setText(f"CPU {cpu:.1f}%")
        self.mem_badge.setText(f"MEM {mem:.1f}%")
        self.cpu_badge.setStyleSheet(f"""
            background-color: {DARK_BG}; color: {cpu_col};
            border: 1px solid {cpu_col}; border-radius: 12px;
            padding: 3px 12px; font-size: 12px; font-weight: 600;
        """)
        self.mem_badge.setStyleSheet(f"""
            background-color: {DARK_BG}; color: {mem_col};
            border: 1px solid {mem_col}; border-radius: 12px;
            padding: 3px 12px; font-size: 12px; font-weight: 600;
        """)
        self.status.showMessage(
            f"  Updated: {data['timestamp']}  |  "
            f"CPU {cpu:.1f}%  |  MEM {mem:.1f}%  |  "
            f"Uptime: {data['uptime']}"
        )

    def _on_process_data(self, procs: list):
        self.proc_tab.update_processes(procs)

    def _on_kill(self, pid: int, name: str):
        """Slot for process kill request from the process tab."""
        self.proc_tab._do_kill(pid, name, signal.SIGKILL)

    # ── Cleanup ──────────────────────────────────────────────

    def closeEvent(self, event):
        self._collector.stop_collection()
        self._thread.quit()
        self._thread.wait(2000)
        event.accept()


# ─────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────

def main():
    # High-DPI support
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName("LPU-CSE316")

    # Set app-wide font
    font = QFont("Segoe UI" if IS_WINDOWS else "Ubuntu", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()