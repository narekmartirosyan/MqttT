import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("shellies/#")
    
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    
from influxdb import InfluxDBClient
client1 = InfluxDBClient(host='localhost', port=8086)
client1.get_list_database()
client1.switch_database('pyexample')
json_body = [
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carrrol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2018-03-28T8:01:00Z",
        "fields": {
            "duration": 1233
        }
    },
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2018-03-29T8:04:00Z",
        "fields": {
            "duration": 1122
        }
    },
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2018-03-30T8:02:00Z",
        "fields": {
            "duration": 124
        }
    }
]

client1.write_points(json_body)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("testuser", "1234")

client.connect("192.168.3.93", 1883, 60)


client.loop_forever()

