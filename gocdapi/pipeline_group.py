"""
Module for gocdapi pipeline group
"""

from gocdapi.gobase import GoBase
from gocdapi.pipeline import Pipeline

from gocdapi.custom_exceptions import GoCdApiException


class PipelineGroup(GoBase):
    """
    Class to hold information on pipeline group of Go Server
    """

    def __init__(self, go_server, data):
        self.pipelines = []
        super(self.__class__, self).__init__(go_server, data=data)

    def poll(self):
        self.__dict__.update(self._data)
        self.pipelines = []
        for item in self._data['pipelines']:
            pipeline = Pipeline(self.go_server, item)
            self.pipelines.append(pipeline)

    def iterkeys(self):
        for pipeline in self.pipelines:
            yield pipeline.name

    def iteritems(self):
        for pipeline in self.pipelines:
            yield pipeline.name, pipeline

    def keys(self):
        return list(self.iterkeys())

    def __contains__(self, name):
        return name in self.keys()

    def __getitem__(self, name):
        self_as_dict = dict(self.iteritems())
        if name in self_as_dict:
            return self_as_dict[name]
        else:
            raise GoCdApiException("No pipeline with the name %s ." % name)

    def __iter__(self):
        return self.iteritems()

    def __len__(self):
        return len(self.keys())

    def __str__(self):
        return 'Pipeline @ %s' % self.go_server.baseurl
