import requests
import time
from SHELLCONNECT import SHELLCONNECT


class STORM:
    def _startdatatopology(self, jarfile, subscriber_classname, appconfig_file, albo_logger):
        """This function is for starting the data topology for the first time.The parameters required
                    are subscriber classname, appconfig file & the jar"""

        self.jarfile = jarfile
        self.appconfig_file = appconfig_file
        self.subscriber_classname = subscriber_classname
        self.albo_logger = albo_logger
        # Starting the topology with the parameters passed
        try:
            regchemcmd = 'storm jar ' + jarfile + ' ' + subscriber_classname + ' ' + appconfig_file
            SHELLCONNECT()._execute(regchemcmd, albo_logger)

        except Exception as e:
            raise Exception('Error starting topology %s' % e)

    def _topology_check(self, topology_name, topology_summary_get, albo_logger):
        self.topology_name = topology_name
        self.topology_summary_get = topology_summary_get
        self.albo_logger = albo_logger

        try:
            count = 1
            while count < 6:
                try:
                    nimbustopolist = requests.get(topology_summary_get).json()
                    break
                except Exception as e:
                    albo_logger.info('Attempt %d ..waiting for 5sec..' % count)
                    time.sleep(5)
                    count += 1
            if count == 6: raise Exception('Cant connect to API..')
            for topologies in nimbustopolist.values():
                for toponame in topologies:
                    if toponame['name'] == topology_name and toponame['status'] == 'ACTIVE':
                        albo_logger.info('Topology present - %s : %s' % (toponame['name'], toponame['status']))
                        return True
            
            albo_logger.info('Topology NOT present')
            return False
        except Exception as e:
            raise Exception(e)

    def _topology_summary_check(self, topology_name, topology_summary_get, albo_logger):
        """This function check whether the topology is up and running. The parameters required
                            are topology name, url for the api page, and logger variable"""

        self.topology_name = topology_name
        self.topology_summary_get = topology_summary_get
        self.albo_logger = albo_logger

        try:
            n = 2
            count = 0
            # Waiting for the topology to become ACTIVE. Timeout period 20 sec
            while count < n:
                counter = 1
                while counter < 10:
                    try:
                        nimbustopolist = requests.get(topology_summary_get).json()
                        break
                    except Exception as e:
                        albo_logger.info('Attempt %d ..waiting for 2sec..' % counter)
                        time.sleep(2)
                        counter += 1
                if counter == 10: raise Exception('Cant connect to API..')

                for topologies in nimbustopolist.values():
                    for toponame in topologies:
                        if toponame['name'] == topology_name and toponame['status'] == 'ACTIVE':
                            # albo_logger.info('Topology status: -- %s -- %s' % (toponame['name'], toponame['status']))
                            topoid = r'%s' % toponame['id']
                            return True, topoid
                time.sleep(10)
                count += 1

            if count == n:
                raise Exception("Timeout. Topology not started")

        except Exception as e:
            raise Exception('Topology summary check failed: %s' % e)

    def _topology_spout_check(self, topology_name, topology_info_base, albo_logger, topoid=None):
        """ This function is to check whether all spout hosts are up and running. The parameters required are
            topology name, url for the api page, logger variable and the ID of the running topology"""

        self.topology_name = topology_name
        self.topoid = r'%s' % topoid
        self.topology_info_base = topology_info_base

        try:
            n = 5
            count = 1;counter = 0
            # Url for the API page
            url = topology_info_base + self.topoid

            while count <= n:
                try:
                    count_api = 1
                    while count_api < 10:
                        try:
                            nimbustopoinfo = requests.get(url).status_code
                            nimbuscheck = requests.get(url).json()
                            break
                        except Exception as e:
                            albo_logger.info('Attempt %d ..waiting for 2sec..' % count_api)
                            time.sleep(2)
                            count_api += 1
                    if count_api == 10: raise Exception('Cant connect to API..')
                    
                    if nimbustopoinfo == 200:
                        albo_logger.info('Response is %d, API Page available' % nimbustopoinfo)
                        
                        for key,value in nimbuscheck.items():
                            if isinstance(value, list):
                                if key == "bolts" or key == "spouts":
                                    for stat in value:
                                        if stat["lastError"] != "" or stat["errorHost"] != "" or stat["errorPort"] != "":
                                            sbid = "boltId" if key == "bolts" else "spoutId"
                                            albo_logger.error('Spout/Bolt: %s, Id: %s,lastError : %s,errorHost : %s, errorPort :%s ' % (key, stat[sbid], stat["lastError"], stat["errorHost"], stat["errorPort"]))
                                            raise Exception("Topology Error:%s "%stat["lastError"] )
                        break
                    else:
                        albo_logger.info('Attempt %d ..waiting for 10sec..' % count)
                        time.sleep(10)
                        count += 1
                        if count == n+1:
                            raise Exception("Timeout. Topology not started")

                except Exception as e:
                    raise Exception(e)
            spoutsummary_code = requests.get(url + '/component/storm-spout').status_code
            if spoutsummary_code != 200:
                raise Exception('Spout summary page unavailable')
            # Waiting for all spouts to come up and starts showing the uptime. Timeout : 50 sec
            while counter < 5:
                host = {}; flag = 0
                count_api = 1
                while count_api < 10:
                    try:
                        nimbusspoutsummary = requests.get(url + '/component/storm-spout').json()
                        break
                    except Exception as e:
                        albo_logger.info('Attempt %d ..waiting for 2sec..' % count_api)
                        time.sleep(2)
                        count_api += 1
                if count_api == 10: raise Exception('Cant connect to API..')
                
                for key, value in nimbusspoutsummary.items():
                    if isinstance(value, list):
                        if key == 'executorStats':
                            for exestat_v in value:
                                if exestat_v['uptime']:
                                    # albo_logger.error('HOST : %s -- UPTIME : %s' % (exestat_v['host'], exestat_v['uptime']))
                                    host[exestat_v['host']] = exestat_v['uptime']
                                else: flag = 1
                if not flag:
                    return True, host
                else:
                    counter += 1
                    time.sleep(10)

            if counter == 5:
                return False, host

        except Exception as e:
            raise Exception('Topology spout check failed : %s' % e)

    def _publish_data(self, publish_jar, publisher_classname, publisher_config, data_file, message_count, albo_logger):
        """Function to publish data to solace"""

        self.publish_jar = publish_jar
        self.publisher_classname = publisher_classname
        self.publisher_config = publisher_config
        self.data_file = data_file
        self.message_count = message_count
        self.albo_logger = albo_logger

        try:
            publishcmd = 'java -cp ' + publish_jar + ' ' + publisher_classname + ' ' + publisher_config + ' ' + data_file + ' ' + message_count
            SHELLCONNECT()._execute(publishcmd, albo_logger)
            albo_logger.info('published ' + message_count + ' messages')

        except Exception as e:
            raise Exception(e)

    def _stop_topology(self, topology_name, albo_logger):
        """Function to kill a specific topology and wait for a certain time"""

        self.topology_name = topology_name
        self.albo_logger = albo_logger

        try:
            killcmd = 'storm kill ' + ' ' + topology_name + ' ' + '-w' + ' ' + '10'
            SHELLCONNECT()._execute(killcmd, albo_logger)
            time.sleep(15)

        except Exception as e:
            raise Exception(e)


