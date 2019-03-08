#!/usr/bin/env python
# license removed for brevity
import serial

import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Int32MultiArray
import Tkinter as tk

rospy.init_node('tkcontrol',anonymous=True)

pub0 = rospy.Publisher('/trigger_command',Int32,queue_size=10)
pub1 = rospy.Publisher('/state',Int32,queue_size=10)
pub2 = rospy.Publisher('/joy/button',Int32MultiArray,queue_size=10)
pub3 = rospy.Publisher('/joy/right',Int32MultiArray,queue_size=10)
pub4 = rospy.Publisher('/joy/left',Int32MultiArray,queue_size=10)

win = tk.Tk()
win.title('tkcontrol')
win.geometry('300x400')

state_data = 0

def reset_onclick():
    global state_data
    state_data = 0
    pub1.publish(state_data)
    sL.config(text = str(state_data))
    pub0.publish(0)

def depthS_onclick():
    global state_data
    state_data = state_data^1
    pub1.publish(state_data)
    sL.config(text = str(state_data))
    if state_data%2 == 1:
        L2.config(text = 'ON', bg = 'green')
    else:
        L2.config(text = 'OFF', bg = 'red')
    pub0.publish(0)
        
def balanceS_onclick():
    global state_data
    state_data = state_data^2
    pub1.publish(state_data)
    sL.config(text = str(state_data))
    if (state_data >> 1)%2 == 1:
        L3.config(text = 'ON', bg = 'green')
    else:
        L3.config(text = 'OFF', bg = 'red')
    pub0.publish(0)

def forwardSt_onclick():
    global state_data
    state_data = state_data^4
    pub1.publish(state_data)
    sL.config(text = str(state_data))
    if (state_data >> 2)%2 == 1:
        L4.config(text = 'ON', bg = 'green')
    else:
        L4.config(text = 'OFF', bg = 'red')
    pub0.publish(0)

def forwardM_onclick():
    pd= [0, 0, 8]
    pub_data = Int32MultiArray(data = pd)
    pub2.publish(pub_data)
    pub0.publish(0)

def turnSt_onclick():
    print('123')
    global state_data
    state_data = state_data^8
    pub1.publish(state_data)
    sL.config(text = str(state_data))
    if (state_data >> 3)%2 == 1:
        L5.config(text = 'ON', bg = 'green')
    else:
        L5.config(text = 'OFF', bg = 'red')
    pub0.publish(0)
    
def turnM_onclick():
    pd= [0, 0, 1]
    pub_data = Int32MultiArray(data = pd)
    pub2.publish(pub_data)
    pub0.publish(0)
    
def forwardG_onclick():
    pd= [0, 1]
    pub_data = Int32MultiArray(data = pd)
    pub4.publish(pub_data)
    pub0.publish(0)

def forwardS_onclick():
    pd= [0, 0]
    pub_data = Int32MultiArray(data = pd)
    pub4.publish(pub_data)
    pub0.publish(0)

def turnR_onclick():
    pd= [1, 0]
    pub_data = Int32MultiArray(data = pd)
    pub3.publish(pub_data)
    pub0.publish(0)

def turnS_onclick():
    pd= [0, 0]
    pub_data = Int32MultiArray(data = pd)
    pub3.publish(pub_data)
    pub0.publish(0)

def turnL_onclick():
    pd= [-1, 0]
    pub_data = Int32MultiArray(data = pd)
    pub3.publish(pub_data)
    pub0.publish(0)

b1 = tk.Button(win, text = 'reset', command = reset_onclick).grid(row = 0, column=0)

sL = tk.Label(win, text = '', bg = 'white')
sL.grid(row = 0, column=2)

b2 = tk.Button(win, text = 'depth', command = depthS_onclick).grid(row = 1, column=0)

L2 = tk.Label(win, text = 'OFF', bg = 'red')
L2.grid(row = 1, column=2)

b3 = tk.Button(win, text = 'balance', command = balanceS_onclick).grid(row = 2, column=0)

L3 = tk.Label(win, text = 'OFF', bg = 'red')
L3.grid(row = 2, column=2)

b4 = tk.Button(win, text = 'forward', command = forwardSt_onclick).grid(row = 3, column=0)
b41 = tk.Button(win, text = 'autoSwitch', command = forwardM_onclick).grid(row = 3, column=1)

L4 = tk.Label(win, text = 'OFF', bg = 'red')
L4.grid(row = 3, column=2)

b5 = tk.Button(win, text = 'turn', command = turnSt_onclick).grid(row = 4, column=0)
b51 = tk.Button(win, text = 'autoSwitch', command = turnM_onclick).grid(row = 4, column=1)

L5 = tk.Label(win, text = 'OFF', bg = 'red')
L5.grid(row = 4, column=2)

b61 = tk.Button(win, text = 'forward GO', command = forwardG_onclick).grid(row = 5, column=0)
b6s = tk.Button(win, text = 'forward stop', command = forwardS_onclick).grid(row = 5, column=1)

b71 = tk.Button(win, text = 'turn left', command = turnL_onclick).grid(row = 6, column=0)
b7s = tk.Button(win, text = 'turn stop', command = turnS_onclick).grid(row = 6, column=1)
b72 = tk.Button(win, text = 'turn right', command = turnR_onclick).grid(row = 6, column=2)
win.mainloop()
