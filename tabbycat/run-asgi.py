# tabbycat/run-asgi.py

import logging
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tabbycat.settings")
django.setup()

root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

import asgi
from daphne.endpoints import build_endpoint_description_strings
from daphne.server import Server

if 'USING_NGINX' in os.environ and bool(int(os.environ['USING_NGINX'])):
    root.info('TC_DEPLOY: Initialising Daphne with NGINX')
    Server(
        application=asgi.application,
        endpoints=build_endpoint_description_strings(
            unix_socket="/tmp/asgi.socket",
        ),
        ping_interval=15,
        ping_timeout=30,
        websocket_timeout=10800,
        websocket_connect_timeout=10,
        application_close_timeout=10,
        verbosity=2,
        proxy_forwarded_address_header="X-Forwarded-For",
        proxy_forwarded_port_header="X-Forwarded-Port",
        proxy_forwarded_proto_header="X-Forwarded-Proto",
    ).run()
else:
    root.info('TC_DEPLOY: Initialising Daphne with Host/Port')
    Server(
        application=asgi.application,
        endpoints=build_endpoint_description_strings(
            host="0.0.0.0",
            port="8000",
        ),
        ping_interval=15,
        ping_timeout=30,
        websocket_timeout=10800,
        websocket_connect_timeout=10,
        application_close_timeout=10,
        verbosity=2,
        proxy_forwarded_address_header="X-Forwarded-For",
        proxy_forwarded_port_header="X-Forwarded-Port",
        proxy_forwarded_proto_header="X-Forwarded-Proto",
    ).run()
