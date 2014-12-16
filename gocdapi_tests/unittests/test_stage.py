import mock

import unittest

from gocdapi.go import Go
from gocdapi.stage import Stage
from gocdapi.pipeline import Pipeline

from gocdapi.custom_exceptions import GoCdApiException

class TestStage(unittest.TestCase):

    DATA0 = {
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
      ],
      "label":"${COUNT}"
    }

    DATA1 = {
       "name":"Deploy"
    }

    def setUp(self):
        self.baseurl = 'http://localhost:8080'
        self.go = Go(self.baseurl)
        pipeline = Pipeline(self.go, self.DATA0)
        self.stage = Stage(self.go, pipeline, self.DATA1)

    def test_repr(self):
        self.assertEquals(str(self.stage), 'Stage @ %s' % self.baseurl)


if __name__ == '__main__':
    unittest.main()