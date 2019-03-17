# -*- coding: utf-8 -*-
import logging
import paho.mqtt.client as paho
import time
from .cul import CUL


class CULMQTT(object):
    
    def __init__(self, cul_port, mqtt_broker, mqtt_client_id="cul",
                 mqtt_topic="cul", delay_send=0.05, log_level=logging.ERROR):
        super(CULMQTT, self).__init__()
        self._cul_port = cul_port
        self._mqtt_broker = mqtt_broker
        self._mqtt_client_id = mqtt_client_id
        self._mqtt_topic = mqtt_topic
        self._delay_send = delay_send
        self._log_level = log_level
        self._send_queue = []
        self._run = False
        self._logger = logging.getLogger("cul-mqqt.MQTT")
        self._logger.setLevel(log_level)
        
    def on_mqtt_recv(self, client, data, msg):
        mqtt_msg = msg.payload
        self._send_queue.append(mqtt_msg)
        self._logger.debug("Queued received message: {0}.".format(mqtt_msg))
        self._logger.debug("Queue length: {0}.".format(len(self._send_queue)))
        
    def on_mqtt_connect(self, client, data, flags, rc):
        if rc == 0:
            self.client.subscribe(self._mqtt_topic + "/send")
        
    def start(self):
        self._run = True
        # configure CUL
        self._cul = CUL(self._cul_port, log_level=self._log_level)
        self._cul.send("X01")
        # set up MQTT client
        self._client = paho.Client(client_id=self._mqtt_client_id)
        self._client.on_message = self.on_mqtt_recv
        self._client.on_connect = self.on_mqtt_connect
        self._client.connect(self._mqtt_broker, 1883)
        self._client.loop_start()
        self._logger.info("MQTT transport configured.")
        self._logger.debug("Broker is '{0}'.".format(self._mqtt_broker))
        self._logger.debug("Client id is '{0}'.".format(self._mqtt_client_id))
        self._logger.debug("Listening for messages with topic '{0}/send'.".format(self._mqtt_topic))
        self._logger.debug("Incoming messages will be published to '{0}/recv'.".format(self._mqtt_topic))
        # handle incoming RF transmission
        while self._run:
            time.sleep(0.05)
            rf_msg = self._cul.recv()
            if rf_msg:
                rf_msg = rf_msg.decode("ascii").strip()
                self._client.publish(self._mqtt_topic + "/recv", rf_msg)
                self._logger.debug("Published message: {0}.".format(rf_msg))
                continue
            # send a message from the send queue
            if self._send_queue:
                mqtt_msg = self._send_queue.pop(0)
                self._cul.send(mqtt_msg)
                self._logger.debug("Queue length: {0}.".format(len(self._send_queue)))
                time.sleep(self._delay_send)

