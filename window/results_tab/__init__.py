from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os, sys, logging 
import numpy as np 

class Results(QWidget):
    def __init__(self, parent):
        super(Results, self).__init__(parent)
        self.tabsTable = parent
        self.tabLayout = QHBoxLayout()

    def linear(x,m,b):
        return m*x + b
    
    def UVvis_vs_FluorescencePlot(self): 
