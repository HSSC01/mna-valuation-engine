import pandas as pd
import numpy as np

raw_data_path = "data/raw/"
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
target_df = combined_df.loc[[target_company]]

ev_ebitda_median = peers_df["ev_ebitda"].median()
ev_ebitda_min = peers_df["ev_ebitda"].min()
ev_ebitda_max = peers_df["ev_ebitda"].max()
pe_median = peers_df["pe"].median()
pe_min = peers_df["pe"].min()
pe_max = peers_df["pe"].max()

peer_multiples_df = peers_df[["ev_ebitda","pe"]].copy()
peer_multiples_df["notes"] = ""
peer_multiples_df.loc[peer_multiples_df["ev_ebitda"].isna(), "notes"] += "EV/EBITDA n/a; "
peer_multiples_df.loc[peer_multiples_df["pe"].isna(), "notes"] += "P/E n/a; "
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
target_ebitda = float(target_df["ebitda_ltm"].iloc[0])
target_net_debt = float(target_df["net_debt"].iloc[0])
target_shares = float(target_df["diluted_shares"].iloc[0])


implied_ev = pd.Series(
    {"min": ev_ebitda_min, "median": ev_ebitda_median, "max": ev_ebitda_max}
) * target_ebitda
implied_equity = implied_ev - target_net_debt
implied_per_share = implied_equity / target_shares

nvda_implied_valuation = pd.DataFrame(
    {
        "implied_enterprise_value": implied_ev,
        "implied_equity_value": implied_equity,
        "implied_per_share_value": implied_per_share,
    }
)


peers_df.to_csv("data/processed/peers_set.csv")
peer_multiples_df.to_csv("data/processed/peer_multiples.csv")
peer_summary_stats_df.to_csv("data/processed/peer_summary_stats.csv")
nvda_implied_valuation.to_csv("data/processed/nvda_implied_valuation.csv")


if __name__ == "__main__":
    print("Peer multiples:")
    print(peer_multiples_df)
    print("\nSummary stats:")
    print(peer_summary_stats_df)
    print("\nNVDA implied valuation:")
    print(nvda_implied_valuation)