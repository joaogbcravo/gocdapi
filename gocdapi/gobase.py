"""
Module for GoBase class
"""

import logging
from json import loads as jsonloads

try:
    from urlparse import urljoin
except ImportError:
    # Python3
    from urllib.parse import urljoin

from requests import get, post
from gocdapi.custom_exceptions import GoCdApiException


class GoBase(object):
    """
    This appears to be the base object that all other Go objects are inherited from
    """
    def __init__(self, go_server, path=None, data=None, poll=True):
        self._data = None
        self.url = None
        self.go_server = go_server
        self.set_self_url(path)
        if poll:
            self._poll(data)

    def _poll(self, data):
        if not data and self.url:
            self._data = GoBase.get_data(self.url)
        else:
            self._data = data
        self.poll()

    def set_self_url(self, path):
        if path:
            self.url = urljoin(self.go_server.baseurl, path)

    def build_url(self, path):
        return urljoin(self.url, path)

    def build_url_with_base(self, path):
        return urljoin(self.go_server.baseurl, path)

    @staticmethod
    def get_json_data(url, params=None):
        json_str = GoBase.get_data(url, params)
        try:
            json_str = GoBase.get_data(url, params)
            return jsonloads(json_str)
        except ValueError:
            logging.exception('Inappropriate content found at %s', url)
            raise GoCdApiException('Cannot parse %s' % json_str)

    @staticmethod
    def load_json_data(json_str):
        try:
            return jsonloads(json_str)
        except ValueError:
            raise GoCdApiException('Cannot parse %s' % json_str)

    @staticmethod
    def get_data(url, params=None):
        return GoBase.get_full_response(url, params).text

    @staticmethod
    def get_full_response(url, params=None):
        response = get(url, params=params)
        return GoBase.do_handle_response(response, "get", url, params)

    @staticmethod
    def do_post(url, params=None, data=None):
        response = post(url, params=params, data=data)
        return GoBase.do_handle_response(response, "post", url, params).text

    @staticmethod
    def do_handle_response(response, method, url, params=None):
        if response.status_code not in [200, 201, 202]:
            logging.error('Failed %s request at %s with params: %s', method, url, params)
            raise GoCdApiException("[%i] - %s" % (response.status_code, response.text))
        return response
