from hx711 import HX711

import time

class Scale:

    def __init__(self, data_pin=5, clock_pin=6):
        self.hx = HX711(data_pin, clock_pin)
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(435.224)
        self.hx.reset()
        self.hx.tare()

        self.ref = False
        self.ref_weight = 0.0
        self.frequency = 15
        self.weight_threshold = 1

    def tare(self):
        time.sleep(1)
        self.ref_weight = self.weight()
        self.hx.set_reference_unit(435.224)
        self.hx.reset()
        self.hx.tare(self.frequency)

    def weight(self):
        return self.hx.get_weight(self.frequency)
    
    def measure(self):
        self.hx.reset()
        val = self.weight()
        if val < -self.weight_threshold and self.ref:
            self.tare()
            self.ref = False
            val = self.weight()
        elif val > self.weight_threshold and not self.ref:
            self.tare()
            self.ref = True
        return (val, self.ref_weight)

    def clean(self):
        import RPi.GPIO as GPIO
        GPIO.cleanup()