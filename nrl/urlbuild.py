"""
This module the functionality for building URLs. The URL that can be sent to
NRL web service to receive the desired response.
"""
from typing import NamedTuple
from urllib.parse import urlunsplit

NETLOC = 'service.iris.edu'
HOSTNAME = 'service.iris.edu'
PATH = '/irisws/nrl/1/'
SCHEME = 'http'


class Components(NamedTuple):
    scheme: str = SCHEME
    netloc: str = NETLOC
    path: str = PATH
    query: str = ''
    fragment: str = ''


class URLBuild:
    """
    The URLBuild class is responsible for building the URL that is being sent
    to NRL web service to receive the requested data.
    """
    def __init__(self, query: str = ''):
        self.scheme: str = SCHEME
        self.netloc: str = NETLOC
        self.params = None
        self.path: str = PATH
        self.hostname: str = HOSTNAME
        self.port: int = 80
        self.query = query
        self.fragment = ''
        # namedtuple to match the internal signature of urlunparse
        self.nrl_components = self.__build_nrl_components()

    def __reset_defaults(self):
        """
        Reset the instance of the URLBuild class
        :return: None
        """
        self.scheme: str = SCHEME
        self.netloc: str = NETLOC
        self.params = None
        self.path: str = PATH
        self.hostname: str = HOSTNAME
        self.port: int = 80
        self.query = ''
        self.fragment = ''
        # namedtuple to match the internal signature of urlunparse
        self.nrl_components = self.__build_nrl_components()

    def build_url(self, nrl_query: str) -> str:
        """
        Build the URL that is being used to fetch the corresponding response
        from the NRL web service.
        :return: The URL that can be sent to the NRL web service.
        :rtype: str
        """
        self.__reset_defaults()
        self.__set_nrl_query(nrl_query)
        # There is small issue with the way web service handles url. The
        # beginning of the query (catalog, combine, or prefix-lookup) should be
        # part of the path, but we can't determine it before having the query
        # information from the user. The solution here is to pass it as the
        # query section and then split it when the final url is being built.
        query_type = self.query.split('?')[0]
        self.path += query_type
        self.query = self.query.split('?')[1]
        # the Structure of the url is like:
        # nrl_url = scheme://netloc/path;parameters?query#fragment
        nrl_url = urlunsplit(self.__build_nrl_components())
        return str(nrl_url)

    def __set_nrl_query(self, nrl_query: str) -> None:
        """
        Set the query part of the final string that will be sent to the NRL
        web service
        :param nrl_query: The string presentation of the query part of the
        final URL link
        :type nrl_query: str
        :return: None
        """
        if nrl_query == '':
            raise ValueError('Query cannot be empty!')
        self.query = nrl_query

    def __build_nrl_components(self) -> Components:
        """
        Set NRL_Components for the urlunsplit method
        :return: The Components of the urlunsplit method
        :rtype: Components
        """
        nrl_components = Components(
            scheme=self.scheme,
            netloc=self.netloc,
            path=self.path,
            query=self.query,
            fragment=self.fragment)

        return nrl_components
