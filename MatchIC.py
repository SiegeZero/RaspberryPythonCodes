#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import time
import MFRC522
import signal
# init the gpio
continue_reading = True
# user_uid_pool
UIDS = [
    '111.217.97.68',
    '175.55.100.68',
    '0.193.181.130',
    '143.167.100.68',
    '79.166.99.68',
    '15.73.100.68'
    ]
# machine_during = alarm_delay + alarm_during
alarm_delay = 0.2
alarm_during = 0.8
GPIO.setmode(GPIO.BOARD)
machine_out1 = 11
machine_out2 = 12
beeper_out = 37
detector_in = 7
GPIO.setup( detector_in, GPIO.IN)
GPIO.setup( machine_out1, GPIO.OUT)
GPIO.setup( machine_out2, GPIO.OUT)
GPIO.setup( beeper_out, GPIO.OUT)
def myCallback( channel):
    # sleep for an hour if the current hour is between 0 o'clock and 5 o'clock, which means that detector would not work at deep night and early morning from 0:00 to 6:00
    current_hour = time.localtime().tm_hour
    if current_hour >= 0 and current_hour <= 5:
        time.sleep(3600)
    if GPIO.input( detector_in):
        # print the current time at std.out
        current_time = time.localtime()
        print "detected at " + str( current_time.tm_year) + "-" + str( current_time.tm_mon) + "-" + str( current_time.tm_mday) + "-" + str( current_time.tm_hour) + "-" + str( current_time.tm_min) + "-" + str( current_time.tm_sec)
        # start the machine
        GPIO.output( machine_out1, GPIO.HIGH)
        GPIO.output( machine_out2, GPIO.LOW)
        # do running the machine while the detector response True and the machine working for less than 1.4 seconds
        t = 0
        while GPIO.input( detector_in) and t < 2:
            t = t + 1
            time.sleep(0.7)
        # stop the machine
        GPIO.output( machine_out1, GPIO.LOW)
        GPIO.output( machine_out2, GPIO.LOW)
        # let the detector rest for 3 seconds after run the machine
        time.sleep(3)
    else:
        # sleep the detector for 1 seconds
        time.sleep(1)
# detector callback
GPIO.add_event_detect( detector_in, GPIO.RISING, callback=myCallback, bouncetime=200)
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
try:
    while continue_reading:
        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            read_uid = str(uid[0])+'.'+str(uid[1])+'.'+str(uid[2])+'.'+str(uid[3])
            current_time = time.localtime()
            time_of_tips = " at " + str( current_time.tm_year) + "-" + str( current_time.tm_mon) + "-" + str( current_time.tm_mday) + "-" + str( current_time.tm_hour) + "-" + str( current_time.tm_min) + "-" + str( current_time.tm_sec)
            tips = "access denied"
            if read_uid in UIDS:
                tips = read_uid
                # run the machine
                GPIO.output( machine_out1, GPIO.HIGH)
                GPIO.output( machine_out2, GPIO.LOW)
                # keep running for 0.2 seconds
                time.sleep( alarm_delay)
                # do not disturb while noon nap
                if current_time.tm_hour <= 12 or current_time.tm_hour >= 15:
                    # the beeper alarm
                    GPIO.output( beeper_out, GPIO.LOW)
                # keep alarming for 0.8 seconds
                time.sleep( alarm_during)
                # stop the machine
                GPIO.output( machine_out1, GPIO.LOW)
                GPIO.output( machine_out2, GPIO.LOW)
                # stop the beeper
                GPIO.output( beeper_out, GPIO.HIGH)
            print tips + time_of_tips
        time.sleep(1.5)
except KeyboardInterrupt:
    print "quit by keyboard"
except:
    print "other exception occurred"
finally:
    GPIO.cleanup()
