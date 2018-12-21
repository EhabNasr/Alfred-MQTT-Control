import paho.mqtt.client as mqtt, os
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse

import RPi.GPIO as GPIO
from time import sleep

#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.output(7,False)
GPIO.output(11,False)
GPIO.output(13,False)
GPIO.output(15,False)

#set GPIO for line follower
GPIO.setup(19,GPIO.IN)
GPIO.setup(21,GPIO.IN)
GPIO.setup(23,GPIO.IN)

#set GPIO for decision making
GPIO.setup(22,GPIO.IN)
GPIO.setup(24,GPIO.IN)
robo_orientation = 0
command_orientation = 0
decision = 0


# Define event callbacks
def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))


def navigate_forward():
    print('I am here')
    while (GPIO.input(22)==False and GPIO.input(24)==False):
        if(GPIO.input(19)==True): #both white move forward
            GPIO.output(7,False)
            GPIO.output(11,True)
        else:
            GPIO.output(7,True)
            GPIO.output(11,True)
        if(GPIO.input(23)==True): #turn right
            GPIO.output(13,False)
            GPIO.output(15,True)
        else:
            GPIO.output(13,True)
            GPIO.output(15,True)
        if(GPIO.input(19)==False and GPIO.input(23)==False):
            break
    print('Reached Destination')
    while(GPIO.input(22)==False or GPIO.input(24)==False):
        if(GPIO.input(22)==False):
            GPIO.output(7,False)
            GPIO.output(11,True)
        else:
            GPIO.output(7,True)
            GPIO.output(11,True)
        if(GPIO.input(24)==False):
            GPIO.output(13,False)
            GPIO.output(15,True)
        else:
            GPIO.output(13,True)
            GPIO.output(15,True)

def step_forward():
    while(GPIO.input(22)==True or GPIO.input(24)==True): #Move forward till you pass the first black line
        if(GPIO.input(22)==True):
            GPIO.output(7,False)
            GPIO.output(11,True)
        else:
            GPIO.output(7,True)
            GPIO.output(11,True)
        if(GPIO.input(24)==True):
            GPIO.output(13,False)
            GPIO.output(15,True)
        else:
            GPIO.output(13,True)
            GPIO.output(15,True)
    print("step out done")
    navigate_forward()


def step_right():
    print("I'm here in the right")
    while (GPIO.input(24)==True): #
        GPIO.output(7,True)
        GPIO.output(11,True)
        GPIO.output(13,False)
        GPIO.output(15,True)
    print("Step 1 finished")
    while (GPIO.input(24)==False):
        GPIO.output(7,True)
        GPIO.output(11,True)
        GPIO.output(13,False)
        GPIO.output(15,True)
    print("Step 2 finished")
    while (GPIO.input(24)==True):
        GPIO.output(7,True)
        GPIO.output(11,True)
        GPIO.output(13,False)
        GPIO.output(15,True)
    while (GPIO.input(22)==True):
        GPIO.output(7,True)
        GPIO.output(11,True)
        GPIO.output(13,False)
        GPIO.output(15,True)
    GPIO.output(7,False)
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(15,False)
    navigate_forward()


def step_left():
    while (GPIO.input(22)==True):
        GPIO.output(7,False)
        GPIO.output(11,True)
        GPIO.output(13,True)
        GPIO.output(15,True)
    while (GPIO.input(22)==False):
        GPIO.output(7,False)
        GPIO.output(11,True)
        GPIO.output(13,True)
        GPIO.output(15,True)
    while (GPIO.input(22)==True):
        GPIO.output(7,False)
        GPIO.output(11,True)
        GPIO.output(13,True)
        GPIO.output(15,True)
    while (GPIO.input(24)==True):
        GPIO.output(7,False)
        GPIO.output(11,True)
        GPIO.output(13,True)
        GPIO.output(15,True)
    GPIO.output(7,False)
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(15,False)
    navigate_forward()


def step_back():
    while (GPIO.input(24)==True):
        GPIO.output(7,False)
        GPIO.output(11,True)
        GPIO.output(13,True)
        GPIO.output(15,False)
    while (GPIO.input(24)==False):
        GPIO.output(7,False)
        GPIO.output(11,True)
        GPIO.output(13,True)
        GPIO.output(15,False)
    while (GPIO.input(24)==True):
        GPIO.output(7,False)
        GPIO.output(11,True)
        GPIO.output(13,True)
        GPIO.output(15,False)
    GPIO.output(7,False)
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(15,False)
    navigate_forward()


def decide_and_move(decision):
    print('decision is: ')
    print(decision)
    print('received command_orientation is: ')
    print(command_orientation)
    print('original robo_orientation is: ')
    print(robo_orientation)
    if decision == 0:
        step_forward()
    elif decision == 90 or decision == -270:
        step_left()
    elif decision == 270 or decision == -90:
        step_right()
    elif decision == -180:
        step_back()
    elif decision == 180:
        step_back()


def on_message(mosq, obj, msg):
    global robo_orientation
    global command_orientation
    global decision
    print("message Received")
    print(msg.payload)
    if msg.topic == "alfred/walk/1":
        if str(msg.payload)[0] == 'u':
            command_orientation = 90
            # print('*Moving forward*')
        elif str(msg.payload)[0] == 'r':
            command_orientation = 0
            # print('*Rotating right*')
        elif str(msg.payload)[0] == 'l':
            command_orientation = 180
            # print('*Rotating left*')
        elif str(msg.payload)[0] == 'd':
            command_orientation = 270
            # print('*Rotating downward*')
        elif str(msg.payload)[0] == 'a': #testing
            step_left()
            return
            # print('*Rotating downward*')
        elif str(msg.payload)[0] == 's': #testing
            step_right()
            return
            # print('*Rotating downward*')
    else:
        print(msg.payload)
    decision = command_orientation - robo_orientation
    decide_and_move(decision)
    robo_orientation = robo_orientation + decision
    print('new robo_orientation is: ')
    print(robo_orientation)

    # sleep(0.5)
    GPIO.output(7,False)
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(15,False)
    global mqttc
    mqttc.publish("ack/here/1","1")
    mqttc.subscribe("alfred/#", 0)




def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)

def apply_func(rc):
    print(rc)
    if rc == 'w':
        print('moving forward')

mqttc = mqtt.Client()
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Uncomment to enable debug messages
#mqttc.on_log = on_log

# Parse CLOUDMQTT_URL (or fallback to localhost)
url_str = 'mqtt://qldkjxzp:gK5_OW6wcgAd@m12.cloudmqtt.com:17492'
url = urlparse(url_str)

print(url_str)
print(url.username)
print(url.password)
print(url.hostname)
print(url.port)

# Connect
mqttc.username_pw_set(url.username, url.password)

mqttc.connect(url.hostname, url.port)

# Start subscribe, with QoS level 0
mqttc.subscribe("alfred/#", 0)

# Continue the network loop, exit when an error occurs
rc = 0
while rc == 0:
    rc = mqttc.loop()
print("rc: " + str(rc))
