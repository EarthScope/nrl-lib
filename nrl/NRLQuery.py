"""
The main module in the library that sends the query to the NRL web service
and handles the response in different ways.
End users are mainly need to deal with this module to communicate with the NRL
web service.
"""
import json
import os
from datetime import datetime

import re
import requests
from typing import Optional, Union
from pathlib import Path
from nrl.urlbuild import URLBuild
from nrl.combine_query import CombineQuery
from nrl.catalog_query import CatalogQuery
from nrl.prefix_lookup_query import PrefixLookupQuery

SUPPORTED_QUERY = ['combine', 'catalog', 'prefix-lookup']


class NRLQuery:
    """
    The NRLQuery class is responsible for communicating with the NRL
    web service
    """

    def __init__(self):
        self.url: str = ''
        self.response = None
        self.nrl_property: dict = dict()
        self.url_builder = URLBuild()
        self.combine_query = CombineQuery()
        self.catalog_query = CatalogQuery()
        self.prefix_lookup_query = PrefixLookupQuery()

    def __reset_defaults(self):
        """
        Reset the instance values of the NRLQuery class
        :return: None
        """
        self.url = ''
        self.response = None
        self.nrl_property = dict()

    def nrl_query(self, query_type: str, nrl_query_property: dict) -> (
            Optional)[requests.Response]:
        """
        Receive the query type (/combine, /catalog, /prefix_lookup) and the
        dictionary that contains necessary information about the requested
        query.
        The nrl_query_property should provide adequate information to build
        the query section of the URL that is being sent to the NRL web service
        to receive the response from the remote service.
        Check the documentation on the website to make sure you know what needs
        to be passed to the method.
        Link: http://service.iris.edu/irisws/nrl/1/
        Three different queries available for the NRL web service and here is
        the detail on how to build the dictionary for each query.

        1. /Combine:
            1.1 The first config is when the user send instconfig
                ```
                nrl_query_property = {
                'instconfig': str,
                'updated_since': datetime --> can be None,
                'format': str,
                'nodata': int,
                'epoch': dict}
                The Epoch dictionary is:
                epoch = {
                'network': str,
                'station': str,
                'location': str,
                'channel':  str,
                'start_time': datetime --> can be None,
                'end_time': datetime --> can be None,
                }
                ```
            1.2 The second config is when the user sends Element/Manufacturer/
            Model
                ```
                nrl_query_property = {
                'element': list --> can be None,
                'manufacturer': list --> can be None,
                'model': list --> can be None,
                'updated_since': datetime --> can be None,
                'format': str,
                'nodata': int,
                'epoch': dict}
                The Epoch dictionary is:
                epoch = {
                'network': str,
                'station': str,
                'location': str,
                'channel': str,
                'start_time': datetime --> can be None,
                'end_time': datetime --> can be None,
                }
                ```
        2. /Catalog:
            ```
            nrl_query_property = {
            'element': list --> can be None,
            'manufacturer': list --> can be None,
            'model': list --> can be None,
            `level`: str --> can be None,
            'updated_since': datetime,
            'format' = str,
            'nodata': int --> can be None,
            }
            ```
        3. /Prefix-lookup:
            ```
            nrl_query_property = {
            'format': str --> can be None,
            'nodata': int --> can be None,
            }
            ````
        :param query_type: The type of query  that should be sent to the NRL
        web service
        :type query_type: str
        :param nrl_query_property: The required information for the specific
        type of query that is being built
        :type nrl_query_property:  dict
        :return: The response from the NRL web service
        :rtype: requests.Response
        """
        self.__reset_defaults()
        self.nrl_property = nrl_query_property
        if query_type not in SUPPORTED_QUERY:
            raise ValueError(f'The query type {query_type} is not a valid '
                             f'type. NRL web service supports /catalog, '
                             f'/prefix-lookup, and /combine types ')
        if query_type == 'combine':
            combine_query_response = self.__combine_query(self.nrl_property)
            return combine_query_response
        elif query_type == 'catalog':
            catalog_query_response = self.__catalog_query(self.nrl_property)
            return catalog_query_response
        elif query_type == 'prefix-lookup':
            prefix_lookup_query_response = self.__prefix_lookup_query(
                self.nrl_property)
            return prefix_lookup_query_response
        return None

    def __combine_query(self, combine_query_property: dict) -> (
            requests.Response):
        """
        Use the CombineQuery class to build the query section of the NRL web
        service
        :param combine_query_property: The required information for the
        combine query that is being built
        :type combine_query_property: dict
        :return: Response from the NRL web service
        :rtype: requests.Response
        """
        # Create the query section of the URL
        comb_query = self.combine_query.build_query(combine_query_property)

        # Build the entire URL
        comb_url = self.__assemble_url(comb_query)
        # Send the request to the NRL web service
        nrl_response = NRLQuery.__send_query(comb_url)
        return nrl_response

    def __catalog_query(self, catalog_query_property: dict) -> (
            requests.Response):
        """
        Use the CatalogQuery class to build the query section of the NRL web
        service
        :param catalog_query_property: The required information for the
         catalog query that is being built
        :type catalog_query_property: dict
        :return: Response from the NRL web service
        :rtype: requests.Response
        """
        # Create the query section of the URL
        cat_query = self.catalog_query.build_query(catalog_query_property)

        # Build the entire URL
        cat_url = self.__assemble_url(cat_query)

        # Send the request to the NRL web service
        nrl_response = NRLQuery.__send_query(cat_url)
        return nrl_response

    def __prefix_lookup_query(self, prefix_lookup_query_property: dict) -> (
            requests.Response):
        """
        Use the PrefixLookupQuery class to build the query section of the NRL
         web servie
        :param prefix_lookup_query_property: The required information for the
         catalog query that is being build
        :type prefix_lookup_query_property: dict
        :return: Response from the NRL web service
        :rtype: requests.Response
        """
        # Create the query section of the URL
        prefix_lookup_query = self.prefix_lookup_query.build_query(
            prefix_lookup_query_property)

        # Build the entire URL
        prefix_url = self.__assemble_url(prefix_lookup_query)

        # Send the request to the NRL web service
        nrl_response = NRLQuery.__send_query(prefix_url)
        return nrl_response

    def __assemble_url(self, query_str: str) -> str:
        """
        Assemble the final URL
        :param query_str: The query section of the URL
        :type query_str: str
        :return: The completed URL
        :rtype: str
        """
        final_url = self.url_builder.build_url(query_str)
        return final_url

    @staticmethod
    def __send_query(url: str) -> requests.Response:
        """
        Send the query to the NRL web service
        :param url: The built url of the NRL web service
        :return: The response file from the NRL web service
        """
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        # Raise an exception for 4xx or 5xx status code
        response.raise_for_status()
        return response

    @staticmethod
    def write_to_file(response: requests.Response,
                      dl_path: Optional[Path] = None) -> None:
        """
        Write the remote server response to a file with correct format
        :param response: Response from the NRL web service
        :type response: requests.Response
        :param dl_path: Path to the folder to save the downloaded file(s)
        :type dl_path: pathlib.Path
        :return: None
        """
        if dl_path is None:
            dl_path = NRLQuery.__path_home_directory()
            print(f'No path is chosen to download response files. the default'
                  f' path, {dl_path}, has been selected.')
        else:
            Path(dl_path).mkdir(parents=True, exist_ok=True)
        # If no content is return from the remote server then no file name can
        # be extracted from the headers
        cont_disposition, file_exten, file_name = (
            NRLQuery.__get_meta_data(response))
        # Rename the file to solve the disappearing files problem.
        file_name = NRLQuery.__rename_file_name_time_stamp(file_name)
        destination = dl_path / file_name
        # Try to save the file based on the format.
        # Downloading zip or xml files need special attention -> byte
        if file_exten in ['zip', 'xml']:
            NRLQuery.__write_zip_xml_file(destination, response)
        # Handle the json format
        elif file_exten == 'json':
            NRLQuery.__write_json_file(destination, response)
        # Handle the resp format
        else:
            NRLQuery.__write_resp_files(destination, response)

    @staticmethod
    def __path_home_directory() -> Path:
        """
        Return the path to ~/.nrl
        :return: the Path to the default download directory
        :rtype: Path
        """
        default_path = (Path.home() / '.nrl')
        default_path.mkdir(parents=True, exist_ok=True)
        return default_path

    @staticmethod
    def __check_file_exists(destination: Path, file_name: str) -> bool:
        file_path = Path(destination) / file_name
        return file_path.is_file()

    @staticmethod
    def __rename_file_name(destination: Path, file_name: str) -> str:
        file_path = Path(destination) / file_name
        new_file_path = file_path
        counter = 1
        while new_file_path.is_file():
            stem = new_file_path.stem
            suffix = new_file_path.suffix
            new_file_path = new_file_path.with_name(
                f"{stem}_{counter}{suffix}")
            counter += 1
        return file_path.rename(new_file_path).name

    @staticmethod
    def __rename_file_name_time_stamp(file_name: str) -> str:
        time_stamp = str(datetime.now().strftime('%Y-%m-%dT%H_%M_%S_%f'))
        prefix = NRLQuery.__extract_prefix(file_name)
        split_file_name = file_name.split('.')
        if len(split_file_name) == 2:
            exten = split_file_name[-1]
        else:
            exten = '.'.join(split_file_name[-2:])
        new_file_name = f"{prefix}-{time_stamp}.{exten}"
        return new_file_name

    @staticmethod
    def __extract_prefix(file_name: str) -> str:
        # Using regular expression to match the pattern
        # The input string will be something like
        # "nrl-2024-07-15T13:48:03.184257.stationxml"
        # or
        # "nrl-2024-07-15T13:48:03.184257.stationxml.zip"
        # or
        # "irisws-nrl-2024-07-15T13:48:01.791934.resp"
        #
        # This regex will split the string into three parts:
        # 1) "nrl" or "irisws-nrl"
        # 2) "2024-07-15T13:48:03.184257"
        # 3) "stationxml" or "stationxml.zip" or "resp"
        match = re.match(r'([\w-]+)_\d{4}-\d{2}-\d{2}T.*(\.\w+)$', file_name)

        if match:
            return match.group(1)
        else:
            # or you could return a default value or raise an exception
            return ''

    @staticmethod
    def __get_meta_data(data: requests.Response) -> tuple:
        try:
            cont_disposition = data.headers.get('content-disposition')
            assert cont_disposition is not None
            file_exten = ((cont_disposition.split('.')[-1].replace('"', ''))
                          .strip())
            # Extract file name
            file_name = ((cont_disposition.split('=')[-1].replace('"', ''))
                         .strip())
        except AttributeError as e:
            print(f'Problem downloading file: {e}')
            return ()

        return cont_disposition, file_exten, file_name

    @staticmethod
    def __write_resp_files(destination: Path, data: requests.Response) -> bool:
        try:
            # time.sleep(1)
            with open(destination, 'w', encoding='utf-8') as out:
                for line in data.iter_lines(decode_unicode=True):
                    out.write(line + '\n')
        except ValueError as e:
            print("Error downloading file", e)
            return False
        return True

    @staticmethod
    def __write_json_file(destination: Path, data: requests.Response) -> bool:
        try:
            with open(destination, 'w', encoding='utf-8') as out:
                json.dump(data.json(), out, ensure_ascii=False,
                          indent=4)
                out.flush()
                os.fsync(out.fileno())
        except ValueError as e:
            print('Error downloading file: ', e)
            return False
        return True

    @staticmethod
    def __write_zip_xml_file(destination: Path, data: requests.Response) ->\
            bool:
        try:
            with open(destination, 'wb') as out:
                for chunk in data.iter_content(chunk_size=8192):
                    if chunk:
                        out.write(chunk)
        except requests.exceptions.RequestException as e:
            print("Error download file", e)
            return False
        return True

    def set_error_handler(self, status: Optional[Union[dict, bool]] = True):
        """
        Set the error handler flag for combine, catalog, and prefix-lookup modules.
        :param status: Boolean to set all, or dict for per-query control.
        :return: None
        """
        if isinstance(status, dict):
            if 'combine' in status:
                self.combine_query.set_error_handler(status['combine'])
            if 'catalog' in status:
                self.catalog_query.set_error_handler(status['catalog'])
            if 'prefix-lookup' in status:
                self.prefix_lookup_query.set_error_handler(
                    status['prefix-lookup'])
        else:
            self.combine_query.set_error_handler(status)
            self.catalog_query.set_error_handler(status)
            self.prefix_lookup_query.set_error_handler(status)
