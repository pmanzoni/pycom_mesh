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

def issingleton(mesh):
    if "true" in mesh.cli('singleton'):
        return True
    else:
        return False


# init...

## disabling WiFi
wlan = WLAN()
wlan.deinit()

## setting LED
pycom.heartbeat(False)
led = pyLED()


print("enabling Lora...")
lora_active = False
while not lora_active:
    try:
        lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
        lora_active = True
    except Exception as e:
        print("DISASTER! exception opening Lora: "+str(e))
        time.sleep(2)

print("enabling Pymesh...")
try:
    mesh = lora.Mesh()
except Exception as e:
    print("DISASTER! exception creating mesh: "+str(e))
    sys.exit()

time.sleep(2)

cstate = mesh.state()
while (cstate<2):       # exits when either "PYMESH_ROLE_CHILD", "PYMESH_ROLE_ROUTER" or "PYMESH_ROLE_LEADER"
    print("%d: looping... [%s]"%(time.time(), PYMESHSTATE[cstate]))
    time.sleep(2)
    cstate = mesh.state()

led.flashLED("green")
cstate = mesh.state()
print("%d: current state [%s]"%(time.time(), PYMESHSTATE[cstate]))

while issingleton(mesh):
    cstate = mesh.state()
    print("%d: waiting for neighbors [%s]"%(time.time(), PYMESHSTATE[cstate]))
    led.flashLED("red", 1)
    time.sleep(2)


led.flashLED("blue", 1)
print("%d: found neighbor"%(time.time()))
print(mesh.cli('neighbor table'))

print("IPv6 unicast addresses: %s"%mesh.ipaddr())

print("Leader data:")
print(mesh.cli('leaderdata'))

# print(mesh.cli('ping fe80:0:0:0:72b3:d549:95a2:c562 64 10 1'))
