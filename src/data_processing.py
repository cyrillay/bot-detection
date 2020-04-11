import pandas as pd


def pre_processing(df):
    """
    Transforms a dataframe of parsed Apache logs to another dataframe with the following transformations :
    - Converts the str timestamp into a datetime
    - Add `day` and `hour` columns
    """
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df["day"] = df["timestamp"].dt.date
    df["hour"] = df["timestamp"].dt.hour
    # TODO : here we could add some data cleaning
    return df


def _window_logs(df, window_time_frame="hour"):
    """
    Utility function to window the dataframe as sessions, facilitates the visualization of the dataframe and debugging.
    """
    aggregation_levels = {"day": ["host", "day"], "hour": ["host", "day", "hour"]}
    if window_time_frame not in aggregation_levels:
        raise ValueError(f"aggregation_level must be one of f{aggregation_levels}.")
    aggregation_columns = aggregation_levels[window_time_frame]

    df = df.sort_values(by=["host", "timestamp"], ascending=True)
    df["timestamp_previous"] = df.groupby(aggregation_columns)["timestamp"].shift(1)
    return df


def get_session_attributes(df, aggregation_level="hour"):
    """
    Aggregates a dataframe of logs and turns it into the following format :
    host | date | hour | number_requests_[GET|POST|HEAD] | number_requests_total | mean_request_interarrival_time |
    127.** | 2020-03-20 | 04 | 25 | 12 | ... |
    """

    # Get the columns to aggregate onto
    # TODO : rename to aggregation_level_to_columns
    aggregation_levels = {"day": ["host", "day"], "hour": ["host", "day", "hour"]}
    if aggregation_level not in aggregation_levels:
        raise ValueError(f"aggregation_level must be one of f{aggregation_levels}.")
    aggregation_columns = aggregation_levels[aggregation_level]

    # Window the dataframe to get the preceding timestamp of each request
    df = df.sort_values(by=aggregation_columns + ["timestamp"], ascending=True)
    df["timestamp_previous"] = df.groupby(aggregation_columns)["timestamp"].shift(1)
    df["timestamp_previous"] = pd.to_datetime(df["timestamp_previous"], utc=True)
    df["request_time_delta"] = (
        df["timestamp"] - df["timestamp_previous"]
    ).dt.total_seconds()

    aggregated_df = (
        df.groupby(aggregation_columns)
        .agg(
            number_requests_GET=pd.NamedAgg(
                column="request",
                aggfunc=(lambda req: (req.str.startswith("GET")).sum()),
            ),
            number_requests_HEAD=pd.NamedAgg(
                column="request",
                aggfunc=(lambda req: (req.str.startswith("HEAD")).sum()),
            ),
            number_requests_POST=pd.NamedAgg(
                column="request",
                aggfunc=(lambda req: (req.str.startswith("POST")).sum()),
            ),
            number_requests_no_referrer=pd.NamedAgg(
                column="referrer",
                aggfunc=(lambda req: (req.str.startswith('"-"')).sum()),
            ),
            number_requests_total=pd.NamedAgg(column="request", aggfunc="count"),
            avg_request_interarrival_time=pd.NamedAgg(
                column="request_time_delta", aggfunc="mean"
            ),
        )
        .reset_index()
    )

    aggregated_df["HEAD_requests_ratio"] = (
        aggregated_df["number_requests_HEAD"] / aggregated_df["number_requests_total"]
    )
    aggregated_df["GET_requests_ratio"] = (
        aggregated_df["number_requests_GET"] / aggregated_df["number_requests_total"]
    )
    aggregated_df["POST_requests_ratio"] = (
        aggregated_df["number_requests_POST"] / aggregated_df["number_requests_total"]
    )
    aggregated_df["no_referrer_requests_ratio"] = (
        aggregated_df["number_requests_no_referrer"]
        / aggregated_df["number_requests_total"]
    )
    # TODO : Add other features : avg request size, page to image requests ratio...
    return aggregated_df
