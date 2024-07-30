import pandas as pd
from datetime import timedelta
import numpy as np
from tqdm.notebook import tqdm

def detect_coordinated_groups(data, time_window=10, min_repetition=2):
    """
    Detect coordinated groups based on input data.

    This function serves as a wrapper for actual calculations.
    It validates the input data before proceeding with the actual calculations.

    :param data: A pandas dataframe containing the columns: "object_id", "id_user", "content_id", "timestamp_share".
        - "object_id" is the identifier for the unique object to be probed for coordination, e.g., cleaned post text, a hashtag, etc. 
        - "id_user" is the identifier for the user who shared the object.
        - "content_id" is the identifier for the shared object, e.g., post ID, hashtag ID, etc. This corresponds to the posts unique id, for example. 
        - "timestamp_share" is the timestamp when the object was shared and should be in standard unix timestamp format.
    :type data: pandas.DataFrame

    :param time_window: Time window in seconds for considering coordination, defaults to 10.
    :type time_window: int

    :param min_repetition: Minimum number of repetitions a user must have before being considered coordinated, defaults to 2.
    :type min_repetition: int

    :return: DataFrame with coordinated group information.
    :rtype: pandas.DataFrame
    """
    # Validate input data
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)
        
    required_columns = ["object_id", "id_user", "content_id", "timestamp_share"]
    
    # Check if all required columns are present in the input data
    for col_name in required_columns:
        if col_name not in data.columns:
            raise ValueError("Columns or their names are incorrect. Ensure your data has the columns: "
                             "object_id, id_user, content_id, timestamp_share")

    print('All columns found')
    
    data = _do_detect_coordinated_groups(data, time_window=time_window, min_repetition=min_repetition)

    return data

def _do_detect_coordinated_groups(data, time_window=10, min_repetition=2):
    """
    Detect coordinated groups within input data.

    :param data: A pandas dataframe containing the columns: "object_id", "id_user", "content_id", "timestamp_share".
    - "object_id" is the identifier for the unique object to be probed for coordination, e.g., cleaned post text, a hashtag, etc. 
    - "id_user" is the identifier for the user who shared the object.
    - "content_id" is the identifier for the shared object, e.g., post ID, hashtag ID, etc. This corresponds to the posts unique id, for example. 
    - "timestamp_share" is the timestamp when the object was shared which should be in unix timestamp format.
    :type data: pandas.DataFrame

    :param time_window: Time window in seconds for considering coordination, defaults to 10.
    :type time_window: int

    :param min_repetition: Minimum number of repetitions a user must have before being considered coordinated, defaults to 2.
    :type min_repetition: int

    :return: DataFrame with coordinated group information.
    :rtype: pandas.DataFrame
    """
    # Initialize variables
    object_id = id_user = content_id = content_id_y = id_user_y = time_delta = None

    print('Beginning coordination check...')

    # --------------------------
    # Pre-filter based on minimum repetitions given that a user must have a number of posts greater than the minimum to be considered coordinated
    data = data.groupby("id_user").filter(lambda group: len(group) > min_repetition)

    def _calc_group_combinations(group, time_window=10):
        """
        Calculate group combinations within a group based on a time window.

        :param group: A subgroup of input data with the same "id_user".
        :type group: pandas.DataFrame

        :param time_window: Time window in seconds for considering coordination, defaults to 10.
        :type time_window: int

        :return: DataFrame with coordinated group combinations.
        :rtype: pandas.DataFrame
        """
        # Reset index and generate new id column
        group = group.reset_index(drop=True)
        group['id'] = group.index

        # Sort by timestamp_share to improve performance
        group = group.sort_values(by='timestamp_share')

        # Convert 'timestamp_share' to numeric values (e.g., seconds)
        timestamp_values = group['timestamp_share'].values.astype('datetime64[s]').astype(np.int64)

        # Calculate time deltas / Difference between each timestamp and every other timestamp
        time_deltas = np.abs(np.subtract.outer(timestamp_values, timestamp_values))

        # Mask rows where time delta is within the time_window
        mask = (time_deltas <= time_window) & (np.triu(np.ones(time_deltas.shape), k=1) > 0)

        # Get row and column indices where mask is True
        row_indices, col_indices = np.where(mask)

        # Create a DataFrame from the indices
        result = pd.DataFrame({
            'object_id': group.iloc[row_indices]['object_id'].values,
            'content_id': group.iloc[row_indices]['content_id'].values,
            'content_id_y': group.iloc[col_indices]['content_id'].values,
            'time_delta': time_deltas[row_indices, col_indices],
            'id_user': group.iloc[row_indices]['id_user'].values,
            'id_user_y': group.iloc[col_indices]['id_user'].values
        })

        # remove loops
        result = result[result["object_id"] != result["content_id"]]
        result = result[result["content_id"] != result["content_id_y"]]
        result = result[result["id_user"] != result["id_user_y"]]

        return result

    # Initialize an empty list to store results
    result_list = []

    # Create a tqdm progress bar
    pbar = tqdm(total=len(data["object_id"].unique()), desc="Detecting coordinated groups")

    # Iterate over each unique object_id grouping in the data
    for _, group in data.groupby("object_id"):
        result = _calc_group_combinations(group, time_window=time_window)
        result_list.append(result)
        pbar.update(1)
    pbar.close()  

    result = pd.concat(result_list)

    #Progress Update
    print('Applying minimum repetition filter...')

    # Filter by minimum repetition
    coordinated_content_ids = set(result["content_id"].tolist())

    filtered_data = data[data["content_id"].isin(coordinated_content_ids)]
    filtered_data = filtered_data.groupby("id_user").filter(lambda g: len(g) > min_repetition)

    # filter the result to only contain content_ids from above
    result = result[(result["content_id"].isin(filtered_data["content_id"]))]
    
    #Progress Update
    print('Minimum repetition filter applied.')


    # Sort output: content_id should be older than content_id_y
    # Create masks for swapping
    swap_mask = result["time_delta"] > 0
    content_id = result.loc[swap_mask, "content_id"].values
    content_id_y = result.loc[swap_mask, "content_id_y"].values
    id_user = result.loc[swap_mask, "id_user"].values
    id_user_y = result.loc[swap_mask, "id_user_y"].values

    # Swap the columns
    result.loc[swap_mask, "content_id"] = content_id_y
    result.loc[swap_mask, "content_id_y"] = content_id
    result.loc[swap_mask, "id_user"] = id_user_y
    result.loc[swap_mask, "id_user_y"] = id_user

    return result

def group_stats(data):
    """
    Calculate group statistics based on input data.

    :param data: Input data, a DataFrame containing columns: "object_id", "time_delta".
    :type data: pandas.DataFrame

    :return: DataFrame with group statistics.
    :rtype: pandas.DataFrame
    """
    grouped_data = data.reset_index(drop=True)

    summary = grouped_data.groupby('object_id', as_index=False).agg({
        'id_user': 'nunique',   # Count the number of unique users
        'content_id': 'nunique',  # Count the number of unique content_id
        'time_delta': 'mean'
    }).rename(columns={'id_user': 'users', 'content_id': 'posts'})

    summary.sort_values("time_delta", inplace=True)
    return summary

def user_stats(data):
    """
    Calculate user statistics based on input data.

    :param data: Input data, a DataFrame containing columns: "id_user", "content_id", "time_delta".
    :type data: pandas.DataFrame

    :return: DataFrame with user statistics.
    :rtype: pandas.DataFrame
    """
    user_summary = data.groupby("id_user").agg(
        total_posts=("content_id", "nunique"),
        mean_time_delta=("time_delta", "mean")
    ).reset_index()

    user_summary.sort_values("id_user", inplace=True)
    return user_summary
