#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'otger'


def gfa_thermal_monitor():
    from gfa_thermal import config, system_names
    from gfa_thermal.monitor_system import SystemMonitorGFAThermal
    from entropyfw.logger import log
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

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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

    s = SystemMonitorGFAThermal(flask_app=app)
    print(app.url_map)

    # Enable channel
    for chan in range(9):
        conf_val = getattr(config, 'TC08_CHAN_{}'.format(chan))
        if conf_val['enable']:
            log.info('Enabling Channel {}'.format(chan))
            s.enable_tc08_channel(chan, tc_type=conf_val['tc_type'], units=conf_val['units'])
    #
    # chan = config.TEMPERATURE_CHANNEL_AMBIENT
    # conf_val = getattr(config, 'TC08_CHAN_{}'.format(chan))
    # if conf_val['enable']:
    #     log.info('Enabling Channel {}'.format(chan))
    #     s.enable_tc08_channel(chan, tc_type=conf_val['tc_type'], units=conf_val['units'])

    # Configure logger values to save
    s.elogger.add_log('{}.{}'.format(system_names.TC08_MOD, 'temperatures'))
    # s.elogger.add_log('{}.{}'.format(system_names.TTiCPX_MOD, 'status.1'))
    # s.elogger.add_log('{}.{}'.format(system_names.TTiCPX_MOD, 'status.2'))

    # start loop on tc08 and tticpx every x seconds set at config
    # s.tticpx.start_timer(config.SENSORS_LOOP_INTERVAL)
    s.pico.start_timer(config.SENSORS_LOOP_INTERVAL)
    print(s.list_callbacks())
    try:
        server.serve_forever()
    finally:
        # s.tticpx.stop_timer()
        s.pico.stop_timer()
        print(s.list_callbacks())
        s.exit()

if __name__ == "__main__":
    gfa_thermal_monitor()
