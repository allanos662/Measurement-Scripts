#! /usr/bin/python3
import serial
import time

class ard(serial.Serial):
    def __init__(self, arduino_address, tout):
        serial.Serial.__init__(self, arduino_address, timeout = tout)

    def switch(self, vdp_switch):
        self.write(bytes(str(vdp_switch), 'utf-8'))
        return self.readline()
