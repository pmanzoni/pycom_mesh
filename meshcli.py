from network import LoRa
import sys
import time

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

while True:
    otcmd = input("cli: ")
    otcmd = otcmd+"\n"
    print(mesh.cli(otcmd))


