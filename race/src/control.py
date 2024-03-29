#!/usr/bin/env python
import math
import rospy
from race.msg import drive_param
from race.msg import pid_input
import time

kp = 6.1
kd = 0.05
servo_offset = 18.5	# zero correction offset in case servo is misaligned.
prev_error = 0.0
angle = 0

pub = rospy.Publisher('drive_parameters', drive_param, queue_size=1)

prev_time = time.time()

def control(data):
	global prev_error
	global kp
	global kd
	global angle
        global prev_time

	## Your code goes here
	# 1. Scale the error
	error = data.pid_error
        cur_time = time.time()
	# 2. Apply the PID equation on error to compute steering
	v0 = (kp*error) + kd*(prev_error - error)/(cur_time-prev_time)
	# 3. Make sure the steering value is within bounds for talker.py
        prev_time = time.time()
	prev_error = error
	angle = -v0

	angle = angle if -100 < angle < 100 else 100 if angle > 100 else -100
	vel_input = data.pid_vel if -100 < data.pid_vel < 100 else 100 if data.pid_vel > 100 else -100
	## END

	msg = drive_param();
	msg.velocity = vel_input
	msg.angle = angle
	print "Angle:", msg.angle
	print "Velocity:", msg.velocity
        print "prev_error:", error
        print "-----------------------"
	pub.publish(msg)

if __name__ == '__main__':
	rospy.init_node('pid_controller', anonymous=True)
	rospy.Subscriber("error", pid_input, control)
	rospy.spin()
