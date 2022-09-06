
import os
import config
import numpy as np
import pandas as pd
import pandas_ta as ta
import yahooquery as yq

from . import logger
from . import df_tools


def download(
    ticker: str,
    root_dir: str,
    period: str = 'max',
    prepare: bool = False,
    overwrite: bool = False,
    log: bool = True,
) -> None:

    # Sanitize the ticker
    ticker = ticker.upper()
    if not ticker.isalpha():
        logger.Log(
            'stocker',
            f'${ticker} contains characters other than a-zA-Z'
        ).warning(is_print=log)

        return

    dl_path: str = f'{root_dir}/{ticker}.csv'

    # If the .csv already exists and
    # we aren't overwriting it, return
    if os.path.exists(dl_path) and not overwrite:
        return

    if log:

        # Build the message we will log
        log_str = 'Downloading'
        if prepare:
            log_str += ' and formatting'
        log_str += f' {ticker}.csv'

        logger.Log(
            'stocker',
            log_str,
        ).normal(is_print=True)

    # Fetch the stock data and format it if needed
    stock: pd.DataFrame = fetch(ticker, period=period, log=False)
    if prepare:
        stock = format(
            stock,
            tolerance=0.06,
            list_path=config.LIST_PATH,
            log=False,
        )

        # Log some errors in the off chance
        # that we couldn't format the stock
        if stock is None:
            logger.Log(
                'stocker',
                f'Failed to format ${ticker}'
            ).critical(is_print=log)
            return

    # Download the final product
    stock.to_csv(dl_path, index=True, header=True)


def fetch(
    ticker: str,
    period: str = 'max',
    log: bool = True,
) -> pd.DataFrame:

    # Sanitize the ticker
    ticker = ticker.upper()
    if not ticker.isalpha():
        logger.Log(
            'stocker',
            f'${ticker} contains characters other than a-zA-Z'
        ).warning(is_print=True)

        return

    if log:
        logger.Log(
            'stocker',
            f'Fetching data from ${ticker}',
        ).normal(is_print=True)

    # Try excepts should be avoided,
    # but Yahooquery will occasionally
    # throw some really obscure errors
    # that are hard to explicitly find
    try:
        return yq.ticker.Ticker(
            ticker,
            validate=True,
            formated=False,
            asynchronous=True,
            max_workers=25,
            retry=3,
        ).history(
            adj_ohlc=False,
            period=period,
            interval='1d',
        ).reset_index()  # Remove annoying indexes

    except Exception as e:
        logger.Log(
            'stocker',
            f'Error while fetching data from ${ticker}:\n\n{e}',
        ).critical(is_print=True)


def format(
    df: pd.DataFrame,
    tolerance: float = 0.07,
    list_path: str = config.LIST_PATH,
    log: bool = True,
) -> pd.DataFrame:
    '''
    Adds technical indicators, cleans up,
    formats, and adds targets to the given df.
    '''

    # Make sure that the DataFrame we are using is valid
    if not df_tools.contains_all_cols(
        df,
        [
            'close',  'open',
            'high',   'low',
            'volume',
        ],
        log=False,
    ):
        if log:
            logger.Log(
                'stocker',
                'Failed to format the given DataFrame'
            ).critical(is_print=True)
        return None

    # Prevent stocks that are too new from being used
    if df.shape[0] < 150:
        return None

    # This is probably one of the
    # worst ways to do this but it works

    # Round everything off to the 5th decimal place
    df['OPEN'] = round(df['open'], 5)
    df['CLOSE'] = round(df['close'], 5)
    df['HIGH'] = round(df['high'], 5)
    df['LOW'] = round(df['low'], 5)
    df['ADJCLOSE'] = round(df['adjclose'], 5)

    df['DATE'] = df['date']
    df['VOLUME'] = df['volume']

    # Drop previous columns since we renamed them
    df = df_tools.drop_col_if_exists(df, 'open')
    df = df_tools.drop_col_if_exists(df, 'close')
    df = df_tools.drop_col_if_exists(df, 'high')
    df = df_tools.drop_col_if_exists(df, 'low')
    df = df_tools.drop_col_if_exists(df, 'adjclose')

    df = df_tools.drop_col_if_exists(df, 'date')
    df = df_tools.drop_col_if_exists(df, 'volume')
    df = df_tools.drop_col_if_exists(df, 'symbol')
    df = df_tools.drop_col_if_exists(df, 'splits')
    df = df_tools.drop_col_if_exists(df, 'dividends')

    # Relative strength index (momentum pattern)
    df['RSI_10'] = round(ta.rsi(df['CLOSE'], length=10), 5)
    df['RSI_25'] = round(ta.rsi(df['CLOSE'], length=25), 5)

    # Exponential moving average (momentum pattern)
    df['EMA_10'] = round(ta.ema(df['CLOSE'], length=10), 5)
    df['EMA_25'] = round(ta.ema(df['CLOSE'], length=25), 5)
    df['EMA_50'] = round(ta.ema(df['CLOSE'], length=50), 5)

    # Pretty good oscillator (momentum pattern)
    df['PGO_10'] = round(
        ta.pgo(df['HIGH'], df['LOW'], df['CLOSE'], length=10), 5
    )
    df['PGO_25'] = round(
        ta.pgo(df['HIGH'], df['LOW'], df['CLOSE'], length=25), 5
    )

    # Relative vigor ingex lines A & B (momentum pattern)
    df['VIA_15'] = round(ta.rvgi(
        df['OPEN'], df['HIGH'], df['LOW'],  df['CLOSE'],
        length=15
    ).loc[:, 'RVGI_15_4'], 5)
    df['VIB_15'] = round(ta.rvgi(
        df['OPEN'], df['HIGH'], df['LOW'],  df['CLOSE'],
        length=15
    ).loc[:, 'RVGIs_15_4'], 5)

    # Relative vigor ingex lines A & B (momentum pattern)
    df['VIA_30'] = round(ta.rvgi(
        df['OPEN'], df['HIGH'], df['LOW'],  df['CLOSE'],
        length=30
    ).loc[:, 'RVGI_30_4'], 5)
    df['VIB_30'] = round(ta.rvgi(
        df['OPEN'], df['HIGH'], df['LOW'],  df['CLOSE'],
        length=30
    ).loc[:, 'RVGIs_30_4'], 5)

    # Balance of power (momentum pattern)
    df['BOP'] = round(
        ta.bop(df['OPEN'], df['HIGH'], df['LOW'], df['CLOSE']), 5
    )

    # Normalized average true range (volatility)
    df['NAT_30'] = round(ta.natr(df['HIGH'], df['LOW'], df['CLOSE'], 30), 5)

    # Entropy (statistic)
    df['ETP_10'] = round(ta.entropy(df['CLOSE'], length=10), 5)
    df['ETP_25'] = round(ta.entropy(df['CLOSE'], length=25), 5)

    # Mean absolute deviation (statistic)
    df['MAD_10'] = round(ta.mad(df['CLOSE'], length=10), 5)
    df['MAD_25'] = round(ta.mad(df['CLOSE'], length=25), 5)

    # Even better sinewave (cyclic pattern)
    df['SIN_25'] = round(ta.ebsw(df['CLOSE'], length=25), 5)
    df['SIN_50'] = round(ta.ebsw(df['CLOSE'], length=50), 5)

    # Linear regression (overlap pattern)
    df['LIN_10'] = round(ta.linreg(df['CLOSE'], length=10), 5)
    df['LIN_90'] = round(ta.linreg(df['CLOSE'], length=90), 5)

    '''
    # Check if we are in a recession
    recessions_path: str = f'{list_path}/recessions.csv'
    if os.path.exists(recessions_path):
        recessions: pd.DataFrame = pd.read_csv(recessions_path)

        # Check if we are in a recession
        df['IN_RECESSION'] = df.apply(
            df_tools.df_is_in_daterange,
            args=(
                recessions,
                True,
            ),
            axis=1
        )

    # Check if we are in an economic boom
    econ_boom_path: str = f'{list_path}/econ-booms.csv'
    if os.path.exists(econ_boom_path):
        econ_booms: pd.DataFrame = pd.read_csv(econ_boom_path)

        # Check if we are in a recession
        df['IN_ECON_BOOM'] = df.apply(
            df_tools.df_is_in_daterange,
            args=(
                econ_booms,
                True,
            ),
            axis=1
        )
    '''

    # Set it to 0 until we have the fully trained
    # model, then we will go back and predict the
    # price difference.
    df['PREDICTION'] = 0

    # Returns the difference in price and percent change that we're targetting
    df['TARGET_DIFF'] = round((df['CLOSE'] - df['OPEN']), 5).shift(-1)
    df['TARGET_PCNT'] = round(
        np.divide(
            (df['CLOSE'] - df['OPEN']), df['OPEN']
        ), 5
    ).shift(-1)

    # How close the model predicted to the target percents
    # difference given a certain amount of error tolerance
    #
    # tolerance / (|percent change - prediction| + tolerance)
    df['TARGET_PCNT'] = round(
        np.divide(
            tolerance,
            np.abs(df['TARGET_PCNT'] - df['PREDICTION']) + tolerance
        ), 5
    )
    df['TARGET_HI'] = df['HIGH'].shift(-1)
    df['TARGET_LO'] = df['LOW'].shift(-1)

    # Drop NaN rows
    return df.dropna()
