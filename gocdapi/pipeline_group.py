"""
Module for gocdapi pipeline group
"""

from gocdapi.gobase import GoBase
from gocdapi.pipeline import Pipeline


class PipelineGroup(GoBase):
    """
    Class to hold information on pipeline group of Go Server
    """

    def __init__(self, go_server, data):
        self.pipelines = []
        super(self.__class__, self).__init__(go_server, data=data)

    def poll(self):
        pipelines_data = self._data.pop('pipelines')
        self.__dict__.update(self._data)

        for item in pipelines_data:
            pipeline = Pipeline(self.go_server, item)
            self.pipelines.append(pipeline)

    def get_pipelines(self):
        return self.pipelines

    def __contains__(self, pipeline_name):
        return pipeline_name in self.pipelines
