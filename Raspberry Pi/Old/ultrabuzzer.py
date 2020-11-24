from __future__ import print_function
import paho.mqtt.client as mqtt
import sys
import time
from grove.gpio import GPIO
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

    pin1 = 12

    mraa_pin1 = getGpioLookup("GPIO%02d" % pin1)
    buzzer = upmBuzzer.Buzzer(mraa_pin1)

    sonar = GroveUltrasonicRanger(pin)

    client = mqtt.Client()
    client.connect("192.168.3.93", 1883, 60)

    while True:
        ##client.publish("distance", '{} cm'.format(sonar.get_distance()))
        if(pin==5):
            while(sonar.get_distance()<5 or (sonar.get_distance()>10 and sonar.get_distance()<25)):
                    print("out")
                    print(buzzer.playSound(upmBuzzer.BUZZER_DO, 100000))
                    client.publish("distance/5", sonar.get_distance())
                    time.sleep(0.25)
            while((sonar.get_distance()>=5 and sonar.get_distance()<=10) or sonar.get_distance()>=25):
                    print("in")
                    print(buzzer.playSound(upmBuzzer.BUZZER_DO, 100000))
                    client.publish("distance/5", sonar.get_distance())
                    time.sleep(5)
        if(pin==16):
            while(sonar.get_distance()<5 or (sonar.get_distance()>10 and sonar.get_distance()<25)):
                    print("out")
                    print(buzzer.playSound(upmBuzzer.BUZZER_DO, 100000))
                    client.publish("distance/16", sonar.get_distance())
                    time.sleep(0.25)
            while((sonar.get_distance()>=5 and sonar.get_distance()<=10) or sonar.get_distance()>=25):
                    print("in")
                    print(buzzer.playSound(upmBuzzer.BUZZER_DO, 100000))
                    client.publish("distance/16", sonar.get_distance())
                    time.sleep(5)

    client.disconnect()

if __name__ == '__main__':
    main()
