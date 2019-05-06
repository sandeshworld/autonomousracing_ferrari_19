#!/usr/bin/env python

import rospy
from race.msg import drive_param # import the custom message
import curses
forward = 0
left = 0

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)
rospy.init_node('keyboard_talker', anonymous=True)
pub = rospy.Publisher('drive_parameters', drive_param, queue_size=1)

stdscr.refresh()

forward_delta = 1
left_delta = 10

key = ''
while key != ord('q'):
	key = stdscr.getch()
	stdscr.refresh()

        if key == ord(' '):  # this key will center the steer and throttle
            forward = 0
            left = 0
        elif key == curses.KEY_UP:
            if -7 < forward < 7:
                forward = 7
            elif forward + forward_delta >= 100:
		forward = 100
            else:
                forward += forward_delta
        elif key == curses.KEY_DOWN:
            if -7 < forward < 7:
                forward = -7
            elif forward - forward_delta <= -100:
		forward = -100
            else:
                forward -= forward_delta
        elif key == curses.KEY_LEFT:
            if left - left_delta <= -100:
                left = -100
            else:
                left -= left_delta
        elif key == curses.KEY_RIGHT:
            if left + left_delta >= 100:
                left = 100
            else:
                left += left_delta
        else:
            print("Invalid key press")

	msg = drive_param()
	msg.velocity = forward
	msg.angle = left
	pub.publish(msg)

curses.endwin()
