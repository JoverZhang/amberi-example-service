import os

from resource_management import Directory, Execute, File, Script, Template, format
from resource_management.core.exceptions import ComponentIsNotRunning

from utils import Logger

PID_FILE = '/var/run/ambari-service-example.pid'
LOG_FILE = '/tmp/ambari-service-example.log'


class Example(Script):

    def __init__(self):
        # Init logger
        self._log = Logger(LOG_FILE).log

    def install(self, env):
        import params

        # Create Home
        Directory([params.install_directory], mode=0o755, cd_access='a', create_parents=True)

        # Create ambari-service-example
        Execute('cd ' + params.install_directory + '; touch ambari-service-example')

    def configure(self, env):
        import params
        env.set_params(params)

        # Create conf/ in Home
        Directory([params.install_directory + '/conf'], mode=0o755, cd_access='a', create_parents=True)

        # Create example.properties from Template
        File(format('{install_directory}/conf/example.properties'),
             content=Template('example.properties.j2'),
             mode=0o600)

    def start(self, env):
        self.configure(env)

        # Create pid file
        Execute('touch ' + PID_FILE)

        self._log(format('tmp_dir: {tmp_dir}'))
        self._log('example component is started')

    def stop(self, env):
        self.configure(env)

        # Remove pid file
        Execute('rm -f ' + PID_FILE)

        self._log('example component is stopped')

    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        # Check pid file
        if not os.path.isfile(PID_FILE):
            raise ComponentIsNotRunning()


if __name__ == '__main__':
    Example().execute()
