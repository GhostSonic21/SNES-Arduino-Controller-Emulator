# Copyright (c) 2014 GhostSonic
# Licensed under the MIT License
# See LICENSE.txt for details

#Keyboard Controls

import serial
import time
import win32api
import win32con

ser =  serial.Serial("COM3", 115200) #Make sure you change the COM port to whatever it is on your setup.

time.sleep(2)
ser.write([0x10])

#Recording stuff
recordFile = open("./recording.tas", 'wb')

def main():
	SNESData1 = 0x00
	SNESData2 = 0x00
	while 1:
		if win32api.GetAsyncKeyState(ord('G')):
			print("Recieved")
			recordFile.close()
			time.sleep(2)
			exit()
	
		if (ser.inWaiting() >= 1 and convertToInt(ser.read(size=1)) == 0x12): #Recieves the byte from the arduino upon latch
			#Up
			if win32api.GetAsyncKeyState(ord('W')):
				SNESData2 = SNESData2 | 0b00010000
			else:
				SNESData2 = SNESData2 & 0b11101111
			#Down
			if win32api.GetAsyncKeyState(ord('A')):
				SNESData2 = SNESData2 | 0b01000000
			else:
				SNESData2 = SNESData2 & 0b10111111
			#Left
			if win32api.GetAsyncKeyState(ord('S')):
				SNESData2 = SNESData2 | 0b00100000
			else:
				SNESData2 = SNESData2 & 0b11011111
			#Right
			if win32api.GetAsyncKeyState(ord('D')):
				SNESData2 = SNESData2 | 0b10000000
			else:
				SNESData2 = SNESData2 & 0b01111111
			#Y
			if win32api.GetAsyncKeyState(ord('N')):
				SNESData2 = SNESData2 | 0b00000010
			else:
				SNESData2 = SNESData2 & 0b11111101
			#B
			if win32api.GetAsyncKeyState(ord('M')):
				SNESData2 = SNESData2 | 0b00000001
			else:
				SNESData2 = SNESData2 & 0b11111110
			#A
			if win32api.GetAsyncKeyState(ord('K')):
				SNESData1 = SNESData1 | 0b00000001
			else:
				SNESData1 = SNESData1 & 0b11111110
			#X
			if win32api.GetAsyncKeyState(ord('J')):
				SNESData1 = SNESData1 | 0b00000010
			else:
				SNESData1 = SNESData1 & 0b11111101
			#L
			if win32api.GetAsyncKeyState(ord('Q')):
				SNESData1 = SNESData1 | 0b00000100
			else:
				SNESData1 = SNESData1 & 0b11111011
			#R
			if win32api.GetAsyncKeyState(ord('R')):
				SNESData1 = SNESData1 | 0b00001000
			else:
				SNESData1 = SNESData1 & 0b11110111
			#Start
			if win32api.GetAsyncKeyState(win32con.VK_RETURN):
				SNESData2 = SNESData2 | 0b00001000
			else:
				SNESData2 = SNESData2 & 0b11110111
			#Select
			if win32api.GetAsyncKeyState(win32con.VK_BACK):
				SNESData2 = SNESData2 | 0b00000100
			else:
				SNESData2 = SNESData2 & 0b11111011
			
			#Recording stuff
			recordFile.write(bytes({SNESData1}))
			recordFile.write(bytes({SNESData2}))
			#Write
			ser.write([SNESData1])
			ser.write([SNESData2])
			#
			print("%s %s" % (hex(SNESData1),hex(SNESData2)))
			

def convertToInt(arrayInput):
	return int(ord(arrayInput[:1]))
	
if __name__ == "__main__":
	main()