import RPi.GPIO as GPIO
#import lgpio as GPIO
import time

class CoinDispenser:
    coin_dispensed = False
    def __init__(self, pin, sensor_pin, duration=0.5):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.sensor_pin = sensor_pin
        GPIO.setup(self.sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.sensor_pin, GPIO.FALLING, callback=self.check_coin_dispensed, bouncetime=100)        

    def check_coin_dispensed(self):
        coin_dispensed = True

    def dispense_coin(self):
        """Activates the coin dispenser for a specified duration."""
        GPIO.output(self.pin, GPIO.HIGH)
        while not coin_dispensed:
            pass
        GPIO.output(self.pin, GPIO.LOW)
        coin_dispensed = False
        print(f"Coin dispensed from pin {self.pin}!")

    def cleanup(self):
        GPIO.cleanup(self.pin)
