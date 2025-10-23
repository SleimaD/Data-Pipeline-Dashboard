# Data Pipeline Dashboard

A **hands-on data engineering and analytics project** built with **Python, Pandas, and Streamlit**.  
It simulates a small end-to-end data pipeline from raw log ingestion to data cleaning, anomaly detection, and interactive visualization.  
The goal is to **learn by doing** and practice how each part of a simple data workflow connects together in a clear and maintainable way.

---

## Project Overview

The **Data Pipeline Dashboard** is a small internal tool that:

-  Ingests raw **Apache/Nginx log files** (or any text-based log dataset)
-  Cleans and transforms the data into structured form (with Pandas)
-  Detects anomalies and suspicious activity using simple logic rules
-  Displays insights and statistics in an interactive Streamlit dashboard

It’s inspired by the type of workflow used in **data, cyber, or DevOps teams**, but simplified to show core concepts clearly.

---


## 📊 Dashboard Preview

<div align="center">

🧩 **Streamlit interface preview**

| Upload view | Dashboard overview |
|--------------|-------------------|
| ![Upload view](assets/dashboard_upload.png) | ![Dashboard overview](assets/dashboard_overview.png) |

| Charts | Detected anomalies |
|--------|--------------------|
| ![Charts](assets/dashboard_charts.png) | ![Detected anomalies](assets/dashboard_anomalies.png) |

</div>

_The dataset used for this demo is a sample log file (non-sensitive, for testing purposes only)._


---


##  Why I Built This Project

I wanted to build a small project that helps me **practice how data pipelines work end-to-end** from ingestion to visualization.  
It was also an opportunity to write clean, modular Python code and create a simple dashboard for non-technical users.  
Through it, I strengthened my skills in **Pandas**, **Streamlit**, and **data transformation**, while learning how to structure a clear and maintainable data workflow.


---

## ⚙️ Tech Stack

| Category | Tools / Libraries |
|-----------|--------------------|
| Language | Python 3.10+ |
| Data manipulation | Pandas, NumPy |
| Dashboard | Streamlit, Altair |
| Data storage | CSV files (local) |
| Automation | Python scripts (CLI) |


---

## How the Pipeline Works

1️ **Ingestion** : Reads `.log` file, extracts key fields (IP, timestamp, path, status...).  
2️ **Transformation** : Converts to clean DataFrame (adds time columns, categories...).  
3️ **Detection** : Finds bursts of failed requests, sensitive path access, high request volumes.  
4️ **Visualization** : Interactive dashboard with charts & key metrics.

---

##  How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/SleimaD/Data-Pipeline-Dashboard.git
cd Data-Pipeline-Dashboard
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate    # On macOS/Linux
# or
venv\Scripts\activate       # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the pipeline 
```bash
python run_pipeline.py -i data/sample_access.log -o data
```
This command will create two new CSV files:
- `data/processed.csv` → cleaned and structured data
- `data/findings.csv` → detected anomalies

### 5. Launch the dashboard
```bash
streamlit run app.py
```
Then open the link shown in the terminal and:
- Upload your own `.log` file (Apache/Nginx format)
- Explore the metrics and visual charts

---

##  Features

**Log ingestion** (supports `.log` or `.txt`)

**Data transformation**: converts timestamps, cleans numeric fields, adds derived columns

**Anomaly detection**:
- Bursts of 401/403 (failed logins)
- Access to sensitive paths 
- Abnormally high request volume from a single IP

**Dashboard** built with Streamlit:
- Requests per hour chart
- HTTP status category breakdown
- Top 10 active IPs
- Error rate metrics
- Download buttons for processed data & anomalies

---


💬 Feel free to share feedback or ideas for improvement!

- 💻 GitHub: [SleimaD](https://github.com/SleimaD)
- 🔗 LinkedIn: [Sleima Ducros](https://linkedin.com/in/sleima-ducros)

