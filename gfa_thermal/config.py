#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging


__author__ = 'otger'

SENSORS_LOOP_INTERVAL = 5

TTiCPX_IP = '172.16.17.55'
TTiCPX_PORT = 9221
TTiCPX_OUTPUT = 1

LAIRD_QC_DESIRED = 1

TEMPERATURE_CHANNEL_CONTROL = 1
TEMPERATURE_CHANNEL_TC_HOT = 2
TEMPERATURE_CHANNEL_TC_COLD = 3

CONTROL_COLD_THRESHOLD = 15  # Min temperature (Electro cooler will be switch off under this value)
CONTROL_HOT_THRESHOLD = 16  # Max temperature (Electro cooler will be switched on above this value)

TC08_CHAN_0 = {'enable': False,
               'units': "Centigrade",  # valid values: 'Centigrade', 'Fahrenheit', 'Kelvin', 'Rankine'
               'tc_type': "T",  # valid values: 'B', 'E', 'J', 'K', 'N', 'R', 'S', 'T'
               }
TC08_CHAN_1 = {'enable': True,
               'units': "Centigrade",  # valid values: 'Centigrade', 'Fahrenheit', 'Kelvin', 'Rankine'
               'tc_type': "T",  # valid values: 'B', 'E', 'J', 'K', 'N', 'R', 'S', 'T'
               }
TC08_CHAN_2 = {'enable': True,
               'units': "Centigrade",  # valid values: 'Centigrade', 'Fahrenheit', 'Kelvin', 'Rankine'
               'tc_type': "T",  # valid values: 'B', 'E', 'J', 'K', 'N', 'R', 'S', 'T'
               }
TC08_CHAN_3 = {'enable': True,
               'units': "Centigrade",  # valid values: 'Centigrade', 'Fahrenheit', 'Kelvin', 'Rankine'
               'tc_type': "T",  # valid values: 'B', 'E', 'J', 'K', 'N', 'R', 'S', 'T'
               }
TC08_CHAN_4 = {'enable': False,
               'units': "Centigrade",  # valid values: 'Centigrade', 'Fahrenheit', 'Kelvin', 'Rankine'
               'tc_type': "T",  # valid values: 'B', 'E', 'J', 'K', 'N', 'R', 'S', 'T'
               }
TC08_CHAN_5 = {'enable': False,
               'units': "Centigrade",  # valid values: 'Centigrade', 'Fahrenheit', 'Kelvin', 'Rankine'
               'tc_type': "T",  # valid values: 'B', 'E', 'J', 'K', 'N', 'R', 'S', 'T'
               }
TC08_CHAN_6 = {'enable': False,
               'units': "Centigrade",  # valid values: 'Centigrade', 'Fahrenheit', 'Kelvin', 'Rankine'
               'tc_type': "T",  # valid values: 'B', 'E', 'J', 'K', 'N', 'R', 'S', 'T'
               }
TC08_CHAN_7 = {'enable': False,
               'units': "Centigrade",  # valid values: 'Centigrade', 'Fahrenheit', 'Kelvin', 'Rankine'
               'tc_type': "T",  # valid values: 'B', 'E', 'J', 'K', 'N', 'R', 'S', 'T'
               }
TC08_CHAN_8 = {'enable': False,
               'units': "Centigrade",  # valid values: 'Centigrade', 'Fahrenheit', 'Kelvin', 'Rankine'
               'tc_type': "T",  # valid values: 'B', 'E', 'J', 'K', 'N', 'R', 'S', 'T'
               }



STREAM_LOG = True  # Outputs logs to screen
STREAM_LOG_LEVEL = logging.INFO

FILE_LOG = True
FILE_LOG_PATH = '/tmp/gfa_thermal.log'
FILE_LOG_MAX_SIZE = 5*1024*1024
FILE_LOG_BACKUP = 3
FILE_LOG_LEVEL = logging.DEBUG