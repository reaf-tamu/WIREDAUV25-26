import Jetson.GPIO as GPIO
import time

# Setup
# sets up mission switch
pin_number = 32	# what pin number is it connected to, needs to be a GPIO pin found on pinout
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_number, GPIO.IN)	# the button is an input

# this is stuck in a loop until the button is pressed
# the rest of our code would be stuck behind the loop
# the button is active low

print("Mission switch activating…")

while (GPIO.input(pin_number) == GPIO.LOW):
	print(GPIO.input(pin_number))
	time.sleep(0.1)

print("beginning code")
time.sleep(3)

count = 0

while True:
	while (GPIO.input(pin_number) == GPIO.LOW):
		print(count)
		count += 1
		time.sleep(0.1)
	
	time.sleep(3)	
	print("pausing code")
	count = 0
	
	while (GPIO.input(pin_number) == GPIO.LOW):
		print(GPIO.input(pin_number))
		time.sleep(0.1)
	
	time.sleep(3)
	print("restarting code")

"""
try:

	print("Mission switch activating…")

	while True:
		print(GPIO.input(pin_number))
		if GPIO.input(pin_number) == GPIO.HIGH:
			
			while GPIO.input(pin_number) == GPIO.HIGH: # Button is held down for a sec
				time.sleep(1)
			
			print(GPIO.input(pin_number))
			
			
			while True:
				if GPIO.input(pin_number) == GPIO.HIGH:
					break # restarts code if button pressed again
			
				else: 
					print(GPIO.input(pin_number)) # if you wanted to still print high after the button is pressed
					time.sleep(0.5)
		else:
			print(GPIO.input(pin_number))
			time.sleep(0.5)

finally:
	GPIO.cleanup()
	"""
