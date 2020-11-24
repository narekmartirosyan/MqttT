import paho.mqtt.client as mqtt
from google.protobuf.text_format import ParseFloat

var1 = 5
print(var1)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
    client.subscribe("var/#")
    
def on_message(client, userdata, msg):   
    topic = str(msg.topic).split("/")
    if("1" in topic):
        var1=ParseFloat(msg.payload)
        print(var1)
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("testuser", "1234")

client.connect("192.168.3.131", 1883, 60)

