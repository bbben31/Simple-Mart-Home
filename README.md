# Simple-Smart-Home

We'll design and implement a simple Smart Home setup. The main focus is on
improving the designed communication channels and payloads over MQTT, and storage data
structures on the edge server.

Imagine a home with multiple defined 'rooms' and a common edge server/router which can
bidirectionally interact with each of the devices using an MQTT server running on the edge
server. Each device can push to, and listen on, various topics on the MQTT server.

The underlying communication layer can be WiFi, bluetooth, etc. We obviously don't have to
worry about that in this particular project, as you'll be running (simulating) all of them on your
local machine. The edge server might also receive commands from consumers (you on your
mobile app) which we’ll simulate here by calling methods on the server from a main.py driver
file. 

Please also assume that every component is trustworthy so there is no expectation of any
authentication or access control.


1. main.py
2. EdgeServer.py
3. LightDevice.py
4. ACDevide.py

Here are the basic functionality of each of these python files: 

	1. main.py is working as a driver code that does the following: 
		a. Intitalize the instance of edgeserver
		b. Intialize each types of devices and all the devices as per the requiremnt. 
		c. Perform the get and set operation on the devices by sending the command to the server. 

	2. EdgeServer.py is the interface between the user and the devices. It will perform  the following tasks: 
		a. The file have necessary topics that will be subscribed to publish and subscribe to the topics. 
		b. Creating the MQTT client to perform the provided commands.
		c. Get and set method to publish the message over different topics based on device_id/device_type/room_type 
		d. Perorm disconnect operation after completion of tasks. 
	3. ACDevice.py and LightDevice.py will do the following tasks:
		a. The file have necessary topics that will be subscribed to publish and subscribe to the topics. 
		b. Constructor will connect with MQTT client and assign coonstant values to the devices at the start. This includes setting default intensity status and default temeperature for relevant devices. 
		c. Perform get and set operation on the devices based on the request received in _on_message() method. 

In order to execute the files and test the cases, please run main.py from the terminal or relevant IDE. 


