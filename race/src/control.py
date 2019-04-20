#!/usr/bin/env python
import math
import rospy
from race.msg import drive_param
from race.msg import pid_input

kp = 14.0
kd = 0.09
servo_offset = 18.5	# zero correction offset in case servo is misaligned.
prev_error = 0.0
vel_input = 25.0	# arbitrarily initialized. 25 is not a special value. This code can input desired velocity from the user.
angle = 90

pub = rospy.Publisher('drive_parameters', drive_param, queue_size=1)

def control(data):
	global prev_error
	global vel_input
	global kp
	global kd
	global angle

	## Your code goes here
	# 1. Scale the error
	error = data.pid_error
	# 2. Apply the PID equation on error to compute steering
	v0 = (kp*error) + kd*(prev_error - error)
	# 3. Make sure the steering value is within bounds for talker.py

	prev_error = error
	angle = angle - v0

	angle = angle if -100 < angle < 100 else 100 if angle > 100 else -100
	vel_input = vel_input if -100 < vel_input < 100 else 100 if vel_input > 100 else -100

	## END

	msg = drive_param();
	msg.velocity = vel_input
	msg.angle = angle
	pub.publish(msg)

if __name__ == '__main__':
	global kp
	global kd
	global vel_input
	print("Listening to error for PID")
	kp = input("Enter Kp Value: ")
	kd = input("Enter Kd Value: ")
	vel_input = input("Enter Velocity: ")
	rospy.init_node('pid_controller', anonymous=True)
	rospy.Subscriber("error", pid_input, control)
	rospy.spin()