




# PWM Signal Generation for Stepper Motor Control
from machine import Pin
from utime import sleep

ena = Pin(16, Pin.OUT)         # Pin Enable
dir = Pin(15, Pin.OUT)         # Pin Drehrichtung 
pul = Pin(14, Pin.OUT)         # Pin PWM Signal

while True:
    ena.value(1)                                 # Enable the stepper motor driver
    dir.value(1)                                 # Set direction to clockwise
    for i in range(200):                         # Generate 200 pulses
        pul.value(1)                             # Set pulse high
        sleep(0.001)                             # Wait for 1 ms
        pul.value(0)                             # Set pulse low
        sleep(0.001)                             # Wait for 1 ms

    sleep(1)                                     # Wait for 1 second before changing direction

    dir.value(0)                                 # Set direction to counter-clockwise
    for i in range(200):                         # Generate 200 pulses
        pul.value(1)                             # Set pulse high
        sleep(0.001)                             # Wait for 1 ms
        pul.value(0)                             # Set pulse low
        sleep(0.001)                             # Wait for 1 ms

    sleep(1)                                     # Wait for 1 second before repeating the loop