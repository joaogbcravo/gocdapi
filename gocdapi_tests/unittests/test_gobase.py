import mock

import unittest

from gocdapi.gobase import GoBase
from gocdapi.go import Go
from requests import Response

from gocdapi.custom_exceptions import GoCdApiException

class TestGoBase(unittest.TestCase):

    @mock.patch.object(GoBase, '_poll')
    def setUp(self, gobase_poll):
        gobase_poll.return_value = True
        go = Go('http://localhost:8080')
        self.gobase = GoBase(go, 'http://localhost:8080', None, False)

    def test_str(self):
        with self.assertRaises(NotImplementedError):
            str(self.gobase)

    @mock.patch.object(GoBase, '__str__')
    def test_repr(self, gobase_str):
        gobase_str.return_value = "test_go_base_str"
        self.assertEqual(repr(self.gobase), """<gocdapi.gobase.GoBase test_go_base_str>""")

    @mock.patch.object(GoBase, 'get_full_response')
    def test_get_json_data(self, gobase_get_full_response):
        response = Response()
        response._content = "not a json object"
        gobase_get_full_response.return_value = response

        with self.assertRaises(GoCdApiException):
            self.gobase.get_json_data(self.gobase.url)

    def test_load_json_data(self):
        with self.assertRaises(GoCdApiException):
            self.gobase.load_json_data("not a json object")

if __name__ == '__main__':
    unittest.main()
