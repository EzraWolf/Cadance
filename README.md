# Cadance V0.03

People typically say that you can't predict the stock market using past data,
and they would be right under a certain lens. You will almost certainly never
get any meaningful information out of training a neural network over just basic
`open`, `close`, `high`, `low`, and `volume` metrics. 

But since we don't have to just use superficial data like this, my goal is to
feed this network as much information as possible, and then, maybe, something
interesting will happen.


## Command-line arguments:
| Short Name: | Long Name:   | Parameters:                                         | Use-case:                                                                                                             |
|-------------|--------------|-----------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| -d        | --download | A single symbol or a list from the `stock.csv` path | Download & format specific stock data from a symbol the `stock.csv` path                                              |
| -c        | --collect  | `news`, or `daily`                                  | Collect news articles for sentiment analysis, or daily stock data that contains more information than historical data |
| -t        | --train    | `news`, `cadance`, or `trader`                      | Train one of the three ML models off of data from `datasets/`                                                         |
| -p        | --predict  | A single symbol or a list from the `stock.csv` path | Predict the given stocks next-day closing price                                                                       |


## Information that Cadance uses:

 - `Open`
 - `Close`
 - `Adjusted Close`
 - `High`
 - `Low`
 - Previous prediction results and their accuracy denoted by an error tolerance
 - Sentiment news analysis done by another neural network
 - The current US GDP percent change since the last month
 - The current US employment rate percent change since the last month

### The current list of utilized indicators:

| Indicators | Information                           | Length(s)        |
|-----------|---------------------------------------|------------------|
| EMA       | Exponential Moving Avg.               | `10`, `25`, `50` |
| RSI       | Relative Strength Index               | `10`, `25`       |
| PGO       | Pretty Good Oscillator                | `10`, `25`       |
| VIA       | Relative Vigor Index line A           | `15`, `30`       |
| VIB       | Relative Vigor Index line B           | `15`, `30`       |
| ETP       | Entropy                               | `10`, `25`       |
| MAD       | Mean Abs. Deviation                   | `10`, `25`       |
| SIN       | "Even Better" Sinewave (`ebsw`)       | `25`, `50`       |
| LIN       | Linear Regression                     | `10`, `90`       |
| NAT       | Normalized Avg. True Range Volatility | `30`             |
| BOP       | Balance of Power                      |                  |


# Dataset information:

### `datasets/lits/stocks.csv`
This dataset was downloaded from `stockanalysis.com/stocks` using a free-trail account.

It takes about `2-3` hours to download using `python main.py -d datasets/lits/stocks.csv`,
and is currently about `5.3gb` large.

### NOTE:

 - The original download was renamed from `stock-list.csv` to `stocks.csv`

 - The header names: `Symbol`, `Name`, `Industry`, and `Market Cap`
   were renamed to `SYMBOL`, `NAME`, `INDUSTRY`, `MARKET_CAP`
   in order to preserve consistency between `*.csv` files

 - About 200~ stocks from this dataset threw errors in Yahoo Finance.
   Many of which were stocks that were listed on stockanalysis.com, but not on YF.
   A lot of stocks were also too new to have enough data to work with.

 - The current `stocks.csv` file has been curated so that none of these stocks are in it

### `datasets/lists/gdp.csv`
This dataset was downloaded from `https://fred.stlouisfed.org/series/A191RP1Q027SBEA`
and in order to download it, use the `download_gdp` function inside of `stocker`

This dataset is about 500kB large, and takes about 30 seconds to download and expand
