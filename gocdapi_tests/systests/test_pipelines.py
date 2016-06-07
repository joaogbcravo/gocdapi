"""
System tests for `gocdapi.go` module.
"""
import unittest

from gocdapi_tests.systests.base import BaseSystemTest


class TestPipelines(BaseSystemTest):
    def test_pipeline_pause_unpause_and_is_paused(self):
        self.pipeline = self.go.pipelines.values()[0]

        self.pipeline.pause("Test purposes")
        self.assertTrue(self.pipeline.is_paused())

        self.pipeline.unpause()
        self.assertFalse(self.pipeline.is_paused())

    def test_pipeline_is_schedulable(self):
        self.pipeline = self.go.pipelines.values()[0]

        self.pipeline.pause("Test purposes")
        self.assertFalse(self.pipeline.is_schedulable())

        self.pipeline.unpause()
        self.assertTrue(self.pipeline.is_schedulable())

    def test_pipeline_is_locked(self):
        self.pipeline = self.go.pipelines.values()[0]
        self.pipeline.unpause()
        self.assertFalse(self.pipeline.is_locked())


if __name__ == '__main__':
    unittest.main()
