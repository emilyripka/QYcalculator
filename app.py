from PyQt5.QtWidgets import QApplication, QMessageBox, qApp
from PyQt5 import QtCore
import sys, ctypes, traceback
from window import Window 

stylesheet = """
QTabWidget::pane{
    background: white;
}
QTabBar::tab{
    width: 100px;
}
QTabBar::tab:selected{
    background: white;
    font-weight: bold;
}
QTabBar::tab:!selected{
    background: #b3b3b3;
}
QGroupBox { 
    border: 1px solid black;
    border-radius: 5px;
    margin-top: 0.5em;
    font-weight: bold;
    font-family: sans-serif;
    font-size: 12px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding-left: 10px;
    padding-right: 10px;
}
"""

def exception_handler(type_, value, traceback_):
    if qApp.thread() is QtCore.QThread.currentThread():
        p = traceback.format_exception(type_, value, traceback_)
        log = ''.join(p)
        msg = QMessageBox()
        msg.setWindowTitle("QYCalculator error")
        msg.setIcon(QMessageBox.Critical)
        msg.setText("An error has occured. For more information, see the log below.")
        msg.setDetailedText(log)
        msg.setEscapeButton(QMessageBox.Ok)
        msg.exec_()
sys.excepthook = exception_handler

if sys.platform == 'win32':
    appID = 'QYCalculatorGUI'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appID)

app = QApplication(sys.argv)
app.setStyleSheet(stylesheet)
window = Window()
sys.exit(app.exec_())
