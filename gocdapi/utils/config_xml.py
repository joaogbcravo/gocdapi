"""
Module for gocdapi ConfigXML Util class
"""
import xml.etree.ElementTree as ET

from gocdapi.custom_exceptions import GoCdApiException


class ConfigXML(ET.ElementTree):
    """ Helper class to handle pipelines (add, remove, update) from the Go Server configuration file.
    """
    def __init__(self, xml_config_data):
        """ Inits the ConfigXML object

        This class inherits from the xml.etree.ElementTree, so it can be used functions like find and find_all on the
        object.

        Args:
            xml_config_data (str): Go Server xml configuration
        """
        super(self.__class__, self).__init__(ET.fromstring(xml_config_data))

    def __str__(self):
        """ Converts the ConfigXML to a string
        """
        return ET.tostring(self.getroot())

    def get_pipeline(self, pipeline_name):
        """ Gets a pipeline Element

        Args:
            pipeline_name (str): pipeline name to find

        Returns:
            ElementTree.Element: pipeline found or None
        """
        return self.find('*/pipeline[@name="%s"]' % pipeline_name)

    def get_pipeline_group(self, group_name):
        """ Gets a pipeline group Element

        Args:
            group_name (str): pipeline group name to find

        Returns:
            ElementTree.Element: pipeline group found or None
        """
        return self.find('pipelines[@group="%s"]' % group_name)

    def get_pipeline_parent_group(self, pipeline_name):
        """ Gets a pipeline group Element parent of a pipeline

        Args:
            pipeline_name (str): pipeline name child of the parent group to get

        Returns:
            ElementTree.Element: pipeline group found or None
        """
        return self.find('*/pipeline[@name="%s"]/..' % pipeline_name)

    def add_pipeline_element_in_group(self, group_name, pipeline_element):
        """ Adds a pipeline Element to a pipeline group Element

        Args:
            group_name (str): pipeline group where will be inserted the pipeline
            pipeline_element (ElementTree.Element): pipeline to be added

        Raises:
            GoCdApiException: When a pipeline with the same name of pipeline_element already exists
            GoCdApiException: When no pipeline group with the group_name exists
        """
        if self.get_pipeline(pipeline_element.get("name")) is not None:
            raise GoCdApiException("Pipeline '%s' already exists." % pipeline_element.get("name"))
        group_element = self.get_pipeline_group(group_name)
        if group_element is None:
            raise GoCdApiException("Pipeline group '%s' doesn't exist." % group_name)
        group_element.append(pipeline_element)

    def remove_pipeline(self, pipeline_name):
        """ Removes a pipeline from the configuration

        Args:
            pipeline_name (str): name of the pipeline to be removed

        Returns:
            ElementTree.Element: pipeline group parent of the removed pipeline

        Raises:
            GoCdApiException: When no pipeline with the pipeline_name exists
        """
        pipeline_element = self.get_pipeline(pipeline_name)
        if pipeline_element is None:
            raise GoCdApiException("Pipeline '%s' doesn't exist." % pipeline_name)

        group_element = self.get_pipeline_parent_group(pipeline_name)
        group_element.remove(pipeline_element)
        return group_element

    def update_pipeline_element(self, pipeline_element):
        """ Replaces an existent pipeline element by a new one

        Args:
            pipeline_element (str): new pipeline Element to replace the existent one
        """
        pipeline_name = pipeline_element.get("name")
        group_element = self.remove_pipeline(pipeline_name)
        group_element.append(pipeline_element)

    def add_pipeline_group_element(self, group_element):
        """ Adds a pipeline group Element to the configuration

        Args:
            pipeline_element (ElementTree.Element): pipeline group to be added

        Raises:
            GoCdApiException: When a pipeline group with the group_name already exists
        """
        if self.get_pipeline_group(group_element.get('group')) is not None:
            raise GoCdApiException("Pipeline group '%s' already exists." % group_element.get('group'))
        self.getroot().insert(1, group_element)

    def remove_pipeline_group(self, group_name):
        """ Removes a pipeline group from the configuration

        Args:
            group_name (str): name of the pipeline group to be removed

        Raises:
            GoCdApiException: When no pipeline with the pipeline_name exists
        """
        group_element = self.get_pipeline_group(group_name)
        if group_element is None:
            raise GoCdApiException("Pipeline group '%s' doesn't exist." % group_name)
        self.getroot().remove(group_element)

    def create_pipeline_group(self, group_name):
        """ Creates an empty pipeline group Element and adds it to the configuration

        Args:
            group_name (str): name of the pipeline group to be created

        Raises:
            GoCdApiException: When a pipeline group with the group_name already exists
        """
        pipeline_group_element = ET.fromstring('<pipelines group="%s"/>' % group_name)
        self.add_pipeline_group_element(pipeline_group_element)

    def update_pipeline_from_xml_string(self, pipeline_config_xml):
        """ Replaces an existent pipeline element by a new one created from a xml string

        Args:
            pipeline_config_xml (str): xml string of the pipeline Element to replace the existent one
        """
        pipeline_element = ET.fromstring(pipeline_config_xml)
        self.update_pipeline_element(pipeline_element)

    def add_pipeline_from_xml_string_in_group(self, group_name, pipeline_config_xml):
        """ Adds a pipeline Element, created from a xml string, to a pipeline group Element

        Args:
            group_name (str): pipeline group where will be inserted the pipeline
            pipeline_config_xml (str): xml string of the pipeline Element to be added
        """
        pipeline_element = ET.fromstring(pipeline_config_xml)
        self.add_pipeline_element_in_group(group_name, pipeline_element)
