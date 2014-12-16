import os
import time
import Queue
import random
import logging
import datetime

import threading
import subprocess
import pkg_resources

from gocdapi.go import Go
from gocdapi.custom_exceptions import GoCdApiException

log = logging.getLogger(__name__)

import sys
import urllib
import zipfile

GO_VERSION = "14.3.0-1186"


def dlProgress(count, blockSize, totalSize):
    percentage = (blockSize * count * 100) / totalSize
    sys.stdout.write("\r%s%%" % percentage)

def get_default_configuration():
    systests_dir, _ = os.path.split(__file__)
    return "%s/%s" % (systests_dir, "cruise-config.xml")

class StreamThread(threading.Thread):

    def __init__(self, name, q, stream, fn_log):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q
        self.stream = stream
        self.fn_log = fn_log

    def run(self):
        log.info("Starting %s", self.name)

        while True:
            line = self.stream.readline()
            if line:
                self.fn_log(line.rstrip())
                self.q.put((self.name, line))
            else:
                break
        self.q.put((self.name, None))


def download_zip(url, destiny_zip_file):
    log.info("Downloading zip from %s" % url)


def run_command(command, env_variables=None):
    return subprocess.Popen(command, env=env_variables,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class GoLauncher(object):
    """
    """

    def __init__(self, runnable_type, working_directory, version = None):
        """
        """
        self.version = version or GO_VERSION
        self.working_directory = working_directory
        self.runnable_type = runnable_type
        self.folder_name = "go-%s-%s" % (self.runnable_type, self.version)
        self.full_directory = "%s/%s" % (self.working_directory, self.folder_name)
        self.http_port = 8153
        self.https_port = self.http_port + 1
        self.q = Queue.Queue()

    def update_runnable(self):
        """
        """
        log.info("Checking if %s exists..." % self.full_directory)
        os.chdir(self.working_directory)
        if os.path.exists(self.folder_name):
            log.info("We already have the go %s locally..." % self.runnable_type)
        else:
            try:
                log.info("Redownloading Go %s..." % self.runnable_type)
                zip_file = "%s.zip" % self.folder_name
                url = "http://download.go.cd/gocd/%s" % zip_file
                urllib.urlretrieve(url, filename=zip_file, reporthook=dlProgress)
                sys.stdout.write("\r100%\n")
            except Exception as e:
                raise Exception("Failed to download %s - %s " % (url, e))

            try:
                log.info("Unzipping %s..." % zip_file)
                zip_ref = zipfile.ZipFile(zip_file, 'r')
                zip_ref.extractall(".")
                zip_ref.close()
                os.remove(zip_file)
            except Exception as e:
                raise Exception("Failed to unzip %s - %s " % (zip_file, e))

            try:
                target_zip_folder = "go-%s-%s" % (self.runnable_type, self.version.split('-')[0])
                log.info("Rename extracted folder from %s to %s..." % (zip_file, target_zip_folder))
                os.rename(target_zip_folder, self.folder_name)
            except Exception as e:
                raise Exception("Failed to unzip %s - %s " % (zip_file, e))


    def stop(self):
        """
        """
        os.chdir(self.full_directory)
        log.info("Shutting down Go %s..." % self.runnable_type)
        self.go_server_process = run_command(["sh", "stop-%s.sh" % self.runnable_type])

    def _start(self, env_variables):
        """
        """
        self.update_runnable()

        log.info("About to start Go %s..." % self.runnable_type)
        os.chdir(self.full_directory)

        gocd_command = "sh %s.sh" % self.runnable_type
        return run_command(gocd_command.split(), env_variables)


class GoServerLauncher(GoLauncher):
    """
    """

    def __init__(self, working_directory, version = None, config_xml = None):
        """
        """
        GoLauncher.__init__(self, "server", working_directory, version)
        self.http_port = 8153
        self.https_port = self.http_port + 1
        self.config_xml = config_xml or get_default_configuration()

    def block_until_is_ready(self, timeout):
        start_time = datetime.datetime.now()
        timeout_time = start_time + datetime.timedelta(seconds=timeout)

        while True:
            try:
                Go('http://localhost:%s' % str(self.http_port))
                log.info('Go Server is finally ready for use.')
                return
            except GoCdApiException:
                log.info('Go Server is not yet ready...')
            if datetime.datetime.now() > timeout_time:
                raise TimeOut('Took too long for Go Server to become ready...')
            time.sleep(5)

    def start(self, timeout=60):
        config_source = "/Users/joaocravo/Work/spikes/gocdapi/gocdapi_utils/"
        env_variables = {
                "DAEMON": "Y",
                "JAVA_HOME": "/usr",
                "GO_SERVER_PORT": "%s" % self.http_port,
                "GO_SERVER_SSL_PORT": "%s" %  self.https_port,
                "GO_CONFIG_DIR": config_source
            }

        process = self._start(env_variables)

        threads = [
            StreamThread('out', self.q, process.stdout, log.info),
            StreamThread('err', self.q, process.stderr, log.warn)
        ]

        # Start the threads
        for t in threads:
            t.start()

        while True:
            try:
                streamName, line = self.q.get(block=True, timeout=timeout)
            except Queue.Empty:
                log.warn("Input ended unexpectedly")
                break
            else:
                if line:
                    if 'Creating cache named messageBundles' in line:
                        log.info(line)
                        break
                else:
                    log.warn('Stream %s has terminated', streamName)

        self.block_until_is_ready(timeout)


class GoAgentLauncher(GoLauncher):
    """
    """

    def __init__(self, working_directory, version = None):
        """
        """
        GoLauncher.__init__(self, "agent", working_directory, version)
        self.http_port = 8153
        self.q = Queue.Queue()

    def start(self, timeout=60):
        """
        """
        env_variables = {
            "DAEMON": "Y",
            "JAVA_HOME": "/usr",
            "GO_SERVER_PORT": "%s" % self.http_port
        }
        process = self._start(env_variables)

        threads = [
            StreamThread('out', self.q, process.stdout, log.info),
            StreamThread('err', self.q, process.stderr, log.warn)
        ]

        # Start the threads
        for t in threads:
            t.start()

        retries = 3
        while True:
            try:
                streamName, line = self.q.get(block=True, timeout=timeout)
            except Queue.Empty:
                log.warn("Input ended unexpectedly")
                break
            else:
                if line:
                    if "Couldn't access Go Server with base url" in line:
                        log.info("Agent running, however can't connect to the server")
                        retries -= 1
                    if retries == 0:
                        raise Exception("Can't connect to the Go Server.")
                else:
                    log.warn('Stream %s has terminated', streamName)


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('').setLevel(logging.INFO)

    current_path = os.getcwd()
    version = "14.3.0-1186"

    log.info("Starting Go Server...!")

    go_server_laucher = GoServerLauncher(current_path, version)
    go_server_laucher.start()
    log.info("Go Server was launched...")

    go_agent_laucher = GoAgentLauncher(current_path, version)
    go_agent_laucher.start()
    log.info("Go Agent was launched...")

    log.info("Waiting 30 seconds before shut it down...")
    time.sleep(30)

    log.info("...now to shut it down!")
    go_agent_laucher.stop()
    go_server_laucher.stop()

