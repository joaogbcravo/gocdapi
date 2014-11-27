"""
Module for gocdapi pipeline groups
"""

from gocdapi.pipeline_group import PipelineGroup
from gocdapi.gobase import GoBase

from gocdapi.custom_exceptions import GoCdApiException


class PipelineGroups(GoBase):
    """
    Class to hold the pipelines groups of Go server
    """

    def __init__(self, go_server):
        self._list = []
        path = 'go/api/config/pipeline_groups/'
        super(self.__class__, self).__init__(go_server, path=path)

    def poll(self):
        data = self.load_json_data(self._data)
        for item in data:
            pipeline_group = PipelineGroup(self.go_server, item)
            self._list.append(pipeline_group)

    def iterkeys(self):
        for pipeline_group in self._list:
            yield pipeline_group.name

    def iteritems(self):
        for pipeline_group in self._list:
            yield pipeline_group.name, pipeline_group

    def keys(self):
        return list(self.iterkeys())

    def __contains__(self, group_name):
        return group_name in self.keys()

    def __getitem__(self, group_name):
        self_as_dict = dict(self.iteritems())
        if group_name in self_as_dict:
            return self_as_dict[group_name]
        else:
            raise GoCdApiException("No pipeline_group with the name %s ." % group_name)

    def __iter__(self):
        return self.iteritems()

    def __len__(self):
        return len(self.keys())

    def __str__(self):
        return 'Pipeline Group @ %s' % self.go_server.baseurl
