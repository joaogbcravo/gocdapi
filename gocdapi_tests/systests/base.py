
import unittest
import logging
import time
#import gocdapi_tests.systests

from gocdapi_tests.systests.pipeline_configs import EMPTY_PIPELINE
from gocdapi.go import Go

log = logging.getLogger(__name__)

DEFAULT_GO_URL = "http://localhost"
DEFAULT_GO_PORT = 8153
DEFAULT_GO_PIPELINE_GROUP = "GO_SYSTESTS"

class BaseSystemTest(unittest.TestCase):

    def pipeline_group_name(self):
        return DEFAULT_GO_PIPELINE_GROUP

    def setUp(self):
        self.go = Go('%s:%d' % (DEFAULT_GO_URL, DEFAULT_GO_PORT))
        self._delete_test_pipelines_group(self.pipeline_group_name())
        self._create_test_pipelines_group(self.pipeline_group_name())

    def tearDown(self):
        self._delete_test_pipelines_group(self.pipeline_group_name())

    def _delete_test_pipelines_group(self, name):
        if name in self.go.pipeline_groups:
            self.go.delete_pipeline_group(name)

    def _create_test_pipelines_group(self, name):
        if name not in self.go.pipeline_groups:
            pipeline_group = self.go.create_pipeline_group(name)

    def _create_pipeline(self, name='DUMMY', config=EMPTY_PIPELINE):
        pipeline = self.go.create_pipeline(name, config)

    def assert_pipeline_is_present(self, name):
        self.assertTrue(self.go.pipeline_exist(name), 'Pipeline %r is absent in Go.' % name)

    def wait_for_agent_reconnection(self, agent_uuid):
        for _ in xrange(3):
            log.info("Waiting for agent %s connect" % agent_uuid)
            time.sleep(10)
            if agent_uuid in self.go.agents:
                return
        raise Exception("Agent %s didn't connect again to the server" % agent_uuid)