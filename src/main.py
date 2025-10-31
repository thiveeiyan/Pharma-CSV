from __future__ import annotations
import argparse
from pathlib import Path
import sys
import time
import random
import pandas as pd
import requests  # only needed if you wire a real API

REQUIRED_COLS = ["year", "revenue", "profit", "cost", "price"]

def read_csv(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df.columns = [c.strip().lower() for c in df.columns]
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"CSV must have columns {REQUIRED_COLS}. Missing {missing}")
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["year"]).copy()
    df["year"] = df["year"].astype(int)
    # remove duplicate years if any
    df = df.sort_values("year").drop_duplicates(subset=["year"], keep="last")
    return df

def ask_years_if_needed(args) -> tuple[int, int]:
    start_y = args.start
    end_y = args.end
    if start_y is None:
        start_y = int(input("Start year: ").strip())
    if end_y is None:
        end_y = int(input("End year: ").strip())
    if end_y < start_y:
        raise ValueError("End year must be greater than or equal to start year")
    return start_y, end_y

# --------- API layer ----------
# Replace the function below with a real API call if you have one.
# Contract: return a dict with the same keys as REQUIRED_COLS.
def fetch_year_report_simulated(year: int, seed: int | None = None) -> dict:
    """
    Deterministic fake data for a given year.
    Keeps numbers stable per year for repeatable demos.
    """
    rnd = random.Random(seed if seed is not None else year)
    base = 1000 + 25 * (year - 1980)  # gentle growth
    revenue = base * (1 + 0.1 * rnd.random())
    cost = revenue * (0.65 + 0.1 * rnd.random())
    profit = revenue - cost
    price = 10 + 0.5 * (year - 1980) + rnd.random()
    return {
        "year": year,
        "revenue": round(revenue, 2),
        "profit": round(profit, 2),
        "cost": round(cost, 2),
        "price": round(price, 2),
    }

# Example template if you wire a real endpoint
def fetch_year_report_real(year: int) -> dict | None:
    """
    Example only. Adjust URL, params, and JSON parsing to your API.
    Should return a dict with keys year, revenue, profit, cost, price.
    Return None if the API has no data for that year.
    """
    url = "https://api.example.com/company/report"
    params = {"year": year}
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        j = r.json()
        if not j:
            return None
        return {
            "year": year,
            "revenue": float(j["revenue"]),
            "profit": float(j["profit"]),
            "cost": float(j["cost"]),
            "price": float(j["price"]),
        }
    except Exception as e:
        print(f"API error for {year}: {e}", file=sys.stderr)
        return None
# --------- end API layer ----------

def fill_missing_years(df: pd.DataFrame, start_y: int, end_y: int, use_real_api: bool = False) -> pd.DataFrame:
    have_years = set(df["year"].tolist())
    target_years = list(range(start_y, end_y + 1))
    missing_years = [y for y in target_years if y not in have_years]

    if not missing_years:
        print("Nothing missing in the requested range. Writing a copy with no changes.")
        return df.sort_values("year").reset_index(drop=True)

    print(f"Missing years in range {start_y} to {end_y}: {missing_years}")

    rows = []
    for y in missing_years:
        print(f"Fetching {y} ...")
        if use_real_api:
            rec = fetch_year_report_real(y)
        else:
            rec = fetch_year_report_simulated(y)
        if rec is None:
            print(f"No data for {y}. Skipping.")
            continue
        rows.append(rec)
        time.sleep(0.1)  # polite pause

    if rows:
        add_df = pd.DataFrame(rows, columns=REQUIRED_COLS)
        df = pd.concat([df, add_df], ignore_index=True)
    else:
        print("No rows fetched")

    df = df.sort_values("year").drop_duplicates(subset=["year"], keep="last").reset_index(drop=True)
    return df

def main():
    ap = argparse.ArgumentParser(description="Fill missing years in a CSV by calling an API for each missing year.")
    ap.add_argument("--csv-in", default="data.csv", help="input CSV path")
    ap.add_argument("--csv-out", default="data_filled.csv", help="output CSV path")
    ap.add_argument("--start", type=int, help="start year, inclusive")
    ap.add_argument("--end", type=int, help="end year, inclusive")
    ap.add_argument("--use-real-api", action="store_true", help="call the real API function instead of simulated data")
    args = ap.parse_args()

    df = read_csv(args.csv_in)
    start_y, end_y = ask_years_if_needed(args)

    out_df = fill_missing_years(df, start_y, end_y, use_real_api=args.use_real_api)
    Path(args.csv_out).parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(args.csv_out, index=False)
    print(f"Wrote {args.csv_out} with {len(out_df)} rows")

if __name__ == "__main__":
    main()
