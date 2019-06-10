from testPlots_tab import TestPlots 
from results_tab import Results 
import sys, os, sip
os.environ['QT_API'] = 'pyqt5'
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def absolute_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

class Window(QMainWindow): 
    def __init__(self):
        super(Window, self).__init__()
        self.init_ui()

    def init_ui(self):
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu("&File")
        exitAction = QAction('Exit', self)
        fileMenu.addAction(exitAction)
        self.setWindowTitle('QYCalculator')
        #icon = absolute_path('resources'+os.path.sep+'logo-icon.png')
        #QApplication.setWindowIcon(QIcon(icon))

        self.setGeometry(0,0,1370,749)
        windowFrame = self.frameGeometry()
        screenCenter = QDesktopWidget().availableGeometry().center()
        windowFrame.moveCenter(screenCenter)
        self.move(windowFrame.topLeft())

        self.table = TableWidget(self)
        self.setCentralWidget(self.table)
        self.show()

class TableWidget(QWidget):
    def __init__(self, parent):
        super(TableWidget, self).__init__(parent)
        self.parent = parent
        self.layout = QHBoxLayout(self)
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200) 
        self.tabs.addTab(self.tab1,"Test Plots")
        self.tabs.addTab(self.tab2,"Results")
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.tab1Layout = QHBoxLayout(self.tab1)
        self.tab2Layout = QHBoxLayout(self.tab2)
        self.testPlots = TestPlots(self)
        self.results = Results(self)
        self.tab1Layout.addWidget(self.testPlots)
        self.tab2Layout.addWidget(self.results)
