import re
import pandas as pd
from datetime import datetime
import datetime as dt

# TODO : A class could be created for Apache log objects

HOST = r"^(?P<host>.*?)"
SPACE = r"\s"
IDENTITY = r"\S+"
USER = r"\S+"
TIME = r"(?P<timestamp>\[.*?\])"
REQUEST = r"\"(?P<request>.*?)\""
STATUS = r"(?P<status>\d{3})"
SIZE = r"(?P<size>\S+)"
REFERER = r"(?P<referrer>\S+)"
USER_AGENT = r"(?P<user_agent>\"(.+?)\")"
LOG_REGEX = (
    HOST
    + SPACE
    + IDENTITY
    + SPACE
    + USER
    + SPACE
    + TIME
    + SPACE
    + REQUEST
    + SPACE
    + STATUS
    + SPACE
    + SIZE
    + SPACE
    + REFERER
    + SPACE
    + USER_AGENT
)


def _parser(log_line):
    """
    Contains the parsing logic to extract host, request time, status code returned, size of the server response and
    user-agent from the Apache log line
    """
    match = re.search(LOG_REGEX, log_line)
    if not match:
        return None
    else:
        return (
            match.group("host"),
            match.group("timestamp"),
            match.group("request"),
            match.group("status"),
            match.group("size"),
            match.group("referrer"),
            match.group("user_agent"),
        )


def parse_log_file(path, from_date: dt.date = None):
    """
    Reads and parses lines from the Apache .log file at `path` and returns it as a dataframe.
    This methods assumes the log file is chronological, it is read from the end until the `from_date` is reached.
    TODO : Make this method more flexible for back filling : add a until_date parameter
    """
    if not from_date:
        from_date = dt.date(2020, 3, 20)
    data = {
        "host": [],
        "timestamp": [],
        "request": [],
        "status": [],
        "size": [],
        "referrer": [],
        "user_agent": [],
    }
    with open(path, "r") as file:
        lines = file.readlines()
        for line in reversed(lines):
            parsed_log_line = _parser(line)
            if parsed_log_line:
                (
                    host,
                    time,
                    request,
                    status,
                    size,
                    referrer,
                    user_agent,
                ) = parsed_log_line
            else:
                continue
            parsed_date = datetime.strptime(time, "[%d/%b/%Y:%H:%M:%S %z]")
            if parsed_date.date() < from_date:
                break
            data["host"].append(host)
            data["timestamp"].append(parsed_date)
            data["request"].append(request)
            data["status"].append(status)
            data["size"].append(size)
            data["referrer"].append(referrer)
            data["user_agent"].append(user_agent)
    return pd.DataFrame(data)
