
import time
from adafruit_servokit import ServoKit
import Jetson.GPIO as GPIO
from adafruit_servokit import ServoKit
from brping import Ping1D

from speeds import up, down, hover
from ping_log import check_depth


GPIO.cleanup()
# sets up mission switch
pin_number = 32	# what pin number is it connected to, needs to be a GPIO pin found on pinout
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_number, GPIO.IN)	# the button is an input


# connect to pinger
myPing = Ping1D()
myPing.connect_serial("/dev/ttyUSB1", 115200)
if myPing.initialize() is False:
    print("Failed to initialize Ping!")
    exit(1)
myPing.set_ping_interval(29)
myPing.set_speed_of_sound(1500)


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


print("Mission switch activating…")
print(GPIO.input(pin_number))
while (GPIO.input(pin_number) == GPIO.LOW):
	print(GPIO.input(pin_number))
	time.sleep(0.1)
print("Beginning code in 3 seconds")
time.sleep(3)
	
	
# begin  loop
while True:
	# main loop
	#stay down
	while (GPIO.input(pin_number) == GPIO.LOW):
		data = myPing.get_distance_simple()
		ping = data['distance']
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
		
	
	
	# stops code and thrusters after first press
	print("stopping code")
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
	time.sleep(3)	
	count = 0
		
	# waiting loop, press button again to restart
	while (GPIO.input(pin_number) == GPIO.LOW):
		GPIO.input(pin_number)
		time.sleep(0.1)
		
	print("restarting code in 3 seconds")
	time.sleep(3)

