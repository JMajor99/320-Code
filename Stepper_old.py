import RPi.GPIO as GPIO
import time

# GPIO pin setup (IN1..IN4 to ULN2003 board)
IN1, IN2, IN3, IN4 = 4, 18, 5, 19
pins = [IN1, IN2, IN3, IN4]

# Stepper motor variables
steps_per_revolution = 2048   # 28BYJ-48
rpm = 20
delay = 60.0 / (steps_per_revolution * rpm)  # seconds per step

# Half-step sequence for 28BYJ-48
sequence = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

# Setup
GPIO.setmode(GPIO.BCM)
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

def step_motor(steps, direction=1):
    """Rotate stepper by number of steps. direction=1 for CW, -1 for CCW."""
    step_count = len(sequence)
    step_dir = direction
    step_index = 0

    for _ in range(abs(steps)):
        for pin in range(4):
            GPIO.output(pins[pin], sequence[step_index][pin])
        step_index = (step_index + step_dir) % step_count
        time.sleep(delay)

    # turn off coils when done
    for pin in pins:
        GPIO.output(pin, 0)

try:
    print("Enter: <rotations> <direction>")
    print("Example: 5 1   --> 5 rotations clockwise")
    print("Example: 3 -1  --> 3 rotations counterclockwise")

    while True:
        user_input = input("Command: ")
        try:
            rotations, direction = map(int, user_input.strip().split())
            steps_to_move = steps_per_revolution * rotations * direction
            print(f"Moving {rotations} rotations in direction {direction}")
            step_motor(steps_to_move, direction)
            print("Done.")
        except ValueError:
            print("Invalid input. Format: <rotations> <direction>")

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    GPIO.cleanup()