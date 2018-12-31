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

# Rainbow
colorList = itertools.cycle(["#ff0000","#ff3300","#ff6600","#ff9900","#ffcc00","#ffff00",
                             "#ccff33","#99ff33","#009900","#00cc00","#00cc66", "#00ffcc",
                             "#0099ff","#3333cc","#9933ff","#cc00cc","#cc3399","#cc0066",
                             "#cc0000"]) 

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

update_in_progress = False

def readUVvis(fileNumber,experimentNumber,numberFiles_variable):
    global yAxis
    global xAxis
    global Standard_shape
    global update_in_progress
    global yAxisExperimentArray_standardVvis

    fileName =  tkFileDialog.askopenfilename(title='Choose a UV-vis file')
    rawData_1 = np.genfromtxt(str(fileName), delimiter=",")
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
    rawData_1 = np.genfromtxt(str(fileName), delimiter=",")
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
    rawData_1 = np.genfromtxt(str(fileName), delimiter=",")
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
    rawData_1 = np.genfromtxt(str(fileName), delimiter=",")
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

def absVsPLplotStandard(fig,ax1,canvas,numberFiles_variable,excitationWavelength_variable,
       lowerWavelengthStandard_variable,upperWavelengthStandard_variable,
       gradientCurveStandard_variable):
    global absorbanceAtExcitationWavelength_standard
    global PLintegral_standard
    global update_in_progress
    global xAxis
    global yAxis
    global xAxis_standardPL
    global yAxis_standardPL
    global yAxisExperimentArray_standardUVvis
    global yAxisExperimentArray_standardPL
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

def absVsPLplotSample(fig,ax2,canvas,numberFiles_variable,
        excitationWavelength_variableSample,lowerWavelengthSample_variable,
        upperWavelengthSample_variable,gradientCurveSample_variable):
    global absorbanceAtExcitationWavelength_sample
    global PLintegral_sample
    global update_in_progress
    global xAxis
    global yAxis
    global xAxis_samplePL
    global yAxis_samplePL
    global yAxisExperimentArray_sampleUVvis
    global yAxisExperimentArray_samplePL
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

def QYcalculation(variable4,variable7,variable2):
    global popt_standard
    global popt_sample
    global perr_standard
    global perr_sample
    global update_in_progress

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

