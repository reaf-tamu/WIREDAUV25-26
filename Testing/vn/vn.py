from vnpy import *	# Vectornav module
import time

s = VnSensor()	# saves VN object to variable s
s.connect("/dev/ttyUSB0",115200)	# connects to VN at USB0, baud rate 115200


while (1):
    orientation = s.read_yaw_pitch_roll()		# reads all three axes
    x = orientation.x		# saves x axis to variable
    print("heading =", x)		# prints x
    time.sleep(0.5)			# sleeps for 0.5 seconds
