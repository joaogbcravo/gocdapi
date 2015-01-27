"""
Module for gocdapi PipelineGroup class
"""

from gocdapi.gobase import GoBase
from gocdapi.pipeline import Pipeline

from gocdapi.custom_exceptions import GoCdApiException


class PipelineGroup(GoBase):
    """
    Class to hold information of PipelineGroup objects

    This class can act like a read-only iterable.
    """

    def __init__(self, go_server, data):
        self._pipelines = {}
        self.name = ""
        GoBase.__init__(self, go_server, data=data)

    def __iter__(self):
        """Iter over pipelines from this pipeline group

        Forwards this method to the _pipelines attribute method with the same name.

        Return:
            iterable: pipelines
        """
        return self._pipelines.__iter__()

    def iteritems(self):
        """Iter over pipelines from this pipeline group

        Forwards this method to the _pipelines attribute method with the same name.

        Return:
            iterable: pipelines
        """
        return self._pipelines.iteritems()

    def __len__(self):
        """Get the number of pipelines that this pipeline group have

        Forwards this method to the _pipelines attribute method with the same name.

        Return:
            int: number of pipelines
        """
        return self._pipelines.__len__()

    def __getitem__(self, name):
        """Get a pipeline from this pipeline group with the 'name'

        Forwards this method to the _pipelines attribute method with the same name.

        Args:
            name (str): the name of the pipeline that it is looking for

        Return:
            Pipeline: the pipeline with the 'name' found

        Raises:
            GoCdApiException: When no pipeline with the 'name' was found
        """
        try:
            return self._pipelines.__getitem__(name)
        except KeyError:
            raise GoCdApiException("No pipeline with the name %s ." % name)

    def __str__(self):
        """Returns a pretty representation of the object

        Returns:
            str: representation of the object
        """
        return 'Pipeline Group @ %s' % self.go_server.baseurl

    def list_of_pipelines(self):
        """Get all pipelines for this pipeline group in a list container.
        """
        return self._pipelines.values()

    def _poll(self):
        """Will store the pipelines of this group in a hash

        Uses _data attribute populated by inherited methods, creating Pipeline objects with that information.
        The Pipeline's objects are saved as a pair (key,value) with their name as key.
        """
        self.name = self._data["name"]
        for item in self._data['pipelines']:
            pipeline = Pipeline(self.go_server, item)
            self._pipelines[pipeline.name] = pipeline
