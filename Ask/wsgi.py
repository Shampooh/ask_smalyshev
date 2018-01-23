"""
WSGI config for Ask project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

#Main WSGI

import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Ask.settings")
application = get_wsgi_application()

"""
#Hello world

from pprint import pformat
from cgi import parse_qsl, escape

def application(environ, start_response):
	output = ['<p>WSGI!</p>']
	output.append('Hello world!')
	if environ['SERVER_PORT'] == '8081':
		output.append('Post:')
		output.append('<form method="post">')
		output.append('<input type="text" name = "test">')
		output.append('<input type="submit" value="Send">')
		output.append('</form>')

		d = parse_qsl(environ['QUERY_STRING'])
		if environ['REQUEST_METHOD'] == 'POST':
			output.append('<h1>Post  data:</h1>')
			output.append(pformat(environ['wsgi.input'].read()))

		if environ['REQUEST_METHOD'] == 'GET':
			output.append('<h1>Get data:</h1>')
			if environ['QUERY_STRING'] != '':
				for ch in d:
					output.append(' = '.join(ch))
					output.append('<br>')

		output_len = sum(len(line) for line in output)
		start_response('200 OK', [('Content-type', 'text/html'), ('Content-Length', str(output_len))])
	return output
"""

"""
	if request.META['SERVER_PORT'] == '8081':
		output.append('Post:')
		output.append('<form method="post">')
		output.append('<input type="text" name = "test">')
		output.append('<input type="submit" value="Send">')
		output.append('</form>')

		d = request.GET
		if request.META['REQUEST_METHOD'] == 'POST':
			output.append('<h1>Post  data:</h1>')
		elif request.META['REQUEST_METHOD'] == 'GET':
			output.append('<h1>Get data:</h1>')
		if request.META['QUERY_STRING'] != '':
			for ch in d:
				output.append(' = '.join(ch))
				output.append('<br>')

		output_len = sum(len(line) for line in output)
		start_response('200 OK', [('Content-type', 'text/html'), ('Content-Length', str(output_len))])
"""