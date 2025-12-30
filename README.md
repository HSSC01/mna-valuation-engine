Comparables:
raw data (all values in millions except for per-share values)
- peer_set = {
    "AMD": "AMD", # Closest GPU/accelerator competitor; similar end markets
    "Broadcom": "AVGO", # High-margin semiconductor IP with data-centre exposure
    "Marvell Technology": "MRVL", # Data-centre and networking silicon; relevant growth vector
    "QUALCOMM": "QCOM", # Fabless, IP-driven margins (mobile skew acknowledged)
    "Intel": "INTC", # Included for scale/compute exposure despite margin differences
}
    Peers selected based on overlap in GPU, data-centre, and semiconductor IP exposure; Intel retained for scale and cycle context despite margin differences.
- market data
    - pulled from nasdaq (https://www.nasdaq.com/market-activity/stocks/[ticker]) compiled manually to immitate raw data pulled from an institutional database
    - previous close based on valuation_date_(t-1)
    - diluted_shares (millions) pulled from latest 10-Q reports

- net debt
    - pulled from latest 10-Q reports
    - total_debt = short_term_debt + long_term_debt
    - net_debt = total_debt - cash
    - enterprise_value = equity_value + net_debt + minority_interest + preferred_equity
    - cash (millions) = 10-Q -> "Cash and cash equivalents" + "Marketable securities/short-term investments"

- financials
    - pulled from latest 10-Q reports
    - negative ebitda > ev/ebitda excluded, flagged
    - negative net income > p/e excluded, flagged
    - ltm period must be consistent across peers
    - LTM = 9M current year + 3M prior year (same quarter)
    - ebitda_ltm (millions) = "operating income proxy"

Trading comparables suggest NVIDIA trades at a premium to peers on EV/EBITDA, reflecting superior margins, growth visibility, and balance sheet strength. Intel is retained in the peer set for scale and cycle context but excluded from affected multiples due to negative LTM profitability.