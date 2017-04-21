#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw import Callback
from .logger import log

"""
callbacks
Created by otger on 23/03/17.
All rights reserved.
"""

# Values received on tc08.temperatures are like
# {'channel_0':{'ts_utc': ...,
#                'value': ...,
#                'units': ...,
#                'tc_type': ...},
#  'channel_1'....
#  }
#

# On temperature callback

class TemperaturesCallback(Callback):
    name = 'temperatures'
    description = "Receive temperatures and update values on control"
    version = "0.1"

    def functionality(self):

        # look for temperature value
        channel = 'channel_{}'.format(self.module.settings.t_control_tc08_chan)

        chan_values = getattr(self.event.value, channel, None)
        if chan_values is None:
            log.error("Received event temperatures without info of channel {}: {}".format(channel,
                                                                                          self.event.value))
            return
        temperature = getattr(chan_values, 'value', None)
        if temperature is None:
            log.error("Received event temperatures without value of temperature value: {}".format(self.event.value))
            return

        self.module.bc.temperature = temperature
        self.module.sm.update()


class ThermoCoolerCallback(Callback):
    name = 'voltage_current'
    description = "Receive VI calculated values for thermo cooler"
    version = "0.1"

    def functionality(self):

        # look for temperature value
        channel = 'channel_{}'.format(self.module.settings.t_control_tc08_chan)

        chan_values = getattr(self.event.value, channel, None)
        if chan_values is None:
            log.error("Received event temperatures without info of channel {}: {}".format(channel,
                                                                                          self.event.value))
            return
        temperature = getattr(chan_values, 'value', None)
        if temperature is None:
            log.error("Received event temperatures without value of temperature value: {}".format(self.event.value))
            return

        self.module.bc.temperature = temperature
        self.module.sm.update()
