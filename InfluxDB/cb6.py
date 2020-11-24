import paho.mqtt.client as mqtt

from influxdb import InfluxDBClient
client1 = InfluxDBClient(host='localhost', port=8086)  
client1.get_list_database()
client1.switch_database('mqtt')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("cb6/#")

    
def on_message(client, userdata, msg):   
         
        topic = str(msg.topic).split("/")

        if ("temperature_C" in topic):
            json_body = [
                {
                    "measurement": "temperature",
                    "tags": {
                        "Wertegeber": "/".join(topic[2:-1])
                    },
                    "fields": {
                    "Ort": "/".join(topic[0:1]),
                    "Kanal": "/".join(topic[1:2]), 
                    "Wert": msg.payload
                    }
                },
            ]    
            client1.write_points(json_body)

        elif (topic[-1]=="0" or topic[-1]=="1"):
            if("input" in topic or "light" in topic or "relay" in topic or "roller" in topic):
                json_body = [
                    {
                        "measurement": "/".join(topic[-2:-1]),
                        "tags": {
                            "Wertegeber": "/".join(topic[2:3]) + "/" + "/".join(topic[-1:])
                        },
                        "fields": {
                        "Ort": "/".join(topic[0:1]),
                        "Kanal": "/".join(topic[1:2]), 
                        "Wert": msg.payload
                        }
                    },
                ]    
                client1.write_points(json_body)
            
        elif (topic[-2]=="0" or topic[-2]=="1"):
            if("energy" in topic or "status" in topic):
                json_body = [
                    {
                        "measurement": "/".join(topic[-3:-2]) + "/".join(topic[-1:]),
                        "tags": {
                            "Wertegeber": "/".join(topic[2:3]) + "/" + "/".join(topic[-2:-1])
                        },
                        "fields": {
                        "Ort": "/".join(topic[0:1]),
                        "Kanal": "/".join(topic[1:2]), 
                        "Wert": msg.payload
                        }
                    },
                ]
                client1.write_points(json_body)
            
        elif ("energy" in topic or "temperature" in topic):
            json_body = [
                {
                    "measurement": "/".join(topic[-1:]),
                    "tags": {
                        "Wertegeber": "/".join(topic[2:3])
                    },
                    "fields": {
                    "Ort": "/".join(topic[0:1]),
                    "Kanal": "/".join(topic[1:2]), 
                    "Wert": msg.payload
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
