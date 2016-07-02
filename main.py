# -*- coding: utf-8 -*-

import argparse
from jetkeys import app, config

parse = argparse.ArgumentParser()
parse.add_argument("--host", dest="host", action="store", default="0.0.0.0", type=str, help="IP Address to listen to")
parse.add_argument("--port", dest="port", action="store", default="9110", type=int, help="Port number to listen to")
parse.add_argument("--period", dest="period", action="store", default='607875500', type=str,
                   help="default value: 607875500")

args, others = parse.parse_known_args()
config.PROLONGATION_PERIOD = args.period

app.run(host=args.host, port=args.port)
