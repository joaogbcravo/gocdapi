"""
System tests for `gocdapi.go` module.
"""
import unittest

from gocdapi_tests.systests.base import BaseSystemTest


class TestAgents(BaseSystemTest):
    def test_delete_agent(self):
        agent = self.go.agents.itervalues().next()
        agent.disable()
        agent.delete()
        self.assertTrue(agent not in self.go.agents)
        self.wait_for_agent_reconnection(agent.uuid)

    def test_enable_disable_agent(self):
        agent = self.go.agents.itervalues().next()
        agent.disable()
        self.assertFalse(agent.is_enabled())

        agent.enable()
        self.assertTrue(agent.is_enabled())


if __name__ == '__main__':
    unittest.main()
