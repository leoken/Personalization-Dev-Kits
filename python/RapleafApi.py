import urllib
from urllib3 import HTTPSConnectionPool, TimeoutError		# See README for download instructions
import json
import hashlib

class RapleafApi:
	apiKey = 'SET_ME'		# Set your API key here
		 
	headers = {'User-Agent' : 'RapleafApi/Python/1.1'}
	basePath = '/v4/dr?api_key=%s' %(apiKey)
	host = 'personalize.rlcdn.com'
	timeout = 2.0
	
	def __init__(self):
		self.handle = HTTPSConnectionPool(RapleafApi.host, timeout = RapleafApi.timeout)
	
	def query_by_email(self, email, hash_email = None):
		"""
		Takes an e-mail and returns a hash which maps attribute fields onto attributes
		If the hash_email option is set, then the email will be hashed before it's sent to Rapleaf
		"""
		if hash_email:
			s = hashlib.sha1()
			s.update(email)
			return self.query_by_sha1(s.digest())
		url = '%s&email=%s' % (RapleafApi.basePath, urllib.quote(email))
		return self.get_json_response(url)
	
	def query_by_md5(self, email):
		"""
		Takes an e-mail that has already been hashed by md5
		and returns a hash which maps attribute fields onto attributes
		"""
		url = '%s&md5_email=%s' % (RapleafApi.basePath, urllib.quote(email))
		return self.get_json_response(url)
	
	def query_by_sha1(self, email):
		"""
		Takes an e-mail that has already been hashed by sha1
		and returns a hash which maps attribute fields onto attributes
		"""
		url = '%s&sha1_email=%s' % (RapleafApi.basePath, urllib.quote(email))
		return self.get_json_response(url)
		
	def query_by_nap(self, first, last, street, city, state, email = None):
		"""
		Takes first name, last name, and postal (street, city, and state acronym),
		and returns a hash which maps attribute fields onto attributes
		Though not necessary, adding an e-mail increases hit rate
		"""
		if email:
			url = '%s&email=%s&street=%s&city=%s&state=%s' % (RapleafApi.basePath, urllib.quote(email), urllib.quote(street), urllib.quote(city), state)
		else:
			url = '%s&street=%s&city=%s&state=%s' % (RapleafApi.basePath, urllib.quote(street), urllib.quote(city), state)
		return self.get_json_response(url)
	
	def query_by_naz(self, first, last, zip4, email = None):
		"""
		Takes first name, last name, and zip4 code (5-digit zip 
		and 4-digit extension separated by a dash as a string),
		and returns a hash which maps attribute fields onto attributes
		Though not necessary, adding an e-mail increases hit rate
		"""
		if email:
			url = '%s&email=%s&first=%s&last=%s&zip4=%s' % (RapleafApi.basePath, urllib.quote(email), first, last, zip4)
		else:
			url = '%s&first=%s&last=%s&zip4=%s' % (RapleafApi.basePath, first, last, zip4)
		return self.get_json_response(url)
		
	def get_json_response(self, path):
		"""
		Pre: Path is an extension to personalize.rlcdn.com
		Note that an exception is raised if an HTTP response code
		other than 200 is sent back. In this case, both the error code
		the error code and error body are accessible from the exception raised
		"""
		json_response = self.handle.get_url(path, headers = RapleafApi.headers)
		if 200 <= json_response.status < 300:
			if json_response.data:
				return json.JSONDecoder().decode(json_response.data)
			else:
				return {}
		else:
			raise Exception(json_response.status, json_response.data)
			