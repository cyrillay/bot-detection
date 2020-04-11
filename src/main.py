from data_processing import pre_processing, _window_logs, get_session_attributes
from parsing import parse_log_file
from detection_rules import (
    has_robots_txt_request,
    has_bot_name_in_user_agent,
    has_high_number_requests,
    has_low_request_interrarival_time,
)
import numpy as np
import datetime as dt

# Processing the input
print("Starting app...")
parsed_logs = parse_log_file("./access.log", from_date=dt.date(2014, 2, 20))
requests = pre_processing(parsed_logs)

# Generating features
hourly_windowed_logs = _window_logs(requests, window_time_frame="hour")
daily_windowed_logs = _window_logs(requests, window_time_frame="day")
hour_sessions = get_session_attributes(requests, aggregation_level="hour")
day_sessions = get_session_attributes(requests, aggregation_level="day")

# Examine generated features to flag potential bots
robots_txt = has_robots_txt_request(requests)
bot_names = has_bot_name_in_user_agent(requests)
low_inter_request_time_hour = has_low_request_interrarival_time(hour_sessions, threshold_number_requests_no_referrer=100)
low_inter_request_time_day = has_low_request_interrarival_time(day_sessions, threshold_number_requests_no_referrer=1000)

high_number_requests_hour = has_high_number_requests(hour_sessions, threshold=100)
high_number_requests_day = has_high_number_requests(day_sessions, threshold=1000)

potential_bot_hosts = np.unique(
    np.concatenate(
        (
            robots_txt,
            bot_names,
            low_inter_request_time_hour,
            low_inter_request_time_day,
            high_number_requests_hour,
            high_number_requests_day,
        )
    )
)
for host in potential_bot_hosts:
    print(host)
potential_bot_requests = daily_windowed_logs[
    daily_windowed_logs["host"].isin(potential_bot_hosts)
]
# print(potential_bot_requests)

# TODO :
#  - 30 minutes windows instead of a full hour, with initial and final phase as in the paper
#  - Evaluate if using columns as first class members instead of strings could be better
#       (df.timestamp vs df["timestamp"])
# TODO : save potential bots in a report file :
# Format could be :
# | host_ip | user_agent | has_robots_txt_request | has_bot_name_in_user_agent | has_low_inter_request_time_hour | ... | sample_session |
# | 127..*  | Mozilla..  | True                   | False                      | True                            | ... | <list of the requests of one flagged session> |
