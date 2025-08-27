import RPi.GPIO as GPIO
import time

servo_pin = 21  # PWM pin (GPIO18)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)  # 50Hz
pwm.start(0)

def set_angle(angle):
    duty = 2 + (angle / 18)  # Maps 0–180 degrees to 2–12% duty
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)  # Stop sending signal (prevents jitter)
    
def open_grabber():
    set_angle(0)
    
def close_grabber():
    set_angle(180)

try:
    while True:
        state = input("Enter State (open/close): ") # 180 degree is fully closed
        if state == "open":
            open_grabber()
        elif state == "close":
            close_grabber()

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    pwm.stop()
    GPIO.cleanup()
