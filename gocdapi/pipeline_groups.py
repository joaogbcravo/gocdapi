"""
Module for gocdapi PipelineGroups class
"""

from gocdapi.pipeline_group import PipelineGroup
from gocdapi.gobase import GoBase

from gocdapi.custom_exceptions import GoCdApiException


class PipelineGroups(dict, GoBase):
    """
    Class to hold information on a collection of PipelineGroups objects

    This class acts like a dictionary
    """
    def __init__(self, go_server):
        """Inits PipelineGroups objects.

        Args:
            go_server (Go): A Go object which this PipelineGroups belongs to.
        """
        dict.__init__(self)
        GoBase.__init__(self, go_server, path='go/api/config/pipeline_groups/')

    def __getitem__(self, group_name):
        """Custom __getitem__ method

        Overrides the default __getitem__ method from dict class to raise a custom exception when the item doen't exist

        Args:
            group_name (str): the name of group of pipelines that it is looking for

        Return:
            PipelineGroup: the PipelineGroups with the 'group_name' found

        Raises:
            GoCdApiException: When no PipelineGroups with the 'group_name' was found
        """
        try:
            self.repoll()
            return dict.__getitem__(self, group_name)
        except KeyError:
            raise GoCdApiException("No PipelineGroup with name %s connected to server." % group_name)

    def __str__(self):
        """Returns a pretty representation of the object

        Returns:
            str: representation of the object
        """
        return 'Pipelines Groups @ %s' % self.go_server.baseurl

    def _poll(self):
        """Will get information of all PipelineGroups in the Go server.

        Uses _data attribute populated by inherited methods, creating PipelineGroups objects with that information.
        The PipelineGroups's objects are saved as a pair (key,value) with their name as key.
        """
        data = self.load_json_data(self._data)
        for item in data:

            pipeline_group = PipelineGroup(self.go_server, item)
            self[pipeline_group.name] = pipeline_group
