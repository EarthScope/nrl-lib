"""
This module is used to set up root logging_setup configuration,
If LOG_CFG variable is set, then use it for logging_setup configuration path.
Since we are using yaml configuration, we need yaml module to load
    configuration file.
Set Root logger configuration using `logging_setup.config.dictConfig()`.
Any exception results in setting up root logger in default configuration.
"""
import logging
import logging.config
import os
import sys
from pathlib import Path
from typing import Optional

import yaml

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.WARNING)
LOG_FILE_PATH: Optional[Path] = None


def setup_logging(default_name='logging.config', default_level=logging.INFO,
                  env_key='LOG_CFG'):
    """
    Setup logging function
    keyword arguments:
    default_name -- (str) Logging configuration file name
    default_level -- (int) Default logging_setup level
    env_key -- (str) Logging config path set in environment variable
    """
    # Create the LOG directory if needed. The end user can use the default path
    global LOG_FILE_PATH
    if LOG_FILE_PATH is None:
        LOG_FILE_PATH = __create_logging_folder()

    # Check and see if logging config path is set in environment variable. If
    # not return None
    value = os.getenv(env_key, None)
    if value is None:
        # Grab the location of the config file
        file_path = Path(__file__)
        location = (Path.cwd() / file_path.parent).resolve()
        path = location.joinpath(default_name)
    else:
        # If value is None then use the path to custom log config file.
        path = Path(value)

    if path.exists():
        with open(path, 'rt') as cnf:
            try:
                config = yaml.safe_load(cnf.read())
                # Read the config file and dynamically modify the filename
                # variable in the config file. This method is safer than using
                # !!python/eval method inside the yaml method.
                __edit_config_filename(config)
                logging.config.dictConfig(config)
            except Exception as err:
                logging.error('Error in Logging Configuration. %s', err)
                logging.warning('Using default configs!!')
                logging.basicConfig(level=default_level, stream=sys.stdout)
    else:
        logging.basicConfig(level=default_level, stream=sys.stdout)
        logging.warning('Failed to load configuration file. Using default '
                        'configs')


def __create_logging_folder(destination: Optional[str] = None) -> Path:
    """
    Create a folder for logging.
    :param destination: The path to logging folder
    :type destination: Optional[str]
    :rtype: Path
    """
    if destination is None:
        folder_path = Path.home() / 'NRL_log'
    else:
        folder_path = Path(destination) / 'NRL_log'
    try:
        folder_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating folder: {e}")
    return folder_path


def set_default_path(destination: Optional[str] = None) -> None:
    """
    Set a new path for saving log files
    :param destination: Path to the folder to keep log files
    :type destination: str
    """
    global LOG_FILE_PATH
    LOG_FILE_PATH = __create_logging_folder(destination)


def change_log_path(destination: str, logger: logging.Logger) ->\
        logging.Logger:
    """
    Change the logging path dynamically. This method provides the
    functionality to change the destination of the logging to whatever user
    wants
    :param destination: The parent directory to keep logs
    :type destination: str
    :param logger: The current logger in use.
    :type logger: logging.Logger
    :return: The new logger
    :rtype: logging.Logger
    """
    root_logger = logger
    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.close()
            root_logger.removeHandler(handler)
    set_default_path(destination)
    setup_logging(default_level=logging.INFO)
    return logging.getLogger(__name__)


def __edit_config_filename(config):
    config['handlers']['info_file_handler']['filename'] = str(
        LOG_FILE_PATH / 'info.log')
    config['handlers']['debug_file_handler']['filename'] = str(
        LOG_FILE_PATH / 'debug.log')
    config['handlers']['warn_file_handler']['filename'] = str(
        LOG_FILE_PATH / 'warn.log')
    config['handlers']['error_file_handler']['filename'] = str(
        LOG_FILE_PATH / 'error.log')
    config['handlers']['critical_file_handler']['filename'] = str(
        LOG_FILE_PATH / 'critical.log')
