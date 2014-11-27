"""
Module for gocdapi overall configuration
"""

from gocdapi.gobase import GoBase
from gocdapi.custom_exceptions import GoCdApiException

import xml.etree.ElementTree as ET


class Configuration(GoBase):
    """
    Class to manage the configuration of a Go server
    """

    def __init__(self, go_server):
        self.md5 = None
        self.xml_config_data = None
        self.list = []
        path = 'go/api/admin/config.xml'
        super(self.__class__, self).__init__(go_server, path=path)

    def poll(self):
        response = self.get_full_response(self.url)
        self.md5 = response.headers['x-cruise-config-md5']
        self.xml_config_data = response.text

    def push_xml_configuration(self, xml_data):
        data = {'xmlFile': xml_data, 'md5': self.md5}
        return self.pust_to_server(self.url, data=data)

    def pust_to_server(self, url, data):
        return self.do_post(url, data=data)

    def create_pipeline_group(self, group):
        # Check if group exists
        xml_root = ET.fromstring(self.xml_config_data)

        pipeline_group = xml_root.find('pipelines[@group="%s"]' % group)
        if pipeline_group is not None:
            raise GoCdApiException("Pipeline group '%s' already exist." % group)

        # insert xml_data as a child
        pipeline_group_xml_data = '<pipelines group="%s"/>' % group
        xml_root.insert(1, ET.fromstring(pipeline_group_xml_data))

        # push to the server
        self.push_xml_configuration(ET.tostring(xml_root))

    def delete_pipeline_group(self, group_name):
        # Check if group exists
        xml_root = ET.fromstring(self.xml_config_data)

        pipeline_group = xml_root.find('pipelines[@group="%s"]' % group_name)
        if pipeline_group is None:
            raise GoCdApiException("Pipeline group '%s' doesn't exist." % group_name)

        xml_root.remove(pipeline_group)

        # push to the server
        self.push_xml_configuration(ET.tostring(xml_root))

    def create_pipeline_from_xml(self, group, pipeline_xml_data):
        # Check if group exists
        xml_root = ET.fromstring(self.xml_config_data)

        pipeline_group = xml_root.find('pipelines[@group="%s"]' % group)
        if pipeline_group is None:
            raise GoCdApiException("Pipeline group '%s' doesn't exist." % group)

        # insert xml_data as a child
        pipeline_group.append(ET.fromstring(pipeline_xml_data))

        # push to the server
        self.push_xml_configuration(ET.tostring(xml_root))

    def update_pipeline_from_xml(self, group, name, pipeline_xml_data):
        # Check if group exists
        xml_root = ET.fromstring(self.xml_config_data)

        pipeline_group = xml_root.find('pipelines[@group="%s"]' % group)
        if pipeline_group is None:
            raise GoCdApiException("Pipeline group '%s' doesn't exist." % group)

        pipeline = pipeline_group.find('pipeline[@name="%s"]' % name)
        if pipeline is not None:
            pipeline_group.remove(pipeline)

        # insert xml_data as a child
        pipeline_group.append(ET.fromstring(pipeline_xml_data))

        # push to the server
        self.push_xml_configuration(ET.tostring(xml_root))

    def __str__(self):
        return 'Configuration @ %s' % self.go_server.baseurl
