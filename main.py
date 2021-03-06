from phue import Bridge
import time
import pygame
import threading
from motors import MotorSet

HUE_MAX = 65535
HUE_CONVERT = 360

b = Bridge("192.168.1.126")
b.connect()

b.get_api()

motor_set = MotorSet([0, 305], 2, 12.5)

pygame.mixer.init()
bomb_sound = pygame.mixer.music.load("./Atomic_Bomb-Sound_Explorer-897730679.mp3")


def move_lantern():
    motor_set.move_xy(275, 190)

def dim_all_lights():
    for l in b.lights:
        l.transitiontime = None
        l.on = False

def explosion():
    colors = [[20, 40, 0], [0, 20, 40], [40, 0, 20]]
    colors = colors * 3

    for l in b.lights:
        l.on = True

    for l in b.lights:
        l.brightness = 0  # Max brightness
        l.saturation = 254  # Max saturation
        l.transitiontime = None

    # Explosion
    explosion_light = b.lights[2]
    explosion_light.hue = HUE_MAX * 20 / HUE_CONVERT
    explosion_light.transitiontime = 2

    pygame.mixer.music.play()
    time.sleep(0.8)
    for i in range(3):
        explosion_light.transitiontime = 10
        explosion_light.brightness = 255
        time.sleep(1.0)
        explosion_light.transitiontime = 2
        explosion_light.brightness = 64
        time.sleep(0.2)

    explosion_light.transitiontime = 0

    for cg in colors:
        for l, c in zip(b.lights, cg):
            print(f"Adjusting {b.name} to {c}")
            if c == 0:
                l.transitiontime = 5
                l.brightness = 128
            else:
                l.transitiontime = 2
                l.brightness = 254
                l.transitiontime = 5
                l.hue = HUE_MAX * c / HUE_CONVERT
        time.sleep(0.3)

    for l in b.lights:
        l.transitiontime = None
        l.brightness = 0

def reset():
    try:
        for l in b.lights:
            l.on = True
            l.transitiontime = None
            l.brightness = 254
            l.hue = HUE_MAX * 60 / HUE_CONVERT
    except:
        print("There was an error setting lights before reset")

    motor_set.move_xy(2, 12.5)

    try:
        for l in b.lights:
            l.brightness = 0
            l.hue = HUE_MAX * 20 / HUE_CONVERT
            l.transitiontime = None
            l.on = False
    except:
        print("There was an error setting lights after reset")

if __name__ == '__main__':
    # while True:
    try:
        dim_all_lights()
        time.sleep(5)
        move_lantern()
        explosion()
        time.sleep(10)
    finally:
        reset()
    motor_set.stop()
