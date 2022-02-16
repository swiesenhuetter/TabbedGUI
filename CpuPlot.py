import threading
import pyqtgraph as pg
import psutil
from collections import deque
from PySide6.QtCore import Signal, Slot, QObject


class CpuGraph(QObject):
    new_data = Signal(float)

    def __init__(self, parent=None):
        super(CpuGraph, self).__init__(parent=parent)
        self.cpu_use = deque(maxlen=100)
        self.graph_widget = pg.PlotWidget(parent)
        self.closing = False
        self.curve = self.graph_widget.plot(self.cpu_use, clear=True)
        self.curve.setPen(pg.mkPen(color='y', width=3))
        self.graph_widget.setXRange(0, 100)
        self.graph_widget.setYRange(0, 100)


    @Slot(float)
    def add_data(self, value):
        self.cpu_use.append(value)
        self.curve.setData(self.cpu_use)

    def graph(self, parent):
        self.new_data.connect(self.add_data)
        return self.graph_widget

    def run(self):
        cpu_usage = psutil.cpu_percent()
        self.new_data.emit(cpu_usage)
        if not self.closing:
            threading.Timer(0.1, self.run).start()

    def close(self):
        print("Closing")
        self.closing = True


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    app = QApplication([])
    cpu_gr = CpuGraph()
    window = cpu_gr.graph(None)
    cpu_gr.run()
    window.show()
    app.exec()
    cpu_gr.close()



