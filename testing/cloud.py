#!/usr/bin/env python3
# -*- coding: utf-8 -*-

############################################################################
# Script Name: cloud.py
#
# Original Version: 15/04/2022 (by Hakan KAYAN)
# Updated Version: 25/12/2024 (by Charith PERERA)
#
# Description:
#   - Demonstrates dual-way communication with ThingsBoard via MQTT.
#   - Reads temperature and humidity from a Grove DHT sensor (connected to D4),
#     and publishes these to a ThingsBoard dashboard.
#   - Subscribes to RPC commands to control a Grove Buzzer (connected to D8).
#   - Illustrates how to exchange sensor data and commands in real-time.
#
# Parameters: Buzzer, Temp & Hum. Sensor
############################################################################

import os
import time
import paho.mqtt.client as mqtt
import json
import grovepi

# -----------------------------------------------------------------------------
# 1. ThingsBoard Configuration
# -----------------------------------------------------------------------------
# Replace 'thingsboard.cs.cf.ac.uk' if you're using a different server, 
# and update ACCESS_TOKEN with your unique token from ThingsBoard.
THINGSBOARD_HOST = 'thingsboard.cs.cf.ac.uk'
ACCESS_TOKEN = 'KV8ua9VXNu9cOQ8Op4DS'  # <== Insert your own access token here.

# -----------------------------------------------------------------------------
# 2. MQTT Callbacks and Setup
# -----------------------------------------------------------------------------
def on_publish(client, userdata, result):
    """
    Callback when data is successfully published to the MQTT broker.
    Prints 'Success' to confirm the publish event.
    """
    print("Success")

def on_message(client, userdata, msg):
    """
    Callback when an MQTT PUBLISH message is received on a subscribed topic.
    In this case, listens for RPC requests to set the buzzer state.
    """
    print('Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
    data = json.loads(msg.payload)

    # Check for method type to set the buzzer's ON/OFF state.
    if data['method'] == 'setValue':
        print(data['params'])
        buzzer_state['State'] = data['params']  # Update local buzzer state dict
        grovepi.digitalWrite(buzzer, data['params'])  # Physically update the buzzer pin

def on_connect(client, userdata, flags, rc, *extra_params):
    """
    Callback for when the client receives a CONNACK response from the server.
    'rc' is the connection result code. 0 indicates success.
    """
    print('Connected with result code ' + str(rc))

# -----------------------------------------------------------------------------
# 3. Sensor and Actuator Setup
# -----------------------------------------------------------------------------
# We assume a Grove Buzzer connected to D8 and a DHT sensor to D4.
buzzer = 8
grovepi.pinMode(buzzer, "OUTPUT")  # Ensure the buzzer pin is set as output

# The DHT sensor can be of type blue (0) or white (1). Adjust to your hardware.
sensor = 4  # DHT sensor on digital port D4
blue = 0    # Blue sensor type
white = 1   # White sensor type

# Store data and state in dictionaries for easy JSON serialization.
sensor_data = {'temperature': 0, 'humidity': 0}
buzzer_state = {'State': False}

# Publishing interval (seconds). A lower interval might stress the sensor or device.
INTERVAL = 3
next_reading = time.time()

# -----------------------------------------------------------------------------
# 4. MQTT Client Creation and Configuration
# -----------------------------------------------------------------------------
client = mqtt.Client()

# Provide the ThingsBoard access token for authentication
client.username_pw_set(ACCESS_TOKEN)

# Bind the callbacks
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message

# Connect to ThingsBoard on port 1883
# 60 seconds is the keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

# Subscribe to the RPC topic so we can control the buzzer from the dashboard
client.subscribe('v1/devices/me/rpc/request/+')

# Start the MQTT client networking loop
client.loop_start()

# -----------------------------------------------------------------------------
# 5. Main Data Collection Loop
# -----------------------------------------------------------------------------
try:
    while True:
        # Read temperature and humidity from DHT sensor
        [temp, humidity] = grovepi.dht(sensor, blue)

        # Short delay to ensure stable readings (especially for DHT sensors)
        time.sleep(3)
        print(u"Temperature: {:g}\u00b0C, Humidity: {:g}%".format(temp, humidity))

        # Prepare sensor data for telemetry
        sensor_data['temperature'] = temp
        sensor_data['humidity'] = humidity

        # Publish sensor data and buzzer state to ThingsBoard
        # - 'telemetry' is the default endpoint for sending data
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
        client.publish('v1/devices/me/telemetry', json.dumps(buzzer_state), 1)

        # Wait until the next interval before sending another reading
        next_reading += INTERVAL
        sleep_time = next_reading - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)

except KeyboardInterrupt:
    # If user presses Ctrl+C, gracefully stop the MQTT loop and disconnect
    client.loop_stop()
    client.disconnect()
    print("Terminated.")
    os._exit(0)
