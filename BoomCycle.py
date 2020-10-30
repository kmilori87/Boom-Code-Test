#deploy and retract the boom a number of times for fatigue testing
from BoomDriver import BoomDriver
import sys
import time

encoder_pins = ["P8_44", "P8_43"]
motor_pins = ["P8_29", "P8_30"]	

driver = BoomDriver(encoder_pins, motor_pins)

print('Hello World')
num_cycles = int(sys.argv[1])
num_steps = int(sys.argv[2])

for i in range(num_cycles):
	print "Starting cycle {}".format(i+1)
	driver.move_num_steps(num_steps)
	time.sleep(1)
	driver.move_num_steps(-num_steps)
	print "Completed cycle {}".format(i+1)
	time.sleep(1)