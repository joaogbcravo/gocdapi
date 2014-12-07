'''
System tests for `gocdapi.go` module.
'''
import unittest

from gocdapi_tests.systests.base import BaseSystemTest

class TestAdmin(BaseSystemTest):

    def test_reload_command_repo_cache(self):
        self.go.admin.reload_command_repo_cache()

if __name__ == '__main__':
    unittest.main()
