"""
Module for gocdapi Agent class
"""

from gocdapi.gobase import GoBase


class Agent(GoBase):
    """
    Class to hold Go Server Agent information
    """

    def __init__(self, go_server, data):
        """Inits Agent objects.

        Args:
            go_server (Go): A Go object which this agent belongs to.
            data (str): A json string representing the agent configuration
        """
        self._data = None
        super(self.__class__, self).__init__(go_server, data=data)

    def __str__(self):
        """Returns a pretty representation of the object

        Returns:
            str: representation of the object
        """
        return 'Agent @ %s' % self.go_server.baseurl

    def repoll_from_agents_url(self):
        """Request to the server new agents configuration to upload agent object

        Because Go Server haven't any API to return a single Agent configuration, this function will do a GET request
        to get information about all the agents, and then update the actual object with the right information.
        """
        agents_data = self.get_json_data(self.build_url_with_base('go/api/agents'))
        self._data = next(data for (index, data) in enumerate(agents_data) if data["uuid"] == self.uuid)
        self.__dict__.update(self._data)

    def is_enabled(self):
        """Check if agent is enabled

        Does a repoll first to get updated data.

        Returns:
            bool: True if enabled
        """
        self.repoll_from_agents_url()
        return self.status != "Disabled"

    def enable(self):
        """Enables the agent

        Will do a POST request to go/api/agents/UUID/enable
        """
        url = self.build_url('enable')
        self.do_post(url)

    def disable(self):
        """Disables the agent

        Will do a POST request to go/api/agents/UUID/disable
        """
        url = self.build_url('disable')
        self.do_post(url)

    def delete(self):
        """Deletes the agent

        Will do a POST request to go/api/agents/UUID/delete
        """
        url = self.build_url('delete')
        self.do_post(url)

    def job_run_history(self, offset=0):
        """Gets the history of the jobs run on the agent

        Go server returns 10 instances at a time, sorted in reverse order.
        You can use offset argument which tells the API how many instances to skip.

        Will do a GET request to go/api/agents/UUID/job_run_history/OFFSET

        Args:
            offset (int): how many instances to skip

        Returns:
            str: JSON representing job history

        """
        url = self.build_url('job_run_history/%s' % offset)
        return self.get_json_data(url)

    def _poll(self):
        """Will create and define the attributes of the agent.

        Uses _data attribute populated by inherited methods, updating object attributes using the bunch pattern.
        Also sets the agent url.
        """
        self.__dict__.update(self._data)
        self.set_self_url('go/api/agents/%s/' % self.uuid)
