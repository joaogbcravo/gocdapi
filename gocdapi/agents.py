"""
Module for gocdapi agents
"""

from gocdapi.agent import Agent
from gocdapi.gobase import GoBase

from gocdapi.custom_exceptions import GoCdApiException


class Agents(GoBase):
    """
    Class to hold information on a collection of agents
    """

    def __init__(self, go_server):
        self._list = []
        super(self.__class__, self).__init__(go_server, path='go/api/agents/')

    def poll(self):
        data = self.load_json_data(self._data)
        for item in data:
            agent = Agent(self.go_server, item)
            self._list.append(agent)

    def iterkeys(self):
        for agent in self._list:
            yield agent.uuid

    def iteritems(self):
        for agent in self._list:
            yield agent.uuid, agent

    def keys(self):
        return list(self.iterkeys())

    def __contains__(self, uuid):
        return uuid in self.keys()

    def __getitem__(self, uuid):
        self_as_dict = dict(self.__iter__())
        if uuid in self_as_dict:
            return self_as_dict[uuid]
        else:
            raise GoCdApiException("No agent with uuid %s connected to server." % uuid)

    def __iter__(self):
        return self.iteritems()

    def __len__(self):
        return len(self.keys())

    def __str__(self):
        return 'Agents @ %s' % self.go_server.baseurl
