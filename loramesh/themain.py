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

UDPPORT = 1234
PYMESHSTATE = ["PYMESH_ROLE_DISABLED", "PYMESH_ROLE_DETACHED", "PYMESH_ROLE_CHILD", "PYMESH_ROLE_ROUTER", "PYMESH_ROLE_LEADER"]

# Handler responsible for receiving packets on UDP Pymesh socket
def receive_pack(s):
    global device_lora_mac

    rcv_data, rcv_addr = s.recvfrom(128)
    if len(rcv_data) > 0:
        rcv_ip   = rcv_addr[0]
        rcv_port = rcv_addr[1]
        print('received %d bytes from %s (port %d)' % (len(rcv_data), rcv_ip, rcv_port))
        print("\t> %s" % rcv_data)

        # Sends an ACK packet if it was an "Hello" packet
        if rcv_data.startswith("Hello"):
            try:
                s.sendto('ACK ' + device_lora_mac + ' ' + str(rcv_data)[2:-1], (rcv_ip, rcv_port))
            except Exception as e:
                print("inside 'receive_pack()': %s" % str(e))
                pass
        mesh.blink(7, .3)


########################################

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
device_lora_mac = str(ubinascii.hexlify(lora.mac()))[2:-1]
print("LoRa MAC: %s"%device_lora_mac)

mesh = Loramesh(lora)

# waiting until it is connected to Mesh network
cstate = mesh._state_update()
while (cstate<2):       # exits when either "PYMESH_ROLE_CHILD", "PYMESH_ROLE_ROUTER" or "PYMESH_ROLE_LEADER"
    mesh.led_state()
    print("%d: waiting... [%s]"%(time.time(), PYMESHSTATE[cstate]))
    time.sleep(2)
    cstate = mesh._state_update()

print('Current status: %s'  % PYMESHSTATE[cstate])

node_ip_addr = mesh.ip()

# create UDP socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.bind(UDPPORT)
mesh.mesh.rx_cb(receive_pack, s)


# Main loop
pack_num = 0
while True:
    mesh.led_state()
    c_state = mesh.cli('state')
    if "true" in mesh.cli('singleton'):
        single = "is singleton"
    else:
        single = "not singleton"
    print("%d: state: %s, IP: %s [%s]" % (time.time(), c_state, node_ip_addr, single))

    # check if topology changes, maybe RLOC IPv6 changed
    new_node_ip_addr = mesh.ip()
    if node_ip_addr != new_node_ip_addr:
        print("IP changed from: %s to %s"%(node_ip_addr, new_node_ip_addr))
        node_ip_addr = new_node_ip_addr

    # update neighbors list
    neigbors = mesh.neighbors_ip()
    print("%d: %d neighbors, IPv6 list: %s" % (time.time(),len(neigbors), neigbors))

    # send PING and UDP packets to all neighbors
    for neighbor in neigbors:

        try:
            tping = mesh.ping(neighbor)
            if tping > 0:
                print('Ping OK from neighbor %s'%neighbor)
                mesh.blink(10, .1)
            else:
                print('Ping not received from neighbor %s'%neighbor)
        except Exception as e:
            print("exception doing PING: "+str(e))
            pass

        time.sleep(5)

        pack_num = pack_num + 1
        try:
            s.sendto("Hello World! from node: " + device_lora_mac + ", pack: " + str(pack_num), (neighbor, UDPPORT))
            print('Sent message to %s' % (neighbor))
        except Exception as e:
            print("exception sending packet: "+str(e))
            pass
        time.sleep(5 + machine.rng()%10)

    # random sleep time
    time.sleep(5 + machine.rng()%10)
