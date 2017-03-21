# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
from .cul import CUL


class CULMQTT(object):
    
    def __init__(self, cul_port, mqtt_broker, mqtt_client_id="cul", mqtt_topic="cul"):
        super(CULMQTT, self).__init__()
        self._cul_port = cul_port
        self._mqtt_broker = mqtt_broker
        self._mqtt_client_id = mqtt_client_id
        self._mqtt_topic = mqtt_topic
        self._run = False
        
    def on_mqtt_recv(self, client, data, msg):
        mqtt_msg = str(msg.payload)
        self._cul.send(mqtt_msg)
        
    def start(self):
        self._run = True
        # configure CUL
        self._cul = CUL(self._cul_port)
        self._cul.send("X01")
        # set up MQTT client
        self._client = paho.Client(client_id=self._mqtt_client_id)
        self._client.on_message = self.on_mqtt_recv
        self._client.connect(self._mqtt_broker, 1883)
        self._client.subscribe(self._mqtt_topic + "/send")
        self._client.loop_start()
        # handler incoming RF transmission
        while self._run:
            rf_msg = self._cul.read()
            if rf_msg:
                rf_msg = rf_msg.decode("ascii").strip()
                self._client.publish(self._mqtt_topic + "/recv", rf_msg)
            time.sleep(0.05)

