import matplotlib.pyplot as plt 
from matplotlib import *
import numpy as np
from PyQt5.QtWidgets import *
import matplotlib.backends.backend_qt5agg as bkend
#from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas)
#from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

class MPLplot(QWidget):
    def __init__(self):
        super(MPLplot, self).__init__()
        self.figure = plt.Figure()
        self.canvas = bkend.FigureCanvasQTAgg(self.figure)
        self.toolbar = bkend.NavigationToolbar2QT(self.canvas, self)
        self.ax = self.figure.add_subplot(111)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
