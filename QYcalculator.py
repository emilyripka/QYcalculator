r'''
 emilygraceripka.com - Quantum Yield Calculator                                           
                                                                                          
 License                                                                                 
 -------                                                                                  

 Notes from EGR 
 -------------- 
 I developed this application to help nanoscientists easily calculate relative
 Quantum Yields from their data. Although the calculation for this value is quite
 simple, getting the varaibles from your data to input into this calculation can be
 quite tedious, especially if you are not using a programming language. Thus, this GUI
 will allow researchers to select the standard and sample files, visualize the UV-vis 
 and fluorescence data, and then calculate their quantum yield with errors, as well as 
 making sure that the errors on the gradient curves are within the desired value.
 
 Future Plans
 ------------ 
 (1) Add solvent selection menus which automatically update refractive index values
 (2) Add standard selection menu which automatically updates reference QY
 
 Author
 ------ 
 Blog: www.emilygraceripka.com
 Instagram: emilygraceripka
 
 Last Updated: 2019-01-01 
'''

import sys
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
import QYcalculator_functions as QYCfunc

# Misc variables
update_in_progress = False
nFiles_Standard = int(sys.argv[1])
nFiles_Sample = int(sys.argv[2])
maxLength = 1000

# Standard global variables
xAxis = np.empty((nFiles_Standard,maxLength))
yAxis = np.empty((nFiles_Standard,maxLength,maxLength))
yAxisExperimentArray_standardUVvis = [int(x) for x in range(nFiles_Standard)]
xAxis_standardPL = np.empty((nFiles_Standard,maxLength))
yAxis_standardPL = np.empty((nFiles_Standard,maxLength,maxLength))
yAxisExperimentArray_standardPL = [int(x) for x in range(nFiles_Standard)]
   
# Sample global variables
xAxisUVvisSample = np.empty((nFiles_Sample,maxLength))
yAxisUVvisSample = np.empty((nFiles_Sample,maxLength,maxLength))
yAxisExperimentArray_sampleUVvis = [int(x) for x in range(nFiles_Sample)]
xAxis_samplePL = np.empty((nFiles_Sample,maxLength))
yAxis_samplePL = np.empty((nFiles_Sample,maxLength,maxLength))
yAxisExperimentArray_samplePL = [int(x) for x in range(nFiles_Sample)]

# QY calculation variables
absorbanceAtExcitationWavelength_standard = np.ones((nFiles_Standard))
absorbanceAtExcitationWavelength_sample = np.ones((nFiles_Sample))
PLintegral_standard = np.ones((nFiles_Standard))
PLintegral_sample = np.ones((nFiles_Sample))
grad_standard = [int(x) for x in range(1)]
grad_sample = [int(x) for x in range(1)] 
error_standard = [int(x) for x in range(1)]
error_sample = [int(x) for x in range(1)] 

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
    ax1Grad.set_title("Standard Gradient Curve")
    ax2Grad.set_title("Sample Gradient Curve")
    canvasGrad = FigureCanvasTkAgg(figGrad, page3)

    # Rainbow
    colorList = itertools.cycle(["#ff0000","#ff3300","#ff6600","#ff9900","#ffcc00","#ffff00",
                                 "#ccff33","#99ff33","#009900","#00cc00","#00cc66", "#00ffcc",
                                 "#0099ff","#3333cc","#9933ff","#cc00cc","#cc3399","#cc0066",
                                 "#cc0000"]) 
    
    # Standard
    # Variables
    expNo = np.array([tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()])
    expNo_standardPL = np.array([tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()])
    QY_standard = tk.IntVar()
    RI_standard = tk.DoubleVar()
    excitationWavelength_variable = tk.DoubleVar()
    lowerWavelengthStandard_variable = tk.DoubleVar()
    upperWavelengthStandard_variable = tk.DoubleVar()

    # Labels
    tk.Label(page1,text="Standard Fluorescence").grid(row=14,column=0,columnspan=6)
    tk.Label(page1, text="QY (%):").grid(row=1,column=33,columnspan=12,sticky="E")
    tk.Label(page1, text="Refractive Index:").grid(row=2,column=33,columnspan=12,sticky="E")
    tk.Label(page1,text="Excitation Wavelength (nm):").grid(row=0,column=7,columnspan=5,sticky="e")
    tk.Label(page1,text="Lower Integration Wavelength (nm):").grid(row=1,column=7,columnspan=5,sticky="e")
    tk.Label(page1,text="Upper Integration Wavelength (nm):").grid(row=2,column=7,columnspan=5,sticky="e")

    # Entry boxes
    tk.Entry(page1, textvariable=QY_standard,width=4).grid(row=1,column=46,columnspan=5,sticky="W")
    tk.Entry(page1,textvariable=RI_standard,width=5).grid(row=2,column=46,columnspan=5,sticky="W")
    tk.Entry(page1,textvariable=excitationWavelength_variable,width=4).grid(row=0, column=13, sticky="w")
    tk.Entry(page1,textvariable=lowerWavelengthStandard_variable,width=4).grid(row=1, column=13, sticky="w")
    tk.Entry(page1,textvariable=upperWavelengthStandard_variable,width=4).grid(row=2, column=13, sticky="w")

    # Buttons w/ labels and entry boxes
    for i in range(nFiles_Standard):
        thisText_i = i+1

        # Standard UV-vis
        thisText = ('File #%d:' % thisText_i) 
        tk.Label(page1,text=thisText).grid(row=i+1,column=0) 
        tk.Button(page1,bg=myGreen,text="Browse",command=lambda i=i:QYCfunc.readFile(
            update_in_progress=update_in_progress,
            fileNumber=i,
            experimentNumber=expNo[i],
            yAxis=yAxis,
            xAxis=xAxis,
            yAxisExperimentArray=yAxisExperimentArray_standardUVvis,
            maxLength=maxLength
            )).grid(row=i+1,column=1)
        thisText = ('Experiment #%d:' % thisText_i)
        tk.Label(page1,text=thisText).grid(row=i+1,column=3)
        tk.Entry(page1,textvariable=expNo[i],width=4).grid(row=i+1,column=4)
        tk.Button(page1,bg=myGreen,text="Plot",command=lambda i=i:QYCfunc.plotExperiment(
            fileNumber=i,
            experimentNumber=expNo[i],
            fig=fig,
            ax=ax1,
            canvas=canvas,
            update_in_progress=update_in_progress,
            xAxis=xAxis,
            yAxis=yAxis,
            colorList=colorList,
            yAxisExperimentArray=yAxisExperimentArray_standardUVvis,
            clearPlot=False
            )).grid(row=i+1,column=5)
        tk.Button(page1,bg=myGreen,text="Clear&Plot",command=lambda i=i:QYCfunc.plotExperiment(
            fileNumber=i,
            experimentNumber=expNo[i],
            fig=fig,
            ax=ax1,
            canvas=canvas,
            update_in_progress=update_in_progress,
            xAxis=xAxis,
            yAxis=yAxis,
            colorList=colorList,
            yAxisExperimentArray=yAxisExperimentArray_standardUVvis,
            clearPlot=True
            )).grid(row=i+1,column=6)

        # Standard fluorescence
        thisText = ('File #%d:' % thisText_i)
        tk.Label(page1,text=thisText).grid(row=i+15,column=0) 
        tk.Button(page1,bg=myGreen,text="Browse",command=lambda i=i:QYCfunc.readFile(
            update_in_progress=update_in_progress,
            fileNumber=i,
            experimentNumber=expNo_standardPL[i],
            yAxis=yAxis_standardPL,
            xAxis=xAxis_standardPL,
            yAxisExperimentArray=yAxisExperimentArray_standardPL,
            maxLength=maxLength 
            )).grid(row=i+15,column=1)
        thisText = ('Experiment #%d:' % thisText_i)
        tk.Label(page1,text=thisText).grid(row=i+15,column=3)
        tk.Entry(page1,textvariable=expNo_standardPL[i],width=4).grid(row=i+15,column=4)
        tk.Button(page1,bg=myGreen,text="Plot",command=lambda i=i:QYCfunc.plotExperiment(
            fileNumber=i,
            experimentNumber=expNo_standardPL[i],
            fig=fig,
            ax=ax2,
            canvas=canvas,
            update_in_progress=update_in_progress,
            xAxis=xAxis_standardPL,
            yAxis=yAxis_standardPL,
            colorList=colorList,
            yAxisExperimentArray=yAxisExperimentArray_standardPL,
            clearPlot=False 
            )).grid(row=i+15,column=5)
        tk.Button(page1,bg=myGreen,text="Clear&Plot",command=lambda i=i:QYCfunc.plotExperiment(
            fileNumber=i,
            experimentNumber=expNo_standardPL[i],
            fig=fig,
            ax=ax2,
            canvas=canvas,
            update_in_progress=update_in_progress,
            xAxis=xAxis_standardPL,
            yAxis=yAxis_standardPL,
            colorList=colorList,
            yAxisExperimentArray=yAxisExperimentArray_standardPL,
            clearPlot=True 
            )).grid(row=i+15,column=6)

    # Sample
    # Variables
    expNo_sample = np.array([tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()])
    expNo_samplePL = np.array([tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()])
    excitationWavelength_variableSample = tk.DoubleVar()
    lowerWavelengthSample_variable = tk.DoubleVar()
    upperWavelengthSample_variable = tk.DoubleVar()
    RI_sample = tk.DoubleVar()

    # Labels
    tk.Label(page2, text="Sample Fluorescence").grid(row=14,column=0,columnspan=6)
    tk.Label(page2,text="Excitation Wavelength (nm):").grid(row=0,column=7,columnspan=5,sticky="e")
    tk.Label(page2,text="Lower Integration Wavelength for Sample (nm):").grid(row=1,column=7,columnspan=5,sticky="e")
    tk.Label(page2,text="Upper Integration Wavelength for Sample (nm):").grid(row=2,column=7,columnspan=5,sticky="e")
    ttk.Label(page2, text="Refractive Index:").grid(row=2,column=33,columnspan=10,sticky="E")

    # Entry boxes
    tk.Entry(page2,textvariable=excitationWavelength_variableSample,width=4).grid(row=0, column=13, sticky="w")
    tk.Entry(page2,textvariable=lowerWavelengthSample_variable,width=4).grid(row=1, column=13, sticky="w")
    tk.Entry(page2,textvariable=upperWavelengthSample_variable,width=4).grid(row=2, column=13, sticky="w")
    ttk.Entry(page2,textvariable=RI_sample,width=5).grid(row=2,column=44,columnspan=5,sticky="W")

    # Buttons w/ labels and entry boxes
    for i in range(nFiles_Sample):
        thisText_i = i+1

        # Sample UV-vis
        thisText = ('File #%d:' % thisText_i) 
        tk.Label(page2,text=thisText).grid(row=i+1,column=0) 
        tk.Button(page2,bg=myGreen,text="Browse",command=lambda i=i:QYCfunc.readFile(
            update_in_progress=update_in_progress,
            fileNumber=i,
            experimentNumber=expNo_sample[i],
            yAxis=yAxisUVvisSample,
            xAxis=xAxisUVvisSample,
            yAxisExperimentArray=yAxisExperimentArray_sampleUVvis,
            maxLength=maxLength 
            )).grid(row=i+1,column=1)
        thisText = ('Experiment #%d:' % thisText_i)
        tk.Label(page2,text=thisText).grid(row=i+1,column=3)
        tk.Entry(page2,textvariable=expNo_sample[i],width=4).grid(row=i+1,column=4)
        tk.Button(page2,bg=myGreen,text="Plot",command=lambda i=i:QYCfunc.plotExperiment(
            fileNumber=i,
            experimentNumber=expNo_sample[i],
            fig=figSample,
            ax=ax1Sample,
            canvas=canvasSample,
            update_in_progress=update_in_progress,
            xAxis=xAxisUVvisSample,
            yAxis=yAxisUVvisSample,
            colorList=colorList,
            yAxisExperimentArray=yAxisExperimentArray_sampleUVvis,
            clearPlot=False
            )).grid(row=i+1,column=5)
        tk.Button(page2,bg=myGreen,text="Clear&Plot",command=lambda i=i:QYCfunc.plotExperiment(
            fileNumber=i,
            experimentNumber=expNo_sample[i],
            fig=figSample,
            ax=ax1Sample,
            canvas=canvasSample,
            update_in_progress=update_in_progress,
            xAxis=xAxisUVvisSample,
            yAxis=yAxisUVvisSample,
            colorList=colorList,
            yAxisExperimentArray=yAxisExperimentArray_sampleUVvis,
            clearPlot=True
            )).grid(row=i+1,column=6)   

        # Sample fluorescence
        thisText = ('File #%d:' % thisText_i)
        tk.Label(page2,text=thisText).grid(row=i+15,column=0) 
        tk.Button(page2,bg=myGreen,text="Browse",command=lambda i=i:QYCfunc.readFile(
            update_in_progress=update_in_progress,
            fileNumber=i,
            experimentNumber=expNo_samplePL[i],
            yAxis=yAxis_samplePL,
            xAxis=xAxis_samplePL,
            yAxisExperimentArray=yAxisExperimentArray_samplePL,
            maxLength=maxLength 
            )).grid(row=i+15,column=1)
        thisText = ('Experiment #%d:' % thisText_i)
        tk.Label(page2,text=thisText).grid(row=i+15,column=3)
        tk.Entry(page2,textvariable=expNo_samplePL[i],width=4).grid(row=i+15,column=4)
        tk.Button(page2,bg=myGreen,text="Plot",command=lambda i=i:QYCfunc.plotExperiment(
            fileNumber=i,
            experimentNumber=expNo_samplePL[i],
            fig=figSample,
            ax=ax2Sample,
            canvas=canvasSample,
            update_in_progress=update_in_progress,
            xAxis=xAxis_samplePL,
            yAxis=yAxis_samplePL,
            colorList=colorList,
            yAxisExperimentArray=yAxisExperimentArray_samplePL,
            clearPlot=False 
            )).grid(row=i+15,column=5)
        tk.Button(page2,bg=myGreen,text="Clear&Plot",command=lambda i=i:QYCfunc.plotExperiment(
            fileNumber=i,
            experimentNumber=expNo_samplePL[i],
            fig=figSample,
            ax=ax2Sample,
            canvas=canvasSample,
            update_in_progress=update_in_progress,
            xAxis=xAxis_samplePL,
            yAxis=yAxis_samplePL,
            colorList=colorList,
            yAxisExperimentArray=yAxisExperimentArray_samplePL,
            clearPlot=True
            )).grid(row=i+15,column=6)

    # Results Page 
    # Variables
    gradientCurveStandard_variable = tk.DoubleVar()
    gradientCurveSample_variable = tk.DoubleVar()
    QYsample_variable = tk.DoubleVar()
    QYsample_error_variable = tk.DoubleVar()

    # Labels
    ttk.Label(page3,text="Standard slope error (%):").grid(row=10,column=4,columnspan=4,sticky="E")
    ttk.Label(page3,text="Sample slope error (%):").grid(row=11,column=4,columnspan=4,sticky="E")
    ttk.Label(page3, text="QY (%):").grid(row=75,column=4,columnspan=1,sticky="e")
    ttk.Label(page3, text="+/-").grid(row=75,column=6,columnspan=1,sticky="e")
 
    # Entry boxes 
    ttk.Entry(page3,textvariable=gradientCurveStandard_variable,width=4).grid(row=10,column=8,columnspan=1,sticky=tk.E+tk.W)
    ttk.Entry(page3,textvariable=gradientCurveSample_variable,width=4).grid(row=11,column=8,columnspan=1,sticky=tk.E+tk.W)
    ttk.Entry(page3, textvariable=QYsample_variable,width=4).grid(row=75,column=5,columnspan=1,sticky=tk.E+tk.W)
    ttk.Entry(page3, textvariable=QYsample_error_variable,width=4).grid(row=75,column=7,columnspan=1,sticky=tk.E+tk.W)  

    # Standard Gradient curve button
    tk.Button(page3,bg=myGreen,text="Standard Gradient Curve", command=lambda:QYCfunc.UVvis_vs_FluorescencePlot(
        fig=figGrad,
        ax=ax1Grad,
        canvas=canvasGrad,
        nFiles=nFiles_Standard,
        excitationWavelength_variable=excitationWavelength_variable,
        lowerWavelength_variable=lowerWavelengthStandard_variable,
        upperWavelength_variable=upperWavelengthStandard_variable,
        gradientCurve_variable=gradientCurveStandard_variable,
        absorbanceAtExcitationWavelength=absorbanceAtExcitationWavelength_standard,
        FluorescenceIntegral=PLintegral_standard,
        update_in_progress=update_in_progress,
        xAxis=xAxis,
        yAxis=yAxis,
        xAxis_Fluorescence=xAxis_standardPL,
        yAxis_Fluorescence=yAxis_standardPL,
        yAxisExperimentArray_UVvis=yAxisExperimentArray_standardUVvis,
        yAxisExperimentArray_Fluorescence=yAxisExperimentArray_standardPL,
        grad=grad_standard,
        error=error_standard
        )).grid(row=10,column=0,columnspan=4)

    # Sample Gradient curve button
    tk.Button(page3,bg=myGreen,text="Sample Gradient Curve",command=lambda:QYCfunc.UVvis_vs_FluorescencePlot(
        fig=figGrad,
        ax=ax2Grad,
        canvas=canvasGrad,
        nFiles=nFiles_Sample,
        excitationWavelength_variable=excitationWavelength_variableSample,
        lowerWavelength_variable=lowerWavelengthSample_variable,
        upperWavelength_variable=upperWavelengthSample_variable,
        gradientCurve_variable=gradientCurveSample_variable,
        absorbanceAtExcitationWavelength=absorbanceAtExcitationWavelength_sample,
        FluorescenceIntegral=PLintegral_sample,
        update_in_progress=update_in_progress,
        xAxis=xAxisUVvisSample, 
        yAxis=yAxisUVvisSample, 
        xAxis_Fluorescence=xAxis_samplePL,
        yAxis_Fluorescence=yAxis_samplePL,
        yAxisExperimentArray_UVvis=yAxisExperimentArray_sampleUVvis,
        yAxisExperimentArray_Fluorescence=yAxisExperimentArray_samplePL,
        grad=grad_sample,
        error=error_sample
        )).grid(row=11,column=0,columnspan=4)

    # QY calculation button
    tk.Button(page3,bg=myGreen,text="Sample QY Calculation",command=lambda:QYCfunc.QYcalculation(
        RI_standard=RI_standard,
        RI_sample=RI_sample,
        QY_standard=QY_standard,
        grad_standard=grad_standard,
        grad_sample=grad_sample,
        error_standard=error_standard,
        error_sample=error_sample,
        QYsample_variable=QYsample_variable,
        QYsample_error_variable=QYsample_error_variable,
        update_in_progress=update_in_progress 
        )).grid(row=75,column=0,columnspan=4)

    # Information page
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

    nb.grid(row=0,column=0)
    root.mainloop()

if __name__ == "__main__":
    QYcalculator()
