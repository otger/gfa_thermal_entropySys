#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw import System

from s_pico_tc08.module import EntropyPicoTc08
from s_tti_cpx.module import EntropyTTiCPX
from s_laird_optotec_ot15.module import EntropyLairdOT15ConstantQc
from .s_controller.module import EntropyController as GFAEntropyController
from s_eventlogger.module import EntropyEventLogger
from . import config

from . import system_names

__author__ = 'otger'


class SystemGFAThermal(System):

    def __init__(self, flask_app):
        System.__init__(self, flask_app)
        self.pico = EntropyPicoTc08(name=system_names.TC08_MOD, channels=[])
        self.add_module(self.pico)
        self.tticpx = EntropyTTiCPX(name=system_names.TTiCPX_MOD)
        self.add_module(self.tticpx)
        self.ot15 = EntropyLairdOT15ConstantQc(name=system_names.LAIRD_MOD, qc=config.LAIRD_QC_DESIRED)
        self.add_module(self.ot15)
        self.controller = GFAEntropyController(name=system_names.CONTROL_MOD)
        self.add_module(self.controller)
        self.elogger = EntropyEventLogger(name=system_names.LOGGER_MOD)
        self.add_module(self.elogger)

    def connect_power_supply(self, ip, port=9221):
        self.tticpx.connect(ip=ip, port=port)
        # args = {'ip': ip,
        #         'port': port}
        # self.send_request(target=system_names.TTiCPX_MOD, command='connect', arguments=args)

    def enable_tc08_channel(self, channel, tc_type, units):
        self.pico.enable(channel=channel, tc_type=tc_type, units=units)
        # args = {'channel': int(channel),
        #         'tc_type': tc_type,
        #         'units': units}
        #
        # return self.send_request(target=system_names.TC08_MOD, command='enable_channel', arguments=args)


