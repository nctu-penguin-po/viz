#!/usr/bin/env python
# license removed for brevity
import cv2
import numpy as np
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Int32
from std_msgs.msg import Float32
from std_msgs.msg import Int32MultiArray 
from std_msgs.msg import Float32MultiArray 
from cv_bridge import CvBridge
import time
import os

#if __name__ == '__main__':
rospy.init_node('save_image',anonymous=True)

rate = rospy.Rate(20)
img = cv2.imread('')
flag_im = False

#cap = cv2.VideoCapture(0)
'''
cap = cv2.VideoCapture(0)
flag_im = False
'''


depth_data = np.zeros((1,8))
balance_data = np.zeros((1,8))
forward_data = np.zeros((1,8))
turn_data = np.zeros((1,8))
sum_data = np.zeros((1,8))
motor_data = np.zeros((1,8))
ft_depth_data = 0
ft_balance_data = np.zeros((1,3))
ft_forward_data = 0
ft_turn_data = 0
posture_data = np.zeros((1,3))
motor_data_2 = np.zeros((1,8))
depth_data_2 = 0
voltage_data = 0
state_data = 0
compass_yaw_data = 0

def imSub(imgmsg):
	global img, flag_img
	bridge = CvBridge()
	img = bridge.imgmsg_to_cv2(imgmsg, 'bgr8')

def ft_depth_cb(data):
	global ft_depth_data
	ft_depth_data = data.data

def ft_balance_cb(data):
	global ft_balance_data
	ft_balance = data.data
	for i in range(3):
		depth_data[0, i] = data[i]

def ft_forward_cb(data):
	global ft_forward_data
	ft_forward_data = data.data

def ft_turn_cb(data):
	global ft_turn_data
	ft_turn_data = data.data

def depth_cb(data):
	global depth_data
	data = data.data
	print('get depth')
	for i in range(8):
		depth_data[0, i] = data[i]

def balance_cb(data):
	global balance_data
	data = data.data
	for i in range(8):
		balance_data[0, i] = data[i]

def forward_cb(data):
	global forward_data
	data = data.data
	for i in range(8):
		forward_data[0, i] = data[i]

def turn_cb(data):
	global turn_data
	data = data.data
	for i in range(8):
		turn_data[0, i] = data[i]

def sum_cb(data):
	global sum_data
	data = data.data
	for i in range(8):
		sum_data[0, i] = data[i]

def motor_cb(data):
	global motor_data
	data = data.data
	for i in range(8):
		motor_data[0, i] = data[i]/100.

def compass_yaw_cb(data):
	global compass_yaw_data
	compass_yaw_data = data.data

def posture_cb(data):
	global posture_data
	posture_data = data.data
	print(posture_data)

def motor_2_cb(data):
	global motor_data_2
	data = data.data
	for i in range(8):
		motor_data_2[0, i] = data[i]/100.

def depth_2_cb(data):
	global depth_data_2
	depth_data_2=data.data

def voltage_cb(data):
	global voltage_data
	voltage_data=data.data
	
def state_cb(data):
	global state_data
	state_data=data.data		

rospy.Subscriber('/force/depth', Float32MultiArray, depth_cb)
rospy.Subscriber('/force/balance', Float32MultiArray, balance_cb)
rospy.Subscriber('/force/forward', Float32MultiArray, forward_cb)
rospy.Subscriber('/force/turn', Float32MultiArray, turn_cb)
rospy.Subscriber('/force/sum', Float32MultiArray, sum_cb)
rospy.Subscriber('/force/motor', Float32MultiArray, motor_cb)
rospy.Subscriber('/ft/depth', Float32, ft_depth_cb)
rospy.Subscriber('/ft/balance', Float32MultiArray, ft_balance_cb)
rospy.Subscriber('/ft/forward', Float32, ft_forward_cb)
rospy.Subscriber('/ft/turn', Float32, ft_turn_cb)
rospy.Subscriber('/posture', Float32MultiArray, posture_cb)
rospy.Subscriber('/depth', Float32, depth_2_cb)
rospy.Subscriber('/voltage', Float32, voltage_cb)
rospy.Subscriber('/compass_yaw', Float32, compass_yaw_cb)
rospy.Subscriber('/state', Int32, state_cb)
rospy.Subscriber('/motor', Int32MultiArray, motor_2_cb)     
rospy.Subscriber('/infront/image_raw', Image, imSub, queue_size=1, buff_size=2**24)
data_head = ['state', 'vol', 'depth', 'pos_x', 'pos_y', 'pos_z', 'compass_yaw', 'ft_depth', 'ft_balance_x', 'ft_balance_y', 'ft_balance_z', 'ft_forward', 'ft_turn']
data_head2 = ['force_depth', 'force_balance', 'force_forward', 'force_turn', 'force_motor', 'force_sum', 'motor']
for i in range(0,50):
	print('spin callback')
	rate.sleep()

	
now_time = time.strftime("%Y-%m-%d.%H-%M-%S", time.gmtime())
path = '/home/eric/image/'
os.mkdir(path+now_time)
i = 0
j = 0
f = open(path+now_time+'/'+'head', 'w')
f.write('\n'.join(data_head))  
f.write('\n')
for jj in range(len(data_head2)):
	for ii in range(8):
		f.write(data_head2[jj]+str(ii)+'\n')
f.write('\n')
f.close()
while not rospy.is_shutdown():
	name_img = path+now_time+'/'+str(i)+'.jpg'
	name_txt = path+now_time+'/'+str(j/10)

	if j%10 == 0:
		cv2.imwrite(name_img,img)
		f = open(name_txt,'w')

	
	with open(name_txt,'a') as f:
		f.write(str(state_data)+' '+str(voltage_data)+' '+str(depth_data_2)+' ')
		for num in range(3):
			f.write(str(posture_data[0, num])+' ')
		f.write(str(compass_yaw_data)+' '+str(ft_depth_data)+' '+str(ft_balance_data[0, 0])+' '+str(ft_balance_data[0, 1])+' '+str(ft_balance_data[0, 2]))
		f.write(str(ft_forward_data)+' '+str(ft_turn_data)+' ')


		for num in range(8):
			f.write(str(depth_data[0, num])+' ')	

		for num in range(8):
			f.write(str(balance_data[0, num])+' ')

		for num in range(8):
			f.write(str(forward_data[0, num])+' ')

		for num in range(8):
			f.write(str(turn_data[0, num])+' ')

		for num in range(8):
			f.write(str(motor_data[0, num])+' ')

		for num in range(8):
			f.write(str(sum_data[0, num])+' ')

		for num in range(8):
			f.write(str(motor_data_2[0, num])+' ')

		f.write('\n')

		f.close()

	print('save',j/10)

	i += 0.1
	j += 1
	time.sleep(0.1)
