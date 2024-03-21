from hx711 import HX711

import time

class Scale:

    def __init__(self, data_pin=5, clock_pin=6):
        
        self.weight_frequency = 10
        self.weight_threshold = 1
        self.ref_weight = 0
        
        self.hx = HX711(data_pin, clock_pin)
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(435.224)
        self.hx.reset()
        self.hx.tare()

    def tare(self):
        time.sleep(1)
        self.ref_weight = self.weight()
        self.hx.set_reference_unit(435.224)
        self.hx.reset()
        self.hx.tare()

    def weight(self, times = 15):
        return self.hx.get_weight(times)
    
    def measure(self):
        self.hx.reset()
        val = self.weight(self.weight_frequency)
        if val < -self.weight_threshold and self.ref:
            self.tare()
            self.ref = False
            val = self.weight(self.weight_frequency)
            self.ref_weight = 0
        elif val > self.weight_threshold and not self.ref:
            self.tare()
            self.ref = True
        return (val, self.ref_weight)

    def clean(self):
        import RPi.GPIO as GPIO
        GPIO.cleanup()