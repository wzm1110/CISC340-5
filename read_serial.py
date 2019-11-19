
#!/usr/bin/env python
import time
import serial
import smtplib
import sys
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


def system(arm,status):
    if arm:
        return check(status)
    else:
        return [False, False] 

def check(status):
     fire_detected = status[0]
     breach_detected = status[1]
     reading = 0      
     while not breach_detected and not fire_detected:
     	x=ser.readline()
     	#print x
	if "button" in x:
            if x[-2] != '0':
                breach_detected = False
                fire_detected = False
		
     	elif "jbin" in x and not breach_detected:
            if x[14:16] == "FD":
                print "breach"
                print breach_detected, fire_detected
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(smtpUser, smtpPass)
                s.sendmail(fromAdd, toAdd, header + '\n' + body_breach)
                print breach_detected, fire_detected
		s.quit()
		breach_detected = True

        elif "VAUX14" in x and not fire_detected:
             if len(x) == 19:
                 reading = x[15:17]
             elif len(x) == 20:
                 reading =  x[15:18]
             if int(reading) > 100:
                 print "fire"
                 print fire_detected, breach_detected
		 s = smtplib.SMTP('smtp.gmail.com', 587)
                 s.ehlo()
             	 s.starttls()
             	 s.ehlo()
             	 s.login(smtpUser, smtpPass)
             	 s.sendmail(fromAdd, toAdd, header + '\n' + body_fire)
             	 print fire_detected, breach_detected
		 s.quit()
		 fire_detected = True
        #else:
            #fire_detected, breach_detected = False, False
     return [fire_detected, breach_detected]
def isFire():
    return fire_detected

def isBreached():
    return breach_detected
