import pandas as pd
import numpy as np
from pathlib import Path

def run_precedents(precedents_deals_csv):
    raw_data_path = "data/precedents/processed/"
    Path("outputs/precedents/tables").mkdir(parents=True, exist_ok=True)
    
    deals_df = pd.read_csv(raw_data_path+precedents_deals_csv)

    deals_df.loc[deals_df["offer_type"] == "cash", "offer_price"] = deals_df["cash_price"]
    deals_df.loc[deals_df["offer_type"] == "stock", "offer_price"] = deals_df["exchange_ratio"] * deals_df["acquirer_price_at_announcement"]
    deals_df.loc[deals_df["offer_type"] == "mixed", "offer_price"] = deals_df["cash_price"] + (deals_df["exchange_ratio"] * deals_df["acquirer_price_at_announcement"])

    deals_df["total_debt"] = deals_df["short_term_debt"] + deals_df["long_term_debt"]
    deals_df["net_debt"] = deals_df["total_debt"] - deals_df["cash_and_equivalents"]
    deals_df["equity_value"] = deals_df["offer_price"] * deals_df["fully_diluted_shares"]
    deals_df["enterprise_value"] = deals_df["equity_value"] + deals_df["net_debt"] + deals_df["minority_interest"] + deals_df["preferred_equity"]

    deals_df = deals_df.rename(
        columns={
            "offer_price": "Offer Price (USD)",
            "cash_price": "Cash Price (USD)",
            "acquirer_price_at_announcement": "Acquirer Price at Announcement (USD)",
            "fully_diluted_shares": "Fully Diluted Shares (millions)",
            "cash_and_equivalents": "Cash (millions)",
            "short_term_debt": "Short Term Debt (USD millions)",
            "long_term_debt": "Long Term Debt (USD millions)",
            "minority_interest": "Minority Interest (USD millions)",
            "preferred_equity": "Preferred Equity (USD millions)",
            "total_debt": "Total Debt (USD millions)",
            "net_debt": "Net Debt (USD millions)",
            "equity_value": "Equity Value (USD millions)",
            "enterprise_value": "Enterprise Value (USD millions)",
            "revenue_ltm": "Revenue LTM (USD millions)",
            "ebitda_ltm": "EBITDA LTM (USD millions)"
        }
    )

    ev_ebitda_mean = (deals_df["Enterprise Value (USD millions)"] / deals_df["EBITDA LTM (USD millions)"]).mean()
    ev_ebitda_median = (deals_df["Enterprise Value (USD millions)"] / deals_df["EBITDA LTM (USD millions)"]).median()
    ev_ebitda_min = (deals_df["Enterprise Value (USD millions)"] / deals_df["EBITDA LTM (USD millions)"]).min()
    ev_ebitda_max = (deals_df["Enterprise Value (USD millions)"] / deals_df["EBITDA LTM (USD millions)"]).max()
    ev_revenue_mean = (deals_df["Enterprise Value (USD millions)"] / deals_df["Revenue LTM (USD millions)"]).mean()
    ev_revenue_median = (deals_df["Enterprise Value (USD millions)"] / deals_df["Revenue LTM (USD millions)"]).median()
    ev_revenue_min = (deals_df["Enterprise Value (USD millions)"] / deals_df["Revenue LTM (USD millions)"]).min()
    ev_revenue_max = (deals_df["Enterprise Value (USD millions)"] / deals_df["Revenue LTM (USD millions)"]).max()

    precedents_summary_stats_df = pd.DataFrame(
        {       
            "min": [ev_ebitda_min, ev_revenue_min],
            "mean": [ev_ebitda_mean, ev_revenue_mean],
            "median": [ev_ebitda_median, ev_revenue_median],
            "max": [ev_ebitda_max, ev_revenue_max]
        },
        index=["EV/EBITDA (LTM)", "EV/Revenue (LTM)"]
    )

    deals_df.to_csv("outputs/precedents/tables/precedents_deals.csv")
    precedents_summary_stats_df.to_csv("outputs/precedents/tables/precedents_summary_stats.csv")
    return {
        "deals": deals_df,
        "summary": precedents_summary_stats_df
    }, print(precedents_summary_stats_df)

if __name__ == "__main__":
    run_precedents("precedents_deals.csv")