import RPi.GPIO as GPIO
import time

# Define the GPIO pins connected to ULN2003 IN1-IN4
motor_pins = [23, 18, 5, 19]  # Example BCM pin numbers
steps_per_revolution = 4096   # 28BYJ-48 in half-step mode
desired_rpm = 15

# Calculate delay per half-step
steps_per_sec = (desired_rpm * steps_per_revolution) / 60.0
step_delay = 1.0 / steps_per_sec  # ≈ 0.000976s

# Half-step sequence
halfstep_sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

# Set up GPIO
GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

def set_step(w1, w2, w3, w4):
    GPIO.output(motor_pins[0], w1)
    GPIO.output(motor_pins[1], w2)
    GPIO.output(motor_pins[2], w3)
    GPIO.output(motor_pins[3], w4)

def rotate_stepper(steps, direction):
    current_step = 0
    for _ in range(abs(steps)):
        if direction == 1:  # Clockwise
            current_step = (current_step + 1) % len(halfstep_sequence)
        else:  # Counter-clockwise
            current_step = (current_step - 1) % len(halfstep_sequence)

        set_step(*halfstep_sequence[current_step])
        time.sleep(step_delay)  # fixed delay for 15 RPM

try:
    print("Enter: <rotations> <direction>")
    print("Example: 5 1   --> 5 rotations clockwise")
    print("Example: 3 -1  --> 3 rotations counterclockwise")

    while True:
        user_input = input("Command: ")
        try:
            rotations, direction = map(int, user_input.split())
        except ValueError:
            print("Invalid input. Use format: <rotations> <direction>")
            continue

        steps = rotations * steps_per_revolution
        print(f"Moving {rotations} rotations in direction {direction} at {desired_rpm} RPM")
        rotate_stepper(steps, direction)
        print("Done. Enter next command:")

except KeyboardInterrupt:
    print("\nStopped by user")

finally:
    GPIO.cleanup()
