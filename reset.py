from adafruit_motorkit import MotorKit

if __name__ == '__main__':
    kit = MotorKit()
    kit.stepper1.release()
    kit.stepper2.release()