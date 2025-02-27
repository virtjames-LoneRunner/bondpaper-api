import RPi.GPIO as GPIO
#import lgpio as GPIO
import time

class CoinDispenser:
    def __init__(self, pin, duration=0.5):
        self.pin = pin
        self.duration = duration
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def dispense_coin(self):
        """Activates the coin dispenser for a specified duration."""
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(self.duration)
        GPIO.output(self.pin, GPIO.LOW)
        print(f"Coin dispensed from pin {self.pin}!")

    def cleanup(self):
        GPIO.cleanup(self.pin)
