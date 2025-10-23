from __future__ import annotations

import streamlit as st
import pandas as pd

from src.ingest import parse_log_file
from src.transform import transform_df
from src.detect import detect_anomalies
from src.viz_utils import bar_chart  # small helper to keep charts consistent (ordering + horizontal labels)


def main() -> None:
    #Entry point of the Streamlit app

    st.set_page_config(page_title="Log Analyzer Dashboard", layout="wide")
    st.title(" Log Analyzer Dashboard")
    st.write("Upload an Apache log file (Common/Combined Log Format) to start the analysis.")

    uploaded_file = st.file_uploader("Select a .log or .txt file", type=["log", "txt"])  
    if uploaded_file is None:
        st.info("No file selected. Please upload a log file to start the analysis.")
        return

    # Ingestion
    with st.spinner("Reading and parsing the file..."):
        df_raw = parse_log_file(uploaded_file)
    if df_raw.empty:
        st.warning("No valid lines were found in the file.")
        return

    # Transformation
    with st.spinner("Cleaning and enriching data..."):
        df = transform_df(df_raw)

    # Detection
    with st.spinner("Detecting anomalies..."):
        findings = detect_anomalies(df)

    # Display global metrics
    st.subheader("📊 Overall statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Number of requests", len(df))
    col2.metric("Unique IPs", df['ip'].nunique())
    error_rate = (df['status'] >= 400).mean() * 100
    col3.metric("Error rate (≥400)", f"{error_rate:.2f}%")

    # Chart. requests per hour
    st.subheader("Requests per hour")
    hour_counts = df.groupby('hour').size().reset_index(name='count')

    # Make sure hour is numeric and sorted 
    hour_counts['hour'] = hour_counts['hour'].astype(int)
    hour_counts = hour_counts.sort_values('hour')
    st.altair_chart(
        bar_chart(
            hour_counts, x='hour', y='count',
            title='Requests per hour',
            x_sort=list(range(24)),  # explicit order for the x axis
            label_angle=0            # keep labels horizontal
        ),
        use_container_width=True
    )

    # Chart. HTTP status category distribution
    st.subheader("HTTP status category breakdown")
    status_counts = df['status_category'].value_counts().sort_index().reset_index()
    status_counts.columns = ['status_category', 'count']

    # Ensure numeric type and ascending order: 2, 3, 4, 5
    status_counts['status_category'] = status_counts['status_category'].astype(int)
    status_counts = status_counts.sort_values('status_category')
    st.altair_chart(
        bar_chart(
            status_counts, x='status_category', y='count',
            title='HTTP status category breakdown',
            x_sort=[2, 3, 4, 5],
            label_angle=0
        ),
        use_container_width=True
    )

    # Chart. top 10 active IPs
    st.subheader("Top 10 most active IPs")
    top_ips = df['ip'].value_counts().head(10).reset_index()
    top_ips.columns = ['ip', 'count']
    st.altair_chart(
        bar_chart(
            top_ips, x='ip', y='count',
            title='Top 10 most active IPs',
            x_sort='-y',           # sort bars by count descending 
            label_angle=0
        ),
        use_container_width=True
    )

    # table for transformed data
    st.subheader("Transformed data (preview)")
    st.dataframe(df.head(1000))
    csv_proc = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=" Download transformed data (CSV)",
        data=csv_proc,
        file_name="processed.csv",
        mime='text/csv'
    )

    # table for detected anomalies 
    st.subheader("Detected anomalies")
    if findings.empty:
        st.info("No anomalies detected with current rules.")
    else:
        st.dataframe(findings)
        csv_find = findings.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=" Download anomalies (CSV)",
            data=csv_find,
            file_name="findings.csv",
            mime='text/csv'
        )


if __name__ == '__main__':
    main()
