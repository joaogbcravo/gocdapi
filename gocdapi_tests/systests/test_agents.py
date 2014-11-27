'''
System tests for `gocdapi.go` module.
'''
import unittest

from gocdapi_tests.systests.base import BaseSystemTest
from gocdapi_tests.systests.pipeline_configs import EMPTY_PIPELINE
from gocdapi_tests.test_utils.random_strings import random_string

import time

class TestAgents(BaseSystemTest):

    def test_delete_agent(self):
        return
        _, agent = self.go.agents.iteritems().next()
        agent.disable()
        agent.delete()
        self.assertTrue(agent not in self.go.agents)
        print
        for _ in xrange(3):
            print "Waiting for agent %s connect" % agent.uuid
            time.sleep(10)
            if agent.uuid in self.go.agents:
                return
        raise Exception("Agent couldn't connect again to the server")

    def test_enable_disable_agent(self):
        _, agent = self.go.agents.iteritems().next()

        agent.disable()
        self.assertTrue(agent.is_disabled())
        self.assertFalse(agent.is_enabled())

        agent.enable()
        self.assertTrue(agent.is_enabled())
        self.assertFalse(agent.is_disabled())

    def test_job_run_history(self):
        _, agent = self.go.agents.iteritems().next()
        agent.job_run_history()


if __name__ == '__main__':
    unittest.main()
