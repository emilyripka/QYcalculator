# QYcalculator
Python-tkinter application for calculating fluorescence quantum yield via the comparative method.<sup>1</sup> See <a href="http://emilygraceripka.com/blog/17">corresponding blog post</a> for further details.

### Dependencies:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->Python 2.7 <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->NumPy  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->matplotlib 2 <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->SciPy <br>

## How-To Guide
First, launch the application from your terminal by navigating to your cloned directory, and entering the following (where the command line arguments are two integers, the first for the number of standard experiments, and the second for the number of sample experiments):
```
$ python QYcalculator.py # #
```

### (I) Standard (navigate to 'Standard' tab)
(i) Enter number of UV-vis measurements made for the QY measurement <br>
(ii) Select files for each UV-vis measurement and enter the experiment number of that measurement file. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>***This data was likely stored in one of two ways:</i> <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(a) all UV-vis measurements were collected, and then all scans were saved to <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;the same file as different scans (i.e. experiment number) <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(b) after each UV-vis measurement, the scan was saved as a new file <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>***It will be helpful to use the 'Plot' and 'Clear&Plot' buttons to visualize which experiment your measurement is</i> <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>***Make sure to keep the 'Experiment #' as the desired value before proceeding.</i> <br>
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
