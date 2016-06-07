'''
System tests for `gocdapi.admin` module.
'''
import unittest

from gocdapi_tests.systests.base import BaseSystemTest
from gocdapi_tests.systests.pipeline_configs import EMPTY_PIPELINE
from gocdapi_tests.test_utils.random_strings import random_string


class TestGo(BaseSystemTest):
    def test_pipeline_exist(self):
        pipeline_name = 'test_pipeline_%s' % random_string()
        self.go.admin.create_pipeline_from_xml(self.pipeline_group_name(), EMPTY_PIPELINE % pipeline_name)
        self.assertTrue(self.go.pipeline_exist(pipeline_name))

        self.assertFalse(self.go.pipeline_exist("false_pipeline"))

    def test_get_pipeline(self):
        pipeline_name = 'test_pipeline_%s' % random_string()

        self.assertIsNone(self.go.get_pipeline(pipeline_name))

        self.go.admin.create_pipeline_from_xml(self.pipeline_group_name(), EMPTY_PIPELINE % pipeline_name)
        self.assertIsNotNone(self.go.get_pipeline(pipeline_name))


if __name__ == '__main__':
    unittest.main()
