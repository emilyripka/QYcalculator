r'''Contains functions for reading/plotting UVvis and Fluorescence files,
as well as quantifying relative quantum yields.
'''
import tkFileDialog, tkMessageBox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import scipy as scipy
from scipy import optimize

def readUVvis(update_in_progress,
              fileNumber,
              experimentNumber,
              yAxis,
              xAxis,
              Shape,
              yAxisExperimentArray_UVvis):
    r'''This reads in UVvis files and assigns x- and y- axes to an input array
    for a given experiment nubmer which is also a parameter.
    
    Args:
        update_in_progress (bool): used to update tkinter varaibles
        fileNumber (int): index for file number
        experimentNumber (int): entry box experiment number for plotting/proccessing 
            purposes
        yAxis (array): 2D array to store y-axis values for all files
        xAxis (array): 2D array to store x-axis values for all files 
        Shape (array): 1D array to store length of y-axis
        yAxisExperimentArray_UVvis (array): 1D array to store chosen experiment number
            for future plotting purposes  

    Returns:
        yAxisExperimentArray_UVvis[fileNumber]: entry box experiment number is assigned
            to the index of the yAxisExperimentArray_UVvis at the current file
            number for future plotting/proccessing purposes  
        xAxis[fileNumber][0:xLength]: assigned to the x-axis of the user-selected file 
        yAxis[fileNumber,0:yLength_1,0:yLength_2]: assigned to the y-axis of the 
            user-selected file
        Shape[fileNumber]: assigned to the length of the y-axis of the user-selected file 

    Notes to EGR:
        (1) Why am I using this shape variable? Do I really need it?

    '''

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

    x_Global = np.ones(x_1.shape[0])
    for i in range(x_1.shape[0]):
        x_Global[i] = x_1[i]
    xLength = x_Global.shape[0]
    xAxis[fileNumber] = np.zeros((1000))

    y_Global = np.ones((y_1.shape[0],y_1.shape[1]))
    for i in range(y_1.shape[0]):
        for j in range(y_1.shape[1]):
            y_Global[i,j] = y_1[i,j]
    yLength_1 = y_Global.shape[0]
    yLength_2 = y_Global.shape[1]
    yAxis[fileNumber] = np.zeros((1000,1000))

    update_in_progress = True
    yAxisExperimentArray_UVvis[fileNumber] = expNumber
    xAxis[fileNumber][0:xLength] = x_Global
    yAxis[fileNumber,0:yLength_1,0:yLength_2] = y_Global
    Shape[fileNumber] = int((np.shape(y_1))[1])
    update_in_progress = False

def plotUVvis(fileNumber, 
              experimentNumber,
              fig,
              ax,
              canvas,
              update_in_progress,
              xAxis,
              yAxis,
              colorList,
              yAxisExperimentArray_UVvis,
              Shape):

    if update_in_progress: return
    expNumber = experimentNumber.get()
    length = int(Shape[fileNumber])
    columnNumber = expNumber - 1
    yAxisPlotting = yAxis[fileNumber][columnNumber][:]
    xAxisPlotting = xAxis[fileNumber]

    ax.plot(xAxisPlotting[:length], yAxisPlotting[:length], color=next(colorList))
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("UV-vis Absorbance (a.u.)")
    canvas.show()
    canvas.get_tk_widget().grid(row=4,rowspan=60,column=7,columnspan=60)
    canvas.draw()

    update_in_progress = True
    yAxisExperimentArray_UVvis[fileNumber] = expNumber
    update_in_progress = False

def clearAndPlotUVvis(fileNumber, 
                      experimentNumber,
                      fig,
                      ax,
                      canvas,
                      update_in_progress,
                      xAxis,
                      yAxis,
                      colorList,
                      yAxisExperimentArray_UVvis,
                      Shape):

    if update_in_progress: return
    expNumber = experimentNumber.get()
    length = int(Shape[fileNumber])

    columnNumber = expNumber - 1
    yAxisPlotting = yAxis[fileNumber][columnNumber][:]
    xAxisPlotting = xAxis[fileNumber]

    ax.clear()
    ax.plot(xAxisPlotting[:length], yAxisPlotting[:length], color=next(colorList))
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("UV-vis Absorbance (a.u.)")
    canvas.show()
    canvas.get_tk_widget().grid(row=4,rowspan=60,column=7,columnspan=60)
    canvas.draw()

    update_in_progress = True
    yAxisExperimentArray_UVvis[fileNumber] = expNumber
    update_in_progress = False

def readFluorescence(fileNumber,
                     experimentNumber,
                     yAxis,
                     xAxis,
                     update_in_progress,
                     Shape_Fluorescence,
                     yAxisExperimentArray_Fluorescence):

    if update_in_progress: return
    try:
        expNumber = experimentNumber.get()
    except ValueError:
        return

    fileName =  tkFileDialog.askopenfilename(title='Choose a PL file')
    rawData_1 = np.genfromtxt(str(fileName), delimiter=",")
    rawData_2 = np.delete(rawData_1, list(range(2, rawData_1.shape[1], 2)), axis=1)
    rawData_3 = np.transpose(rawData_2)
    x_1 = rawData_3[0,:]
    y_1 = rawData_3[1:,:]

    x_Global = np.ones(x_1.shape[0])
    for i in range(x_1.shape[0]):
        x_Global[i] = x_1[i]
    xLength = x_Global.shape[0]
    xAxis[fileNumber] = np.zeros((1000))

    y_Global = np.ones((y_1.shape[0],y_1.shape[1]))
    for i in range(y_1.shape[0]):
        for j in range(y_1.shape[1]):
            y_Global[i,j] = y_1[i,j]
    yLength_1 = y_Global.shape[0]
    yLength_2 = y_Global.shape[1]
    yAxis[fileNumber] = np.zeros((1000,1000))

    update_in_progress = True
    xAxis[fileNumber][0:xLength] = x_Global
    yAxisExperimentArray_Fluorescence[fileNumber] = expNumber
    yAxis[fileNumber,0:yLength_1,0:yLength_2] = y_Global
    Shape_Fluorescence[fileNumber] = int((np.shape(y_1))[1])
    update_in_progress = False

def plotFluorescence(fileNumber, 
                     experimentNumber,
                     fig,
                     ax,
                     canvas,
                     update_in_progress,
                     xAxis,
                     yAxis,
                     colorList,
                     yAxisExperimentArray_Fluorescence,
                     Shape_Fluorescence):

    if update_in_progress: return
    try:
        expNumber = experimentNumber.get()
    except ValueError:
        return

    length = int(Shape_Fluorescence[fileNumber])
    columnNumber = expNumber - 1
    yAxisPlotting = yAxis[fileNumber][columnNumber][:]
    xAxisPlotting = xAxis[fileNumber]

    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.plot(xAxisPlotting[:length], yAxisPlotting[:length], color=next(colorList))
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("PL Intensity (a.u.)")
    canvas.show()
    canvas.get_tk_widget().grid(row=4,rowspan=60,column=7,columnspan=60)
    canvas.draw()

    update_in_progress = True
    yAxisExperimentArray_Fluorescence[fileNumber] = expNumber
    update_in_progress = False

def clearAndplotFluorescence(fileNumber, 
                             experimentNumber,
                             fig,
                             ax,
                             canvas,
                             update_in_progress,
                             xAxis,
                             yAxis,
                             colorList,
                             yAxisExperimentArray_Fluorescence,
                             Shape_Fluorescence):

    if update_in_progress: return
    try:
        expNumber = experimentNumber.get()
    except ValueError:
        return

    length = int(Shape_Fluorescence[fileNumber])
    columnNumber = expNumber - 1
    yAxisPlotting = yAxis[fileNumber][columnNumber][:]
    xAxisPlotting = xAxis[fileNumber]

    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.plot(xAxisPlotting[:length], yAxisPlotting[:length], color=next(colorList))
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("PL Intensity (a.u.)")
    canvas.show()
    canvas.get_tk_widget().grid(row=4,rowspan=60,column=7,columnspan=60)
    canvas.draw()

    update_in_progress = True
    yAxisExperimentArray_Fluorescence[fileNumber] = expNumber
    update_in_progress = False

def linear(x,m,b):
    return m*x + b

def UVvis_vs_FluorescencePlot(fig,
                              ax,
                              canvas,
                              nFiles,
                              excitationWavelength_variable,
                              lowerWavelength_variable,
                              upperWavelength_variable,
                              gradientCurve_variable,
                              absorbanceAtExcitationWavelength,
                              FluorescenceIntegral,
                              update_in_progress,
                              xAxis,
                              yAxis,
                              xAxis_Fluorescence,
                              yAxis_Fluorescence,
                              yAxisExperimentArray_UVvis,
                              yAxisExperimentArray_Fluorescence,
                              grad,
                              error): 

    if update_in_progress: return
    try:
        excitationWavelengthEntry = excitationWavelength_variable.get()
        lowerWavelength = lowerWavelength_variable.get()
        upperWavelength = upperWavelength_variable.get()
    except ValueError:
        return

    absorbanceAtExcitationWavelength = np.ones((nFiles))
    excitationWavelengthIndex = 0

    for counter,value in enumerate(xAxis[0]):
        if value == excitationWavelengthEntry:
            excitationWavelengthIndex = counter

    lowerWavelengthIndex = 0
    upperWavelengthIndex = 0
    xAxisEnumerate = xAxis_Fluorescence[0,:]

    for counter,value in enumerate(xAxisEnumerate):
        if value == lowerWavelength:
            lowerWavelengthIndex = counter

    for counter,value in enumerate(xAxisEnumerate):
        if value == upperWavelength:
            upperWavelengthIndex = counter

    for i in range(nFiles):
       absorbanceAtExcitationWavelength[i] = \
                    yAxis[i,(yAxisExperimentArray_UVvis[i]-1),excitationWavelengthIndex]

    PLintegral = np.ones((nFiles))
    for i in range(nFiles):
        PLintegral[i] = np.trapz(yAxis_Fluorescence[i,(yAxisExperimentArray_Fluorescence[i]-1),lowerWavelengthIndex:upperWavelengthIndex])

    ax.plot(absorbanceAtExcitationWavelength, PLintegral, "ro")
    ax.set_xlabel("Absorbance at Excitation Wavelength", family="serif",  fontsize=10)
    ax.set_ylabel("Area Under Fluorescence Curve", family="serif", fontsize=10)
    popt_local, pcov_local = scipy.optimize.curve_fit(linear, absorbanceAtExcitationWavelength,PLintegral, p0=[(2e8/0.0225),0])
    perr_local = np.sqrt(np.diag(pcov_local))

    ax.plot(absorbanceAtExcitationWavelength, linear(absorbanceAtExcitationWavelength, *popt_local),"k-")
    gradientCurve_variable.set((perr_local[0]/popt_local[0])*100)
    canvas.show()
    canvas.get_tk_widget().grid(row=13,rowspan=59,column=0,columnspan=60)
    canvas.draw()

    update_in_progress = True
    grad[0] = popt_local[0] 
    error[0] = perr_local[0] 
    update_in_progress = False

def QYcalculation(RI_standard,
                  RI_sample,
                  QY_standard,
                  grad_standard,
                  grad_sample,
                  error_standard,
                  error_sample,
                  QYsample_variable,
                  QYsample_error_variable,
                  update_in_progress):

    if update_in_progress: return
    try:
        RI_standardEntry = RI_standard.get()
        RI_sampleEntry = RI_sample.get()
        QY_standardEntry = QY_standard.get()
    except ValueError:
        return

    QY_sample = 100*((QY_standardEntry*0.01)*(grad_sample[0]/grad_standard[0])*((RI_sampleEntry**2)/(RI_standardEntry**2)))
    QY_sample_error = (abs(QY_sample)*np.sqrt(((error_sample[0]/grad_sample[0])**2)+((error_standard[0]/grad_standard[0])**2)))

    update_in_progress = True
    QYsample_variable.set(QY_sample)
    QYsample_error_variable.set(QY_sample_error)
    update_in_progress = False