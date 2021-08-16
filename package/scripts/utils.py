from datetime import datetime

from resource_management import Execute


class Logger():
    def __init__(self, log_file):
        self._log_file = log_file

    def log(self, msg):
        Execute("echo '{0} {1}' >> {2}".format(self._now(), msg, self._log_file))

    @staticmethod
    def _now():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
