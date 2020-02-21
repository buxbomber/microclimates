import serial
import xlsxwriter
import time
import sys

# Initialize Workbook
workbook = xlsxwriter.Workbook('sensordata.xlsx')
worksheet1 = workbook.add_worksheet()
worksheet2 = workbook.add_worksheet
row = 0
col = 0
select = 1

#Input statements so the user can enter custom data without having to change the code.
#Leaving it empty will default.
#Code to detect the OS and then try the USB port
serialPort = sys.platform
if serialPort == 'darwin':
    serialPort = "/dev/cu.usbmodem14101"
    print("MAC Detected")
else:
    serialPort = "COM3"
    print("Windows Detected")
print("Enter the baud rate or leave blank (Default = 9600)")
#If changing the baud
baud = raw_input()
if baud == '':
	baud = 9600
else:
	baud = int(baud)
#Data read interval
print("Enter interval in s or leave blank (Default = 1)")
interval = raw_input()
if interval == '':
	interval = 1
else:
	interval = int(interval)
#How many datapoints to collect
print("Enter datapoints to collect or leave blank (Default = 30)")
datapoints = raw_input()
if datapoints == '':
	datapoints = 31
else:
	datapoints = int(datapoints)+1
	

# "COM3" is the port that your Arduino board is connected.set it to port that your are using        
try:
    ser = serial.Serial(port=serialPort, baudrate=baud)
except:
    print("The Arduino is not working or not connected\n--\n--")

# Set how many datapoints to collect:
#datapoints = 30

for i in range(datapoints):
    # Get time
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    # Read Arduino output, parse, and assign to entrynum, temp, and hum
    if select == 1:
        ser.write("R1")
        select = 2
    else:
        ser.write("R2")
        select = 1

    cc = str(ser.readline())
    cc = (cc[2:][:-5])   
    cc = (cc.split(','))
    sensorNum = cc[0]
    ardTime = cc[1]
    temp = cc[2]
    hum = cc[3]

    print(sensorNum,current_time,ardTime,temp,hum)

    # Write data to Workbook
    if select == 1
        worksheet1.write(row, col, sensorNum)
        worksheet1.write(row, col + 1, current_time)
        worksheet1.write(row, col + 2, ardtime)
        worksheet1.write(row, col + 3, temp)
        worksheet1.write(row, col + 4, hum)
    else:
        worksheet2.write(row, col, sensorNum)
        worksheet2.write(row, col + 1, current_time)
        worksheet2.write(row, col + 2, ardtime)
        worksheet2.write(row, col + 3, temp)
        worksheet2.write(row, col + 4, hum)
        
    row += 1

    time.sleep(interval)

workbook.close()
