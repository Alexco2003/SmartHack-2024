import re
from typing import List, Union


def extract_ids(string) -> Union[List[str], None]:
    # regex to match IDs
    regex = r"\w{8}_\w{4}_\w{4}_\w{4}_\w{12}"

    matches = re.findall(regex, string)

    return matches
