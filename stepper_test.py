import time
import RPi.GPIO as gpio
from include.config import a4_step_motors, long_step_motors
import sys

# defines
CW  = 1
CCW = 0

class StepperMotor():
    def __init__(self, config = { 'pulse_pin': 0, 'dir_pin': 0 }):
        self.pulse_pin = config['pulse_pin']
        self.dir_pin = config['dir_pin']

        gpio.setmode(gpio.BCM)
        gpio.setup(self.pulse_pin, gpio.OUT)
        gpio.setup(self.dir_pin, gpio.OUT)

    def _stepper_rotate(self, steps, direction, delay=0.001):
        gpio.output(self.dir_pin, gpio.HIGH if direction else gpio.LOW)
        for _ in range(steps):
            gpio.output(self.pulse_pin, gpio.HIGH)
            time.sleep(delay)  # Pulse duration
            gpio.output(self.pulse_pin, gpio.LOW)
            time.sleep(delay)  # Pulse interval


class DCMotor():

    def __init__(self, config = { 'pulse_pin': 0, 'dir_pin': 0 }):
        self.IN1 = config['pulse_pin']
        self.IN2 = config['dir_pin']

        gpio.setup(self.IN1, gpio.OUT)
        gpio.setup(self.IN2, gpio.OUT)

        # Set up PWM on both self.IN1 and IN2 (1 kHz frequency)
        pwm_in1 = gpio.PWM(self.IN1, 1000)
        pwm_in2 = gpio.PWM(self.IN2, 1000)

        gpio.setmode(gpio.BCM)
        gpio.setup(self.IN1, gpio.OUT)
        gpio.setup(self.IN2, gpio.OUT)

        pwm_in1.start(0)  # Start with 0% duty cycle (motor off)
        pwm_in2.start(0)

    def rotate(self, speed, direction):
        if direction.lower() == "forward":
            self.pwm_in1.ChangeDutyCycle(speed)  # Apply PWM to IN1
            self.pwm_in2.ChangeDutyCycle(0)      # Keep IN2 LOW
        elif direction.lower() == "backward":
            self.pwm_in1.ChangeDutyCycle(0)      # Keep IN1 LOW
            self.pwm_in2.ChangeDutyCycle(speed)  # Apply PWM to IN2
        else:
            self.pwm_in1.ChangeDutyCycle(0)
            self.pwm_in2.ChangeDutyCycle(0)



class PaperDispenser():

    # Default steps values
    stepper_one_steps = 1000
    # stepper_two_steps = 1000

    # Stepper motor config objects = {pulse_pin, dir_pin, steps}
    def __init__(self, stepper_one = {}, stepper_two = {}):
        self.stepper_one = StepperMotor(stepper_one)
        self.stepper_one_steps = stepper_one['steps']

        # self.stepper_two = StepperMotor(stepper_two)
        # self.stepper_two_steps = stepper_two['steps']
        self.dc_motor = DCMotor(stepper_two)

    def dispense(self, num_of_papers):
        for _ in range(num_of_papers):
            self.stepper_one._stepper_rotate(self.stepper_one_steps, CW)
            # self.stepper_two._stepper_rotate(self.stepper_two_steps, CW)
            self.dc_motor.rotate(50, 1)


n = len(sys.argv)
if n < 4:
    print("Usage: python3 stepper_test <stepper_one_steps> <stepper_two_steps> <number_of_papers>")
    sys.exit()

a4_step_motors['stepper_one']['steps'] = sys.argv[1]
a4_step_motors['stepper_two']['steps'] = sys.argv[2]


dispensers = {
    "A4": PaperDispenser(a4_step_motors['stepper_one'], a4_step_motors['stepper_two']),
    # "LONG": PaperDispenser(long_step_motors['stepper_one'], long_step_motors['stepper_two'])
}

dispensers['A4'].dispense(sys.argv[3])

