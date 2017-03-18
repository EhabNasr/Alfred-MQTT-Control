import paho.mqtt.client as mqtt, os, urllib.parse as urlparse

# Define event callbacks
def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))
def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)

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
#"mqtt://qldkjxzp:gK5_OW6wcgAd@m12.cloudmqtt.com:17492"
url = urlparse.urlparse(url_str)
print(url_str)

print(url.username)
print(url.password)
print(url.hostname)
print(url.port)

# Connect
mqttc.username_pw_set(url.username, url.password)

mqttc.connect(url.hostname, url.port)

# Start subscribe, with QoS level 0
#mqttc.subscribe("alfred", 0)

# Publish a message
mqttc.publish("alfred/walk", "w")

