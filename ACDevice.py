
import json
import paho.mqtt.client as mqtt

# TOPICS USED TO SUBSCRIBE AND PUBLISH THE DATA

REGISTER_STATUS = "device/register/response/"  
AC_DEVICES = "device/ac/"  
REGISTER_DEVICE = "device/register"  
DEVICE_REGISTER_MSG = "device/register_status"  
DEVICE_STATUS = "device/status" 

HOST = "localhost"
PORT = 1883

# AC_DEVICE class will take the commands from the edge server to perform various operation
# This includes registration, status and controlling the devices 

class AC_Device():
    
    _MIN_TEMP = 18  
    _MAX_TEMP = 32  

    def __init__(self, device_id, room):
        
        # Setting up the device related information, while creating the object
        self._device_id = device_id
        self._room_type = room
        self._temperature = 22
        self._device_type = "AC"
        self._device_registration_flag = False
        self._switch_status = "OFF"
        self._DEVICE_ID_TOPIC = "device/" + self._device_id + "/"
        self._ROOM_TOPIC = "device/" + self._room_type + "/"
        # Calling the MQTT client to enable the required methods 
        self.client = mqtt.Client(self._device_id)  
        self.client.on_connect = self._on_connect  
        self.client.on_message = self._on_message  
        self.client.connect(HOST, PORT, keepalive=60)  
        self.client.loop_start()  
        # Method to perform the regitration while creating the ACDevice object
        self._register_device(self._device_id, self._room_type, self._device_type)
        
    # Method to register the device on the server
    def _register_device(self, device_id, room_type, device_type):
        
        while not self.client.is_connected():
            pass
        ac_device = dict()
        ac_device['device_id'] = device_id
        ac_device['room'] = room_type
        ac_device['type'] = device_type
        
        self.client.publish(REGISTER_DEVICE, json.dumps(ac_device))

    # Subscribing to the topics such as
    # indvidual devices, rooms and dvice_types
    def _on_connect(self, client, userdata, flags, result_code):
        
        if result_code == 0:
            
            while not self.client.is_connected():
                pass
            self.client.subscribe(REGISTER_STATUS + self._device_id)
            self.client.subscribe(self._DEVICE_ID_TOPIC)  
            self.client.subscribe(self._ROOM_TOPIC)   
            self.client.subscribe(AC_DEVICES) 
        else:
            print("Bad connection for {0} instance {1} with result code : {2}".format(self._device_type, self._device_id, str(result_code)))
            if result_code == 4:
                print("MQTT server is unavailable.")

    # performing various operation based on the received request from the server
    # This method will internally call get and set method to get the status and controll the values respectively.
    # this method will also show the register status for each device request received.

    def _on_message(self, client, userdata, msg):            
        received_message = (msg.payload.decode("utf-8")).split(',')
        # Publishing registration status 

        if msg.topic == (REGISTER_STATUS + self._device_id):
            self._device_registration_flag = True
            ac_device_register = dict()
            ac_device_register['device_id'] = self._device_id
            ac_device_register['registered_status'] = self._device_registration_flag
            ac_device_register['msg'] = "AC-DEVICE Registered!"
            self.client.publish(DEVICE_REGISTER_MSG, json.dumps(ac_device_register))

        # Performing get or control operation based on the request received for direct device_id, device_type, or room_type      
        elif msg.topic in [self._DEVICE_ID_TOPIC, AC_DEVICES, self._ROOM_TOPIC]:
            if received_message[0] == 'get':
                # Status will be published at the end for set type message as well
                pass
            elif received_message[0] in ("ON", "OFF"):
                self._set_switch_status(received_message[0])
            elif type(received_message[0] == int):
                if self._switch_status != 'ON':
                    self._set_switch_status("ON")
                self._set_temperature(received_message[0])        
        
            # Creating the payload to publish the status of the devices.
            ac_device_state = dict()
            ac_device_state['device_id'] = self._device_id
            ac_device_state['switch_state'] = self._get_switch_status()
            ac_device_state['temperature'] = self._get_temperature()
            self.client.publish(DEVICE_STATUS, json.dumps(ac_device_state))

    # Current switch status
    def _get_switch_status(self):
        return self._switch_status

    # Setting the switch based on the request
    def _set_switch_status(self, switch_state):
        self._switch_status = switch_state

    # Getting the temperature of the AC devices
    def _get_temperature(self):
        return self._temperature
    
    # Setting the temperature of the AC devices based on the request
    def _set_temperature(self, temperature):    
        if temperature.isnumeric() and (self._MIN_TEMP <= int(temperature) <= self._MAX_TEMP):
            self._temperature = int(temperature)

        elif (temperature.isalpha()):
            pass
        else:
            print("\nTemperature Change FAILED. Invalid temperature value received")    
