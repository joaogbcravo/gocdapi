import unittest

from gocdapi.go import Go
from gocdapi.pipeline import Pipeline


class TestPipeline(unittest.TestCase):
    DATA0 = {
        "stages": [
            {
                "name": "Deploy"
            },
            {
                "name": "tests"
            }
        ],
        "name": "Super_pipeline",
        "materials": [
            {
                "description": "Web_Services",
                "fingerprint": "65a208bb26bb8fb2c12442e49069d42cb9ba76ef6449b04a4f26b55c8e9ede59",
                "type": "Pipeline"
            },
            {
                "description": "outra",
                "fingerprint": "a815699d795e895c68c3bb10d802e16e35178fc2b16749f9511dbe4a6c57b458",
                "type": "Pipeline"
            },
            {
                "description": "URL: git@localhost:vagrant/workshop-functional_tests, Branch: master",
                "fingerprint": "1c3469370cf090a8b40193fc6914f910b815a0a83d0e829e0a32f6d007250f0a",
                "type": "Git"
            }
        ],
        "label": "${COUNT}"
    }

    def setUp(self):
        self.baseurl = 'http://localhost:8080'
        self.go = Go(self.baseurl)
        self.pipeline = Pipeline(self.go, self.DATA0)

    def test_repr(self):
        self.assertEquals(str(self.pipeline), 'Pipeline @ %s' % self.baseurl)


if __name__ == '__main__':
    unittest.main()
