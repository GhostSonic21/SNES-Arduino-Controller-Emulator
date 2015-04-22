# Copyright (c) 2014 GhostSonic
# Licensed under the MIT License
# See LICENSE.txt for details

import serial
import time
import os
from tkinter import filedialog, Tk

ser =  serial.Serial("COM4", 115200) #Make sure you change the COM port to whatever it is on your setup.

root = Tk()
root.withdraw()

tasFilePath = filedialog.askopenfilename(filetypes = [('Lag-Stripped TAS File', '.tas'), ('All files','.*')])

tasFile = open(tasFilePath,'rb')
tasFileSize = int((os.stat(tasFilePath).st_size)/2) #gets the file size, divided by 2 for 2 input per frame.

time.sleep(1)
ser.write([0x10])

print('Ready...')

def main():
	amountRead = 0
	endOfFile = False
	while 1:
		#os.system("title " + ('Frame Counter: ' + str(amountRead) + '/' + str(tasFileSize))) #This is just pretty. But it seems to cause desyncs if it's active, uncomment at your own risk.
		
		if (convertToInt(ser.read(size=1)) == 0x12): #Receives the byte from the Arduino upon latch
			if (not endOfFile):
				SNESData1 = tasFile.read(1)
				SNESData2 = tasFile.read(1)
				ser.write(SNESData1)
				ser.write(SNESData2)
				print ("%d: %s %s" % (amountRead, hex(int.from_bytes(SNESData1,'little')), hex(int.from_bytes(SNESData2,'little'))))
				amountRead += 1
			else:
				ser.write([0x00])
				ser.write([0x00]) 					# Send 0 if the end of file is reached
			if (amountRead >= tasFileSize and not endOfFile):
				endOfFile = True
				print("End of File!")
		else:
			pass

def convertToInt(arrayInput):
	return int(ord(arrayInput[:1]))
	
def freeze():
	while 1:
		pass
		
if __name__ == "__main__":
	main()
