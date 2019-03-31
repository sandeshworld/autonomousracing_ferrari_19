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
pub = rospy.Publisher('drive_parameters', drive_param, queue_size=10)

stdscr.refresh()

delta = None

key = ''
while key != ord('q'):
	key = stdscr.getch()
	stdscr.refresh()

        if key == ord(' '):  # this key will center the steer and throttle
            forward = 0
            left = 0
            delta = None
        elif key == curses.KEY_UP or key == curses.KEY_DOWN or key == curses.KEY_LEFT or key == curses.KEY_RIGHT:
            if delta is None:
                delta = 1  # first press of a movement key
            else:
                delta += 1  # building on previous key presses

            if key == curses.KEY_UP:
                forward += delta 
            elif key == curses.KEY_DOWN:
                forward -= delta
            if key == curses.KEY_LEFT:
                left += delta
            elif key == curses.KEY_RIGHT:
                left -= delta
        else:
            delta = None

	msg = drive_param()
	msg.velocity = forward if -100 <= forward <= 100 else -100 if forward < 0 else 100
	msg.angle = left if -100 <= left <= 100 else -100 if left < 0 else 100
	pub.publish(msg)

curses.endwin()
