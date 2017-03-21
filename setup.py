#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from distutils.core import setup
from culmqtt import __version__ as ver


setup(name="culmqtt",
      version=ver,
      description="CUL to MQTT bridge.",
      author="Sven Festersen",
      author_email="sven@sven-festersen.de",
      packages=["culmqtt"],
      requires=["paho.mqtt"],
      scripts=["cli/cul-mqtt"]
     )
