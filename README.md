# QYcalculator
Python-tkinter application for calculating fluorescence quantum yield via the comparative method.<sup>1</sup>

## How-To Guide
### (I) Standard (navigate to 'Standard' tab)
(i) Enter number of UV-vis measurements made for the QY measurement 
(ii) Select files for each UV-vis measurement and enter the experiment number of that measurement file. <br>
<i>This data was likely stored in one of two ways:</i> <br>
(a) all UV-vis measurements were collected, and then all scans were saved to the same file as different scans (i.e. experiment number) <br>
(b) after each UV-vis measurement, the scan was saved as a new file <br>
<i>It will be helpful to use the 'Plot' and 'Clear&Plot' buttons to visualize which experiment your measurement is <br>
<i>Make sure to keep the 'Experiment #' as the desired value before proceeding.</i> <br>
(iii) Repeat step (ii) for the fluorescence measurments. <br> 
(iii) Repeat step (ii) for the fluorescence measurments. <br>
(iv) Fill in the blanks at the top-right of the tab. <br>
(v) Navigate to the Results tab, and click the 'Standard Gradient Curve' button. <br>
<i>The printed 'Standard slope error (%)' needs to be less than 10% to be an accurate standard gradient curve.</i> <br>
### (II) Sample (navigate to 'Sample' tab)
(i) Repeat Standard steps (i) through (iv) <br>
(ii) Navigate to the Results tab, and click the 'Sample Gradient Curve' button. <br>
<i>The printed 'Sample slope error (%)' needs to be less than 10% to be an accurate sample gradient curve.</i> <br>
### (III) QY calculation (navigate to the 'Results' tab)
(i) Click the 'Sample QY Calculation' button <br>

## References
(1) A. T. R. Williams, S. A. Winfield, and J. N. Miller. Relative fluorescence quantum yields using a computer controlled luminescence spectrometer. <i>Analyst</i>, <b>1983</b>, <i>108</i>, 1067. 
