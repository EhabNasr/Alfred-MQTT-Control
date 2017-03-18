import paho.mqtt.client as mqtt, os, urllib.parse as urlparse




# Define event callbacks
def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
    if msg.topic == "alfred/walk":
        if str(msg.payload)[0] == 'u':
            print('*Moving forward*')
            ser.write("u")
        elif str(msg.payload)[0] == 'd':
            print('*Moving backward*')
            ser.write('d')
        elif str(msg.payload)[0] == 'r':
            print('Moving right')
            ser.write('r')
        elif str(msg.payload)[0] == 'l':
            print('Moving left')
            ser.write('l')
        elif str(msg.payload)[0] == 's':
            print('stop')
            ser.write('s')
    else:
        print(msg.payload)





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
url = urlparse.urlparse(url_str)

#print(url_str)
#print(url.username)
#print(url.password)
#print(url.hostname)
#print(url.port)

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