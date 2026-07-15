"""
Motor setup shared by the main mission script and speeds.py.

Keeping the ServoKit/Motor definitions here (instead of in the main script)
lets speeds.py import the same motor objects without a circular import.
"""

from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)  # PCA9685 servo/ESC driver, 16 channels


class Motor:
    """Wraps a single ESC/servo channel and only sends a PWM update when the
    target speed actually changes (avoids spamming the bus). Because the
    servo driver holds the last angle it was given, you only need to call
    run() once per change — no need to keep re-calling it to "hold" a speed."""

    def __init__(self, channel):
        self.channel = channel
        self.speed = 90          # 90 = neutral (~1500 microsecond pulse)
        self.prev_speed = None   # forces an update the first time run() is called

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


# Channel assignments
A1 = Motor(12)
A2 = Motor(13)
A3 = Motor(14)
A4 = Motor(15)
M1 = Motor(2)
M2 = Motor(3)
M3 = Motor(4)
M4 = Motor(5)

ALL_MOTORS = [A1, A2, A3, A4, M1, M2, M3, M4]


def stop_all_motors():
    """Set every thruster back to neutral (90)."""
    for motor in ALL_MOTORS:
        motor.stop()


def initialize_escs():
    """Send neutral signal to all ESCs and wait for the arming beeps."""
    print("Initializing thrusters, should hear two beeps after power cycle")
    for motor in ALL_MOTORS:
        motor.set_speed(90)
        motor.run()
    import time
    time.sleep(5)  # give ESCs time to arm (listen for 2 beeps)
