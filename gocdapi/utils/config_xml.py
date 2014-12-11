"""
Module for gocdapi ConfigXML Util class
"""
from gocdapi.custom_exceptions import GoCdApiException

import xml.etree.ElementTree as ET

class ConfigXML(ET.ElementTree):
    """TODO
    """
    def __init__(self, xml_config_data):
        super(self.__class__, self).__init__(ET.fromstring(xml_config_data))

    def __str__(self):
        return ET.tostring(self.getroot())

    def get_pipeline(self, pipeline_name):
        return self.find('*/pipeline[@name="%s"]' % pipeline_name)

    def get_pipeline_group(self, group_name):
        return self.find('pipelines[@group="%s"]' % group_name)

    def get_pipeline_parent_group(self, pipeline_name):
        return self.find('*/pipeline[@name="%s"]/..' % pipeline_name)

    def add_pipeline_element_in_group(self, group_name, pipeline_element):
        if self.get_pipeline(pipeline_element.get("name")) is not None:
            raise GoCdApiException("Pipeline '%s' already exists." % pipeline_element.get("name"))
        group_element = self.get_pipeline_group(group_name)
        if group_element is None:
            raise GoCdApiException("Pipeline group '%s' doesn't exist." % group_name)
        group_element.append(pipeline_element)

    def remove_pipeline(self, pipeline_name):
        pipeline_element = self.get_pipeline(pipeline_name)
        if pipeline_element is None:
            raise GoCdApiException("Pipeline '%s' doesn't exist." % pipeline_name)

        group_element = self.get_pipeline_parent_group(pipeline_name)
        group_element.remove(pipeline_element)

    def update_pipeline_element(self, new_pipeline_element):
        pipeline_name = new_pipeline_element.get("name")
        pipeline_element = self.get_pipeline(pipeline_name)
        if pipeline_element is None:
            raise GoCdApiException("Pipeline '%s' doesn't exist." % pipeline_name)

        group_element = self.get_pipeline_parent_group(pipeline_name)
        group_element.remove(pipeline_element)
        group_element.append(new_pipeline_element)


    def add_pipeline_group_element(self, group_element):
        if self.get_pipeline_group(group_element.get('group')) is not None:
            raise GoCdApiException("Pipeline group '%s' already exists." % group_element.get('group'))

        self.getroot().insert(1, group_element)

    def remove_pipeline_group(self, group_name):
        group_element = self.get_pipeline_group(group_name)
        if group_element is None:
            raise GoCdApiException("Pipeline group '%s' doesn't exist." % group_name)
        print dir(self)
        self.getroot().remove(group_element)

    def create_pipeline_group(self, group_name):
        if self.get_pipeline_group(group_name) is not None:
            raise GoCdApiException("Pipeline group '%s' already exists." % group_name)
        pipeline_group_element = ET.fromstring('<pipelines group="%s"/>' % group_name)
        self.add_pipeline_group_element(pipeline_group_element)

    def update_pipeline_from_xml_string(self, new_pipeline_config_xml):
        new_pipeline_element = ET.fromstring(new_pipeline_config_xml)
        self.update_pipeline_element(new_pipeline_element)

    def update_pipeline_from_xml_string(self, group_name, new_pipeline_config_xml):
        new_pipeline_element = ET.fromstring(new_pipeline_config_xml)
        self.add_pipeline_element_in_group(group_name, new_pipeline_element)
