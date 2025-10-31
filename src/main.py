from __future__ import annotations
import argparse
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
# --------- end API layer ----------

def results_functionality(df: pd.DataFrame, start_y: int, end_y: int, ): # void function
    main functionality
    loop through years
    in each loop check if the df has the year and if it does then simply pull the report,
    if the csv doesnt have then call the api function

    we can append all results of years in range to a list, and then after the loop we can basically create a new csv using pandas with said data. and we will export to the result.csv, to outpiut dir "Results"

def main():
    ap = argparse.ArgumentParser(description="Fill missing years in a CSV by calling an API for each missing year.")
    ap.add_argument("--csv-in", default="data.csv", help="input CSV path")
    ap.add_argument("--csv-out", default="data_filled.csv", help="output CSV path")
    ap.add_argument("--start", type=int, help="start year, inclusive")
    ap.add_argument("--end", type=int, help="end year, inclusive")
    ap.add_argument("--use-real-api", action="store_true", help="call the real API function instead of simulated data")
    args = ap.parse_args()

    print("Welcome to the Pharma Report Analysit Tool")

    start, end = ask_years()
    # asks for year ranges
    df = read_csv("Data/LogData.csv")
    # df for csv

    results_functionality(df, start, end)
    print ('results saved')


if __name__ == "__main__":
    main()
