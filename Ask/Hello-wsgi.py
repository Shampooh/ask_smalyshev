"""
WSGI config for Ask project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from pprint import pformat
from cgi import parse_qsl, escape

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Ask.settings")

def application(environ, start_response):
	start_response('200 OK', [('Content-Type', 'text/plain')])
	return ['Hello World!\n']