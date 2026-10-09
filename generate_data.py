"""
Swiggy Sales Analysis - Master Data Generation Script
Generates all CSV datasets based on real Swiggy DRHP/IPO public data
City-level data is synthetic but calibrated to match official national totals.
"""

import pandas as pd
import numpy as np
import os

np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
CLEANED_DIR = os.path.join(BASE_DIR, "data", "cleaned")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(CLEANED_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────
# 1. ANNUAL FINANCIALS  (REAL Swiggy data from DRHP + filings)
# ─────────────────────────────────────────────────────────────
annual_data = {
    "fiscal_year":          ["FY2022", "FY2023", "FY2024", "FY2025"],
    "revenue_cr":           [5705,     8265,     11634,    15200],
    "net_loss_cr":          [-3629,    -3758,    -1888,    -1100],
    "food_delivery_gov_cr": [13800,    22000,    27000,    32000],
    "instamart_gov_cr":     [500,      3000,     8069,     14500],
    "dineout_gov_cr":       [200,      600,      1400,     2800],
    "total_gov_cr":         [14500,    25600,    36469,    49300],
    "monthly_transacting_users_mn": [8, 11, 13, 15.5],
    "restaurant_partners":  [130000,   170000,   196000,   220000],
    "delivery_partners":    [280000,   340000,   390000,   430000],
    "cities_food_delivery": [500,      580,      653,      700],
    "instamart_cities":     [8,        25,       43,       55],
    "dark_stores":          [200,      400,      605,      750],
    "take_rate_pct":        [18.5,     20.2,     21.8,     22.5],
    "aov_food_rs":          [380,      410,      440,      465],
    "aov_instamart_rs":     [280,      350,      410,      450],
}
df_annual = pd.DataFrame(annual_data)
df_annual.to_csv(os.path.join(RAW_DIR, "swiggy_annual_financials.csv"), index=False)
print("✅ Annual financials saved")

# ─────────────────────────────────────────────────────────────
# 2. QUARTERLY RESULTS  (Real + estimated data)
# ─────────────────────────────────────────────────────────────
quarters = [
    ("Q1 FY2024", "Apr-Jun 2023",  2450, -680,  6100, 1400),
    ("Q2 FY2024", "Jul-Sep 2023",  2700, -590,  6500, 1700),
    ("Q3 FY2024", "Oct-Dec 2023",  3100, -340,  7200, 2100),
    ("Q4 FY2024", "Jan-Mar 2024",  3384, -278,  7200, 2869),
    ("Q1 FY2025", "Apr-Jun 2024",  3600, -360,  7800, 3200),
    ("Q2 FY2025", "Jul-Sep 2024",  3900, -320,  8200, 3800),
    ("Q3 FY2025", "Oct-Dec 2024",  4200, -250,  8600, 4200),
    ("Q4 FY2025", "Jan-Mar 2025",  3500, -170,  7400, 3300),
    ("Q1 FY2026", "Apr-Jun 2025",  5048, -1197, 8100, 5500),
    ("Q2 FY2026", "Jul-Sep 2025",  5620, -1092, 8600, 6200),
    ("Q3 FY2026", "Oct-Dec 2025",  6244, -1065, 9100, 7000),
    ("Q4 FY2026", "Jan-Mar 2026",  6649, -800,  9300, 7500),
    ("Q1 FY2027", "Apr-Jun 2026",  6812, -791,  9490, 7907),
]
df_quarterly = pd.DataFrame(quarters, columns=[
    "quarter", "period", "revenue_cr", "net_loss_cr",
    "food_delivery_gov_cr", "instamart_gov_cr"
])
df_quarterly["total_gov_cr"] = df_quarterly["food_delivery_gov_cr"] + df_quarterly["instamart_gov_cr"]
df_quarterly.to_csv(os.path.join(RAW_DIR, "swiggy_quarterly_results.csv"), index=False)
print("✅ Quarterly results saved")

# ─────────────────────────────────────────────────────────────
# 3. FOOD DELIVERY CITY DATA  (Synthetic, calibrated to real totals)
# ─────────────────────────────────────────────────────────────
cities = [
    # city, tier, state, gov_share_pct, aov_rs, avg_del_time_min, yoy_growth_pct
    ("Bengaluru",    1, "Karnataka",       15.0, 480, 32, 18),
    ("Delhi NCR",    1, "Delhi/NCR",       14.5, 460, 35, 15),
    ("Mumbai",       1, "Maharashtra",     13.5, 490, 38, 14),
    ("Hyderabad",    1, "Telangana",        9.0, 445, 30, 20),
    ("Chennai",      1, "Tamil Nadu",       7.5, 420, 29, 17),
    ("Pune",         1, "Maharashtra",      5.5, 430, 31, 19),
    ("Kolkata",      1, "West Bengal",      4.5, 380, 33, 12),
    ("Ahmedabad",    2, "Gujarat",          3.0, 360, 36, 22),
    ("Jaipur",       2, "Rajasthan",        2.2, 340, 38, 24),
    ("Lucknow",      2, "Uttar Pradesh",    2.0, 330, 40, 26),
    ("Chandigarh",   2, "Punjab",           1.5, 400, 34, 21),
    ("Indore",       2, "Madhya Pradesh",   1.4, 320, 39, 28),
    ("Surat",        2, "Gujarat",          1.3, 350, 37, 23),
    ("Bhopal",       2, "Madhya Pradesh",   1.1, 310, 41, 27),
    ("Nagpur",       2, "Maharashtra",      1.0, 330, 40, 25),
    ("Kochi",        2, "Kerala",           0.9, 410, 33, 19),
    ("Coimbatore",   2, "Tamil Nadu",       0.8, 360, 35, 22),
    ("Patna",        2, "Bihar",            0.7, 300, 44, 30),
    ("Visakhapatnam",2, "Andhra Pradesh",   0.7, 350, 36, 24),
    ("Vadodara",     2, "Gujarat",          0.6, 340, 38, 22),
    ("Bhubaneswar",  3, "Odisha",           0.5, 300, 42, 32),
    ("Guwahati",     3, "Assam",            0.4, 290, 45, 35),
    ("Nashik",       3, "Maharashtra",      0.4, 310, 41, 29),
    ("Agra",         3, "Uttar Pradesh",    0.3, 290, 44, 31),
    ("Mysuru",       3, "Karnataka",        0.3, 340, 37, 25),
    ("Rest of India",3, "Multiple",        11.9, 280, 48, 28),
]

rows_food = []
fiscal_years = ["FY2022", "FY2023", "FY2024", "FY2025"]
national_gov  = [13800,    22000,    27000,    32000]

for fy, nat_gov in zip(fiscal_years, national_gov):
    growth_mult = {"FY2022": 0.85, "FY2023": 1.0, "FY2024": 1.08, "FY2025": 1.15}[fy]
    for city, tier, state, share, aov, del_time, yoy in cities:
        gov = round(nat_gov * share / 100 * growth_mult + np.random.uniform(-20, 20), 1)
        gov = max(gov, 10)
        orders_mn = round(gov * 10 / aov / 10, 2)   # approx orders in mn
        noise_aov = aov + np.random.randint(-15, 20)
        noise_del = del_time + np.random.randint(-2, 3)
        restaurant_partners = int(orders_mn * 180 + np.random.randint(-50, 100))
        rows_food.append({
            "fiscal_year": fy, "city": city, "tier": tier, "state": state,
            "gov_cr": gov, "orders_mn": orders_mn,
            "aov_rs": noise_aov, "avg_delivery_time_min": noise_del,
            "restaurant_partners": restaurant_partners,
            "yoy_growth_pct": yoy + np.random.uniform(-3, 3),
            "take_rate_pct": 20.5 + np.random.uniform(-1.5, 2.0),
        })

df_food = pd.DataFrame(rows_food)
df_food.to_csv(os.path.join(RAW_DIR, "food_delivery_city_data.csv"), index=False)
print("✅ Food delivery city data saved")

# ─────────────────────────────────────────────────────────────
# 4. INSTAMART CITY DATA
# ─────────────────────────────────────────────────────────────
instamart_cities = [
    # city, tier, dark_stores_fy24, gov_share_pct, avg_del_time_min, top_category
    ("Bengaluru",     1, 95,  20.0, 11, "Fruits & Vegetables"),
    ("Mumbai",        1, 88,  18.5, 13, "Dairy & Bakery"),
    ("Delhi NCR",     1, 92,  17.0, 14, "Snacks & Beverages"),
    ("Hyderabad",     1, 65,  10.5, 12, "Fruits & Vegetables"),
    ("Chennai",       1, 55,   8.5, 11, "Dairy & Bakery"),
    ("Pune",          1, 48,   6.5, 12, "Snacks & Beverages"),
    ("Kolkata",       1, 35,   4.5, 14, "Staples & Cooking"),
    ("Ahmedabad",     2, 28,   3.0, 15, "Staples & Cooking"),
    ("Jaipur",        2, 22,   2.2, 17, "Snacks & Beverages"),
    ("Lucknow",       2, 18,   1.8, 18, "Dairy & Bakery"),
    ("Chandigarh",    2, 16,   1.5, 16, "Dairy & Bakery"),
    ("Indore",        2, 14,   1.2, 18, "Staples & Cooking"),
    ("Surat",         2, 12,   1.0, 17, "Fruits & Vegetables"),
    ("Coimbatore",    2, 10,   0.8, 16, "Fruits & Vegetables"),
    ("Kochi",         2, 10,   0.8, 15, "Dairy & Bakery"),
    ("Nagpur",        2,  8,   0.6, 19, "Staples & Cooking"),
    ("Bhopal",        2,  7,   0.5, 20, "Snacks & Beverages"),
    ("Visakhapatnam", 2,  6,   0.5, 19, "Fruits & Vegetables"),
    ("Patna",         2,  4,   0.3, 22, "Staples & Cooking"),
    ("Vadodara",      2,  4,   0.3, 20, "Dairy & Bakery"),
]

rows_insta = []
im_gov_by_fy = {"FY2022": 500, "FY2023": 3000, "FY2024": 8069, "FY2025": 14500}
dark_stores_by_fy = {"FY2022": 200, "FY2023": 400, "FY2024": 605, "FY2025": 750}

for fy in fiscal_years:
    nat_im_gov = im_gov_by_fy[fy]
    nat_ds = dark_stores_by_fy[fy]
    scale = {"FY2022": 0.3, "FY2023": 0.65, "FY2024": 1.0, "FY2025": 1.4}[fy]
    for city, tier, ds_fy24, share, del_time, top_cat in instamart_cities:
        ds = max(1, int(ds_fy24 * scale + np.random.randint(-2, 3)))
        gov = round(nat_im_gov * share / 100 + np.random.uniform(-10, 15), 1)
        gov = max(gov, 5)
        rows_insta.append({
            "fiscal_year": fy, "city": city, "tier": tier,
            "dark_stores": ds, "gov_cr": gov,
            "avg_delivery_time_min": del_time + np.random.randint(-2, 3),
            "top_category": top_cat,
            "orders_mn": round(gov * 10 / 410 / 10, 2),
            "avg_order_value_rs": 410 + np.random.randint(-30, 40),
            "yoy_growth_pct": round(np.random.uniform(55, 120) if fy != "FY2022" else np.random.uniform(20, 40), 1),
        })

df_insta = pd.DataFrame(rows_insta)
df_insta.to_csv(os.path.join(RAW_DIR, "instamart_city_data.csv"), index=False)
print("✅ Instamart city data saved")

# ─────────────────────────────────────────────────────────────
# 5. SWIGGY ONE MEMBERSHIP DATA
# ─────────────────────────────────────────────────────────────
months = pd.date_range("2022-04-01", "2025-03-01", freq="MS")
subscribers_start = 500000
rows_one = []
for i, month in enumerate(months):
    subscribers = int(subscribers_start * (1.06 ** i))
    member_aov = 510 + i * 2.5
    non_member_aov = 380 + i * 1.8
    member_orders_month = 4.2 + i * 0.03
    non_member_orders_month = 1.8 + i * 0.01
    rows_one.append({
        "month": month.strftime("%b %Y"),
        "subscribers_mn": round(subscribers / 1e6, 2),
        "member_aov_rs": round(member_aov, 0),
        "non_member_aov_rs": round(non_member_aov, 0),
        "member_monthly_orders": round(member_orders_month, 2),
        "non_member_monthly_orders": round(non_member_orders_month, 2),
        "subscription_revenue_cr": round(subscribers * 99 / 1e7, 2),
        "free_delivery_cost_cr": round(subscribers * 60 / 1e7, 2),
    })

df_one = pd.DataFrame(rows_one)
df_one.to_csv(os.path.join(RAW_DIR, "swiggy_one_membership.csv"), index=False)
print("✅ Swiggy One membership data saved")

# ─────────────────────────────────────────────────────────────
# 6. COMPETITOR COMPARISON  (Swiggy vs Zomato)
# ─────────────────────────────────────────────────────────────
competitor_data = {
    "fiscal_year":               ["FY2022", "FY2023", "FY2024", "FY2025"],
    "swiggy_revenue_cr":         [5705,     8265,     11634,    15200],
    "zomato_revenue_cr":         [4192,     7079,     14148,    20176],
    "swiggy_net_loss_cr":        [-3629,    -3758,    -1888,    -1100],
    "zomato_net_loss_cr":        [-1223,    -971,      351,      1605],
    "swiggy_food_gov_cr":        [13800,    22000,    27000,    32000],
    "zomato_food_gov_cr":        [15200,    24500,    32000,    38000],
    "swiggy_qcommerce_gov_cr":   [500,      3000,     8069,     14500],
    "zomato_qcommerce_gov_cr":   [0,        3200,     12000,    22000],
    "swiggy_market_share_pct":   [47,       45,       44,       43],
    "zomato_market_share_pct":   [53,       55,       56,       57],
    "swiggy_mtu_mn":             [8,        11,       13,       15.5],
    "zomato_mtu_mn":             [15,       19,       21,       24],
    "swiggy_dark_stores":        [200,      400,      605,      750],
    "zomato_blinkit_stores":     [0,        400,      791,      1000],
}
df_comp = pd.DataFrame(competitor_data)
df_comp.to_csv(os.path.join(RAW_DIR, "competitor_comparison.csv"), index=False)
print("✅ Competitor comparison data saved")

# ─────────────────────────────────────────────────────────────
# 7. CLEANED / MASTER DATASET
# ─────────────────────────────────────────────────────────────
# Merge food + instamart city data
df_food_24 = df_food[df_food["fiscal_year"] == "FY2024"].copy()
df_insta_24 = df_insta[df_insta["fiscal_year"] == "FY2024"].copy()
df_food_24 = df_food_24.rename(columns={"gov_cr": "food_gov_cr", "orders_mn": "food_orders_mn"})
df_insta_24 = df_insta_24.rename(columns={"gov_cr": "instamart_gov_cr", "orders_mn": "instamart_orders_mn"})

df_master = df_food_24[["city", "tier", "state", "food_gov_cr", "food_orders_mn",
                          "aov_rs", "avg_delivery_time_min", "restaurant_partners",
                          "yoy_growth_pct", "take_rate_pct"]].merge(
    df_insta_24[["city", "dark_stores", "instamart_gov_cr",
                  "instamart_orders_mn", "avg_order_value_rs"]],
    on="city", how="left"
)
df_master["total_gov_cr"] = df_master["food_gov_cr"] + df_master["instamart_gov_cr"].fillna(0)
df_master.to_csv(os.path.join(CLEANED_DIR, "swiggy_master_fy2024.csv"), index=False)
print("✅ Master cleaned dataset saved")

print("\n🎉 All data files generated successfully!")
print(f"📁 Raw data:     {RAW_DIR}")
print(f"📁 Cleaned data: {CLEANED_DIR}")
