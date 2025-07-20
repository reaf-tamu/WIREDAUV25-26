import matplotlib.pyplot as plt
import numpy as np



# PID to center horizontally
center = 672/2
pid = PIDController(Kp=1.0, Ki=0.1, Kd=0.05, setpoint=setpoint)
while obj_cen_x != center:
	# read camera each time
	
	center_out = pid.compute(obj_cen_x, dt)

# PID to get closer
width = 100
pid = PIDController(Kp=1.0, Ki=0.1, Kd=0.05, setpoint=setpoint)
while obj_w != width:
	#read camera each time
	
	width_out = pid.compute(obj_w, dt)
