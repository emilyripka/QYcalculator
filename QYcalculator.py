import Tkinter as tk
import ttk
import tkFileDialog, tkMessageBox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import gridspec
import itertools as itertools
import scipy as scipy
from scipy import optimize
from PIL import ImageTk, Image

colorList = itertools.cycle(["#ff0000","#ff3300","#ff6600","#ff9900","#ffcc00","#ffff00","#ccff33",
                          "#99ff33","#009900","#00cc00","#00cc66", "#00ffcc","#0099ff","#3333cc",
                          "#9933ff","#cc00cc","#cc3399","#cc0066","#cc0000"]) #rainbow

# Font options
l_Font = "Cambria 14"
m_Font = "Cambria 12"
s_Font = "Cambria 10"
l_Font_Bold = "Cambria 14 bold"
m_Font_Bold = "Cambria 12 bold"
s_Font_Bold = "Cambria 10 bold"
l_Font_Italic = "Cambria 14 italic"
m_Font_Italic = "Cambria 12 italic"
s_Font_Italic = "Cambria 10 italic"

# Button colors
myGreen = "#DEFCE0"

# Standard global variables
update_in_progress = False
xAxis = np.empty((10,1000))
yAxis = np.empty((10,1000,1000))
Standard_shape = np.empty(10)
yAxisExperimentArray_standardUVvis = [int(x) for x in range(10)]
xAxis_standardPL = np.empty((10,1000))
yAxis_standardPL = np.empty((10,1000,1000))
Standard_shape_PL = np.empty(10)
yAxisExperimentArray_standardPL = [int(x) for x in range(10)]

# Sample global variables
xAxisUVvisSample = np.empty((10,1000))
yAxisUVvisSample = np.empty((10,1000,1000))
Sample_shape = np.empty(10)
yAxisExperimentArray_sampleUVvis = [int(x) for x in range(10)]
xAxis_samplePL = np.empty((10,1000))
yAxis_samplePL = np.empty((10,1000,1000))
Sample_shape_PL = np.empty(10)
yAxisExperimentArray_samplePL = [int(x) for x in range(10)]

# QY calculation variables
absorbanceAtExcitationWavelength_standard = np.ones((10))
absorbanceAtExcitationWavelength_sample = np.ones((10))
PLintegral_standard = np.ones((10))
PLintegral_sample = np.ones((10))
popt_standard = np.ones((2))
pcov_standard = np.ones((2,2))
perr_standard = np.ones((2))
popt_sample = np.ones((2))
pcov_sample = np.ones((2,2))
perr_sample = np.ones((2))
########################################################################################################################

def QYcalculator():
    root = tk.Tk()
    root.title("QYcalculator")
    tk.Tk.iconbitmap(root,default="Icon.ico")
    nb = ttk.Notebook(root)
    page0 = ttk.Frame(nb)
    page1 = ttk.Frame(nb)
    page2 = ttk.Frame(nb)
    page3 = ttk.Frame(nb)
    nb.add(page0, text="Information")
    nb.add(page1, text='Standard')
    nb.add(page2, text='Sample')
    nb.add(page3, text='Results')

    # nb FUNCTIONS
    update_in_progress = False
    def readUVvis(fileNumber,experimentNumber,numberFiles_variable):
        global yAxis
        global xAxis
        global Standard_shape
        global update_in_progress
        global yAxisExperimentArray_standardVvis

        fileName =  tkFileDialog.askopenfilename(title='Choose a UV-vis file')
        rawData_1 = np.genfromtxt(str(fileName), delimiter=",", skip_header=3, skip_footer=95)
        rawData_2 = np.delete(rawData_1, list(range(2, rawData_1.shape[1], 2)), axis=1)
        rawData_3 = np.transpose(rawData_2)
        x_1 = rawData_3[0,:]
        y_1 = rawData_3[1:,:]

        if update_in_progress: return
        try:
            expNumber = experimentNumber.get()
        except ValueError:
            return
        numberFilesEntry = numberFiles_variable.get()
        update_in_progress = True
        yAxisExperimentArray_standardUVvis[fileNumber] = expNumber
        update_in_progress = False

        x_Global = np.ones((numberFilesEntry,x_1.shape[0]))
        for i in range(x_1.shape[0]):
            x_Global[fileNumber,i] = x_1[i]
        xLength = x_Global.shape[1]
        xAxis[fileNumber] = np.zeros((1000))
        update_in_progress = True
        xAxis[fileNumber][0:xLength] = x_Global[fileNumber]
        update_in_progress = False

        y_Global = np.ones((numberFilesEntry,y_1.shape[0],y_1.shape[1]))
        for i in range(y_1.shape[0]):
            for j in range(y_1.shape[1]):
                y_Global[fileNumber,i,j] = y_1[i,j]
        yLength_1 = y_Global.shape[1]
        yLength_2 = y_Global.shape[2]
        yAxis[fileNumber] = np.zeros((1000,1000))

        update_in_progress = True
        yAxis[fileNumber,0:yLength_1,0:yLength_2] = y_Global[fileNumber]
        update_in_progress = True
        Standard_shape[fileNumber] = int((np.shape(y_1))[1])
        update_in_progress = False

    def readUVvisSample(fileNumber,experimentNumber,numberFiles_variable):
        global yAxisUVvisSample
        global xAxisUVvisSample
        global Sample_shape
        global update_in_progress
        global yAxisExperimentArray_sampleUVvis

        fileName =  tkFileDialog.askopenfilename(title='Choose a UV-vis file')
        rawData_1 = np.genfromtxt(str(fileName), delimiter=",", skip_header=3, skip_footer=95)
        rawData_2 = np.delete(rawData_1, list(range(2, rawData_1.shape[1], 2)), axis=1)
        rawData_3 = np.transpose(rawData_2)
        x_1 = rawData_3[0,:]
        y_1 = rawData_3[1:,:]

        if update_in_progress: return
        try:
            expNumber = experimentNumber.get()
        except ValueError:
            return
        numberFilesEntry = numberFiles_variable.get()
        update_in_progress = True
        yAxisExperimentArray_sampleUVvis[fileNumber] = expNumber
        update_in_progress = False

        x_Global = np.ones((numberFilesEntry,x_1.shape[0]))
        for i in range(x_1.shape[0]):
            x_Global[fileNumber,i] = x_1[i]
        xLength = x_Global.shape[1]
        xAxisUVvisSample[fileNumber] = np.zeros((1000))
        update_in_progress = True
        xAxisUVvisSample[fileNumber][0:xLength] = x_Global[fileNumber]
        update_in_progress = False

        y_Global = np.ones((numberFilesEntry,y_1.shape[0],y_1.shape[1]))
        for i in range(y_1.shape[0]):
            for j in range(y_1.shape[1]):
                y_Global[fileNumber,i,j] = y_1[i,j]
        yLength_1 = y_Global.shape[1]
        yLength_2 = y_Global.shape[2]
        yAxisUVvisSample[fileNumber] = np.zeros((1000,1000))

        update_in_progress = True
        yAxisUVvisSample[fileNumber,0:yLength_1,0:yLength_2] = y_Global[fileNumber]
        Sample_shape[fileNumber] = int((np.shape(y_1))[1])
        update_in_progress = False

    def plotUVvis(fileNumber, experimentNumber,fig,ax1,canvas):
        global update_in_progress
        global xAxis
        global yAxis
        global colorList
        global yAxisExperimentArray_standardUVvis

        if update_in_progress: return
        expNumber = experimentNumber.get()
        length = int(Standard_shape[fileNumber])

        update_in_progress = True
        yAxisExperimentArray_standardUVvis[fileNumber] = expNumber
        update_in_progress = False

        columnNumber = expNumber - 1
        yAxisPlotting = yAxis[fileNumber][columnNumber][:]
        xAxisPlotting = xAxis[fileNumber]
        ax1.plot(xAxisPlotting[:length], yAxisPlotting[:length], color=next(colorList))
        ax1.set_xlabel("Wavelength (nm)")
        ax1.set_ylabel("UV-vis Absorbance (a.u.)")
        canvas.show()
        canvas.get_tk_widget().grid(row=4,rowspan=60,column=7,columnspan=60)
        canvas.draw()

    def plotUVvisSample(fileNumber, experimentNumber,fig,ax1,canvas):
        global update_in_progress
        global xAxisUVvisSample
        global yAxisUVvisSample
        global colorList
        global yAxisExperimentArray_sampleUVvis

        if update_in_progress: return
        expNumber = experimentNumber.get()
        length = int(Sample_shape[fileNumber])

        update_in_progress = True
        yAxisExperimentArray_sampleUVvis[fileNumber] = expNumber
        update_in_progress = False

        columnNumber = expNumber - 1
        yAxisPlotting = yAxisUVvisSample[fileNumber][columnNumber][:]
        xAxisPlotting = xAxisUVvisSample[fileNumber]
        ax1.plot(xAxisPlotting[:length], yAxisPlotting[:length], color=next(colorList))
        ax1.set_xlabel("Wavelength (nm)")
        ax1.set_ylabel("UV-vis Absorbance (a.u.)")
        canvas.show()
        canvas.get_tk_widget().grid(row=4,rowspan=60,column=7,columnspan=60)
        canvas.draw()

    def clearAndPlotUVvis(fileNumber, experimentNumber,fig,ax1,canvas):
        global update_in_progress
        global xAxis
        global yAxis
        global colorList
        global yAxisExperimentArray_standardUVvis

        if update_in_progress: return
        expNumber = experimentNumber.get()
        length = int(Standard_shape[fileNumber])

        update_in_progress = True
        yAxisExperimentArray_standardUVvis[fileNumber] = expNumber
        update_in_progress = False

        columnNumber = expNumber - 1
        yAxisPlotting = yAxis[fileNumber][columnNumber][:]
        xAxisPlotting = xAxis[fileNumber]
        ax1.clear()
        ax1.plot(xAxisPlotting[:length], yAxisPlotting[:length], color=next(colorList))
        ax1.set_xlabel("Wavelength (nm)")
        ax1.set_ylabel("UV-vis Absorbance (a.u.)")
        canvas.show()
        canvas.get_tk_widget().grid(row=4,rowspan=60,column=7,columnspan=60)
        canvas.draw()

    def clearAndPlotUVvisSample(fileNumber, experimentNumber,fig,ax1,canvas):
        global update_in_progress
        global xAxisUVvisSample
        global yAxisUVvisSample
        global colorList
        global yAxisExperimentArray_sampleUVvis

        if update_in_progress: return
        expNumber = experimentNumber.get()
        length = int(Sample_shape[fileNumber])

        update_in_progress = True
        yAxisExperimentArray_sampleUVvis[fileNumber] = expNumber
        update_in_progress = False

        columnNumber = expNumber - 1
        yAxisPlotting = yAxisUVvisSample[fileNumber][columnNumber][:]
        xAxisPlotting = xAxisUVvisSample[fileNumber]
        ax1.clear()
        ax1.plot(xAxisPlotting[:length], yAxisPlotting[:length], color=next(colorList))
        ax1.set_xlabel("Wavelength (nm)")
        ax1.set_ylabel("UV-vis Absorbance (a.u.)")
        canvas.show()
        canvas.get_tk_widget().grid(row=4,rowspan=60,column=7,columnspan=60)
        canvas.draw()

    def readPLstandard(fileNumber,experimentNumber,numberFiles_variable):
        global yAxis_standardPL
        global xAxis_standardPL
        global update_in_progress
        global Standard_shape_PL
        global yAxisExperimentArray_standardPL

        if update_in_progress: return
        try:
            numberFilesEntry = numberFiles_variable.get()
            expNumber = experimentNumber.get()
        except ValueError:
            return

        update_in_progress = True
        numberFiles_variable = numberFilesEntry
        update_in_progress = False

        fileName =  tkFileDialog.askopenfilename(title='Choose a PL file')
        rawData_1 = np.genfromtxt(str(fileName), delimiter=",", skip_header=3, skip_footer=37)
        rawData_2 = np.delete(rawData_1, list(range(2, rawData_1.shape[1], 2)), axis=1)
        rawData_3 = np.transpose(rawData_2)
        x_1 = rawData_3[0,:]
        y_1 = rawData_3[1:,:]

        if update_in_progress: return
        try:
            expNumber = experimentNumber.get()
        except ValueError:
            return
        update_in_progress = True
        yAxisExperimentArray_standardPL[fileNumber] = expNumber
        update_in_progress = False
        numberFilesEntry = numberFiles_variable

        x_Global = np.ones((numberFilesEntry,x_1.shape[0]))
        for i in range(x_1.shape[0]):
            x_Global[fileNumber,i] = x_1[i]
        xLength = x_Global.shape[1]
        xAxis_standardPL[fileNumber] = np.zeros((1000))
        update_in_progress = True
        xAxis_standardPL[fileNumber][0:xLength] = x_Global[fileNumber]
        update_in_progress = False

        y_Global = np.ones((numberFilesEntry,y_1.shape[0],y_1.shape[1]))
        for i in range(y_1.shape[0]):
            for j in range(y_1.shape[1]):
                y_Global[fileNumber,i,j] = y_1[i,j]
        yLength_1 = y_Global.shape[1]
        yLength_2 = y_Global.shape[2]
        yAxis_standardPL[fileNumber] = np.zeros((1000,1000))

        update_in_progress = True
        yAxis_standardPL[fileNumber,0:yLength_1,0:yLength_2] = y_Global[fileNumber]
        Standard_shape_PL[fileNumber] = int((np.shape(y_1))[1])
        update_in_progress = False

    def readPLsample(fileNumber,experimentNumber,numberFiles_variable):
        global yAxis_samplePL
        global xAxis_samplePL
        global Sample_shape_PL
        global update_in_progress
        global yAxisExperimentArray_samplePL

        if update_in_progress: return
        try:
            numberFilesEntry = numberFiles_variable.get()
            expNumber = experimentNumber.get()
        except ValueError:
            return

        update_in_progress = True
        numberFiles_variable = numberFilesEntry
        update_in_progress = False

        fileName =  tkFileDialog.askopenfilename(title='Choose a PL file')
        rawData_1 = np.genfromtxt(str(fileName), delimiter=",", skip_header=3, skip_footer=37)
        rawData_2 = np.delete(rawData_1, list(range(2, rawData_1.shape[1], 2)), axis=1)
        rawData_3 = np.transpose(rawData_2)
        x_1 = rawData_3[0,:]
        y_1 = rawData_3[1:,:]

        if update_in_progress: return
        try:
            expNumber = experimentNumber.get()
        except ValueError:
            return

        update_in_progress = True
        yAxisExperimentArray_samplePL[fileNumber] = expNumber
        update_in_progress = False

        numberFilesEntry = numberFiles_variable
        x_Global = np.ones((numberFilesEntry,x_1.shape[0]))
        for i in range(x_1.shape[0]):
            x_Global[fileNumber,i] = x_1[i]
        xLength = x_Global.shape[1]
        xAxis_samplePL[fileNumber] = np.zeros((1000))

        update_in_progress = True
        xAxis_samplePL[fileNumber][0:xLength] = x_Global[fileNumber]
        update_in_progress = False

        y_Global = np.ones((numberFilesEntry,y_1.shape[0],y_1.shape[1]))
        for i in range(y_1.shape[0]):
            for j in range(y_1.shape[1]):
                y_Global[fileNumber,i,j] = y_1[i,j]
        yLength_1 = y_Global.shape[1]
        yLength_2 = y_Global.shape[2]
        yAxis_samplePL[fileNumber] = np.zeros((1000,1000))

        update_in_progress = True
        yAxis_samplePL[fileNumber,0:yLength_1,0:yLength_2] = y_Global[fileNumber]
        Sample_shape_PL[fileNumber] = int((np.shape(y_1))[1])
        update_in_progress = False

    def plotPLstandard(fileNumber, experimentNumber,fig,ax2,canvas):
        global update_in_progress
        global xAxis_standardPL
        global yAxis_standardPL
        global colorList
        global yAxisExperimentArray_standardPL

        if update_in_progress: return
        expNumber = experimentNumber.get()

        update_in_progress = True
        yAxisExperimentArray_standardPL[fileNumber] = expNumber
        update_in_progress = False

        length = int(Standard_shape_PL[fileNumber])
        columnNumber = expNumber - 1
        yAxisPlotting = yAxis_standardPL[fileNumber][columnNumber][:]
        xAxisPlotting = xAxis_standardPL[fileNumber]
        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position("right")
        ax2.plot(xAxisPlotting[:length], yAxisPlotting[:length], color=next(colorList))
        ax2.set_xlabel("Wavelength (nm)")
        ax2.set_ylabel("PL Intensity (a.u.)")
        canvas.show()
        canvas.get_tk_widget().grid(row=4,rowspan=60,column=7,columnspan=60)
        canvas.draw()

    def plotPLsample(fileNumber, experimentNumber,fig,ax2,canvas):
        global update_in_progress
        global xAxis_samplePL
        global yAxis_samplePL
        global colorList
        global yAxisExperimentArray_samplePL

        if update_in_progress: return
        expNumber = experimentNumber.get()
        length = int(Sample_shape_PL[fileNumber])

        update_in_progress = True
        yAxisExperimentArray_samplePL[fileNumber] = expNumber
        update_in_progress = False
        
        columnNumber = expNumber - 1
        yAxisPlotting = yAxis_samplePL[fileNumber][columnNumber][:]
        xAxisPlotting = xAxis_samplePL[fileNumber]
        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position("right")
        ax2.plot(xAxisPlotting[:length], yAxisPlotting[:length], color=next(colorList))
        ax2.set_xlabel("Wavelength (nm)")
        ax2.set_ylabel("PL Intensity (a.u.)")
        canvas.show()
        canvas.get_tk_widget().grid(row=4,rowspan=60,column=7,columnspan=60)
        canvas.draw()

    def clearAndPlotPLstandard(fileNumber, experimentNumber,fig,ax2,canvas):
        global update_in_progress
        global xAxis_standardPL
        global yAxis_standardPL
        global colorList
        global yAxisExperimentArray_standardPL

        if update_in_progress: return
        expNumber = experimentNumber.get()

        update_in_progress = True
        yAxisExperimentArray_standardPL[fileNumber] = expNumber
        update_in_progress = False

        length = int(Standard_shape_PL[fileNumber])
        columnNumber = expNumber - 1
        yAxisPlotting = yAxis_standardPL[fileNumber][columnNumber][:]
        xAxisPlotting = xAxis_standardPL[fileNumber]
        ax2.clear()
        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position("right")
        ax2.plot(xAxisPlotting[:length], yAxisPlotting[:length], color=next(colorList))
        ax2.set_xlabel("Wavelength (nm)")
        ax2.set_ylabel("PL Intensity (a.u.)")
        canvas.show()
        canvas.get_tk_widget().grid(row=4,rowspan=60,column=7,columnspan=60)
        canvas.draw()

    def clearAndPlotPLsample(fileNumber, experimentNumber,fig,ax2,canvas):
        global update_in_progress
        global xAxis_samplePL
        global yAxis_samplePL
        global colorList
        global yAxisExperimentArray_samplePL

        if update_in_progress: return
        expNumber = experimentNumber.get()
        length = int(Sample_shape_PL[fileNumber])

        update_in_progress = True
        yAxisExperimentArray_samplePL[fileNumber] = expNumber
        update_in_progress = False
        
        columnNumber = expNumber - 1
        yAxisPlotting = yAxis_samplePL[fileNumber][columnNumber][:]
        xAxisPlotting = xAxis_samplePL[fileNumber]
        ax2.clear()
        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position("right")
        ax2.plot(xAxisPlotting[:length], yAxisPlotting[:length], color=next(colorList))
        ax2.set_xlabel("Wavelength (nm)")
        ax2.set_ylabel("PL Intensity (a.u.)")
        canvas.show()
        canvas.get_tk_widget().grid(row=4,rowspan=60,column=7,columnspan=60)
        canvas.draw()

    def linear(x,m,b):
        return m*x + b

    def absVsPLplotStandard(absorbanceAtExcitationWavelength_standard,PLintegral_standard,update_in_progress,
            xAxis,yAxis,xAxis_standardPL,yAxis_standardPL,yAxisExperimentArray_standardUVvis,
            yAxisExperimentArray_standardPL,fig,ax1,canvas,numberFiles_variable):
        global popt_standard
        global pcov_standard
        global perr_standard 

        if update_in_progress: return
        try:
            excitationWavelengthEntry = excitationWavelength_variable.get()
            lowerWavelength = lowerWavelengthStandard_variable.get()
            upperWavelength = upperWavelengthStandard_variable.get()
            nFiles = numberFiles_variable.get()
        except ValueError:
            return

        absorbanceAtExcitationWavelength = np.ones((nFiles))
        excitationWavelengthIndex = 0
        for counter,value in enumerate(xAxis[0]):
            if value == excitationWavelengthEntry:
                excitationWavelengthIndex = counter
        lowerWavelengthIndex = 0
        upperWavelengthIndex = 0
        xAxisEnumerate = xAxis_standardPL[0,:]
        for counter,value in enumerate(xAxisEnumerate):
            if value == lowerWavelength:
                lowerWavelengthIndex = counter
        for counter,value in enumerate(xAxisEnumerate):
            if value == upperWavelength:
                upperWavelengthIndex = counter
        for i in range(nFiles):
           absorbanceAtExcitationWavelength[i] = \
                        yAxis[i,(yAxisExperimentArray_standardUVvis[i]-1),excitationWavelengthIndex]

        update_in_progress = True
        absorbanceAtExcitationWavelength_standard = absorbanceAtExcitationWavelength
        update_in_progress = False

        PLintegral = np.ones((nFiles))
        for i in range(nFiles):
            PLintegral[i] = np.trapz(yAxis_standardPL[i,(yAxisExperimentArray_standardPL[i]-1),
                                     lowerWavelengthIndex:upperWavelengthIndex])

        update_in_progress = True
        PLintegral_standard = PLintegral
        update_in_progress = False

        ax1.clear()
        ax1.set_title("Standard Gradient Curve")
        ax1.plot(absorbanceAtExcitationWavelength, PLintegral, "ro")
        ax1.set_xlabel("Absorbance at Excitation Wavelength", family="serif",  fontsize=10)
        ax1.set_ylabel("Area Under PL Curve", family="serif", fontsize=10)
        popt, pcov = scipy.optimize.curve_fit(linear, absorbanceAtExcitationWavelength,
                                                      PLintegral, p0=[(2e8/0.0225),0])
        perr = np.sqrt(np.diag(pcov))

        update_in_progress = True
        popt_standard = popt
        pcov_standard = pcov
        perr_standard = perr
        update_in_progress = False

        ax1.plot(absorbanceAtExcitationWavelength, linear(absorbanceAtExcitationWavelength, *popt),"k-")
        gradientCurveStandard_variable.set((perr[0]/popt[0])*100)
        canvas.show()
        canvas.get_tk_widget().grid(row=13,rowspan=59,column=0,columnspan=60)
        canvas.draw()

    def absVsPLplotSample(absorbanceAtExcitationWavelength_sample,PLintegral_sample,update_in_progress,
            xAxis,yAxis,xAxis_samplePL,yAxis_samplePL,yAxisExperimentArray_sampleUVvis,
            yAxisExperimentArray_samplePL,fig,ax2,canvas,numberFiles_variable):
        global popt_sample
        global pcov_sample
        global perr_sample

        if update_in_progress: return
        try:
            excitationWavelengthEntry = excitationWavelength_variableSample.get()
            lowerWavelength = lowerWavelengthSample_variable.get()
            upperWavelength = upperWavelengthSample_variable.get()
            nFiles = numberFiles_variable.get()
        except ValueError:
            return

        absorbanceAtExcitationWavelength = np.ones((nFiles))
        excitationWavelengthIndex = 0
        for counter,value in enumerate(xAxis[0]):
            if value == excitationWavelengthEntry:
                excitationWavelengthIndex = counter
        lowerWavelengthIndex = 0
        upperWavelengthIndex = 0
        xAxisEnumerate = xAxis_samplePL[0,:]
        for counter,value in enumerate(xAxisEnumerate):
            if value == lowerWavelength:
                lowerWavelengthIndex = counter
        for counter,value in enumerate(xAxisEnumerate):
            if value == upperWavelength:
                upperWavelengthIndex = counter
        for i in range(nFiles):
           absorbanceAtExcitationWavelength[i] = \
                        yAxis[i,(yAxisExperimentArray_sampleUVvis[i]-1),excitationWavelengthIndex]

        update_in_progress = True
        absorbanceAtExcitationWavelength_sample = absorbanceAtExcitationWavelength
        update_in_progress = False

        PLintegral = np.ones((nFiles))
        for i in range(nFiles):
            PLintegral[i] = np.trapz(yAxis_samplePL[i,(yAxisExperimentArray_samplePL[i]-1),
                                     lowerWavelengthIndex:upperWavelengthIndex])

        update_in_progress = True
        PLintegral_sample = PLintegral
        update_in_progress = False

        ax2.clear()
        ax2.set_title("Sample Gradient Curve")
        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position("right")
        ax2.plot(absorbanceAtExcitationWavelength, PLintegral, "ro")
        ax2.set_xlabel("Absorbance at Excitation Wavelength", family="serif",  fontsize=10)
        ax2.set_ylabel("Area Under PL Curve", family="serif", fontsize=10)
        popt, pcov = scipy.optimize.curve_fit(linear, absorbanceAtExcitationWavelength,
                                                      PLintegral, p0=[(2e8/0.0225),0])
        perr = np.sqrt(np.diag(pcov))

        update_in_progress = True
        popt_sample = popt
        pcov_sample = pcov
        perr_sample = perr
        update_in_progress = False

        ax2.plot(absorbanceAtExcitationWavelength, linear(absorbanceAtExcitationWavelength, *popt),"k-")
        gradientCurveSample_variable.set((perr[0]/popt[0])*100)
        canvas.show()
        canvas.get_tk_widget().grid(row=13,rowspan=59,column=0,columnspan=60)
        canvas.draw()

    def QYcalculation(popt_standard,popt_sample,perr_standard,perr_sample,update_in_progress,variable4,variable7,variable2):
        grad_standard = popt_standard[0]
        grad_sample = popt_sample[0]
        error_standard = perr_standard[0]
        error_sample = perr_sample[0]
        if update_in_progress: return
        try:
            RI_standardEntry = variable4.get()
            RI_sampleEntry = variable7.get()
            QY_standardEntry = variable2.get()
        except ValueError:
            return
        QY_sample = 100*((QY_standardEntry*0.01)*(grad_sample/grad_standard)*((RI_sampleEntry**2)/(RI_standardEntry**2)))
        QY_sample_error = (abs(QY_sample)*np.sqrt(((error_sample/grad_sample)**2)+((error_standard/grad_standard)**2)))
        QYsample_variable.set(QY_sample)
        QYsample_error_variable.set(QY_sample_error)

    # Standard Figure
    fig = Figure(figsize=(10,4), dpi=100)
    gs = gridspec.GridSpec(1, 2)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    canvas = FigureCanvasTkAgg(fig, page1)

    # Sample Figure
    figSample = Figure(figsize=(10,4), dpi=100)
    gsSample = gridspec.GridSpec(1, 2)
    ax1Sample = figSample.add_subplot(gsSample[0])
    ax2Sample = figSample.add_subplot(gsSample[1])
    canvasSample = FigureCanvasTkAgg(figSample, page2)

    # Gradient Curve Figures
    figGrad = Figure(figsize=(10,4), dpi=100)
    gsGrad = gridspec.GridSpec(1, 2)
    ax1Grad = figGrad.add_subplot(gsGrad[0])
    ax2Grad = figGrad.add_subplot(gsGrad[1])
    canvasGrad = FigureCanvasTkAgg(figGrad, page3)

    # Information page
    #tk.Label(page0, text="*** This is an open source application for finding relative quantum yield of fluorophores ***").grid(row=0,column=0,columnspan=20, sticky="ew")
    tk.Label(page0,text="How-To Guide",font=l_Font_Bold).grid(row=1,column=0,columnspan=3, sticky=tk.E+tk.W)
    tk.Label(page0,text="(I) Standard (navigate to 'Standard' tab)",font=m_Font_Bold).grid(row=2,column=0,columnspan=3, sticky="W")
    tk.Label(page0,text="").grid(row=3,column=0,columnspan=1, sticky="W")
    tk.Label(page0,text="(i) Enter number of UV-vis measurements made for the QY measurement",\
            font=s_Font).grid(row=3,column=1,columnspan=2, sticky="w")
    tk.Label(page0,text="(ii) Select files for each UV-vis measurement and enter the experiment number of that measurement file.",\
            font=s_Font).grid(row=4,column=1,columnspan=2, sticky="w")            
    tk.Label(page0,text="**This data was likely stored in one of two ways:",\
            font=s_Font_Italic).grid(row=5,column=1,columnspan=2, sticky="w")
    tk.Label(page0,text="(a) all UV-vis measurements were collected, and then all scans were saved to the same file as different scans (i.e. experiment number)",\
            font=s_Font_Italic).grid(row=6,column=2,columnspan=1, sticky="w")
    tk.Label(page0,text="(b) after each UV-vis measurement, the scan was saved as a new file",\
            font=s_Font_Italic).grid(row=7,column=2,columnspan=1, sticky="w")
    tk.Label(page0,text="**It will be helpful to use the 'Plot' and 'Clear&Plot' buttons to visualize which experiment your measurement is",\
            font=s_Font_Italic).grid(row=8,column=2,columnspan=1, sticky="w")
    tk.Label(page0,text="**Make sure to keep the 'Experiment #' as the desired value before proceeding.",
            font=s_Font_Italic).grid(row=9,column=2,columnspan=1, sticky="w")
    tk.Label(page0,text="(iii) Repeat step (ii) for the fluorescence measurments.",
            font=s_Font).grid(row=10,column=1,columnspan=2, sticky="w")
    tk.Label(page0,text="(iii) Repeat step (ii) for the fluorescence measurments.",
            font=s_Font).grid(row=10,column=1,columnspan=2, sticky="w")
    tk.Label(page0,text="(iv) Fill in the blanks at the top-right of the tab.",
            font=s_Font).grid(row=11,column=1,columnspan=2, sticky="w")
    tk.Label(page0,text="(v) Navigate to the Results tab, and click the 'Standard Gradient Curve' button.",
            font=s_Font).grid(row=12,column=1,columnspan=2, sticky="w")
    tk.Label(page0,text="**The printed 'Standard slope error (%)' needs to be <10% to be an accurate standard gradient curve.",
            font=s_Font_Italic).grid(row=13,column=1,columnspan=2, sticky="w")
    tk.Label(page0,text="(II) Sample (navigate to 'Sample' tab)",
            font=m_Font_Bold).grid(row=14,column=0,columnspan=3, sticky="w")
    tk.Label(page0,text="(i) Repeat Standard steps (i) through (iv)",
            font=s_Font).grid(row=15,column=1,columnspan=2, sticky="w")
    tk.Label(page0,text="(ii) Navigate to the Results tab, and click the 'Sample Gradient Curve' button.",
            font=s_Font).grid(row=16,column=1,columnspan=2, sticky="w")
    tk.Label(page0,text="**The printed 'Sample slope error (%)' needs to be <10% to be an accurate sample gradient curve.",
            font=s_Font_Italic).grid(row=17,column=1,columnspan=2, sticky="w")
    tk.Label(page0,text="(III) QY calculation (navigate to the 'Results' tab)",
            font=m_Font_Bold).grid(row=18,column=0,columnspan=3, sticky="w")
    tk.Label(page0,text="(i) Click the 'Sample QY Calculation' button",
            font=s_Font).grid(row=19,column=1,columnspan=2, sticky="w")

    # Standard
    numberFilesVariableStandard = tk.IntVar()
    tk.Label(page1, text="Number of UV-vis files for standard (1-10):").grid(row=0,column=0,columnspan=6)#, sticky=tk.E+tk.W)
    tk.Entry(page1, textvariable=numberFilesVariableStandard,width=4).grid(row=0, column=6)
    tk.Label(page1,text="Standard Fluorescence").grid(row=14,column=0,columnspan=6)
    expNo = np.array([tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()])
    expNo_standardPL = np.array([tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()])
    # Standard compound choice menu
    tk.Label(page1, text="Compound:").grid(row=1,column=19,columnspan=1,sticky="E")
    variable = tk.StringVar()
    variable.set("Rhodamine 6G") # default value
    ttk.OptionMenu(page1,variable,"Rhodamine 6G","Rhodamine 6G","Standard #2", "Standard #3").grid(row=1,column=21,columnspan=10,sticky="W")
    # Standard compound QY entry box
    tk.Label(page1, text="QY (%):").grid(row=1,column=33,columnspan=12,sticky="E")
    variable2 = tk.IntVar()
    variable2.set(95) # default value
    tk.Entry(page1, textvariable=variable2,width=4).grid(row=1,column=46,columnspan=5,sticky="W")
    # Standard solvent selection optionmenu
    tk.Label(page1, text="Solvent:").grid(row=2,column=19,columnspan=1,sticky="E")
    variable3 = tk.StringVar()
    variable3.set("ethanol") # default value
    ttk.OptionMenu(page1,variable3,"ethanol","ethanol","methanol","butanol","acetone","toluene","hexane").grid(row=2,column=21,columnspan=10,sticky="W")
    # Standard solvent refractive index entry box
    tk.Label(page1, text="Refractive Index:").grid(row=2,column=33,columnspan=12,sticky="E")
    variable4 = tk.DoubleVar()
    tk.Entry(page1,textvariable=variable4,width=5).grid(row=2,column=46,columnspan=5,sticky="W")
    # Excitation wavelength assignment entry box
    excitationWavelength_variable = tk.DoubleVar()
    tk.Label(page1,text="Excitation Wavelength (nm):").grid(row=0,column=7,columnspan=5,sticky="e")
    tk.Entry(page1,textvariable=excitationWavelength_variable,width=4).grid(row=0, column=13, sticky="w")
    # Lower standard PL wavelength for integration assignment entry box
    lowerWavelengthStandard_variable = tk.DoubleVar()
    tk.Label(page1,text="Lower Integration Wavelength (nm):").grid(row=1,column=7,columnspan=5,sticky="e")
    tk.Entry(page1,textvariable=lowerWavelengthStandard_variable,width=4).grid(row=1, column=13, sticky="w")
    # Upper standard PL wavelength for integration assignment entry box
    upperWavelengthStandard_variable = tk.DoubleVar()
    tk.Label(page1,text="Upper Integration Wavelength (nm):").grid(row=2,column=7,columnspan=5,sticky="e")
    tk.Entry(page1,textvariable=upperWavelengthStandard_variable,width=4).grid(row=2, column=13, sticky="w")

    # Sample
    numberFilesVariableSample = tk.IntVar()
    tk.Label(page2, text="Number of UV-vis files for sample (1-10):").grid(row=0,column=0,columnspan=6,sticky="e")
    tk.Entry(page2, textvariable=numberFilesVariableSample,width=4).grid(row=0, column=6, sticky="w")
    tk.Label(page2, text="Sample PL").grid(row=14,column=0,columnspan=6)
    expNo_sample = np.array([tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()])
    expNo_samplePL = np.array([tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()])
    # Excitation wavelength assignment entry box
    excitationWavelength_variableSample = tk.DoubleVar()
    tk.Label(page2,text="Excitation Wavelength (nm):").grid(row=0,column=7,columnspan=5,sticky="e")
    tk.Entry(page2,textvariable=excitationWavelength_variableSample,width=4).grid(row=0, column=13, sticky="w")
    # Lower sample PL wavelength for integration assignment entry box
    lowerWavelengthSample_variable = tk.DoubleVar()
    tk.Label(page2,text="Lower Integration Wavelength for Sample (nm):").grid(row=1,column=7,columnspan=5,sticky="e")
    tk.Entry(page2,textvariable=lowerWavelengthSample_variable,width=4).grid(row=1, column=13, sticky="w")
    # Upper sample PL wavelength for integration assignment entry box
    upperWavelengthSample_variable = tk.DoubleVar()
    tk.Label(page2,text="Upper Integration Wavelength for Sample (nm):").grid(row=2,column=7,columnspan=5,sticky="e")
    tk.Entry(page2,textvariable=upperWavelengthSample_variable,width=4).grid(row=2, column=13, sticky="w")
    # Sample compound selection menu
    ttk.Label(page2, text="Compound:").grid(row=1,column=19,columnspan=1,sticky="E")
    variable8 = tk.StringVar()
    variable8.set("unknown") # default value
    ttk.OptionMenu(page2,variable8,"CsPbBr3","CsPbBr3","CsPbCl3", "CsPbI3").grid(row=1,column=21,columnspan=10,sticky="W")
    #  Sample solvent selection optionmenu
    ttk.Label(page2, text="Solvent:").grid(row=2,column=19,columnspan=1,sticky="E")
    variable6 = tk.StringVar()
    variable6.set("toluene") # default value
    ttk.OptionMenu(page2,variable6,"toluene",'toluene',"hexane","ethanol","methanol","butanol","acetone").grid(row=2,column=21,columnspan=10,sticky="W")
    # Sample solvent refractive index entry box
    ttk.Label(page2, text="Refractive Index:").grid(row=2,column=33,columnspan=10,sticky="E")
    variable7 = tk.DoubleVar()
    ttk.Entry(page2,textvariable=variable7,width=5).grid(row=2,column=44,columnspan=5,sticky="W")

    for i in range(0,10):
        thisText_i = i+1
        # Standard UV-vis
        thisText = ('File #%d:' % thisText_i) 
        tk.Label(page1,text=thisText).grid(row=i+1,column=0) 
        tk.Button(page1,bg=myGreen,text="Browse",command=lambda i=i:readUVvis(fileNumber=i,experimentNumber=expNo[i],
            numberFiles_variable=numberFilesVariableStandard)).grid(row=i+1,column=1)
        thisText = ('Experiment #%d:' % thisText_i)
        tk.Label(page1,text=thisText).grid(row=i+1,column=3)
        tk.Entry(page1,textvariable=expNo[i],width=4).grid(row=i+1,column=4)
        tk.Button(page1,bg=myGreen,text="Plot",command=lambda i=i:plotUVvis(fileNumber=i,experimentNumber=expNo[i],
            fig=fig,ax1=ax1,canvas=canvas)).grid(row=i+1,column=5)
        tk.Button(page1,bg=myGreen,text="Clear&Plot",command=lambda i=i:clearAndPlotUVvis(fileNumber=i,experimentNumber=expNo[i],
            fig=fig,ax1=ax1,canvas=canvas)).grid(row=i+1,column=6)
        # Standard fluorescence
        thisText = ('File #%d:' % thisText_i)
        tk.Label(page1,text=thisText).grid(row=i+15,column=0) 
        tk.Button(page1,bg=myGreen,text="Browse",command=lambda i=i:readPLstandard(fileNumber=i,experimentNumber=expNo_standardPL[i],
            numberFiles_variable=numberFilesVariableStandard)).grid(row=i+15,column=1)
        thisText = ('Experiment #%d:' % thisText_i)
        tk.Label(page1,text=thisText).grid(row=i+15,column=3)
        tk.Entry(page1,textvariable=expNo_standardPL[i],width=4).grid(row=i+15,column=4)
        tk.Button(page1,bg=myGreen,text="Plot",command=lambda i=i:plotPLstandard(fileNumber=i,experimentNumber=expNo_standardPL[i],
            fig=fig,ax2=ax2,canvas=canvas)).grid(row=i+15,column=5)
        tk.Button(page1,bg=myGreen,text="Clear&Plot",command=lambda i=i:clearAndPlotPLstandard(fileNumber=i,experimentNumber=expNo_standardPL[i],
            fig=fig,ax2=ax2,canvas=canvas)).grid(row=i+15,column=6)
        # Sample UV-vis
        thisText = ('File #%d:' % thisText_i) 
        tk.Label(page2,text=thisText).grid(row=i+1,column=0) 
        tk.Button(page2,bg=myGreen,text="Browse",command=lambda i=i:readUVvisSample(fileNumber=i,experimentNumber=expNo_sample[i],
            numberFiles_variable=numberFilesVariableSample)).grid(row=i+1,column=1)
        thisText = ('Experiment #%d:' % thisText_i)
        tk.Label(page2,text=thisText).grid(row=i+1,column=3)
        tk.Entry(page2,textvariable=expNo_sample[i],width=4).grid(row=i+1,column=4)
        tk.Button(page2,bg=myGreen,text="Plot",command=lambda i=i:plotUVvisSample(fileNumber=i,experimentNumber=expNo_sample[i],
            fig=figSample,ax1=ax1Sample,canvas=canvasSample)).grid(row=i+1,column=5)
        tk.Button(page2,bg=myGreen,text="Clear&Plot",command=lambda i=i:clearAndPlotUVvisSample(fileNumber=i,experimentNumber=expNo_sample[i],
            fig=figSample,ax1=ax1Sample,canvas=canvasSample)).grid(row=i+1,column=6)   
        # Sample fluorescence
        thisText = ('File #%d:' % thisText_i)
        tk.Label(page2,text=thisText).grid(row=i+15,column=0) 
        tk.Button(page2,bg=myGreen,text="Browse",command=lambda i=i:readPLsample(fileNumber=i,experimentNumber=expNo_samplePL[i],
            numberFiles_variable=numberFilesVariableSample)).grid(row=i+15,column=1)
        thisText = ('Experiment #%d:' % thisText_i)
        tk.Label(page2,text=thisText).grid(row=i+15,column=3)
        tk.Entry(page2,textvariable=expNo_samplePL[i],width=4).grid(row=i+15,column=4)
        tk.Button(page2,bg=myGreen,text="Plot",command=lambda i=i:plotPLsample(fileNumber=i,experimentNumber=expNo_samplePL[i],
            fig=figSample,ax2=ax2Sample,canvas=canvasSample)).grid(row=i+15,column=5)
        tk.Button(page2,bg=myGreen,text="Clear&Plot",command=lambda i=i:clearAndPlotPLsample(fileNumber=i,experimentNumber=expNo_samplePL[i],
            fig=figSample,ax2=ax2Sample,canvas=canvasSample)).grid(row=i+15,column=6)
    
    # Results Page 
    # standard gradient curve slope error entry box
    ttk.Label(page3,text="Standard slope error (%):").grid(row=10,column=4,columnspan=4,sticky="E")
    gradientCurveStandard_variable = tk.DoubleVar()
    gradientCurveStandard_variable.set("?") 
    ttk.Entry(page3,textvariable=gradientCurveStandard_variable,width=4).grid(row=10,column=8,columnspan=1,sticky=tk.E+tk.W)

    # sample gradient curve slope error entry box
    ttk.Label(page3,text="Sample slope error (%):").grid(row=11,column=4,columnspan=4,sticky="E")
    gradientCurveSample_variable = tk.DoubleVar()
    gradientCurveSample_variable.set("?") 
    ttk.Entry(page3,textvariable=gradientCurveSample_variable,width=4).grid(row=11,column=8,columnspan=1,sticky=tk.E+tk.W)

    # Sample compound QY entry box
    ttk.Label(page3, text="QY (%):").grid(row=75,column=4,columnspan=1,sticky="e")
    QYsample_variable = tk.DoubleVar()
    QYsample_variable.set("?") 
    ttk.Entry(page3, textvariable=QYsample_variable,width=4).grid(row=75,column=5,columnspan=1,sticky=tk.E+tk.W)

    # Sample compound QY error entry box
    ttk.Label(page3, text="+/-").grid(row=75,column=6,columnspan=1,sticky="e")
    QYsample_error_variable = tk.DoubleVar()
    QYsample_error_variable.set("?") 
    ttk.Entry(page3, textvariable=QYsample_error_variable,width=4).grid(row=75,column=7,columnspan=1,sticky=tk.E+tk.W)  

    tk.Button(page3,bg=myGreen,text="Standard Gradient Curve", command=lambda:absVsPLplotStandard(
            absorbanceAtExcitationWavelength_standard=absorbanceAtExcitationWavelength_standard,
            PLintegral_standard=PLintegral_standard,
            update_in_progress=update_in_progress,
            xAxis=xAxis,
            yAxis=yAxis,
            xAxis_standardPL=xAxis_standardPL,
            yAxis_standardPL=yAxis_standardPL,
            yAxisExperimentArray_standardUVvis=yAxisExperimentArray_standardUVvis,
            yAxisExperimentArray_standardPL=yAxisExperimentArray_standardPL,
            fig=figGrad,
            ax1=ax1Grad,
            canvas=canvasGrad,
            numberFiles_variable=numberFilesVariableStandard)).grid(row=10,column=0,columnspan=4)

    tk.Button(page3,bg=myGreen,text="Sample Gradient Curve",command=lambda:absVsPLplotSample(
            absorbanceAtExcitationWavelength_sample=absorbanceAtExcitationWavelength_sample,
            PLintegral_sample=PLintegral_sample,
            update_in_progress=update_in_progress,
            xAxis=xAxisUVvisSample,
            yAxis=yAxisUVvisSample,
            xAxis_samplePL=xAxis_samplePL,
            yAxis_samplePL=yAxis_samplePL,
            yAxisExperimentArray_sampleUVvis=yAxisExperimentArray_sampleUVvis,
            yAxisExperimentArray_samplePL=yAxisExperimentArray_samplePL,
            fig=figGrad,
            ax2=ax2Grad,
            canvas=canvasGrad,
            numberFiles_variable=numberFilesVariableSample)).grid(row=11,column=0,columnspan=4)

    tk.Button(page3,bg=myGreen,text="Sample QY Calculation",command=lambda:QYcalculation(
                popt_standard=popt_standard,popt_sample=popt_sample,perr_sample=perr_sample,
                perr_standard=perr_standard,update_in_progress=update_in_progress,
                variable4=variable4,variable7=variable7,variable2=variable2)).grid(row=75,column=0,columnspan=4)

    ttk.Label(page3,text="").grid(row=0,column=0)
    ttk.Label(page3,text="").grid(row=12,column=0)
    ttk.Label(page3,text="").grid(row=74,column=0)

    nb.grid(row=0,column=0)
    root.mainloop()

if __name__ == "__main__":
    QYcalculator()
