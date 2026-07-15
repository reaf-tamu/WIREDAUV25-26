import time
from adafruit_servokit import ServoKit

# Initialize PCA9685
kit = ServoKit(channels=16)

# Thruster channels to initialize
THRUSTER_CHANNELS = range(8, 16)

print("Initializing thrusters on channels 8-15 to neutral (90°)...")

for channel in THRUSTER_CHANNELS:
    # Set ESC pulse width range
    kit.servo[channel].set_pulse_width_range(1100, 1900)

    # Send neutral signal
    kit.servo[channel].angle = 90

    print(f"Channel {channel} set to 90°")

print("Holding neutral signal for 5 seconds...")
time.sleep(5)

print("Initialization complete.")
