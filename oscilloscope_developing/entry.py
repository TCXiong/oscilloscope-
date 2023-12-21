import mainWindow 
import setParameter as sp
import measure as ms
import waveform_plot as wp
import pyvisa as visa

from PyQt5.Qt import *
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import webbrowser
import sys


class InfoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('info.ui', self)

        # manual button
        self.dev_manual.clicked.connect(self.dev_btn_callback)
        self.user_manual.clicked.connect(self.usr_btn_callback)
        # contribution
        self.contri.clicked.connect(self.contribution_btn_callback)
        # source code
        self.source.clicked.connect(self.source_btn_callback)
        # self.test_btn.clicked.connect(self.test_btn_callback)

        # connection source input
        self.check.clicked.connect(self.check_btn_callback)
        self.address.setText("USB0::0x2A8D::0x9009::MY53120104::INSTR")
        self.address.returnPressed.connect(self.check_btn_callback)


    def usr_btn_callback(self):
        url = 'file:///C:/Users/seung-jin%20orr/OneDrive%20-%20STMicroelectronics/Desktop/qt_test/user.html'
        webbrowser.open(url)


    def dev_btn_callback(self):
        url = 'file:///C:/Users/seung-jin%20orr/OneDrive%20-%20STMicroelectronics/Desktop/qt_test/developer.html'
        webbrowser.open(url)

    
    def contribution_btn_callback(self):
        url = 'https://gist.githubusercontent.com/tiancheng-st/b3c58a6af3641719d21cbca95dbd2f3a/raw/644b9b26300dd820ce96cec103bff48535a66bef/gistfile1.txt?_sm_au_=iVVD44FknRR475M3cLpsvK618Vf61'
        webbrowser.open(url)

    def source_btn_callback(self):
        url = 'https://github.com/tiancheng-st/qt_practice'
        webbrowser.open(url)

    def check_btn_callback(self):
        addr = self.address.text()
        self.connection_test(addr)

    def connection_test(self, addr=""):
        rm = visa.ResourceManager()
        try:
            rm = visa.ResourceManager()
            scope = rm.open_resource(addr)
            sp.initialize(scope)
            ms.initialize(scope)
            wp.initialize(scope)
            self.sucess_msg()
        except:
            self.error_msg()
    
    def error_msg(self):
        self.error = Error()
        self.error.show()

    def sucess_msg(self):
        self.sucess = SucessConnect()
        self.sucess.show() 



class Error(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('error.ui', self)


class SucessConnect(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('sucess.ui', self)
        # self.test_btn.clicked.connect(self.test_begin)
        self.test_btn.clicked.connect(self.close_and_begin)

    # close the current window and open the main control pannel
    def close_and_begin(self):
        self.close()
        self.main_window = mainWindow.MyWindowClass()
        self.main_window.show()        

    
app = QApplication(sys.argv)

myWindow = InfoWindow()
myWindow.show()

app.exec_()
