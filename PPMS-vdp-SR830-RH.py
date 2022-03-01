#! /usr/bin/python3
import qcodes as qc
import numpy as np
from qcodes.instrument_drivers.QuantumDesign.DynaCoolPPMS.DynaCool import DynaCool
from time import sleep
from qcodes.instrument_drivers.stanford_research.SR830 import SR830
from PPMS-codes import ard
from PPMS-codes import setup_lia
import yaml
import datetime as dt

#connect to vdp arduino switch
with open('temp_sweep.yaml', 'r') as f:
    params = yaml.load(f, Loader=yaml.FullLoader)

vanderpaw = ard('COM4', 0.1)
time.sleep(5) #delay to open arduino
date = dt.datetimee.now()

#configure data file
data_file = open(params['DATA_FILE']+'\n', 'w')

data_file.write(params['SAMPLE']+'\n')
data_file.write(f'{date.year}-{date.month}-{date.day}')

data_file.write('LOCK-IN PARAMETERS'+'\n')
for key in params['LIA']: #record LIA parameters in datafile
    data_file.write(key+': 'str(params['LIA'][key])+'\n')

data_file.write('T_PPMS(K)\t H_PPMS(Oe)\tVDP_config\tLIA_X(V)\tLIA_Y(V)\tLIA_PHASE\n')

#connect to dynacool, lock in, set vdp configs
dynacool = DynaCool('dynacool', address="TCPIP0::127.0.0.1::5000::SOCKET")

sr = SR830('lockin', 'GPIB0::'+str(params['LIA']['ADDRESS'])+'::INSTR')
setup_lia(sr, params['LIA'])

active_switches = params['VDP'] #desired vdp configuration

#Pre-Measurement
print('Measurment Parameters':)
print(params)
while(1):
    #print settings
    go = input('ready to measure[y/n]? : ')
    if go == 'y':
        break
    if go == 'n':
        quit()    

dynacool.temperature_rate(params['QUICK_RAMP_TEMP'])
dynacool.temperature_setpoint(params['T_START'])

dynacool.field_rate(params['QUICK_RAMP_FIELD'])
dynacool.field_ramp(params['H_START'])
print("ramping to starting temperature and field setpoints...")

while dynacool.temperature_state() != 'settled' or dynacool.magnet_state() != 'settled'
    continue

print(f"holding for additional settling time: {params['SETTLE']} mins")
time.sleep(params['SETTLE'])

#Measurment Loop
#begin ramp command
dynacool.field_rate(params['H_RAMP_MEASURE'])
dynacool.field_ramp(params['H_FINAL'])

#print(f'ramping to {params[T_FINAL]} at {params[SWEEP_RATE]}K/min')
while dynacool.magnet_state() == 'chasing':
    for config in active_switches:
        vanderpauw.switch(config) #changes the vanderpaw config 
        time.sleep(params['DELAY']) #waits for set delay before recording
        temp = dynacool.temperature() #gets Temp
        H = dynacool.field_measured() #gets field

        timenow = dt.datetime.now() #gets time
        values = sr.snap('x', 'y', 'phase') #measured values from LIA

        data_file.write(f'{timenow.hour}:{timenow.minute}:{timenow.second}\t{temp}\t{H}\t{config}\t{values[0]}\t{values[1]}\t{values[2]}\n')
