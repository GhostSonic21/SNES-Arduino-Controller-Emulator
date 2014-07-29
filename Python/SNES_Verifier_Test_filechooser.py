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

tasFile = open(tasFilePath,'r',encoding='latin-1') #Need to change encoding to latin1, or else python freaks out.
tasFileSize = int((os.stat(tasFilePath).st_size)/2) #gets the file size, divided by 2 plus 1.

time.sleep(1)
ser.write([0x10])

print('Ready...')

def main():
	amountRead = 0
	while 1:
		os.system("title " + ('Frame Counter: ' + str(amountRead) + '/' + str(tasFileSize))) #This is just pretty.
		
		if (convertToInt(ser.read(size=1)) == 0x12 and amountRead < tasFileSize): #Receives the byte from the Arduino upon latch
			SNESData1 = ord(tasFile.read(1))
			SNESData2 = ord(tasFile.read(1))
			ser.write([SNESData1])
			ser.write([SNESData2])
			print(SNESData1, SNESData2)
			amountRead += 1
		elif (amountRead >= tasFileSize): #This should prevent an exception at the end of file
			print('End of File!')
			ser.write([0x00])
			freeze() #Freeze the script when it's over.
			#exit() can be used here to exit it instead.
		else:
			pass

def convertToInt(arrayInput):
	return int(ord(arrayInput[:1]))
	
def freeze():
	while 1:
		pass
		
if __name__ == "__main__":
	main()