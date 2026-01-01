import pandas as pd
import numpy as np

raw_data_path = "data/comparables/raw/"
target_company = "NVDA"


comps_market_data_df = pd.read_csv(raw_data_path + "comps_market_data.csv")
comps_net_debt_df = pd.read_csv(raw_data_path + "comps_net_debt.csv")
comps_financials_df = pd.read_csv(raw_data_path + "comps_financials.csv")

for df in [comps_financials_df, comps_market_data_df, comps_net_debt_df]:
    df.set_index("ticker", inplace=True)
    

combined_df = (
    comps_market_data_df
    .join(comps_net_debt_df, how="inner")
    .join(comps_financials_df, how="inner")
)
assert combined_df.index.is_unique
assert combined_df.shape[0] == len(comps_market_data_df)

combined_df["equity_value"] = combined_df["price"] * combined_df["diluted_shares"]
combined_df["total_debt"] = combined_df["short_term_debt"] + combined_df["long_term_debt"]
combined_df["net_debt"] = combined_df["total_debt"] - combined_df["cash"]
combined_df["enterprise_value"] = combined_df["equity_value"] + combined_df["net_debt"] + combined_df["minority_interest"] + combined_df["preferred_equity"]
combined_df["ev_ebitda"] = np.where(
    combined_df["ebitda_ltm"] > 0,
    combined_df["enterprise_value"] / combined_df["ebitda_ltm"],
    np.nan,
)
combined_df["pe"] = np.where(
    combined_df["net_income_ltm"] > 0,
    combined_df["equity_value"] / combined_df["net_income_ltm"],
    np.nan,
)
peers_df = combined_df.drop(index=target_company)
peers_df = peers_df.rename(
    columns={
        "price": "Price (USD / share)",
        "diluted_shares": "Diluted shares (millions)",
        "cash": "cash (USD millions)",
        "short_term_debt": "Short-Term Debt (USD millions)",
        "long_term_debt": "Long-Term Debt (USD millions)",
        "minority_interest": "Minority Interest (USD millions)",
        "preferred_equity": "Preferred Equity (USD millions)",
        "equity_value": "Equity value (USD millions)",
        "total_debt": "Total Debt (USD millions)",
        "enterprise_value": "Enterprise value (USD millions)",
        "ev_ebitda": "EV / EBITDA (LTM)",
        "pe": "P / E (LTM)",
        "revenue_ltm": "Revenue LTM (USD millions)",
        "ebitda_ltm": "EBITDA LTM (USD millions)",
        "net_income_ltm": "Net income LTM (USD millions)",
        "net_debt": "Net debt (USD millions)"
    }
)

target_df = combined_df.loc[[target_company]]
target_df = target_df.rename(
    columns={
        "price": "Price (USD / share)",
        "diluted_shares": "Diluted shares (millions)",
        "equity_value": "Equity value (USD millions)",
        "enterprise_value": "Enterprise value (USD millions)",
        "revenue_ltm": "Revenue LTM (USD millions)",
        "ebitda_ltm": "EBITDA LTM (USD millions)",
        "net_income_ltm": "Net income LTM (USD millions)",
        "net_debt": "Net debt (USD millions)",
    }
)

ev_ebitda_median = peers_df["EV / EBITDA (LTM)"].median()
ev_ebitda_min = peers_df["EV / EBITDA (LTM)"].min()
ev_ebitda_max = peers_df["EV / EBITDA (LTM)"].max()
pe_median = peers_df["P / E (LTM)"].median()
pe_min = peers_df["P / E (LTM)"].min()
pe_max = peers_df["P / E (LTM)"].max()

peer_multiples_df = peers_df[["EV / EBITDA (LTM)","P / E (LTM)"]].copy()
peer_multiples_df["notes"] = ""
peer_multiples_df.loc[peer_multiples_df["EV / EBITDA (LTM)"].isna(), "notes"] += "EV/EBITDA n/a; "
peer_multiples_df.loc[peer_multiples_df["P / E (LTM)"].isna(), "notes"] += "P/E n/a; "
peer_multiples_df["notes"] = peer_multiples_df["notes"].str.strip().str.rstrip(";")


peer_summary_stats_df = pd.DataFrame(
    {       
        "min": [ev_ebitda_min, pe_min],
        "median": [ev_ebitda_median, pe_median],
        "max": [ev_ebitda_max, pe_max],
    },
    index=["EV/EBITDA (LTM)", "P/E (LTM)"]
)


# Implied valuation for target using peer EV/EBITDA range
target_ebitda = float(target_df["EBITDA LTM (USD millions)"].iloc[0])
target_net_debt = float(target_df["Net debt (USD millions)"].iloc[0])
target_shares = float(target_df["Diluted shares (millions)"].iloc[0])


implied_ev = pd.Series(
    {"min": ev_ebitda_min, "median": ev_ebitda_median, "max": ev_ebitda_max}
) * target_ebitda
implied_equity = implied_ev - target_net_debt
implied_per_share = implied_equity / target_shares

nvda_implied_valuation = pd.DataFrame(
    {
        "implied_enterprise_value (USD millions)": implied_ev,
        "implied_equity_value (USD millions)": implied_equity,
        "implied_per_share_value (USD)": implied_per_share,
    }
)

combined_df.to_csv("data/comparables/processed/raw_merged.csv")
peers_df.to_csv("outputs/comparables/tables/peers_set.csv")
peer_multiples_df.to_csv("outputs/comparables/tables/peer_multiples.csv")
peer_summary_stats_df.to_csv("outputs/comparables/tables/peer_summary_stats.csv")
nvda_implied_valuation.to_csv("outputs/comparables/tables/nvda_implied_valuation.csv")


if __name__ == "__main__":
    print("Peer multiples:")
    print(peer_multiples_df)
    print("\nSummary stats:")
    print(peer_summary_stats_df)
    print("\nNVDA implied valuation:")
    print(nvda_implied_valuation)