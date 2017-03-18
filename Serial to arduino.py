import os
import time
import serial
from time import sleep 
from datetime import datetime

# Serial port parameters
serial_speed = 9600
serial_port = '/dev/ttyACM0'

# Test with USB-Serial connection
# serial_port = '/dev/ttyACM0'
ser = serial.Serial(serial_port, serial_speed, timeout=1)

#os.system("sh keyboard.sh &") #start any script here

while True: #parsing to arduino
	if(incomming_char == "u"):
		ser.write("u")
	elif(incomming_char == "d"):
		ser.write("d")
	elif(incomming_char == "r"):
		ser.write("r")
	elif(incomming_char == "l"):
		ser.write("l")
	

