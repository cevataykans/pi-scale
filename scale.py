from hx711 import HX711

class Scale:

    def __init__(self, data_pin=5, clock_pin=6):
        self.hx = HX711(data_pin, clock_pin)
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(435.224)

    def tare(self):
        self.hx.reset()
        self.hx.tare()
    
    def weight(self):
        self.hx.reset()
        val = self.hx.get_weight(10)
        print("Def: ", val, " Rounded: ", round(val))
        return val

    def clean(self):
        import RPi.GPIO as GPIO
        GPIO.cleanup()