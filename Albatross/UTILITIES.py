import os
import sys
from logging.handlers import RotatingFileHandler
import logging

# Setting the variables for sys path
scriptdir = os.path.dirname(os.path.abspath(__file__))
reportdir = os.path.dirname(scriptdir) + '/REPORTS'
bindir = os.path.dirname(scriptdir) + '/BIN'
datadir = os.path.dirname(scriptdir) + '/DATA'
libdir = os.path.dirname(scriptdir) + '/LIB'
confdir = os.path.dirname(scriptdir) + '/CONF'
pylibdir = os.path.dirname(scriptdir) + '/PYLIB'
sixdir = pylibdir + '/six'
sys.path.append(sixdir)
paths = [reportdir, bindir, datadir, libdir, pylibdir, confdir]
#paths = [reportdir, bindir, datadir, libdir, pylibdir, confdir]
sys.path.append(paths)

class FILEEXISTS:
    """Utilities class contains variables and functions which are customised or sort of a tool kit for Automation"""

    def __init__(self):
        pass

    def _file_exists(self, file, albo_logger):
        """Function to validate if the data/config files exist or not"""
        self.file = file
        self.albo_logger = albo_logger
        try:
            assert (os.path.exists(file)), "File %s doesn't exist" % file
            albo_logger.info(file + ' : EXISTS')

        except AssertionError as e:
            albo_logger.error(e)
            raise AssertionError(e)


class LOGGER:
    """LOGGER class contains definitions for many useful and custom utilities required to address the test
      capabilities of the Test framework.It contains all the logger methods
     """

    def __init__(self):

        pass

    """    def _log(self, message, exitcode=0, failonexit=False):
        Function for logging a specific message
          USAGE:
          _execute('message')

          message : The message which needs to be logged

          NOTE:
          This method/function can be used for any message logging


        self.message = message
        self.exitcode = exitcode
        self.failonexit = failonexit

        if exitcode == 0:
            logger.info('%s', message)
        else:
            logger.error('%s. Exit code %d', message, exitcode)
        if failonexit:
            logger.error('exiting with errorcode : %d', exitcode)
    """
    def _setup_logger(self, loggername, logfile, level=logging.INFO, maxFileBytes=100000):
        """
          Function for logging the entire test run details into a file specified with timestamp
          USAGE:
          _execute('loggername', 'logfile')

          loggername : The name of the logger (ex: Daily_Metrics)
          logfile    : The file name including the directory name

          NOTE:
          This method/function can be used for logging and test event into a specific logger file
          """

        self.loggername = loggername
        self.logfile = logfile
        self.maxFileBytes = maxFileBytes

        # logging.basicConfig(filename=logfile, level=level, format="%(asctime)s - %(levelname)s - %(message)s",
        #                   datefmt='%Y-%m-%d %H:%M:%S')
        logs = logging.getLogger(loggername)
        logs.setLevel(level)
        handler = RotatingFileHandler(logfile, maxBytes=maxFileBytes, backupCount=5)
        fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(fmt)
        logs.addHandler(handler)
        assert isinstance(logs, object)
        return logs
