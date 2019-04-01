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
            else:
                forward += forward_delta 
        elif key == curses.KEY_DOWN:
            if -7 < forward < 7:
                forward = -7
            else:
                forward -= forward_delta 
        elif key == curses.KEY_LEFT:
            left -= left_delta
        elif key == curses.KEY_RIGHT:
            left += left_delta
        else:
            print("Invalid key press")

	msg = drive_param()
	msg.velocity = forward if -100 <= forward <= 100 else -100 if forward < 0 else 100
	msg.angle = left if -100 <= left <= 100 else -100 if left < 0 else 100
	pub.publish(msg)

curses.endwin()
