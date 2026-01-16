#!/usr/bin/env python3
"""
Generate wide-format 7-day snowfall forecast CSVs (inches) for CA and CO
using Open-Meteo daily snowfall sums.
"""

import os
from datetime import datetime

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from combined_scraper import RESORT_DATA


CALIFORNIA_CSV = "california_resorts_combined.csv"
COLORADO_CSV = "colorado_resorts_combined.csv"

OUTPUT_CA = "california_snow_forecast.csv"
OUTPUT_CO = "colorado_snow_forecast.csv"


DAILY_VARS = [
    "snowfall_sum",
]


def _load_resorts(csv_path, state_label):
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df = df.rename(columns={"latitude": "Latitude", "longitude": "Longitude"})
        df = df[df["Latitude"].notna() & df["Longitude"].notna()]
        df["State"] = state_label
        return df[["name", "Latitude", "Longitude", "State"]]

    if state_label == "CO":
        fallback_rows = [
            {"name": name, "Latitude": data["lat"], "Longitude": data["lng"], "State": "CO"}
            for name, data in RESORT_DATA.items()
        ]
        return pd.DataFrame(fallback_rows)

    raise FileNotFoundError(f"Missing resort CSV: {csv_path}")


def _fetch_open_meteo_daily(lat, lon):
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ",".join(DAILY_VARS),
        "forecast_days": 7,
        "timezone": "auto",
    }
    resp = session.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=60)
    resp.raise_for_status()
    return resp.json()


def _cm_to_inches(values):
    return [round(float(value) / 2.54, 2) for value in values]


def _format_date_labels(date_strings):
    labels = []
    for value in date_strings:
        try:
            dt = datetime.fromisoformat(value)
            labels.append(f"{dt.month}/{dt.day}/{dt.year}")
        except (TypeError, ValueError):
            continue
    return labels


def _build_rows(resorts_df):
    rows = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_headers = None

    for _, row in resorts_df.iterrows():
        name = str(row["name"])
        lat = float(row["Latitude"])
        lon = float(row["Longitude"])

        try:
            payload = _fetch_open_meteo_daily(lat, lon)
            daily = payload.get("daily", {})
            snowfall_cm = daily.get("snowfall_sum", []) or []
            if date_headers is None:
                date_headers = _format_date_labels(daily.get("time", [])[:7])
        except requests.RequestException:
            snowfall_cm = []

        snowfall_in = _cm_to_inches(snowfall_cm[:7]) if snowfall_cm else []
        while len(snowfall_in) < 7:
            snowfall_in.append(0.0)

        total_7day = round(sum(snowfall_in), 2)
        days_with_snow = sum(1 for val in snowfall_in if val > 0)

        row_data = {
            "Resort": name,
            "Seven-day snowfall forecast": total_7day,
            "Forecasted snowfall days": days_with_snow,
            "Last_Updated": timestamp,
        }

        if date_headers:
            for idx, label in enumerate(date_headers):
                row_data[label] = snowfall_in[idx]
        else:
            for idx in range(7):
                row_data[f"Day{idx+1}"] = snowfall_in[idx]

        rows.append(row_data)

    if date_headers:
        ordered_columns = (
            ["Resort"]
            + date_headers
            + ["Seven-day snowfall forecast", "Forecasted snowfall days", "Last_Updated"]
        )
        return pd.DataFrame(rows)[ordered_columns]

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
