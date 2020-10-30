import time
import Adafruit_BBIO.GPIO as GPIO
import sys

class BoomDriver(object):
	def __init__(self, encoder_pins, motor_pins):
		#This class is responsible for controlling the boom deployment
		#inputs:
			#encoder_pins: 1 by 2 array containing the names of the encoder pins [A,B]
			#motor_pins: 1 by 2 array containing the names of the motor pins [+,-]
		self.encoder_pins = encoder_pins
		self.motor_pins = motor_pins
		GPIO.cleanup()
		for i in range(2):
			#set the pins as inputs or outputs
			GPIO.setup(self.encoder_pins[i], GPIO.IN)
			GPIO.setup(self.motor_pins[i], GPIO.OUT)

	def drive_motor(self, direction):
		#This function actually drives the motor
		#inputs:
			#direction: 1 to drive the motor out, 0 to retract it
		if direction == 1: #deploy out
			GPIO.output(self.motor_pins[1], GPIO.LOW)
			GPIO.output(self.motor_pins[0], GPIO.HIGH)
		elif (direction == 0): #retract in
			#retract by switching the pin polarity
			GPIO.output(self.motor_pins[0], GPIO.LOW)
			GPIO.output(self.motor_pins[1], GPIO.HIGH)
		else: #stop motor
			#turn both pins off to stop motor
			GPIO.output(self.motor_pins[0], GPIO.LOW)
			GPIO.output(self.motor_pins[1], GPIO.LOW)

	def move_nun_steps(self, num_steps):
		#Move the motor until the encoder turns a given number of steps relative to current position
		#inputs:
			#num_steps: number of encoder steps relative to current position
				#can be positive or negative
		print "System moving {} steps".format(num_steps)
		cur_step_count = 0
		sample_delay = 0.01 #seconds to wait before next sample
		if num_steps >= 0:
			direction = 1 #deploy out
		elif num_steps <= 0:
			direction = 0 #retract in
		else:
			direction = -1 #don't run the motor

		encoder_a_last = GPIO.input(self.encoder_pins[0])
		self.drive_motor(direction)
		while(cur_step_count < num_steps and direction == 1) or (cur_step_count > num_steps and direction == 0):
			#keep looking until desired step count reached
			encoder_a = GPIO.input(self.encoder_pins[0])
			encoder_b = GPIO.input(self.encoder_pins[1])	
			print "Encoder a: {}, Encoder b: {}".format(encoder_a, encoder_b)
			#Update if the A channel hits a rising edge. The B channel determines the rotation direction
			if(encoder_a == 1 and encoder_a_last == 0):
				#Encoder moving in
				if encoder_b == 1:
					cur_step_count = cur_step_count - 1
				#Encoder moving out
				else:
					cur_step_count = cur_step_count + 1

			print "Encoder counts: {}".format(cur_step_count)

			#Update the last value of Encoder A
			encoder_a_last = encoder_a
			time.sleep(sample_delay)
		self.drive_motor(-1) #stop motor

	if __name__ == "__main__":
		deployer_num = int(sys.argv[1])
		num_steps = int(sys.argv[2])
		encoder_pins = []
		motor_pins = []
		if deployer_num == 1:
			encoder_pins = ["P8_44", "P8_43"]
			motor_pins = ["P8_29", "P8_30"]	