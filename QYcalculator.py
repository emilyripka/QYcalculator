###########################################################################################
# emilygraceripka.com - Quantum Yield Calculator                                           
#                                                                                          
# License                                                                                 
# -------                                                                                  
#
# Notes from EGR 
# -------------- 
# I developed this application to help nanoscientists easily calculate relative
# Quantum Yields from their data. Although the calculation for this value is quite
# simple, getting the varaibles from your data to input into this calculation can be
# quite tedious, especially if you are not using a programming language. Thus, this GUI
# will allow researchers to select the standard and sample files, visualize the UV-vis 
# and fluorescence data, and then calculate their quantum yield with errors, as well as 
# making sure that the errors on the gradient curves are within the desired value.
# 
# Future Plans
# ------------ 
# (1) Add solvent selection menus which automatically update refractive index values
# (2) Add standard selection menu which automatically updates reference QY
# 
# Author
# ------ 
# Blog: www.emilygraceripka.com
# Instagram: emilygraceripka
# 
# Last Updated: 2018-12-29 
###########################################################################################
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
###########################################################################################
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
    ######################################################################################
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
    # Number of sample files optional CLA
    nFiles_startStandard = int(sys.argv[1])
    # Number of sample files optional CLA
    nFiles_startSample = int(sys.argv[2])
    ######################################################################################
    # Standard Figure
    fig = Figure(figsize=(10,4), dpi=100)
    gs = gridspec.GridSpec(1, 2)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    canvas = FigureCanvasTkAgg(fig, page1)
    ######################################################################################
    # Sample Figure
    figSample = Figure(figsize=(10,4), dpi=100)
    gsSample = gridspec.GridSpec(1, 2)
    ax1Sample = figSample.add_subplot(gsSample[0])
    ax2Sample = figSample.add_subplot(gsSample[1])
    canvasSample = FigureCanvasTkAgg(figSample, page2)
    ######################################################################################
    # Gradient Curve Figures
    figGrad = Figure(figsize=(10,4), dpi=100)
    gsGrad = gridspec.GridSpec(1, 2)
    ax1Grad = figGrad.add_subplot(gsGrad[0])
    ax2Grad = figGrad.add_subplot(gsGrad[1])
    canvasGrad = FigureCanvasTkAgg(figGrad, page3)
    ######################################################################################
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
    ######################################################################################
    # Standard
    numberFilesVariableStandard = tk.IntVar()
    numberFilesVariableStandard.set(int(sys.argv[1]))
    #tk.Label(page1, text="Number of UV-vis files for standard (1-10):").grid(row=0,column=0,columnspan=6)
    #tk.Entry(page1, textvariable=numberFilesVariableStandard,width=4).grid(row=0, column=6)
    tk.Label(page1,text="Standard Fluorescence").grid(row=14,column=0,columnspan=6)
    expNo = np.array([tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()])
    expNo_standardPL = np.array([tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()])
    ## Standard compound choice menu
    #tk.Label(page1, text="Compound:").grid(row=1,column=19,columnspan=1,sticky="E")
    #variable = tk.StringVar()
    #variable.set("Rhodamine 6G") # default value
    #ttk.OptionMenu(page1,variable,"Rhodamine 6G","Rhodamine 6G","Standard #2", "Standard #3").grid(row=1,column=21,columnspan=10,sticky="W")
    # Standard compound QY entry box
    tk.Label(page1, text="QY (%):").grid(row=1,column=33,columnspan=12,sticky="E")
    variable2 = tk.IntVar()
    tk.Entry(page1, textvariable=variable2,width=4).grid(row=1,column=46,columnspan=5,sticky="W")
    ## Standard solvent selection optionmenu
    #tk.Label(page1, text="Solvent:").grid(row=2,column=19,columnspan=1,sticky="E")
    #variable3 = tk.StringVar()
    #variable3.set("ethanol") # default value
    #ttk.OptionMenu(page1,variable3,"ethanol","ethanol","methanol","butanol","acetone","toluene","hexane").grid(row=2,column=21,columnspan=10,sticky="W")
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
    for i in range(nFiles_startStandard):
        thisText_i = i+1
        # Standard UV-vis
        thisText = ('File #%d:' % thisText_i) 
        tk.Label(page1,text=thisText).grid(row=i+1,column=0) 
        tk.Button(page1,bg=myGreen,text="Browse",command=lambda i=i:QYCfunc.readUVvis(fileNumber=i,experimentNumber=expNo[i],
            numberFiles_variable=numberFilesVariableStandard)).grid(row=i+1,column=1)
        thisText = ('Experiment #%d:' % thisText_i)
        tk.Label(page1,text=thisText).grid(row=i+1,column=3)
        tk.Entry(page1,textvariable=expNo[i],width=4).grid(row=i+1,column=4)
        tk.Button(page1,bg=myGreen,text="Plot",command=lambda i=i:QYCfunc.plotUVvis(fileNumber=i,experimentNumber=expNo[i],
            fig=fig,ax1=ax1,canvas=canvas)).grid(row=i+1,column=5)
        tk.Button(page1,bg=myGreen,text="Clear&Plot",command=lambda i=i:QYCfunc.clearAndPlotUVvis(fileNumber=i,experimentNumber=expNo[i],
            fig=fig,ax1=ax1,canvas=canvas)).grid(row=i+1,column=6)
        # Standard fluorescence
        thisText = ('File #%d:' % thisText_i)
        tk.Label(page1,text=thisText).grid(row=i+15,column=0) 
        tk.Button(page1,bg=myGreen,text="Browse",command=lambda i=i:QYCfunc.readPLstandard(fileNumber=i,experimentNumber=expNo_standardPL[i],
            numberFiles_variable=numberFilesVariableStandard)).grid(row=i+15,column=1)
        thisText = ('Experiment #%d:' % thisText_i)
        tk.Label(page1,text=thisText).grid(row=i+15,column=3)
        tk.Entry(page1,textvariable=expNo_standardPL[i],width=4).grid(row=i+15,column=4)
        tk.Button(page1,bg=myGreen,text="Plot",command=lambda i=i:QYCfunc.plotPLstandard(fileNumber=i,experimentNumber=expNo_standardPL[i],
            fig=fig,ax2=ax2,canvas=canvas)).grid(row=i+15,column=5)
        tk.Button(page1,bg=myGreen,text="Clear&Plot",command=lambda i=i:QYCfunc.clearAndPlotPLstandard(fileNumber=i,experimentNumber=expNo_standardPL[i],
            fig=fig,ax2=ax2,canvas=canvas)).grid(row=i+15,column=6)
    ######################################################################################
    # Sample
    numberFilesVariableSample = tk.IntVar()
    numberFilesVariableSample.set(int(sys.argv[2]))
    #tk.Label(page2, text="Number of UV-vis files for sample (1-10):").grid(row=0,column=0,columnspan=6)
    #tk.Entry(page2, textvariable=numberFilesVariableSample,width=4).grid(row=0, column=6)
    tk.Label(page2, text="Sample Fluorescence").grid(row=14,column=0,columnspan=6)
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
    ## Sample compound selection menu
    #ttk.Label(page2, text="Compound:").grid(row=1,column=19,columnspan=1,sticky="E")
    #variable8 = tk.StringVar()
    #variable8.set("unknown") # default value
    #ttk.OptionMenu(page2,variable8,"CsPbBr3","CsPbBr3","CsPbCl3", "CsPbI3").grid(row=1,column=21,columnspan=10,sticky="W")
    ##  Sample solvent selection optionmenu
    #ttk.Label(page2, text="Solvent:").grid(row=2,column=19,columnspan=1,sticky="E")
    #variable6 = tk.StringVar()
    #variable6.set("toluene") # default value
    #ttk.OptionMenu(page2,variable6,"toluene",'toluene',"hexane","ethanol","methanol","butanol","acetone").grid(row=2,column=21,columnspan=10,sticky="W")
    # Sample solvent refractive index entry box
    ttk.Label(page2, text="Refractive Index:").grid(row=2,column=33,columnspan=10,sticky="E")
    variable7 = tk.DoubleVar()
    ttk.Entry(page2,textvariable=variable7,width=5).grid(row=2,column=44,columnspan=5,sticky="W")
    for i in range(nFiles_startSample):
        thisText_i = i+1
        # Sample UV-vis
        thisText = ('File #%d:' % thisText_i) 
        tk.Label(page2,text=thisText).grid(row=i+1,column=0) 
        tk.Button(page2,bg=myGreen,text="Browse",command=lambda i=i:QYCfunc.readUVvisSample(fileNumber=i,experimentNumber=expNo_sample[i],
            numberFiles_variable=numberFilesVariableSample)).grid(row=i+1,column=1)
        thisText = ('Experiment #%d:' % thisText_i)
        tk.Label(page2,text=thisText).grid(row=i+1,column=3)
        tk.Entry(page2,textvariable=expNo_sample[i],width=4).grid(row=i+1,column=4)
        tk.Button(page2,bg=myGreen,text="Plot",command=lambda i=i:QYCfunc.plotUVvisSample(fileNumber=i,experimentNumber=expNo_sample[i],
            fig=figSample,ax1=ax1Sample,canvas=canvasSample)).grid(row=i+1,column=5)
        tk.Button(page2,bg=myGreen,text="Clear&Plot",command=lambda i=i:QYCfunc.clearAndPlotUVvisSample(fileNumber=i,experimentNumber=expNo_sample[i],
            fig=figSample,ax1=ax1Sample,canvas=canvasSample)).grid(row=i+1,column=6)   
        # Sample fluorescence
        thisText = ('File #%d:' % thisText_i)
        tk.Label(page2,text=thisText).grid(row=i+15,column=0) 
        tk.Button(page2,bg=myGreen,text="Browse",command=lambda i=i:QYCfunc.readPLsample(fileNumber=i,experimentNumber=expNo_samplePL[i],
            numberFiles_variable=numberFilesVariableSample)).grid(row=i+15,column=1)
        thisText = ('Experiment #%d:' % thisText_i)
        tk.Label(page2,text=thisText).grid(row=i+15,column=3)
        tk.Entry(page2,textvariable=expNo_samplePL[i],width=4).grid(row=i+15,column=4)
        tk.Button(page2,bg=myGreen,text="Plot",command=lambda i=i:QYCfunc.plotPLsample(fileNumber=i,experimentNumber=expNo_samplePL[i],
            fig=figSample,ax2=ax2Sample,canvas=canvasSample)).grid(row=i+15,column=5)
        tk.Button(page2,bg=myGreen,text="Clear&Plot",command=lambda i=i:QYCfunc.clearAndPlotPLsample(fileNumber=i,experimentNumber=expNo_samplePL[i],
            fig=figSample,ax2=ax2Sample,canvas=canvasSample)).grid(row=i+15,column=6)
    ######################################################################################
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
    tk.Button(page3,bg=myGreen,text="Standard Gradient Curve", command=lambda:QYCfunc.absVsPLplotStandard(fig=figGrad,
               ax1=ax1Grad,
               canvas=canvasGrad,
               numberFiles_variable=numberFilesVariableStandard,
               excitationWavelength_variable=excitationWavelength_variable,
               lowerWavelengthStandard_variable=lowerWavelengthStandard_variable,
               upperWavelengthStandard_variable=upperWavelengthStandard_variable,
               gradientCurveStandard_variable=gradientCurveStandard_variable  
               )).grid(row=10,column=0,columnspan=4)
    tk.Button(page3,bg=myGreen,text="Sample Gradient Curve",command=lambda:QYCfunc.absVsPLplotSample(fig=figGrad,
          ax2=ax2Grad,
          canvas=canvasGrad,
          numberFiles_variable=numberFilesVariableSample,
          excitationWavelength_variableSample=excitationWavelength_variableSample,
          lowerWavelengthSample_variable=lowerWavelengthSample_variable,
          upperWavelengthSample_variable=upperWavelengthSample_variable,
          gradientCurveSample_variable=gradientCurveSample_variable)).grid(row=11,column=0,columnspan=4)
    tk.Button(page3,bg=myGreen,text="Sample QY Calculation",command=lambda:QYCfunc.QYcalculation(variable4=variable4,
      variable7=variable7,
      variable2=variable2)).grid(row=75,column=0,columnspan=4)

    nb.grid(row=0,column=0)
    root.mainloop()

if __name__ == "__main__":
    QYcalculator()
