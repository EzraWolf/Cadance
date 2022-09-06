# Cadance

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
| `-d`        | `--download` | A single symbol or a list from the `stock.csv` path | Download & format specific stock data from a symbol the `stock.csv` path                                              |
| `-c`        | `--collect`  | `news`, or `daily`                                  | Collect news articles for sentiment analysis, or daily stock data that contains more information than historical data |
| `-t`        | `--train`    | `news`, `cadance`, or `trader`                      | Train one of the three ML models off of data from `datasets/`                                                         |
| `-p`        | `--predict`  | A single symbol or a list from the `stock.csv` path | Predict the given stocks next-day closing price                                                                       |


## Information that Cadance uses per stock:

 1. Open
 2. Close
 3. High
 4. Low
 5. Adjusted close
 6. Volume
 7. EMA, lengths 10, 25, 50 (Exponential Moving Avg.)
 8. RSI, lengths 10, 25 (Relative Strength Index)
 9. PGO, lengths 10, 25 (Pretty Good Oscillator)
 10. VIA, lengths 15, 30 (Relative Vigor Index line A)
 11. VIB, lengths 15, 30 (Relative Vigor Index line B)
 12. ETP, lengths 10, 25 (Entropy)
 13. MAD, lengths 10, 25 (Mean Absolute Deviation)
 14. SIN, lengths 25, 50 (Sinewave `ebsw` in `pandas_ta`)
 15. LIN, lengths 10, 90 (Linear Regression)
 16. NAT, length 30 (Normalized Avg. True range volatility)
 17. BOP (Balance Of Power)
 18. Previous predictions and their accuracy are based
       on a certain amount of tolerance. E.G. Lesser
       tolerance, such as 3%, would yield stricter results
       than per se, 15%.
 19. News sentiment scraped on each specific stock
 20. If we are currently in an economic boom or recession
 21. The current US GDP and its percent change since last month
 22. The current US employment rate and its percent change since last month


## Dataset information:

### `datasets/lits/stocks.csv`
This dataset was downloaded from stockanalysis.com/stocks/ using a free-trail account.

It takes about `2-3` hours to download using `python main.py -d datasets/lits/stocks.csv`,
and is currently about `5.3gb` large.


NOTE:

 - The original download was renamed from `stock-list.csv` to `stocks.csv`

 - The header names: `Symbol`, `Name`, `Industry`, and `Market Cap`
   were renamed to `SYMBOL`, `NAME`, `INDUSTRY`, `MARKET_CAP`
   in order to preserve consistency between `*.csv` files

 - About 200~ stocks from this dataset threw errors in Yahoo Finance.
   Many of which were stocks that were listed on stockanalysis.com, but not on YF.
   A lot of stocks were also too new to have enough data to work with.

 - The current `stocks.csv` file has been curated so that none of these stocks are in it
