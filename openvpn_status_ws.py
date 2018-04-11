#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import signal
import logging
from tornado.options import define, parse_command_line, options
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from openvpn_status_ws_helper import parse_status_log
from openvpn_status_ws_application import OpenvpnStatusWsApplication

define('debug', default=False, type=bool, help='Run in debug mode')
define('port', default=12200, type=int, help='Server port')
define('allowed_hosts', default="localhost:12200", multiple=True,
       help='Allowed hosts for cross domain connections')


parse_command_line()
application = OpenvpnStatusWsApplication(debug=options.debug)
server = HTTPServer(application)
server.listen(options.port)
signal.signal(signal.SIGINT, lambda sig, frame: shutdown(server))
logging.info('Starting server on localhost:{}'.format(options.port))
IOLoop.instance().start()

def shutdown(server):
    ioloop = IOLoop.instance()
    logging.info('Stopping server.')
    server.stop()
