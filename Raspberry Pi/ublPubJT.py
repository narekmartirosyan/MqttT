import paho.mqtt.client as mqtt
import sys
import seeed_dht
import json
import time
from grove.gpio import GPIO

__all__ = ['GroveLed', 'GPIO']

usleep = lambda x: time.sleep(x / 1000000.0)

_TIMEOUT1 = 1000
_TIMEOUT2 = 10000
counter = 0

class GroveUltrasonicRanger(object):
    def __init__(self, pin):
        self.dio = GPIO(pin)

    def _get_distance(self):
        self.dio.dir(GPIO.OUT)
        self.dio.write(0)
        usleep(2)
        self.dio.write(1)
        usleep(10)
        self.dio.write(0)

        self.dio.dir(GPIO.IN)

        t0 = time.time()
        count = 0
        while count < _TIMEOUT1:
            if self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT1:
            return None

        t1 = time.time()
        count = 0
        while count < _TIMEOUT2:
            if not self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT2:
            return None

        t2 = time.time()

        dt = int((t1 - t0) * 1000000)
        if dt > 530:
            return None

        distance = ((t2 - t1) * 1000000 / 29 / 2)    # cm

        return distance

    def get_distance(self):
        while True:
            dist = self._get_distance()
            if dist:
                return dist
            
class GroveLed(GPIO):
    '''
    Class for Grove - XXXX Led

    Args:
        pin(int): number of digital pin the led connected.
    '''
    def __init__(self, pin):
        super(GroveLed, self).__init__(pin, GPIO.OUT)

    def on(self):
        '''
        light on the led
        '''
        self.write(1)

    def off(self):
        '''
        light off the led
        '''
        self.write(0)

Grove = GroveUltrasonicRanger


def main():
    from grove.helper import SlotHelper
    sh = SlotHelper(SlotHelper.GPIO)
    pin = sh.argv2pin()

    pinBlue = 22
    pinRed = 24
    pinGreen = 16
    
    ledBlue = GroveLed(pinBlue)
    ledGreen = GroveLed(pinGreen)
    ledRed = GroveLed(pinRed)
    
    sonar = GroveUltrasonicRanger(pin)
    
    Werte = [0,100,10,25]

    def on_connect(client, userdata, flags, rc):
        client.subscribe("json")
    
    def on_message(client, userdata, msg):
        body = json.loads(msg.payload)
        Werte[0] = body["Messbereich"][0]
        Werte[1] = body["Messbereich"][1]
        Werte[2] = body["ok"][0]
        Werte[3] = body["ok"][1]       
 
    def temperatur():
        sensor = seeed_dht.DHT("11", 12)
        humi, temp = sensor.read()
        client.publish("pi4/temp",'{1:.1f}'.format(sensor.dht_type, temp))  
                
    def abstand():  
        global counter      
        if((sonar.get_distance()>Werte[0] and sonar.get_distance()<Werte[2]) or (sonar.get_distance()>Werte[3] and sonar.get_distance()<Werte[1])):
            print("out")
            ledGreen.off()
            ledRed.on()
            ledBlue.on()
            client.publish("pi4/D" + str(pin) + "/distance", sonar.get_distance())
            time.sleep(0.25)
            ledBlue.off()
            time.sleep(0.15)
            counter += 4
        elif(sonar.get_distance()>=Werte[2] and sonar.get_distance()<=Werte[3]):
            print("in")
            ledRed.off()
            ledGreen.on()
            ledBlue.on()
            client.publish("pi4/D" + str(pin) + "/distance", sonar.get_distance())
            time.sleep(0.5)
            ledBlue.off()
            time.sleep(2.4)
            counter += 29
            
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("testuser","1234")
    client.connect("192.168.3.131", 1883, 60)
    #client.reconnect()
    client.loop_start()
    
    global counter
    try:
        while True:
            counter += 1
            if(counter >= 100):
                temperatur()
            if(counter >= 100):
                counter = 0
            abstand()
            time.sleep(0.1)
    except KeyboardInterrupt:                
        client.disconnect()
        ledBlue.off()
        ledGreen.off()
        ledRed.off()
        client.loop_stop()

if __name__ == '__main__':
    main()
