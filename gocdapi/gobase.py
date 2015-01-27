"""
Module for gocdapi GoBase class
"""

import logging
from json import loads as jsonloads
from urlparse import urljoin

from requests import get, post
from gocdapi.custom_exceptions import GoCdApiException


class GoBase(object):
    """
    Base Class that all other GoCD objects are inherited from
    """
    def __init__(self, go_server, path=None, data=None, poll=True):
        """Inits GoBase objects.

        Args:
            go_server (Go): A Go object which this object belongs to
            path (str): Subpath of the full url to interact in the Go server API with the object.
            data (str): A json string representing the object configuration
            poll (bool): If it's to poll Go server to get new update data from the object
        """
        self._data = None
        self.url = None
        self.go_server = go_server
        self.set_self_url(path)

        if poll and self.url:
            self._data = self.get_data()
        elif data is not None:
            self._data = data
        self._poll()

    def __repr__(self):
        """Returns a representation string of the python object

        Returns:
            str: representation of the python object
        """
        return """<%s.%s %s>""" % (self.__class__.__module__, self.__class__.__name__, str(self))

    def __str__(self):
        """Returns a pretty representation of the object

        Should be override by the class that inherits from this one.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    def get_data(self):
        """Will poll object's data from Go server

        Gets information doing a GET request to url's object
        """
        return GoBase.get_text_data(self.url)

    def repoll(self):
        """Will repoll object's data from Go server

        Gets information doing a GET request to url's object
        """
        self._data = self.get_data()
        self._poll()

    def set_self_url(self, path):
        """Set the url of object

        Args:
            path (str): subpath to join to base url of Go Server
        """
        if path:
            self.url = urljoin(self.go_server.baseurl, path)

    def build_url(self, path):
        """Joins the url of the object with the given path

        Args:
            path (str): subpath to join to the object's url
        """
        return urljoin(self.url, path)

    def build_url_with_base(self, path):
        """Joins the base url of the Go server with the given path

        Args:
            path (str): subpath to join to the object's url
        """
        return urljoin(self.go_server.baseurl, path)

    @staticmethod
    def get_json_data(url, params=None):
        """Get the json data from a GET request

        Args:
            url (str): url to get the json data
            params (dict): params to be passed through the GET request

        Returns:
            str: json string from the response of the request

        Raises:
            GoCdApiException: when the response can't be parsed as a json string
        """

        try:
            response = GoBase.get_full_response(url, params)
            return response.json()
        except ValueError:
            logging.exception('Inappropriate content found at %s', url)
            raise GoCdApiException('Cannot parse %s' % response.text)

    @staticmethod
    def load_json_data(json_str):
        try:
            return jsonloads(json_str)
        except ValueError:
            raise GoCdApiException('Cannot parse %s' % json_str)

    @staticmethod
    def get_text_data(url, params=None):
        """Get the text response from a GET request

        Args:
            url (str): url to get the json data
            params (dict): params to be passed through the GET request

        Returns:
            str: text response from the get request.
        """
        return GoBase.get_full_response(url, params).text

    @staticmethod
    def get_full_response(url, params=None):
        """Do a GET request

        Args:
            url (str): url to get the json data
            params (dict): params to be passed through the GET request

        Returns:
            requests.Response: response from the get request
        """
        response = get(url, params=params)
        return GoBase.do_handle_response(response)

    @staticmethod
    def do_post(url, params=None, data=None):
        """Do a POST request

        Args:
            url (str): url to get the json data
            params (dict): params to be passed through the POST request
            data (dict): data to be passed through the POST request

        Returns:
            requests.Response: response from the get request
        """
        response = post(url, params=params, data=data)
        return GoBase.do_handle_response(response).text

    @staticmethod
    def do_handle_response(response):
        """Handle a requests.Response looking for http error codes

        Args:
            response (requests.Response): the response to handle

        Returns:
            requests.Response: response, passed as argument, when it it a good response

        Raises:
            GoCdApiException: When response is a 4XX client error or 5XX server error response
        """
        try:
            response.raise_for_status()
            return response
        except Exception:
            logging.error('Failed %s request at %s', response.request.method, response.url)
            raise GoCdApiException("[%i] - %s" % (response.status_code, response.text))

    def _poll(self):
        """ To be overrided. Goal: poll new data to fill the object attributes.

        Should be override by the class that inherits from this one.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError
