import os
from gocdapi_utils.go_laucher import GoServerLauncher
from gocdapi_utils.go_laucher import GoAgentLauncher

go_instances = {}

def setUpPackage():
    version = "14.3.0-1186"
    systests_dir, _ = os.path.split(__file__)
    go_instances['server'] = GoServerLauncher(systests_dir, version)
    go_instances['agent'] = GoAgentLauncher(systests_dir, version)
    go_instances['server'].start()
    go_instances['agent'].start()



def tearDownPackage():
    go_instances['agent'].stop()
    go_instances['server'].stop()
