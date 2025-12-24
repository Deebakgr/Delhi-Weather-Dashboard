# import pandas as pd

# def process_excel(filepath):
#     """Read Excel, normalize column names, and extract key features."""
#     df = pd.read_excel(filepath)
#     df.columns = [c.strip().lower() for c in df.columns]

#     # Identify date column
#     date_col = [c for c in df.columns if "date" in c or "time" in c or "datetime" in c][0]
#     df.rename(columns={date_col: "date"}, inplace=True)
#     df["date"] = pd.to_datetime(df["date"], errors="coerce")
#     df.dropna(subset=["date"], inplace=True)

#     # Extract temporal parts
#     df["year"] = df["date"].dt.year
#     df["month"] = df["date"].dt.month
#     df["day"] = df["date"].dt.day

#     # Map known columns from dataset
#     mapping = {
#         "_conds": "weather_condition",
#         "_tempm": "temperature",
#         "_hum": "humidity",
#         "_pressurem": "pressure",
#         "_heatindexm": "heat_index"
#     }
#     for src, tgt in mapping.items():
#         if src in df.columns:
#             df.rename(columns={src: tgt}, inplace=True)

#     # Ensure necessary columns exist
#     for c in ["weather_condition", "temperature", "humidity", "pressure", "heat_index"]:
#         if c not in df.columns:
#             df[c] = None

#     df = df[["date", "year", "month", "day", "temperature", "humidity", "pressure", "heat_index", "weather_condition"]]
#     return df


import pandas as pd
import numpy as np

def process_excel(filepath):
    """Read Excel, normalize column names, and extract key features safely (handles -9999 correctly)."""
    df = pd.read_excel(filepath)
    df.columns = [c.strip().lower() for c in df.columns]

    # Identify date column
    date_col = [c for c in df.columns if "date" in c or "time" in c or "datetime" in c]
    if not date_col:
        raise ValueError("❌ No date/time column found in dataset.")
    df.rename(columns={date_col[0]: "date"}, inplace=True)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df.dropna(subset=["date"], inplace=True)

    # Extract temporal parts
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day

    # Map known columns from dataset
    mapping = {
        "_conds": "weather_condition",
        "_tempm": "temperature",
        "_hum": "humidity",
        "_pressurem": "pressure",
        "_heatindexm": "heat_index"
    }
    for src, tgt in mapping.items():
        if src in df.columns:
            df.rename(columns={src: tgt}, inplace=True)

    # Clean -9999 and similar invalid placeholders
    numeric_cols = ["temperature", "humidity", "pressure", "heat_index"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].replace([-9999, -9999.0, -999, -99], np.nan)

    # Clean text-based -9999 (if any string data slipped in)
    text_cols = df.select_dtypes(include=["object"]).columns
    for col in text_cols:
        df[col] = df[col].replace(["-9999", "-999", "NA", "NaN"], np.nan)

    # Ensure necessary columns exist
    for c in ["weather_condition", "temperature", "humidity", "pressure", "heat_index"]:
        if c not in df.columns:
            df[c] = np.nan

    # Final column order
    df = df[["date", "year", "month", "day", "temperature", "humidity", "pressure", "heat_index", "weather_condition"]]

    print(f"✅ Processed {len(df)} rows | Cleaned -9999 values replaced with NaN (None).")
    return df
