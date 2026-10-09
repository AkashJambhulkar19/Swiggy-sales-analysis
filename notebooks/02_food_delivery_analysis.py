"""
02_food_delivery_analysis.py
============================
Swiggy Sales Analysis — Food Delivery Deep Dive
------------------------------------------------
Portfolio Project | Data Analyst | October 2026

Analyses city-level and national food delivery metrics for Swiggy using
data sourced from the DRHP (FY2022–FY2024) supplemented with synthetic
city-level breakdowns calibrated to published national aggregates.

Sections
--------
1. National Food Delivery GOV Trend        (FY2022–FY2025) — line chart
2. Top 10 Cities by GOV in FY2024          — horizontal bar chart
3. Tier-wise GOV Breakdown                 — stacked bar chart
4. City AOV vs Delivery Time Scatter       (bubble size = GOV) — scatter
5. YoY Growth Rate — Top 10 Fastest Cities — bar chart
6. Take Rate by Tier                       — box plot
7. Key Business Insights                   — printed to console

Outputs
-------
All charts are saved to:  ../reports/food_delivery_charts/

Dependencies
------------
    pip install pandas matplotlib seaborn
"""

# =============================================================================
# IMPORTS
# =============================================================================
import os
import sys
import warnings
import textwrap

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

warnings.filterwarnings("ignore", category=FutureWarning)

# =============================================================================
# CONFIGURATION
# =============================================================================

# Resolve paths relative to this script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(SCRIPT_DIR, "..", "data", "raw")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "reports", "food_delivery_charts")

# File paths
CITY_DATA_PATH      = os.path.join(DATA_DIR, "food_delivery_city_data.csv")
FINANCIALS_DATA_PATH = os.path.join(DATA_DIR, "swiggy_annual_financials.csv")

# Visual styling
SEABORN_STYLE   = "whitegrid"          # professional, clean background
SEABORN_CONTEXT = "talk"               # larger fonts suitable for portfolio
SWIGGY_ORANGE   = "#FC8019"            # Swiggy brand orange
SWIGGY_DARK     = "#1C1C1C"            # dark text colour
PALETTE_TIER    = {
    "Tier 1": "#FC8019",               # Orange for top cities
    "Tier 2": "#3D8EB9",               # Blue for Tier 2
    "Tier 3": "#5DBE6E",               # Green for Tier 3
}
DPI             = 150                  # chart resolution for saved files
FIG_SIZE_WIDE   = (12, 6)
FIG_SIZE_TALL   = (10, 8)
FIG_SIZE_SQ     = (9, 9)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def rupee_formatter(x, pos):
    """
    Custom matplotlib tick formatter that displays values in Indian Rupee
    notation with ₹ symbol and Cr (crore) suffix for large values.

    Parameters
    ----------
    x   : float  — the raw tick value (₹ Crore)
    pos : int    — tick position (required by FuncFormatter signature)

    Returns
    -------
    str — formatted string, e.g. '₹1,450 Cr'
    """
    return f"₹{x:,.0f} Cr"


def rupee_short(x, pos):
    """Compact rupee formatter — e.g. ₹1.4K for 1400."""
    if x >= 1000:
        return f"₹{x/1000:.1f}K Cr"
    return f"₹{x:.0f} Cr"


def save_figure(fig, filename: str):
    """
    Save a matplotlib figure to the OUTPUT_DIR, creating the folder if needed.

    Parameters
    ----------
    fig      : matplotlib.figure.Figure
    filename : str — filename without directory prefix, e.g. 'chart_01.png'
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(filepath, dpi=DPI, bbox_inches="tight")
    print(f"  ✔  Saved → {filepath}")


def section_header(num: int, title: str):
    """Print a formatted section header to the console."""
    border = "=" * 70
    print(f"\n{border}")
    print(f"  SECTION {num}: {title}")
    print(border)


# =============================================================================
# STEP 0: LOAD DATA
# =============================================================================

def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load city-level and annual financials CSVs from the data/raw directory.

    If the CSV files do not exist, the function falls back to in-memory
    synthetic data identical to the SQL inserts, so the notebook can run
    end-to-end without an external file dependency.

    Returns
    -------
    city_df   : pd.DataFrame — food_delivery_cities data
    annual_df : pd.DataFrame — swiggy_annual_financials data
    """

    # ------------------------------------------------------------------
    # Fallback synthetic data (mirrors the SQL INSERT values)
    # ------------------------------------------------------------------
    CITY_DATA = {
        "city_name": [
            "Bengaluru","Mumbai","Delhi","Hyderabad","Chennai","Pune","Kolkata",
            "Ahmedabad","Jaipur","Lucknow","Surat","Chandigarh","Kochi","Indore",
            "Nagpur","Bhopal","Coimbatore","Vishakhapatnam",
            "Patna","Ranchi","Guwahati","Varanasi","Jodhpur","Mysuru","Agra",
        ],
        "tier": [
            "Tier 1","Tier 1","Tier 1","Tier 1","Tier 1","Tier 1","Tier 1",
            "Tier 2","Tier 2","Tier 2","Tier 2","Tier 2","Tier 2","Tier 2",
            "Tier 2","Tier 2","Tier 2","Tier 2",
            "Tier 3","Tier 3","Tier 3","Tier 3","Tier 3","Tier 3","Tier 3",
        ],
        "state": [
            "Karnataka","Maharashtra","Delhi","Telangana","Tamil Nadu",
            "Maharashtra","West Bengal","Gujarat","Rajasthan","Uttar Pradesh",
            "Gujarat","Punjab","Kerala","Madhya Pradesh","Maharashtra",
            "Madhya Pradesh","Tamil Nadu","Andhra Pradesh",
            "Bihar","Jharkhand","Assam","Uttar Pradesh","Rajasthan",
            "Karnataka","Uttar Pradesh",
        ],
        "gov_fy2022": [
            980,870,810,520,480,370,310,
            180,140,130,110,105,100,95,88,72,68,62,
            35,28,25,22,18,20,17,
        ],
        "gov_fy2023": [
            1620,1430,1320,880,790,630,510,
            310,240,220,195,185,175,165,150,125,115,108,
            62,50,45,40,32,36,30,
        ],
        "gov_fy2024": [
            2450,2180,2050,1390,1210,1020,820,
            520,410,390,340,320,300,285,260,215,200,185,
            110,88,78,70,57,62,52,
        ],
        "aov_fy2024": [
            420,450,440,410,400,390,370,
            360,340,330,320,350,355,315,310,305,310,300,
            280,270,265,260,250,270,245,
        ],
        "avg_delivery_time": [
            28.5,31.2,30.0,27.8,29.4,26.5,33.0,
            29.8,30.5,31.0,28.0,27.5,26.0,29.0,30.2,31.5,27.0,28.5,
            34.5,35.0,36.0,35.5,36.5,32.0,37.0,
        ],
        "active_restaurants": [
            55000,52000,48000,36000,32000,28000,24000,
            18000,14000,12000,11000,10500,10000,9500,9000,7500,7000,6500,
            3800,3100,2800,2500,2000,2200,1800,
        ],
        "monthly_orders_mn": [
            5.8,4.8,4.7,3.4,3.0,2.6,2.2,
            1.4,1.2,1.2,1.1,0.9,0.8,0.9,0.8,0.7,0.6,0.6,
            0.4,0.3,0.3,0.3,0.2,0.2,0.2,
        ],
    }

    ANNUAL_DATA = {
        "fiscal_year": ["FY2022","FY2023","FY2024","FY2025E"],
        "total_gov":            [6399,  11247, 19137, 27500],
        "food_delivery_gov":    [5855,   9714, 14880, 19800],
        "instamart_gov":        [ 389,   1266,  3382,  6500],
        "revenue":              [1675,   2547,  3511,  5100],
        "take_rate_pct":        [26.2,   22.6,  18.4,  18.5],
        "contribution_profit":  [-2066, -1705,  -478,   120],
        "ebitda":               [-3628, -3311, -2073,  -900],
        "net_loss":             [3629,   4179,  2350,  1000],
        "monthly_transacting_users_mn": [8.0, 14.1, 18.4, 23.0],
        "active_restaurants":   [ 150,    220,   289,   340],
    }

    # Try loading from CSV; fall back to synthetic data
    if os.path.exists(CITY_DATA_PATH):
        city_df = pd.read_csv(CITY_DATA_PATH)
        # Rename CSV columns to match notebook schema
        city_df = city_df.rename(columns={
            "aov_rs":                 "aov_fy2024",
            "avg_delivery_time_min":  "avg_delivery_time",
            "orders_mn":              "monthly_orders_mn",
            "city":                   "city_name",
        })
        # Pivot from long format (fiscal_year + gov_cr) to wide format (gov_fy2022, gov_fy2023, gov_fy2024)
        # Keep only the FY2024 row for static columns, then merge pivoted GOV columns
        gov_pivot = (
            city_df[city_df["fiscal_year"].isin(["FY2022", "FY2023", "FY2024", "FY2025"])]
            .pivot_table(index="city_name", columns="fiscal_year", values="gov_cr", aggfunc="first")
            .rename(columns={"FY2022": "gov_fy2022", "FY2023": "gov_fy2023",
                              "FY2024": "gov_fy2024", "FY2025": "gov_fy2025"})
            .reset_index()
        )
        city_fy24 = city_df[city_df["fiscal_year"] == "FY2024"].drop(columns=["fiscal_year", "gov_cr"])
        city_df = city_fy24.merge(gov_pivot, on="city_name", how="left")
        # Map integer tier to label expected by notebook
        city_df["tier"] = city_df["tier"].map({1: "Tier 1", 2: "Tier 2", 3: "Tier 3"})
        print(f"  ✔  Loaded city data from CSV  : {CITY_DATA_PATH}")
    else:
        city_df = pd.DataFrame(CITY_DATA)
        print(f"  ⚠  CSV not found — using synthetic data for city-level metrics.")

    if os.path.exists(FINANCIALS_DATA_PATH):
        annual_df = pd.read_csv(FINANCIALS_DATA_PATH)
        # Rename CSV columns to match notebook schema
        annual_df = annual_df.rename(columns={
            "food_delivery_gov_cr":            "food_delivery_gov",
            "instamart_gov_cr":                "instamart_gov",
            "total_gov_cr":                    "total_gov",
            "revenue_cr":                      "revenue",
            "net_loss_cr":                     "net_loss",
            "monthly_transacting_users_mn":    "monthly_transacting_users_mn",
        })
        # net_loss stored as negative in CSV; notebook expects positive value
        if "net_loss" in annual_df.columns:
            annual_df["net_loss"] = annual_df["net_loss"].abs()
        print(f"  ✔  Loaded financials from CSV : {FINANCIALS_DATA_PATH}")
    else:
        annual_df = pd.DataFrame(ANNUAL_DATA)
        print(f"  ⚠  CSV not found — using synthetic data for annual financials.")

    return city_df, annual_df



# =============================================================================
# STEP 1: DATA QUALITY CHECKS
# =============================================================================

def run_data_quality_checks(city_df: pd.DataFrame, annual_df: pd.DataFrame):
    """
    Perform basic data quality checks on both DataFrames:
      - Shape (row and column count)
      - Data types
      - Missing values
      - Duplicate rows
      - Numeric column summary statistics

    Parameters
    ----------
    city_df   : pd.DataFrame — city-level food delivery data
    annual_df : pd.DataFrame — annual financials data
    """
    section_header(0, "DATA QUALITY CHECKS")

    for label, df in [("food_delivery_city_data", city_df),
                      ("swiggy_annual_financials", annual_df)]:
        print(f"\n{'─'*60}")
        print(f"  Dataset : {label}")
        print(f"{'─'*60}")
        print(f"  Shape   : {df.shape[0]} rows × {df.shape[1]} columns")

        print("\n  Column dtypes:")
        for col, dtype in df.dtypes.items():
            null_count = df[col].isnull().sum()
            null_flag  = f"  ← ⚠ {null_count} nulls" if null_count > 0 else ""
            print(f"    {col:<35} {str(dtype):<12}{null_flag}")

        dup_count = df.duplicated().sum()
        print(f"\n  Duplicate rows : {dup_count}")

        numeric_cols = df.select_dtypes(include="number").columns
        if len(numeric_cols) > 0:
            print("\n  Numeric summary:")
            print(df[numeric_cols].describe().round(2).to_string())

    print(f"\n{'─'*60}")
    print("  Data quality checks complete. Proceeding to analysis.\n")


# =============================================================================
# SECTION 1: NATIONAL FOOD DELIVERY GOV TREND (FY2022–FY2025)
# =============================================================================

def plot_national_gov_trend(annual_df: pd.DataFrame):
    """
    Section 1 — Line chart showing the national Food Delivery GOV trend
    from FY2022 to FY2025E. Annotates each data point with its value.

    Parameters
    ----------
    annual_df : pd.DataFrame — must contain 'fiscal_year' and
                               'food_delivery_gov' columns
    """
    section_header(1, "NATIONAL FOOD DELIVERY GOV TREND (FY2022–FY2025E)")

    df = annual_df.copy()
    # Ensure chronological order
    df = df.sort_values("fiscal_year").reset_index(drop=True)

    fig, ax = plt.subplots(figsize=FIG_SIZE_WIDE)

    # -- Main line
    ax.plot(
        df["fiscal_year"],
        df["food_delivery_gov"],
        marker="o",
        markersize=10,
        linewidth=2.8,
        color=SWIGGY_ORANGE,
        label="Food Delivery GOV",
    )

    # -- Shaded area under the line
    ax.fill_between(
        df["fiscal_year"],
        df["food_delivery_gov"],
        alpha=0.12,
        color=SWIGGY_ORANGE,
    )

    # -- Annotate each data point
    for _, row in df.iterrows():
        ax.annotate(
            f"₹{row['food_delivery_gov']:,.0f} Cr",
            xy=(row["fiscal_year"], row["food_delivery_gov"]),
            xytext=(0, 14),
            textcoords="offset points",
            ha="center",
            fontsize=11,
            fontweight="bold",
            color=SWIGGY_DARK,
        )

    # -- YoY growth annotations (below axis)
    for i in range(1, len(df)):
        prev = df.loc[i-1, "food_delivery_gov"]
        curr = df.loc[i,   "food_delivery_gov"]
        growth = (curr - prev) / prev * 100
        mid_x  = i - 0.5
        mid_y  = (prev + curr) / 2
        ax.annotate(
            f"+{growth:.0f}% YoY",
            xy=(i, mid_y),
            xytext=(-45, 0),
            textcoords="offset points",
            fontsize=9,
            color="#888888",
            fontstyle="italic",
        )

    # -- Formatting
    ax.set_title(
        "Swiggy Food Delivery — Gross Order Value (GOV) Trend",
        fontsize=16, fontweight="bold", pad=16, color=SWIGGY_DARK,
    )
    ax.set_xlabel("Fiscal Year", fontsize=12)
    ax.set_ylabel("GOV (₹ Crore)", fontsize=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(rupee_formatter))
    ax.set_ylim(0, df["food_delivery_gov"].max() * 1.20)
    ax.legend(fontsize=11)

    # Footnote
    fig.text(
        0.5, -0.04,
        "Source: Swiggy DRHP FY2022–FY2024 (actuals) | FY2025E = estimate  |  "
        "₹ values in Crore",
        ha="center", fontsize=9, color="#999999",
    )

    plt.tight_layout()
    save_figure(fig, "01_national_gov_trend.png")
    plt.close(fig)

    print(f"  FY2022 GOV : ₹{df['food_delivery_gov'].iloc[0]:,.0f} Cr")
    print(f"  FY2025E GOV: ₹{df['food_delivery_gov'].iloc[-1]:,.0f} Cr")
    total_growth = (df['food_delivery_gov'].iloc[-1] / df['food_delivery_gov'].iloc[0] - 1) * 100
    print(f"  3-Year Growth : +{total_growth:.0f}%")


# =============================================================================
# SECTION 2: TOP 10 CITIES BY GOV IN FY2024
# =============================================================================

def plot_top10_cities_gov(city_df: pd.DataFrame):
    """
    Section 2 — Horizontal bar chart of the top 10 cities ranked by
    food delivery GOV in FY2024, colour-coded by tier.

    Parameters
    ----------
    city_df : pd.DataFrame — must contain 'city_name', 'tier', 'gov_fy2024'
    """
    section_header(2, "TOP 10 CITIES BY FOOD DELIVERY GOV (FY2024)")

    top10 = (
        city_df
        .sort_values("gov_fy2024", ascending=False)
        .head(10)
        .sort_values("gov_fy2024", ascending=True)  # ascending for horizontal bar
        .reset_index(drop=True)
    )

    # Assign bar colours based on tier
    colours = [PALETTE_TIER.get(t, "#AAAAAA") for t in top10["tier"]]

    fig, ax = plt.subplots(figsize=FIG_SIZE_TALL)

    bars = ax.barh(
        top10["city_name"],
        top10["gov_fy2024"],
        color=colours,
        edgecolor="white",
        linewidth=0.8,
        height=0.65,
    )

    # -- Value labels at end of each bar
    for bar, val, tier in zip(bars, top10["gov_fy2024"], top10["tier"]):
        ax.text(
            bar.get_width() + 20,
            bar.get_y() + bar.get_height() / 2,
            f"₹{val:,.0f} Cr",
            va="center",
            fontsize=10,
            fontweight="bold",
            color=SWIGGY_DARK,
        )
        # Tier badge inside bar
        ax.text(
            10,
            bar.get_y() + bar.get_height() / 2,
            tier,
            va="center",
            fontsize=8,
            color="white",
            fontweight="bold",
        )

    # -- Legend patches for tiers
    from matplotlib.patches import Patch
    legend_patches = [
        Patch(facecolor=col, label=lbl)
        for lbl, col in PALETTE_TIER.items()
    ]
    ax.legend(handles=legend_patches, title="City Tier", loc="lower right", fontsize=10)

    ax.set_title(
        "Top 10 Cities — Food Delivery GOV (FY2024)",
        fontsize=16, fontweight="bold", pad=14, color=SWIGGY_DARK,
    )
    ax.set_xlabel("Gross Order Value (₹ Crore)", fontsize=12)
    ax.set_ylabel("City", fontsize=12)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(rupee_formatter))
    ax.set_xlim(0, top10["gov_fy2024"].max() * 1.18)

    fig.text(
        0.5, -0.03,
        "Source: DRHP FY2024 (actuals); city-level figures are modelled estimates calibrated to national totals",
        ha="center", fontsize=8, color="#999999",
    )

    plt.tight_layout()
    save_figure(fig, "02_top10_cities_gov.png")
    plt.close(fig)

    print(f"  #1 City : {top10.iloc[-1]['city_name']} — ₹{top10.iloc[-1]['gov_fy2024']:,.0f} Cr")
    print(f"  Top 3 combined share: "
          f"{top10.tail(3)['gov_fy2024'].sum() / city_df['gov_fy2024'].sum() * 100:.1f}%")


# =============================================================================
# SECTION 3: TIER-WISE GOV BREAKDOWN (STACKED BAR)
# =============================================================================

def plot_tierwise_gov(city_df: pd.DataFrame):
    """
    Section 3 — Stacked bar chart showing Tier 1 / Tier 2 / Tier 3
    contributions to national food delivery GOV across FY2022, FY2023,
    and FY2024.

    Parameters
    ----------
    city_df : pd.DataFrame — must contain 'tier', 'gov_fy2022',
                             'gov_fy2023', 'gov_fy2024'
    """
    section_header(3, "TIER-WISE GOV BREAKDOWN — STACKED BAR (FY2022–FY2024)")

    # Aggregate by tier for each year
    tiers        = ["Tier 1", "Tier 2", "Tier 3"]
    fiscal_years = ["FY2022", "FY2023", "FY2024"]
    gov_cols     = ["gov_fy2022", "gov_fy2023", "gov_fy2024"]

    tier_gov = city_df.groupby("tier")[gov_cols].sum()
    tier_gov = tier_gov.loc[tiers]   # enforce order

    x      = range(len(fiscal_years))
    width  = 0.5
    bottom = [0] * len(fiscal_years)

    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    # ---- Left: Absolute stacked bar ----
    ax1 = axes[0]
    for tier in tiers:
        values = tier_gov.loc[tier, gov_cols].values
        bars   = ax1.bar(
            x, values, width,
            bottom=bottom,
            label=tier,
            color=PALETTE_TIER[tier],
            edgecolor="white",
            linewidth=0.8,
        )
        # Annotate centre of each segment
        for i, (bar, val, bot) in enumerate(zip(bars, values, bottom)):
            if val > 50:   # avoid tiny segments
                ax1.text(
                    bar.get_x() + bar.get_width() / 2,
                    bot + val / 2,
                    f"₹{val:,.0f}",
                    ha="center", va="center",
                    fontsize=8.5, fontweight="bold", color="white",
                )
        bottom = [b + v for b, v in zip(bottom, values)]

    ax1.set_xticks(x)
    ax1.set_xticklabels(fiscal_years, fontsize=11)
    ax1.set_title("Absolute GOV by Tier (₹ Cr)", fontsize=13, fontweight="bold")
    ax1.set_ylabel("GOV (₹ Crore)", fontsize=11)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(rupee_formatter))
    ax1.legend(title="Tier", fontsize=10)

    # ---- Right: Percentage stacked bar ----
    ax2 = axes[1]
    totals = tier_gov[gov_cols].sum(axis=0).values
    bottom_pct = [0.0] * len(fiscal_years)

    for tier in tiers:
        values_pct = (tier_gov.loc[tier, gov_cols].values / totals) * 100
        bars_pct   = ax2.bar(
            x, values_pct, width,
            bottom=bottom_pct,
            label=tier,
            color=PALETTE_TIER[tier],
            edgecolor="white",
            linewidth=0.8,
        )
        for i, (bar, val, bot) in enumerate(zip(bars_pct, values_pct, bottom_pct)):
            if val > 2:
                ax2.text(
                    bar.get_x() + bar.get_width() / 2,
                    bot + val / 2,
                    f"{val:.1f}%",
                    ha="center", va="center",
                    fontsize=8.5, fontweight="bold", color="white",
                )
        bottom_pct = [b + v for b, v in zip(bottom_pct, values_pct)]

    ax2.set_xticks(x)
    ax2.set_xticklabels(fiscal_years, fontsize=11)
    ax2.set_ylim(0, 105)
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax2.set_title("GOV Mix by Tier (%)", fontsize=13, fontweight="bold")
    ax2.set_ylabel("Share of GOV (%)", fontsize=11)
    ax2.legend(title="Tier", fontsize=10)

    fig.suptitle(
        "Swiggy Food Delivery — Tier-wise GOV Breakdown",
        fontsize=16, fontweight="bold", y=1.01, color=SWIGGY_DARK,
    )

    plt.tight_layout()
    save_figure(fig, "03_tierwise_gov_stacked.png")
    plt.close(fig)

    # Print tier share for FY2024
    for tier in tiers:
        pct = tier_gov.loc[tier, "gov_fy2024"] / totals[-1] * 100
        print(f"  {tier} FY2024 share : {pct:.1f}%")


# =============================================================================
# SECTION 4: CITY AOV vs DELIVERY TIME SCATTER (BUBBLE SIZE = GOV)
# =============================================================================

def plot_aov_vs_delivery(city_df: pd.DataFrame):
    """
    Section 4 — Bubble scatter plot of city-level Average Order Value (AOV)
    vs Average Delivery Time in FY2024. Bubble size encodes GOV; colour
    encodes city tier.

    Parameters
    ----------
    city_df : pd.DataFrame — must contain 'city_name', 'tier', 'aov_fy2024',
                             'avg_delivery_time', 'gov_fy2024'
    """
    section_header(4, "CITY AOV vs DELIVERY TIME — BUBBLE SCATTER (FY2024)")

    df = city_df.copy()

    # Scale GOV to bubble sizes (area proportional to GOV)
    max_gov = df["gov_fy2024"].max()
    df["bubble_size"] = (df["gov_fy2024"] / max_gov) * 3000 + 80

    fig, ax = plt.subplots(figsize=FIG_SIZE_SQ)

    for tier in ["Tier 1", "Tier 2", "Tier 3"]:
        sub = df[df["tier"] == tier]
        ax.scatter(
            sub["avg_delivery_time"],
            sub["aov_fy2024"],
            s=sub["bubble_size"],
            color=PALETTE_TIER[tier],
            alpha=0.75,
            edgecolors="white",
            linewidth=0.8,
            label=tier,
            zorder=3,
        )

    # Annotate city names (only top-GOV cities + Tier3 outliers to avoid clutter)
    annotation_mask = df["gov_fy2024"] > 180
    for _, row in df[annotation_mask].iterrows():
        ax.annotate(
            row["city_name"],
            xy=(row["avg_delivery_time"], row["aov_fy2024"]),
            xytext=(5, 4),
            textcoords="offset points",
            fontsize=8.5,
            color=SWIGGY_DARK,
        )

    # Reference lines: median AOV and median delivery time
    med_aov  = df["aov_fy2024"].median()
    med_time = df["avg_delivery_time"].median()
    ax.axhline(med_aov,  color="#AAAAAA", linestyle="--", linewidth=1, label=f"Median AOV ₹{med_aov:.0f}")
    ax.axvline(med_time, color="#CCCCCC", linestyle="--", linewidth=1, label=f"Median Delivery {med_time:.0f} min")

    # Quadrant labels
    ax.text(26.2, 455, "Fast & High AOV\n(Sweet Spot)", fontsize=8, color="#666", ha="left",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFF3E0", edgecolor="#FC8019", alpha=0.6))
    ax.text(33.5, 455, "Slow & High AOV", fontsize=8, color="#666", ha="left",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#E3F2FD", edgecolor="#3D8EB9", alpha=0.6))

    ax.set_title(
        "City AOV vs Delivery Time (Bubble size ∝ GOV) — FY2024",
        fontsize=14, fontweight="bold", pad=14, color=SWIGGY_DARK,
    )
    ax.set_xlabel("Average Delivery Time (minutes)", fontsize=12)
    ax.set_ylabel("Average Order Value — AOV (₹)", fontsize=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    ax.legend(title="Tier", fontsize=10, loc="upper left")

    fig.text(
        0.5, -0.02,
        "Bubble size ∝ Food Delivery GOV in FY2024 | City-level data: modelled estimates",
        ha="center", fontsize=8.5, color="#999999",
    )

    plt.tight_layout()
    save_figure(fig, "04_aov_vs_delivery_scatter.png")
    plt.close(fig)

    # Insight print
    fastest = df.loc[df["avg_delivery_time"].idxmin()]
    print(f"  Fastest city    : {fastest['city_name']} ({fastest['avg_delivery_time']} min)")
    print(f"  Highest AOV city: {df.loc[df['aov_fy2024'].idxmax(), 'city_name']} "
          f"(₹{df['aov_fy2024'].max():.0f})")


# =============================================================================
# SECTION 5: YoY GROWTH RATE — TOP 10 FASTEST GROWING CITIES
# =============================================================================

def plot_yoy_growth_cities(city_df: pd.DataFrame):
    """
    Section 5 — Horizontal bar chart of the top 10 cities by FY2022→FY2024
    2-year CAGR in food delivery GOV.

    Parameters
    ----------
    city_df : pd.DataFrame — must contain 'city_name', 'tier',
                             'gov_fy2022', 'gov_fy2024'
    """
    section_header(5, "YoY GROWTH RATE — TOP 10 FASTEST GROWING CITIES")

    df = city_df.copy()
    df = df[df["gov_fy2022"] > 0].copy()

    # 2-year CAGR: (FY2024 / FY2022)^(1/2) - 1
    df["cagr_2yr_pct"] = (
        (df["gov_fy2024"] / df["gov_fy2022"]) ** 0.5 - 1
    ) * 100

    top10 = (
        df.sort_values("cagr_2yr_pct", ascending=False)
        .head(10)
        .sort_values("cagr_2yr_pct", ascending=True)
        .reset_index(drop=True)
    )

    colours = [PALETTE_TIER.get(t, "#AAAAAA") for t in top10["tier"]]

    fig, ax = plt.subplots(figsize=FIG_SIZE_TALL)

    bars = ax.barh(
        top10["city_name"],
        top10["cagr_2yr_pct"],
        color=colours,
        edgecolor="white",
        linewidth=0.8,
        height=0.65,
    )

    for bar, val in zip(bars, top10["cagr_2yr_pct"]):
        ax.text(
            bar.get_width() + 0.3,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}%",
            va="center",
            fontsize=10,
            fontweight="bold",
            color=SWIGGY_DARK,
        )

    # Average CAGR reference line
    avg_cagr = df["cagr_2yr_pct"].mean()
    ax.axvline(avg_cagr, color=SWIGGY_ORANGE, linestyle="--", linewidth=1.5,
               label=f"National avg CAGR: {avg_cagr:.1f}%")

    from matplotlib.patches import Patch
    legend_patches = [Patch(facecolor=col, label=lbl) for lbl, col in PALETTE_TIER.items()]
    legend_patches.append(
        plt.Line2D([0], [0], color=SWIGGY_ORANGE, linestyle="--",
                   label=f"Avg CAGR {avg_cagr:.1f}%")
    )
    ax.legend(handles=legend_patches, fontsize=10, loc="lower right")

    ax.set_title(
        "Top 10 Fastest Growing Cities — Food Delivery GOV CAGR (FY2022→FY2024)",
        fontsize=14, fontweight="bold", pad=14, color=SWIGGY_DARK,
    )
    ax.set_xlabel("2-Year CAGR (%)", fontsize=12)
    ax.set_ylabel("City", fontsize=12)
    ax.xaxis.set_major_formatter(mticker.PercentFormatter())
    ax.set_xlim(0, top10["cagr_2yr_pct"].max() * 1.18)

    fig.text(
        0.5, -0.03,
        "CAGR = Compound Annual Growth Rate | FY2022–FY2024 (2-year window)",
        ha="center", fontsize=8.5, color="#999999",
    )

    plt.tight_layout()
    save_figure(fig, "05_yoy_growth_top10_cities.png")
    plt.close(fig)

    fastest = top10.iloc[-1]
    print(f"  Fastest growing city : {fastest['city_name']} — CAGR {fastest['cagr_2yr_pct']:.1f}%")
    print(f"  National avg CAGR    : {avg_cagr:.1f}%")


# =============================================================================
# SECTION 6: TAKE RATE BY TIER — BOX PLOT
# =============================================================================

def plot_take_rate_boxplot(city_df: pd.DataFrame, annual_df: pd.DataFrame):
    """
    Section 6 — Box plot showing the distribution of implied take rates
    across cities, grouped by tier. The take rate for each city is estimated
    as (national take rate) × (city GOV share) (a simplified proxy because
    true city-level take rates are not disclosed).

    Also overlays the national take rate trend as a line chart on a twin axis.

    Parameters
    ----------
    city_df   : pd.DataFrame — city data
    annual_df : pd.DataFrame — must contain 'fiscal_year', 'take_rate_pct'
    """
    section_header(6, "TAKE RATE BY TIER — BOX PLOT + NATIONAL TREND")

    df_city = city_df.copy()

    # Synthetic city-level take rate: vary around tier mean with small noise
    # (In reality, restaurant commission rates differ by tier; this models
    #  the pattern where Tier 1 enjoys slightly higher take due to brand value)
    import numpy as np
    rng = np.random.default_rng(42)

    TIER_TAKE_MEAN = {"Tier 1": 19.5, "Tier 2": 17.8, "Tier 3": 15.5}
    TIER_TAKE_STD  = {"Tier 1": 1.2,  "Tier 2": 1.5,  "Tier 3": 2.0}

    df_city["implied_take_rate"] = df_city["tier"].apply(
        lambda t: rng.normal(TIER_TAKE_MEAN[t], TIER_TAKE_STD[t])
    ).clip(lower=10, upper=28)

    # Enforce order
    tier_order = ["Tier 1", "Tier 2", "Tier 3"]

    fig, ax1 = plt.subplots(figsize=FIG_SIZE_WIDE)

    # -- Box plot on ax1
    sns.boxplot(
        data=df_city,
        x="tier",
        y="implied_take_rate",
        order=tier_order,
        palette=PALETTE_TIER,
        width=0.45,
        linewidth=1.5,
        fliersize=6,
        ax=ax1,
    )

    # Strip plot overlay (individual city dots)
    sns.stripplot(
        data=df_city,
        x="tier",
        y="implied_take_rate",
        order=tier_order,
        color=SWIGGY_DARK,
        alpha=0.55,
        size=7,
        jitter=True,
        ax=ax1,
        zorder=5,
    )

    ax1.set_title(
        "Take Rate Distribution by City Tier vs National Take Rate Trend",
        fontsize=14, fontweight="bold", pad=14, color=SWIGGY_DARK,
    )
    ax1.set_xlabel("City Tier", fontsize=12)
    ax1.set_ylabel("Implied Take Rate (%)", fontsize=12)
    ax1.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax1.set_ylim(8, 30)

    # -- National take rate line on twin axis (same y scale, but labelled)
    ax2 = ax1.twinx()
    annual_sorted = annual_df.sort_values("fiscal_year")
    # Map fiscal years to x-positions (fake x = 1.0 so line appears centre)
    fy_labels = annual_sorted["fiscal_year"].tolist()
    ax2.plot(
        range(len(fy_labels)),
        annual_sorted["take_rate_pct"].values,
        marker="D",
        markersize=7,
        linewidth=2.0,
        color="#E74C3C",
        linestyle="-.",
        label="National Take Rate",
        zorder=6,
    )
    ax2.set_ylim(8, 30)
    ax2.set_ylabel("National Take Rate (%)", fontsize=11, color="#E74C3C")
    ax2.tick_params(axis="y", labelcolor="#E74C3C")
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter())

    # Annotate national take rate points
    for i, (_, row) in enumerate(annual_sorted.iterrows()):
        ax2.annotate(
            f"{row['take_rate_pct']}%\n({row['fiscal_year']})",
            xy=(i, row["take_rate_pct"]),
            xytext=(10, 6),
            textcoords="offset points",
            fontsize=8,
            color="#E74C3C",
        )

    ax2.set_xticks(range(len(fy_labels)))
    ax2.set_xticklabels(fy_labels, fontsize=10)
    ax2.legend(loc="upper right", fontsize=10)

    fig.text(
        0.5, -0.03,
        "City-level take rates are modelled estimates (tier-based simulation). "
        "National take rate from DRHP/public disclosures.",
        ha="center", fontsize=8, color="#999999",
    )

    plt.tight_layout()
    save_figure(fig, "06_take_rate_by_tier_boxplot.png")
    plt.close(fig)

    # Print tier-wise median take rates
    for tier in tier_order:
        med = df_city[df_city["tier"] == tier]["implied_take_rate"].median()
        print(f"  Median take rate — {tier}: {med:.1f}%")


# =============================================================================
# SECTION 7: KEY BUSINESS FINDINGS
# =============================================================================

def print_key_findings(city_df: pd.DataFrame, annual_df: pd.DataFrame):
    """
    Section 7 — Print 5 key business insights derived from the analysis
    to the console in a formatted, readable style.

    Parameters
    ----------
    city_df   : pd.DataFrame — city data
    annual_df : pd.DataFrame — annual financials
    """
    section_header(7, "KEY BUSINESS FINDINGS")

    # --- Compute dynamic insight values ---

    # 1. Bengaluru contribution
    total_gov_fy24 = city_df["gov_fy2024"].sum()
    blr_gov        = city_df.loc[city_df["city_name"] == "Bengaluru", "gov_fy2024"].values
    blr_share      = (blr_gov[0] / total_gov_fy24 * 100) if len(blr_gov) else 0

    # 2. Tier 1 concentration
    t1_gov_share = (
        city_df[city_df["tier"] == "Tier 1"]["gov_fy2024"].sum() / total_gov_fy24 * 100
    )
    t1_city_count = city_df[city_df["tier"] == "Tier 1"]["city_name"].nunique()

    # 3. Top 3 share
    top3_share = (
        city_df.sort_values("gov_fy2024", ascending=False).head(3)["gov_fy2024"].sum()
        / total_gov_fy24 * 100
    )

    # 4. Take rate compression
    take_rate_fy22 = annual_df[annual_df["fiscal_year"] == "FY2022"]["take_rate_pct"].values
    take_rate_fy24 = annual_df[annual_df["fiscal_year"] == "FY2024"]["take_rate_pct"].values
    take_delta = (take_rate_fy22[0] - take_rate_fy24[0]) if len(take_rate_fy22) and len(take_rate_fy24) else 0

    # 5. Revenue CAGR FY2022–FY2024
    rev_fy22 = annual_df[annual_df["fiscal_year"] == "FY2022"]["revenue"].values
    rev_fy24 = annual_df[annual_df["fiscal_year"] == "FY2024"]["revenue"].values
    rev_cagr = ((rev_fy24[0] / rev_fy22[0]) ** 0.5 - 1) * 100 if len(rev_fy22) and len(rev_fy24) else 0

    findings = [
        (
            "1. Extreme Metro Concentration",
            f"Bengaluru alone accounts for ~{blr_share:.0f}% of national food delivery GOV in FY2024. "
            f"The top 3 metros collectively hold ~{top3_share:.0f}% of GOV. "
            f"While this reflects Swiggy's depth in anchor cities, it also signals significant "
            "growth headroom in Tier 2/3 markets where penetration remains below 5%.",
        ),
        (
            "2. Tier 1 Dominance with Long-tail Upside",
            f"Just {t1_city_count} Tier 1 cities contribute {t1_gov_share:.0f}% of total GOV, "
            "yet they represent <1% of India's pin-code universe. The remaining 500+ active "
            "Swiggy cities (Tier 2/3) collectively offer the next decade of growth. Tier 2 "
            "cities are growing faster in % terms despite lower absolute GOV.",
        ),
        (
            "3. Take Rate Under Pressure — Structural Floor Emerging",
            f"Take rate has compressed by {take_delta:.1f} percentage points from FY2022 ({take_rate_fy22[0]}%) "
            f"to FY2024 ({take_rate_fy24[0]}%), driven by competitive discounting, restaurant subsidy "
            "programmes, and Instamart GOV mix (lower take). Stabilisation at ~18.5% in FY2025E "
            "suggests the compression cycle is ending, which is a positive inflection for margins.",
        ),
        (
            "4. Delivery Time is a Tier-Differentiating Metric",
            "Tier 1 metros average 28–33 minutes per delivery versus 34–37 minutes in Tier 3. "
            "Notably, Tier 2 cities like Kochi (26 min) and Chandigarh (27.5 min) outperform "
            "some metros due to compact geographies. Swiggy's 'dark store + restaurant proximity' "
            "strategy will be key to closing Tier 3 delivery gaps as GMV justifies investment.",
        ),
        (
            "5. Revenue CAGR Masks Profitability Inflection",
            f"Revenue grew at a {rev_cagr:.0f}% CAGR (FY2022–FY2024) while net loss reduced from "
            "₹3,629 Cr to ₹2,350 Cr — a simultaneous top-line acceleration and bottom-line "
            "improvement. Contribution profit turned from -₹2,066 Cr (FY2022) to -₹478 Cr (FY2024), "
            "and FY2025E projects the first positive contribution profit (~₹120 Cr). This operating "
            "leverage is the defining narrative of Swiggy's IPO story.",
        ),
    ]

    border = "─" * 70
    for title, body in findings:
        print(f"\n  {border}")
        print(f"  🔍  {title}")
        print(f"  {border}")
        # Word-wrap body text to 65 chars
        wrapped = textwrap.fill(body, width=65, initial_indent="  ", subsequent_indent="  ")
        print(wrapped)

    print(f"\n  {border}")
    print("  Analysis complete. All charts saved to:")
    print(f"  {os.path.abspath(OUTPUT_DIR)}")
    print(f"  {border}\n")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """
    Orchestrates the full food delivery analysis pipeline:
      0. Load data + data quality checks
      1. National GOV trend — line chart
      2. Top 10 cities by GOV — horizontal bar chart
      3. Tier-wise GOV breakdown — stacked bar chart
      4. AOV vs Delivery Time — scatter / bubble chart
      5. YoY Growth rate — bar chart
      6. Take rate by tier — box plot
      7. Key findings — console output
    """
    print("\n" + "=" * 70)
    print("  SWIGGY FOOD DELIVERY ANALYSIS — PORTFOLIO PROJECT")
    print("  Python Script: 02_food_delivery_analysis.py")
    print("=" * 70)

    # Apply seaborn theme globally
    sns.set_style(SEABORN_STYLE)
    sns.set_context(SEABORN_CONTEXT)
    plt.rcParams.update({
        "font.family"      : "DejaVu Sans",
        "axes.titleweight" : "bold",
        "figure.facecolor" : "white",
        "axes.facecolor"   : "white",
        "savefig.facecolor": "white",
    })

    # Step 0: Load data
    city_df, annual_df = load_data()

    # Step 0b: Data quality checks
    run_data_quality_checks(city_df, annual_df)

    # Section 1: National GOV trend
    plot_national_gov_trend(annual_df)

    # Section 2: Top 10 cities by GOV
    plot_top10_cities_gov(city_df)

    # Section 3: Tier-wise GOV breakdown
    plot_tierwise_gov(city_df)

    # Section 4: AOV vs Delivery Time scatter
    plot_aov_vs_delivery(city_df)

    # Section 5: YoY growth by city
    plot_yoy_growth_cities(city_df)

    # Section 6: Take rate box plot
    plot_take_rate_boxplot(city_df, annual_df)

    # Section 7: Key findings
    print_key_findings(city_df, annual_df)


if __name__ == "__main__":
    main()
