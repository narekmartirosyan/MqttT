import paho.mqtt.client as mqtt

client = mqtt.Client()
##client.tls_set()
##client.username_pw_set("icz", "u7V38ayL")
##client.connect("vmd53640.contaboserver.net", 8883, 60)
client.username_pw_set("testuser", "1234")
client.connect("192.168.3.131", 1883, 60)
client.publish("var/1", '10')
client.publish("var/2", '25')
client.publish("var/3", '35')
client.disconnect()
