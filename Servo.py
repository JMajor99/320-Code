import RPi.GPIO as GPIO
import time

servo_pin = 18  # PWM pin (GPIO18)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)  # 50Hz
pwm.start(0)

def set_angle(angle):
    duty = 2 + (angle / 18)  # Maps 0–180 degrees to 2–12% duty
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)  # Stop sending signal (prevents jitter)

try:
    while True:
        angle = int(input("Enter angle (0 to 180): "))
        set_angle(angle)

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    pwm.stop()
    GPIO.cleanup()
