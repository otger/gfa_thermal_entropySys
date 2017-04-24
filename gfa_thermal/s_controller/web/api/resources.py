#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw.api.rest import ModuleResource
from flask import jsonify
from flask_restful import reqparse
from entropyfw.common import get_utc_ts
from PicoController.common.definitions import THERMOCOUPLES, UNITS
from .logger import log
from s_pico_tc08 import T_UNITS, TC_TYPES
"""
resources
Created by otger on 29/03/17.
All rights reserved.
"""


class StartCooling(ModuleResource):
    url = 'start_cooling'
    description = "Configures GFA Thermal tests controller to enable Electro cooler"

    def __init__(self, module):
        super(StartCooling, self).__init__(module)

    def post(self):
        self.module.start_cooling()

        return jsonify({'utc_ts': get_utc_ts(),
                        'result': 'done'})


class StopCooling(ModuleResource):
    url = 'stop_cooling'
    description = "Configures GFA Thermal tests controller to stop Electro cooler cycles"

    def __init__(self, module):
        super(StopCooling, self).__init__(module)

    def post(self):
        self.module.stop_cooling()

        return jsonify({'utc_ts': get_utc_ts(),
                        'result': 'done'})


class SetThresholds(ModuleResource):
    url = 'set_thresholds'
    description = "GFA Thermal tests when running switches on and of an electro cooler based on thresholds"

    def __init__(self, module):
        super(SetThresholds, self).__init__(module)
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('cold_threshold', type=float, required=True, location='json')
        self.reqparse.add_argument('hot_threshold', type=float, required=True, location='json')

    def post(self):
        args = self.reqparse.parse_args()

        try:
            self.module.set_thresholds(t_cold=args['cold_threshold'], t_hot=args['hot_threshold'])
        except Exception as ex:
            log.exception('Something went wrong when setting thresholds with arguments: {0}'.format(args))

        return jsonify({'args': args,
                        'utc_ts': get_utc_ts(),
                        'result': 'done'})


class Status(ModuleResource):
    url = 'status'
    description = "Returns status of controller"

    def get(self):
        return jsonify(self.module.func.status)


def get_api_resources():
    return [StartCooling, StopCooling, SetThresholds, Status]
