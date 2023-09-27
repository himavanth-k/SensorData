import RPi.GPIO as GPIO
import time
from pyrebase import initialize_app

# Initialize Firebase
config = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_AUTH_DOMAIN",
    "databaseURL": "YOUR_DATABASE_URL",
    "projectId": "YOUR_PROJECT_ID",
    "storageBucket": "YOUR_STORAGE_BUCKET",
    "messagingSenderId": "YOUR_MESSAGING_SENDER_ID",
    "appId": "YOUR_APP_ID"
}

firebase = initialize_app(config)
db = firebase.database()

pir_sensor = 11
piezo = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(piezo, GPIO.OUT)
GPIO.setup(pir_sensor, GPIO.IN)

current_state = 0 

try:
    while True:
        time.sleep(0.1)
        current_state = GPIO.input(pir_sensor)
        
        if current_state == 1:
            print("Motion detected")
            GPIO.output(piezo, True)
            time.sleep(1)
            GPIO.output(piezo, False)
            
            # Push data to Firebase
            db.child("motion").push({"status": "detected"})
        else:
            print("No motion detected")
            
            # Push data to Firebase
            db.child("motion").push({"status": "not detected"})

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
