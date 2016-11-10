import csv

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


BASE_URL = 'https://api.domo.com'
AUTH_URI = 'oauth/token?grant_type=client_credentials&scope=data'

class DomoApi(object):

	def __init__(self, client_id, client_secret, base_url=BASE_URL):
		self._client_id = client_id
		self._client_secret = client_secret
		self._base_url = base_url
		self._response_headers = [()]

	def send_request(self, http_method, route_uri, data=None, params={}, headers=None, base_url=BASE_URL, auth_uri=AUTH_URI):

		token_url = '%s/%s' % (base_url, auth_uri)
		client = BackendApplicationClient(client_id=self.client_id)
		oauth = OAuth2Session(client=client)
		token = oauth.fetch_token(token_url=token_url, client_id=self.client_id, client_secret=self.client_secret)      
		
		request_url = '%s/%s' % (base_url, route_uri)
		request = oauth.request(http_method, request_url, data=data, headers=headers, params=params)

		return request

	def export(self, dataset_id, params={'includeHeader':'true'}):
		route_uri = 'v1/datasets/%s/data' % (dataset_id)
		request = self.send_request('get', route_uri, params=params)

		data = []
		
		lines = request.text.splitlines()
		keys = lines.pop(0).split(',')
		for line in lines:
			data.append(dict(zip(keys, line.split(','))))

		return data

	@property
	def response_headers(self):
		"""Get the response's header from last request made.
		Type signature:
		    () -> [(header,value)]
		"""
		return self._response_headers

	def get_client_secret(self):
		"""Secret Key getter.
		Type signature:
		    () -> str
		Example:
		    api = api(...)
		    print 'the client secret is ', api.client_secret
		"""
		return self._client_secret

	def set_client_secret(self, value):
		"""Secret Key setter.
		Type signature:
		    (str) -> None
		Parameters:
		    value - the secret key to be set
		Example:
		    api = api(...)
		    api.secret_key = "xxxxxx"
		    print 'the new client secret is ', api.client_secret
		"""
		self._client_secret = value

	client_secret = property(get_client_secret, set_client_secret)

	def get_client_id(self):
		"""Client ID getter.
		Type signature:
		    () -> str
		Example:
		    api = api(...)
		    print 'the API key is ', api.client_id
		"""
		return self._client_id

	def set_client_id(self, value):
		"""Client ID setter.
		Type signature:
		    (str) -> None
		Parameters:
		    value - the API key to be set
		Example:
		    api = api(...)
		    api.client_id = "yyyyyy"
		    print 'the new API key is ', api.client_id
		"""
		self._client_id = value

	client_id = property(get_client_id, set_client_id)

	def get_base_url(self):
		"""Base url getter.
		Type signature:
			() -> str
		Example:
			api = api(...)
			print 'the base url is ', api.base_url
		"""
		return self._base_url

	def set_base_url(self, value):
		"""Base url setter.
		Type signature:
			(str) -> None
		Parameters:
			value - the url's base to be set
		Example:
			api = api(...)
			api.base_url = "cache.api.ooyala.com"
			print 'the new url's base is ', api.base_url
		"""
		self._base_url = value

	base_url = property(get_base_url, set_base_url)
    



