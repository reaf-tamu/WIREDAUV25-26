#!/usr/bin/env python3
import time
from adafruit_servokit import ServoKit
import Jetson.GPIO as GPIO
from brping import Ping1D  # <-- NEW: bring in Ping1D

# ---------------------------
# USER TUNABLES for pinger
# ---------------------------
TARGET_DISTANCE_M = 1.0      # descend until distance to floor <= this (meters)
CONFIDENCE_MIN = 50          # ignore noisy sonar readings below this confidence (%)
PING_PORT = "/dev/ttyUSB0"   # adjust if needed
PING_BAUD = 9600
PING_HZ = 5                  # sonar poll rate (Hz)
# ---------------------------

# --- Helper: connect to Ping1D ---
def connect_ping(port=PING_PORT, baud=PING_BAUD):
    ping = Ping1D()
    print(f"[Ping1D] Connecting on {port} @ {baud} ...")
    if not ping.connect_serial(port, baud):
        raise RuntimeError(f"Could not connect to Ping1D on {port}")
    print("[Ping1D] Connected.")
    return ping

# --- Helper: single sonar reading ---
def read_floor_distance(ping):
    """
    Returns (distance_m, confidence) or (None, None) if failed.
    """
    try:
        data = ping.get_distance()
        if not data:
            return None, None
        return data["distance"] / 1000.0, data["confidence"]  # mm -> m
    except Exception as e:
        print(f"[Ping1D][ERROR] {e}")
        return None, None

# -----------------------------------
# ORIGINAL SETUP (unchanged)
# -----------------------------------
GPIO.cleanup()
pin_number = 32
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_number, GPIO.IN)

kit = ServoKit(channels=16)

# NOTE: these initial direct assignments set channels to 90 once.
# You immediately replace A1..M4 with Motor() objects below (which is fine).
# Keeping them to match your original flow.
A1 = kit.servo[12].angle = 90
A2 = kit.servo[13].angle = 90
A3 = kit.servo[14].angle = 90
A4 = kit.servo[15].angle = 90

M1 = kit.servo[2].angle = 90
M2 = kit.servo[3].angle = 90
M3 = kit.servo[4].angle = 90
M4 = kit.servo[5].angle = 90

class Motor:
    def __init__(self, channel):
        self.channel = channel
        self.speed = 90
        self.prev_speed = None

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

# Re-create motors exactly like your code
A1 = Motor(12)
A2 = Motor(13)
A3 = Motor(14)
A4 = Motor(15)

M1 = Motor(2)
M2 = Motor(3)
M3 = Motor(4)
M4 = Motor(5)

# ESC initialization (unchanged)
print("Initializing thrusters, should hear two beeps after power cycle")
for m in (A1, A2, A3, A4, M1, M2, M3, M4):
    m.set_speed(90); m.run()

time.sleep(3)  # Wait for ESC tones

# ---------------------------
# NEW: Connect Ping1D here
# ---------------------------
try:
    ping = connect_ping()
except RuntimeError as e:
    print(f"[FATAL] {e}")
    # Fail safe: keep running without sonar (will never exit the 'go down' loop)
    # You can 'return' or 'exit' if you prefer to abort entirely.
    ping = None

# -----------------------------------
# MISSION SWITCH (unchanged)
# -----------------------------------
print("Mission switch activating…")
while (GPIO.input(pin_number) == GPIO.LOW):
    print("LOW")
    time.sleep(0.5)
print("HIGH")

print("beginning code")
time.sleep(3)

# ---------------------------------------------------------
# MAIN SECTION
# Only the **down** part is soft-coded with sonar now.
# Hover and Forward remain hard-coded exactly as you had them.
# ---------------------------------------------------------
while True:
    while (GPIO.input(pin_number) == GPIO.LOW):
        # ============ SOFT-CODED DESCENT USING PINGER ============
        print("going down (sensor-guided)")

        # Command your existing 'down' speeds while we check sonar.
        # (These are your known-good "go down" values)
        A2.set_speed(75); A2.run()
        A3.set_speed(75); A3.run()
        M2.set_speed(75); M2.run()
        M3.set_speed(75); M3.run()

        # Keep descending until we reach the target distance from floor
        # or until we get a good reading that says we're close enough.
        # If sonar is missing/low-confidence, we keep descending cautiously.
        period = 1.0 / max(1, PING_HZ)
        while True:
            if ping is None:
                # No sonar available: keep previous 'down' for your original 3.5 s then break
                time.sleep(3.5)
                break

            dist, conf = read_floor_distance(ping)
            if dist is None:
                print("[WARN] sonar no data; continuing down a bit…")
                time.sleep(period)
                continue

            if conf < CONFIDENCE_MIN:
                print(f"[LOW CONF] {conf}% | last dist {dist:.3f} m | continuing down…")
                time.sleep(period)
                continue

            # Good reading: print it
            print(f"[PING] floor: {dist:.3f} m | conf: {conf}%")

            # STOP DESCENT when we are within or below target distance to the floor
            if dist <= TARGET_DISTANCE_M:
                print(f"[PING] target reached (<= {TARGET_DISTANCE_M:.2f} m).")
                # Neutralize vertical thrusters before switching to hover
                A2.set_speed(90); A2.run()
                A3.set_speed(90); A3.run()
                M2.set_speed(90); M2.run()
                M3.set_speed(90); M3.run()
                break

            # Otherwise keep descending with your same speeds
            # (optional) small pause to avoid spamming the bus
            time.sleep(period)

        # ============ HARDCODED HOVER + FORWARD (UNCHANGED) ============
        while True:
            # freshwater pool -- can maybe make hovering higher
            print("hovering")
            A2.set_speed(82); A2.run()
            A3.set_speed(82); A3.run()
            M2.set_speed(82); M2.run()
            M3.set_speed(82); M3.run()
            
            # forward
            # A1 is much stronger than A4
            # m1 and m4 are about the same, m4 slightly weaker
            print("forward")
            A1.set_speed(98);  A1.run()
            A4.set_speed(77);  A4.run()
            M1.set_speed(101); M1.run()
            M4.set_speed(79);  M4.run()

    time.sleep(3)	
    print("pausing code")
    count = 0
	
    while (GPIO.input(pin_number) == GPIO.LOW):
        print(GPIO.input(pin_number))
        A1.set_speed(90); A1.run()
        A2.set_speed(90); A2.run()
        A3.set_speed(90); A3.run()
        A4.set_speed(90); A4.run()
        M1.set_speed(90); M1.run()
        M2.set_speed(90); M2.run()
        M3.set_speed(90); M3.run()
        M4.set_speed(90); M4.run()
        time.sleep(0.1)
	
    time.sleep(3)
    print("restarting code")


# -------------- (Unreachable in your original file) --------------
# Keeping your additional demo loops below, but note that your
# 'while True' above never exits. Left here unchanged for parity.
while True:
    print("going down")
    A2.set_speed(70); A2.run()
    A3.set_speed(70); A3.run()
    M2.set_speed(70); M2.run()
    M3.set_speed(70); M3.run()
    time.sleep(2)
	
    print("hovering")
    A2.set_speed(83); A2.run()
    A3.set_speed(81); A3.run()
    M2.set_speed(83); M2.run()
    M3.set_speed(81); M3.run()
	
    print("forward")
    A1.set_speed(110); A1.run()
    A4.set_speed(70);  A4.run()
    M1.set_speed(110); M1.run()
    M4.set_speed(70);  M4.run()
    print(f"Foward thruster speeds: {A1.speed}, {A4.speed}, {M1.speed}, {M4.speed}")
    time.sleep(5)

# ...and the CCW/CW block stays as in your file (unreachable)
