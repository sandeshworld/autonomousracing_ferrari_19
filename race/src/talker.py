#!/usr/bin/env python

import rospy
from race.msg import drive_values
from race.msg import drive_param


"""
What you should do:
 1. Subscribe to the keyboard messages (If you use the default keyboard.py, you must subcribe to "drive_paramters" which is publishing messages of "drive_param")
 2. Map the incoming values to the needed PWM values
 3. Publish the calculated PWM values on topic "drive_pwm" using custom message drive_values
"""

varP = drive_values()
varP.pwm_drive = 9830
varP.pwn_angle = 9830

def fnc_callback(msg):
    # mapping function
    global varP
    varP.pwm_drive = int((msg.velocity * 32.76) + 9830)
    varP.pwm_angle = int((msg.angle * 32.76) + 9830)


if __name__=='__main__':
    rospy.init_node('pub_n_sub')

    pub=rospy.Publisher('drive_pwm', drive_values, queue_size=1)
    sub=rospy.Subscriber('drive_parameters', drive_param, fnc_callback)
    rate=rospy.Rate(10)


    while not rospy.is_shutdown():
	pub.publish(varP)
        rate.sleep()
