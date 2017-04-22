#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
from entropyfw import Module
from entropyfw.common import get_utc_ts
from .state_machine import StateMachine, StateRequests

from .actions import StartTempLoop, EnableChannel, StopTempLoop
# from .web.api.resources import get_api_resources
# from .web.blueprints import get_blueprint
from gfa_thermal.system_names import *
from .callbacks import ThermoCoolerCallback, TemperaturesCallback

from gfa_thermal import config
"""
module
Created by otger on 23/03/17.
All rights reserved.
"""


class EntropyController(Module):
    name = 'gfa_thermal'
    description = "GFA Thermal tests controller"

    def __init__(self, name=None):
        Module.__init__(self, name=name)
        self.settings = Settings()
        self.func = Functionality(parent=self)
        self.bc = BoundaryConditions()
        self.sm = StateMachine(functionality=self.func, settings=self.settings,
                               boundary_conditions=self.bc)

    def start_cooling(self):
        self.sm.start_cooling()

    def stop_cooling(self):
        self.sm.stop_cooling()

    def set_thresholds(self, t_cold, t_hot):
        self.settings.cold_threshold = t_cold
        self.settings.hot_threshold = t_hot
        self.sm.update()

    def set_channels(self, control_temp, thermo_cooler_cold, thermo_cooler_hot):
        """
        This method sets which TC08 channels have to be used for each one of the temperatures
        :param control_temp: TC08 channel of temperature to be used as control
        :param thermo_cooler_cold: TC08 channel of the thermocouple placed at cold side of thermo cooler
        :param thermo_cooler_hot: TC08 channel of the thermocouple placed at hot side of thermo cooler
        :return:
        """
        pass

    def register_electrocooler_calc(self, event_name):
        self.register_callback(ThermoCoolerCallback, pattern=event_name)

    def register_temperatures_callback(self, event_name, temp_control_channel, hot_threshold, cold_threshold):
        self.settings.t_control_tc08_chan = temp_control_channel
        self.settings.cold_threshold = cold_threshold
        self.settings.hot_threshold = hot_threshold
        self.register_callback(TemperaturesCallback, pattern=event_name)

class Functionality(object):
    """Functionality for module state machine"""
    def __init__(self, parent):
        self.p = parent

    def enable_power_supply(self, blocking=False, timeout=-1):
        args = {'output': self.p.settings.ps_output}
        req = self.p.request(target=TTiCPX_MOD, command='enable_output', arguments=args)
        if blocking:
            req.wait_answer(blocking=blocking, timeout=timeout)
            return req.return_value

    def disable_power_supply(self, blocking=False, timeout=-1):
        args = {'output': self.p.settings.ps_output}
        req = self.p.request(target=TTiCPX_MOD, command='disable_output', arguments=args)
        if blocking:
            req.wait_answer(blocking=blocking, timeout=timeout)
            return req.return_value

    def power_supply_update_vi(self, blocking=False, timeout=-1):
        args = {'output': self.p.settings.ps_output,
                'voltage': self.p.bc.voltage,
                'current_limit': self.p.bc.current}

        req = self.p.request(target=TTiCPX_MOD, command='update_vi', arguments=args)
        if blocking:
            req.wait_answer(blocking=blocking, timeout=timeout)
            return req.return_value

    def publish_status(self):
        status = {'state': self.p.sm.current_state.name,
                  'ps_output': self.p.settings.ps_output,
                  'tc_08_channel': self.p.settings.tc08_channel,
                  'cold_threshold': self.p.settings.cold_threshold,
                  'hot_threshold': self.p.settings.hot_threshold,
                  'temperature': self.p.bc.temperature,
                  'voltage': self.p.bc.voltage,
                  'current_limit': self.p.bc.current
                  }
        self.p.pub_event('status', status)


class BoundaryConditions(object):

    def __init__(self):
        self.temperature = 25
        self.voltage = 0
        self.current = 0


class Settings(object):
    def __init__(self):
        self.ps_output = 1  # Output of the Power Supply that feeds the electro cooler
        self.t_control_tc08_chan = 1  # tc to be used to enable/disable electro cooler
        self.cold_threshold = 15  # Thermo cooler switches off for lower temperatures
        self.hot_threshold = 16  # Thermo cooler switches on for higher temperatures
