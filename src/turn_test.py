#!/usr/bin/env python
# license removed for brevity
import numpy as np
import rospy
from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray 
from std_msgs.msg import Int32MultiArray
import time

import Tkinter as tk

from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
posture_data=[0,0,0]
motor_data=[0,0,0,0,0,0,0,0]
turn_data=[0,0,0,0,0]


#if __name__ == '__main__':
def B_onclick():
    global eList
    for i in range(5):
        turn_data[i] = int(eList[i].get())
    motorrrr=Int32MultiArray(data = turn_data)
    pub1.publish(motorrrr)

win = tk.Tk()
win.title('Dummy motor')

eList = []
for i in range(5):
    L = tk.Label(win, text = 'turn'+str(i)).grid(row=i, column=0)
    e = tk.Entry(win)
    eList.append(e)
    e.grid(row=i, column=1)
    e.insert('insert', 0)
b = tk.Button(win, text = 'turn', command = B_onclick).grid(row = 5, column=0)

rospy.init_node('turn_test',anonymous=True)
pub1 = rospy.Publisher('/flag/PIDturn',Int32MultiArray,queue_size=10)
#print("posture666")



for i in range(len(turn_data)):
    turn_data[i] = 0
time.sleep(1)
motorrrr=Int32MultiArray(data = turn_data)
pub1.publish(motorrrr)

win.mainloop()
