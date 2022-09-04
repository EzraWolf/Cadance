
import numpy as np
import pandas as pd
# import pandas_ta as ta


def set_indicator_values(df: pd.DataFrame) -> np.float32:
    """
    Sets up multiple pandas_ta indicators
    for the given DataFrame
    """
    pass


def df_is_in_recession(row, recessions: pd.DataFrame) -> bool:
    """
    Usecase: `df.apply(df_is_in_recession, args=(recessions)))`

    Determines if any given row is in a recession
    and for how long based on a list of US recessions
    """
    pass


def df_is_in_econ_boom(row, econ_booms: pd.DataFrame) -> bool:
    """
    Usecase: `df.apply(df_is_in_econ_boom, args=(econ_booms)))`

    Determines if any given row is in an economic boom
    and for how long based on a list of US economic booms
    """
    pass


def df_get_empl_pcnt(row, empl_pcnts: pd.DataFrame) -> np.float32:
    """
    Usecase: `df.apply(df_get_empl_pcnt, args=(empl_pcnts)))`

    Returns how much percent the US employment rate has changed
    """
    pass


def df_get_gdp_pcnt(row, gdp_pcnts) -> np.float32:
    """
    Usecase: `df.apply(df_get_gdp_pcnt, args=(gdp_pcnts)))`

    Returns how much percent the US GDP rate has changed
    """
    pass


def df_get_target_dir(
    row,
    open: np.float32,
    close: np.float32,
    tolerance: np.float32 = 0.02
) -> bool:
    """
    Usecase:
    `df.apply(df_target_dir, args=(open, close, tolerance))).shift(-1)`

    Gets the difference between the current open and close,
    and if it is more than <tolerance> percent away from 0,
    the stock is either going up or down.
    """
    pass
