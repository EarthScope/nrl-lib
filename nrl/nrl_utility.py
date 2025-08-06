"""
This module is maintaining the utilities that are needed for the library to
work properly
"""
import logging
import re
from nrl.nrl_q_property import VALID_ELEMENT

logger = logging.getLogger(__name__)


def __convert_wildcard_to_regex(pattern: str) -> str:
    """
    convert the wildcard pattern to a regular expression
    :param pattern: A string with wildcards (?, *)
    :type pattern: str
    :return: A string representing the equivalent regular expression
    :rtype: str
    """
    # Escape special regex characters except for * and ?
    logger.debug(f"Converting wildcard pattern '{pattern}' to regex.")
    pattern = re.escape(pattern)
    # Replace the escaped * and ? back to their wildcard meanings
    pattern = (pattern.replace(r'\*', '.*')
               .replace(r'\?', '.'))
    # Ensure the pattern matches the entire string
    regex_pattern = '^' + pattern + '$'
    logger.debug(f"Converted '{pattern}' to regex '{regex_pattern}'")
    return regex_pattern


def is_valid_element(input_str) -> bool:
    """
    Check if the input string matches any of the valid elements or their
    wildcard representations.
    :param input_str: The input string to check
    :type input_str: str
    :return: True if the input string matches any valid element or its
    wildcard representations. False otherwise.
    :rtype: bool
    """
    wildcard_pattern = __convert_wildcard_to_regex(input_str)
    logger.debug(f"Checking if '{input_str}' with regex '{wildcard_pattern}' "
                 f"is a valid element.")
    # Check for wildcard matches
    for element in VALID_ELEMENT:
        if re.match(wildcard_pattern, element):
            logger.debug(f"'{input_str}' matched valid element '{element}'.")
            return True

    logger.debug(f"'{input_str}' did not match any valid element.")
    return False
