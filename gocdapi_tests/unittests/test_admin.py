import unittest

from gocdapi.admin import Admin
from gocdapi.go import Go


class TestAdmin(unittest.TestCase):
    def setUp(self):
        self.baseurl = 'http://localhost:8080'
        self.go = Go(self.baseurl)
        self.admin = Admin(self.go)

    def test_repr(self):
        self.assertEquals(str(self.admin), 'Admin Control @ %s' % self.baseurl)


if __name__ == '__main__':
    unittest.main()
