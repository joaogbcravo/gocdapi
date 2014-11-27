import mock

import unittest

from gocdapi.go import Go
from gocdapi.pipeline import Pipeline
from gocdapi.pipeline_group import PipelineGroup

from gocdapi.custom_exceptions import GoCdApiException

class TestPipelineGroup(unittest.TestCase):

    DATA0 = {
       "pipelines":[
          {
             "stages":[
                {
                   "name":"Deploy"
                },
                {
                   "name":"tests"
                }
             ],
             "name":"Super_pipeline",
             "materials":[
                {
                   "description":"Web_Services",
                   "fingerprint":"65a208bb26bb8fb2c12442e49069d42cb9ba76ef6449b04a4f26b55c8e9ede59",
                   "type":"Pipeline"
                },
                {
                   "description":"outra",
                   "fingerprint":"a815699d795e895c68c3bb10d802e16e35178fc2b16749f9511dbe4a6c57b458",
                   "type":"Pipeline"
                },
                {
                   "description":"URL: git@localhost:vagrant/workshop-functional_tests, Branch: master",
                   "fingerprint":"1c3469370cf090a8b40193fc6914f910b815a0a83d0e829e0a32f6d007250f0a",
                   "type":"Git"
                }
             ],
             "label":"${COUNT}"
          },
          {
             "stages":[
                {
                   "name":"Build"
                },
                {
                   "name":"Unit_Test"
                },
                {
                   "name":"Package"
                }
             ],
             "name":"outra5",
             "materials":[
                {
                   "description":"URL: git@localhost:vagrant/consumer_website, Branch: master",
                   "fingerprint":"2a2e03a1f18c99f394e860530862d13bf1fe6bf5da99ce202591f27885a5c3ba",
                   "type":"Git"
                },
                {
                   "description":"Web_Services",
                   "fingerprint":"65a208bb26bb8fb2c12442e49069d42cb9ba76ef6449b04a4f26b55c8e9ede59",
                   "type":"Pipeline"
                }
             ],
             "label":"${COUNT}"
          }
       ],
       "name":"Deploy_stuff"
    }


    def setUp(self):
        self.baseurl = 'http://localhost:8080'
        self.go = Go(self.baseurl)
        self.pipeline_group = PipelineGroup(self.go, self.DATA0)


    def test_pipeline_exists(self):
        pipeline_name = 'Super_pipeline'
        self.assertIn(pipeline_name, self.pipeline_group)

        pipeline_name = 'false-pipeline'
        self.assertNotIn(pipeline_name, self.pipeline_group)

    def test_no_URL(self):
        self.assertIsNone(self.pipeline_group.url)

    def test_get_pipeline(self):
        pipeline_name = 'Super_pipeline'
        pipeline = self.pipeline_group[pipeline_name]
        self.assertIsInstance(pipeline, Pipeline)

        pipeline_name = 'false-group_name'
        with self.assertRaises(GoCdApiException):
            self.pipeline_group[pipeline_name]

    def test_pipeline_group_iterable(self):
        for name, pipeline in self.pipeline_group:
            self.assertIsInstance(pipeline, Pipeline)

    def test_repr(self):
        repr(self.pipeline_group)

    def test_there_is_pipeline_group(self):
        self.assertTrue(self.pipeline_group)


if __name__ == '__main__':
    unittest.main()