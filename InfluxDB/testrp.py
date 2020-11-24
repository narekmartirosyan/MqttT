import paho.mqtt.client as mqtt

from influxdb import InfluxDBClient
from google.protobuf.text_format import ParseFloat
client1 = InfluxDBClient(host='localhost', port=8086)  
client1.get_list_database()
client1.switch_database('testrp')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("cb6/shellies/#")

    
def on_message(client, userdata, msg):   
         
        topic = str(msg.topic).split("/")
            
        if ("energy" in topic or "temperature" in topic):
            if (topic[2]=="shellyswitch25-76D3E5"):
                tpc = "ZN1"
            elif (topic[2]=="shellydimmer-D47455"):
                tpc = "ZN2"
            elif (topic[2]=="shellydimmer-D47CD0"):
                tpc = "RA1"
            elif (topic[2]=="shellyswitch25-76C618"):
                tpc = "RA2"
            
            if (topic[2]=="shellyswitch25-76D3E5" or topic[2]=="shellydimmer-D47455" 
            or topic[2]=="shellydimmer-D47CD0" or topic[2]=="shellyswitch25-76C618"):
                
                json_body = [
                    {
                        "measurement": "/".join(topic[-1:]),
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
client.tls_set()


client.username_pw_set("icz", "u7V38ayL")

client.connect("vmd53640.contaboserver.net", 8883, 60)


client.loop_forever()
