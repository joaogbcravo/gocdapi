"""
Module for gocdapi Agents class
"""

from gocdapi.agent import Agent
from gocdapi.gobase import GoBase

from gocdapi.custom_exceptions import GoCdApiException


class Agents(dict, GoBase):
    """
    Class to hold information on a collection of Agent objects

    This class acts like a dictionary
    """

    def __init__(self, go_server):
        """Inits Agents objects.

        Args:
            go_server (Go): A Go object which this agent belongs to.
        """
        dict.__init__(self)
        GoBase.__init__(self, go_server, path='go/api/agents/')

    def __getitem__(self, uuid):
        """Custom __getitem__ method

        Overrides the default __getitem__ method from dict class to raise a custom exception when the item doen't exist

        Args:
            uuid (str): the uuid of the Agent that it is looking for

        Return:
            Agent: the Agent with the 'uuid' found

        Raises:
            GoCdApiException: When no Agent with the 'uuid' was found
        """
        try:
            return dict.__getitem__(self, uuid)
        except KeyError:
            raise GoCdApiException("No agent with uuid %s connected to server." % uuid)

    def __str__(self):
        """Returns a pretty representation of the object

        Returns:
            str: representation of the object
        """
        return 'Agents @ %s' % self.go_server.baseurl

    def _poll(self):
        """Will get information of all agents in the Go server.

        Uses _data attribute populated by inherited methods, creating Agent objects with that information.
        The Agent's objects are saved as a pair (key,value) with their uuid as key.
        """
        data = self.load_json_data(self._data)
        for item in data:
            agent = Agent(self.go_server, item)
            self[agent.uuid] = agent
