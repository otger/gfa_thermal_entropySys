#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw import Callback
from .logger import log

"""
callbacks
Created by otger on 23/03/17.
All rights reserved.
"""

# Values received on tc08.temperatures were like
# {'channel_0':{'ts_utc': ...,
#                'value': ...,
#                'units': ...,
#                'tc_type': ...},
#  'channel_1'....
#  }
# Now they are like: {'channel_0':315.9, 'channel_1':276.87,...}

# On temperature callback


class TemperaturesCallback(Callback):
    name = 'temperatures'
    description = "Receive temperatures and update values on control"
    version = "0.1"

    def functionality(self):

        # look for temperature value
        channel = 'channel_{}'.format(self.module.settings.t_control_tc08_chan)

        chan_value = self.event.value.get(channel, None)
        if chan_value is None:
            log.error("Received event temperatures without info of channel {}: {}".format(channel,
                                                                                          self.event.value))
            return

        self.module.bc.temperature = chan_value
        # Every time a temperatures updates i sent, electro cooler calculator will generate a thermo cooler callback, no need to do it twice
        # self.module.sm.update()


class ThermoCoolerCallback(Callback):
    name = 'voltage_current'
    description = "Receive VI calculated values for thermo cooler"
    version = "0.1"

    def functionality(self):
        voltage = self.event.value.get('voltage')
        current = self.event.value.get('current')
        try:
            voltage = float(voltage)
            current = float(current)
        except:
            log.exception("Bad values on thermo cooler callback. Event values: {}".format(self.event.values))
            raise
        self.module.bc.voltage = voltage
        self.module.bc.current = current
        self.module.sm.update()
