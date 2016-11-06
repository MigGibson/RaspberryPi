#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal

#################
import urllib
import time
#################

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Raffle"
print "Press Ctrl-C to stop."
print "For visualization purposes we are displaying here."
print "Currently in Raffle Mode."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        # Print UID
        print "Card read UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3])
        cardID = str(uid[0]) + "," +str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3])
        
        if(cardID == "37,131,26,78")
            opener = urllib.FancyURLopener({})
            f = opener.open("http://192.168.43.193:9876/Service1.svc/recordBoxChallengeTime/" + cardID)
            response = f.read()
            
        if(response == "0"):
		    print "You have successfully entered the raffle!"
        
    
