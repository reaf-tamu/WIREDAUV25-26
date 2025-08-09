import time
from brping import Ping1D

# function or in sub?
"""
class PingSensor
    def __init__(self, port="/dev/ttyUSB0", baudrate=9600):
        self.ping = Ping1D()
        print(f"Connecting to Ping1D on {port}...")
        if not self.ping.connect_serial(port, baudrate):
            raise RuntimeError(f"Failed to connect to Ping1D on {port}")
        print("Ping1D connected successfully.")
"""

    def get_distance(self):
        try:
            data = self.ping.get_distance()
            if data:
                distance_m = data["distance"] / 1000.0  # mm to meters
                confidence = data["confidence"]
                return distance_m, confidence
            else:
                return None, None
        except Exception as e:
            print(f"[ERROR] get_distance failed: {e}")
            return None, None

    def disconnect(self):
        try:
            self.ping.disconnect()
            print("Ping1D disconnected.")
        except Exception as e:
            print(f"[ERROR] while disconnecting: {e}")

def main():
    TARGET_DEPTH = 1.0    # meters
    TOLERANCE = 0.1       # meters
    CONFIDENCE_THRESHOLD = 50  # ignore low-confidence measurements

    try:
        ping_sensor = PingSensor(port="/dev/ttyUSB0", baudrate=9600)
    except RuntimeError as e:
        print(f"[FATAL] Could not initialize Ping sensor: {e}")
        return

    try:
        while True:
            distance, confidence = ping_sensor.get_distance()
            if distance is not None:
                if confidence < CONFIDENCE_THRESHOLD:
                    print(f"Low confidence ({confidence}%), ignoring measurement.")
                    time.sleep(1)
                    continue

                print(f"Depth: {distance:.2f} m | Confidence: {confidence}%")

                # hover logic
                if distance < TARGET_DEPTH - TOLERANCE:
                    print("Too shallow, go down.")
                elif distance > TARGET_DEPTH + TOLERANCE:
                    print("Too deep, go up.")
                else:
                    print("Within hover band, maintain position.")
            else:
                print("[WARN] Failed to read distance data.")

            time.sleep(1)

    except KeyboardInterrupt:
        print("Terminated by user.")
    except Exception as e:
        print(f"[FATAL] Unexpected error: {e}")
    finally:
        ping_sensor.disconnect()

if __name__ == "__main__":
    main()
