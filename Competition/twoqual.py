"""
AUV Mission Script
-------------------
Hardcoded dive-and-drive mission (no pinger, no mission switch):
  1. Wait 5 seconds at startup (gives you time to drop it in / get clear).
  2. Arm/initialize the ESCs (listen for two beeps).
  3. Dive to submerge, then drive forward while staying submerged.
  4. Stop all thrusters.

There's no depth sensor and no switch in this version, so "staying
underwater" is just a fixed dive time before switching to forward thrust —
tune DIVE_TIME, FORWARD_TIME, and the thruster speeds in speeds.py to get
the behavior you want.

Note: thrusters don't need to be re-commanded every second to "hold" a
speed — the servo driver keeps outputting the last angle it was given until
you change it. So each maneuver below is triggered once, then held for its
duration with a single time.sleep().
"""

import time

from motors import initialize_escs, stop_all_motors
from speeds import down, forward

# ---------------------------------------------------------------------------
# Mission timing (adjust these to tune behavior)
# ---------------------------------------------------------------------------
STARTUP_WAIT = 5     # seconds to wait before the mission starts
DIVE_TIME = 5        # seconds spent diving before going forward
FORWARD_TIME = 30    # seconds spent driving forward while submerged

# ---------------------------------------------------------------------------
# Startup sequence
# ---------------------------------------------------------------------------
print(f"Waiting {STARTUP_WAIT} seconds before starting mission...")
time.sleep(STARTUP_WAIT)

initialize_escs()

print("Beginning code in 3 seconds")
time.sleep(3)

# ---------------------------------------------------------------------------
# Dive phase: submerge for a fixed duration before moving forward
# ---------------------------------------------------------------------------
print(f"Diving for {DIVE_TIME} seconds...")
down()
time.sleep(DIVE_TIME)

# ---------------------------------------------------------------------------
# Forward phase: drive forward while staying submerged
# ---------------------------------------------------------------------------
print(f"Driving forward for {FORWARD_TIME} seconds...")
forward()
time.sleep(FORWARD_TIME)

# ---------------------------------------------------------------------------
# Stop phase: mission complete, kill all thrusters
# ---------------------------------------------------------------------------
print("Mission complete, stopping thrusters")
stop_all_motors()
