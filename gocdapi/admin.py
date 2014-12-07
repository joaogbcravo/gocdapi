"""
Module for gocdapi Admin class
"""

from gocdapi.gobase import GoBase
from gocdapi.custom_exceptions import GoCdApiException

import xml.etree.ElementTree as ET


class Admin(GoBase):
    """Access admin functions of a Go server

    TODO: Some methods should be refactored.
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
        pass

    def _poll_configuration(self):
        url = self.build_url('config.xml')
        response = self.get_full_response(url)
        md5 = response.headers['x-cruise-config-md5']
        xml_config_data = response.text
        return url, md5, xml_config_data

    def push_xml_configuration(self, url, md5, xml_data):
        data = {'xmlFile': xml_data, 'md5': md5}
        return self.pust_to_server(url, data=data)

    def pust_to_server(self, url, data):
        return self.do_post(url, data=data)

    def create_pipeline_group(self, group):
        url, md5, xml_config_data = self._poll_configuration()
        # Check if group exists
        xml_root = ET.fromstring(xml_config_data)

        pipeline_group = xml_root.find('pipelines[@group="%s"]' % group)
        if pipeline_group is not None:
            raise GoCdApiException("Pipeline group '%s' already exist." % group)

        # insert xml_data as a child
        pipeline_group_xml_data = '<pipelines group="%s"/>' % group
        xml_root.insert(1, ET.fromstring(pipeline_group_xml_data))

        # push to the server
        self.push_xml_configuration(url, md5, ET.tostring(xml_root))

    def delete_pipeline_group(self, group_name):
        url, md5, xml_config_data = self._poll_configuration()
        # Check if group exists
        xml_root = ET.fromstring(xml_config_data)

        pipeline_group = Admin._get_pipeline_group_from_xml(xml_root, group_name)
        xml_root.remove(pipeline_group)

        # push to the server
        self.push_xml_configuration(url, md5, ET.tostring(xml_root))

    def create_pipeline_from_xml(self, group, name, pipeline_xml_data):
        return self.update_pipeline_from_xml(group, name, pipeline_xml_data, False)

    def update_pipeline_from_xml(self, group, name, pipeline_xml_data, new=True):
        url, md5, xml_config_data = self._poll_configuration()
        # Check if group exists
        xml_root = ET.fromstring(xml_config_data)

        pipeline_group = Admin._get_pipeline_group_from_xml(xml_root, group)

        pipeline = pipeline_group.find('pipeline[@name="%s"]' % name)
        if pipeline is not None:
            if new:
                raise GoCdApiException("A pipeline with name '%s' already exist." % name)
            else:
                pipeline_group.remove(pipeline)

        # insert xml_data as a child
        pipeline_group.append(ET.fromstring(pipeline_xml_data))

        # push to the server
        self.push_xml_configuration(url, md5, ET.tostring(xml_root))

    @staticmethod
    def _get_pipeline_group_from_xml(xml_root, group):
        pipeline_group = xml_root.find('pipelines[@group="%s"]' % group)
        if pipeline_group is None:
            raise GoCdApiException("Pipeline group '%s' doesn't exist." % group)
        return pipeline_group
