"""
Module for gocdapi pipeline groups
"""

from gocdapi.pipeline_group import PipelineGroup
from gocdapi.gobase import GoBase


class PipelineGroups(GoBase):
    """
    Class to hold the pipelines groups of Go server
    """

    def __init__(self, go_server):
        self.list = []
        path = 'go/api/config/pipeline_groups/'
        super(self.__class__, self).__init__(go_server, path=path)

    def poll(self):
        data = self.load_json_data(self._data)
        for item in data:
            pipeline_group = PipelineGroup(self.go_server, item)
            self.list.append(pipeline_group)

    def get_all(self):
        return self.list

    def exist(self, name):
        return any(name == group.name for group in self.list)

    def pipeline_exist(self, name):
        for group in self.get_all():
            if any(name == pipe.name for pipe in group.get_pipelines()):
                return True
        return False

    def __contains__(self, pipeline_group_name):
        return any(pipeline_group_name == group.name for group in self.list)
