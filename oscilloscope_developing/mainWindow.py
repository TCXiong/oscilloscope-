import setParameter as sp
import measure as ms
import waveform_plot as wp

import pyvisa as visa

from PyQt5.Qt import *
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
import webbrowser
import sys


class MyWindowClass(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        # self.setupUi(self)
        self.source = "CHANnel1"

        self.user.clicked.connect(self.open_manual)
        
        self.optionmenu_channel.activated.connect(self.optionmenu_channel_callback)
        self.optionmenu_impedance.activated.connect(self.impedance_callback)
        self.optionmenu_slope.activated.connect(self.slope_callback)
        self.autoscale.clicked.connect(self.auto_scale_callback)

        # change the value of slider
        self.slider1.valueChanged.connect(self.general_vertical_scaling)
        self.slider2.valueChanged.connect(self.general_vertical_offset)
        self.slider3.valueChanged.connect(self.general_horizontal_scaling)
        self.slider4.valueChanged.connect(self.general_horizontal_offset)

        # display the value of slider
        self.indicator1.setText(str(self.slider1.value()) + " mV")
        self.indicator2.setText(str(self.slider2.value()) + " mV")
        self.indicator3.setText(str(self.slider3.value()) + " μs")
        self.indicator4.setText(str(self.slider4.value()) + " μs")

        # setting the depth of memory
        self.memory_depth.returnPressed.connect(self.points_acquire_callback)
        self.points_auto.clicked.connect(self.points_auto_callback)

        
        # setting the sampling rate
        self.sample_rate_set.returnPressed.connect(self.sample_rate_callback)
        self.sample_auto.clicked.connect(self.sample_auto_callback)

        # average setting (call function)
        self.avg_box.stateChanged.connect(self.average_setting)

        # show waveform
        self.show_waveform_btn.clicked.connect(self.show_waveform_callback)

        # pop up the window for downloading the data measurement
        # self.measure_btn.clicked.connect(self.pop_window_measure)
        # wait for testing!!
        self.measure_btn.clicked.connect(self.pop_window_measure_selection)
        

        # pop up the window for downloading the waveform data
        # self.waveform_data_download_btn.clicked.connect(self.pop_window_waveform_data)
        self.waveform_data_download_btn.clicked.connect(self.developing_pop_window_waveform_data)
        

        # pop up the window for downloading the waveform plot
        # self.waveform_plot_download_btn.clicked.connect(self.pop_window_waveform_plot)
        self.waveform_plot_download_btn.clicked.connect(self.developing_pop_window_wave_plot)

        # pop up the window for downloading the screenshot
        # self.screenshot_download_btn.clicked.connect(self.pop_window_screenshot)
        self.screenshot_download_btn.clicked.connect(self.developing_pop_window_screenshot)
        

    def open_manual(self):
        url = 'file:///C:/Users/seung-jin%20orr/OneDrive%20-%20STMicroelectronics/Desktop/qt_test/user.html'
        webbrowser.open(url)

    def optionmenu_channel_callback(self, index):
        if index == 0:
            self.source = "CHANnel1"
        elif index == 1:
            self.source = "CHANnel2"
        elif index == 2:
            self.source = "CHANnel3"
        else:
            self.source = "CHANnel4"

        sp.channel_control_select(index)
        print("channel:", self.source)

    def impedance_callback(self, index):
        choice = "DC"
        if index == 0:
            choice = "DC"
        elif index == 1:
            choice = "DC50"
        elif index == 2:
            choice = "AC"
        else:
            choice = "LFR2"
        sp.impedance_control_select(choice)
        print("impedance:", choice)     
    
    def slope_callback(self, index):
        mode = "rise"
        if index == 0:
            mode = "POS"
        elif index == 1:
            mode = "NEG"
        else:
            mode = "EITH"
        sp.trigger_slope_select(mode)

    def auto_scale_callback(self):
        sp.autoScle()

    def general_vertical_scaling(self, value):
        print(value)
        self.indicator1.setText(str(value) + " mV")
        sp.vertical_scaling(value)

    def general_vertical_offset(self,value):
        print(value)
        self.indicator2.setText(str(value) + " mV")
        sp.vertical_offset(value)

    def general_horizontal_scaling(self, value):
        print(value)
        self.indicator3.setText(str(value) + " μs")
        sp.horizontal_scaling(value)

    def general_horizontal_offset(self, value):
        print(value)
        self.indicator4.setText(str(value) + " μs")
        sp.horizontal_offset(value)

    def points_acquire_callback(self):
        num = self.memory_depth.text()
        print(num)
        sp.points_acquire(num)
        # erase the display in the entry
        # self.memory_depth.setText("")

    def points_auto_callback(self):
        sp.points_auto_clicked()

    
    def sample_rate_callback(self):
        num = self.sample_rate_set.text()
        print(num)
        sp.sample_rate(num)
        # erase the display in the entry
        # self.sample_rate_set.setText("")

    def sample_auto_callback(self):
        sp.sample_auto_clicked()

    def average_setting(self):
        test = self.avg_box.isChecked()
        if test:
            sp.average_on_off("on")
        else:
            sp.average_on_off("off")


    def show_waveform_callback(self):
        wp.read_and_plot(source=self.source, plot_show=True)


    def pop_window_measure(self):
        self.mea = Measure(self.source)
        self.mea.show()

    # def pop_window_waveform_data(self):
    #     self.waveform_data = Waveform_data(self.source)
    #     self.waveform_data.show()

    def developing_pop_window_screenshot(self):
        self.screenshot = Developing_screenshot(self.source)
        self.screenshot.show()

    # new feature testing 
    def developing_pop_window_waveform_data(self):
        self.developing_wave = Developing_Waveform_data(self.source)
        self.developing_wave.show()
    # new feature testing 
    def developing_pop_window_wave_plot(self):
        self.waveform = Developing_wave_plot(self.source)
        self.waveform.show()

    def pop_window_waveform_plot(self):
        self.waveform_plot = Waveform_plot(self.source)
        self.waveform_plot.show()

    def pop_window_screenshot(self):
        self.screenshot_plot = Screenshot(self.source)
        self.screenshot_plot.show()

    def pop_window_measure_selection(self):
        self.measure_selection = MeasureSelection(self.source)
        self.measure_selection.show()


class Developing_screenshot(QDialog):
    def __init__(self, source_obj):
        super().__init__()
        uic.loadUi('developing_screenshot_download.ui', self)
        self.source = source_obj
        self.browse_file.clicked.connect(self.open_folder_dialog)
        self.screenshot_path = "./"        
        self.download_btn.clicked.connect(self.data_download_callback)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.pathOfFile.setText(folder_path)
        self.screenshot_path = folder_path

    def data_download_callback(self):
        wp.download_screen_image(path=(self.screenshot_path + "/screenshot.png"))


# new feature tested!
class Developing_wave_plot(QDialog):
    def __init__(self, source_obj):
        super().__init__()
        uic.loadUi('developing_wave_plot_download.ui', self)
        self.source = source_obj
        self.browse_file.clicked.connect(self.open_folder_dialog)
        self.waveform_path = "./"        
        self.download_btn.clicked.connect(self.data_download_callback)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.pathOfFile.setText(folder_path)
        self.waveform_path = folder_path

    def data_download_callback(self):
        wp.download_screen_image(self.waveform_path + "/waveform.png")


# new feature tested!
class Developing_Waveform_data(QDialog):
    def __init__(self, source_obj):
        super().__init__()
        uic.loadUi('developing_wave_data_download.ui', self)
        self.source = source_obj
        self.browse_file.clicked.connect(self.open_folder_dialog)
        self.data_path = "./"        
        self.download_btn.clicked.connect(self.data_download_callback)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.pathOfFile.setText(folder_path)
        self.data_path = folder_path

    def data_download_callback(self):
        wp.read_and_plot(download_data=True ,source=self.source, csv_path=(self.data_path+"/waveform_data.csv"), waveform_path="")



# wait for testing
class MeasureSelection(QMainWindow):
    def __init__(self, source_objs):
        super().__init__()
        uic.loadUi('data_measurements.ui', self)
        self.source = source_objs
        selected_item = self.comboBox.currentText()
        self.comboBox.activated.connect(self.updateTheValue)
        self.label = "None"
        self.measure.clicked.connect(self.runMeasurements)

       
    def updateTheValue(self, index):
        if index == 0:
            self.label = "Measurement: "
            self.measure_value.setText("None")
        elif index == 1:
            self.label = "rise time: "
        elif index == 2:
            self.label = "fall time: "
        elif index == 3:
            self.label = "frequency: "
        elif index == 4:
            self.label = "period: "
        elif index == 5:
            self.label = "amplitude: "
        elif index == 6:
            self.label = "pulse width: "
        elif index == 7:
            self.label = "duty cycle: "
        
        self.measure_label.setText(self.label)

    
    def runMeasurements(self):
        if self.label == "rise time: ":
            riseTime = ms.mea_rise_time(self.source)
            self.measure_value.setText(str(riseTime))
            print(ms.mea_unit(self.source))
        elif self.label == "fall time: ":
            fallTime = ms.mea_fall_time(self.source)
            self.measure_value.setText(str(fallTime))
        elif self.label == "frequency: ":
            frequency = ms.mea_frequency(self.source)
            self.measure_value.setText(str(frequency))
        elif self.label == "period: ":
            period = ms.mea_period(self.source)
            self.measure_value.setText(str(period))
        elif self.label == "amplitude: ":
            amplitude = ms.mea_amplitude(self.source)
            self.measure_value.setText(str(amplitude))
        elif self.label == "pulse width: ":
            pulse_width = ms.mea_pulse_width(self.source)
            self.measure_value.setText(str(pulse_width))
        elif self.label == "duty cycle: ":
            duty_cycle = ms.mea_duty_cycle(self.source)
            self.measure_value.setText(str(duty_cycle))
        




class Measure(QDialog):
    def __init__(self, source_obj):
        super().__init__()
        uic.loadUi('data_download.ui', self)
        # self.setupUi(self)
        self.source = source_obj

        print(self.source)
        
        self.measure_path.returnPressed.connect(self.download_callback)

    def download_callback(self):
        # print(self.source)
        path = self.measure_path.text() + ".csv"
        print(path)
        ms.measure(self.source, path, debug=False)


# class Waveform_data(QDialog):
#     def __init__(self, source_obj):
#         super().__init__()
#         uic.loadUi('waveform_data_download.ui', self)
#         # self.setupUi(self)
#         self.source = source_obj
#         print(self.source)
#         self.data_download.returnPressed.connect(self.data_download_callback)

#     def data_download_callback(self):
#         # print(self.source)
#         data_path = self.data_download.text() + ".csv"
#         print(data_path)
#         wp.read_and_plot(download_data=True ,source=self.source, csv_path=data_path, waveform_path="")



# class Waveform_plot(QDialog):
#     def __init__(self, source_obj):
#         super().__init__()
#         uic.loadUi('waveform_plot_download.ui', self)
#         # self.setupUi(self)
#         self.source = source_obj
#         print(self.source)
#         self.plot_download.returnPressed.connect(self.plot_download_callback)   

#     def plot_download_callback(self):
#         plot_path = self.plot_download.text() + ".png"
#         print(plot_path)
#         wp.read_and_plot(download_plot=True, plot_show=True,source=self.source, csv_path="", waveform_path=plot_path)



class Screenshot(QDialog):
    def __init__(self, source_obj):
        super().__init__()
        uic.loadUi('screenshot_download.ui', self)
        # self.setupUi(self)
        self.source = source_obj
        print(self.source)
        self.screenshot_path.returnPressed.connect(self.screenshot_download_callback)

    def screenshot_download_callback(self):
        # print(self.source)
        data_path = self.screenshot_path.text() + ".png"
        print(data_path)
        wp.download_screen_image(path=data_path)


# test section

# rm = visa.ResourceManager()
# scope = rm.open_resource("USB0::0x0957::0x9009::MY53120106::0::INSTR")
# scope.timeout = 20000
# sp.initialize(scope)
# ms.initialize(scope)
# wp.initialize(scope)



# app = QApplication(sys.argv)

# myWindow = MyWindowClass()
# myWindow.show()


# app.exec_()