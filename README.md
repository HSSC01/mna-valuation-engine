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
    - cash (millions) = 10-Q -> "Cash and cash equivalents" + "Marketable securities" + "short-term investments"

- financials
    - pulled from latest 10-Q reports
    - negative ebitda > ev/ebitda excluded, flagged
    - negative net income > p/e excluded, flagged
    - ltm period must be consistent across peers
    - ebitda_ltm (millions) = "operating income proxy"

Trading comparables suggest NVIDIA trades at a premium to peers on EV/EBITDA, reflecting superior margins, growth visibility, and balance sheet strength. Intel is retained in the peer set for scale and cycle context but excluded from affected multiples due to negative LTM profitability.



Precedents:
- frame valuation range at which strategic buyers have historically acquired control of similar platform assets.
- NVIDIA target
    - mission-critical compute and IP platform whose value to acquirers is driven by ecosystem integration, strategic optionality and long-term control rather than standalone cashflows.
    - which acquisitions involved similar economic control value?
        - industry / sub-sector
        - business model (platform)
        - buyer type (strategic)
        - deal type (full control)
        - size/relevance
    - annual "largest tech M&A" articles
        - exclude deals that
            - were minority stakes (does not convey control)
            - were joint ventures (split decision rights)
            - were distressed / forced sales (price distorted by liquidity constraints)
            - occurred in a completely different regime (multiples not transferable)
            - have no usable financials (cannot compute reliable multiples)
- chosen deals:
    core semiconductor control precedents
    - amd acquires xilinx (2022)
        + semiconductor ip
        + platform-level integration
        + strategic buyer
        + clear roadmap and architectural synergies
        + control mattered enormously
        - smaller scale than nvidia
        - fpga vs gpu economics
        - lower ecosystem dominance
        = core semiconductor control precedent
    - avago acquires broadcom (2016)
        + semiconductor platform consolidation
        + strategic buyer
        + control unlocked pricing power and cash-flow optimisation
        + massive scale and ecosystem relevance
        - buyer is financial-strategic hybrid
        - focused heavily on cash extraction
        - less innovation-driven than nvidia
        = upper-mid control benchmark
        = illustrates how buyers price cash-generative ip platforms
    strategic infrastructure platform precedents
    - ibm acquires red hat (2019)
        + mission-critical platform
        + ecosystem leverage
        + strategic buyer
        + control enabled long-term repositioning
        + paid very large premium vs comps
        - software vs semiconductor
        - subscription economics
        - higher margins, different capital intensity
        = upper-bound "platform optionality" precedent
        = shows what buyers pay for strategic relevance, not ebitda.
    - dell acquires emc (2016)
        + large scale platform acquisition
        + strategic buyer
        + full control
        + significant integration optionality
        + control allowed dell to reshape capital structure and operating model
        - hardware + services (not semiconductor)
        - much more leverage-driven
        - slower growth than nvidia
        - less ip-driven upside
        = lower-bound/capital-structure-heavy precedent
        = shows what control cleared at for large, entrenched infrastructure platforms
    = while no transaction is a perfect analogue for nvidia, the selected precedents capture how strategic buyers have historically priced control of large-scale semiconductor and infrastructure platforms with embedded optionality
- Buyer type is used to distinguish strategic acquisitions, which often embed synergies and control premiums, from financial sponsor transactions with return constraints
- offer price is the implied value per target common share at announcement, using acquirer share prices on the announcement date.
    - amd / xilinx
        - each share of xilinx converted to the right to receive 1.7234 shares of AMD common stock
    - avago / broadcom
        - each share of broadcom has the right to receive $54.50 cash or 0.4378 shares of avago
    - ibm / red hat
        - each share of red hat converted to the right to receive $190 in cash
    - dell / emc
        - each share of emc will be cancelled and converted into the right to receive $24.05 in cash and class v common stock
- all-cash consideration
    - offer_price = stated cash per target share
    - ibm / red hate, offer_price = $190
- all-stock consideration
    - offer_price = exchange_ratio * acquirer share price (announcement date)
    - amd / xilinx, offer_price = 1.7234 * P_AMD
- mixed cash + stock
    - offer_price = cash_per_share + (exchange_ratio * acquirer share price)
    - avago / broadcom, offer_price = 54.5 + (0.4378 * acquirer share price)
    - dell / emc, offer_price = 24.05 + (class v exchange ratio * dell class v price)
- equity_value = offer_price * fully_diluted_shares
- enterprise_value = equity_value + net_debt + minority interest + preferred equity
