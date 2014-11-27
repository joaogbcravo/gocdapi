"""
Module for gocdapi agent
"""

from gocdapi.gobase import GoBase


class Agent(GoBase):
    """
    Class to hold Go Server Agent information
    """

    def __init__(self, go_server, data):
        self._data = None
        super(self.__class__, self).__init__(go_server, data=data)

    def poll(self):
        self.__dict__.update(self._data)
        self.set_self_url('go/api/agents/%s/' % self.uuid)

    def repoll_from_agents_url(self):
        agents_data = self.get_json_data(self.build_url_with_base('go/api/agents'))
        self._data = next(data for (index, data) in enumerate(agents_data) if data["uuid"] == self.uuid)
        self.__dict__.update(self._data)

    def is_disabled(self):
        return self.status == "Disabled"

    def is_enabled(self):
        return self.status != "Disabled"

    def enable(self):
        url = self.build_url('enable')
        self.do_post(url)
        self.repoll_from_agents_url()

    def disable(self):
        url = self.build_url('disable')
        self.do_post(url)
        self.repoll_from_agents_url()

    def delete(self):
        url = self.build_url('delete')
        self.do_post(url)

    def job_run_history(self, offset=0):
        url = self.build_url('job_run_history/%s' % offset)
        return self.get_json_data(url)

    def __str__(self):
        return 'Agent @ %s' % self.go_server.baseurl
