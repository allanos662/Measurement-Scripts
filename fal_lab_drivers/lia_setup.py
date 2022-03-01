#! /usr/bin/python3
def setup_lia(lia, lia_params) :
    lia.time_constant = lia_params['TAU']
    lia.sensitivity = lia_params['SENSITVITY']
    lia.frequency = lia_params['FREQUENCY']
    lia.amplitude = lia_params['AMP']
    lia.input_coupling = lia_params['COUPLING']
    lia.filter_slope = lia_params['LP_FILTER']
    lia.sync_filter = lia_params['SYNC_FILTER']
    lia.notch_filter = lia_params['NOTCH_FILTER']


