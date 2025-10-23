from __future__ import annotations

import pandas as pd


def transform_df(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    # Make sure the timestamp column is in datetime format
    if df.get('timestamp') is not None and not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Convert numeric columns to nullable integer types 
    for col in ['status', 'size']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

    # Add extra columns hour, day, and weekday from timestamp
    if 'timestamp' in df.columns:
        df['hour'] = df['timestamp'].dt.hour
        df['day'] = df['timestamp'].dt.date
        df['weekday'] = df['timestamp'].dt.day_name()

    # Create status category
    if 'status' in df.columns:
        df['status_category'] = (df['status'] // 100).astype('Int64')

    # Lowercase paths to make searches easier
    if 'path' in df.columns:
        df['path_lower'] = df['path'].str.lower()
    return df
