from PyQt5.Qt import *
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import webbrowser
import sys




class MeasureSelection(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('combo_test.ui', self)

    

        selected_item = self.comboBox.currentText()
        self.comboBox.activated.connect(self.updateTheValue)
        # print(selected_item)

       

    def updateTheValue(self, index):
        measure_label = "None"
        if index == 0:
            measure_label = "Measurement: "
        elif index == 1:
            measure_label = "rise time: "
        elif index == 2:
            measure_label = "fall time: "
        elif index == 3:
            measure_label = "frequency: "
        elif index == 4:
            measure_label = "period: "
        elif index == 5:
            measure_label = "amplitude: "
        elif index == 6:
            measure_label = "pulse width: "
        elif index == 7:
            measure_label = "duty cycle: "
        
        self.measure_label.setText(measure_label)



app = QApplication(sys.argv)

myWindow = MeasureSelection()
myWindow.show()

app.exec_()