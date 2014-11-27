"""
Module for gocdapi stage
"""

from gocdapi.gobase import GoBase


class Stage(GoBase):
    """
    Class to hold Go Server Stage information
    """

    def __init__(self, go_server, pipeline, data):
        self.pipeline = pipeline
        super(self.__class__, self).__init__(go_server, data=data)

    def poll(self):
        self.__dict__.update(self._data)
        self.set_self_url('go/api/stages/%s/%s/' % (self.pipeline.name, self.name))

    def cancel(self):
        url = self.build_url('cancel')
        self.do_post(url)

    def history(self, offset=0):
        url = self.build_url('history/%s' % offset)
        return self.get_json_data(url)
