from phue import Bridge
import time
from playsound import playsound
import threading

HUE_MAX = 65535
HUE_CONVERT = 360

b = Bridge("192.168.1.126")
b.connect()

b.get_api()

colors = [[20, 40, 0], [0, 20, 40], [40, 0, 20]]
colors = colors * 2

for l in b.lights:
    l.brightness = 0  # Max brightness
    l.saturation = 254  # Max saturation
    l.transitiontime = 0

# Explosion
explosion_light = b.lights[2]
explosion_light.hue = HUE_MAX * 20 / HUE_CONVERT
explosion_light.transitiontime = 2

sound_thread = threading.Thread(target=lambda: playsound('./Atomic_Bomb-Sound_Explorer-897730679.mp3'))
sound_thread.start()
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
    l.transitiontime = 0
    l.brightness = 0
