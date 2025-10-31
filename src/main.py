from __future__ import annotations
from pathlib import Path
import sys
import time
import pandas as pd
import requests

REQUIRED_COLS = ["year", "revenue", "profit", "cost", "price"] # standard double check if the data we have has all the columns as needed, but it will in our case

def read_csv(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df.columns = [c.strip().lower() for c in df.columns]
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"CSV must have columns {REQUIRED_COLS}. Missing {missing}")
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["year"]).copy()
    df["year"] = df["year"].astype(int)
    df = df.sort_values("year").drop_duplicates(subset=["year"], keep="last") # duplicate removal
    return df

def ask_years():
    start = int(input("Start year: ").strip())
    end = int(input("End year: ").strip())
    if end < start:
        raise ValueError("End year must be greater than or equal to start year")
    return start, end

def fetch_year_report_api(year: int) -> dict | None:

    url = "https://pharamapi.com/financialReport/"
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

def results_functionality(df: pd.DataFrame, start_y: int, end_y: int) -> None:
    by_year = df.set_index("year")

    rows = []
    for year in range(start_y, end_y + 1):

        if year in by_year.index:
            s = by_year.loc[year]
            rec = {
                "year": int(year),
                "revenue": float(s["revenue"]),
                "profit": float(s["profit"]),
                "cost": float(s["cost"]),
                "price": float(s["price"]),
            }
        else:
   
            rec = fetch_year_report_api(year)
            if rec is None:
                print(f"No data available for {year}, skipping.", file=sys.stderr)
                continue

        rows.append(rec)
        time.sleep(0.05)  

    if not rows:
        print("No rows to write for the requested range.")
        return

    out_df = (
        pd.DataFrame(rows, columns=REQUIRED_COLS)
          .sort_values("year")
          .reset_index(drop=True)
    )

    out_dir = Path("Results")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "result.csv"
    out_df.to_csv(out_path, index=False)
    print(f"Wrote {out_path} with {len(out_df)} rows")

def main():

    print("Welcome to the Pharma Report Analysis Tool")

    start, end = ask_years()
    # asks for year ranges
    df = read_csv("Data/LogData.csv")
    # df for csv

    results_functionality(df, start, end)
    print ('results saved')


if __name__ == "__main__":
    main()
