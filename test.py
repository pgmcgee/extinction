import unittest
from motors import MotorSet


class TestMotorSet(unittest.TestCase):
    # def test_move_300_216(self):
    #     motor_set = MotorSet([0, 305], 3, 15)
    #     xy = (290, 195,)
    #
    #     print(f"Moving to {xy[0]} {xy[1]}")
    #     motor_set.move_xy(xy[0], xy[1])
    #
    #     xy = (2, 12.5,)
    #     print(f"\n\n\n\n   !!!! Moving to {xy[0]} {xy[1]} !!!!\n\n\n\n")
    #     motor_set.move_xy(xy[0], xy[1])

    def test_move_300_216(self):
        motor_set = MotorSet([0, 305], 275, 205)
        xy = (2, 12.5,)

        print(f"Moving to {xy[0]} {xy[1]}")
        motor_set.move_xy(xy[0], xy[1])


if __name__ == '__main__':
    unittest.main()
