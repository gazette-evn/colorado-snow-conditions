#!/usr/bin/env python3
"""
Generate wide-format 7-day snowfall forecast CSVs (inches) for CA and CO
using Open-Meteo daily snowfall sums.
"""

import os
from datetime import datetime

import pandas as pd
import requests


CALIFORNIA_CSV = "california_resorts_combined.csv"
COLORADO_CSV = "colorado_resorts_combined.csv"

OUTPUT_CA = "california_snow_forecast.csv"
OUTPUT_CO = "colorado_snow_forecast.csv"


DAILY_VARS = [
    "snowfall_sum",
]


def _load_resorts(csv_path, state_label):
    df = pd.read_csv(csv_path)
    df = df.rename(columns={"latitude": "Latitude", "longitude": "Longitude"})
    df = df[df["Latitude"].notna() & df["Longitude"].notna()]
    df["State"] = state_label
    return df[["name", "Latitude", "Longitude", "State"]]


def _fetch_open_meteo_daily(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ",".join(DAILY_VARS),
        "forecast_days": 7,
        "timezone": "auto",
    }
    resp = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def _cm_to_inches(values):
    return [round(float(value) / 2.54, 2) for value in values]


def _build_rows(resorts_df):
    rows = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for _, row in resorts_df.iterrows():
        name = str(row["name"])
        lat = float(row["Latitude"])
        lon = float(row["Longitude"])

        payload = _fetch_open_meteo_daily(lat, lon)
        daily = payload.get("daily", {})
        snowfall_cm = daily.get("snowfall_sum", []) or []

        snowfall_in = _cm_to_inches(snowfall_cm[:7])
        while len(snowfall_in) < 7:
            snowfall_in.append(0.0)

        total_7day = round(sum(snowfall_in), 2)
        days_with_snow = sum(1 for val in snowfall_in if val > 0)

        rows.append({
            "Resort": name,
            "Day1": snowfall_in[0],
            "Day2": snowfall_in[1],
            "Day3": snowfall_in[2],
            "Day4": snowfall_in[3],
            "Day5": snowfall_in[4],
            "Day6": snowfall_in[5],
            "Day7": snowfall_in[6],
            "Total_7day": total_7day,
            "Days_With_Snow": days_with_snow,
            "Last_Updated": timestamp,
        })

    return pd.DataFrame(rows)


def _write_csv(df, output_path):
    df.to_csv(output_path, index=False)
    print(f"Saved {output_path} ({len(df)} rows)")


def main():
    run_ca = os.environ.get("RUN_CA", "").lower() in {"1", "true", "yes"}
    run_co = os.environ.get("RUN_CO", "true").lower() in {"1", "true", "yes"}

    if run_ca and os.path.exists(CALIFORNIA_CSV):
        ca_resorts = _load_resorts(CALIFORNIA_CSV, "CA")
        ca_df = _build_rows(ca_resorts)
        _write_csv(ca_df, OUTPUT_CA)

    if run_co:
        co_resorts = _load_resorts(COLORADO_CSV, "CO")
        co_df = _build_rows(co_resorts)
        _write_csv(co_df, OUTPUT_CO)


if __name__ == "__main__":
    main()
