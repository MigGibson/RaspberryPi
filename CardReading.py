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
registration = True
count = 0
eventID = ""

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
print "Welcome to the Athlete Kinect"
print "Press Ctrl-C to stop."
print "For visualization purposes we are displaying here."
print "Currently in Registration Mode."

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
        print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
        
        opener = urllib.FancyURLopener({})
        f = opener.open("http://192.168.0.19:9876/Service1.svc/NewCardID/" + str(uid[0]) + "," +str(uid[1]) + "," + str(uid[2])+ "," + str(uid[3]))
        response = f.read()
        
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        
        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
        
        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            #Check if the card is the switcher card.
            #CardID = 86,162,118,203
            cardID = str(uid[0]) + "," +str(uid[1]) + "," + str(uid[2])+ "," + str(uid[3])
            
            if cardID == "86,162,118,203":
                if registration:
                    registration = False
                else:
                    registration = True
                
                if registration:
                    print "Registration mode on!"
                else:
                    print "Recording mode on!"
                
            opener = urllib.FancyURLopener({})
            #Get Event ID
            if count == 0:
                f = opener.open("http://192.168.0.28:9876/Service1.svc/getEventID/" + str(uid[0]) + "," +str(uid[1]) + "," + str(uid[2])+ "," + str(uid[3]) + "/" + time.strftime("%d/%m/%Y"))
                response = f.read()
                print response
				
                if response != "{\"getEventIDResult\":\"\"}":
                    eventID = response[21:-2]
                    count += 1
            else:
                #####################
                #Add participant to register.
                if registration:
                    f = opener.open("http://192.168.0.28:9876/Service1.svc/RegisterParticipant/" + cardID)
                else:
                    f = opener.open("http://192.168.0.28:9876/Service1.svc/RecordTime/" + cardID + "/" + eventID)
                    print "http://192.168.0.28:9876/Service1.svc/RecordTime/" + cardID + "/" + eventID
                #####################
                #Do something with result:
                response = f.read()
                print response
                #####################
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print "Authentication error"
        
    
