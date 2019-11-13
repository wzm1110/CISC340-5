#!/usr/bin/env python
import time
import serial
import smtplib
'''
This is the python script for cisc340 project, which includes the function of minicom to show
the reading of data from serial port, and can also send notification to users when certain 
signal/breach is detected.
 
Team 5
'''
smtpUser = '2019cisc340.team5@gmail.com'
smtpPass = 'team5password'

toAdd = '2019cisc340.team5@gmail.com'
fromAdd = '2019cisc340.team5@gmail.com'

subject = 'Alert msg for cisc340 project'
header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject
body_fire = 'Fire detected!'
body_breach = 'Breach detected!'


ser = serial.Serial(
 port='/dev/ttyUSB1',
 baudrate = 9600,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=1
)

fire_detected = False
breach_detected = False

while 1:
 reading = 0
 magnet = 0
 x=ser.readline()
 if "button" in x:
     if x[-2] != '0':
	breach_detected = False
	fire_detected = False
 elif "jbin" in x:
     if x[14:16] == "FD" and breach_detected == False:
	print "breach"
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(smtpUser, smtpPass)
        s.sendmail(fromAdd, toAdd, header + '\n' + body_breach)
        breach_detected = True
	s.quit()
 elif "VAUX14" in x :
     if len(x) == 19:
         reading = x[15:17]
     elif len(x) == 20:
         reading =  x[15:18]
     if int(reading) > 100 and fire_detected == False:
         print "fire"
         s = smtplib.SMTP('smtp.gmail.com', 587)
         s.ehlo()
         s.starttls()
         s.ehlo()
         s.login(smtpUser, smtpPass)
         s.sendmail(fromAdd, toAdd, header + '\n' + body_fire)
         fire_detected = True
	 s.quit()
