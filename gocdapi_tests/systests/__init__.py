import os
from gocdapi_utils.go_launcher import GoServerLauncher
from gocdapi_utils.go_launcher import GoAgentLauncher
from testconfig import config

go_instances = {}
static_instances = config.get('static_instances', False)

def setUpPackage():
    if not static_instances:
        version = "16.5.0-3305"
        systests_dir, _ = os.path.split(__file__)
        go_instances['server'] = GoServerLauncher(systests_dir, version)
        go_instances['agent'] = GoAgentLauncher(systests_dir, version)
        go_instances['server'].start()
        go_instances['agent'].start()

def tearDownPackage():
    if not static_instances:
        go_instances['agent'].stop()
        go_instances['server'].stop()
