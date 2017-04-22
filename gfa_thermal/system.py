#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw import System

from s_pico_tc08.module import EntropyPicoTc08
from s_tti_cpx.module import EntropyTTiCPX
from s_laird_optotec_ot15.module import EntropyLairdOT15ConstantQc
from .s_controller.module import EntropyController as GFAEntropyController
from s_eventlogger.module import EntropyEventLogger

from . import system_names

__author__ = 'otger'


class SystemGFAThermal(System):

    def __init__(self, flask_app):
        System.__init__(self, flask_app)
        self.pico = EntropyPicoTc08(name=system_names.TC08_MOD)
        self.add_module(self.pico)
        self.tticpx = EntropyTTiCPX(name=system_names.TTiCPX_MOD)
        self.add_module(self.tticpx)
        self.ot15 = EntropyLairdOT15ConstantQc(name=system_names.LAIRD_MOD, qc=config.LAIRD_QC_DESIRED)
        self.add_module(self.ot15)
        self.controller = GFAEntropyController(name=system_names.CONTROL_MOD)
        self.add_module(self.controller)
        self.elogger = EntropyEventLogger(name=system_names.LOGGER_MOD)

    def connect_power_supply(self, ip, port=9221):
        args = {'ip': ip,
                'port': port}
        self.send_request(target=system_names.TTiCPX_MOD, command='connect', arguments=args)

    def enable_tc08_channel(self, channel, tc_type='T', units='Kelvin'):
        args = {'channel': int(channel),
                'tc_type': tc_type,
                'units': units}

        self.send_request(target=system_names.TC08_MOD, command='enable_channel', arguments=args)


if __name__ == "__main__":
    from . import config
    from entropyfw.logger import log, formatter
    import logging
    from logging.handlers import RotatingFileHandler
    from gevent.wsgi import WSGIServer
    from flask import Flask, url_for

    from flask.templating import DispatchingJinjaLoader

    app = Flask(__name__)
    server = WSGIServer(("", 5000), app)
    server.start()


    @app.errorhandler(Exception)
    def all_exception_handler(error):
        log.exception('Whatever exception')

    @app.errorhandler(404)
    def handle_bad_request(e):
        log.exception('Whatever exception')

    if config.STREAM_LOG:
        ch = logging.StreamHandler()
        ch.setLevel(config.STREAM_LOG_LEVEL)
        ch.setFormatter(formatter)
        log.addHandler(ch)

    if config.FILE_LOG:
        ch = RotatingFileHandler(config.FILE_LOG_PATH,
                                 mode='a',
                                 maxBytes=config.FILE_LOG_MAX_SIZE,
                                 backupCount=config.FILE_LOG_BACKUP,
                                 encoding=None,
                                 delay=0
                                 )
        ch.setLevel(config.FILE_LOG_LEVEL)
        ch.setFormatter(formatter)
        log.addHandler(ch)

    s = SystemGFAThermal(flask_app=app)
    print(app.url_map)

    # Enable channel
    for chan in range(9):
        conf_val = getattr(config, 'TC08_CHAN_{}'.format(chan))
        if conf_val['enable']:
            s.enable_tc08_channel(chan, tc_type=conf_val['tc_type'], units=conf_val['units'])

    # connect to tticpx
    s.connect_power_supply(ip=config.TTiCPX_IP, port=config.TTiCPX_PORT)

    # Register temperatures and applied V, I for electro cooler calculator
    s.ot15.register_temp_event('{}.temperatures'.format(system_names.TC08_MOD),
                               tc_keyword='channel_{}'.format(config.TEMPERATURE_CHANNEL_TC_COLD),
                               th_keyword='channel_{}'.format(config.TEMPERATURE_CHANNEL_TC_HOT))
    s.ot15.register_event_iv_applied(pattern='{}.status.{}'.format(system_names.TTiCPX_MOD, config.TTiCPX_OUTPUT),
                                     i_keyword='current',
                                     v_keyword='voltage')
    # Register event for control
    s.controller.register_electrocooler_calc(event_name='{}.constant_qc_vi'.format(system_names.LAIRD_MOD))
    s.controller.register_temperatures_callback(event_name='{}.temperatures'.format(system_names.TC08_MOD),
                                                temp_control_channel=config.TEMPERATURE_CHANNEL_CONTROL,
                                                cold_threshold=config.CONTROL_COLD_THRESHOLD,
                                                hot_threshold=config.CONTROL_HOT_THRESHOLD)

    # Configure logger values to save

    # start loop on tc08 and tticpx every x seconds set at config
    s.tticpx.start_timer(config.SENSORS_LOOP_INTERVAL)
    s.pico.start_timer(config.SENSORS_LOOP_INTERVAL)

    try:
        server.serve_forever()
    finally:
        s.exit()
