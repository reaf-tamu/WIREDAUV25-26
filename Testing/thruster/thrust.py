import time
from adafruit_servokit import ServoKit

# Initialize PCA9685 with 16 channels
kit = ServoKit(channels=16)

# Set correct PWM range for ESC on channel 7
kit.servo[0].set_pulse_width_range(1100, 1900)

class Motor:
    def __init__(self, channel):
        self.channel = channel
        self.speed = 90  # Default to neutral (1500 µs)
        self.prev_speed = None  # Force update on first run

    def set_speed(self, angle):
        self.speed = angle

    def run(self):
        if self.prev_speed != self.speed:
            print(f"Sending PWM: {self.speed}° on channel {self.channel}")
            kit.servo[self.channel].angle = self.speed
            self.prev_speed = self.speed
        else:
            # Keep refreshing PWM signal (some ESCs require this)
            kit.servo[self.channel].angle = self.speed

    def stop(self):
        self.set_speed(90)
        self.run()

# Initialize motor
motor_A1 = Motor(0)

# STEP 1: ESC Initialization
print("Initializing ESC with 1500 µs (90°) signal...")
motor_A1.set_speed(90)
motor_A1.run()
time.sleep(5)  # Wait for ESC to arm

# STEP 2: Run continuously
motor_A1.set_speed(80)
print("Running motor. Press Ctrl+C to stop.")

try:
    while True:
        motor_A1.run()
        time.sleep(0.05)  # Refresh at 20 Hz
except KeyboardInterrupt:
    print("\nStopping motor.")
    motor_A1.stop()
    time.sleep(1)

