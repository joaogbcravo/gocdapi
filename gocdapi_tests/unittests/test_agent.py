import mock

import unittest

from gocdapi.go import Go
from gocdapi.agents import Agents
from gocdapi.agent import Agent

from gocdapi.custom_exceptions import GoCdApiException

class TestAgents(unittest.TestCase):

    DATA0 = {
        "resources": [],
        "sandbox": "/var/lib/go-agent",
        "os": "Linux",
        "free_space": "35.7 GB",
        "ip_address": "127.0.0.1",
        "agent_name": "vagrant-ubuntu-trusty-32",
        "environments":[],
        "status":"Idle",
        "uuid": "a8b7c2b4-3986-476a-a797-abb3a065587e",
        "build_locator": ""
    }

    def setUp(self):
        self.baseurl = 'http://localhost:8080'
        self.go = Go(self.baseurl)
        self.agent = Agent(self.go, self.DATA0)

    def test_agent_enabled(self):
        self.assertTrue(self.agent.is_enabled())
        self.assertFalse(self.agent.is_disabled())

    def test_agent_disabled(self):
        self.agent.status = "Disabled"
        self.assertFalse(self.agent.is_enabled())
        self.assertTrue(self.agent.is_disabled())

    def test_repr(self):
        print repr(self.agent)

if __name__ == '__main__':
    unittest.main()