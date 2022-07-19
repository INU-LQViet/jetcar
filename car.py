from motor import Motor

class Car():
    def __init__(self):
        self.ENA = 33
        self.IN1 = 21
        self.IN2 = 23

        self.ENB = 35
        self.IN3 = 29
        self.IN4 = 31
        self.lmotor = Motor(self.IN1, self.IN2, self.ENA)
        self.rmotor = Motor(self.IN3, self.IN4, self.ENB)

    def carforward(self):
        self.lmotor.forward()
        self.rmotor.forward()

    def carbackward(self):
        self.lmotor.backward()
        self.rmotor.backward()

    def carleft(self):
        self.lmotor.stop()
        self.rmotor.forward()

    def carright(self):
        self.rmotor.stop()
        self.lmotor.forward()

    def stop(self):
        self.rmotor.stop()
        self.lmotor.stop()
