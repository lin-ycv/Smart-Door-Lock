import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import datetime
import csv

relayPin = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin, GPIO.OUT)
GPIO.output(relayPin,1)

def pin_on(pin):
    GPIO.output(pin,0)

def pin_off(pin):
    GPIO.output(pin,1)

def getUsers():
    with open("/home/pi/Desktop/verified") as file:
        return list(csv.reader(file))

def tmr():
    return datetime.date.today()+ datetime.timedelta(days=1)
    
rfid= SimpleMFRC522()
verified = getUsers()
updateDate = tmr()

print("Sentry started")
try:
    while True:
        cardid = rfid.read_id()
        print(cardid)
        now = datetime.datetime.now()
        if now.date() >= updateDate:
            verified = getUsers()
            updateDate = tmr()
        for user in verified:
            if user[2] == str(cardid):
                if str(now.isoweekday()) in user[3]:
                    pin_on(relayPin)
                    print(user[0],now)
                    time.sleep(2)
                    pin_off(relayPin)
                    break
                else:
                    print(user[0], ":Time restricted -", now)            
        time.sleep(2)

finally:
    pin_off(relayPin)
    GPIO.cleanup()
    print("cleaned up")
