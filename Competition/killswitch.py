import time
from motors import initialize_escs, stop_all_motors
# Assuming your motors file has a function to set servo angles directly
# from motors import set_all_thrusters 


print(f"Waiting {STARTUP_WAIT} seconds...")
time.sleep(STARTUP_WAIT)

print("Initializing ESCs (listen for the beeps)...")
initialize_escs()
time.sleep(3)

print("Setting all thrusters to 90...")
# If you have a custom servo kit instance inside motors.py, you would call it here.
# For example, if you use Adafruit PCA9685 ServoKit under the hood:
# for i in range(8):  # Adjust to your number of thrusters
#     kit.servo[i].angle = 90

# Hold the speed indefinitely (or until interrupted)
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping thrusters...")
    stop_all_motors()
