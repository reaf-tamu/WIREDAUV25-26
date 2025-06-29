from vnpy import VnSensor
import time

class VectorNavHeading:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200):
        self.vn = VnSensor()
        print(f"Connecting to VectorNav on {port}...")
        self.vn.connect(port, baudrate)
        print("VectorNav connected successfully.")
        self.origin = None
        self.bound = 10  # degrees left/right from origin, can adjust later

    def get_heading(self):
        try:
            orientation = self.vn.read_yaw_pitch_roll()
            heading = orientation.x  # yaw in degrees
            return heading
        except Exception as e:
            print(f"[ERROR] Could not read heading: {e}")
            return None

    def calibrate_origin(self, samples=5):
        headings = []
        print("Calibrating origin heading...")
        for i in range(samples):
            heading = self.get_heading()
            if heading is not None:
                headings.append(heading)
                print(f"Sample {i+1}: {heading:.2f}")
            time.sleep(0.5)
        if headings:
            self.origin = sum(headings) / len(headings)
            print(f"Origin heading set to {self.origin:.2f}")
        else:
            raise RuntimeError("Could not calibrate origin -- no heading data.")

    def check_orientation(self, heading):
        left_bound = self.origin - self.bound
        right_bound = self.origin + self.bound
        
        if origin >= 0:
        	left_range = self.origin - 180
        	right_range = (self.origin + 180) - 360
        elif origin < 0:
        	left_range = (self.origin - 180) + 360
        	right_range = self.origin + 180
        

        # handle wrap-around properly - these values will never be achieved (-180 to 180)
        """
        if heading > 180:
            heading -= 360
        elif heading < -180:
            heading += 360
        """
        


        if (heading < left_bound):
            print(f"Heading {heading:.2f} outside left bound ({left_bound:.2f}), turn right.")
        elif heading > right_bound:
            print(f"Heading {heading:.2f} outside right bound ({right_bound:.2f}), turn left.")
        else:
            print(f"Heading {heading:.2f} within bounds, hold course.")

    def run(self):
        try:
            while True:
                heading = self.get_heading()
                if heading is not None:
                    self.check_orientation(heading)
                else:
                    print("No heading data available.")
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("Stopped by user.")
        finally:
            self.vn.disconnect()
            print("VectorNav disconnected.")

if __name__ == "__main__":
    vn_heading = VectorNavHeading(port="/dev/ttyUSB0", baudrate=115200)
    vn_heading.calibrate_origin(samples=5)
    vn_heading.run()
