import re
from typing import List, Union


def extract_ids(string) -> Union[List[str], None]:
    """Extracts and returns a list of unique identifier strings from a given input string.

    The function uses a regular expression to match identifiers in the format:
    "XXXXXXXX_XXXX_XXXX_XXXX_XXXXXXXXXXXX", where "X" represents a word character (alphanumeric
    or underscore). If no matches are found, the function returns an empty list.

    Parameters:
        string (str): The input string from which to extract IDs.

    Returns:
        Union[List[str], None]: A list of matched ID strings if found, or an empty list otherwise.
    """
    regex = r"\w{8}_\w{4}_\w{4}_\w{4}_\w{12}"

    matches = re.findall(regex, string)

    return matches
