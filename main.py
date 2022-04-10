import sys

from PySide6.QtWidgets import QApplication, QTextEdit, QMainWindow, \
    QDockWidget, QHBoxLayout, QTreeView, QToolBar, QFileSystemModel, QFileDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt, QUrl, QDir
from PySide6.QtGui import QIcon, QAction
import CpuPlot


class DockDemo(QMainWindow):
    def __init__(self, parent=None):
        super(DockDemo, self).__init__(parent)
        self.setWindowIcon(QIcon('Eulitha_icon.ico'))
        self.setWindowTitle('Eulitha Phabler')
        central_widget = QTextEdit()
        layout = QHBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.create_docks(central_widget)
        self.create_menus()
        self.create_toolbar()
        self.statusBar().setStatusTip("Eulitha Phabler")

    def create_menus(self):
        open_action = QAction("&Open", self)
        open_action.setStatusTip("Open a polygon file")
        open_action.triggered.connect(self.click_open)

        bar = self.menuBar()
        file_menu = bar.addMenu('File')
        file_menu.addAction('New')
        file_menu.addAction(open_action)
        file_menu.addAction('Save')
        file_menu.addAction('Exit')

        win_menu = bar.addMenu('Windows')
        win_menu.addAction(self.graph_dock.toggleViewAction())
        win_menu.addAction(self.web_dock.toggleViewAction())
        win_menu.addAction(self.tree_dock.toggleViewAction())

    def create_docks(self, parent):
        self.graph_dock = QDockWidget('Plot CPU %', parent)
        self.graph_widget = CpuPlot.CpuGraph(self.graph_dock)
        self.graph_dock.setWidget(self.graph_widget)

        self.web_dock = QDockWidget('Company Homepage', parent)
        self.webView = QWebEngineView()
        self.webView.setUrl(QUrl('https://www.eulitha.com'))
        self.web_dock.setWidget(self.webView)

        self.tree_dock = QDockWidget('Phabler Machine', parent)
        self.tree_view = QTreeView()
        self.tree_dock.setWidget(self.tree_view)

        model = QFileSystemModel()
        model.setRootPath(QDir.currentPath())
        self.tree_view.setModel(model)
        self.tree_view.setRootIndex(model.index(QDir.currentPath()))
        self.tree_view.doubleClicked.connect(self.double_click_tree)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.tree_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.web_dock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.graph_dock)

    def create_toolbar(self):
        toolbar = QToolBar("Phabler Main Toolbar")
        self.addToolBar(toolbar)
        wec_action = QAction("WEC", self)
        wec_action.setStatusTip("Perform Wedge Error Correction")
        wec_action.triggered.connect(self.click_wec)
        toolbar.addAction(wec_action)

        exp_action = QAction("Exposure", self)
        exp_action.setStatusTip("DTL Exposure")
        exp_action.triggered.connect(self.click_exp)
        toolbar.addAction(exp_action)

    def click_wec(self):
        print("WEC")

    def click_exp(self):
        print("Exposure")

    def click_open(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", "c:/", "Images (*.png *.xpm *.jpg)")
        print("Open Document %s" % fileName[0])

    def double_click_tree(self, index):
        model = self.tree_view.model()
        abs_file_name = model.fileInfo(index).absoluteFilePath()
        print("Double Clicked %s" % abs_file_name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DockDemo()
    demo.show()
    demo.graph_widget.run()
    result = app.exec()
    demo.graph_widget.close()
    sys.exit(result)
