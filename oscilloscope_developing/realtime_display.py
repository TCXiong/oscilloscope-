import pyvisa as visa
import struct
import matplotlib.pyplot as plt

def do_query_number(query):
    results = myScope.query("%s" % query)
    return float(results)

instAddress = "USB0::0x0957::0x9009::MY53120106::0::INSTR"
rm = visa.ResourceManager()
myScope = rm.open_resource(instAddress) # example instAddress ='GPIB0::12::INSTR'

myScope.write(":SYSTem:HEADer OFF") 
myScope.write(":ACQuire:MODE RTIME")
myScope.write(":ACQuire:COMPlete 100")
myScope.write(":WAVeform:SOURce CHANnel1")
myScope.write(":WAVeform:FORMat BYTE")
myScope.write(":ACQuire:COUNt 8")
myScope.write(":ACQuire:POINts 50000")

while True:
    myScope.write(":DIGitize CHANnel1")

    rawData = myScope.query_binary_values(":WAVeform:DATA?", datatype = 's', container = bytes)

    x_increment = do_query_number(":WAVeform:XINCrement?")
    x_origin = do_query_number(":WAVeform:XORigin?")
    y_increment = do_query_number(":WAVeform:YINCrement?")
    y_origin = do_query_number(":WAVeform:YORigin?")

    values = struct.unpack("%db" % len(rawData), rawData)
    print("Number of data values: %d" % len(values))

    time = []
    volt = []
    for i in range(0, len(values) - 1):
        time_val = x_origin + (i * x_increment)
        voltage = (values[i] * y_increment) + y_origin
        time.append(time_val)
        volt.append(voltage)

    plt.clf()
    plt.plot(time, volt)
    plt.title("real time display")
    plt.xlabel('Time(s)')
    plt.ylabel('Voltage(V)')    
    plt.pause(0.01)
