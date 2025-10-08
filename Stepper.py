import RPi.GPIO as GPIO
import time

# Pin setup
DIR = 20      # Direction pin
STEP = 21     # Step pin
SPR = 200     # Steps per revolution (adjust if microstepping)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

try:
    # Input: "0 5" for 5 rev CW, "1 2.5" for 2.5 rev CCW
    direction, revs = input("Enter direction (0=CW, 1=CCW) and revolutions: ").split()
    direction = int(direction)
    revs = float(revs)

    GPIO.output(DIR, GPIO.HIGH if direction == 0 else GPIO.LOW)

    steps = int(SPR * revs)
    delay = 0.001  # adjust for speed

    print(f"Rotating {revs} revolutions {'CW' if direction == 0 else 'CCW'}...")

    for _ in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(delay)

    print("Done")

except KeyboardInterrupt:
    print("\nStopped manually.")
finally:
    GPIO.cleanup()
