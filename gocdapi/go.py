"""
Module for gocdapi Go object
"""

from gocdapi.agents import Agents
from gocdapi.configuration import Configuration
from gocdapi.pipeline_groups import PipelineGroups


class Go(object):
    """
    Represents a Go environment.
    """
    def __init__(self, baseurl, username=None, password=None):
        self.baseurl = baseurl
        self.username = username
        self.password = password

    @property
    def agents(self):
        return Agents(self)

    @property
    def pipeline_groups(self):
        return PipelineGroups(self)

    @property
    def configuration(self):
        return Configuration(self)

    def create_pipeline(self, group, config):
        return self.configuration.create_pipeline_from_xml(group, config)

    def create_pipeline_group(self, group_name):
        return self.configuration.create_pipeline_group(group_name)

    def delete_pipeline_group(self, group_name):
        return self.configuration.delete_pipeline_group(group_name)

    def pipeline_exist(self, name):
        for _, pipeline_group in self.pipeline_groups:
            if any(name == pipe_name for pipe_name, pipe in pipeline_group):
                return True
        return False
