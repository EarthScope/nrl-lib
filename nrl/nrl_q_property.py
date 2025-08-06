"""
The interface to build an NRL query property object. Three different types of
property objects can be built. Combine, Catalog, and Prefix Lookup.
Each query type requires different types of information to be constructed.
Details for each type will be discussed in their respective module.
"""

import abc

VALID_OUTPUT_FORMAT = ['xml', 'json', 'text']
VALID_COMBINE_OUTPUT_FORMATS = ['stationxml', 'stationxml-resp', 'resp',
                                'stationxml.zip', 'stationxml-resp.zip',
                                'resp.zip']
VALID_NODATA = [204, 404]
VALID_ELEMENT = ['sensor', 'datalogger', 'integrated', 'soh']
VALID_LEVEL = ['element', 'manufacturer', 'model', 'configuration']


class NRLQueryPropertyInterface(metaclass=abc.ABCMeta):
    def __init__(self):
        self.error_handler = True

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'build_query') and
                callable(subclass.build_query) and
                hasattr(subclass, 'set_error_handler') and
                callable(subclass.set_error_handler) or
                NotImplemented)

    @abc.abstractmethod
    def set_error_handler(self, status: bool) -> None:
        """
        Change the status of the error handler for different combine queries.
        True means ignore input errors and continue processing the rest of the
        requests, and False means terminate the process and return the error
        message.
        :param status: Set the status of the error handler
        :return: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def build_query(self, nrl_property: dict) -> str:
        """
        Build the query section of the NRL query string
        :param nrl_property: Dictionary containing needed information for a
        specific type of query.
        :return: The string presentation of the information
        """
        raise NotImplementedError
