import time


class Stepper:
    def __init__(self, index):
        self.index = index

    def onestep(self, direction):
        print(f"Stepping {self.index}")


class MotorKit:
    def __init__(self):
        self.stepper1 = Stepper(1)
        self.stepper2 = Stepper(2)
