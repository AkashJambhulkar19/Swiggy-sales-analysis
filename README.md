# 🍕 Swiggy Sales Analysis — End-to-End Data Analyst Portfolio Project

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-3.0-150458?style=flat&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-7.1-3F4F75?style=flat&logo=plotly&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Excel](https://img.shields.io/badge/Excel-PowerBI_Ready-217346?style=flat&logo=microsoftexcel&logoColor=white)

**An end-to-end sales analysis of Swiggy (NSE: SWIGGY) covering Food Delivery, Instamart, Swiggy One, and competitive positioning — FY2022 to FY2025**

[📊 View Dashboard](#dashboard) · [🗄️ SQL Analysis](#sql-queries) · [📓 Notebooks](#notebooks) · [📈 Key Findings](#key-findings)

</div>

---

## 📌 Project Overview

This project performs a comprehensive sales analysis of **Swiggy Limited** — India's leading food delivery and quick-commerce platform — using real publicly available financial data from Swiggy's DRHP, IPO filings, and quarterly investor reports.

**Business Questions Answered:**
- Which Indian cities drive the most food delivery revenue?
- How explosive is Instamart's growth vs Food Delivery?
- What does Swiggy's path to profitability look like?
- How does Swiggy stack up against Zomato across all segments?
- What impact does Swiggy One membership have on order behavior?

---

## 📊 Dashboard

Open `dashboard/swiggy_dashboard.html` in any browser — no server required.

### Dashboard Tabs:
| Tab | Contents |
|-----|----------|
| 📊 **Overview** | KPI cards, Revenue vs Loss trend, Quarterly performance, Path to profitability |
| 🍔 **Food Delivery** | Top 15 cities by GOV, AOV vs Delivery time scatter, User & partner growth |
| 🛒 **Instamart** | GOV explosive growth, Dark store expansion, City-wise Instamart analysis |
| 🏙️ **City Analysis** | Tier 1 vs Tier 2 vs Tier 3 GOV contribution over 4 years |
| 💳 **Swiggy One** | Subscriber growth, Member vs Non-member AOV & order frequency |
| ⚔️ **vs Zomato** | Revenue, GOV, market share, and quick-commerce head-to-head |

---

## 📁 Project Structure

```
swiggy_sales_analysis/
│
├── data/
│   ├── raw/
│   │   ├── swiggy_annual_financials.csv      # Real national figures (DRHP + filings)
│   │   ├── swiggy_quarterly_results.csv      # Quarterly P&L (Q1FY24 to Q1FY27)
│   │   ├── food_delivery_city_data.csv       # 26 cities × 4 fiscal years
│   │   ├── instamart_city_data.csv           # 20 cities × 4 fiscal years
│   │   ├── swiggy_one_membership.csv         # Monthly membership metrics
│   │   └── competitor_comparison.csv         # Swiggy vs Zomato by year
│   └── cleaned/
│       └── swiggy_master_fy2024.csv          # Merged master dataset
│
├── notebooks/
│   ├── 02_food_delivery_analysis.py          # Food delivery EDA
│   └── (additional notebooks)
│
├── sql/
│   └── swiggy_business_questions.sql         # 20 SQL business queries
│
├── dashboard/
│   └── swiggy_dashboard.html                 # 6-tab interactive dashboard
│
├── powerbi_data/
│   └── swiggy_powerbi_ready.xlsx             # 8-sheet Power BI ready Excel
│
├── generate_data.py                          # Master data generation script
├── generate_dashboard.py                     # Dashboard builder
└── export_powerbi.py                         # Excel export script
```

---

## 🔢 Real Data Used (Sources)

| Metric | FY2022 | FY2023 | FY2024 |
|--------|--------|--------|--------|
| Revenue (₹ Cr) | 5,705 | 8,265 | 11,634 |
| Net Loss (₹ Cr) | 3,629 | 3,758 | 1,888 |
| Food Delivery GOV (₹ Cr) | 13,800 | 22,000 | 27,000 |
| Instamart GOV (₹ Cr) | 500 | 3,000 | 8,069 |
| Dark Stores | 200 | 400 | 605 |
| Monthly Users (Mn) | 8 | 11 | 13 |

**Sources:** Swiggy DRHP (SEBI Filing Sep 2024) · NSE Quarterly Reports · Swiggy Investor Relations

> ⚠️ **Data Disclaimer:** National-level metrics are sourced from Swiggy's real public filings. City-level breakdown is **realistic synthetic data** calibrated to match official national totals. This is standard practice in portfolio projects where granular data is not publicly available.

---

## 🔍 Key Findings

### 🍔 Food Delivery
- **Bengaluru, Delhi NCR, Mumbai** together contribute **~43% of national food delivery GOV**
- Tier 2 cities (Jaipur, Lucknow, Indore) show **24-28% YoY growth** — outpacing Tier 1 cities
- Mumbai has the highest AOV (₹490) vs Patna at ₹300 — showing urban pricing premiums
- Hyderabad has the **fastest delivery time** (~30 min) among Tier 1 cities

### 🛒 Instamart
- GOV grew from **₹500 Cr → ₹8,069 Cr in just 2 years** — a **29x surge**
- Bengaluru leads with **95 dark stores** and 20% of national Instamart GOV
- Average delivery time is **11-14 minutes** in Tier 1 cities (within 15-min promise)
- By Q1 FY2027, Instamart reached **contribution breakeven** — unit economics validated

### 💳 Swiggy One
- Members order **4.2x more** per month than non-members
- Member AOV (₹510) is **34% higher** than non-member AOV (₹380)
- Subscription revenue at ₹99/month covers free delivery costs with a net margin

### ⚔️ vs Zomato
- Zomato turned profitable in FY2024 (₹351 Cr profit) while Swiggy remains loss-making
- Swiggy holds **~44% food delivery market share** vs Zomato's 56%
- Quick commerce battle: **Blinkit (791 stores) vs Instamart (605)** — Blinkit ahead but gap narrowing

---

## 🗄️ SQL Queries

The `sql/swiggy_business_questions.sql` file contains **20 business questions** covering:
- Window functions: `RANK()`, `ROW_NUMBER()`, `LAG()`, `SUM() OVER`
- CTEs for complex multi-step analysis
- JOINs across multiple dimension tables
- Subqueries for above-average comparisons
- Aggregations: revenue by segment, tier, city, quarter

---

## 📓 Notebooks

| Notebook | Analysis |
|----------|----------|
| `02_food_delivery_analysis.py` | City-wise GOV, AOV, delivery time, tier comparison |

---

## 🚀 Setup & Run

### Prerequisites
```bash
pip install pandas plotly openpyxl
```

### Generate Everything
```bash
# Step 1: Generate all CSV datasets
python generate_data.py

# Step 2: Build interactive dashboard
python generate_dashboard.py

# Step 3: Export Power BI Excel
python export_powerbi.py
```

### Open Dashboard
Open `dashboard/swiggy_dashboard.html` in Chrome, Firefox, or Edge.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.13** | Core language |
| **Pandas** | Data manipulation & cleaning |
| **Plotly** | Interactive visualizations |
| **SQLite / SQL** | Business query analysis |
| **openpyxl** | Excel export for Power BI |
| **Matplotlib / Seaborn** | Notebook-level charts |

---

## 👤 About

Built by **Akash** as a portfolio project for Data Analyst job applications.

**LinkedIn:** [Add your LinkedIn]  
**Email:** [Add your email]

---

*This is a portfolio/educational project. All company names and trademarks belong to their respective owners. Financial data is sourced from publicly available regulatory filings.*
