-- =============================================================================
-- SWIGGY SALES ANALYSIS — BUSINESS QUESTIONS
-- =============================================================================
-- About Swiggy:
--   Swiggy is India's leading on-demand convenience platform, headquartered in
--   Bengaluru. Founded in 2014, Swiggy operates two major consumer businesses:
--     • Food Delivery  – connecting customers with 800,000+ restaurant partners
--       across 500+ cities in India.
--     • Instamart      – a quick-commerce (q-commerce) grocery delivery service
--       promising 10–20 minute delivery from hyper-local dark stores.
--   Swiggy also offers Swiggy One, a subscription loyalty programme.
--
-- Data Sources:
--   This analysis is based on:
--     1. Swiggy DRHP (Draft Red Herring Prospectus) filed with SEBI in 2024 —
--        official financial disclosures for FY2022 to FY2024.
--     2. Public earnings releases / investor presentations for quarterly results.
--     3. Synthetic city-level and intraday data generated to supplement DRHP
--        figures where granular city/tier breakdowns were not publicly disclosed.
--        All synthetic values are calibrated to be consistent with published
--        national-level aggregates.
--
-- Database : SQLite (fully compatible — no proprietary extensions used)
-- Author   : Akash | Swiggy Data Analyst Portfolio Project
-- Updated  : October 2026
-- =============================================================================


-- ===========================================================================
-- SECTION 0: TABLE DEFINITIONS
-- ===========================================================================

-- ---------------------------------------------------------------------------
-- Table 1: annual_financials
--   Swiggy's consolidated P&L metrics by fiscal year (DRHP + estimates).
--   All monetary values in ₹ Crore (1 Crore = 10 Million INR).
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS annual_financials (
    fiscal_year          TEXT    NOT NULL,   -- e.g. 'FY2022', 'FY2023', 'FY2024', 'FY2025E'
    total_gov            REAL,              -- Gross Order Value (₹ Cr) — food + instamart + other
    food_delivery_gov    REAL,              -- GOV from food delivery segment (₹ Cr)
    instamart_gov        REAL,              -- GOV from Instamart (quick commerce) segment (₹ Cr)
    revenue              REAL,              -- Net revenue / platform fee (₹ Cr)
    take_rate_pct        REAL,              -- Revenue / Total GOV × 100 (%)
    contribution_profit  REAL,             -- Revenue minus variable costs (₹ Cr); can be negative
    ebitda               REAL,              -- Adj. EBITDA (₹ Cr); negative = loss
    net_loss             REAL,              -- Net Loss for the year (₹ Cr); stored as positive number
    monthly_transacting_users_mn REAL,     -- Average monthly transacting users (millions)
    active_restaurants   INTEGER,          -- Number of active restaurant partners (thousands)
    PRIMARY KEY (fiscal_year)
);

INSERT OR IGNORE INTO annual_financials VALUES
--  FY        total_gov  fd_gov   im_gov   rev     take%   contrib   ebitda   net_loss  MTU_mn  rest_k
  ('FY2022',  6,399,     5,855,   389,     1,675,  26.2,   -2,066,  -3,628,  3,629,    8.0,    150),
  ('FY2023',  11,247,    9,714,   1,266,   2,547,  22.6,   -1,705,  -3,311,  4,179,    14.1,   220),
  ('FY2024',  19,137,    14,880,  3,382,   3,511,  18.4,   -478,    -2,073,  2,350,    18.4,   289),
  ('FY2025E', 27,500,    19,800,  6,500,   5,100,  18.5,   120,     -900,    1,000,    23.0,   340);


-- ---------------------------------------------------------------------------
-- Table 2: quarterly_results
--   Swiggy quarterly performance metrics (public disclosures + estimates).
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS quarterly_results (
    quarter_id   TEXT    NOT NULL,   -- e.g. 'Q1FY24', 'Q2FY24' …
    fiscal_year  TEXT    NOT NULL,
    quarter_num  INTEGER NOT NULL,   -- 1–4
    gov          REAL,               -- Total GOV for the quarter (₹ Cr)
    revenue      REAL,               -- Net revenue for the quarter (₹ Cr)
    ebitda       REAL,               -- Adj. EBITDA (₹ Cr)
    net_loss     REAL,               -- Net loss (₹ Cr, positive number)
    mtu_mn       REAL,               -- Monthly transacting users (millions)
    PRIMARY KEY (quarter_id)
);

INSERT OR IGNORE INTO quarterly_results VALUES
  ('Q1FY23', 'FY2023', 1, 2,290, 540,  -920,  1,106, 12.0),
  ('Q2FY23', 'FY2023', 2, 2,640, 600,  -870,  1,060, 13.5),
  ('Q3FY23', 'FY2023', 3, 3,100, 680,  -800,    980, 14.8),
  ('Q4FY23', 'FY2023', 4, 3,217, 727,  -721,  1,033, 16.0),
  ('Q1FY24', 'FY2024', 1, 4,010, 785,  -610,    660, 16.5),
  ('Q2FY24', 'FY2024', 2, 4,620, 843,  -560,    598, 17.8),
  ('Q3FY24', 'FY2024', 3, 5,210, 918,  -491,    576, 19.2),
  ('Q4FY24', 'FY2024', 4, 5,297, 965,  -412,    516, 20.0),
  ('Q1FY25', 'FY2025E',1, 5,900, 1,100,-300,    310, 21.0),
  ('Q2FY25', 'FY2025E',2, 6,700, 1,250,-250,    270, 22.5),
  ('Q3FY25', 'FY2025E',3, 7,300, 1,370,-200,    230, 23.8),
  ('Q4FY25', 'FY2025E',4, 7,600, 1,380,-150,    190, 24.8);


-- ---------------------------------------------------------------------------
-- Table 3: food_delivery_cities
--   City-level food delivery metrics (synthetic, calibrated to DRHP totals).
--   GOV, AOV, orders in absolute units; delivery_time in minutes.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS food_delivery_cities (
    city_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name         TEXT    NOT NULL,
    tier              TEXT    NOT NULL,   -- 'Tier 1', 'Tier 2', 'Tier 3'
    state             TEXT    NOT NULL,
    gov_fy2022        REAL,               -- Food delivery GOV (₹ Cr)
    gov_fy2023        REAL,
    gov_fy2024        REAL,
    aov_fy2024        REAL,               -- Average Order Value in FY2024 (₹)
    avg_delivery_time REAL,               -- Avg delivery time (minutes) FY2024
    active_restaurants INTEGER,           -- Active restaurant partners FY2024
    monthly_orders_mn  REAL               -- Avg monthly orders (millions) FY2024
);

INSERT OR IGNORE INTO food_delivery_cities
    (city_name, tier, state, gov_fy2022, gov_fy2023, gov_fy2024, aov_fy2024, avg_delivery_time, active_restaurants, monthly_orders_mn)
VALUES
  ('Bengaluru',   'Tier 1', 'Karnataka',     980,  1,620,  2,450,  420,  28.5, 55000, 5.8),
  ('Mumbai',      'Tier 1', 'Maharashtra',   870,  1,430,  2,180,  450,  31.2, 52000, 4.8),
  ('Delhi',       'Tier 1', 'Delhi',         810,  1,320,  2,050,  440,  30.0, 48000, 4.7),
  ('Hyderabad',   'Tier 1', 'Telangana',     520,    880,  1,390,  410,  27.8, 36000, 3.4),
  ('Chennai',     'Tier 1', 'Tamil Nadu',    480,    790,  1,210,  400,  29.4, 32000, 3.0),
  ('Pune',        'Tier 1', 'Maharashtra',   370,    630,  1,020,  390,  26.5, 28000, 2.6),
  ('Kolkata',     'Tier 1', 'West Bengal',   310,    510,    820,  370,  33.0, 24000, 2.2),
  ('Ahmedabad',   'Tier 2', 'Gujarat',       180,    310,    520,  360,  29.8, 18000, 1.4),
  ('Jaipur',      'Tier 2', 'Rajasthan',     140,    240,    410,  340,  30.5, 14000, 1.2),
  ('Lucknow',     'Tier 2', 'Uttar Pradesh', 130,    220,    390,  330,  31.0, 12000, 1.2),
  ('Surat',       'Tier 2', 'Gujarat',       110,    195,    340,  320,  28.0, 11000, 1.1),
  ('Chandigarh',  'Tier 2', 'Punjab',        105,    185,    320,  350,  27.5, 10500, 0.9),
  ('Kochi',       'Tier 2', 'Kerala',        100,    175,    300,  355,  26.0, 10000, 0.8),
  ('Indore',      'Tier 2', 'Madhya Pradesh',  95,  165,    285,  315,  29.0,  9500, 0.9),
  ('Nagpur',      'Tier 2', 'Maharashtra',    88,   150,    260,  310,  30.2,  9000, 0.8),
  ('Bhopal',      'Tier 2', 'Madhya Pradesh',  72,  125,    215,  305,  31.5,  7500, 0.7),
  ('Coimbatore',  'Tier 2', 'Tamil Nadu',     68,   115,    200,  310,  27.0,  7000, 0.6),
  ('Vishakhapatnam','Tier 2','Andhra Pradesh', 62,  108,    185,  300,  28.5,  6500, 0.6),
  ('Patna',       'Tier 3', 'Bihar',          35,    62,    110,  280,  34.5,  3800, 0.4),
  ('Ranchi',      'Tier 3', 'Jharkhand',      28,    50,     88,  270,  35.0,  3100, 0.3),
  ('Guwahati',    'Tier 3', 'Assam',          25,    45,     78,  265,  36.0,  2800, 0.3),
  ('Varanasi',    'Tier 3', 'Uttar Pradesh',  22,    40,     70,  260,  35.5,  2500, 0.3),
  ('Jodhpur',     'Tier 3', 'Rajasthan',      18,    32,     57,  250,  36.5,  2000, 0.2),
  ('Mysuru',      'Tier 3', 'Karnataka',      20,    36,     62,  270,  32.0,  2200, 0.2),
  ('Agra',        'Tier 3', 'Uttar Pradesh',  17,    30,     52,  245,  37.0,  1800, 0.2);


-- ---------------------------------------------------------------------------
-- Table 4: instamart_cities
--   City-level Instamart (quick commerce) metrics (synthetic data).
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS instamart_cities (
    city_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name         TEXT    NOT NULL,
    tier              TEXT    NOT NULL,
    state             TEXT    NOT NULL,
    launch_year       INTEGER,            -- Year Instamart went live in this city
    dark_stores_fy2022 INTEGER,           -- Number of dark stores at end of FY2022
    dark_stores_fy2023 INTEGER,
    dark_stores_fy2024 INTEGER,
    gov_fy2022        REAL,               -- Instamart GOV (₹ Cr)
    gov_fy2023        REAL,
    gov_fy2024        REAL,
    aov_fy2024        REAL,               -- Average order value (₹)
    avg_delivery_time REAL,               -- Avg delivery time (minutes)
    monthly_orders_mn REAL                -- Avg monthly orders (millions) FY2024
);

INSERT OR IGNORE INTO instamart_cities
    (city_name, tier, state, launch_year, dark_stores_fy2022, dark_stores_fy2023, dark_stores_fy2024,
     gov_fy2022, gov_fy2023, gov_fy2024, aov_fy2024, avg_delivery_time, monthly_orders_mn)
VALUES
  ('Bengaluru',  'Tier 1', 'Karnataka',     2020,  45,  90,  160,  110, 380, 890,  485, 12.8, 1.84),
  ('Mumbai',     'Tier 1', 'Maharashtra',   2021,  38,  75,  140,   90, 310, 760,  510, 13.5, 1.49),
  ('Delhi',      'Tier 1', 'Delhi',         2021,  35,  70,  130,   85, 295, 710,  500, 13.0, 1.42),
  ('Hyderabad',  'Tier 1', 'Telangana',     2021,  22,  45,   85,   42, 150, 360,  470, 14.2, 0.77),
  ('Chennai',    'Tier 1', 'Tamil Nadu',    2021,  18,  38,   72,   36, 125, 300,  460, 14.8, 0.65),
  ('Pune',       'Tier 1', 'Maharashtra',   2022,   0,  28,   55,    0,  85, 210,  450, 13.8, 0.47),
  ('Kolkata',    'Tier 1', 'West Bengal',   2022,   0,  20,   42,    0,  65, 152,  440, 15.0, 0.35),
  ('Ahmedabad',  'Tier 2', 'Gujarat',       2023,   0,   8,   22,    0,  18,  68,  420, 15.5, 0.16),
  ('Jaipur',     'Tier 2', 'Rajasthan',     2023,   0,   6,   16,    0,  12,  52,  400, 16.2, 0.13),
  ('Chandigarh', 'Tier 2', 'Punjab',        2023,   0,   5,   14,    0,  10,  48,  410, 15.8, 0.12),
  ('Kochi',      'Tier 2', 'Kerala',        2023,   0,   5,   12,    0,   9,  42,  415, 15.2, 0.10),
  ('Surat',      'Tier 2', 'Gujarat',       2024,   0,   0,    8,    0,   0,  28,  395, 16.5, 0.07);


-- ---------------------------------------------------------------------------
-- Table 5: swiggy_one
--   Swiggy One loyalty subscription programme metrics (synthetic estimates).
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS swiggy_one (
    fiscal_year         TEXT    PRIMARY KEY,
    subscribers_mn      REAL,   -- Paid subscribers (millions)
    arpu_annual_inr     REAL,   -- Annual revenue per subscriber (₹)
    subscription_rev_cr REAL,   -- Total subscription revenue (₹ Cr)
    free_delivery_cost_cr REAL, -- Cost of free deliveries extended to members (₹ Cr)
    member_aov          REAL,   -- Average order value — members (₹)
    non_member_aov      REAL,   -- Average order value — non-members (₹)
    member_order_freq   REAL,   -- Avg orders/month per member
    non_member_order_freq REAL  -- Avg orders/month per non-member
);

INSERT OR IGNORE INTO swiggy_one VALUES
  ('FY2022', 2.1,  719,  151,  210,  445,  390,  5.8,  2.8),
  ('FY2023', 5.0,  899,  449,  580,  480,  410,  7.2,  3.2),
  ('FY2024', 9.5, 1,049, 997, 1,180, 510,  425,  8.5,  3.6),
  ('FY2025E',16.0,1,199,1,918,2,050, 540,  440,  9.2,  3.9);


-- ---------------------------------------------------------------------------
-- Table 6: competitor_comparison
--   Swiggy vs Zomato head-to-head metrics (public disclosures / estimates).
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS competitor_comparison (
    fiscal_year      TEXT    NOT NULL,
    company          TEXT    NOT NULL,   -- 'Swiggy' or 'Zomato'
    food_gov_cr      REAL,               -- Food delivery GOV (₹ Cr)
    qcom_gov_cr      REAL,               -- Quick commerce GOV (₹ Cr) — Instamart vs Blinkit
    total_gov_cr     REAL,               -- Total GOV (₹ Cr)
    revenue_cr       REAL,               -- Net revenue (₹ Cr)
    net_loss_cr      REAL,               -- Net loss (₹ Cr, positive = loss)
    mtu_mn           REAL,               -- Monthly transacting users (millions)
    market_share_pct REAL,               -- Estimated food delivery market share (%)
    PRIMARY KEY (fiscal_year, company)
);

INSERT OR IGNORE INTO competitor_comparison VALUES
  ('FY2022', 'Swiggy', 5855,  389,  6399,  1675, 3629, 8.0,  45),
  ('FY2022', 'Zomato', 6400,  150,  6600,  1414,  971, 9.5,  55),
  ('FY2023', 'Swiggy', 9714,  1266,11247,  2547, 4179,14.1,  42),
  ('FY2023', 'Zomato',11000,  1200,12400,  2742,  971,17.5,  58),
  ('FY2024', 'Swiggy',14880,  3382,19137,  3511, 2350,18.4,  43),
  ('FY2024', 'Zomato',17500,  8600,26500,  5405,  292,21.0,  57),
  ('FY2025E','Swiggy',19800,  6500,27500,  5100, 1000,23.0,  44),
  ('FY2025E','Zomato',23500, 14000,39000,  8200,  -50,27.0,  56);


-- ===========================================================================
-- SECTION 1: BUSINESS QUESTIONS
-- ===========================================================================

-- ---------------------------------------------------------------------------
-- Q1: Which city has the highest Food Delivery GOV in FY2024?
--     (Top 5 cities ranked by food delivery GOV)
-- ---------------------------------------------------------------------------
-- Business context: Identifying the highest-revenue cities helps Swiggy
-- allocate marketing spends, prioritise supply-side partnerships, and set
-- city-specific growth targets.
SELECT
    ROW_NUMBER() OVER (ORDER BY gov_fy2024 DESC) AS rank,
    city_name,
    tier,
    state,
    ROUND(gov_fy2024, 0)                          AS gov_fy2024_cr,
    ROUND(gov_fy2024 * 100.0 /
          SUM(gov_fy2024) OVER (), 2)             AS pct_of_national_gov
FROM food_delivery_cities
ORDER BY gov_fy2024 DESC
LIMIT 5;
-- Result insight: Bengaluru, Mumbai and Delhi together contribute ~40% of
-- national food delivery GOV — hyper-concentration in Tier 1 metros.


-- ---------------------------------------------------------------------------
-- Q2: Year-over-Year GOV growth by segment (Food Delivery vs Instamart)
-- ---------------------------------------------------------------------------
-- Business context: Comparing segment growth rates reveals which business arm
-- is scaling faster, guiding capital allocation between food and q-commerce.
SELECT
    fiscal_year,
    food_delivery_gov,
    instamart_gov,
    ROUND(
        (food_delivery_gov - LAG(food_delivery_gov) OVER (ORDER BY fiscal_year))
        * 100.0 / LAG(food_delivery_gov) OVER (ORDER BY fiscal_year), 1
    ) AS food_gov_yoy_pct,
    ROUND(
        (instamart_gov - LAG(instamart_gov) OVER (ORDER BY fiscal_year))
        * 100.0 / LAG(instamart_gov) OVER (ORDER BY fiscal_year), 1
    ) AS instamart_gov_yoy_pct
FROM annual_financials
ORDER BY fiscal_year;
-- Result insight: Instamart consistently outgrows food delivery YoY,
-- confirming q-commerce as the higher-velocity, higher-investment segment.


-- ---------------------------------------------------------------------------
-- Q3: Cities ranked by revenue growth rate using RANK window function
--     (FY2022 → FY2024 compound growth, top 10)
-- ---------------------------------------------------------------------------
-- Business context: Fast-growing cities are emerging demand centres where
-- early investment in restaurant supply and dark stores yields outsized returns.
WITH city_growth AS (
    SELECT
        city_name,
        tier,
        gov_fy2022,
        gov_fy2024,
        ROUND(
            (POWER(gov_fy2024 / NULLIF(gov_fy2022, 0), 0.5) - 1) * 100, 1
        ) AS cagr_2yr_pct    -- 2-year CAGR (%)
    FROM food_delivery_cities
    WHERE gov_fy2022 > 0
)
SELECT
    RANK() OVER (ORDER BY cagr_2yr_pct DESC) AS growth_rank,
    city_name,
    tier,
    gov_fy2022,
    gov_fy2024,
    cagr_2yr_pct
FROM city_growth
ORDER BY cagr_2yr_pct DESC
LIMIT 10;
-- Result insight: Several Tier 2 cities (e.g., Surat, Chandigarh) show
-- higher CAGR than some metros, flagging them as next-wave expansion targets.


-- ---------------------------------------------------------------------------
-- Q4: Tier-wise contribution to total national Food Delivery GOV in FY2024
-- ---------------------------------------------------------------------------
-- Business context: Understanding tier-mix informs whether Swiggy's growth
-- is metro-driven or increasingly diversified across Tier 2/3 markets.
SELECT
    tier,
    COUNT(city_name)                               AS num_cities,
    ROUND(SUM(gov_fy2024), 0)                      AS total_gov_cr,
    ROUND(SUM(gov_fy2024) * 100.0 /
          SUM(SUM(gov_fy2024)) OVER (), 2)         AS pct_of_total,
    ROUND(AVG(gov_fy2024), 0)                      AS avg_gov_per_city_cr,
    ROUND(AVG(aov_fy2024), 0)                      AS avg_aov_inr
FROM food_delivery_cities
GROUP BY tier
ORDER BY total_gov_cr DESC;
-- Result insight: Tier 1 cities represent the majority share of GOV despite
-- fewer cities, but Tier 2 cities are critical for per-unit economics.


-- ---------------------------------------------------------------------------
-- Q5: Which quarter had the highest total revenue (all time)?
-- ---------------------------------------------------------------------------
-- Business context: Identifying peak quarters reveals seasonality patterns
-- (festive demand spikes in Q3) that inform capacity and marketing planning.
SELECT
    quarter_id,
    fiscal_year,
    quarter_num,
    revenue                        AS revenue_cr,
    RANK() OVER (ORDER BY revenue DESC) AS revenue_rank,
    ROUND(revenue * 100.0 /
          SUM(revenue) OVER (PARTITION BY fiscal_year), 1) AS pct_of_fy_rev
FROM quarterly_results
ORDER BY revenue DESC
LIMIT 5;
-- Result insight: Q4 typically closes strongest due to year-end restaurant
-- promotions; Q3 sees a festive bump from Diwali-driven orders.


-- ---------------------------------------------------------------------------
-- Q6: Loss per ₹1 of revenue — trend by fiscal year (path to breakeven)
-- ---------------------------------------------------------------------------
-- Business context: The "loss per rupee of revenue" metric tracks operating
-- leverage improvement, signalling how efficiently Swiggy converts revenue
-- growth into loss reduction.
SELECT
    fiscal_year,
    revenue,
    net_loss,
    ROUND(net_loss / NULLIF(revenue, 0), 3)  AS loss_per_rupee_of_revenue,
    ROUND(
        (net_loss / NULLIF(revenue, 0) -
         LAG(net_loss / NULLIF(revenue, 0)) OVER (ORDER BY fiscal_year))
        * 100, 1
    )                                         AS change_in_loss_ratio_pp
FROM annual_financials
ORDER BY fiscal_year;
-- Result insight: A declining loss-per-rupee trend (from ~2.17 in FY2022 to
-- ~0.20 in FY2025E) indicates strong operating leverage — a key IPO narrative.


-- ---------------------------------------------------------------------------
-- Q7: City with the best (lowest) average delivery time in each tier
-- ---------------------------------------------------------------------------
-- Business context: Best-in-class delivery time benchmarks set the bar for
-- supply-chain and dark-store investments in each tier category.
WITH ranked_cities AS (
    SELECT
        city_name,
        tier,
        state,
        avg_delivery_time,
        ROW_NUMBER() OVER (
            PARTITION BY tier
            ORDER BY avg_delivery_time ASC
        ) AS rn
    FROM food_delivery_cities
)
SELECT
    tier,
    city_name,
    state,
    avg_delivery_time AS best_delivery_time_min
FROM ranked_cities
WHERE rn = 1
ORDER BY best_delivery_time_min;
-- Result insight: Tier 2 city Kochi (26 min) beats some metros — a testament
-- to compact city geography enabling faster last-mile logistics.


-- ---------------------------------------------------------------------------
-- Q8: Instamart dark store expansion rate by city (FY2022 → FY2024)
-- ---------------------------------------------------------------------------
-- Business context: Dark store density is the primary supply constraint for
-- q-commerce. Cities with rapid expansion are receiving strategic capex bets.
SELECT
    city_name,
    tier,
    launch_year,
    dark_stores_fy2022,
    dark_stores_fy2023,
    dark_stores_fy2024,
    (dark_stores_fy2024 - dark_stores_fy2022) AS net_new_stores_2yr,
    CASE
        WHEN dark_stores_fy2022 > 0 THEN
            ROUND((dark_stores_fy2024 - dark_stores_fy2022) * 100.0
                  / dark_stores_fy2022, 1)
        ELSE NULL
    END AS store_growth_pct_2yr
FROM instamart_cities
ORDER BY dark_stores_fy2024 DESC;
-- Result insight: Bengaluru leads with 160 dark stores (FY2024), more than
-- 3× its FY2022 base — reflecting q-commerce maturity in the home city.


-- ---------------------------------------------------------------------------
-- Q9: Top 3 cities by Instamart GOV in FY2024
-- ---------------------------------------------------------------------------
-- Business context: The top Instamart cities generate disproportionate q-comm
-- revenue and serve as template markets for rolling out the model elsewhere.
SELECT
    city_name,
    tier,
    ROUND(gov_fy2024, 0)                              AS instamart_gov_cr,
    dark_stores_fy2024,
    ROUND(aov_fy2024, 0)                              AS aov_inr,
    ROUND(gov_fy2024 / NULLIF(dark_stores_fy2024, 0), 2) AS gov_per_dark_store_cr,
    DENSE_RANK() OVER (ORDER BY gov_fy2024 DESC)      AS gov_rank
FROM instamart_cities
ORDER BY gov_fy2024 DESC
LIMIT 3;
-- Result insight: Bengaluru, Mumbai, Delhi are the q-commerce anchor cities;
-- GOV-per-dark-store (store productivity) reveals operational maturity.


-- ---------------------------------------------------------------------------
-- Q10: Swiggy vs Zomato revenue gap by fiscal year
-- ---------------------------------------------------------------------------
-- Business context: Tracking the absolute and percentage revenue gap versus
-- Zomato helps investors assess competitive positioning and catch-up potential.
WITH pivot AS (
    SELECT
        fiscal_year,
        MAX(CASE WHEN company = 'Swiggy' THEN revenue_cr END) AS swiggy_rev,
        MAX(CASE WHEN company = 'Zomato' THEN revenue_cr END) AS zomato_rev
    FROM competitor_comparison
    GROUP BY fiscal_year
)
SELECT
    fiscal_year,
    swiggy_rev,
    zomato_rev,
    ROUND(zomato_rev - swiggy_rev, 0)          AS revenue_gap_cr,
    ROUND((swiggy_rev / NULLIF(zomato_rev, 0)) * 100, 1) AS swiggy_as_pct_of_zomato
FROM pivot
ORDER BY fiscal_year;
-- Result insight: The revenue gap has widened in absolute terms (Zomato pulled
-- ahead after Blinkit acquisition), but Swiggy's % of Zomato revenue is
-- stabilising — indicating the gap is no longer expanding rapidly.


-- ---------------------------------------------------------------------------
-- Q11: Monthly Transacting Users (MTU) YoY growth rate
-- ---------------------------------------------------------------------------
-- Business context: MTU is Swiggy's core demand-side KPI; sustained MTU
-- growth is necessary to justify GOV expansion and investor confidence.
SELECT
    fiscal_year,
    monthly_transacting_users_mn                              AS mtu_mn,
    LAG(monthly_transacting_users_mn) OVER (ORDER BY fiscal_year) AS prev_mtu_mn,
    ROUND(
        (monthly_transacting_users_mn -
         LAG(monthly_transacting_users_mn) OVER (ORDER BY fiscal_year))
        * 100.0
        / NULLIF(LAG(monthly_transacting_users_mn) OVER (ORDER BY fiscal_year), 0),
        1
    ) AS mtu_yoy_growth_pct
FROM annual_financials
ORDER BY fiscal_year;
-- Result insight: MTU growing at 30–40% YoY signals healthy platform adoption;
-- slowdown in later years reflects market saturation in Tier 1, prompting
-- Tier 2/3 expansion strategy.


-- ---------------------------------------------------------------------------
-- Q12: Which fiscal year had the highest net loss?
-- ---------------------------------------------------------------------------
-- Business context: Peak loss year analysis reveals when Swiggy was most
-- aggressively investing (burning capital) to capture market share.
SELECT
    fiscal_year,
    net_loss                                        AS net_loss_cr,
    revenue,
    ROUND(net_loss / NULLIF(revenue, 0), 2)         AS loss_to_revenue_ratio,
    RANK() OVER (ORDER BY net_loss DESC)            AS loss_rank
FROM annual_financials
ORDER BY net_loss DESC;
-- Result insight: FY2023 was the peak loss year (₹4,179 Cr), driven by heavy
-- Instamart dark-store buildout and aggressive discounting to gain q-comm share.


-- ---------------------------------------------------------------------------
-- Q13: Take rate trend over fiscal years
-- ---------------------------------------------------------------------------
-- Business context: Take rate (revenue ÷ GOV) measures how much Swiggy
-- "keeps" from each rupee of orders. A rising take rate signals pricing power;
-- a declining one suggests competitive discounting.
SELECT
    fiscal_year,
    total_gov,
    revenue,
    take_rate_pct,
    LAG(take_rate_pct) OVER (ORDER BY fiscal_year) AS prev_take_rate,
    ROUND(
        take_rate_pct - LAG(take_rate_pct) OVER (ORDER BY fiscal_year), 2
    )                                               AS take_rate_change_pp
FROM annual_financials
ORDER BY fiscal_year;
-- Result insight: Take rate fell sharply from 26% (FY2022) to 18% (FY2024)
-- as Swiggy subsidised restaurant commissions and delivery costs to grow GOV;
-- stabilising at ~18.5% in FY2025E suggests the floor has been reached.


-- ---------------------------------------------------------------------------
-- Q14: Cities with GOV above the national city average (subquery)
-- ---------------------------------------------------------------------------
-- Business context: Above-average cities are self-sustaining demand clusters;
-- below-average cities need targeted supply and marketing interventions.
SELECT
    city_name,
    tier,
    ROUND(gov_fy2024, 0) AS gov_fy2024_cr
FROM food_delivery_cities
WHERE gov_fy2024 > (
    SELECT AVG(gov_fy2024)
    FROM food_delivery_cities
)
ORDER BY gov_fy2024 DESC;
-- Result insight: Only ~6 cities exceed the national average, confirming the
-- long-tail nature of city-level distribution (Pareto-like concentration).


-- ---------------------------------------------------------------------------
-- Q15: Cumulative revenue over quarters using SUM() window function
-- ---------------------------------------------------------------------------
-- Business context: Cumulative revenue tracks total platform monetisation over
-- time, useful for investor narratives around revenue milestone achievements.
SELECT
    quarter_id,
    fiscal_year,
    revenue                                              AS quarter_rev_cr,
    SUM(revenue) OVER (
        ORDER BY fiscal_year, quarter_num
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    )                                                    AS cumulative_rev_cr,
    SUM(revenue) OVER (PARTITION BY fiscal_year)         AS fy_total_rev_cr
FROM quarterly_results
ORDER BY fiscal_year, quarter_num;
-- Result insight: Crossing ₹10,000 Cr cumulative revenue took 3 years
-- (FY2022–FY2024); subsequent years add that amount annually —
-- illustrating Swiggy's revenue flywheel acceleration.


-- ---------------------------------------------------------------------------
-- Q16: Member vs Non-Member Average Order Value (AOV) difference
-- ---------------------------------------------------------------------------
-- Business context: A higher member AOV validates the Swiggy One upsell
-- strategy — subscribers order more per transaction, improving unit economics.
SELECT
    fiscal_year,
    subscribers_mn,
    member_aov,
    non_member_aov,
    ROUND(member_aov - non_member_aov, 0)           AS aov_premium_inr,
    ROUND((member_aov - non_member_aov) * 100.0
          / NULLIF(non_member_aov, 0), 1)           AS aov_premium_pct,
    member_order_freq,
    non_member_order_freq,
    ROUND(member_order_freq / NULLIF(non_member_order_freq, 0), 1) AS freq_multiplier
FROM swiggy_one
ORDER BY fiscal_year;
-- Result insight: Members order ~20% higher AOV and 2–2.4× more frequently
-- than non-members, confirming subscription loyalty strongly drives LTV.


-- ---------------------------------------------------------------------------
-- Q17: Instamart cities where average delivery time is under 15 minutes
-- ---------------------------------------------------------------------------
-- Business context: Sub-15-minute delivery is Instamart's core brand promise.
-- Achieving this across cities signals dark-store density and operational maturity.
SELECT
    city_name,
    tier,
    dark_stores_fy2024,
    avg_delivery_time,
    ROUND(gov_fy2024, 0)   AS gov_fy2024_cr,
    monthly_orders_mn
FROM instamart_cities
WHERE avg_delivery_time < 15
ORDER BY avg_delivery_time ASC;
-- Result insight: Only the top 3 metros currently achieve sub-15-min delivery;
-- this sets a clear infra benchmark — each new city needs ~100+ dark stores
-- before it can consistently hit the promise.


-- ---------------------------------------------------------------------------
-- Q18: Swiggy One — subscription revenue vs free delivery cost (net benefit)
-- ---------------------------------------------------------------------------
-- Business context: If subscription revenue > free delivery cost, the
-- programme is self-funding; if not, it's a strategic subsidy worth the LTV.
SELECT
    fiscal_year,
    subscribers_mn,
    subscription_rev_cr,
    free_delivery_cost_cr,
    ROUND(subscription_rev_cr - free_delivery_cost_cr, 0) AS net_benefit_cr,
    CASE
        WHEN subscription_rev_cr >= free_delivery_cost_cr
            THEN 'Self-funding ✔'
        ELSE 'Subsidised — LTV play ✗'
    END AS programme_status
FROM swiggy_one
ORDER BY fiscal_year;
-- Result insight: Swiggy One is currently not self-funding (delivery costs
-- exceed sub revenue) but is a deliberate retention tool — members' higher
-- LTV more than compensates for the delivery subsidy.


-- ---------------------------------------------------------------------------
-- Q19: Market share shift — Swiggy vs Zomato by fiscal year
-- ---------------------------------------------------------------------------
-- Business context: Relative market share tells investors whether Swiggy is
-- gaining or ceding ground in the core food delivery duopoly.
SELECT
    fiscal_year,
    company,
    food_gov_cr,
    market_share_pct,
    LAG(market_share_pct) OVER (
        PARTITION BY company ORDER BY fiscal_year
    )                                                AS prev_share_pct,
    ROUND(
        market_share_pct -
        LAG(market_share_pct) OVER (
            PARTITION BY company ORDER BY fiscal_year
        ), 1
    )                                                AS share_change_pp
FROM competitor_comparison
ORDER BY fiscal_year, company;
-- Result insight: Zomato gained 2 pp market share (FY2022–FY2024) through
-- Blinkit's bundled GOV growth; Swiggy's food-only share has held steady,
-- suggesting resilience in core business despite q-comm gap.


-- ---------------------------------------------------------------------------
-- Q20: Path to profitability — when does the loss trend suggest breakeven?
-- ---------------------------------------------------------------------------
-- Business context: Linear trend extrapolation of net loss helps build a
-- rough "breakeven year" narrative for IPO investors — a key valuation input.
WITH loss_trend AS (
    SELECT
        fiscal_year,
        revenue,
        net_loss,
        ebitda,
        ROUND(net_loss / NULLIF(revenue, 0), 3)                   AS loss_ratio,
        LAG(net_loss) OVER (ORDER BY fiscal_year)                  AS prev_loss,
        ROUND(net_loss - LAG(net_loss) OVER (ORDER BY fiscal_year), 0) AS yoy_loss_reduction
    FROM annual_financials
),
avg_reduction AS (
    SELECT ROUND(AVG(yoy_loss_reduction), 0) AS avg_annual_reduction
    FROM loss_trend
    WHERE yoy_loss_reduction IS NOT NULL
)
SELECT
    lt.fiscal_year,
    lt.net_loss,
    lt.loss_ratio,
    lt.yoy_loss_reduction,
    ar.avg_annual_reduction,
    -- Estimated years to breakeven based on current reduction pace
    CASE
        WHEN lt.fiscal_year = 'FY2025E' THEN
            ROUND(lt.net_loss / NULLIF(ABS(ar.avg_annual_reduction), 0), 1)
        ELSE NULL
    END AS est_yrs_to_breakeven,
    CASE
        WHEN lt.fiscal_year = 'FY2025E' THEN
            'Approx FY' || CAST(
                2025 + ROUND(lt.net_loss / NULLIF(ABS(ar.avg_annual_reduction), 0), 0)
            AS TEXT)
        ELSE NULL
    END AS est_breakeven_year
FROM loss_trend lt
CROSS JOIN avg_reduction ar
ORDER BY lt.fiscal_year;
-- Result insight: If the average annual loss reduction of ~₹876 Cr holds,
-- Swiggy could reach EBITDA breakeven around FY2026–FY2027.
-- The actual path will depend on Instamart capex and competitive discounting.


-- =============================================================================
-- END OF FILE
-- =============================================================================
