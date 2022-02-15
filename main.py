import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDockWidget, QHBoxLayout, QTextEdit
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon
import CpuPlot


class DockDemo(QMainWindow):
    def __init__(self, parent=None):
        super(DockDemo, self).__init__(parent)
        layout = QHBoxLayout()
        bar = self.menuBar()
        file = bar.addMenu('File')
        file.addAction('New')
        file.addAction('Save')
        file.addAction('Exit')

        self.graph_view = QDockWidget('CPU %', self)
        self.gr = CpuPlot.CpuGraph()
        self.graph_view.setWidget(self.gr.graph(self.graph_view))
        self.graph_view.setFloating(False)

        self.web_dock = QDockWidget('Search Page', self)
        self.webView = QWebEngineView()
        self.webView.setUrl(QUrl('https://www.python.org'))
        self.web_dock.setWidget(self.webView)
        self.web_dock.setFloating(False)

        self.setCentralWidget(QTextEdit())

        self.addDockWidget(Qt.RightDockWidgetArea, self.web_dock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.graph_view)

        self.setLayout(layout)
        self.setWindowIcon(QIcon('Eulitha_icon.ico'))
        self.setWindowTitle('Eulitha Phabler')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DockDemo()
    demo.show()
    demo.gr.run()
    result = app.exec()
    demo.gr.close()
    sys.exit(result)
