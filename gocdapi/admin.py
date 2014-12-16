"""
Module for gocdapi Admin class
"""

from gocdapi.gobase import GoBase
from gocdapi.utils.config_xml import ConfigXML


class Admin(GoBase):
    """
    Access admin functions of a Go server
    """
    def __init__(self, go_server):
        """Inits Admin objects.

        Args:
            go_server (Go): A Go object which this agent belongs to.
        """
        path = 'go/api/admin/'
        super(self.__class__, self).__init__(go_server, path=path, poll=False)

    def __str__(self):
        """Returns a pretty representation of the object

        Returns:
            str: representation of the object
        """
        return 'Admin Control @ %s' % self.go_server.baseurl

    def reload_command_repo_cache(self):
        """Reloads the command repository cache on the Go server.

        Will do a POST request to go/api/admin/command-repo-cache/reload

        Returns:
            str: The text response to the POST request
        """
        url = self.build_url('command-repo-cache/reload')
        return self.do_post(url)

    def _poll(self):
        """ Do nothing

        Should be implemented to not be raised a NotImplementedError
        """
        pass

    def _poll_configuration(self):
        """ Polls Go configuration

        Will do a GET request to go/api/admin/config.xml

        Returns:
            tuple (string, string): md5 of the config when polled, config xml data
        """
        url = self.build_url('config.xml')
        response = self.get_full_response(url)
        md5 = response.headers['x-cruise-config-md5']
        xml_config_data = response.text
        return md5, xml_config_data

    def push_xml_configuration(self, md5, xml_data):
        """ Push a xml data as config to the Go server

        Args:
            md5 (string): md5 when config was pulled
            xml_data(string): new configuration to be pushed to the server

        Will do a POST request to go/api/admin/config.xml
        """
        url = self.build_url('config.xml')
        data = {'xmlFile': xml_data, 'md5': md5}
        self.do_post(url, data=data)

    def create_pipeline_group(self, group_name):
        """ Creates a pipeline group in the Go Server

        Will do a POST request to go/api/admin/config.xml

        Args:
            group_name(str): name of the group to be created
        """
        md5, xml_config_data = self._poll_configuration()

        config_xml = ConfigXML(xml_config_data)
        config_xml.create_pipeline_group(group_name)

        self.push_xml_configuration(md5, config_xml)

    def delete_pipeline_group(self, group_name):
        """ Deletes a pipeline group in the Go Server

        Will do a POST request to go/api/admin/config.xml

        Args:
            group_name(str): name of the group to be deleted
        """
        md5, xml_config_data = self._poll_configuration()

        config_xml = ConfigXML(xml_config_data)
        config_xml.remove_pipeline_group(group_name)

        self.push_xml_configuration(md5, config_xml)

    def update_pipeline_from_xml(self, pipeline_xml_data):
        """ Updates a pipeline in the Go Server

        Will do a POST request to go/api/admin/config.xml

        Args:
            pipeline_xml_data(str): xml data of pipeline to be updated
        """
        md5, xml_config_data = self._poll_configuration()

        config_xml = ConfigXML(xml_config_data)
        config_xml.update_pipeline_from_xml_string(pipeline_xml_data)

        self.push_xml_configuration(md5, config_xml)

    def create_pipeline_from_xml(self, group_name, pipeline_xml_data):
        """ Creates a pipeline inside a group in the Go Server

        Will do a POST request to go/api/admin/config.xml

        Args:
            group_name(str): name of pipeline group which pipeline should belong
            pipeline_xml_data(str): xml data of pipeline to be updated
        """
        md5, xml_config_data = self._poll_configuration()

        config_xml = ConfigXML(xml_config_data)
        config_xml.add_pipeline_from_xml_string_in_group(group_name, pipeline_xml_data)

        self.push_xml_configuration(md5, config_xml)
