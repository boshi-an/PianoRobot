import RPi.GPIO as GPIO
import time
from serial.tools import list_ports
import pydobot

class ArmServo() :
    
    def __init__(self) :
        
        available_ports = list_ports.comports()
        print(f'available ports: {[x.device for x in available_ports]}')
        self.port = available_ports[0].device
        self.device = pydobot.Dobot(port=self.port, verbose=True)

        # self.pose = self.device.pose()
        
        # print('current pose: {}'.format(self.pose))
    
    def init_pose(self) :
        
        x, y, z, r, j1, j2, j3, j4 = self.device.pose()
        
        print('current pose: {}, {}, {}'.format(x, y, z))
        
        self.device.move_to(180, 0, -40, r, wait=True)
        
        x, y, z, r, j1, j2, j3, j4 = self.device.pose()
        
        print('pose after reset: {}, {}, {}'.format(x, y, z))
    
    def move_to(self, displace) :
        
        x, y, z, r, j1, j2, j3, j4 = self.device.pose()
        
        self.device.move_to(180, displace*20, -40, r, wait=True)

class HandServo() :
    
    def __init__(self) :
        
        # Corresponding fingers: 1, 2, 3, 4, 5
        self.port = [5, 6, 13, 19, 26]
        self.base = [5, 5.8, 5.8, 5.6, 5]
        self.freq = 50
        GPIO.setmode(GPIO.BCM)
        for port in self.port :
            GPIO.setup(port, GPIO.OUT)
        self.pwms = [GPIO.PWM(port, self.freq) for port in self.port]
        for pwm in self.pwms :
            pwm.start(0)
    
    def __del__(self) :
        
        GPIO.cleanup()
    
    def set_angle(self, angle) :
        
        for p, a, b in zip(self.pwms, angle, self.base) :
            
            duty = a + b
            p.ChangeDutyCycle(duty)

if __name__ == "__main__" :
    
    arm = ArmServo()
    
    arm.init_pose()
    
    arm.move_to(1)
    
    time.sleep(1)
    
    arm.move_to(2)
    
    exit()
    
    servo = HandServo()
    # while True :
    for i in range(1) :
        servo.set_angle([0, 30, 0, 0, 0])
        time.sleep(1)
        servo.set_angle([0, 0, 30, 0, 0])
        time.sleep(1)
        servo.set_angle([0, 0, 0, 30, 0])
        time.sleep(1)
        servo.set_angle([0, 0, 0, 0, 30])
        time.sleep(1)
    servo.set_angle([0, 0, 0, 0, 0])
    time.sleep(1)
    del servo