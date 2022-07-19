import time
from motor import Motor
import evdev

devicePath = "/dev/input/event2"

device = evdev.InputDevice(devicePath)

# for 1st Motor on ENA
ENA = 33
IN1 = 21
IN2 = 23

ENB = 35
IN3 = 31
IN4 = 29

lmotor = Motor(IN1, IN2, ENA)
rmotor = Motor(IN3, IN4, ENB)

def carforward(lmotor, rmotor):
    lmotor.forward()
    rmotor.forward()

def carbackward(lmotor, rmotor):
    lmotor.backward()
    rmotor.backward()

def carleft(lmotor, rmotor):
    lmotor.backward()
    rmotor.forward()

def carright(lmotor, rmotor):
    rmotor.backward()
    lmotor.forward()

def stop(lmotor, rmotor):
    rmotor.stop()
    lmotor.stop()

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        if event.value == 1:
            if event.code == 288:
                carforward(lmotor, rmotor)
                print("Game pad 1!")
            elif event.code == 289:
                carright(lmotor, rmotor)
                print("Game pad 2!")
            elif event.code == 290:
                carbackward(lmotor, rmotor)
                print("Game pad 3!")
            elif event.code == 291:
                carleft(lmotor, rmotor)
                print("Game pad 4!")
            else :
                stop(lmotor, rmotor)
        else:
            stop(lmotor, rmotor)