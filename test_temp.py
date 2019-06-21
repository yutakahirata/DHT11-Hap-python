import logging,serial,requests,signal,time,datetime
import RPi.GPIO as GPIO
import dht11
from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import (CATEGORY_SENSOR)
logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin=14)
global hum
class TemperatureSensor(Accessory):
    category = CATEGORY_SENSOR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('TemperatureSensor')
        self.char_temp = serv_temp.configure_char('CurrentTemperature')

    @Accessory.run_at_interval(3)
    async def run(self):
        global hum
        result = instance.read()
        if result.is_valid():
            self.char_temp.set_value(result.temperature)
            hum=result.humidity

class HumiditySensor(Accessory):
    category = CATEGORY_SENSOR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('HumiditySensor')
        self.char_temp = serv_temp.configure_char('CurrentRelativeHumidity')

    @Accessory.run_at_interval(3)
    async def run(self):
        global hum
        self.char_temp.set_value(hum)


def get_bridge(driver):
    bridge = Bridge(driver, 'Bridge')
    bridge.add_accessory(TemperatureSensor(driver, '温度'))
    bridge.add_accessory(HumiditySensor(driver, '湿度'))
    return bridge
driver = AccessoryDriver(port=51826, persist_file='test.state')
driver.add_accessory(accessory=get_bridge(driver))
signal.signal(signal.SIGTERM, driver.signal_handler)
driver.start()
