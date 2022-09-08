
import os
import models
import config
import utility
import argparse

import pandas as pd


def main(args: argparse.Namespace) -> None:
    if args.train == 'news':
        pass

    elif args.train == 'predictor':
        pass

    elif args.train == 'trader':
        pass

    if args.collect:
        pass

    if args.download:
        if os.path.exists(args.download) and args.download.endswith('.csv'):
            stock_list: pd.DataFrame = pd.read_csv(args.download)
            for _, row in stock_list.iterrows():
                utility.stocker.download(
                    row['SYMBOL'],
                    config.STOCK_PATH,
                    prepare=True,
                    overwrite=False,
                    log=True,
                )

        utility.stocker.download(
            args.download,
            config.STOCK_PATH,
            prepare=True,
            overwrite=True,
            log=True,
        )

    elif args.download:
        pass

    if args.predict:
        symbol: str = args.predict
        length: int = 1
        if '+' in symbol:
            symbol: str = args.predict.split('+')[0]
            _length: str = args.predict.split('+')[1]

        # Convert _length into an integer when possible
        if not isinstance(_length, int) and _length.isdigit():
            length = int(_length)

        cadance = models.Cadance().load(config.MODEL_SAVE_PATH + 'cadance.h5')
        cadance.predict(length)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t',
        '--train',
        dest='train',
        type=str,
        required=False,
        default=None,
        help='Train a specific model, either "news", "predictor", or "trader"'
    )

    parser.add_argument(
        '-c',
        '--collect',
        dest='collect',
        type=bool,
        required=False,
        default=False,
        help='Collect news and daily data'
    )

    parser.add_argument(
        '-d',
        '--download',
        dest='download',
        type=str,
        required=False,
        default=None,
        help='Download a specific stock, or a list from a *.csv file'
    )

    parser.add_argument(
        '-p',
        '--predict',
        dest='predict',
        type=str,
        required=False,
        default=None,
        help='Specify a stocks symbol to predict, \
add "+<n>d" to predict n days into the future'
    )

    args: argparse.Namespace = parser.parse_args()

    gdp_path: str = 'datasets/lists/gdp.csv'
    gdp = pd.read_csv(gdp_path)

    test_df: pd.DataFrame = pd.DataFrame(gdp, columns=['DATE', 'GDP_CHANGE'])

    start_date: str = '1947-04-01'

    main(args)
