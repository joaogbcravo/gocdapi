import unittest
import xml.etree.ElementTree as ET

from gocdapi.admin import ConfigXML
from gocdapi.custom_exceptions import GoCdApiException


class TestConfigXML(unittest.TestCase):
    DATA0 = """

        <cruise >
          <server artifactsdir="artifacts" commandRepositoryLocation="default"
            serverId="4f2a09d1-bfc1-4b67-acd9-a33cc80d02de" />
          <pipelines group="Group_1">
            <pipeline name="Pipeline_1">
            </pipeline>
          </pipelines>
          <pipelines group="Group_2">
            <pipeline name="Pipeline_2">
            </pipeline>
            <pipeline name="Pipeline_3">
            </pipeline>
            <pipeline name="Pipeline_4">
            </pipeline>
          </pipelines>
          <pipelines group="Group_3" />
          <templates>
          </templates>
          <agents>
          </agents>
        </cruise>
    """

    DATA1 = """
        <pipeline name="SuperPipeline">
        </pipeline>
    """

    DATA2 = """
        <pipeline name="Pipeline_4" arg="newarg">
        </pipeline>
    """

    DATA3 = """
        <pipeline name="Pipeline_4">
        </pipeline>
    """

    DATA4 = """
        <pipelines group="SuperGroup" />
    """

    DATA5 = """
        <pipelines group="Group_3" />
    """

    def setUp(self):
        self.config_xml = ConfigXML(self.DATA0)

    def test_get_pipeline(self):
        self.assertIsNotNone(self.config_xml.get_pipeline("Pipeline_3"))
        self.assertIsNone(self.config_xml.get_pipeline("False_Pipeline"))

    def test_get_pipeline_group(self):
        self.assertIsNotNone(self.config_xml.get_pipeline_group("Group_1"))
        self.assertIsNone(self.config_xml.get_pipeline_group("False_group"))

    def test_get_pipeline_parent_group(self):
        pipeline_group = self.config_xml.get_pipeline_parent_group("Pipeline_3")
        self.assertIsNotNone(pipeline_group)
        self.assertEqual(pipeline_group.get("group"), "Group_2")
        self.assertEqual(pipeline_group.tag, "pipelines")

        self.assertIsNone(self.config_xml.get_pipeline_parent_group("False_Pipeline"))

    def test_add_pipeline_element_in_group(self):
        pipeline_element_to_add = ET.fromstring(self.DATA1)
        with self.assertRaises(GoCdApiException):
            self.config_xml.add_pipeline_element_in_group("Group_False", pipeline_element_to_add)

        pipeline_element_to_add = ET.fromstring(self.DATA1)
        self.config_xml.add_pipeline_element_in_group("Group_1", pipeline_element_to_add)

        pipeline_group = self.config_xml.get_pipeline_parent_group("SuperPipeline")
        pipeline_element = self.config_xml.get_pipeline("SuperPipeline")
        self.assertIsNotNone(pipeline_group)
        self.assertIsNotNone(pipeline_element)
        self.assertEqual(pipeline_element.get("name"), "SuperPipeline")
        self.assertEqual(pipeline_group.get("group"), "Group_1")

        pipeline_element_to_add = ET.fromstring(self.DATA2)
        with self.assertRaises(GoCdApiException):
            self.config_xml.add_pipeline_element_in_group("Group_1", pipeline_element_to_add)

    def test_remove_pipeline(self):
        pipeline_group = self.config_xml.remove_pipeline("Pipeline_3")
        self.assertIsNone(self.config_xml.get_pipeline("Pipeline_3"))
        self.assertIsNotNone(pipeline_group)
        self.assertEqual(pipeline_group.get('group'), "Group_2")
        with self.assertRaises(GoCdApiException):
            self.config_xml.remove_pipeline("Pipeline_False")

    def test_update_pipeline_element(self):
        pipeline_element_to_update = ET.fromstring(self.DATA2)

        pipeline_name = pipeline_element_to_update.get("name")
        pipeline_group_old = self.config_xml.get_pipeline_parent_group(pipeline_name)
        pipeline_element_old = self.config_xml.get_pipeline(pipeline_name)

        self.config_xml.update_pipeline_element(pipeline_element_to_update)

        pipeline_group_new = self.config_xml.get_pipeline_parent_group(pipeline_name)
        pipeline_element_new = self.config_xml.get_pipeline(pipeline_name)

        self.assertEqual(pipeline_element_old.get("name"), pipeline_element_new.get("name"))
        self.assertEqual(pipeline_group_old.get("group"), pipeline_group_new.get("group"))
        self.assertIsNotNone(pipeline_element_new.get("arg"))
        self.assertEqual(pipeline_element_new.get("arg"), "newarg")

        pipeline_element_to_update = ET.fromstring(self.DATA1)
        with self.assertRaises(GoCdApiException):
            self.config_xml.update_pipeline_element(pipeline_element_to_update)

    def test_add_pipeline_group_element(self):
        group_element = ET.fromstring(self.DATA4)
        self.config_xml.add_pipeline_group_element(group_element)
        self.assertIsNotNone(self.config_xml.get_pipeline_group("SuperGroup"))

        group_element = ET.fromstring(self.DATA5)
        with self.assertRaises(GoCdApiException):
            self.config_xml.add_pipeline_group_element(group_element)

    def test_remove_pipeline_group(self):
        self.config_xml.remove_pipeline_group("Group_3")
        self.assertIsNone(self.config_xml.get_pipeline_group("Group_3"))
        with self.assertRaises(GoCdApiException):
            self.config_xml.remove_pipeline_group("Group_False")

    def test_create_pipeline_group(self):
        self.config_xml.create_pipeline_group("Group_5")
        self.assertIsNotNone(self.config_xml.get_pipeline_group("Group_5"))

        with self.assertRaises(GoCdApiException):
            self.config_xml.create_pipeline_group("Group_3")

    def test_add_pipeline_from_xml_string_in_group(self):
        with self.assertRaises(GoCdApiException):
            self.config_xml.add_pipeline_from_xml_string_in_group("Group_False", self.DATA1)

        pipeline_element_to_add = ET.fromstring(self.DATA1)
        self.config_xml.add_pipeline_from_xml_string_in_group("Group_1", self.DATA1)

        pipeline_group = self.config_xml.get_pipeline_parent_group("SuperPipeline")
        pipeline_element = self.config_xml.get_pipeline("SuperPipeline")
        self.assertIsNotNone(pipeline_group)
        self.assertIsNotNone(pipeline_element)
        self.assertEqual(pipeline_element.get("name"), "SuperPipeline")
        self.assertEqual(pipeline_group.get("group"), "Group_1")

        with self.assertRaises(GoCdApiException):
            self.config_xml.add_pipeline_from_xml_string_in_group("Group_1", self.DATA2)

    def test_update_pipeline_from_xml_string(self):
        pipeline_name = "Pipeline_4"
        pipeline_group_old = self.config_xml.get_pipeline_parent_group(pipeline_name)
        pipeline_element_old = self.config_xml.get_pipeline(pipeline_name)

        self.config_xml.update_pipeline_from_xml_string(self.DATA2)

        pipeline_group_new = self.config_xml.get_pipeline_parent_group(pipeline_name)
        pipeline_element_new = self.config_xml.get_pipeline(pipeline_name)

        self.assertEqual(pipeline_element_old.get("name"), pipeline_element_new.get("name"))
        self.assertEqual(pipeline_group_old.get("group"), pipeline_group_new.get("group"))
        self.assertIsNotNone(pipeline_element_new.get("arg"))
        self.assertEqual(pipeline_element_new.get("arg"), "newarg")

        with self.assertRaises(GoCdApiException):
            self.config_xml.update_pipeline_from_xml_string(self.DATA1)

    def test_str(self):
        str(self.config_xml)


if __name__ == '__main__':
    unittest.main()
