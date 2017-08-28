import RPi.GPIO as GPIO
import time
GPIO.setwarnings( False)

while True:
    #sleep for an hour if the current hour is between 0 and 5
    hour = time.localtime().tm_hour
    if hour >= 0 and hour <= 5:
        time.sleep(3600)
    #get input from pin 7
    GPIO.setmode( GPIO.BOARD)
    GPIO.setup(7, GPIO.IN)
    if GPIO.input(7):
        # do something
        GPIO.setmode( GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(12, GPIO.OUT)
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(12, GPIO.LOW)
        t = 0
        # keep doing that thing if s.b. is still there til it stay 1.5 seconds
        while GPIO.input(7) and t < 3:
            t = t + 1
            time.sleep(0.5)
        # stop do that thing
        GPIO.output(11, GPIO.LOW)
        time.sleep(5)
    else:
        time.sleep(1)
GPIO.cleanup()
