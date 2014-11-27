'''
System tests for `gocdapi.go` module.
'''
import unittest

from gocdapi_tests.systests.base import BaseSystemTest
from gocdapi_tests.systests.pipeline_configs import EMPTY_PIPELINE
from gocdapi_tests.test_utils.random_strings import random_string


class TestPipelines(BaseSystemTest):

    def test_create_pipeline(self):
        pipeline_name = 'test_pipeline_%s' % random_string()
        self.go.create_pipeline(self.pipeline_group_name(), EMPTY_PIPELINE % pipeline_name)
        self.assert_pipeline_is_present(pipeline_name)

    def test_create_pipeline_group(self):
        pipeline_group = 'test_pipeline_group_%s' % random_string()
        self.go.create_pipeline_group(pipeline_group)
        self.assertTrue(pipeline_group in self.go.pipeline_groups)

    def test_delete_pipeline_group(self):
        pipeline_group = 'test_pipeline_group_%s' % random_string()
        self.go.create_pipeline_group(pipeline_group)
        self.go.delete_pipeline_group(pipeline_group)
        self.assertFalse(pipeline_group in self.go.pipeline_groups)


if __name__ == '__main__':
    unittest.main()
