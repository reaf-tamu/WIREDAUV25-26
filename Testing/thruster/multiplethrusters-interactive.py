import time
from adafruit_servokit import ServoKit

# Initialize PCA9685 with 16 channels
kit = ServoKit(channels=16)


class Motor:
    def __init__(self, channel):
        self.channel = channel
        self.speed = 90  # Neutral
        self.prev_speed = None

        # Set PWM range for Blue Robotics ESCs
        kit.servo[self.channel].set_pulse_width_range(1100, 1900)

    def set_speed(self, angle):
        self.speed = angle

    def run(self):
        if self.prev_speed != self.speed:
            print(f"Channel {self.channel}: Sending {self.speed}°")
            kit.servo[self.channel].angle = self.speed
            self.prev_speed = self.speed

    def stop(self):
        self.set_speed(90)
        self.run()


if __name__ == "__main__":
    print("=========================================")
    print("      AUV THRUSTER INDIVIDUAL TESTER      ")
    print("=========================================")
    print("Ensure the main thruster battery is disconnected until")
    print("the script initializes all selected channels to 90°.")
    print("-----------------------------------------")

    active_thrusters = []

    try:
        while True:

            # --------------------------
            # Select one or more channels
            # --------------------------
            user_input = input(
                "\nEnter PCA9685 channel(s) to test (0-15).\n"
                "Separate multiple channels with commas.\n"
                "Example: 0,1,4,7\n"
                "Or enter 'q' to quit: "
            ).strip()

            if user_input.lower() == "q":
                print("Exiting test suite.")
                break

            try:
                # Accept commas or spaces
                channel_list = [
                    int(ch.strip())
                    for ch in user_input.replace(" ", ",").split(",")
                    if ch.strip()
                ]

                # Remove duplicates while preserving order
                channel_list = list(dict.fromkeys(channel_list))

                if len(channel_list) == 0:
                    raise ValueError

                for ch in channel_list:
                    if ch < 0 or ch > 15:
                        raise ValueError

            except ValueError:
                print("Error: Please enter valid channel numbers between 0 and 15.")
                continue

            # --------------------------
            # Ask run time
            # --------------------------
            try:
                run_time = float(
                    input("Enter how many seconds to run the thruster(s): ")
                )

                if run_time <= 0:
                    print("Run time must be greater than zero.")
                    continue

            except ValueError:
                print("Please enter a valid number.")
                continue

            print(f"\n--- Starting Test on Channels {channel_list} ---")

            # Create motors
            active_thrusters = [Motor(ch) for ch in channel_list]

            # --------------------------
            # Arm ESCs
            # --------------------------
            print("Step 1: Arming ESCs at neutral (90°)...")

            for thruster in active_thrusters:
                thruster.set_speed(90)
                thruster.run()

            print("Waiting 5 seconds for ESCs to arm...")
            time.sleep(5)

            # --------------------------
            # Spin Forward
            # --------------------------
            print(f"Step 2: Running thrusters forward for {run_time} seconds...")

            for thruster in active_thrusters:
                thruster.set_speed(100)
                thruster.run()

            time.sleep(run_time)

            # --------------------------
            # Stop
            # --------------------------
            print("Step 3: Stopping thrusters...")

            for thruster in active_thrusters:
                thruster.stop()

            print(f"--- Test Complete for Channels {channel_list} ---")

            active_thrusters = []

    except KeyboardInterrupt:
        print("\nTesting interrupted by user.")

    finally:
        print("Stopping any active thrusters...")

        for thruster in active_thrusters:
            thruster.stop()

        time.sleep(1)
        print("Safely exited.")
