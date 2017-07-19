import json
from jsonpath_rw_ext import parse as jsonparse
import xpath
from xml.dom.minidom import parse as xmlparse


class XMLXPATH:
    """XMLXPATH class contains definitions for many useful and custom utilities required to address the capabilities
       of the Test framework.It contains methods for parsing XML data
    """

    def __init__(self):
        pass

    def _xmlparser(self, datafile, xpathfile):
        # type: () -> object

        """
        Custom parser for xml using xpath
        USAGE:
        _xmlparser(datafile,xpathfile)

        datafile : file containing actual xml data
        xpathfile : file containing all the xpath's mentioned in a file

        NOTE:
        This method/function can be used for any test involving xml parsing using xpath's
        """
        self.datafile = datafile
        self.xpathfile = xpathfile

        loaddatafile = xmlparse(datafile)
        xpaths = open(xpathfile, 'r+')

        for xpathlist in xpaths:
            try:
                response = xpath.find(xpathlist, loaddatafile)
                for xpathe in response:
                    for xchild in xpathe.childNodes:
                        if xchild.nodeType == xchild.TEXT_NODE:
                            xvalue = xchild.nodeValue
                            print('%s : %s' % (xpathe, xvalue))
                            # print('%s' % xvalue)

            except TypeError:
                raise Exception('TypeError')

            except Exception as e:
                raise Exception("Error Occurred : %s" % e)

    def _xmlparserwithspecificxpath(self, datafile, xpathe):
        # type: () -> object

        """
        Custom parser for xml using specific xpath
        USAGE:
        _xmlparserwithspecificxpath(datafile,xpathe)

        datafile : file containing actual xml data
        xpath : provide the specific xpath which needs to be parsed

        NOTE:
        This method/function can be used for any test involving xml parsing using specific xpath
        """
        self.datafile = datafile
        self.xpathe = xpathe
        loaddatafile = xmlparse(datafile)

        try:
            response = xpath.find(xpathe, loaddatafile)
            for xpathee in response:
                for xchild in xpathee.childNodes:
                    if xchild.nodeType == xchild.TEXT_NODE:
                        xvalue = xchild.nodeValue
                        print(xvalue)

        except TypeError:
            raise Exception('None')

        except Exception as e:
            raise Exception("Error Occurred : %s" % e)


class Json:
    """Json class contains definitions for many useful and custom utilities required to address the capabilities
    of the Dev/Test framework.It contains methods for parsing json data"""

    def __init__(self):
        pass

    def _jsonparser(self, datafile, jpathfile):
        # type: () -> object

        """
        Custom parser for Json using jpath
        USAGE:
        _jsonparser(datafile,jpathfile)

        datafile : file containing actual json data
        jpathfile : file containing all the jpath's mentioned in the file

        NOTE:
        This method/function can be used for any test involving json parsing using jpath's
        """

        self.datafile = datafile
        self.jpathfile = jpathfile

        loaddatafile = json.load(open(datafile, 'r+'))
        jpaths = open(jpathfile, 'r+')

        for jpathlist in jpaths:
            try:
                response = jsonparse(jpathlist).find(loaddatafile)
                for jpath in response:
                    print('%s : %s' % (jpath.path, jpath.value))

            except TypeError:
                print('None')

            except Exception as e:
                print("Error Occurred : %s" % e)

    def _jsonparserwithspecificjpath(self, datafile, jpath):
        # type: () -> object

        """
        Custom parser for Json using specific jpath
        USAGE:
        _jsonparser(datafile,jpath)

        datafile : file containing actual json data
        jpath : provide the specific jpath which needs to be parsed

        NOTE:
        This method/function can be used for any test involving json parsing using specific jpath
        """

        self.datafile = datafile
        self.jpath = jpath

        loaddatafile = json.load(open(datafile))

        try:
            response = jsonparse(jpath).find(loaddatafile)
            for jpath in response:
                print('%s' % jpath.value)

        except TypeError:
            print('None')

        except Exception as e:
            print("Error Occurred : %s" % e)
