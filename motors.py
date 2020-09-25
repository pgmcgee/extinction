try:
    from adafruit_motorkit import MotorKit
except NotImplementedError:
    from test_motorkit import MotorKit

from adafruit_motor import stepper

import math
import os

"""
    All length measurements in this package are in `cm`
    All time measurements in this package are in `ms`
"""

STEP_DEGREES = 1.8
SPOOL_CIRCUMFERENCE = 7.8


class Motor:

    def __init__(self, name, stepper, x_offset, length):
        self.name = name
        self.x_offset = x_offset
        self.length = length
        self.stepper = stepper
        self.spool_circumference = SPOOL_CIRCUMFERENCE

    def onestep(self, direction=stepper.BACKWARD):
        print(f"Moving {self.name} " + ("forward" if direction == stepper.FORWARD else "backward"))

        if os.environ.get("ENV") != "test":
            self.stepper.onestep(direction=direction)
        self.length = self.nextstep(direction)

    def nextstep(self, direction=stepper.BACKWARD):
        length_change = 1 if self.is_longer(direction) else -1
        return self.length + length_change * (self.spool_circumference / (360 / STEP_DEGREES))

    def is_longer(self, direction):
        if self.name == "motor1":
            return direction == stepper.BACKWARD
        else:
            return direction == stepper.FORWARD


class MotorSet:
    def __init__(self, motor_locs, init_x, init_y):
        self.kit = MotorKit()

        self.motor_locs = motor_locs

        length1, length2 = self._calculate_lengths(init_x, init_y)

        self.motor1 = Motor("motor1", self.kit.stepper1, self.motor_locs[0], length1)
        self.motor2 = Motor("motor2", self.kit.stepper2, self.motor_locs[1], length2)

        self.x, self.y = self.original_x, self.original_y = init_x, init_y

    def move_xy(self, x, y):
        self.original_x, self.original_y = self.x, self.y

        while abs(x - self.x) > 1 or abs(y - self.y) > 1:
            combinations = [(self.motor1, stepper.FORWARD, 'motor1'), (self.motor1, stepper.BACKWARD, 'motor1'),
                            (self.motor2, stepper.FORWARD, 'motor2'), (self.motor2, stepper.BACKWARD, 'motor2')]

            best_distance = math.inf
            best_combo = None

            results = []

            for combo in combinations:
                motor = combo[0]
                direction = combo[1]
                kw = combo[2] + '_length'

                new_length = motor.nextstep(direction=direction)
                new_x, new_y = self._calculate_xy(**{kw: new_length})
                distance = self._evaluate_new_point(new_x, new_y, x, y)

                if distance < best_distance:
                    best_combo = combo
                    best_distance = distance

                results.append({
                    'distance': distance,
                    'new_length': new_length,
                    'new_x': new_x,
                    'new_y': new_y,
                })

            best_motor = best_combo[0]
            best_direction = best_combo[1]
            best_motor.onestep(direction=best_direction)

            self.x, self.y = self._calculate_xy()

        self.original_x, self.original_y = self.x, self.y

    def _distance_from_line(self, x1, y1, x2, y2, x0, y0):
        return abs((y2 - y1) * x0 - (x2 - x1) * y0 + (x2 * y1) - (y2 * x1)) / math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)

    def _calculate_lengths(self, x, y):
        length1 = math.sqrt(x ** 2 + y ** 2)
        length2 = math.sqrt((self.motor_locs[1] - x) ** 2 + y ** 2)
        return [length1, length2]

    def _calculate_xy(self, motor1_length=None, motor2_length=None):
        if motor1_length is None:
            motor1_length = self.motor1.length
        if motor2_length is None:
            motor2_length = self.motor2.length

        motors_length = self.motor_locs[1] - self.motor_locs[0]

        x = abs(motors_length ** 2 + motor1_length ** 2 - motor2_length ** 2) / (2 * motors_length)
        y = math.sqrt(abs(motor1_length ** 2 - x ** 2))
        return x, y

    def _evaluate_new_point(self, new_x, new_y, result_x, result_y):
        distance_from_point = math.sqrt((result_x - new_x) ** 2 + (result_y - new_y) ** 2)
        distance_from_line = self._distance_from_line(self.original_x, self.original_y, result_x, result_y, new_x, new_y)
        return 2 * distance_from_point ** 2 + distance_from_line ** 3

    # def _evaluate_new_point(self, new_x, new_y, result_x, result_y):
    #     new_y_slope = new_y - self.y
    #     new_x_slope = new_x - self.x
    #     result_y_slope = result_y - self.y
    #     result_x_slope = result_x - self.x
    #
    #     if result_x_slope > 0 and new_x_slope < 0:
    #         return math.inf
    #     if result_x_slope < 0 and new_x_slope > 0:
    #         return math.inf
    #
    #     # Confirm we're moving in the right direction
    #     if (new_y_slope > 0 and result_y_slope < 0) or \
    #         (new_y_slope < 0 and result_y_slope > 0):
    #         correct_y = False
    #     else:
    #         correct_y = True
    #     if (new_x_slope > 0 and result_x_slope < 0) or \
    #         (new_x_slope < 0 and result_x_slope > 0):
    #         correct_x = False
    #     else:
    #         correct_x = True
    #
    #     if not correct_x and not correct_y:
    #         return math.inf
    #
    #     return self._distance_from_line(self.original_x, self.original_y, result_x, result_y, new_x, new_y)


    # def move_xy(self, x, y):
    #     length1, length2 = self._calculate_lengths(x, y)
    #     length_diff1 = length1 - self.motor1.length
    #     length_diff2 = length2 - self.motor2.length
    #
    #     while abs(length_diff1) >= 1 and abs(length_diff2) >= 1:
    #         if abs(length_diff1) > abs(length_diff2):
    #             direction = stepper.BACKWARD if length_diff1 > 0 else stepper.FORWARD
    #             print("Moving motor1 " + ("forward" if direction == stepper.FORWARD else "backward"))
    #             self.motor1.onestep(direction=direction)
    #         else:
    #             direction = stepper.BACKWARD if length_diff2 > 0 else stepper.FORWARD
    #             print("Moving motor2 " + ("forward" if direction == stepper.FORWARD else "backward"))
    #             self.motor2.onestep(direction=direction)
    #         length1, length2 = self._calculate_lengths(x, y)
    #         length_diff1 = length1 - self.motor1.length
    #         length_diff2 = length2 - self.motor2.length