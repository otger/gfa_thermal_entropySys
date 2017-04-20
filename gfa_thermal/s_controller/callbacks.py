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


class TemperaturesCallback(Callback):
    name = 'temperatures'
    description = "Receive temperatures and update values on control"
    version = "0.1"

    def functionality(self):

        temperature = getattr(self.event.value, 'output', None)

        try:
            self.module.enable_output(output_1=(output == 1), output_2=(output == 2))
            self.module.pub_status(output)
        except:
            log.exception('Exception on enable output callback')

