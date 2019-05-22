from network import LoRa

lora = LoRa(mode=LoRa.LORA)
pymesh = lora.Mesh()
pymesh.state()

while True:
	otcmd = input("cli: ")
	print(pymesh.cli(otcmd))


