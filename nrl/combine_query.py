"""
The combine_query is used to build the /combine query. The NRL web service will
return fully formed instrument responses in FDSN StationXML, RESP, or
StationXML-Response formats. It can also return a full version of the Library
for local use, similar to that used by the original Nominal Response Library.
"""
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Union, List

from nrl.logging_setup import log_config_manager
from nrl.nrl_q_property import (NRLQueryPropertyInterface,
                                VALID_COMBINE_OUTPUT_FORMATS, VALID_NODATA)
from nrl.nrl_utility import is_valid_element

# set up the logger
log_config_manager.setup_logging(default_level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CombineFlags:
    # True if instconfig is selected
    instconfig_selected: bool = True
    # Element/Manufacturer/Model
    element_selected: bool = True
    manufacturer_selected: bool = True
    model_selected: bool = True
    # Flag for update_since parameter
    updated_since_selected: bool = True
    # Epoch entries
    epoch_selected: bool = True
    network_selected: bool = True
    station_selected: bool = True
    location_selected: bool = True
    channel_selected: bool = True
    # Flags for enabling or disabling the epoch's start and end times
    start_time_selected: bool = True
    end_time_selected: bool = True


@dataclass
class Epoch:
    network: Optional[str] = field(default=None)
    station: Optional[str] = field(default=None)
    location: Optional[str] = field(default=None)
    channel: Optional[str] = field(default=None)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime = field(default_factory=datetime.now)


@dataclass
class CombineProperty:
    element: list = field(default_factory=list)
    manufacturer: list = field(default_factory=list)
    model: list = field(default_factory=list)
    instconfig: list = field(default_factory=list)
    updated_since: datetime = datetime.now()
    output_format: str = 'resp'
    nodata: int = 404
    epoch: Epoch = field(default_factory=Epoch)

    def reset_combine_prop(self):
        self.element = list()
        self.manufacturer = list()
        self.model = list()
        self.instconfig = list()
        self.updated_since = datetime.now()
        self.output_format: str = 'resp'
        self.nodata: int = 404
        self.epoch = Epoch()


BAD_USER_ENTRY = ['', None]


class CombineQuery(NRLQueryPropertyInterface):
    """
    The CombineQuery is used to build the /combine query.
    """
    def __init__(self):
        super().__init__()
        self.combine_prop = CombineProperty()
        self.flag = CombineFlags()
        self.__error_handler = True

    def __reset_defaults(self) -> None:
        """
        Reset CombineQuery class variables to their default values
        :return: None
        """
        self.combine_prop.reset_combine_prop()
        self.flag = CombineFlags()

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
        Link to documentation:
        http://service.iris.edu/irisws/nrl/1/
        Implementation of the build_query method for the combine query. This query needs the following parameters:
        
        * \ *element:* \ Filter by element type. Current elements include sensor, datalogger, integrated and soh. Accepts wildcards and lists.

        * \ *manufacturer:* \ Filter by manufacturer. Accepts wildcards and lists.

        * \ *model:* \ Filter by model. Accepts wildcards and lists.

        * \ *instconfig:* \ Specify the instrument configuration(s) for the response file(s) requested. Separating two instrument configuration strings with a comma (,) returns individual responses for each instrument in the list. Joining multiple instrument configuration strings with a colon (:) returns a single response file that cascades each joined instrument in order. Accepts lists when format is specified as a .zip file, but not wildcards.

        * \ *updated_since:* \ Filter for information updated on or since the beginning day boundary of this date (UTC).

        * \ *output_format:* \ Specify output format. Accepted values are stationxml, stationxml-resp, resp, stationxml.zip, stationxml-resp.zip, resp.zip.

        * \ *nodata:* \ Specify which HTTP status code is returned when no data is found.

        * \ *epoch:* \ A dictionary which is consist of the following parameters:

            * network: Specify a network code to include in the response file.
            * station: Specify a station code to include in the response file.
            * location: Specify a location code to include in the response file.
            * channel: Specify a channel code to include in the response file.
            * starttime: Specify an epoch start date to include in the response file.
            * endtime: Specify an epoch start date to include in the response file.
        :param nrl_property: A dictionary that contains keys, "element", "manufacturer", "model", "instconfig", "updated_since"  "format", "nodata", and "epoch", and their respective values.
        :return: The query string part of the final URL that will be used to construct the combine query. The string format of the output will be: combine? (selection-options) [epoch-options] [format-options] [nodata-options] [administrative-options]
        """  # noqa: E501,W605,W293
        # Make sure all variables are set to default
        self.__reset_defaults()
        if ('instconfig' in nrl_property and
                nrl_property['instconfig'] is not None):
            self.flag.instconfig_selected = True
            self.flag.element_selected = False
            self.flag.manufacturer_selected = False
            self.flag.model_selected = False
        else:
            self.flag.instconfig_selected = False
        self.__build_combine_query(nrl_property)

        # Build the query parameters in a list
        params = []

        # If instrument configuration is chosen
        if self.flag.instconfig_selected:
            params.append(self.__build_instconfig())
        # If Element/Manufacturer/Model is chosen
        else:
            if self.flag.element_selected and self.combine_prop.element:
                params.append(self.__build_element())
            if self.flag.manufacturer_selected and self.combine_prop.manufacturer:
                params.append(self.__build_manufacturer())
            if self.flag.model_selected and self.combine_prop.model:
                params.append(self.__build_model())

        # Add common parameters
        if self.flag.updated_since_selected:
            params.append(self.__build_updated_since())

        # Add epoch parameters if selected
        if self.flag.epoch_selected:
            epoch_params = self.__build_epoch()
            if epoch_params:
                params.extend(epoch_params.split('&')[1:]
                              if epoch_params.startswith('&')
                              else [epoch_params])

        # Add format and nodata parameters
        params.append(f"format={self.combine_prop.output_format}")
        params.append(f"nodata={self.combine_prop.nodata}")

        # Build the final query
        return f"combine?{params[0]}" + ''.join(f"&{param}" for param in params[1:] if param)

    def __build_combine_query(self, user_input: dict) -> None:
        """
        Check the validity of the user entry for the combine query.
        :param user_input: The user input dictionary that contains keys,
        "element", "manufacturer", "model", "instconfig", "updated_since"
        "format", "nodata", and "epoch", and their respective values.
        :return: None
        """
        if user_input is None:
            if self.__error_handler:
                logging.error("No data provided for the combine query! The "
                              "input dictionary must contain the following "
                              "keys and values: element, manufacturer, model,"
                              " instconfig, updated_since  format, nodata, and"
                              " epoch")
            else:
                raise ValueError("No data provided for the combine query! The "
                                 "input dictionary must contain the following "
                                 "keys and values: element, manufacturer, "
                                 "model, instconfig, updated_since  format, "
                                 "nodata, and epoch")
        # First check and see if the user has provided the entry for any of
        # the following parameters
        if not self.flag.instconfig_selected:
            if 'element' not in user_input:
                self.flag.element_selected = False
            if 'manufacturer' not in user_input:
                self.flag.manufacturer_selected = False
            if 'model' not in user_input:
                self.flag.model_selected = False
        if 'updated_since' not in user_input:
            self.flag.updated_since_selected = False
        if 'epoch' not in user_input:
            self.flag.epoch_selected = False

        # If the user has neither provide the instconfig nor
        # element/manufacturer/model then raise valueerror
        if (not self.flag.instconfig_selected and
                not self.flag.element_selected and
                not self.flag.manufacturer_selected and
                not self.flag.model_selected):
            if self.__error_handler:
                logging.error("No entry provided for neither instrument "
                              "configuration nor element|manufacturer|model. "
                              "The query has been ignored")
            else:
                logging.critical('You must provide a value for the instconfig'
                                 ' parameter (non-wildcard). Alternatively '
                                 'provide element|manufacturer|model '
                                 'parameters (wildcards allowed)')
                raise ValueError
        # Go through the user entry and address each one separately
        for key, value in user_input.items():
            if key == 'element':
                self.__validate_element(value)
            elif key == 'manufacturer':
                self.__validate_manufacturer(value)
            elif key == 'model':
                self.__validate_model(value)
            elif key == 'instconfig':
                self.__validate_instconfig(value)
            elif key == 'updated_since':
                self.__validate_updated_since(value)
            elif key == 'format':
                self.__validate_output_format(value)
            elif key == 'nodata':
                self.__validate_nodata(value)
            elif key == 'epoch':
                self.__validate_epoch(value)

    def __validate_nodata(self, nodata: int) -> None:
        """
        Validate and assign the correct "nodata" value for the combine lookup
        :param nodata: User entry for the nodata value
        :return: None
        """
        if nodata in VALID_NODATA:
            self.combine_prop.nodata = nodata
        else:
            logging.warning(
                f"The value, {nodata}, is not a valid input for the nodata. "
                f"The default nodata value, 204, is chosen."
                )
            self.combine_prop.nodata = 204

    def __build_nodata(self) -> str:
        """
        Return the string presentation of the nodata value
        :return: string presentation of the nodata value
        """
        return f'nodata={self.combine_prop.nodata}'

    def __validate_element(self, element: Union[List[str], str]) -> None:
        """
        Validate and assign the correct "element" value for the combine query
        :param element: The user entry for the list of elements.
        :return: None
        """
        # If Instrument configuration is added to the combine query then we
        # don't need the element key and value
        if self.flag.instconfig_selected:
            return

        # Convert single string to list if needed
        if isinstance(element, str):
            element = [element]

        # The default for element if it's not provided
        if not self.flag.element_selected or not element:
            self.combine_prop.element = ['']
            return

        for item in element:
            # Case-insensitive validation of element
            if is_valid_element(item.lower()):
                self.combine_prop.element.append(item)
            else:
                if self.__error_handler:
                    logging.error(f'The entry {item} for the element input is '
                                  f'not valid and will be ignored.')
                else:
                    logging.critical(f"The entry '{item}' is not a valid input"
                                     f" for the element!")
                    raise ValueError(f"The entry '{item}' is not a valid input"
                                     f" for the element!")

    def __build_element(self) -> str:
        """
        Return the string presentation of the element entry
        :return: The string presentation of the element list
        """
        # If Instrument configuration is added then no need for element entry
        # The user is sending the instrument configuration or the user hasn't
        # provided any entry for the element variable
        if (self.flag.instconfig_selected
                or not self.flag.element_selected
                or not self.combine_prop.element):
            return ''
        str_element = ','.join(self.combine_prop.element)
        return f'element={str_element}'

    def __validate_manufacturer(self, manufacturer: Union[List[str], str]) -> None:
        """
        Validate and assign the correct "manufacturer" value for the combine
        query
        :param manufacturer: The user entry for the manufacturer value
        :return: None
        """
        # If Instrument configuration is added to the combine query then we
        # don't need the manufacturer key and value
        if self.flag.instconfig_selected:
            return

        # Convert single string to list if needed
        if isinstance(manufacturer, str):
            manufacturer = [manufacturer]

        # If manufacturer is not provided and the instconfig_selected is false
        # then use the wildcard `*`
        if not self.flag.manufacturer_selected or not manufacturer:
            self.flag.manufacturer_selected = False
            self.combine_prop.manufacturer = ['']
            return

        for mnfr in manufacturer:
            self.combine_prop.manufacturer.append(mnfr)

    def __build_manufacturer(self) -> str:
        """
        Return the string presentation of the manufacturer list
        :return: The string presentation of the manufacturer list
        """
        # If Instrument configuration is added then no need for manufacturer entry
        if (self.flag.instconfig_selected
                or not self.flag.manufacturer_selected
                or not self.combine_prop.manufacturer):
            return ''
        str_manufacturer = ','.join(self.combine_prop.manufacturer)
        return f'manufacturer={str_manufacturer}'

    def __validate_model(self, model: Union[List[str], str]) -> None:
        """
        Validate and assign the correct model value for the combine query
        :param model: The user entry for the model value
        :return: None
        """
        # If Instrument configuration is added to the combine query then we
        # don't need the model key and value
        if self.flag.instconfig_selected:
            return

        # Convert single string to list if needed
        if isinstance(model, str):
            model = [model]

        # If model is not provided and the instconfig_selected is false then
        # use the wildcard `*`
        if not self.flag.model_selected or not model:
            self.flag.model_selected = False
            self.combine_prop.model = ['']
            return

        for mdl in model:
            self.combine_prop.model.append(mdl)

    def __build_model(self) -> str:
        """
        Return the string presentation of the model list
        :return: The string presentation of the model list
        """
        # If Instrument configuration is added then no need for model entry
        if (self.flag.instconfig_selected
                or not self.flag.model_selected
                or not self.combine_prop.model):
            return ''
        str_model = ','.join(self.combine_prop.model)
        return f'model={str_model}'

    def __validate_instconfig(self, instconfig: str) -> None:
        """
        Specify the instrument configuration(s) for the response file(s)
        requested. Separating two instrument configuration strings with a
        comma (,) returns individual responses for each instrument in the
        list. Joining multiple instrument configuration strings with a
        colon (:) returns a single response file that cascades each joined
        instrument in order.
        Accepts lists when format is specified as a .zip file, but not
        wildcards.
        :param instconfig: The string representation of the instrument
        configuration(s)
        :return: None
        """
        delimiters = [':', ',']
        if not self.flag.instconfig_selected:
            return
        # Split the input based on the ':' or "," delimiter
        instconf_split = re.split(r'(:|,)', instconfig)
        # Remove any whitespace from the strings
        instconf_split_no_whitespace = [elem.strip() for elem in
                                        instconf_split]
        if len(instconf_split_no_whitespace) >= 1 and (instconf_split[0]
                                                       not in delimiters):
            # Handle the first instconfig entry separately. The first one
            # doesn't have any delimiter
            self.combine_prop.instconfig.append(
                {'no_delimiter': instconf_split[0]})

            # Take care of the potential error at end of the string. User
            # has added an extra delimiter without any instrument
            # configuration after that
            if instconf_split_no_whitespace[-1] in delimiters:
                instconf_split_no_whitespace.pop()
            for indx in range(len(instconf_split_no_whitespace)):
                if indx == 0:
                    continue
                # If the delimiter is ':' then update the dictionary with
                # key and value -> ':' : next entry in the list
                if instconf_split_no_whitespace[indx] == ':':
                    self.combine_prop.instconfig.append(
                        {':': instconf_split_no_whitespace[indx+1]})
                # If the delimiter is ',' then update the dictionary with
                # key and value -> ',' : next entry in the list
                if instconf_split_no_whitespace[indx] == ',':
                    self.combine_prop.instconfig.append(
                        {',': instconf_split_no_whitespace[indx+1]})

    def __build_instconfig(self) -> str:
        """
        Return the string presentation of the instrument configuration(s)
        :return:The string presentation of the instrument configuration(s)
        """
        if not self.flag.instconfig_selected:
            return ''
        str_instconfig = 'instconfig='
        for ic in self.combine_prop.instconfig:
            for key, value in ic.items():
                if key == 'no_delimiter':
                    str_instconfig += f'{value}'
                elif key == ':':
                    str_instconfig += f':{value}'
                elif key == ',':
                    str_instconfig += f',{value}'
        return str_instconfig

    def __validate_updated_since(self, updated_since: datetime) -> None:
        """
        Validate and assign the correct "updated_since" value for the combine
        query
        :param updated_since: The user entry for the updated_since value
        :return: None
        """
        if updated_since is None:
            self.flag.updated_since_selected = False
            return
        # Reset the time part of the entry to the beginning of the day
        self.combine_prop.updated_since = updated_since.strftime('%Y-%m-%d')

    def __build_updated_since(self) -> str:
        """
        Return the string presentation of the updated_since
        :return: The string presentation of the updated_since
        """
        if not self.flag.updated_since_selected:
            return ''
        return f'updatedsince={self.combine_prop.updated_since}'

    def __validate_output_format(self, output_format: str) -> None:
        """
        Validate and assign the correct "format" value for the combine query
        :param output_format: The user entry for the output format value
        :return: None
        """
        if output_format.lower() in VALID_COMBINE_OUTPUT_FORMATS:
            self.combine_prop.output_format = output_format.lower()
        else:
            logging.warning(f"The value, {output_format}, is not a valid input"
                            f" for the format. The default format, stationxml, "
                            f"chosen.")
            self.combine_prop.output_format = 'stationxml'

    def __build_output_format(self) -> str:
        """
        Return the string presentation of the output format
        :return: The string presentation of the output format
        """
        return f'format={self.combine_prop.output_format}'

    def __validate_epoch(self, epoch: dict) -> None:
        """
        Validate the entries for the "epoch" value for the combine query. The
        "epoch" variable is a dictionary that contains keys, "network",
        "station", "location", "channel", "start_time", and "end_time" their
        respective values.
        :param epoch: A dictionary that contains keys, "network",
        "station", "location", "channel", "start_time", and "end_time" their
        respective values.
        :return: None
        """
        if epoch is None or not self.flag.epoch_selected:
            return
        if 'network' not in epoch:
            self.flag.network_selected = False
        if 'station' not in epoch:
            self.flag.station_selected = False
        if 'location' not in epoch:
            self.flag.location_selected = False
        if 'channel' not in epoch:
            self.flag.channel_selected = False
        if 'start_time' not in epoch:
            self.flag.start_time_selected = False
        if 'end_time' not in epoch:
            self.flag.end_time_selected = False
        for key, value in epoch.items():
            if key == 'network':
                self.__validate_network(value)
            elif key == 'station':
                self.__validate_station(value)
            elif key == 'location':
                self.__validate_location(value)
            elif key == 'channel':
                self.__validate_channel(value)
            elif key == 'start_time':
                self.__validate_start_time(value)
            elif key == 'end_time':
                self.__validate_end_time(value)
            else:
                if self.__error_handler:
                    logging.error(f'The pair key, {key}, -> value, {value}, is'
                                  f' not a valid entry for the Epoch. The '
                                  f'entry is ignored.')
                else:
                    logging.critical(f'The pair key, {key}, -> value, {value},'
                                     f' is not a valid entry for the Epoch')
                    raise ValueError(f'The pair key, {key}, -> value, {value},'
                                     f' is not a valid entry for the Epoch')

    def __build_epoch(self) -> str:
        """
        Implementation of the "epoch" value for the combine query.
        :return: The string presentation of the epoch value
        """
        epoch_params = []
        if not self.flag.epoch_selected:
            return ''

        if self.flag.network_selected and self.combine_prop.epoch.network:
            epoch_params.append(f'net={self.combine_prop.epoch.network}')

        if self.flag.station_selected and self.combine_prop.epoch.station:
            epoch_params.append(f'sta={self.combine_prop.epoch.station}')

        if self.flag.location_selected and self.combine_prop.epoch.location:
            epoch_params.append(f'loc={self.combine_prop.epoch.location}')

        if self.flag.channel_selected and self.combine_prop.epoch.channel:
            epoch_params.append(f'cha={self.combine_prop.epoch.channel}')

        if self.flag.start_time_selected and self.combine_prop.epoch.start_time:
            epoch_params.append(f'starttime={self.combine_prop.epoch.start_time}')

        if self.flag.end_time_selected and self.combine_prop.epoch.end_time:
            epoch_params.append(f'endtime={self.combine_prop.epoch.end_time}')

        return '&'.join(epoch_params)

    def __validate_network(self, network: str) -> None:
        """
        Validate the network entry for the combine query.
        :param network: The user entry for the network value
        :return: None
        """
        # Network field can be left empty in the NRL web service
        if network in BAD_USER_ENTRY or not self.flag.network_selected:
            self.flag.network_selected = False
            return
        if len(network) != 2:
            if self.__error_handler:
                logging.error(f"Network codes must be represented with two "
                              f"letters. The invalid network code, {network}, "
                              f"is ignored.")
            else:
                logging.critical(f"The value for the network, {network}, is "
                                 f"not a valid input.")
                raise ValueError(f"The value for the network, {network}, is "
                                 f"not a valid input.")
        self.combine_prop.epoch.network = network

    def __build_network(self) -> str:
        """
        Return the string presentation of the network code
        :return:The string presentation of the network code
        """
        if not self.flag.network_selected:
            return ''
        return f'net={self.combine_prop.epoch.network}'

    def __validate_station(self, station: str) -> None:
        """
        Validate the station entry for the combine query.
        :param station: The user entry for the station code
        :return: None
        """
        if station in BAD_USER_ENTRY or not self.flag.station_selected:
            self.flag.station_selected = False
            return
        self.combine_prop.epoch.station = station

    def __build_station(self) -> str:
        """
        Return the string presentation of the station code
        :return:The string presentation of the station code
        """
        if not self.flag.station_selected:
            return ''
        return f'sta={self.combine_prop.epoch.station}'

    def __validate_location(self, location: str) -> None:
        """
        Validate the location entry for the combine query.
        :param location: The user entry for the location code
        :return: None
        """
        if location in BAD_USER_ENTRY or not self.flag.location_selected:
            self.flag.location_selected = False
            return
        self.combine_prop.epoch.location = location

    def __build_location(self) -> str:
        """
        Return the string presentation of the location code
        :return:The string presentation of the location code
        """
        if not self.flag.location_selected:
            return ''
        return f'loc={self.combine_prop.epoch.location}'

    def __validate_channel(self, channel: str) -> None:
        """
        Validate the channel entry for the combine query.
        :param channel: The user entry for the channel code
        :return: None
        """
        if channel in BAD_USER_ENTRY or not self.flag.channel_selected:
            self.flag.channel_selected = False
            return
        self.combine_prop.epoch.channel = channel

    def __build_channel(self) -> str:
        """
        Return the string presentation of the channel code
        :return: The string presentation of the channel code
        """
        if not self.flag.channel_selected:
            return ''
        return f'cha={self.combine_prop.epoch.channel}'

    def __validate_start_time(self, start_time: datetime) -> None:
        """
        Validate the start time entry for the combine query.
        :param start_time: The user entry for the start time value
        :return: None
        """
        # Start time can be ignored
        if start_time in BAD_USER_ENTRY:
            self.flag.start_time_selected = False
            return
        self.combine_prop.epoch.start_time = (
            start_time.strftime('%Y-%m-%dT%H:%M:%S'))

    def __build_start_time(self) -> str:
        """
        Return the string presentation of the start time code
        :return: The string presentation of the start time code
        """
        # Start time can be ignored
        if not self.flag.start_time_selected:
            return ''
        return f'starttime={self.combine_prop.epoch.start_time}'

    def __validate_end_time(self, end_time: datetime) -> None:
        """
        Validate the end time entry for the combine query.
        :param end_time: the user entry for the end time value
        :return: None
        """
        # End time can be ignored
        if end_time in BAD_USER_ENTRY:
            self.flag.end_time_selected = False
            return
        self.combine_prop.epoch.end_time = (
            end_time.strftime('%Y-%m-%dT%H:%M:%S'))

    def __build_end_time(self) -> str:
        """
        Return the string presentation of the end time code
        :return: The string presentation of the end time code
        """
        # End time can be ignored
        if not self.flag.end_time_selected:
            return ''
        return f'endtime={self.combine_prop.epoch.end_time}'
