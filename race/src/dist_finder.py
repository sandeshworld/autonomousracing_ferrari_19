#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from race.msg import drive_values
from race.msg import pid_input

# Some useful variable declarations.
angle_range = 240	# sensor angle range of the lidar
car_length = 2	# distance (in m) that we project the car forward for correcting the error. You may want to play with this.
desired_distance = 0.9 # distance from the wall (left or right - we cad define..but this is defined for right). You should try different values
vel = 10		# this vel variable is not really used here.
error = 0.0
stopped = 0
go_left = True

pub = rospy.Publisher('error', pid_input, queue_size=1)


def getError(theta, a, b):
	global car_length
	swing = math.radians(theta)

	## Your code goes here to compute alpha, AB, and CD..and finally the error.
	alpha = math.atan((a*math.cos(swing) - b)/(a*math.sin(swing)))
	ab = b*math.cos(alpha)
	desired_trajectory = desired_distance - ab
	cd = ab + car_length*math.sin(alpha)
	return desired_trajectory - cd
	

##	Input: 	data: Lidar scan data
##			theta: The angle at which the distance is requried
##	OUTPUT: distance of scan at angle theta

def getRange(data, theta):
	# Find the index of the arary that corresponds to angle theta.
	# Return the lidar scan value at that index
	# Do some error checking for NaN and ubsurd values

	# assuming angle_min = 0, angle_max = 240, angle_increment = 1
	index = int((theta + 30)*3.025)
        while math.isnan(data.ranges[index]): 
       		index+=1
                if index > 720:
                	return 10
        return data.ranges[index]

"""for i in range(1,10,2):
		dist_list = [data.ranges[index + j] for j in range(-2*i, 2*i + 1)]
		dist_list = [1 if math.isnan(dist) else dist for dist in dist_list]  # filter NaN
		#if len(dist_list) == 0:
		#	continue  # increase the range we're scanning and try again
		print("List:", dist_list)
		return sorted(dist_list)[len(dist_list)//2]
	print("Everythig was NaN")

        
	return -0.5  # TODO change this

"""
def callback(data):
	global car_length
	global stopped
	global go_left
	global vel

	theta1 = 70
	theta2 = 60
	a1 = getRange(data, theta1)
	a2 = getRange(data, theta2)
	b = getRange(data,0)	# Note that the 0 implies a horizontal ray..the actual angle for the LIDAR may be 30 degrees and not 0.
	c = getRange(data, 90)  # is there something directly in front of the car?
	# d = getRange(data, 180)  # is there something directly in front of the car?

	msg = pid_input()
	if c < 0.7:
		stopped += 1
		if 20 <= stopped < 35:
			print "Chill out"
			msg.pid_vel = 0
			msg.pid_error = 0
		elif 35 <= stopped < 50:
			if stopped == 35:
				go_left = c < getRange(data, 80)
			print "back up"
			msg.pid_vel = -20
			msg.pid_error = 2 if go_left else -2
		# elif stopped > 60:
		#	print "Give up"
		#	msg.pid_vel = 0
		#	msg.pid_error = 0
		else:
			print "Avoid obstacle!"
			msg.pid_vel = 7
			msg.pid_error = 2
		pub.publish(msg)
		return
	elif stopped > 20 or stopped < 0:
		stopped = -15 if stopped > 0 else stopped + 1
		print "Waiting..."
		msg.pid_vel = stopped * -1
		msg.pid_error = 0
		pub.publish(msg)
		return
	else: 
		stopped = 0
	

	## END
	error1 = getError(theta1, a1, b)
	error2 = getError(theta2, a2, b)
	error =  (2*error1 + 2*error2)/4
	print("Error:", error)
	msg.pid_error = error		# this is the error that you wantt o send to the PID for steering correction.
	msg.pid_vel = vel if c > 2.5 and (-0.1 > error or error > 0.1) else 15 # velocity error is only provided as an extra credit field.
	pub.publish(msg)


if __name__ == '__main__':
	print("Laser node started")
	rospy.init_node('dist_finder',anonymous = True)
	rospy.Subscriber("scan",LaserScan,callback)
        
        rospy.spin()
        
