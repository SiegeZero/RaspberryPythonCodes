import RPi.GPIO as GPIO
import time
GPIO.setmode( GPIO.BOARD)
GPIO.setup( 37, GPIO.OUT)
GPIO.output( 37, GPIO.LOW)
time.sleep(0.7)
GPIO.output( 37, GPIO.HIGH)

GPIO.cleanup()
