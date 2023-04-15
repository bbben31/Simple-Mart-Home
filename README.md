# Simple-Mart-Home

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
