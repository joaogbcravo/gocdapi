"""
Module for gocdapi pipeline
"""

from gocdapi.gobase import GoBase
from gocdapi.stage import Stage


class Pipeline(GoBase):
    """
    Class to hold Go Server Pipeline information
    """

    def __init__(self, go_server, data):
        self.stages = []
        super(self.__class__, self).__init__(go_server, data=data)

    def poll(self):
        self.__dict__.update(self._data)
        self.set_self_url('go/api/pipelines/%s/' % self.name)

        self.stages = []
        for item in self._data['stages']:
            stage = Stage(self.go_server, self, item)
            self.stages.append(stage)

    def schedule(self, data=None):
        url = self.build_url('schedule')
        self.do_post(url, data)

    def release_lock(self):
        url = self.build_url('releaseLock')
        self.do_post(url)

    def pause(self, pauseCause):
        url = self.build_url('pause')
        self.do_post(url, {'pauseCause': pauseCause})

    def unpause(self):
        url = self.build_url('unpause')
        self.do_post(url)

    def history(self, offset=0):
        url = self.build_url('history/%s' % offset)
        return self.get_json_data(url)

    def __str__(self):
        return 'Pipeline @ %s' % self.go_server.baseurl
