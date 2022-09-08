
import pandas as pd
import datetime as dt

from . import logger


def contains_all_cols(
    df: pd.DataFrame,
    cols: list[str],
    log: bool = True,
) -> bool:
    '''
    Checks if a DataFrame contains all
    of the columns listed in cols.

    Returns a tuple showing if the DataFrame
    had every column listed, and the columns
    that were not in the DataFrame, if some weren't
    '''

    valid: bool = True
    missed: list[str] = []

    for col in cols:
        if col not in df.columns:
            valid = False
            missed.append(col)

    if not valid and log:
        logger.Log(
            'df_tools',
            f'Insufficient data. DataFrame requires the columns: {missed}'
        ).critical(is_print=True)

    return valid


def drop_col_if_exists(df: pd.DataFrame, col: str) -> pd.DataFrame:
    '''
    Removes a column from a DataFrame if it exists
    '''
    if col in df.columns:
        return df.drop([col], axis=1)

    return df


def expand_dates(df: pd.DataFrame):
    day = dt.datetime(int(df['DATE'][0].split('-')[0]), 1, 1)
    end_date = dt.datetime.now()
    df_res: pd.DataFrame = pd.DataFrame(columns=df.columns)
    value: float = 0.0
    while day <= end_date:

        # Update the current GDP
        new_value = df.loc[
            df['DATE'] == day.strftime('%Y-%m-%d'),
            df.iloc[:, 1]
        ]

        if new_value.shape[0] > 0:
            value = new_value.tail(1).item()

        # Append new rows
        df_res.loc[len(df_res)] = [day.strftime('%Y-%m-%d'), value]
        day += dt.timedelta(days=1)

    return df_res


def df_is_in_daterange(
    row: pd.Series,
    date_range_df: pd.DataFrame,
    log: bool = True
) -> bool:
    '''
    Usecase: `df.apply(df_is_in_daterange, args=(date_range_df)))`

    Determines if any given row is in a recession
    and for how long based on a list of US recessions
    '''
    if not contains_all_cols(
        date_range_df,
        [
            'start_date',
            'end_date',
        ],
        log=False
    ):
        logger.Log(
            'df_tools',
            'The provided DataFrame did not \
contain a "start_date" and or "end_date" column'
        ).warning(is_print=log)
        return False

    for _, df_row in date_range_df.iterrows():
        start_date = dt.datetime.strptime(df_row['start_date'], '%Y-%m-%d')
        end_date = dt.datetime.strptime(df_row['end_date'], '%Y-%m-%d')

        # Convert the "row['date]" type date into type datetime
        crnt_date = dt.datetime.combine(row['DATE'], dt.time())

        # We use the "<=" here to prevent overlapping dates
        # e.g.
        # From 2020-02-01 to 2020-04-01,
        # The applied range would actually be:
        #      2020-02-01 to 2020-03-31
        if start_date <= crnt_date < end_date:
            return True

    return False


def df_get_empl_pcnt(row, empl_pcnts: pd.DataFrame) -> float:
    '''
    Usecase: `df.apply(df_get_empl_pcnt, args=(empl_pcnts)))`

    Returns how much percent the US employment rate has changed
    '''
    pass


def df_get_gdp_pcnt(row, gdp_pcnts) -> float:
    '''
    Usecase: `df.apply(df_get_gdp_pcnt, args=(gdp_pcnts)))`

    Returns how much percent the US GDP rate has changed
    '''
    pass


def df_get_target_dir(
    row,
    open: float,
    close: float,
    tolerance: float = 0.02,
) -> bool:
    '''
    Usecase:
    `df.apply(df_target_dir, args=(open, close, tolerance))).shift(-1)`

    Gets the difference between the current open and close,
    and if it is more than <tolerance> percent away from 0,
    the stock is either going up or down.
    '''
    pass
