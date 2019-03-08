#!/usr/bin/env python
# license removed for brevity

import numpy as np
import pylab as plt
import time

import rospy
from std_msgs.msg import Float32
from std_msgs.msg import Int32
from std_msgs.msg import Float32MultiArray 
from std_msgs.msg import Int32MultiArray
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats

import Tkinter as tk

def FtoS(v):
    if abs(v) > 1:
        return '%5f' % v
    if abs(v) > 0.0001:
        return '%.5f' % v
    return '%.2e' % v

def ItoS(v):
    return '%5d' % v

def handle_updateI(data, t):
    global labelList
    data = data.data
    for i in range(8):
        labelList[i][t].config(text = ItoS(data[i]))

def handle_update(data, t):
    global labelList
    data = data.data
    for i in range(8):
        if abs(data[i]) < 0.5:
            b = 'white'
        elif abs(data[i]) > 20:
            b = 'red'
        elif data[i] > 0:
            b = 'green'
        else:
            b = 'blue'
        labelList[i][t].config(text = FtoS(data[i]), bg = b)

def fdepth_cb(data):
    handle_update(data, 0)


def fbalance_cb(data):
    handle_update(data, 1)
        
def fforward_cb(data):
    handle_update(data, 2)
        
def fturn_cb(data):
    handle_update(data, 3)
    
def fsum_cb(data):
    handle_update(data, 4)
    
def fmotor_cb(data):
    handle_updateI(data, 5)

def jfdepth_cb(data):
    global inforLabelList4
    data = data.data
    if data == 0:
        inforLabelList4[0].config(text = 'auto', bg = 'green')
    elif data == 1:
        inforLabelList4[0].config(text = 'manual', bg = 'blue')

def jfbalance_cb(data):
    global inforLabelList4
    data = data.data
    if data == 0:
        inforLabelList4[1].config(text = 'auto', bg = 'green')
    elif data == 1:
        inforLabelList4[1].config(text = 'manual', bg = 'blue')
        
def jfforward_cb(data):
    global inforLabelList4
    data = data.data
    if data == 0:
        inforLabelList4[2].config(text = 'auto', bg = 'green')
    elif data == 1:
        inforLabelList4[2].config(text = 'manual', bg = 'blue')
        
def jfturn_cb(data):
    global inforLabelList4
    data = data.data
    if data == 0:
        inforLabelList4[3].config(text = 'auto', bg = 'green')
    elif data == 1:
        inforLabelList4[3].config(text = 'manual', bg = 'blue')

def depth_cb(data):
    global inforLabelList
    data = data.data
    inforLabelList[0].config(text = str(data))

def posture_cb(data):
    global inforLabelList
    data = data.data
    s = 'row:'+FtoS(data[0])+'\npitch:'+FtoS(data[1])+'\nyaw: '+FtoS(data[2])
    inforLabelList[1].config(text = s)

def voltage_cb(data):
    global inforLabelList
    data = data.data
    inforLabelList[2].config(text = str(data))
    
def time_cb(data):
    global inforLabelList
    data = data.data
    inforLabelList[3].config(text = FtoS(data))

def block_cb(data):
    global inforLabelList
    data = data.data
    inforLabelList[4].config(text = FtoS(data))

def state_cb(data):
    global inforLabelList
    data = data.data
    inforLabelList[5].config(text = ItoS(data))

def joy_state_cb(data):
    global inforLabelList2
    data = data.data
    inforLabelList2[0].config(text = ItoS(data))
    
def joy_button_cb(data):
    global inforLabelList2
    data = data.data
    s = ItoS(data[0])+', '+ItoS(data[1])+', '+ItoS(data[2])+', '
    inforLabelList2[1].config(text = s)
    
def joy_right_cb(data):
    global inforLabelList2
    data = data.data
    s = ItoS(data[0])+', '+ItoS(data[1])
    inforLabelList2[2].config(text = s)
    
def joy_left_cb(data):
    global inforLabelList2
    data = data.data
    s = ItoS(data[0])+', '+ItoS(data[1])
    inforLabelList2[3].config(text = s)

def depth_ft_cb(data):
    global inforLabelList3
    data = data.data
    inforLabelList3[0].config(text = FtoS(data))

def balance_ft_cb(data):
    global inforLabelList3
    data = data.data
    s = ItoS(data[0])+', '+ItoS(data[1])+', '+ItoS(data[2])
    inforLabelList3[1].config(text = s)
    
def forward_ft_cb(data):
    global inforLabelList3
    data = data.data
    inforLabelList3[2].config(text = FtoS(data))
    
def turn_ft_cb(data):
    global inforLabelList3
    data = data.data
    inforLabelList3[3].config(text = FtoS(data))

rospy.init_node('dashboard',anonymous=True)

rospy.Subscriber('/depth', Float32, depth_cb)
rospy.Subscriber('/posture', numpy_msg(Floats), posture_cb)
rospy.Subscriber('/voltage', Float32, voltage_cb)
rospy.Subscriber('/compass_yaw', Float32, time_cb)
rospy.Subscriber('/block/yaw/err', Float32, block_cb)
rospy.Subscriber('/state', Int32, state_cb)

rospy.Subscriber('/joy/error_state',Int32, joy_state_cb)
rospy.Subscriber('/joy/button',Int32MultiArray, joy_button_cb)
rospy.Subscriber('/joy/right',Int32MultiArray, joy_right_cb)
rospy.Subscriber('/joy/left',Int32MultiArray, joy_left_cb)

rospy.Subscriber('/ft/depth',Float32, depth_ft_cb)
rospy.Subscriber('/ft/balance',Float32MultiArray, balance_ft_cb)
rospy.Subscriber('/ft/forward',Float32, forward_ft_cb)
rospy.Subscriber('/ft/turn',Float32, turn_ft_cb)

jfPubName = ['/joy/flag/depth', '/joy/flag/balance', '/joy/flag/forward', '/joy/flag/turn']
jfPubClass = [Int32, Int32, Int32, Int32]
jfPubFunc = [jfdepth_cb, jfbalance_cb, jfforward_cb, jfturn_cb]

for i in range(4):
    rospy.Subscriber(jfPubName[i], jfPubClass[i], jfPubFunc[i])

forcePubList = []
forcePubName = ['/force/depth', '/force/balance', '/force/forward', '/force/turn', '/force/sum', '/motor']
forcePubClass = [Float32MultiArray, Float32MultiArray, Float32MultiArray, Float32MultiArray, Float32MultiArray, Int32MultiArray]
forcePubFunc = [fdepth_cb, fbalance_cb, fforward_cb, fturn_cb, fsum_cb, fmotor_cb]

for i in range(6):
    p = rospy.Subscriber(forcePubName[i], forcePubClass[i], forcePubFunc[i])
    forcePubList.append(p)


win = tk.Tk()
win.title('Dashboard')
win.geometry('1000x800')

placeListx = [2, 2, 0, 4, 1, 1, 3, 3]
placeListy = [0, 8, 4, 4, 2, 6, 2, 6]
labelList = []
for i in range(8):
    sublabelList = []
    f = tk.Frame(win)
    f.place(x = placeListx[i]*100, y = placeListy[i]*80, anchor = 'nw')
    l = tk.Label(f, width = 20, text = 'motor'+str(i), font=('Arial', 12), bg = 'black', fg = 'white')
    l.pack(side='top')
    fl = tk.Frame(f)
    fl.pack(side='left')
    fr = tk.Frame(f)
    fr.pack(side='right')
    
    for j in range(4):
        l = tk.Label(fl, width = 10, text = '-', font=('Arial', 12))
        l.pack()
        sublabelList.append(l)
    for j in range(2):
        l = tk.Label(fr, width = 10, height=2, text = '-', font=('Arial', 12))
        l.pack()
        sublabelList.append(l)
    labelList.append(sublabelList)
    
f2 = tk.Frame(win)
f2.place(x = 600, y = 0, anchor = 'n')
f3 = tk.Frame(win)
f3.place(x = 800, y = 0, anchor = 'nw')
f4 = tk.Frame(win)
f4.place(x = 250, y = 270, anchor = 'nw')
f5 = tk.Frame(win)
f5.place(x = 600, y = 500, anchor = 'nw')

inforLabelList = []
topicList = ['Depth', 'Posture', 'voltage', 'compass_yaw', 'block_error', 'state']
heightList = [1, 3, 1, 1, 1, 1]
for i in range(len(topicList)):
    l = tk.Label(f2, text = topicList[i], bg = 'black', fg = 'white', font=('Arial', 12))
    l.pack()
    L = tk.Label(f2, text = '-', height = heightList[i], font=('Arial', 12))
    L.pack()
    inforLabelList.append(L)
    
inforLabelList2 = []
topicList2 = ['joy state', 'joy button', 'joy right', 'joy left']
heightList2 = [1, 1, 1, 1]
for i in range(len(topicList2)):
    l = tk.Label(f3, text = topicList2[i], bg = 'black', fg = 'white', font=('Arial', 12))
    l.pack()
    L = tk.Label(f3, text = '-', height = heightList2[i], font=('Arial', 12))
    L.pack()
    inforLabelList2.append(L)
    
inforLabelList3 = []
topicList3 = ['depth ft', 'balance ft', 'forward ft', 'turn ft']
heightList3 = [1, 1, 1, 1]
for i in range(len(topicList2)):
    l = tk.Label(f4, text = topicList3[i], bg = 'black', fg = 'white', font=('Arial', 12))
    l.pack()
    L = tk.Label(f4, text = '-', height = heightList3[i], font=('Arial', 12))
    L.pack()
    inforLabelList3.append(L)

inforLabelList4 = []
topicList4 = ['depth', 'balance', 'forward', 'turn']
heightList4 = [1, 1, 1, 1]
for i in range(len(topicList2)):
    l = tk.Label(f5, text = topicList4[i], bg = 'black', fg = 'white', font=('Arial', 12))
    l.pack()
    L = tk.Label(f5, text = 'auto', height = heightList4[i], font=('Arial', 12), bg = 'green')
    L.pack()
    inforLabelList4.append(L)

win.mainloop()
