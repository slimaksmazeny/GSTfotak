from gpiozero import PWMLED

LED_PIN = 13   # BCM 13 = fyzický pin 33. NE BCM 17 (pin 11) – to je RST displeje!

class StatusLed:
    def __init__(self, pin=LED_PIN):
        self.led = PWMLED(pin)
    def ready(self):   self.led.on()                                          # svítí = připraveno
    def busy(self):    self.led.blink(on_time=0.1, off_time=0.1)              # ostření/focení
    def writing(self): self.led.pulse(fade_in_time=0.8, fade_out_time=0.8)    # zápis na e-ink
    def error(self):   self.led.blink(on_time=0.15, off_time=0.15, n=2)
    def off(self):     self.led.off()
