"""
Module for gocdapi Stage class
"""

from gocdapi.gobase import GoBase


class Stage(GoBase):
    """
    Class to hold Go Server Stage information
    """

    def __init__(self, go_server, pipeline, data):
        """Inits Stage objects.

        Args:
            go_server (Go): A Go object which this Stage belongs to.
            pipeline (Pipeline): A Go pipeline which this Stage belongs to.
            data (str): A json string representing the Stage configuration
        """
        self.pipeline = pipeline
        super(self.__class__, self).__init__(go_server, data=data)

    def __str__(self):
        """Returns a pretty representation of the object

        Returns:
            str: representation of the object
        """
        return 'Stage @ %s' % self.go_server.baseurl

    def cancel(self):
        """Cancels the stage

        Will do a POST request to go/api/stages/PIPELINE_NAME/STAGE_NAME/cancel
        """
        url = self.build_url('cancel')
        self.do_post(url)

    def history(self, offset=0):
        """Gets the history of the Stage

        Go server returns 10 instances at a time, sorted in reverse order.
        You can use offset argument which tells the API how many instances to skip.

        Will do a GET request to go/api/stages/PIPELINE_NAME/STAGE_NAME/history/OFFSET

        Args:
            offset (int): how many instances to skip

        Returns:
            str: JSON representing job history

        """
        url = self.build_url('history/%s' % offset)
        return self.get_json_data(url)

    def _poll(self):
        """Will create and define the attributes of the stage.

        Uses _data attribute populated by inherited methods, updating object attributes using the bunch pattern.
        Also sets the stage url.
        """
        self.__dict__.update(self._data)
        self.set_self_url('go/api/stages/%s/%s/' % (self.pipeline.name, self.name))
