#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import time
import MFRC522
import signal
continue_reading = True
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    continue_reading = False

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
is_roommates = True
# Welcome message

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    is_roommates = False
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        if str(uid[0])+'.'+str(uid[1])+'.'+str(uid[2])+'.'+str(uid[3]) in ['111.217.97.68','175.55.100.68','0.193.181.130','143.167.100.68']:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(11, GPIO.OUT)
            GPIO.setup(12, GPIO.OUT)
            GPIO.output(11, GPIO.HIGH)
            GPIO.output(12, GPIO.LOW)

            time.sleep(0.2)
            GPIO.setup(37, GPIO.OUT)
            GPIO.output(37, GPIO.LOW)

            time.sleep(0.8)
        GPIO.cleanup()
