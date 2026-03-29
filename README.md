# NewsSumm++

🚀 An end-to-end, data-centric AI pipeline for text summarization datasets. NewsSumm++ cleans raw article-summary pairs, engineers NLP features, extracts named entities with spaCy, generates analytics outputs, and launches an interactive Streamlit dashboard for exploration.

## 🚀 Project Overview

NewsSumm++ transforms raw summarization data into a richer, analysis-ready dataset.

It performs the complete workflow:

- cleans noisy `article` and `summary` text
- removes duplicates and low-quality short rows
- computes useful textual statistics
- extracts named entities using spaCy
- generates analytics tables and visualizations
- logs pipeline activity to file and terminal
- launches a Streamlit dashboard for browser-based analysis

This repository follows a practical data-centric AI approach: improve the quality of the dataset first, then analyze and evaluate the outcome.

## 🏗️ Architecture / Flow

```text
Raw Data
   |
   v
cleaning.py
   |
   v
feature_engineering.py
   |
   v
entity_extraction.py
   |
   v
metrics.py + visualization.py
   |
   v
Processed Files + Logs + Dashboard
```

### Modular Components

```text
main.py
```
Runs the full pipeline end to end.

```text
src/cleaning.py
```
Loads the dataset, cleans text, removes duplicates, and filters short rows.

```text
src/feature_engineering.py
```
Adds `doc_length`, `summary_length`, `compression_ratio`, and `readability_score`.

```text
src/entity_extraction.py
```
Loads spaCy and computes `entity_count` for each article.

```text
src/metrics.py
```
Creates analytics tables such as dataset stats, main results, and error analysis.

```text
src/visualization.py
```
Generates saved graphs for length distribution and readability comparison.

```text
app.py
```
Launches the Streamlit dashboard.

```text
logger.py
```
Provides a reusable custom logger for console and file logging.

```text
config.yaml
```
Stores configurable paths and runtime parameters.

## 🛠️ Tech Stack

```text
Language      : Python
Data Handling : Pandas, OpenPyXL
NLP           : spaCy, textstat
Visualization : Matplotlib
Dashboard     : Streamlit
Config        : PyYAML
Evaluation    : ROUGE, Hugging Face Evaluate, Transformers
```

## ⚙️ How to Run

NewsSumm++ supports a one-click workflow:

```bash
./run_all.sh
```

On Windows PowerShell with Git Bash:

```powershell
& "C:\Program Files\Git\bin\bash.exe" -lc "./run_all.sh"
```

### What `run_all.sh` does

```text
1. Creates a virtual environment
2. Installs required dependencies
3. Downloads the spaCy English model
4. Runs the NewsSumm++ pipeline
5. Launches the Streamlit dashboard
```

After execution, open the local URL printed in the terminal.

## 📊 Key Features

### Data Cleaning

- removes duplicate records
- filters very short rows
- applies basic text normalization

### NLP Feature Engineering

- `doc_length`
- `summary_length`
- `compression_ratio`
- `readability_score`

### Entity Extraction

- uses spaCy for named entity detection
- adds `entity_count` as a structured feature

### Analytics and Monitoring

- generates summary tables in Excel and CSV
- creates saved visualizations
- writes structured logs to terminal and file
- provides an interactive dashboard for dataset exploration

## 📈 Output Generated

### Processed Dataset

```text
data/processed/newssum_plus_plus.xlsx
```

### Analytics Tables

```text
outputs/tables/dataset_stats.xlsx
outputs/tables/main_results.xlsx
outputs/tables/error_analysis.xlsx
```

CSV versions are also generated for easy viewing and sharing.

### Graphs

```text
outputs/graphs/document_length_distribution.png
outputs/graphs/readability_comparison.png
```

### Logs

```text
logs/pipeline.log
```

### Dashboard

The Streamlit app includes:

- Data Overview
- Quality Metrics
- Visualizations
- Model Evaluation

## 🌟 Why NewsSumm++?

NewsSumm++ is more than a simple preprocessing script. It is a modular, presentation-ready NLP pipeline that combines:

- data cleaning
- feature enrichment
- analytics generation
- logging and monitoring
- dashboard-based inspection

It is well-suited for:

- NLP portfolio projects
- academic submissions
- data-centric AI demonstrations
- summarization dataset analysis workflows

## 📂 Repository Structure

```text
NewsSummProject/
├── app.py
├── config.yaml
├── evaluate_baseline.py
├── logger.py
├── main.py
├── requirements.txt
├── requirements-eval.txt
├── run_all.sh
├── data/
│   ├── raw/
│   └── processed/
├── logs/
├── outputs/
│   ├── graphs/
│   └── tables/
├── results/
├── src/
│   ├── cleaning.py
│   ├── config_utils.py
│   ├── entity_extraction.py
│   ├── feature_engineering.py
│   ├── metrics.py
│   └── visualization.py
└── tests/
```

## 🤝 Closing Note

NewsSumm++ demonstrates how raw summarization data can be transformed into a cleaner, richer, and more explainable dataset through a structured NLP workflow.

If you are exploring data-centric AI, NLP preprocessing, or lightweight MLOps-style project design, this repository provides a strong practical foundation.
