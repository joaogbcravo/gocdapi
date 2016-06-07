import unittest

import mock

from gocdapi.agent import Agent
from gocdapi.go import Go


class TestAgent(unittest.TestCase):
    DATA0 = {
        "resources": [],
        "sandbox": "/var/lib/go-agent",
        "os": "Linux",
        "free_space": "35.7 GB",
        "ip_address": "127.0.0.1",
        "agent_name": "vagrant-ubuntu-trusty-32",
        "environments": [],
        "status": "Idle",
        "uuid": "a8b7c2b4-3986-476a-a797-abb3a065587e",
        "build_locator": ""
    }

    def setUp(self):
        self.baseurl = 'http://localhost:8080'
        self.go = Go(self.baseurl)
        self.agent = Agent(self.go, self.DATA0)

    @mock.patch.object(Agent, 'get_json_data')
    def test_agent_is_enabled_or_disabled(self, agent_get_json_data):
        agent_get_json_data.return_value = [self.DATA0]
        self.assertTrue(self.agent.is_enabled())

        self.DATA0['status'] = "Disabled"
        agent_get_json_data.return_value = [self.DATA0]
        self.assertFalse(self.agent.is_enabled())

    def test_repr(self):
        self.assertEquals(str(self.agent), 'Agent @ %s' % self.baseurl)


if __name__ == '__main__':
    unittest.main()
