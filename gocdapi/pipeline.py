"""
Module for gocdapi Pipeline class
"""

from gocdapi.gobase import GoBase
from gocdapi.stage import Stage


class Pipeline(GoBase):
    """
    Class to hold Go Server Pipeline information
    """

    def __init__(self, go_server, data):
        """Inits Pipeline objects.

        Args:
            go_server (Go): A Go object which this agent belongs to.
            data (str): A json string representing the pipeline configuration
        """
        self.stages = []
        super(self.__class__, self).__init__(go_server, data=data)

    def __str__(self):
        """Returns a pretty representation of the object

        Returns:
            str: representation of the object
        """
        return 'Pipeline @ %s' % self.go_server.baseurl

    def schedule(self):
        """Triggers a new instance of the pipeline with the latest revision of all materials

        Will do a POST request to go/api/pipelines/PIPELINE_NAME/schedule
        """
        url = self.build_url('schedule')
        self.do_post(url)

    def release_lock(self):
        """Releases a lock on the pipeline

        Will do a POST request to go/api/pipelines/PIPELINE_NAME/releaseLock
        """
        url = self.build_url('releaseLock')
        self.do_post(url)

    def pause(self, pause_cause):
        """Pauses the pipeline with the given reason.

        Will do a POST request to go/api/pipelines/PIPELINE_NAME/pause

        Args:
            pause_cause (str): reason to pause the pipeline
        """
        url = self.build_url('pause')
        self.do_post(url, {'pauseCause': pause_cause})

    def unpause(self):
        """Unpauses the pipeline.

        Will do a POST request to go/api/pipelines/PIPELINE_NAME/unpause
        """
        url = self.build_url('unpause')
        self.do_post(url)

    def status(self):
        """Gets information about status of pipeline.

        Will do a POST request to go/api/pipelines/PIPELINE_NAME/status

        Return:
            dict: dict based in a JSON containing status information about paused, locked & schedulable.
        """
        url = self.build_url('status')
        return self.get_json_data(url)

    def is_paused(self):
        """Check if pipeline is paused

        Uses status method to get updated data.

        Returns:
            bool: True if paused
        """
        return self.status()["paused"]

    def is_locked(self):
        """Check if pipeline is locked

        Uses status method to get updated data.

        Returns:
            bool: True if locked
        """
        return self.status()["locked"]

    def is_schedulable(self):
        """Check if pipeline is schedulable

        Uses status method to get updated data.

        Returns:
            bool: True if schedulable
        """
        return self.status()["schedulable"]

    def history(self, offset=0):
        """List Pipeline history.

        Will do a POST request to go/api/pipelines/PIPELINE_NAME/history/OFFSET

        Args:
            offset (int): how many instances to skip

        Returns:
            str: JSON representing pipeline history
        """
        url = self.build_url('history/%s' % offset)
        return self.get_json_data(url)

    def _poll(self):
        """Will create and define the attributes of the pipeline.

        Uses _data attribute populated by inherited methods, updating object attributes using the bunch pattern.
        Save stages of pipeline found in the configuration in a container.
        Also sets the pipeline url.
        """
        self.__dict__.update(self._data)
        self.set_self_url('go/api/pipelines/%s/' % self.name)

        self.stages = []
        for item in self._data['stages']:
            stage = Stage(self.go_server, self, item)
            self.stages.append(stage)
