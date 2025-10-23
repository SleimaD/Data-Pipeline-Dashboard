#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os

from src.ingest import parse_log_file
from src.transform import transform_df
from src.detect import detect_anomalies


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Runs the full pipeline: ingestion, transformation and anomaly detection"
    )
    parser.add_argument(
        '--input', '-i', required=True, help="Path to the Apache log file to analyze"
    )
    parser.add_argument(
        '--outdir', '-o', default='data', help="Directory where CSV files will be saved"
    )
    parser.add_argument(
        '--error-threshold', type=int, default=3, help="Minimum number of 401/403 errors to trigger a burst alert"
    )
    parser.add_argument(
        '--window-minutes', type=int, default=1, help="Window size (in minutes) for counting bursts"
    )
    args = parser.parse_args()

    log_path = args.input
    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    # Ingestion
    print(f"Reading file {log_path}...")
    df_raw = parse_log_file(log_path)
    print(f"{len(df_raw)} valid lines read.")

    # Transformation
    df_processed = transform_df(df_raw)
    processed_path = os.path.join(outdir, 'processed.csv')
    df_processed.to_csv(processed_path, index=False)
    print(f"Processed data saved to {processed_path}")

    # Detection
    df_findings = detect_anomalies(
        df_processed,
        error_threshold=args.error_threshold,
        window_minutes=args.window_minutes
    )
    findings_path = os.path.join(outdir, 'findings.csv')
    df_findings.to_csv(findings_path, index=False)
    print(f"Detected anomalies saved to {findings_path}")


if __name__ == '__main__':
    main()
