from PySide6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg


class LiveGraph(QWidget):
    def __init__(self, title="Graph"):
        super().__init__()

        self.data = []

        layout = QVBoxLayout()

        self.plot = pg.PlotWidget()
        self.plot.setTitle(title)
        self.plot.setYRange(0, 100)
        self.plot.showGrid(x=True, y=True)

        self.curve = self.plot.plot(pen=pg.mkPen(color='cyan', width=2))

        layout.addWidget(self.plot)
        self.setLayout(layout)

    def update_graph(self, value):
        self.data.append(value)
        self.data = self.data[-50:]
        self.curve.setData(self.data)