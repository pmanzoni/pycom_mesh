# Pymesh micropython code

This repository cointains examples of the use of Pycom's proprietary LoRa Mesh network (**Pymesh**).

* [Official Pymesh docs](https://docs.pycom.io/firmwareapi/pycom/network/lora/pymesh.html)
* [Forum Pymesh announcements](https://forum.pycom.io/topic/4449/pymesh-updates)
* [a simple example](https://docs.pycom.io/tutorials/lora/lora-mesh.html)
* [a more complete example](https://github.com/pycom/pycom-libraries/tree/master/lib/pymesh)

The scripts included in this repository were created and tested using a [Lopy4](https://pycom.io/product/lopy4/), using the firmware release [**1.20.0.rc11**].

## Mesh basics
The Pymesh LoRa Mesh is implemented using [OpenThread](https://openthread.io/guides/thread-primer).

To understand the OpenThread terms and overall functionality, these guides are highly recommended:

* [What is Thread?](https://openthread.io/guides/thread-primer)
* [Node Roles and Types](https://openthread.io/guides/thread-primer/node-roles-and-types)
* [IPv6 Addressing](https://openthread.io/guides/thread-primer/ipv6-addressing) (especially, RLOC unicast address)

## A simple CLI:

**File: `"meshcli.py"`**

This extremely simple file allows to manually test the [OpenThread CLI](https://github.com/openthread/openthread/blob/c482301ec73b80985445102e4d0a936346172ddb/src/cli/README.md)

This example https://codelabs.developers.google.com/codelabs/openthread-simulation/#2 can be replicated.

Notes:
* 'panid' seems that cannot be changed. It is fixed to '1234'
