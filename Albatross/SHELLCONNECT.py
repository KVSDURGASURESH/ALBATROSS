import sys
import subprocess


class SHELLCONNECT:
    """SHELLCONNECT class contains definitions for many useful and custom utilities required to address the 
     capabilities of the Dev/Test framework.It contains methods for executing any sort of shell commands
    """

    def __init__(self):

        pass

    def _execute(self, cmd, albo_logger=None, failonexit=False):
        """ Function for executing any shell command
         USAGE:
         _execute('cmd')

         cmd : The shell command which needs to be executed

         NOTE:
         This method/function can be used for any test involving execution of shell commands
         """

        self.cmd = cmd
        self.failonexit = failonexit
        self.albo_logger = albo_logger

        try:
            pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = pipe.communicate()
            ret = pipe.wait()
            if ret == 0:
                albo_logger.info('Execution of ' + cmd + ' successful')
            else:
                albo_logger.info('Execution of ' + cmd + ' failed')
                raise Exception('Execution of %s  failed'% cmd)

            return out, err, ret

        except Exception as e:
            albo_logger.error('Error : %s ' % e)
            raise Exception(e)

    def _execute_with_action(self, cmd, promptmsg, albo_logger=None, failonexit=False):
        # type: (object, object) -> object
        # type: (object, object) -> object
        """
         Function for executing any shell command
         USAGE:
         _execute('cmd')

         cmd : The shell command which needs to be executed

         NOTE:
         This method/function can be used for any test involving execution of shell commands
         """

        self.cmd = cmd
        self.promptmsg = promptmsg
        self.albo_logger = albo_logger
        self.failonexit = failonexit

        try:
            pipe = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            out, err = pipe.communicate(input=self.promptmsg)
            ret = pipe.wait()
            if ret == 0:
                albo_logger.info('Execution of ' + cmd + ' successful')
            else:
                albo_logger.info('Execution of ' + cmd + ' failed')
                if failonexit:
                    sys.exit(ret)
            return out, err, ret

        except Exception as e:
            albo_logger.error('Error : %s ' % e)
            raise Exception(e)


