#! /usr/bin/python3
import serial
import time

def setup_lia(lia, lia_params) :
    lia.time_constant = lia_params['TAU']
    lia.sensitivity = lia_params['SENSITVITY']
    lia.frequency = lia_params['FREQUENCY']
    lia.amplitude = lia_params['AMP']
    lia.input_coupling = lia_params['COUPLING']
    lia.filter_slope = lia_params['LP_FILTER']
    lia.sync_filter = lia_params['SYNC_FILTER']
    lia.notch_filter = lia_params['NOTCH_FILTER']


class ard(serial.Serial):
    def __init__(self, arduino_address, tout):
        serial.Serial.__init__(self, arduino_address, timeout = tout)

    def switch(self, vdp_switch):
        self.write(bytes(str(vdp_switch), 'utf-8'))
        return self.readline()

vdp = ard('/dev/cu.usbmodem143301', 0.1)
time.sleep(2) #time for arduino to start up
response = vdp.switch(2)
print(response)
