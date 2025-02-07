import RPi.GPIO as GPIO
import time
from fastapi import FastAPI
from include.config import a4_step_motors, long_step_motors
from include.dispenser import PaperDispenser
from include.item_model import Item
from include.coin_dispenser import CoinDispenser

app = FastAPI()

COIN_PIN = 27  # Change to your actual GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(COIN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

coin_count = 0  # Global variable to store the count
pulse_count = 0

dispensers = {
    "A4": PaperDispenser(a4_step_motors['stepper_one'], a4_step_motors['stepper_two']),
    "LONG": PaperDispenser(long_step_motors['stepper_one'], long_step_motors['stepper_two'])
}

# Define coin dispensers for different values
coins = {
    10: CoinDispenser(pin=24, duration=1.0),
    5: CoinDispenser(pin=23, duration=0.7),
    1: CoinDispenser(pin=18, duration=0.5)
}
def dispense_amount(amount):
    """Determines the number of each coin needed to match the given amount."""
    for value in sorted(coins.keys(), reverse=True):
        count = amount // value
        if count > 0:
            coins[value].dispense_coin(count)
            amount -= count * value

def count_pulse(channel):
    """Callback function for each pulse received."""
    global pulse_count
    pulse_count += 1

def check_coin_slot_interrupt():
    global pulse_count
    if pulse_count > 0:
        # Determine coin value based on pulse count
        if pulse_count == 1:
            current_coin_value = 1  # 1 Peso
        elif pulse_count == 5:
            current_coin_value = 5  # 5 Pesos
        elif pulse_count == 10:
            current_coin_value = 10  # 10 Pesos
        else:
            current_coin_value = 0  # Unknown coin
        # Add logic here to handle the coin insertion 
        # (e.g., update a counter, dispense a product, etc.)
        pulse_count = 0  # Reset pulse count for the next coin
        return current_coin_value
    return 0
    
def coin_inserted(channel):
    global coin_count
    coin_count += check_coin_slot_interrupt()
    print(f"Coin detected! Total: {coin_count}")

# Detect falling edge (coin pulse)
GPIO.add_event_detect(COIN_PIN, GPIO.FALLING, callback=coin_inserted, bouncetime=100)






# ROUTES
@app.get("/coins")
def get_coin_count():
    return {"coins": coin_count}

@app.post("/reset-coins")
def reset_coins():
    global coin_count
    coin_count = 0
    return {"message": "Coin count reset"}

@app.get("/buy")
async def get_coin_count(item: Item):
    global coin_count
    change = 0
    try:
        amount = int(change)
        if amount > 0:
            dispensers[item.paper].dispense(item.quantity)
            dispense_amount(amount)
            coin_count = 0
        else:
            print("Please enter a positive amount.")
    except ValueError:
        print("Invalid input. Please enter a valid amount.")


    return {"coins": coin_count, "request": item}