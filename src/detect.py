from __future__ import annotations

from typing import List, Dict, Any

import pandas as pd


def detect_anomalies(
    df: pd.DataFrame,
    error_threshold: int = 3,
    window_minutes: int = 1,
    sensitive_paths: List[str] | None = None,
) -> pd.DataFrame:
    findings: List[Dict[str, Any]] = []
    if df.empty:
        return pd.DataFrame(columns=['timestamp', 'ip', 'path', 'signal', 'score'])

    df_sorted = df.sort_values('timestamp')

    # Detect bursts of 401/403 errors 
    error_codes = {401, 403}
    err_df = df_sorted[df_sorted['status'].isin(error_codes)].copy()

    # Group by ip so we can analyze each IP's activity independently
    for ip, group in err_df.groupby('ip'):

        # Reset index to make it easier to iterate over timestamps by position
        times = group['timestamp'].reset_index(drop=True)

        # Slide over each timestamp to find a window with enough errors
        for i in range(len(times)):
            start_time = times[i]
            end_time = start_time + pd.Timedelta(minutes=window_minutes)
            count = ((times >= start_time) & (times < end_time)).sum()
            
            if count >= error_threshold:

                row = group.iloc[i]

                findings.append({
                    'timestamp': row['timestamp'],
                    'ip': ip,
                    'path': row['path'],
                    'signal': 'burst_401_403',
                    'score': int(count)
                })
                break  # Stop after finding the first burst for this IP

    # Detect accesses to sensitive paths which might indicate probing or attacks
    if sensitive_paths is None:
        sensitive_paths = [
            '/.env', '/wp-admin', '/wp-login', '/wp-login.php', '/admin', '/login',
            '/.git', '/.ds_store', '/etc/passwd', '/wp-config', '/wp-content',
            '/cgi-bin', '/secret', '/config', '/system', '/dashboard'
        ]

    # Check each log entry's path against sensitive path keywords
    for _, row in df_sorted.iterrows():
        for sp in sensitive_paths:

            # Use lowercase comparison to catch case variations
            if sp.lower() in (row.get('path_lower') or ''):
                findings.append({
                    'timestamp': row['timestamp'],
                    'ip': row['ip'],
                    'path': row['path'],
                    'signal': 'sensitive_path',
                    'score': 1
                })
                break 

    # Detect IPs with unusually high request volumes compared to others
    count_series = df_sorted.groupby('ip').size()

    if not count_series.empty:

        std = count_series.std()

        # if std is zero or NaN then fallback to max count
        if pd.isna(std) or std == 0:
            threshold = count_series.max()
        else:
            threshold = count_series.mean() + 3 * std   # Use mean + 3*std deviation as threshold to find outliers,

        for ip, total in count_series[count_series > threshold].items():

            # Record the first occurrence for this ip as representative
            row = df_sorted[df_sorted['ip'] == ip].iloc[0]
            findings.append({
                'timestamp': row['timestamp'],
                'ip': ip,
                'path': row['path'],
                'signal': 'high_volume',
                'score': int(total)
            })

    return pd.DataFrame(findings, columns=['timestamp', 'ip', 'path', 'signal', 'score'])
