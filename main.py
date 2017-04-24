#!/usr/bin/python
# -*- coding: utf-8 -*-


__author__ = 'otger'
if __name__ == "__main__":
    from gfa_thermal import config, system_names
    from gfa_thermal.system import SystemGFAThermal
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

    s = SystemGFAThermal(flask_app=app)
    print(app.url_map)

    # Enable channel
    for chan in range(9):
        conf_val = getattr(config, 'TC08_CHAN_{}'.format(chan))
        if conf_val['enable']:
            log.info('Enabling Channel {}'.format(chan))
            s.enable_tc08_channel(chan, tc_type=conf_val['tc_type'], units=conf_val['units'])

    # connect to tticpx
    log.info('Connecting to power supply at {}:{}'.format(config.TTiCPX_IP, config.TTiCPX_PORT))
    s.connect_power_supply(ip=config.TTiCPX_IP, port=config.TTiCPX_PORT)

    # Register temperatures and applied V, I for electro cooler calculator
    log.info('Electro cooler calculator - registering temperature event')
    s.ot15.register_temp_event('{}.temperatures'.format(system_names.TC08_MOD),
                               tc_keyword='channel_{}'.format(config.TEMPERATURE_CHANNEL_TC_COLD),
                               th_keyword='channel_{}'.format(config.TEMPERATURE_CHANNEL_TC_HOT))
    log.info('Electro cooler calculator - registering power supply values event')
    s.ot15.register_event_iv_applied(pattern='{}.status.{}'.format(system_names.TTiCPX_MOD, config.TTiCPX_OUTPUT),
                                     i_keyword='current',
                                     v_keyword='voltage')
    # Set configuration values for controller
    s.controller.register_temperatures_callback(event_name='{}.temperatures'.format(system_names.TC08_MOD),
                                                temp_control_channel=config.TEMPERATURE_CHANNEL_CONTROL,
                                                cold_threshold=config.CONTROL_COLD_THRESHOLD,
                                                hot_threshold=config.CONTROL_HOT_THRESHOLD)
    # s.controller.set_thresholds(t_cold=config.CONTROL_COLD_THRESHOLD,
    #                             t_hot=config.CONTROL_HOT_THRESHOLD)
    # Register event for control
    # s.controller.set_channels(control_temp=config.TEMPERATURE_CHANNEL_CONTROL,
    #                           cooler_cold_side=config.TEMPERATURE_CHANNEL_TC_COLD,
    #                           cooler_hot_side=config.TEMPERATURE_CHANNEL_TC_HOT)
    s.controller.register_electrocooler_calc(event_name='{}.constant_qc_vi'.format(system_names.LAIRD_MOD))

    # Configure logger values to save
    s.elogger.add_log('{}.{}'.format(system_names.TC08_MOD, 'temperatures'))
    s.elogger.add_log('{}.{}'.format(system_names.LAIRD_MOD, 'status'))

    # start loop on tc08 and tticpx every x seconds set at config
    s.tticpx.start_timer(config.SENSORS_LOOP_INTERVAL)
    s.pico.start_timer(config.SENSORS_LOOP_INTERVAL)
    print(s.list_callbacks())
    try:
        server.serve_forever()
    finally:
        s.tticpx.stop_timer()
        s.pico.stop_timer()
        print(s.list_callbacks())
        s.exit()
