import paho.mqtt.client as mqtt

from influxdb import InfluxDBClient
from google.protobuf.text_format import ParseFloat
client1 = InfluxDBClient(host='localhost', port=8086)  
client1.get_list_database()
client1.switch_database('hqm')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("pi4/#")

#Git TEST
    
def on_message(client, userdata, msg):   
            
        topic = str(msg.topic).split("/")
        
        if (topic[1] == "temp"):
            json_body = [
                {
                    "measurement": "temp",
                    "tags": {
                        "Wertegeber": "pi4"
                    },
                    "fields": {
                    "Ort": "W0002",
                    "Kategorie": "Anlagen", 
                    "Wert": msg.payload
                    }
                },
            ]
            client1.write_points(json_body)
        else:            
            if (topic[1] == "D5"):
                tpc="ZN2"
            
            if (topic[1] == "D26"):
                tpc="ZN1"
            
            json_body = [
                {
                    "measurement": "distance",
                    "tags": {
                        "Wertegeber": tpc
                    },
                    "fields": {
                    "Ort": "W0002",
                    "Kategorie": "Anlagen", 
                    "Wert": ParseFloat(msg.payload)
                    }
                },
            ]
            client1.write_points(json_body)
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("testuser","1234")
client.connect("192.168.3.131", 1883, 60)


client.loop_forever()