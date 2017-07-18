import mysql.connector
from mysql.connector import errorcode
import time


class MYSQLCONNECT:
    """MYSQLCONNECT class contains definitions for many useful and custom utilities required to address the test capabilities
       of the Test framework.It contains methods for executing DDL & DML SQL Queries to MYSQL
    """

    def __init__(self, host, database, username, password, port=3306):
        """
         Initialization function
         USAGE:
         a = MYSQLCONNECT('host', 'database', 'username', 'password')

         host     : Database hostname
         database : Database name
         username : Username of the user connecting
         password : Password of the user connecting
         """

        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.port = port
    
    def _name(self):
        return "manoj"

    def _getdbconnection(self):
        """
         Function for establishing a connection to Database with specified parameters in the init function
         USAGE:
         _getdbconnection()
         """

        cnx = None
        cursor = None
        try:
            dbconfig = {
                'user': self.username,
                'password': self.password,
                'host': self.host,
                'database': self.database,
                'port': str(self.port),
                'raise_on_warnings': False,
            }
            cnx = mysql.connector.connect(**dbconfig)
            cursor = cnx.cursor(buffered=True)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise Exception('Something is wrong with your user name or password for database', err.errno)
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise Exception('database does not exist', err.errno)
            else:
                raise Exception('unexpected error. failed to connect to database')
        return cnx, cursor

    def _sql_connect(self, sql_query, albo_logger, waittime=None):

        """Function for establishing a connection to Database with specified parameters in the init function
        USAGE:
        _sql_connect(sql_query<to be executed>,albo_logger<logger defined at the begin of the test>,waitime<if required in sec>)"""

        time.sleep(waittime)
        realtimecnx, realtimecursor = self._getdbconnection()
        if realtimecnx is None or realtimecursor is None:
            raise Exception('Database Connection Failure')
        realtimecursor.execute(sql_query)
        sqlquery_result = realtimecursor.fetchall()

        if realtimecnx is not None or realtimecursor is not None:
            albo_logger.info('Execution of "' + sql_query + '" successful')
        else:
            albo_logger.error('Execution of "' + sql_query + '" failed')

        return sqlquery_result

