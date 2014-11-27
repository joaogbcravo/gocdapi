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
        stages_data = self._data.pop('stages')
        self.__dict__.update(self._data)

        self.set_self_url('go/api/pipelines/%s/' % self.name)

        for item in stages_data:
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
