#!/usr/bin/env python
# license removed for brevity
import serial

import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Int32MultiArray

from os import popen
import time


serial_port = popen('readlink -f /dev/serial/by-path/pci-0000\:00\:14.0-usb-0\:2\:1.0').read().split()[0] #left:2:1.0
serial_port = '/dev/ttyUSB0'
print(serial_port)
rospy.init_node('joy',anonymous=True)
ser = serial.Serial(serial_port, 57600, timeout = 1)
pub1 = rospy.Publisher('/joy/error_state',Int32,queue_size=10)
pub2 = rospy.Publisher('/joy/button',Int32MultiArray,queue_size=10)
pub3 = rospy.Publisher('/joy/right',Int32MultiArray,queue_size=10)
pub4 = rospy.Publisher('/joy/left',Int32MultiArray,queue_size=10)
pos = [0, 0, 0]
while not rospy.is_shutdown():
	start = time.time()
	a = ser.readline()
	print(a)
	if len(a) < 1:
		continue
	a = a.split()
	
	if len(a) < 8:
		continue
	button = [int(a[1]), int(a[2]), int(a[3])]
	button = Int32MultiArray(data = button)
	joy_right = [int(a[4]), int(a[5])]
	joy_right = Int32MultiArray(data = joy_right)
	joy_left  = [int(a[6]), int(a[7])]
	joy_left = Int32MultiArray(data = joy_left)
	pub1.publish(int(a[0]))
	pub2.publish(button)
	pub3.publish(joy_right)
	pub4.publish(joy_left)
	end = time.time()
	print(end-start)
