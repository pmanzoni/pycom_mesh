from network import LoRa

lora = LoRa(mode=LoRa.LORA)
pymesh = lora.Mesh()
pymesh.state()

while True:
	otcmd = input("cli: ")
	otcmd = otcmd+"\n"
	print(pymesh.cli(otcmd))


