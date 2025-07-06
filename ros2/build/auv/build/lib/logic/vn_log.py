# logic/vn_log.py

from vnpy import VnSensor
import time


def check_vn(heading, origin, bound):
	left_bound = origin - bound
	right_bound = origin + bound
        
	print(heading)
	if origin >= 0:
		middle = origin - 180
		# right_range = (origin + 180) - 360
		if (left_bound <= heading <= right_bound):
			print("S")
		else:
			if (middle < heading <= origin):
				print("R")
			else:
				print("L")
	elif origin < 0:
		# left_range = (origin - 180) + 360
		middle = origin + 180
		if (left_bound <= heading <= right_bound):
			print("S")
		else:
			if (middle > heading >= origin):
				print("L")
			else:
				print("R")
	print()

