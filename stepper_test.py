import time
import RPi.GPIO as gpio
from include.config import a4_step_motors, long_step_motors
import sys

# defines
CW  = 1
CCW = 0

gpio.setmode(gpio.BCM)

class StepperMotor():
    def __init__(self, config = { 'pulse_pin': 0, 'dir_pin': 0 }):
        self.pulse_pin = config['pulse_pin']
        self.dir_pin = config['dir_pin']

        gpio.setmode(gpio.BCM)
        gpio.setup(self.pulse_pin, gpio.OUT)
        gpio.setup(self.dir_pin, gpio.OUT)

    def _stepper_rotate(self, steps, direction, delay=0.001):
        gpio.output(self.dir_pin, gpio.HIGH if direction else gpio.LOW)
        print("Starting")
        for _ in range(steps):
            #print("step")
            gpio.output(self.pulse_pin, gpio.HIGH)
            time.sleep(delay)  # Pulse duration
            gpio.output(self.pulse_pin, gpio.LOW)
            time.sleep(delay)  # Pulse interval


class PaperDispenser():

    # Default steps values
    stepper_one_steps = 1000

    # Stepper motor config objects = {pulse_pin, dir_pin, steps}
    def __init__(self, stepper_one = {}, stepper_two = {}):
        self.stepper_one = StepperMotor(stepper_one)
        self.stepper_one_steps = stepper_one['steps']

        self.stepper_two = StepperMotor(stepper_two)
        self.stepper_two_steps = stepper_two['steps']
        #self.dc_motor = DCMotor(stepper_two)
        self.IN1 = stepper_two['pulse_pin']
        self.IN2 = stepper_two['dir_pin']
        self.ENA = 13

        gpio.setup(self.IN1, gpio.OUT)
        gpio.setup(self.IN2, gpio.OUT)
        gpio.setup(self.ENA, gpio.OUT)

        self.pwm = gpio.PWM(self.ENA, 1000)
        self.pwm.start(100)

        gpio.output(self.IN1, gpio.LOW)
        gpio.output(self.IN2, gpio.LOW)

    def dispense(self, num_of_papers):
        for _ in range(num_of_papers):
            gpio.output(self.IN1, gpio.HIGH)
            gpio.output(self.IN2, gpio.LOW)
            time.sleep(2)
            self.stepper_one._stepper_rotate(self.stepper_one_steps, CCW)
            gpio.output(self.IN1, gpio.LOW)
            gpio.output(self.IN2, gpio.LOW)
            time.sleep(2)
            gpio.output(self.IN1, gpio.LOW)
            gpio.output(self.IN2, gpio.HIGH)
            time.sleep(12)
            gpio.output(self.IN1, gpio.LOW)
            gpio.output(self.IN2, gpio.LOW)


n = len(sys.argv)
if n < 4:
    print("Usage: python3 stepper_test <stepper_one_steps> <stepper_two_steps> <number_of_papers>")
    sys.exit()

a4_step_motors['stepper_one']['steps'] = int(sys.argv[1])
a4_step_motors['stepper_two']['steps'] = int(sys.argv[2])


dispensers = {
    "A4": PaperDispenser(a4_step_motors['stepper_one'], a4_step_motors['stepper_two']),
    # "LONG": PaperDispenser(long_step_motors['stepper_one'], long_step_motors['stepper_two'])
}

print("Dispensing", int(sys.argv[3]))
dispensers['A4'].dispense(int(sys.argv[3]))

