#!/usr/bin/python
#


import logging
from cgi import parse_qs
from datetime import datetime
import re
import random
import os
import string
import urllib
from urlparse import urlparse
import json
import webapp2
from google.appengine.api import oauth
import traceback




# _ENCODE_TRANS_TABLE = string.maketrans('-: .@', '_____')

class BaseHandler(webapp2.RequestHandler):
	"""The other handlers inherit from this class.  Provides some helper methods
	for rendering a template."""

	@webapp2.cached_property
	def jinja2(self):
	  return jinja2.get_jinja2(app=self.app)

	def render_template(self, filename, template_args):
	  self.response.write(self.jinja2.render_template(filename, **template_args))





class MainHandler(BaseHandler):
	"""Handles search requests for comments."""



	def get(self):
		
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Hi there!\n')

		# Note, unlike in the Android app below, there's no 'oauth2:' prefix here
		scope = 'https://www.googleapis.com/auth/userinfo.email'
		try:
		  self.response.write('\noauth.get_current_user(%s)' % repr(scope))

		  # validates audience of the OAuth2 access token
		  #allowed_clients = ['407408718192.apps.googleusercontent.com'] # list your client ids here
		  token_audience = oauth.get_client_id(scope)
		  self.response.write('\ntoken_audience = %s\n' % token_audience)		  

		  # gets user object for the user represented by the oauth token
		  user = oauth.get_current_user(scope)
		  self.response.write(' = %s\n' % user)
		  self.response.write('- auth_domain = %s\n' % user.auth_domain())
		  self.response.write('- email       = %s\n' % user.email())
		  self.response.write('- nickname    = %s\n' % user.nickname())
		  self.response.write('- user_id     = %s\n' % user.user_id())
		except oauth.OAuthRequestError, e:
		  self.response.set_status(401)
		  self.response.write(' -> %s %s\n' % (e.__class__.__name__, e.message))
		  logging.warn(traceback.format_exc())

		#self.response.write('Main')

   
logging.getLogger().setLevel(logging.DEBUG)


application = webapp2.WSGIApplication([
	('/.*', MainHandler)

	],
	debug=True)


