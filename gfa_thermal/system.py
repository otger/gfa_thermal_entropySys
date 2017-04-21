#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw import System

from s_pico_tc08.module import EntropyPicoTc08
from s_tti_cpx.module import EntropyTTiCPX
from s_laird_optotec_ot15.module import EntropyLairdOT15ConstantQc
from .s_controller.module import EntropyController as GFAEntropyController

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

    def connect_power_supply(self, ip, port=9221):
        args = {'ip': ip,
                'port': port}
        self.send_request(target=system_names.TTiCPX_MOD, command='connect', arguments=args)


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

    # Register udpatevi callback for selected values of tticpx output on config
    # self.ot15

    # start loop on tc08 and tticpx every x seconds set at config

    # connect to tticpx
    s.connect_power_supply(ip=config.TTiCPX_IP, port=config.TTiCPX_PORT)

    try:
        server.serve_forever()
    finally:
        s.exit()
