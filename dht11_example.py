import RPi.GPIO as GPIO
import datetime,time,RPi,dht11
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance =dht11. DHT11(pin=14)

while True:
    result = instance.read()
    if result.is_valid():
        print("時刻: " + str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')),end="")
        print(" 温度: %d C " % result.temperature,end="")
        print("湿度: %d %%" % result.humidity)
    time.sleep(2)

