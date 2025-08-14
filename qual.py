import time
from adafruit_servokit import ServoKit

# Initialize PCA9685 with 16 channels,
kit = ServoKit(channels=16)

#Set up thrusters
A1 = kit.servo[12].angle = 90 # this one works
A2 = kit.servo[13].angle = 90
A3 = kit.servo[14].angle = 90 # this one works
A4 = kit.servo[15].angle = 90 # this one works

M1 = kit.servo[2].angle = 90 # this one works
M2 = kit.servo[3].angle = 90 # this one works
M3 = kit.servo[4].angle = 90 # this one works
M4 = kit.servo[5].angle = 90 # this one works


class Motor:
    def __init__(self, channel):
        self.channel = channel
        self.speed = 90  # Default to neutral (1500 µs)
        self.prev_speed = None  # Force update on first run

    def set_speed(self, angle):
        self.speed = angle

    def run(self):
        if self.prev_speed != self.speed:
            print(f"Sending PWM: {self.speed}")
            kit.servo[self.channel].angle = self.speed
            self.prev_speed = self.speed

    def stop(self):
        self.set_speed(90)
        self.run()

# Initialize A1 on channel 7 (ESC signal wire is connected here),
A1 = Motor(12)
A2 = Motor(13)
A3 = Motor(14)
A4 = Motor(15)

M1 = Motor(2)
M2 = Motor(3)
M3 = Motor(4)
M4 = Motor(5)


# ESC Initialization
print("Initializing thrusters, should hear two beeps after power cycle")

A1.set_speed(90)
A1.run()
A2.set_speed(90)
A2.run()
A3.set_speed(90)
A3.run()
A4.set_speed(90)
A4.run()
M1.set_speed(90)
M1.run()
M2.set_speed(90)
M2.run()
M3.set_speed(90)
M3.run()
M4.set_speed(90)
M4.run()

time.sleep(5)  # Wait 5 seconds for ESC to sound (listen for 2 beeps)


# run thrusters forward for 5 seconds, reverse for 5 seconds
#Add in going and staying down while going forward

print("Mission switch activating…")
print(ms)
while (ms == False):
	print(ms)
	ping, ms = sub.get_data()
	time.sleep(0.1)
print("Beginning code in 3 seconds")
time.sleep(3)
	
	
	# begin  loop
while True:
# main loop
	#stay down
	ms = sub.get_data()
	while ms == False:
		ms = sub.get_data()
		if check_depth(16, 1, ping) == "D":
			down()
		elif check_depth(16, 1, ping) == "U":
			up()
		else:
			hover()
	
		# forward
		A1.set_speed(100)  
		A1.run()
		A4.set_speed(100)
		A4.run()
		M1.set_speed(100)  
		M1.run()
		M4.set_speed(100)
		M4.run()
		print(f"Foward thruster speeds: {A1.speed}, {A4.speed}, {M1.speed}, {M4.speed}")
		time.sleep(5)
		
	
	
	# stops code after first press
	print("stopping code")
	time.sleep(3)	
	count = 0
		
	# waiting loop, press button again to restart
	ms = sub.get_data()
	while (ms == False):
		print(ms)
		ms = sub.get_data()
		time.sleep(0.1)
		
	print("restarting code in 3 seconds")
	time.sleep(3)

