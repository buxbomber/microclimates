import serial
import xlsxwriter
import time
import sys
def loop():
    #Input statements so the user can enter custom data without having to change the code.
    #Leaving it empty will default.
    #Code to detect the OS and then try the USB port
    serialPort = sys.platform
    if serialPort == 'darwin':
        serialPort = "/dev/cu.usbmodem14101"
        serialPort2 = "/dev/cu.usbmodem14201"
        print("MAC Detected")
    elif serialPort == 'linux':
        serialPort = "/dev/ttyACM0"
        print("Linux Detected")
    else:
        serialPort = "COM3"
        print("Windows Detected")
    print("Enter the baud rate or leave blank (Default = 9600)")
    #If changing the baud
    #baud = input()
    baud = 9600
    if baud == '':
        baud = 9600
    else:
        baud = int(baud)
    #Data read interval
    print("Enter interval in s or leave blank (Default = 1)")
    interval = input()
    if interval == '':
        interval = 1
    else:
        interval = int(interval)
    #How many sensors are connected
    print("How many sensors are connected? (Default = 1)")
    sensornum = input()
    if sensornum == '':
        sensornum = 1
    else:
        sensornum = int(sensornum)
    #Collecting for number or time
    print("Are you collecting data for a set number of points (0) or set amount of time (1)? (Default = 0)")
    collectiontype = input()
    if collectiontype == '':
        collectiontype = 0
    else:
        collectiontype = int(collectiontype)
    
    if collectiontype == 0:
        #How many datapoints to collect
        print("Enter datapoints to collect or leave blank (Default = 30)")
        datapoints = input()
        if datapoints == '':
            datapoints = 31
        else:
            datapoints = int(datapoints)+1
    elif collectiontype == 1:
        #How long to collect
        print("Enter how many minutes to collect or leave blank (Default = 1)")
        minutes = input()
        if minutes == '':
            minutes = 1
        else:
            minutes = float(minutes)
        datapoints = 999999999
        initt = time.localtime()
        initt = (initt.tm_hour*60)+(initt.tm_min)+(initt.tm_sec/60)

        

    # "COM3" is the port that your Arduino board is connected.set it to port that your are using        
    try:
        ser = serial.Serial(port=serialPort, baudrate=baud)
    except:
        try:
            ser = serial.Serial(port=serialPort2, baudrate=baud)
        except:
            print("The Arduino is not working or not connected\n--\n--")

    # Initialize Workbook
    global workbook 
    workbook = xlsxwriter.Workbook('sensordata.xlsx')
    worksheet1 = workbook.add_worksheet()
    if sensornum >=2:
        worksheet2 = workbook.add_worksheet()
    row = 0
    col = 0
    print(time.time())
    for i in range(datapoints):

        row = i

        for j in range(sensornum):
            # Get time
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)

            # Read Arduino output, parse, and assign to entrynum, temp, and hum
            if j == 0:
                ser.write(str.encode("R1"))
            else:
                ser.write(str.encode("R2"))
            cc = str(ser.readline())
            cc = (cc[2:][:-5])   
            cc = (cc.split(','))
            ardNum = cc[0]
            sensorAdd = cc[1]
            ardTime = cc[2]
            temp = cc[3]
            hum = cc[4]

            try:
                sensorAdd = int(sensorAdd)
            except:
                sensorAdd = 45

            print(ardNum,sensorAdd,current_time,ardTime,temp,hum)
            # Write data to Workbook
            if sensorAdd == 45:
                worksheet1.write(row, col, ardNum)
                worksheet1.write(row, col + 1, sensorAdd)
                worksheet1.write(row, col + 2, current_time)
                worksheet1.write(row, col + 3, ardTime)
                worksheet1.write(row, col + 4, temp)
                worksheet1.write(row, col + 5, hum)
            else:
                worksheet2.write(row, col, ardNum)
                worksheet2.write(row, col + 1, sensorAdd)
                worksheet2.write(row, col + 2, current_time)
                worksheet2.write(row, col + 3, ardTime)
                worksheet2.write(row, col + 4, temp)
                worksheet2.write(row, col + 5, hum)
            time.sleep(interval/2)


        if collectiontype == 1:
            currentt = time.localtime()
            currentt = (currentt.tm_hour*60)+(currentt.tm_min)+(currentt.tm_sec/60)
            timediff = currentt - initt
            if timediff >= minutes:
                break
    workbook.close()


def destroy():
    workbook.close()

try:
    loop()
except KeyboardInterrupt:
    print("\nWriting")
    print(time.time())
    destroy()
