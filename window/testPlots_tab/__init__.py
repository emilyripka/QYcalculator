from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
import numpy as np 
from matplotlib import *
from MPLplot import *

class TestPlots(QWidget):
    def __init__(self, parent):
        super(TestPlots, self).__init__(parent)
        self.table = parent
        self.tabLayout = QVBoxLayout()
        self.setLayout(self.tabLayout)
        self.hlayout = QHBoxLayout()
        self.tabLayout.addLayout(self.hlayout)
        self.colors = ["#ff0000","#ff3300","#ff6600","#ff9900","#ffcc00",
                        "#ffff00","#ccff33","#99ff33","#009900","#00cc00",
                        "#00cc66", "#00ffcc","#0099ff","#3333cc","#9933ff",
                        "#cc00cc","#cc3399","#cc0066","#cc0000"]
        self.iterColors = iter(self.colors)
        rcParams['font.family']= 'sans-serif'
        rcParams['font.size']= 18
########################################################################
# UV vis
        # upload data 
        #{{{
        prepareUVvis = QVBoxLayout() 
        width = 200
        self.hlayout.addLayout(prepareUVvis) 
        fileBox = QGroupBox("Import Data")
        fileBox.setMinimumWidth(width)
        dataLayout = QVBoxLayout()
        btnsLayout = QHBoxLayout()
        self.dataBtn = QPushButton("Upload files...")
        self.dataBtn.clicked.connect(self.browse)
        self.dataRemove = QPushButton("Remove selected")
        self.dataRemove.clicked.connect(self.remove)
        btnsLayout.addWidget(self.dataBtn)
        btnsLayout.addWidget(self.dataRemove)
        dataLayout.addLayout(btnsLayout)
        # show all uploaded files in list
        self.filesList = []
        self.dataList = QListWidget()
        self.dataList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        dataLayout.addWidget(self.dataList)
        fileBox.setLayout(dataLayout)
        prepareUVvis.addWidget(fileBox) # closes UVvisFileBox 
        # }}}
        # Plot
        # {{{
        self.UVvisLayout = QVBoxLayout()
        self.hlayout.addLayout(self.UVvisLayout)
        self.UVvisBox = QGroupBox("UV-vis Plot")
        self.vlayout = QVBoxLayout()
        UVvisForm = QFormLayout()
        UVvisPlotBoxBtnLayout = QHBoxLayout()
        UVvisComboLayout = QVBoxLayout()
        self.comboBox = QComboBox()
        self.comboFilesList = ['Choose file to plot...']
        self.comboBox.addItems(self.comboFilesList)
        UVvisComboLayout.addWidget(self.comboBox)
        self.vlayout.addLayout(UVvisComboLayout) # adds combo box to UVvisPlotBox layout
        self.expno = QLineEdit()
        self.expno.setFixedWidth(40)
        UVvisForm.addRow("Exp. #:", self.expno)
        self.vlayout.addLayout(UVvisForm) # adds form to UVvisPlotBox layout
        self.UVvisPlotBtn = QPushButton("Plot")
        self.UVvisPlotBtn.clicked.connect(self.UVvisPlot)
        UVvisPlotBoxBtnLayout.addWidget(self.UVvisPlotBtn)  
        self.UVvisClearBtn = QPushButton("Clear")
        self.UVvisClearBtn.clicked.connect(self.clearUVvisPlot)
        UVvisPlotBoxBtnLayout.addWidget(self.UVvisClearBtn)  
        self.vlayout.addLayout(UVvisPlotBoxBtnLayout)

        self.UVvisBox.setLayout(self.vlayout)
        self.UVvisLayout.addWidget(self.UVvisBox)
        self.UVvisFig = MPLplot()
        self.vlayout.addWidget(self.UVvisFig)
        # }}}
########################################################################
# Fluorescence
        # Plot 
        # {{{
        self.fluorescenceLayout = QVBoxLayout()
        self.hlayout.addLayout(self.fluorescenceLayout)
        self.fluorescenceBox = QGroupBox("Fluorescence Plot")
        self.vlayoutFluorescence = QVBoxLayout()

        fluorescenceForm = QFormLayout()
        fluorescencePlotBoxBtnLayout = QHBoxLayout()
        fluorescenceComboLayout = QVBoxLayout()
        self.fluorescenceComboBox = QComboBox()
        self.fluorescenceComboFilesList = ['Choose file to plot...']
        self.fluorescenceComboBox.addItems(self.fluorescenceComboFilesList)
        fluorescenceComboLayout.addWidget(self.fluorescenceComboBox)
        self.vlayoutFluorescence.addLayout(fluorescenceComboLayout) # adds combo box to UVvisPlotBox layout
        self.fluorescenceExpno = QLineEdit()
        self.fluorescenceExpno.setFixedWidth(40)
        fluorescenceForm.addRow("Exp. #:", self.fluorescenceExpno)
        self.vlayoutFluorescence.addLayout(fluorescenceForm) # adds form to UVvisPlotBox layout
        self.fluorescencePlotBtn = QPushButton("Plot")
        self.fluorescencePlotBtn.clicked.connect(self.fluorescencePlot)
        fluorescencePlotBoxBtnLayout.addWidget(self.fluorescencePlotBtn)  
        self.fluorescenceClearBtn = QPushButton("Clear")
        self.fluorescenceClearBtn.clicked.connect(self.clearFluorescencePlot)
        fluorescencePlotBoxBtnLayout.addWidget(self.fluorescenceClearBtn)  
        self.vlayoutFluorescence.addLayout(fluorescencePlotBoxBtnLayout)

        self.fluorescenceBox.setLayout(self.vlayoutFluorescence)
        self.fluorescenceLayout.addWidget(self.fluorescenceBox)
        self.fluorescenceFig = MPLplot()
        self.vlayoutFluorescence.addWidget(self.fluorescenceFig)
        # }}}
        self.folder_path = ''
########################################################################
    def browse(self):
        dialog = QFileDialog()
        self.workDir = QHBoxLayout()
        self.workDirName = QLineEdit()
        self.workDir.addWidget(self.workDirName)
        wd = self.workDirName.text()
        self.folder_path = dialog.getExistingDirectory(None, "Select Folder")
        self.workDirName.setText(self.folder_path + '/')
        paths = dialog.getOpenFileNames(self, "Upload files...", wd, "(*.csv)")[0]
        comboFilesList_temp = self.comboFilesList 
        fluorescenceComboFilesList_temp = self.fluorescenceComboFilesList 
        self.comboBox.clear()
        self.fluorescenceComboBox.clear()
        for path in paths:
            self.filesList.append(path)
            path = os.path.basename(path)
            self.dataList.addItem(path)
            comboFilesList_temp.append(path)
            fluorescenceComboFilesList_temp.append(path)
        self.comboBox.addItems(comboFilesList_temp)
        self.fluorescenceComboBox.addItems(fluorescenceComboFilesList_temp)

    def remove(self):
        for i in self.dataList.selectedItems():
            idx = self.dataList.row(i)
            self.dataList.takeItem(idx)
            del self.filesList[idx]
            combo_idx = idx+1
            self.comboBox.removeItem(combo_idx)

    def clearUVvisPlot(self):
        self.UVvisFig.canvas.figure.clear()
        self.UVvisFig.figure.add_subplot(111)
        self.UVvisFig.canvas.draw()
        self.iterColors = iter(self.colors)

    def clearFluorescencePlot(self):
        self.fluorescenceFig.canvas.figure.clear()
        self.fluorescenceFig.figure.add_subplot(111)
        self.fluorescenceFig.canvas.draw()
        self.iterColors = iter(self.colors)

    def UVvisPlot(self):
        self.workDirName.setText(self.folder_path + '/')
        fileName = self.folder_path + r'/' + self.comboBox.currentText() 
        rawData_1 = np.genfromtxt(str(fileName), delimiter=",")
        rawData_2 = np.delete(rawData_1, list(range(2, rawData_1.shape[1], 2)), axis=1)
        rawData_3 = np.transpose(rawData_2)
        expno = int(self.expno.text())
        xData = rawData_3[0,:]
        yData = rawData_3[expno,:]
        ax = self.UVvisFig.figure.add_subplot(111)
        ax.plot(xData, yData,color=next(self.iterColors))
        ax.set(yLabel=r'Absorption / a.u.',xlabel=r'Wavelength / nm')
        self.UVvisFig.canvas.figure.tight_layout()
        self.UVvisFig.canvas.draw()

    def fluorescencePlot(self):
        self.workDirName.setText(self.folder_path + '/')
        fileName = self.folder_path + r'/' + self.fluorescenceComboBox.currentText() 
        rawData_1 = np.genfromtxt(str(fileName), delimiter=",")
        rawData_2 = np.delete(rawData_1, list(range(2, rawData_1.shape[1], 2)), axis=1)
        rawData_3 = np.transpose(rawData_2)
        expno = int(self.fluorescenceExpno.text())
        xData = rawData_3[0,:]
        yData = rawData_3[expno,:]
        ax = self.fluorescenceFig.figure.add_subplot(111)
        ax.plot(xData, yData,color=next(self.iterColors))
        ax.set(yLabel=r'Intensity / a.u.',xlabel=r'Wavelength / nm')
        self.fluorescenceFig.canvas.figure.tight_layout()
        self.fluorescenceFig.canvas.draw()
