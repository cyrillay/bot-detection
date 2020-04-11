"""
Contains methods that operate on an Apache server log dataframe.
Each method corresponds to a detection rule, and returns a list of the hosts matching the rule. 
"""


def has_robots_txt_request(requests_df):
    """:returns hosts that once requested the `robots.txt` file"""
    return requests_df[requests_df["request"].str.contains("robots.txt")][
        "host"
    ].unique()


def has_bot_name_in_user_agent(requests_df, known_bot_names=None):
    """:returns hosts that had a known bot name appear at least once in their user-agent"""
    if known_bot_names is None:
        known_bot_names = ["Googlebot", "bingbot", "bot", "crawler", "spider"]
    filter_condition = "|".join(known_bot_names).lower()
    df_bots = requests_df[
        requests_df["user_agent"].str.lower().str.contains(filter_condition)
    ]["host"].unique()
    return df_bots


def has_low_request_interrarival_time(
    sessions_df,
    threshold_request_interarrival_time=20,
    threshold_number_requests_no_referrer=30,
):
    """
    :returns hosts that have an average inter-request time below `threshold_request_interarrival_time` (seconds) across
    their daily sessions. In an attempt to avoid false positives on sub-sequent requests for assets of a page, only
    sessions with more than `number_requests_no_referrer` are considered.
    """
    df_bots = sessions_df[
        (
            sessions_df["number_requests_no_referrer"]
            > threshold_number_requests_no_referrer
        )
        & (
            sessions_df["avg_request_interarrival_time"]
            < threshold_request_interarrival_time
        )
    ]
    return df_bots["host"].unique()


def has_high_number_requests(sessions_df, threshold=1500):
    """
    :returns hosts that had more than `threshold` requests in one of their sessions
    """
    return sessions_df[sessions_df["number_requests_total"] > threshold][
        "host"
    ].unique()


# TODO : Add other detection rules : has_low_image_to_page_requests_ratio, etc..