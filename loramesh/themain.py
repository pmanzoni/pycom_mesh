#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#
# Modified by PM, May 2019

from network import LoRa
import socket
import time
import utime
import ubinascii
import pycom
import machine

from lorameshlib import Loramesh

PYMESHSTATE = ["PYMESH_ROLE_DISABLED", "PYMESH_ROLE_DETACHED", "PYMESH_ROLE_CHILD", "PYMESH_ROLE_ROUTER", "PYMESH_ROLE_LEADER"]

# handler responsible for receiving packets on UDP Pymesh socket
def receive_pack():
    print("ENTERING UDP HANDLER")
    # listen for incomming packets
    while True:
        rcv_data, rcv_addr = s.recvfrom(128)
        if len(rcv_data) == 0:
            break
        rcv_ip = rcv_addr[0]
        rcv_port = rcv_addr[1]
        print('Incomming %d bytes from %s (port %d)'%(len(rcv_data), rcv_ip, rcv_port))
        print(rcv_data)
        # could send some ACK pack:
        if rcv_data.startswith("Hello"):
            try:
                s.sendto('ACK ' + MAC + ' ' + str(rcv_data)[2:-1], (rcv_ip, rcv_port))
            except Exception:
                pass
        mesh.blink(7, .3)



pycom.wifi_on_boot(False)
pycom.heartbeat(False)

print("enabling Lora...")
lora_active = False
while not lora_active:
    try:
        lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_125KHZ, sf=7)
        lora_active = True
    except Exception as e:
        print("DISASTER! exception opening Lora: "+str(e))
        time.sleep(2)
MAC = str(ubinascii.hexlify(lora.mac()))[2:-1]
print("LoRa MAC: %s"%MAC)

mesh = Loramesh(lora)


# waiting until it is connected to Mesh network
cstate = mesh._state_update()
while (cstate<2):       # exits when either "PYMESH_ROLE_CHILD", "PYMESH_ROLE_ROUTER" or "PYMESH_ROLE_LEADER"
    mesh.led_state()
    print("%d: looping... [%s]"%(time.time(), PYMESHSTATE[cstate]))
    time.sleep(2)
    cstate = mesh._state_update()


print('Neighbors found: %s'%mesh.neighbors())

# create UDP socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
myport = 1234
s.bind(myport)

pack_num = 1
msg = "Hello World! MAC: " + MAC + ", pack: "
ip = mesh.ip()
mesh.mesh.rx_cb(receive_pack, s)

# infinite main loop
while True:
    mesh.led_state()
    print("%d: state: %s, is singleton: %s, IP: %s"%(time.time(), mesh.cli('state'), mesh.cli('singleton'), mesh.ip()))

    # check if topology changes, maybe RLOC IPv6 changed
    new_ip = mesh.ip()
    if ip != new_ip:
        print("IP changed from: %s to %s"%(ip, new_ip))
        ip = new_ip

    # update neighbors list
    neigbors = mesh.neighbors_ip()
    print("%d neighbors, IPv6 list: %s"%(len(neigbors), neigbors))

    # send PING and UDP packets to all neighbors
    for neighbor in neigbors:
        if mesh.ping(neighbor) > 0:
            print('Ping OK from neighbor %s'%neighbor)
            mesh.blink(10, .1)
        else:
            print('Ping not received from neighbor %s'%neighbor)

        time.sleep(10)

        pack_num = pack_num + 1
        try:
            s.sendto(msg + str(pack_num), (neighbor, myport))
            print('Sent message to %s'%(neighbor))
        except Exception:
            pass
        time.sleep(20 + machine.rng()%20)

    # random sleep time
    time.sleep(30 + machine.rng()%30)
