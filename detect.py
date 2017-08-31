import RPi.GPIO as GPIO
import time
GPIO.setmode( GPIO.BOARD)
detector_in = 7
machine_out1 = 11
machine_out2 = 12
GPIO.setup(detector_in, GPIO.IN)
GPIO.setmode( GPIO.BOARD)
GPIO.setup( machine_out1, GPIO.OUT)
GPIO.setup( machine_out2, GPIO.OUT)
try:
    while True:
        #sleep for an hour if the current hour is between 0 o'clock and 5 o'clock, which means that detector would not work at deep night and early morning from 0:00 to 6:00
        current_hour = time.localtime().tm_hour
        if current_hour >= 0 and current_hour <= 5:
            time.sleep(3600)
        if GPIO.input( detector_in):
            # print the current time at std.out
            current_time = time.localtime()
            print "detected at " + str( current_time.tm_year) + "-" + str( current_time.tm_mon) + "-" + str( current_time.tm_mday) + "-" + str( current_time.tm_hour) + "-" + str( current_time.tm_min) + "-" + str( current_time.tm_sec)
            time.sleep(1.5)
            if GPIO.input(detector_in) == 0:
                continue
            # start the machine
            GPIO.output( machine_out1, GPIO.HIGH)
            GPIO.output( machine_out2, GPIO.LOW)
            # do running the machine while the detector response True and the machine working for less than 1.5 seconds
            t = 0
            while GPIO.input( detector_in) and t < 3:
                t = t + 1
                time.sleep(0.6)
            # stop the machine
            GPIO.output( machine_out1, GPIO.LOW)
            GPIO.output( machine_out2, GPIO.LOW)
            # let the detector rest for 3 seconds after run the machine
            time.sleep(3)
        else:
            # sleep the detector for 1 seconds
            time.sleep(1)
except KeyboardInterrupt:
    print "quit by keyboard"
except:
    print "other exception"
finally:
    GPIO.cleanup()
