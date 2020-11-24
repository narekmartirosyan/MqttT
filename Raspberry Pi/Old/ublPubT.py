from __future__ import print_function
import paho.mqtt.client as mqtt
import sys
import time
from grove.gpio import GPIO
from grove.grove_led import GroveLed
from mraa import getGpioLookup
from upm import pyupm_buzzer as upmBuzzer

usleep = lambda x: time.sleep(x / 1000000.0)

_TIMEOUT1 = 1000
_TIMEOUT2 = 10000

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
            
Grove = GroveUltrasonicRanger


def main():
    from grove.helper import SlotHelper
    from grove import helper
    from grove.helper import helper
    helper.root_check()
    sh = SlotHelper(SlotHelper.GPIO)
    pin = sh.argv2pin()

    pinB = 12
    pinOrange = 22
    pinGreen = 24
    pinRed = 26
    
    ledOrange = GroveLed(pinOrange)
    ledGreen = GroveLed(pinGreen)
    ledRed = GroveLed(pinRed)


    mraa_pinB= getGpioLookup("GPIO%02d" % pinB)
    buzzer = upmBuzzer.Buzzer(mraa_pinB)

    sonar = GroveUltrasonicRanger(pin)
    
    global start1
    start1 = 0
    global start2
    start2 = 0
    global start3
    start3 = 0
    global var1
    var1 = 0
    global var2
    var2 = 0
    global var3
    var3 = 0

    def on_connect(client, userdata, flags, rc):
        client.subscribe("var/#")
    
    def on_message(client, userdata, msg):
        topic = str(msg.topic).split("/")
        if("1" in topic):
            global var1
            var1 = int(msg.payload)
            global start1
            start1 = 1
        if("2" in topic):
            global var2
            var2 = int(msg.payload)
            global start2
            start2 = 1
        if("3" in topic):
            global var3
            var3 = int(msg.payload)
            global start3
            start3 = 1
            
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("testuser","1234")
    client.connect("192.168.3.131", 1883, 60)
    client.loop_start()
    
    try:
        while True:        
            if (start1 == 1 and start2 == 1 and start3 == 1):
            ##client.publish("distance", '{} cm'.format(sonar.get_distance()))
                if(pin==5):
                    while(sonar.get_distance()<var1 or (sonar.get_distance()>var2 and sonar.get_distance()<var3)):
                        print("out")
                        ledGreen.off()
                        ledRed.on()
                        ledOrange.on()
                        print(buzzer.playSound(upmBuzzer.BUZZER_DO, 100000))
                        client.publish("distance/5", sonar.get_distance())
                        ledOrange.off()
                        time.sleep(0.25)
                    while((sonar.get_distance()>=var1 and sonar.get_distance()<=var2) or sonar.get_distance()>=var3):
                        print("in")
                        ledRed.off()
                        ledGreen.on()
                        ledOrange.on()
                        print(buzzer.playSound(upmBuzzer.BUZZER_DO, 100000))
                        client.publish("distance/5", sonar.get_distance())
                        ledOrange.off()
                        time.sleep(5)
                if(pin==16):
                    while(sonar.get_distance()<var1 or (sonar.get_distance()>var2 and sonar.get_distance()<var3)):
                        print("out")
                        ledGreen.off()
                        ledRed.on()
                        ledOrange.on()
                        print(buzzer.playSound(upmBuzzer.BUZZER_DO, 100000))
                        client.publish("distance/16", sonar.get_distance())
                        ledOrange.off()
                        time.sleep(0.25)
                    while((sonar.get_distance()>=var1 and sonar.get_distance()<=var2) or sonar.get_distance()>=var3):
                        print("in")
                        ledRed.off()
                        ledGreen.on()
                        ledOrange.on()
                        print(buzzer.playSound(upmBuzzer.BUZZER_DO, 100000))
                        client.publish("distance/16", sonar.get_distance())
                        ledOrange.off()
                        time.sleep(5)
    except KeyboardInterrupt:                
        client.disconnect()
        ledOrange.off()
        ledGreen.off()
        ledRed.off()
        client.loop_stop()

if __name__ == '__main__':
    main()
