from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

from multiprocessing import Process

def move_motor(motor, direction, steps):
    for i in range(steps):
        motor.onestep(direction=direction)

if __name__ == '__main__':
    kit = MotorKit()
    t1 = Process(target=move_motor, args=(kit.stepper1, stepper.FORWARD, 0,))
    t2 = Process(target=move_motor, args=(kit.stepper2, stepper.BACKWARD, 100,))
    t1.start()
    t2.start()
