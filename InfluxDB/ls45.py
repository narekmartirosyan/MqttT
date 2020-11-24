import paho.mqtt.client as mqtt

from influxdb import InfluxDBClient
client1 = InfluxDBClient(host='localhost', port=8086)  
client1.get_list_database()
client1.switch_database('mqtt')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("shellies/#")

    
def on_message(client, userdata, msg):   
       
        topic = str(msg.topic).split("/")
         
        json_body = [
            {
                "measurement": "/".join(topic[2:]),
                "tags": {
                    "Wertegeber": msg.topic
                },
                "fields": {
                "Value": msg.payload
                }
            },
        ]
        ##print(json_body)    
        client1.write_points(json_body)
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("testuser", "1234")

client.connect("192.168.3.93", 1883, 60)


client.loop_forever()
