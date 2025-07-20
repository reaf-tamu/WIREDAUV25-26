

class PIDController:
	def __init__(self, Kp, Ki, Kd, desire):
		self.Kp = Kp
		self.Ki = Ki
		self.Kd = Kd
		self.desire = desire
		self.previous_error = 0
		self.integral = 0

	def compute(self, real, dt):
		# Calculate error
		error = self.desire - real

		# Proportional term
		P_out = self.Kp * error

		# Integral term
		self.integral += error * dt
		I_out = self.Ki * self.integral

		# Derivative term
		derivative = (error - self.previous_error) / dt
		D_out = self.Kd * derivative

		# Compute total output
		output = P_out + I_out + D_out

		# Update previous error
		self.previous_error = error

		return output
