import time
from adafruit_servokit import ServoKit
import Jetson.GPIO as GPIO
from brping import Ping1D
myPing = Ping1D()
myPing.connect_serial("/dev/ttyUSB0", 115200)
GPIO.cleanup()
# sets up mission switch
pin_number = 32 # what pin number is it connected to, needs to be a GPIO pin found on pinout
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_number, GPIO.IN) # the button is an input
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

def set_vertical_pwm(pwm):#vertical thruster speed function  -PID
    pwm = max(75, min(95, pwm))

    A2.set_speed(pwm)
    A3.set_speed(pwm)
    M2.set_speed(pwm)
    M3.set_speed(pwm)

    A2.run()
    A3.run()
    M2.run()
    M3.run()

class PID:
    def __init__(self, kp, ki, kd, setpoint, output_limits=(-10, 10)):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_time = time.time()
        self.min_out, self.max_out = output_limits

    def compute(self, measurement):
        now = time.time()
        dt = now - self.prev_time #PID needs to know how fast things are changing, not just how much
        if dt <= 0:
            return 0

        error = self.setpoint - measurement #if we are far from target, push further
        self.integral += error * dt #fixes slow drift, if we have been off target for a long time, fix more aggressively 
        derivative = (error - self.prev_error) / dt #if we are approaching target too fast, slow down

        output = (
            self.kp * error +
            self.ki * self.integral +
            self.kd * derivative
        ) #blends all 3 together

        output = max(self.min_out, min(self.max_out, output))

        self.prev_error = error
        self.prev_time = now
        return output


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
time.sleep(3)  # Wait 5 seconds for ESC to sound (listen for 2 beeps)
print("beginning code")
time.sleep(3)
while True:
if myPing.initialize() is False:
    print("Failed to initialize Ping!")
    exit(1)

if myPing.initialize() is False:#PID-  without loop
    print("Failed to initialize Ping!")
    exit(1)


#PID setup
TARGET_DEPTH = 530
NEUTRAL_PWM = 90

pid = PID(
    kp=0.035,
    ki=0.0004,
    kd=0.02,
    setpoint=TARGET_DEPTH,
    output_limits=(-8, 8)
)

print("Starting PID depth hold...")

while True:

    data = myPing.get_distance()

    if not data or data["confidence"] < 80:
        set_vertical_pwm(NEUTRAL_PWM)
        continue

    depth = data["distance"] #if reading is not reliable 

    pid_output = pid.compute(depth)
    pwm = NEUTRAL_PWM - pid_output #subtract because increasing depth requires opposite thrust direction 

    set_vertical_pwm(pwm) #apply to thrusters

    print(
        f"Depth: {depth:.1f} | "
        f"Error: {TARGET_DEPTH - depth:.1f} | "
        f"PWM: {pwm:.2f}"
    )

    time.sleep(0.1)





