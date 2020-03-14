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
        serialPort = "/dev/cu.usbmodem14101" #Initial USB Port
        serialPort2 = "/dev/cu.usbmodem14201" #Alternative USB Port
        print("MAC Detected")
    elif serialPort == 'linux':
        serialPort = "/dev/ttyACM0"
        serialPort2 = "/dev/ttyACM0"
        print("Linux Detected")
    else:
        serialPort = "COM3" 
        serialPort2 = "COM4"
        print("Windows Detected")
    #print("Enter the baud rate or leave blank (Default = 9600)")
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
    print("How many sensors are connected? (Default = 2)")
    sensornum = input()
    if sensornum == '':
        sensornum = 2
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
        #How long to collect data for
        print("Enter how many minutes to collect or leave blank (Default = 1)")
        minutes = input()
        if minutes == '':
            minutes = 1
        else:
            minutes = float(minutes)
        datapoints = 999999999
        initt = time.localtime()#Initiate the timer for time based data collection
        initt = (initt.tm_hour*60)+(initt.tm_min)+(initt.tm_sec/60)
        startup = False #To activate the pause timer later so that the first datapoint gets captured        

    # "COM3" is the port that your Arduino board is connected.set it to port that your are using        
    try:#Primary port to try
        ser = serial.Serial(port=serialPort, baudrate=baud, timeout = 1.5)
    except:
        try:#Alternative port to try
            ser = serial.Serial(port=serialPort2, baudrate=baud, timeout = 1.5)
        except:
            print("The Arduino is not working or not connected\n--\n--")
            sys.exit()
    
    serial.PARITY_EVEN #Parity activation?

    # Initialize Workbook 1 and 2 if selected
    global workbook 
    workbook = xlsxwriter.Workbook('sensordata.xlsx')
    worksheet1 = workbook.add_worksheet()
    if sensornum >=2:
        worksheet2 = workbook.add_worksheet()
    row = 2
    col = 0
    cc = ["Arduino #","Sensor Addr","Time","Elapsed (s)","Temp (C)","Hum (RH%)"]
    for i in range(6):#Initiate the first row of the spreadsheet with the category names
        worksheet1.write(0, col + i, cc[i])
        try:
            worksheet2.write(0, col + i, cc[i])
        except:
            continue

    for row in range(1,datapoints+1):
        for j in range(sensornum):
            # Get time
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            # Read Arduino output, parse, and as2sign to entrynum, temp, and hum
            cc = []
            while cc == [] or not ("AWK" in cc):            
                if j == 0:
                    ser.write(str.encode("R1"))#Read Sensor 1
                else:
                    ser.write(str.encode("R2"))#Read Sensor 2
                cc = str(ser.readline())
            cc = (cc[2:][:-5])   #Get rid of the extra bits in front of the code and end
            cc = (cc.split(','))    #Split data by detecting the commas        
            try:
                ardNum = cc[0]
                sensorAdd = cc[1]                
                ardTime = cc[2]
                temp = cc[3]
                hum = cc[4]
            except:# Try reading the arduino again before throwing another exception and ending the program.
                try:
                    cc = []
                    while cc == [] or not ("AWK" in cc):            
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
                except:
                    print("------\nArduino Not Configured Properly\n")
                    sys.exit()

            print(ardNum,sensorAdd,current_time,ardTime,temp,hum)
            # Write data to Workbook
            if j == 0:
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
        time.sleep(interval)

        if (collectiontype == 1) and startup: #Timer to check when to end program for time based data collection
            currentt = time.localtime()
            currentt = (currentt.tm_hour*60)+(currentt.tm_min)+(currentt.tm_sec/60)
            if (currentt - initt) >= minutes:
                break
        startup = True
    destroy()

def destroy():#Will clean up the program and close the worksheet
    print("\nWriting")
    workbook.close()
    sys.exit()   
try:
    loop() #Main program
except KeyboardInterrupt:   #If Control C is pressed 
    destroy()