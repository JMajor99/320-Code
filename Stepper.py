import RPi.GPIO as GPIO
import time

# Pin setup
DIR = 20      # Direction pin
STEP = 16     # Step pin
SPR = 200     # Steps per revolution (adjust if microstepping)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
delay = 0.001 

step_count = 0 # This needs to be within the range of 0 -30 as this is the limits of the lift

def Lift(direction, revs):
    if direction == 0:
        step_count -= revs
    elif direction == 1:
        step_count += revs

    GPIO.output(DIR, GPIO.HIGH if direction == 0 else GPIO.LOW)
    steps = int(SPR * revs)
    for _ in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(delay)

while(1):
    # Input: "0 5" for 5 rev CW, "1 2.5" for 2.5 rev CCW
    direction, revs = input("Enter direction (0=CW, 1=CCW) and revolutions: ").split()
    direction = int(direction)
    revs = float(revs)

    GPIO.output(DIR, GPIO.HIGH if direction == 0 else GPIO.LOW)

    steps = int(SPR * revs)
    
    print(f"Rotating {revs} revolutions {'CW' if direction == 0 else 'CCW'}...")

    for _ in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(delay)

    print("Done")