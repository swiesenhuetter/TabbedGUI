import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDockWidget, QHBoxLayout, QTextEdit, QToolBar
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon, QAction
import CpuPlot


class DockDemo(QMainWindow):
    def __init__(self, parent=None):
        super(DockDemo, self).__init__(parent)
        layout = QHBoxLayout()
        bar = self.menuBar()
        file_menu = bar.addMenu('File')
        file_menu.addAction('New')
        file_menu.addAction('Save')
        file_menu.addAction('Exit')

        self.graph_dock = QDockWidget('Plot CPU %', self)
        self.graph_widget = CpuPlot.CpuGraph(self.graph_dock)
        self.graph_dock.setWidget(self.graph_widget)
        self.graph_dock.setFloating(False)

        self.web_dock = QDockWidget('Search Page', self)
        self.webView = QWebEngineView()
        self.webView.setUrl(QUrl('https://www.python.org'))
        self.web_dock.setWidget(self.webView)
        self.web_dock.setFloating(False)

        self.setCentralWidget(QTextEdit())

        win_menu = bar.addMenu('Windows')
        win_menu.addAction(self.graph_dock.toggleViewAction())
        win_menu.addAction(self.web_dock.toggleViewAction())

        self.addDockWidget(Qt.RightDockWidgetArea, self.web_dock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.graph_dock)

        self.setLayout(layout)
        self.setWindowIcon(QIcon('Eulitha_icon.ico'))
        self.setWindowTitle('Eulitha Phabler')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DockDemo()
    demo.show()
    demo.graph_widget.run()
    result = app.exec()
    demo.graph_widget.close()
    sys.exit(result)
