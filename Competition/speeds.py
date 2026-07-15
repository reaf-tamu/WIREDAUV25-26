"""
Movement presets for the AUV.

Each function sets a combination of thruster speeds to produce a basic
maneuver (hover, turn, drive forward, dive, surface). Motors are imported
from motors.py so this file and the main mission script both control the
same physical thrusters.

Speed reference (Motor.speed is a servo angle, 90 = neutral):
  - Vertical thrusters (A2, A3, M2, M3): >90 pushes down, <90 pushes up
  - Horizontal thrusters (A1, A4, M1, M4): differential speed = turning
"""

from motors import A1, A2, A3, A4, M1, M2, M3, M4

# The robot is positively buoyant, so it needs a constant downward push just
# to hold depth while moving -- otherwise it drifts back up once it's
# underway. This is added to the vertical thrusters during forward().
# Tune this value based on testing: higher = pushes down harder.
FORWARD_DOWN_BIAS = 97


def hover():
    """Small, roughly balanced push on the vertical thrusters to hold depth."""
    print("hovering")
    A2.set_speed(95)
    A3.set_speed(95)
    M2.set_speed(95)
    M3.set_speed(95)
    A2.run()
    A3.run()
    M2.run()
    M3.run()


def right():
    """Turn right by driving the port/starboard horizontal thrusters unevenly."""
    print("turning right")
    A1.set_speed(80)
    A4.set_speed(100)
    M1.set_speed(100)
    M4.set_speed(80)
    A1.run()
    A4.run()
    M1.run()
    M4.run()


def left():
    """Turn left by driving the port/starboard horizontal thrusters unevenly."""
    print("turning left")
    A1.set_speed(100)
    A4.set_speed(80)
    M1.set_speed(80)
    M4.set_speed(100)
    A1.run()
    A4.run()
    M1.run()
    M4.run()


def forward():
    """Drive straight ahead, with a constant downward bias on the vertical
    thrusters to counteract positive buoyancy so it doesn't float up while
    underway."""
    print("going forward")
    A1.set_speed(80)
    A4.set_speed(80)
    M1.set_speed(100)
    M4.set_speed(100)
    A2.set_speed(FORWARD_DOWN_BIAS)
    A3.set_speed(FORWARD_DOWN_BIAS)
    M2.set_speed(FORWARD_DOWN_BIAS)
    M3.set_speed(FORWARD_DOWN_BIAS)
    A1.run()
    A4.run()
    M1.run()
    M4.run()
    A2.run()
    A3.run()
    M2.run()
    M3.run()


def down():
    """Dive: push all vertical thrusters downward."""
    print("going down")
    A2.set_speed(100)
    A3.set_speed(100)
    M2.set_speed(100)
    M3.set_speed(100)
    A2.run()
    A3.run()
    M2.run()
    M3.run()


def up():
    """Surface: pull all vertical thrusters upward."""
    print("going up")
    A2.set_speed(80)
    A3.set_speed(80)
    M2.set_speed(80)
    M3.set_speed(80)
    A2.run()
    A3.run()
    M2.run()
    M3.run()
