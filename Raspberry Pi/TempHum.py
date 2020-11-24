import time
import seeed_dht
def main():

    # for DHT11/DHT22
    sensor = seeed_dht.DHT("11", 12)
    # for DHT10
    # sensor = seeed_dht.DHT("10")
    
    while True:
        humi, temp = sensor.read()
        print('temperature {1:.1f}*'.format(sensor.dht_type, temp))
        time.sleep(1)

if __name__ == '__main__':
    main()



