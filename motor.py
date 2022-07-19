import Jetson.GPIO as GPIO

class Motor():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    def __init__(self, IN1, IN2, EN):
        self.IN1 = IN1
        self.IN2 = IN2
        self.EN = EN
        GPIO.setup(self.EN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN2, GPIO.OUT, initial=GPIO.LOW)
    def stop(self):
        GPIO.output(self.EN, GPIO.LOW)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
    
    def forward(self):
        GPIO.output(self.EN, GPIO.HIGH)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        
    def backward(self):
        GPIO.output(self.EN, GPIO.HIGH)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        