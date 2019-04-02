#!/usr/bin/env python

import rospy
from race.msg import drive_values
from race.msg import drive_param
import subprocess
import signal

"""
What you should do:
 1. Subscribe to the keyboard messages (If you use the default keyboard.py, you must subcribe to "drive_paramters" which is publishing messages of "drive_param")
 2. Map the incoming values to the needed PWM values
 3. Publish the calculated PWM values on topic "drive_pwm" using custom message drive_values
"""

class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException


signal.signal(signal.SIGALRM, timeout_handler)
varP = drive_values()
varP.pwm_drive = 9830
varP.pwm_angle = 9830


def check_connection():
    address = '192.168.1.31'
    signal.alarm(1)
    try:
        res = subprocess.call(['ping','-c','1',address])
        return res == 0
    except TimeoutException:
        return False


def fnc_callback(msg):
    # mapping function
    global varP
    varP.pwm_drive = int((msg.velocity * 32.76) + 9830)
    varP.pwm_angle = int((msg.angle * 32.76) + 9830)
        
if __name__=='__main__':
    k = 1
    rospy.init_node('pub_n_sub')

    pub=rospy.Publisher('drive_pwm', drive_values, queue_size=1)
    sub=rospy.Subscriber('drive_parameters', drive_param, fnc_callback)
    rate=rospy.Rate(60)

    while not rospy.is_shutdown():
        if k % 20 == 0:
            if not check_connection():
                varP.pwm_drive=9830
                varP.pwm_angle=9830
                pub.publish(varP)
                exit()
        k += 1
	pub.publish(varP)
        rate.sleep()

