"""
Swiggy Sales Analysis - Power BI Ready Excel Export
Creates a multi-sheet Excel file optimized for Power BI / Tableau import.
Run AFTER generate_data.py
"""

import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR  = os.path.join(BASE_DIR, "data", "raw")
CLEAN_DIR= os.path.join(BASE_DIR, "data", "cleaned")
PBI_DIR  = os.path.join(BASE_DIR, "powerbi_data")
os.makedirs(PBI_DIR, exist_ok=True)

out_path = os.path.join(PBI_DIR, "swiggy_powerbi_ready.xlsx")

df_annual  = pd.read_csv(os.path.join(RAW_DIR, "swiggy_annual_financials.csv"))
df_qtr     = pd.read_csv(os.path.join(RAW_DIR, "swiggy_quarterly_results.csv"))
df_food    = pd.read_csv(os.path.join(RAW_DIR, "food_delivery_city_data.csv"))
df_insta   = pd.read_csv(os.path.join(RAW_DIR, "instamart_city_data.csv"))
df_one     = pd.read_csv(os.path.join(RAW_DIR, "swiggy_one_membership.csv"))
df_comp    = pd.read_csv(os.path.join(RAW_DIR, "competitor_comparison.csv"))
df_master  = pd.read_csv(os.path.join(CLEAN_DIR, "swiggy_master_fy2024.csv"))

with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
    df_annual.to_excel(writer,  sheet_name="Annual_Financials",     index=False)
    df_qtr.to_excel(writer,     sheet_name="Quarterly_Results",      index=False)
    df_food.to_excel(writer,    sheet_name="FoodDelivery_Cities",    index=False)
    df_insta.to_excel(writer,   sheet_name="Instamart_Cities",       index=False)
    df_one.to_excel(writer,     sheet_name="SwiggyOne_Membership",   index=False)
    df_comp.to_excel(writer,    sheet_name="Competitor_Comparison",  index=False)
    df_master.to_excel(writer,  sheet_name="Master_FY2024",          index=False)

    # ── Data Dictionary sheet ──
    data_dict = pd.DataFrame([
        ("Annual_Financials",    "fiscal_year",                  "string", "Fiscal year e.g. FY2024"),
        ("Annual_Financials",    "revenue_cr",                   "float",  "Total operating revenue in ₹ Crores"),
        ("Annual_Financials",    "net_loss_cr",                  "float",  "Net profit/loss in ₹ Crores (negative=loss)"),
        ("Annual_Financials",    "food_delivery_gov_cr",         "float",  "Gross Order Value of food delivery segment"),
        ("Annual_Financials",    "instamart_gov_cr",             "float",  "Gross Order Value of Instamart segment"),
        ("Annual_Financials",    "total_gov_cr",                 "float",  "Total GOV across all segments"),
        ("Annual_Financials",    "monthly_transacting_users_mn", "float",  "Average monthly transacting users in Millions"),
        ("Annual_Financials",    "dark_stores",                  "int",    "Number of active Instamart dark stores"),
        ("Annual_Financials",    "take_rate_pct",                "float",  "Commission/take rate percentage"),
        ("Quarterly_Results",    "quarter",                      "string", "Quarter identifier e.g. Q1 FY2024"),
        ("Quarterly_Results",    "revenue_cr",                   "float",  "Quarterly revenue in ₹ Crores"),
        ("FoodDelivery_Cities",  "city",                         "string", "City name"),
        ("FoodDelivery_Cities",  "tier",                         "int",    "City tier (1=Metro, 2=Tier 2, 3=Tier 3)"),
        ("FoodDelivery_Cities",  "gov_cr",                       "float",  "Gross Order Value for that city-year"),
        ("FoodDelivery_Cities",  "aov_rs",                       "float",  "Average Order Value in ₹"),
        ("FoodDelivery_Cities",  "avg_delivery_time_min",        "float",  "Average food delivery time in minutes"),
        ("Instamart_Cities",     "dark_stores",                  "int",    "Number of Instamart dark stores in city"),
        ("Instamart_Cities",     "top_category",                 "string", "Most ordered category in Instamart"),
        ("SwiggyOne_Membership", "subscribers_mn",               "float",  "Swiggy One subscribers in Millions"),
        ("SwiggyOne_Membership", "member_aov_rs",                "float",  "Avg order value for Swiggy One members"),
        ("Competitor_Comparison","swiggy_market_share_pct",      "float",  "Swiggy food delivery market share %"),
        ("Competitor_Comparison","zomato_blinkit_stores",        "int",    "Zomato's Blinkit dark store count"),
    ], columns=["sheet", "column", "dtype", "description"])
    data_dict.to_excel(writer, sheet_name="Data_Dictionary", index=False)

print(f"✅ Power BI Excel file saved → {out_path}")
print(f"   Sheets: Annual_Financials | Quarterly_Results | FoodDelivery_Cities")
print(f"           Instamart_Cities | SwiggyOne_Membership | Competitor_Comparison")
print(f"           Master_FY2024 | Data_Dictionary")
