"""
Set up the filter for the logger.
    Logging filter: Show log messages below input level.
    - CRITICAL = 50
    - FATAL = CRITICAL
    - ERROR = 40
    - WARNING = 30
    - WARN = WARNING
    - INFO = 20
    - DEBUG = 10
    - NOTSET = 0
"""
import logging


class InfoFilter(logging.Filter):
    """
    A logging filter that allows only log records with the INFO level to pass through.

    This filter can be used in custom loggers to restrict logging output to only informational
    messages, filtering out messages with other levels (e.g., DEBUG, WARNING, ERROR, etc.).

    Attributes:
        name (str): The name of the filter, used to identify this specific filter instance.
    """
    def __init__(self):
        """
        Initializes the InfoFilter instance with a specific name.

        The name 'filter_info_logs' is used to distinguish this filter when added to a logger.
        This name can be helpful in managing multiple filters within the same logging configuration.
        """
        super().__init__(name='filter_info_logs')

    def filter(self, record):
        """
        Return Log Record Object based on condition - Return only info logs

        keyword arguments:
        record -- (logging_setup.LogRecord) Log Record Object

        return: True if record level is Logging.INFO, else False
        """
        assert isinstance(record, logging.LogRecord)
        return record.levelno == logging.INFO


class LevelPassFilter:
    """
    A custom logging filter that allows only log messages of a
    specific logging level to pass through. When applied to a logger,
    this filter will restrict the output to log records that match the
    specified logging level, ignoring all other log levels.
    """
    def __init__(self, level):
        self.__level = level

    def filter(self, record):
        """
        Filters log records to pass only those that match the specified
        logging level.

        This method checks the log level of the provided log record and
        determines whether it matches the level specified during the filter's
        initialization. Only log records with this exact level are allowed
        to pass through, while others are filtered out.

        keyword arguments:
        record -- (logging_setup.LogRecord) The log record object containing
        all the information pertinent to the event being logged.

        return:
        bool: True if the log record's level matches the specified level,
        allowing it to be processed and displayed. Returns False if the log
        record's level does not match, causing it to be ignored.

        Example:
            If the filter is initialized with `logging.ERROR`, only log
            messages with the level `ERROR` will pass through, and all other
            levels such as `DEBUG`, `INFO`, or `WARNING` will be filtered out.
        """
        return record.levelno == self.__level
