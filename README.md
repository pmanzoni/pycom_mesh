# Pymesh micropython code

This repository cointains examples of the use of Pycom's proprietary LoRa Mesh network (**Pymesh**).

* [Official Pymesh docs](https://docs.pycom.io/firmwareapi/pycom/network/lora/pymesh.html)
* [Forum Pymesh announcements](https://forum.pycom.io/topic/4449/pymesh-updates)

* [a simple Pymesh example](https://docs.pycom.io/tutorials/lora/lora-mesh.html)
* [a more complete example](https://github.com/pycom/pycom-libraries/tree/master/lib/pymesh)

The scripts included in this repository were created and tested using a [Lopy4](https://pycom.io/product/lopy4/), using the firmware release [**1.20.0.rc11**].

## Mesh basics
The Pymesh LoRa Mesh is implemented using [OpenThread](https://openthread.io/guides/thread-primer).

To understand the OpenThread terms and overall functionality, these guides are highly recommended:

* [What is Thread?](https://openthread.io/guides/thread-primer)
* [Node Roles and Types](https://openthread.io/guides/thread-primer/node-roles-and-types)
* [IPv6 Addressing](https://openthread.io/guides/thread-primer/ipv6-addressing) (especially, RLOC unicast address)

## A simple CLI:

