import mock

import unittest

from gocdapi.go import Go
from gocdapi.agents import Agents
from gocdapi.agent import Agent

from gocdapi.custom_exceptions import GoCdApiException

class TestAgents(unittest.TestCase):

    DATA0 = """
        [
            {
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
        ]
    """

    @mock.patch.object(Agents, 'get_data')
    def setUp(self, get_data_agents):
        get_data_agents.return_value = self.DATA0
        self.baseurl = 'http://localhost:8080'

        go = Go(self.baseurl)
        self.agents = go.agents

    def test_agent_exists(self):
        uuid = 'a8b7c2b4-3986-476a-a797-abb3a065587e'
        self.assertIn(uuid, self.agents)

        uuid = 'a8b7c2b4-3986-476a-a797-false-uuid'
        self.assertNotIn(uuid, self.agents)

    def test_check_URL(self):
        self.assertEquals(self.agents.url, '%s/go/api/agents/' % self.baseurl)

    def test_get_agent(self):
        uuid = 'a8b7c2b4-3986-476a-a797-abb3a065587e'
        agent = self.agents[uuid]
        self.assertIsInstance(agent, Agent)

        uuid = 'a8b7c2b4-3986-476a-a797-false-uuid'
        with self.assertRaises(GoCdApiException):
            self.agents[uuid]

    def test_agents_iterable(self):
        for agent in self.agents.values():
            self.assertIsInstance(agent, Agent)

    def test_repr(self):
        self.assertEquals(str(self.agents), 'Agents @ %s' % self.baseurl)

    def test_there_is_agents(self):
        self.assertTrue(self.agents)


if __name__ == '__main__':
    unittest.main()