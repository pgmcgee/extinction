from phue import Bridge

b = Bridge("192.168.1.126")
b.connect()

b.get_api()

for l in b.lights:
    l.transitiontime = 1
    l.hue = 15331
    l.saturation = 127
