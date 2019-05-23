import pycom

from network import LoRa
from network import WLAN

import time

PYMESHSTATE = ["PYMESH_ROLE_DISABLED", "PYMESH_ROLE_DETACHED", "PYMESH_ROLE_CHILD", "PYMESH_ROLE_ROUTER", "PYMESH_ROLE_LEADER"]

class pyLED:
    color = {'off': 0x000000, 'red':0xff0000, 'orange': 0xff8000, 'yellow': 0xffff00, 'green': 0x00ff00, 'lightlite' : 0xe0e0e0, 'blue' : 0x00bfff, 'purple' : 0x8000ff, 'pink': 0xff00ff}
    debug = False

    def setLED(self, value):
        if (not self.debug):
            pycom.rgbled(self.color[value])

    def flashLED(self, value, d=2):
        if (not self.debug):
            pycom.rgbled(self.color[value])
            time.sleep(d)
            pycom.rgbled(self.color['off'])


# init...

## disabling WiFi
wlan = WLAN()
wlan.deinit()

## setting LED
pycom.heartbeat(False)
led = pyLED()


print("Enabling Pymesh")
lora = LoRa(mode=LoRa.LORA)# region=LoRa.EU868, frequency = 863000000, bandwidth=LoRa.BW_125KHZ, sf=7
try:
    mesh = lora.Mesh()
except e:
    print(e)
    exit()

time.sleep(2)

print("looping")
while True:
    cstate1 = mesh.cli('state')
    cstate2 = PYMESHSTATE[mesh.state()]
    print("%d: current state %s [%s]"%(time.time(), cstate1, cstate2))

    if ("router" in cstate1) or ("leader" in cstate1) or ("child" in cstate1):
        break
    else:
        time.sleep(2)


led.flashLED("green")
cstate1 = mesh.cli('state')
cstate2 = PYMESHSTATE[mesh.state()]
print("%d: current state %s [%s]"%(time.time(), cstate1, cstate2))


while mesh.cli('singleton'):
    cstate1 = mesh.cli('state')
    cstate2 = PYMESHSTATE[mesh.state()]
    print("%d: waiting for neighbors [%s]"%(time.time(), cstate2))
    led.flashLED("red",1)
    time.sleep(2)


led.flashLED("blue",1)
print("%d: found neighbor"%(time.time()))


print(mesh.cli('neighbor table'))

print("Pymesh node role: %d"%mesh.state())

print("IPv6 unicast addresses: %s"%mesh.ipaddr())

print(mesh.cli('leaderdata'))

# print(mesh.cli('ping fe80:0:0:0:72b3:d549:95a2:c562 64 10 1'))
