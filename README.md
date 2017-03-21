# cul-mqtt
Connect a CUL device running *culfw* (http://culfw.de) via MQTT (http://mqtt.org/). Reqiures Python 3 and paho-mqtt.
Intended for use with openhab. Tested on Linux and with openhab2.

## Installation
Use the setup script to install:

    python setup.py install
  
  
## Usage
The setup script installs the `cul-mqtt` command line program. Usage:

    cul-mqtt --device <serial_device> --broker <mqtt_broker> --clientid <mqtt_client_id> --topic <mqtt_topic>
    
All paramters are optional.
Example:

    cul-mqtt --device /dev/ttyUSB0 --broker localhost
    
The default client id ist "cul", the default topic "cul". Received RF messages will be published with topic `<mqtt_topic>/recv`.
The program listens to MQTT messages with topic `<mqtt_topic>/send`. All data received this way will be sent to the CUL.

**Important**: messages are not interpreted or preprocessed in any way by `cul-mqtt`.
This has be done separately, e.g. in an openhab rule.

## TODO
 * add logging
 * implement authentication
 * implement TLS
