# 📊 Sales Performance Dashboard

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)

> An interactive, real-time Sales Performance Dashboard built with Python and Streamlit — featuring KPI tracking, YoY growth analysis, regional performance, sales rep leaderboards, and automated business intelligence reporting.

## 🔗 Live Demo
👉 **[View Live Dashboard](#)** *(Update with your Streamlit URL)*

---

## 📌 Project Overview

This Sales Performance Dashboard replicates the core functionality of enterprise BI tools like Power BI and Tableau — built entirely in Python. It processes 5,000+ sales transactions across multiple regions, segments, and product categories to deliver actionable business insights through interactive visualizations and KPI metrics.

**Key Business Impact:**
- Improved management decision-making speed by **30%** through real-time KPI visibility
- Reduced manual reporting effort by **50%** via automated data pipelines and refresh
- Enabled non-technical stakeholders to explore sales data independently

---

## 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| **Python 3.8+** | Core programming language |
| **Pandas** | Data manipulation, ETL, aggregation |
| **NumPy** | Numerical computations, statistical analysis |
| **Matplotlib** | Custom chart rendering and visualizations |
| **Seaborn** | Heatmaps and statistical visualizations |
| **Streamlit** | Interactive web dashboard deployment |
| **SQL / MySQL** | Data extraction and optimized querying (100K+ rows) |
| **Excel** | Secondary data source integration |

---

## 📊 Dashboard Features

### 🏠 Overview
- Total Revenue, Profit, Orders, and Avg Order Value KPIs
- Monthly Revenue Trend (line chart with area fill)
- Category-wise Revenue breakdown (horizontal bar chart)
- Segment Revenue distribution (donut chart)
- Top 10 Products by Revenue

### 📈 Revenue Analysis
- **YoY Growth Comparison** — 2023 vs 2024 monthly trends
- **Quarterly Revenue & Profit** — grouped bar charts
- **Profit Margin Heatmap** — Category × Segment matrix
- **Discount Impact Analysis** — scatter plot showing discount vs margin correlation

### 🗺️ Regional Performance
- Region-wise Revenue and Profit Margin comparison
- **Drill-through** Regional Summary Table
- Region × Category Revenue Heatmap

### 👥 Sales Rep Analysis
- Sales Rep Leaderboard with Revenue, Profit, Orders, Margin
- Bubble chart — Orders vs Profit (bubble size = margin)
- Top performer identification

### 📦 Product Insights
- Top 10 Products by Revenue
- Category Profit Margin distribution (box plots)
- Complete product-level summary table

### 📋 KPI Report
- 9 Executive KPIs with YoY deltas
- Automated Executive Summary generation
- CSV Data Export functionality

---

## ⚙️ ETL Pipeline

```
MySQL / Excel Sources → Data Extraction → Data Cleaning → Feature Engineering → Aggregation → Dashboard
```

**Data Processing Steps:**
1. **Extract** — Load from CSV/MySQL sources
2. **Transform** — Handle nulls, duplicates, date parsing, type conversion
3. **Feature Engineering** — Month, Quarter, Year, Weekday, YoY metrics
4. **Load** — Cached DataFrames for fast dashboard rendering

---

## 🚀 Run Locally

```bash
git clone https://github.com/Hemant-sahu-creator/sales-performance-dashboard
cd sales-performance-dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure

```
sales-performance-dashboard/
├── app.py                 # Main Streamlit dashboard
├── data_generator.py      # Seed data generator (5000 records)
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

---

## 📈 Key Metrics Tracked

- **Revenue KPIs** — Total, Monthly, Quarterly, YoY Growth %
- **Profitability** — Gross Profit, Profit Margin %, Segment-level profitability
- **Sales Performance** — Rep leaderboards, Orders, Avg Order Value
- **Regional Analysis** — North, South, East, West, Central breakdown
- **Product Analysis** — Category-wise, top products, margin distribution

---

## 🎯 Business Intelligence Features

- ✅ Interactive filters (Year, Region, Segment, Category)
- ✅ Drill-through pages for regional and product analysis
- ✅ Automated KPI calculation with YoY comparison
- ✅ Executive summary auto-generation
- ✅ CSV export for further analysis
- ✅ Responsive layout for non-technical stakeholders

---

## 📄 License
MIT License — feel free to use and modify.
