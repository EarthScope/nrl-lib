"""
The prefix_lookup_query is used to build the /prefix-lookup query. The NRL web
service will return the prefix table of instrument configuration prefixes with
 their names and associated logic tree questions.
 The output format can be xml, json or txt .
"""
import logging
from dataclasses import dataclass
from nrl.nrl_q_property import (NRLQueryPropertyInterface, VALID_NODATA,
                                VALID_OUTPUT_FORMAT)
from nrl.logging_setup import log_config_manager

# set up the logger
log_config_manager.setup_logging(default_level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class _PrefixLookupProperty:
    output_format: str = 'xml'
    nodata: int = 404


class PrefixLookupQuery(NRLQueryPropertyInterface):
    """
    The PrefixLookupQuery is used to build the /prefix-lookup query
    """
    def __init__(self):
        super().__init__()
        self.prefix_prop = _PrefixLookupProperty()
        self.__error_handler = True

    def __reset_defaults(self) -> None:
        """
        Reset PrefixLookupQuery variables to their default values
        :return: None
        """
        self.prefix_prop = _PrefixLookupProperty()

    def set_error_handler(self, status: bool) -> None:
        """
        Change the status of the error handler for different combine queries.
        True means ignore input errors and continue processing the rest of the
         requests, and False means terminate the process and return the error
        message.
        :param status: Set the status of the error handler
        :return: None
        """
        self.__error_handler = status

    def build_query(self, nrl_property: dict) -> str:
        """
        Implementation of the build_query method for the prefix-lookup query.
        This query only needs the following parameters:

        format: xml, json, or txt

        nodata: Specify which HTTP status code is returned when no data is found. 404 or 204.

        - 404: Refresh the browser window, leaving a blank or nearly blank screen if no data is returned.
        - 204: Do not refresh the browser window if no data is returned.

        :param nrl_property: a dictionary that contains keys, "format" and
        "nodata", and their respective values. The default values for "format"
        and "nodata" keys are "xml" and 404 respectively.
        :return: The query string part of the final URL that will be used to
        construct the prefix lookup query. The string format of the output will
        be /prefix-lookup? [format-options] [nodata-options]
        """  # noqa: E501
        self.__build_prefix_lookup_property(nrl_property)
        prefix_query = (f"prefix-lookup?format="
                        f"{self.prefix_prop.output_format}&nodata="
                        f"{self.prefix_prop.nodata}")
        return prefix_query

    def __build_prefix_lookup_property(self, user_input: dict) -> None:
        """
        Check the validity of the user input for the prefix lookup
        :param user_input: The user input dictionary that contains keys,
        "format" and "nodata", and their respective values.
        :return: None
        """
        if user_input is None:
            self.prefix_prop = _PrefixLookupProperty(output_format="xml",
                                                     nodata=404)
        if user_input is not None and len(user_input) != 2:
            if self.__error_handler:
                logger.error("The query, prefix_lookup, accepts two entries, "
                             "nodata and format. The additional input will be"
                             " ignored")
            else:
                logger.critical(f"Two key/value pairs, 'format' and 'nodata',"
                                f" are required for the prefix lookup query. "
                                f"The size of the input dictionary is "
                                f"{len(user_input)}")
                raise ValueError(f"Two key/value pairs, 'format' and 'nodata',"
                                 f" are required for the prefix lookup query. "
                                 f"The size of the input dictionary is "
                                 f"{len(user_input)}")

        for key, value in user_input.items():
            if key == 'format':
                self.__validate_output_format(value)
            elif key == 'nodata':
                self.__validate_input_nodata(value)
            else:
                if self.__error_handler:
                    logging.error(f'The key, {key} is not a valid entry')
                else:
                    logging.critical(f'The key, {key} is not a valid entry')
                    raise ValueError(f'The key, {key} is not a valid entry')

    def __validate_output_format(self, output_format: str) -> None:
        """
        Validate and assign the correct "output" format for the prefix lookup
        class
        :param output_format: user entry for the output format
        :return: None
        """
        if output_format in VALID_OUTPUT_FORMAT:
            self.prefix_prop.output_format = output_format
        else:
            logging.warning(f"The value, {output_format}, is not a valid input"
                            f" for the format. The default format, xml, "
                            f"chosen.")
            print(f"The value, {output_format}, is not a valid input for the "
                  f"format. The default format, xml, chosen.")

    def __validate_input_nodata(self, nodata: int) -> None:
        """
        Validate and assign the correct "nodata" value for the prefix lookup
        :param nodata: User entry for the nodata value
        :return: None
        """
        if nodata in VALID_NODATA:
            self.prefix_prop.nodata = nodata
        else:
            logging.warning(f"The value, {nodata}, is not a valid input for "
                            f"the nodata. The default nodata value, 404, "
                            f"chosen")
            print(f"The value, {nodata}, is not a valid input for the "
                  f"nodata. The default nodata value, 404, chosen")
