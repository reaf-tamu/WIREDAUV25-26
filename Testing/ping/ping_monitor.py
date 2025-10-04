#!/usr/bin/env python3   # tells Linux to use Python 3 to run this script

import time              # lets us pause between readings
from brping import Ping1D  # import the Ping1D class from the brping library (controls the sonar)

# ------------------- SETTINGS -------------------
PORT = "/dev/ttyUSB0"     # this is where the Ping1D sonar is connected (USB serial port)
BAUD = 9600               # the communication speed between the Jetson and Ping1D
CONFIDENCE_MIN = 50       # ignore readings that have less than 50% confidence
HZ = 2                    # how many readings to take per second (2 Hz = every 0.5 seconds)
# ------------------------------------------------


def connect_ping(port=PORT, baud=BAUD):
    """
    Connect to the Ping1D sonar using the specified port and baud rate.
    Returns a Ping1D object if successful.
    """
    p = Ping1D()   # create a Ping1D object (represents our sonar)
    print(f"[Ping1D] Connecting on {port} @ {baud} ...")   # print connection info

    # try to connect over serial port
    if not p.connect_serial(port, baud):
        # if connection fails, raise an error and stop program
        raise RuntimeError(f"Could not connect to Ping1D on {port}")

    # if we reach this line, connection worked
    print("[Ping1D] Connected successfully.")
    return p  # return the connected Ping1D object to the caller


def get_distance_m(p):
    """
    Ask the sonar for one distance measurement.
    Returns (distance_in_meters, confidence_percent)
    or (None, None) if it fails.
    """
    try:
        # ask Ping1D for distance data (returns dictionary)
        data = p.get_distance()

        # if no data was returned, something went wrong
        if not data:
            return None, None

        # 'distance' is in millimeters — convert to meters by dividing by 1000
        # 'confidence' is the sonar’s confidence in this reading (0–100%)
        return data["distance"] / 1000.0, data["confidence"]

    # if an error occurs (for example, sensor disconnected), catch it here
    except Exception as e:
        print(f"[Ping1D][ERROR] {e}")
        return None, None


def main():
    """
    Main function — connects to the sonar and prints distance repeatedly.
    """
    try:
        # try connecting to Ping1D using the settings above
        ping = connect_ping()
    except RuntimeError as e:
        # if it fails, print why and stop
        print(f"[FATAL] {e}")
        return

    # calculate how long to wait between readings
    period = 1.0 / HZ

    print("[Ping1D] Streaming distance data — press Ctrl+C to stop.")

    try:
        # infinite loop — keeps reading data until you stop the program
        while True:
            # get one distance reading
            dist, conf = get_distance_m(ping)

            # check if reading was invalid
            if dist is None:
                print("[WARN] No data received.")
            # check if confidence is too low
            elif conf < CONFIDENCE_MIN:
                print(f"[LOW CONFIDENCE] {conf}% — ignoring this measurement.")
            else:
                # valid reading — print distance in meters and confidence
                print(f"Distance to floor: {dist:.3f} m | Confidence: {conf}%")

            # wait before next reading
            time.sleep(period)

    # this runs if you press Ctrl+C to stop the script
    except KeyboardInterrupt:
        print("\n[EXIT] Stopped by user.")

    finally:
        # cleanly disconnect sonar when program exits
        try:
            ping.disconnect()
        except Exception:
            pass
        print("[Ping1D] Disconnected cleanly.")


# Python runs this block only if you execute the script directly
if __name__ == "__main__":
    main()
