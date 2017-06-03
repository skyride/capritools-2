import requests
import json

from base64 import b64encode
from urllib import urlencode
from hashlib import sha256

from django.conf import settings
from django.core.cache import cache


# ESI Api wrapper
class ESI():
    token = None
    url = settings.ESI_URL
    datasource = settings.ESI_DATASOURCE


    # Wrapper for GET
    def get(self, url, data=None, get_vars={}, cache_time=30, debug=settings.DEBUG):
        return self.request(url, data=data, method=requests.get, get_vars=get_vars, cache_time=cache_time, debug=debug)

    # Wrapper for POST
    def post(self, url, data=None, get_vars={}, cache_time=30, debug=settings.DEBUG):
        return self.request(url, data=data, method=requests.post, get_vars=get_vars, cache_time=30, debug=debug)


    def request(self, url, data=None, method=requests.get, retries=0, get_vars={}, cache_time=30, debug=settings.DEBUG):
        # Do replacements
        full_url = url

        # Try request
        full_url = "%s%s?%s" % (self.url, full_url, self._get_variables(get_vars))
        if debug:
            print full_url

        # Check the cache for a response
        cache_key = sha256("%s:%s:%s" % (str(method), full_url, json.dumps(data))).hexdigest()
        r = cache.get(cache_key)
        if r != None:
            r = json.loads(r)
            if r == None:
                return None
            else:
                return r

        # Nope, no cache, hit the API
        r = method(full_url, data=data)

        # ESI is buggy, so lets give it up to 10 retries for 500 error
        if r.status_code in [500, 502]:
            if retries < settings.ESI_RETRIES:
                return self.request(url, data=data, method=method, retries=retries+1)
            else:
                cache.set(cache_key, json.dumps(None), cache_time)
                return None

        # Load json and return
        if r.status_code == 200:
            j = json.loads(r.text)
            cache.set(cache_key, r.text, cache_time)
            return j
        else:
            cache.set(cache_key, json.dumps(None), cache_time)
            return None


    # Takes an ESIToken object as the constructor
    def __init__(self, token=None):
        self.token = token


    def _bearer_header(self):
        if self.token == None:
            headers = {}
        else:
            headers = {
                "Authorization": "Bearer %s" % self.token.access_token
            }
        return headers


    def _get_variables(self, get_vars):
        get_vars['datasource'] = self.datasource
        return urlencode(get_vars)
