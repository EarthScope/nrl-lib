"""
The catalog_query module is used to build the /catalog query. It Returns
information about types, manufacturers, models and configuration parameters
of instruments whose responses are available in the nrl web service.

Output formats:
    xml (XML .xml)
    json (JSON .json)
    text (plain text .txt)
"""
import logging
from dataclasses import dataclass, field
from datetime import datetime
from nrl.nrl_utility import is_valid_element
from nrl.nrl_q_property import (NRLQueryPropertyInterface, VALID_NODATA,
                                VALID_OUTPUT_FORMAT,
                                VALID_LEVEL)
from nrl.logging_setup import log_config_manager

# Set up logger
log_config_manager.setup_logging(default_level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class _CatalogFlags:
    updated_since_selected: bool = True
    element_selected: bool = True
    manufacturer_selected: bool = True
    model_selected: bool = True


@dataclass
class _CatalogProperty:
    element: list = field(default_factory=list)
    manufacturer: list = field(default_factory=list)
    model: list = field(default_factory=list)
    level: str = 'configuration'
    updated_since: datetime = datetime.now()
    output_format: str = 'xml'
    nodata: int = 404


class CatalogQuery(NRLQueryPropertyInterface):
    """
    The CatalogQuery class is used to build the /catalog query.
    """
    __BAD_USER_ENTRY = ['', None]

    def __init__(self):
        super().__init__()
        self.catalog_prop = _CatalogProperty()
        self.flag = _CatalogFlags()
        self.__error_handler = True
        logger.debug("CatalogQuery initialized with default properties.")

    def __reset_defaults(self) -> None:
        """
        Reset CatalogQuery variables to their default values
        :return: None
        """
        self.catalog_prop = _CatalogProperty()
        self.flag = _CatalogFlags()
        logger.info("CatalogQuery properties and flags reset to defaults.")

    def set_error_handler(self, status: bool = True) -> None:
        """
        Change the status of the error handler for different combine queries.
        True means ignore input errors and continue processing the rest of the
         requests, and False means terminate the process and return the error
        message.
        :param status: Set the status of the error handler
        :return: None
        """
        self.__error_handler = status
        logger.info(f"Error handler set to {status}.")

    def build_query(self, nrl_property: dict) -> str:
        """
        Implementation of the build_query method for the catalog query. This
        query needs the following parameters:

        nodata: Specify which HTTP status code is returned when no data is found. 404 or 204

        - 404: Refresh the browser window, leaving a blank or nearly blank screen if no data is returned.
        - 204: Do not refresh the browser window if no data is returned.

        element: Filter by element type. Current elements include sensor, datalogger, integrated and soh. Wild cards * and ? are supported as well.

        manufacturer: Filter by manufacturer

        model: Filter by model.

        level: Specify the level of desired detail. Accepted values are element, manufacturer, model and configuration.

        updatedsince: Filter for information updated on or since the beginning day boundary of this date (UTC).

        format: Specify output format. Accepted values are json, xml, and text.

        :param nrl_property: a dictionary that contains keys, "element", "manufacturer", "model", "updated_since"  "format" and "nodata", and their respective values.
        :return: The query string part of the final URL that will be used to construct the catalog query. The string format of the output will be: /catalog? [selection-options] [reference-options] [format-options] [nodata-options]
        """  # noqa: E501
        logger.debug(f"Building catalog query with input: {nrl_property}")
        self.__reset_defaults()
        # Make sure the user has provided the updated_since entry.
        if ('updated_since' not in nrl_property or
                nrl_property['updated_since'] is None):
            self.flag.updated_since_selected = False

        self.__build_catalog_property(nrl_property)

        params = []
        if self.flag.element_selected and self.catalog_prop.element:
            params.append(self.__build_element())
        if self.flag.manufacturer_selected and self.catalog_prop.manufacturer:
            params.append(self.__build_manufacturer())
        if self.flag.model_selected and self.catalog_prop.model:
            params.append(self.__build_model())

        params.append(self.__build_level())

        if self.flag.updated_since_selected:
            params.append(self.__build_updated_since())

        params.append(self.__build_output_format())
        params.append(self.__build_nodata())
        catalog_query_output = f"catalog?{'&'.join(filter(None, params))}"
        logging.info(f"Catalog query: {catalog_query_output}")
        logger.info("Catalog query built successfully.")
        return catalog_query_output

    def __build_catalog_property(self, user_input: dict) -> None:
        """
        Check the validity of the user input for the catalog query.
        :param user_input:  The user input dictionary that contains keys,
        "nodata", "element", "manufacturer", "model", "level", "format", and
        "updated_since" and their respective values
        :return: None
        """
        logger.debug(f"Building catalog property from user input: {user_input}")
        if user_input is None:
            if self.__error_handler:
                logger.error("Error: No data provided for the catalog query!")
            else:
                logger.critical("No data provided for the catalog query! The "
                                "input dictionary must contain the following "
                                "key/value pairs: nodata, element, "
                                "manufacturer, model, level, format, and "
                                "updated_since")
                raise ValueError("No data provided for the catalog query! The "
                                 "input dictionary must contain the following "
                                 "key/value pairs: nodata, element, "
                                 "manufacturer, model, level, format, and "
                                 "updated_since")
        # First check and see if the user has provided the entry for any of
        # the following parameters
        if 'element' not in user_input:
            self.flag.element_selected = False
        if 'manufacturer' not in user_input:
            self.flag.manufacturer_selected = False
        if 'model' not in user_input:
            self.flag.model_selected = False
        if 'level' not in user_input:
            if self.__error_handler:
                logger.warning('The entry, level, is missing. The default  '
                               'value, configuration, will be used.')
                self.__validate_level('configuration')
            else:
                logger.error('The entry, level, is missing. The default '
                             'value, configuration, will be used.')
                self.__validate_level('configuration')
        else:
            self.__validate_level(user_input.get('level', 'configuration'))

        for key, value in user_input.items():
            if key == 'element':
                self.__validate_element(value)
            elif key == 'manufacturer':
                self.__validate_manufacturer(value)
            elif key == 'model':
                self.__validate_model(value)
            elif key == 'level':
                # Already handled above
                pass
            elif key == 'format':
                self.__validate_output_format(value)
            elif key == 'updated_since':
                self.__validate_updated_since(value)
            elif key == 'nodata':
                self.__validate_nodata(value)
            else:
                logging.warning(f'Wrong key, {key}, is passed to the '
                                f'dictionary. It will be ignored.')
                print(f'Wrong key, {key}, is passed to the dictionary. It will'
                      f' be ignored.')
        logger.info("Catalog property built.")

    def __validate_nodata(self, nodata: str) -> None:
        """
        Validate and assign the correct "nodata" value for the catalog lookup
        :param nodata: User entry for the nodata value
        :return: None
        """
        logger.debug(f"Validating nodata: {nodata}")
        if nodata in VALID_NODATA:
            self.catalog_prop.nodata = nodata
        else:
            logging.warning(f"The value, {nodata}, is not a valid input for "
                            f"the nodata. The default nodata value, 204, "
                            f"chosen")
            self.catalog_prop.nodata = 404
        logger.info(f"Nodata validated: {nodata}")

    def __build_nodata(self) -> str:
        """
        Return the string presentation of the nodata value
        :return: string presentation of the nodata value
        """
        logger.debug("Building nodata string.")
        return f'nodata={self.catalog_prop.nodata}'

    def __validate_element(self, element: list) -> None:
        """
        Validate and assign the correct "element" value for the catalog query
        :param element: The user entry for the list of elements.
        :return: None
        """
        logger.debug(f"Validating element: {element}")
        # if no entry or empty entry for element, then change the flag to false
        # and return empty string for element
        if not self.flag.element_selected or element in self.__BAD_USER_ENTRY:
            self.flag.element_selected = False
            self.catalog_prop.element = []
            return
        for item in element:
            if is_valid_element(item.lower()):
                self.catalog_prop.element.append(item)
            else:
                if self.__error_handler:
                    logger.error(f'The entry, element, {item}, is invalid.')
                    print(f'The entry for element attribute, {item}, is not '
                          f'valid. The entry will be excluded from the query.')
                else:
                    logger.critical(f'The entry, element, {item}, is invalid.')
                    raise ValueError(f"The entry '{item}' is not a valid "
                                     f"input for the element!")
        logger.info(f"Element validated: {element}")

    def __build_element(self) -> str:
        """
        Return the string presentation of the element entry
        :return: The string presentation of the element list
        """
        logger.debug("Building element string.")
        if not self.flag.element_selected:
            return ''
        str_element = ','.join(self.catalog_prop.element)
        return f'element={str_element}'

    def __validate_manufacturer(self, manufacturer: list) -> None:
        """
        Validate and assign the correct "manufacturer" value for the catalog
        query
        :param manufacturer: The user entry for the manufacturer value
        :return: None
        """
        logger.debug(f"Validating manufacturer: {manufacturer}")
        # TODO: improve this method to capture the incorrect entry for the
        #  manufacturer. One way to improve the error checking is having a
        #  dictionary of all manufacturers for sensors, dataloggers, etc. and
        #  compare the entry with the valid ones. The dictionary can be
        #  updated periodically to make sure the list is up to date.
        if (not self.flag.manufacturer_selected or
                manufacturer in self.__BAD_USER_ENTRY):
            self.flag.manufacturer_selected = False
            self.catalog_prop.manufacturer = []
            return
        for mnfr in manufacturer:
            self.catalog_prop.manufacturer.append(mnfr)
        logger.info(f"Manufacturer validated: {manufacturer}")

    def __build_manufacturer(self) -> str:
        """
        Return the string presentation of the manufacturer list
        :return: The string presentation of the manufacturer list
        """
        logger.debug("Building manufacturer string.")
        if not self.flag.manufacturer_selected:
            return ''
        str_manufacturer = ','.join(self.catalog_prop.manufacturer)
        return f'manufacturer={str_manufacturer}'

    def __validate_model(self, model: list) -> None:
        """
        Validate and assign the correct "model" value for the catalog query
        :param model: The user entry for the model value
        :return: None
        """
        # TODO: improve this method to capture the incorrect entry for the
        #  model. One way to improve the error checking is having a dictionary
        #  of all models for sensors, dataloggers, etc. and compare the entry
        #  with the valid ones. The dictionary can be updated periodically to
        #  make sure the list is up to date.
        """
        If no element is passed to the method, the default value, '*', will be
        chosen.
        """
        logger.debug(f"Validating model: {model}")
        if not self.flag.model_selected or model in self.__BAD_USER_ENTRY:
            self.flag.model_selected = False
            self.catalog_prop.model = []
            return
        for mdl in model:
            self.catalog_prop.model.append(mdl)
        logger.info(f"Model validated: {model}")

    def __build_model(self) -> str:
        """
        Return the string presentation of the model list
        :return: The string presentation of the model list
        """
        logger.debug("Building model string.")
        if not self.flag.model_selected:
            return ''
        str_model = ','.join(self.catalog_prop.model)
        return f'model={str_model}'

    def __validate_level(self, level: str) -> None:
        """
        Validate and assign the correct "level" value for the catalog query
        :param level: The user entry for the level value
        :return: None
        """
        logger.debug(f"Validating level: {level}")
        if level.lower() not in VALID_LEVEL:
            if self.__error_handler:
                # TODO: Replace the print statement with logging
                print(f"Invalid entry: {level} for the level attribute.")
                print("The default value, configuration is chosen")
                self.catalog_prop.level = 'configuration'
            else:
                raise ValueError(f"Invalid entry: {level} for the level.")
        else:
            self.catalog_prop.level = level.lower()
        logger.info(f"Level validated: {level}")

    def __build_level(self) -> str:
        """
        Return the string presentation of the level
        :return: The string presentation of the level
        """
        logger.debug("Building level string.")
        return f'level={self.catalog_prop.level}'

    def __validate_output_format(self, output_format: str) -> None:
        """
        Validate and assign the correct "format" value for the catalog query
        :param output_format: The user entry for the output format value
        :return: None
        """
        logger.debug(f"Validating output format: {output_format}")
        if output_format.lower() in VALID_OUTPUT_FORMAT:
            self.catalog_prop.output_format = output_format.lower()
        else:
            print(f"The value, {output_format}, is not a valid input for the "
                  f"format. The default format, xml, chosen.")
        logger.info(f"Output format validated: {output_format}")

    def __build_output_format(self) -> str:
        """
        Return the string presentation of the output format
        :return: The string presentation of the output format
        """
        logger.debug("Building output format string.")
        return f'format={self.catalog_prop.output_format}'

    def __validate_updated_since(self, updated_since: datetime) -> None:
        """
        Validate and assign the correct "updated_since" value for the catalog
        query
        :param updated_since: The user entry for the updated_since value
        :return: None
        """
        logger.debug(f"Validating updated_since: {updated_since}")
        # Reset the time part of the entry to the beginning of the day
        self.catalog_prop.updated_since = updated_since.strftime('%Y-%m-%d')
        logger.info(f"Updated since validated: {updated_since}")

    def __build_updated_since(self) -> str:
        """
        Return the string presentation of the updated_since
        :return: The string presentation of the updated_since
        """
        logger.debug("Building updated_since string.")
        if not self.flag.updated_since_selected:
            logger.warning("updated_since_selected flag is False, "
                           "skipping updated_since.")
            return ''
        return f'updatedsince={self.catalog_prop.updated_since}'
