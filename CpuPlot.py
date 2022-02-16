import threading
import pyqtgraph as pg
import psutil
from collections import deque
from PySide6.QtCore import Signal, Slot


class CpuGraph(pg.PlotWidget):
    new_data = Signal(float)

    def __init__(self, parent=None):
        super(CpuGraph, self).__init__(parent=parent)
        self.cpu_use = deque(maxlen=100)
        self.closing = False
        self.curve = self.plot(self.cpu_use, clear=True)
        self.setLabel('left', "CPU usage", units='%')
        self.curve.setPen(pg.mkPen(color='y', width=3))
        self.setXRange(0, 100, padding=0.0)
        self.setYRange(0, 100)
        self.new_data.connect(self.add_data)

    @Slot(float)
    def add_data(self, value):
        self.cpu_use.append(value)
        self.curve.setData(self.cpu_use)

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
    cpu_gr.run()
    cpu_gr.show()
    app.exec()
    cpu_gr.close()



