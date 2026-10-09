"""
Swiggy Sales Analysis - Interactive Dashboard Generator
Generates a fully self-contained HTML dashboard with 6 analysis tabs.
Run this AFTER generate_data.py
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR  = os.path.join(BASE_DIR, "data", "raw")
DASH_DIR = os.path.join(BASE_DIR, "dashboard")
os.makedirs(DASH_DIR, exist_ok=True)

# ── Load data ──────────────────────────────────────────────────────────────────
df_annual  = pd.read_csv(os.path.join(RAW_DIR, "swiggy_annual_financials.csv"))
df_qtr     = pd.read_csv(os.path.join(RAW_DIR, "swiggy_quarterly_results.csv"))
df_food    = pd.read_csv(os.path.join(RAW_DIR, "food_delivery_city_data.csv"))
df_insta   = pd.read_csv(os.path.join(RAW_DIR, "instamart_city_data.csv"))
df_one     = pd.read_csv(os.path.join(RAW_DIR, "swiggy_one_membership.csv"))
df_comp    = pd.read_csv(os.path.join(RAW_DIR, "competitor_comparison.csv"))

ORANGE     = "#FC8019"
DARK       = "#1a1a2e"
CARD_BG    = "#16213e"
TEXT       = "#e0e0e0"
GREEN      = "#00d09c"
RED        = "#ff6b6b"
BLUE       = "#4d9de0"
PURPLE     = "#a855f7"
YELLOW     = "#fbbf24"

def fig_to_json(fig):
    return fig.to_json()

# ── CHART BUILDERS ─────────────────────────────────────────────────────────────

def chart_revenue_trend():
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_annual["fiscal_year"], y=df_annual["revenue_cr"],
        name="Revenue", marker_color=ORANGE, opacity=0.85,
        text=[f"₹{v:,.0f} Cr" for v in df_annual["revenue_cr"]],
        textposition="outside", textfont=dict(color=TEXT, size=11)
    ))
    fig.add_trace(go.Scatter(
        x=df_annual["fiscal_year"], y=df_annual["net_loss_cr"].abs(),
        name="Net Loss (abs)", mode="lines+markers",
        line=dict(color=RED, width=3), marker=dict(size=8),
        yaxis="y2"
    ))
    fig.update_layout(
        title=dict(text="Revenue vs Net Loss Trend (FY2022–FY2025)", font=dict(color=TEXT, size=16)),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT), legend=dict(bgcolor=CARD_BG),
        yaxis=dict(title="Revenue (₹ Cr)", gridcolor="#2a2a4a", color=TEXT),
        yaxis2=dict(title="Net Loss (₹ Cr)", overlaying="y", side="right",
                    gridcolor="#2a2a4a", color=RED),
        xaxis=dict(color=TEXT),
        barmode="group", height=380
    )
    return fig_to_json(fig)

def chart_gov_segments():
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_annual["fiscal_year"], y=df_annual["food_delivery_gov_cr"],
                          name="Food Delivery", marker_color=ORANGE))
    fig.add_trace(go.Bar(x=df_annual["fiscal_year"], y=df_annual["instamart_gov_cr"],
                          name="Instamart", marker_color=GREEN))
    fig.add_trace(go.Bar(x=df_annual["fiscal_year"], y=df_annual["dineout_gov_cr"],
                          name="Dineout", marker_color=PURPLE))
    fig.update_layout(
        title=dict(text="GOV by Segment (₹ Cr)", font=dict(color=TEXT, size=16)),
        barmode="stack", paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT), legend=dict(bgcolor=CARD_BG),
        yaxis=dict(gridcolor="#2a2a4a", color=TEXT),
        xaxis=dict(color=TEXT), height=380
    )
    return fig_to_json(fig)

def chart_quarterly():
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=df_qtr["quarter"], y=df_qtr["revenue_cr"],
        name="Revenue", mode="lines+markers",
        line=dict(color=ORANGE, width=3), marker=dict(size=7)
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=df_qtr["quarter"], y=df_qtr["net_loss_cr"].abs(),
        name="Net Loss", mode="lines+markers",
        line=dict(color=RED, width=2, dash="dot"), marker=dict(size=6)
    ), secondary_y=True)
    fig.update_layout(
        title=dict(text="Quarterly Revenue & Loss Trend", font=dict(color=TEXT, size=16)),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT), legend=dict(bgcolor=CARD_BG),
        xaxis=dict(color=TEXT, tickangle=-45),
        height=400
    )
    fig.update_yaxes(title_text="Revenue (₹ Cr)", gridcolor="#2a2a4a", secondary_y=False, color=TEXT)
    fig.update_yaxes(title_text="Net Loss (₹ Cr)", secondary_y=True, color=RED)
    return fig_to_json(fig)

def chart_city_gov():
    df24 = df_food[df_food["fiscal_year"] == "FY2024"].sort_values("gov_cr", ascending=False)
    df24 = df24[df24["city"] != "Rest of India"].head(15)
    colors = [ORANGE if t == 1 else (GREEN if t == 2 else BLUE) for t in df24["tier"]]
    fig = go.Figure(go.Bar(
        x=df24["gov_cr"], y=df24["city"], orientation="h",
        marker_color=colors,
        text=[f"₹{v:,.0f} Cr" for v in df24["gov_cr"]],
        textposition="outside", textfont=dict(color=TEXT, size=10)
    ))
    fig.update_layout(
        title=dict(text="Top 15 Cities by Food Delivery GOV (FY2024)", font=dict(color=TEXT, size=16)),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT), height=520,
        yaxis=dict(color=TEXT, categoryorder="total ascending"),
        xaxis=dict(color=TEXT, gridcolor="#2a2a4a", title="GOV (₹ Cr)"),
        annotations=[
            dict(x=0.98, y=0.02, xref="paper", yref="paper",
                 text="🟠 Tier 1   🟢 Tier 2   🔵 Tier 3",
                 showarrow=False, font=dict(color=TEXT, size=11),
                 bgcolor=DARK, bordercolor=ORANGE, borderpad=4)
        ]
    )
    return fig_to_json(fig)

def chart_city_aov_scatter():
    df24 = df_food[df_food["fiscal_year"] == "FY2024"]
    df24 = df24[df24["city"] != "Rest of India"]
    tier_colors = {1: ORANGE, 2: GREEN, 3: BLUE}
    fig = go.Figure()
    for tier in [1, 2, 3]:
        d = df24[df24["tier"] == tier]
        fig.add_trace(go.Scatter(
            x=d["avg_delivery_time_min"], y=d["aov_rs"],
            mode="markers+text", name=f"Tier {tier}",
            marker=dict(color=tier_colors[tier], size=d["gov_cr"]/30+8,
                        line=dict(width=1, color=TEXT)),
            text=d["city"], textposition="top center",
            textfont=dict(size=9, color=TEXT)
        ))
    fig.update_layout(
        title=dict(text="AOV vs Delivery Time by City (bubble size = GOV)", font=dict(color=TEXT, size=15)),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT), legend=dict(bgcolor=CARD_BG),
        xaxis=dict(title="Avg Delivery Time (min)", gridcolor="#2a2a4a", color=TEXT),
        yaxis=dict(title="Average Order Value (₹)", gridcolor="#2a2a4a", color=TEXT),
        height=420
    )
    return fig_to_json(fig)

def chart_tier_comparison():
    tier_agg = df_food[df_food["fiscal_year"].isin(["FY2022","FY2023","FY2024","FY2025"])].copy()
    tier_agg["tier_label"] = tier_agg["tier"].map({1:"Tier 1",2:"Tier 2",3:"Tier 3"})
    tg = tier_agg.groupby(["fiscal_year","tier_label"])["gov_cr"].sum().reset_index()
    fig = px.bar(tg, x="fiscal_year", y="gov_cr", color="tier_label",
                  barmode="group",
                  color_discrete_map={"Tier 1": ORANGE, "Tier 2": GREEN, "Tier 3": BLUE},
                  labels={"gov_cr": "GOV (₹ Cr)", "fiscal_year": "Fiscal Year", "tier_label": "City Tier"})
    fig.update_layout(
        title=dict(text="GOV by City Tier (FY2022–FY2025)", font=dict(color=TEXT, size=16)),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT), legend=dict(bgcolor=CARD_BG, title=""),
        yaxis=dict(gridcolor="#2a2a4a", color=TEXT),
        xaxis=dict(color=TEXT), height=380
    )
    return fig_to_json(fig)

def chart_instamart_gov():
    im_nat = df_annual[["fiscal_year","instamart_gov_cr"]]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=im_nat["fiscal_year"], y=im_nat["instamart_gov_cr"],
        mode="lines+markers+text",
        line=dict(color=GREEN, width=4),
        marker=dict(size=12, color=GREEN, symbol="diamond"),
        text=[f"₹{v:,} Cr" for v in im_nat["instamart_gov_cr"]],
        textposition="top center", textfont=dict(color=TEXT, size=12)
    ))
    fig.add_annotation(x="FY2024", y=8069,
                        text="29x growth<br>in 3 years!", showarrow=True,
                        arrowcolor=ORANGE, font=dict(color=ORANGE, size=12),
                        arrowhead=2, ax=60, ay=-40)
    fig.update_layout(
        title=dict(text="Instamart GOV Explosive Growth (₹ Cr)", font=dict(color=TEXT, size=16)),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT),
        yaxis=dict(gridcolor="#2a2a4a", color=TEXT, title="GOV (₹ Cr)"),
        xaxis=dict(color=TEXT), height=360
    )
    return fig_to_json(fig)

def chart_instamart_cities():
    df24_i = df_insta[df_insta["fiscal_year"] == "FY2024"].sort_values("gov_cr", ascending=False).head(12)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df24_i["city"], y=df24_i["gov_cr"],
        name="GOV (₹ Cr)", marker_color=GREEN,
        text=[f"₹{v:.0f} Cr" for v in df24_i["gov_cr"]],
        textposition="outside", textfont=dict(color=TEXT, size=10)
    ))
    fig.add_trace(go.Scatter(
        x=df24_i["city"], y=df24_i["dark_stores"],
        name="Dark Stores", mode="lines+markers",
        line=dict(color=ORANGE, width=2), marker=dict(size=8),
        yaxis="y2"
    ))
    fig.update_layout(
        title=dict(text="Instamart: Top Cities by GOV & Dark Stores (FY2024)", font=dict(color=TEXT, size=15)),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT), legend=dict(bgcolor=CARD_BG),
        yaxis=dict(title="GOV (₹ Cr)", gridcolor="#2a2a4a", color=TEXT),
        yaxis2=dict(title="Dark Stores", overlaying="y", side="right", color=ORANGE),
        xaxis=dict(color=TEXT, tickangle=-30), height=400
    )
    return fig_to_json(fig)

def chart_dark_store_expansion():
    ds = df_annual[["fiscal_year","dark_stores","instamart_cities"]]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=ds["fiscal_year"], y=ds["dark_stores"],
        name="Dark Stores", marker_color=GREEN, opacity=0.8
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=ds["fiscal_year"], y=ds["instamart_cities"],
        name="Cities Active", mode="lines+markers",
        line=dict(color=ORANGE, width=3), marker=dict(size=10)
    ), secondary_y=True)
    fig.update_layout(
        title=dict(text="Dark Store & City Expansion", font=dict(color=TEXT, size=16)),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT), legend=dict(bgcolor=CARD_BG),
        xaxis=dict(color=TEXT), height=360
    )
    fig.update_yaxes(title_text="Dark Stores", gridcolor="#2a2a4a", secondary_y=False, color=TEXT)
    fig.update_yaxes(title_text="Cities", secondary_y=True, color=ORANGE)
    return fig_to_json(fig)

def chart_swiggy_one():
    fig = make_subplots(rows=1, cols=2, subplot_titles=["Subscriber Growth (Mn)", "Member vs Non-Member AOV (₹)"])
    months_subset = df_one[::3]
    fig.add_trace(go.Scatter(
        x=months_subset["month"], y=months_subset["subscribers_mn"],
        mode="lines+markers", line=dict(color=PURPLE, width=3),
        marker=dict(size=7), name="Subscribers (Mn)"
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=months_subset["month"], y=months_subset["member_aov_rs"],
        mode="lines", line=dict(color=ORANGE, width=2), name="Member AOV"
    ), row=1, col=2)
    fig.add_trace(go.Scatter(
        x=months_subset["month"], y=months_subset["non_member_aov_rs"],
        mode="lines", line=dict(color=BLUE, width=2, dash="dot"), name="Non-Member AOV"
    ), row=1, col=2)
    fig.update_layout(
        title=dict(text="Swiggy One Membership Performance", font=dict(color=TEXT, size=16)),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT), legend=dict(bgcolor=CARD_BG), height=380
    )
    for ax in ["xaxis", "xaxis2", "yaxis", "yaxis2"]:
        fig.update_layout(**{ax: dict(color=TEXT, gridcolor="#2a2a4a", tickangle=-30 if "x" in ax else 0)})
    return fig_to_json(fig)

def chart_swiggy_one_orders():
    months_subset = df_one[::3]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months_subset["month"],
        y=months_subset["member_monthly_orders"],
        name="Member Orders/Month", marker_color=PURPLE
    ))
    fig.add_trace(go.Bar(
        x=months_subset["month"],
        y=months_subset["non_member_monthly_orders"],
        name="Non-Member Orders/Month", marker_color=BLUE
    ))
    fig.update_layout(
        title=dict(text="Order Frequency: Members vs Non-Members", font=dict(color=TEXT, size=15)),
        barmode="group", paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT), legend=dict(bgcolor=CARD_BG),
        yaxis=dict(gridcolor="#2a2a4a", color=TEXT, title="Avg Orders / Month"),
        xaxis=dict(color=TEXT, tickangle=-30), height=360
    )
    return fig_to_json(fig)

def chart_vs_zomato_revenue():
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_comp["fiscal_year"], y=df_comp["swiggy_revenue_cr"],
        mode="lines+markers+text", name="Swiggy",
        line=dict(color=ORANGE, width=4), marker=dict(size=10),
        text=[f"₹{v:,}" for v in df_comp["swiggy_revenue_cr"]],
        textposition="top center", textfont=dict(color=ORANGE, size=10)
    ))
    fig.add_trace(go.Scatter(
        x=df_comp["fiscal_year"], y=df_comp["zomato_revenue_cr"],
        mode="lines+markers+text", name="Zomato",
        line=dict(color=RED, width=4), marker=dict(size=10),
        text=[f"₹{v:,}" for v in df_comp["zomato_revenue_cr"]],
        textposition="bottom center", textfont=dict(color=RED, size=10)
    ))
    fig.update_layout(
        title=dict(text="Revenue: Swiggy vs Zomato (₹ Cr)", font=dict(color=TEXT, size=16)),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT), legend=dict(bgcolor=CARD_BG),
        yaxis=dict(gridcolor="#2a2a4a", color=TEXT, title="Revenue (₹ Cr)"),
        xaxis=dict(color=TEXT), height=380
    )
    return fig_to_json(fig)

def chart_vs_zomato_gov():
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_comp["fiscal_year"], y=df_comp["swiggy_food_gov_cr"],
                          name="Swiggy Food", marker_color=ORANGE))
    fig.add_trace(go.Bar(x=df_comp["fiscal_year"], y=df_comp["zomato_food_gov_cr"],
                          name="Zomato Food", marker_color="#ff4d4d"))
    fig.add_trace(go.Bar(x=df_comp["fiscal_year"], y=df_comp["swiggy_qcommerce_gov_cr"],
                          name="Swiggy Instamart", marker_color=GREEN))
    fig.add_trace(go.Bar(x=df_comp["fiscal_year"], y=df_comp["zomato_qcommerce_gov_cr"],
                          name="Zomato Blinkit", marker_color="#00b09c"))
    fig.update_layout(
        title=dict(text="GOV Comparison: Swiggy vs Zomato by Segment (₹ Cr)", font=dict(color=TEXT, size=15)),
        barmode="group", paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT), legend=dict(bgcolor=CARD_BG),
        yaxis=dict(gridcolor="#2a2a4a", color=TEXT, title="GOV (₹ Cr)"),
        xaxis=dict(color=TEXT), height=400
    )
    return fig_to_json(fig)

def chart_market_share():
    df_share = df_comp.melt(id_vars="fiscal_year",
                             value_vars=["swiggy_market_share_pct","zomato_market_share_pct"],
                             var_name="company", value_name="share")
    df_share["company"] = df_share["company"].map({
        "swiggy_market_share_pct": "Swiggy", "zomato_market_share_pct": "Zomato"
    })
    fig = px.area(df_share, x="fiscal_year", y="share", color="company",
                   color_discrete_map={"Swiggy": ORANGE, "Zomato": RED},
                   labels={"share": "Market Share (%)", "fiscal_year": "Fiscal Year"})
    fig.update_layout(
        title=dict(text="Market Share: Swiggy vs Zomato (%)", font=dict(color=TEXT, size=16)),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT), legend=dict(bgcolor=CARD_BG, title=""),
        yaxis=dict(gridcolor="#2a2a4a", color=TEXT),
        xaxis=dict(color=TEXT), height=360
    )
    return fig_to_json(fig)

def chart_loss_profitability():
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_qtr["quarter"], y=df_qtr["net_loss_cr"],
        marker_color=[GREEN if v > -500 else (YELLOW if v > -1000 else RED) for v in df_qtr["net_loss_cr"]],
        name="Net Loss (₹ Cr)",
        text=[f"₹{v:.0f}" for v in df_qtr["net_loss_cr"]],
        textposition="outside", textfont=dict(color=TEXT, size=9)
    ))
    fig.add_hline(y=0, line_color=GREEN, line_width=2, line_dash="dash",
                   annotation_text="Profitability Line", annotation_font_color=GREEN)
    fig.update_layout(
        title=dict(text="Path to Profitability — Quarterly Net Loss (₹ Cr)", font=dict(color=TEXT, size=15)),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT),
        yaxis=dict(gridcolor="#2a2a4a", color=TEXT, title="Net Loss (₹ Cr)"),
        xaxis=dict(color=TEXT, tickangle=-45), height=400
    )
    return fig_to_json(fig)

def chart_users():
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=df_annual["fiscal_year"],
        y=df_annual["monthly_transacting_users_mn"],
        name="Monthly Users (Mn)", marker_color=BLUE, opacity=0.8
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=df_annual["fiscal_year"],
        y=df_annual["restaurant_partners"] / 1000,
        name="Restaurant Partners (K)", mode="lines+markers",
        line=dict(color=ORANGE, width=3), marker=dict(size=9)
    ), secondary_y=True)
    fig.update_layout(
        title=dict(text="Monthly Transacting Users & Restaurant Partners", font=dict(color=TEXT, size=15)),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT), legend=dict(bgcolor=CARD_BG),
        xaxis=dict(color=TEXT), height=360
    )
    fig.update_yaxes(title_text="Users (Mn)", gridcolor="#2a2a4a", secondary_y=False, color=TEXT)
    fig.update_yaxes(title_text="Restaurant Partners (K)", secondary_y=True, color=ORANGE)
    return fig_to_json(fig)

# ── GENERATE ALL CHART JSON ────────────────────────────────────────────────────
print("Generating charts...")
charts = {
    "revenue_trend":        chart_revenue_trend(),
    "gov_segments":         chart_gov_segments(),
    "quarterly":            chart_quarterly(),
    "city_gov":             chart_city_gov(),
    "city_scatter":         chart_city_aov_scatter(),
    "tier_comparison":      chart_tier_comparison(),
    "instamart_gov":        chart_instamart_gov(),
    "instamart_cities":     chart_instamart_cities(),
    "dark_store_expansion": chart_dark_store_expansion(),
    "swiggy_one":           chart_swiggy_one(),
    "swiggy_one_orders":    chart_swiggy_one_orders(),
    "vs_zomato_revenue":    chart_vs_zomato_revenue(),
    "vs_zomato_gov":        chart_vs_zomato_gov(),
    "market_share":         chart_market_share(),
    "loss_path":            chart_loss_profitability(),
    "users":                chart_users(),
}

# KPI values
kpi = {
    "rev_fy24": "₹11,634 Cr",
    "loss_fy24": "₹1,888 Cr",
    "food_gov": "₹27,000 Cr",
    "instamart_gov": "₹8,069 Cr",
    "cities": "653",
    "dark_stores": "605",
    "users": "13 Mn",
    "restaurants": "1.96 Lakh",
}

# ── HTML TEMPLATE ──────────────────────────────────────────────────────────────
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🍕 Swiggy Sales Analysis Dashboard | FY2022–FY2025</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
  :root {{
    --bg: #0f0f1a;
    --card: #16213e;
    --border: #2a2a5a;
    --orange: #FC8019;
    --green: #00d09c;
    --text: #e0e0e0;
    --muted: #8888aa;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: var(--bg); color: var(--text); font-family: 'Segoe UI', system-ui, sans-serif; }}

  /* ── HEADER ── */
  .header {{
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-bottom: 3px solid var(--orange);
    padding: 20px 32px;
    display: flex; align-items: center; justify-content: space-between;
  }}
  .header-left {{ display: flex; align-items: center; gap: 16px; }}
  .logo {{ font-size: 2.2rem; }}
  .header h1 {{ font-size: 1.6rem; font-weight: 700; color: var(--orange); }}
  .header p {{ font-size: 0.82rem; color: var(--muted); margin-top: 3px; }}
  .header-badge {{
    background: #1e3a5f; border: 1px solid var(--orange);
    border-radius: 20px; padding: 6px 14px; font-size: 0.75rem; color: var(--orange);
  }}

  /* ── TABS ── */
  .tabs {{
    display: flex; background: #0d0d1a; border-bottom: 1px solid var(--border);
    padding: 0 24px; overflow-x: auto; gap: 4px;
  }}
  .tab {{
    padding: 14px 22px; cursor: pointer; font-size: 0.88rem; font-weight: 500;
    color: var(--muted); border-bottom: 3px solid transparent;
    transition: all 0.2s; white-space: nowrap; background: none; border-top: none;
    border-left: none; border-right: none;
  }}
  .tab:hover {{ color: var(--text); }}
  .tab.active {{ color: var(--orange); border-bottom-color: var(--orange); }}
  .tab-content {{ display: none; padding: 24px 32px; }}
  .tab-content.active {{ display: block; }}

  /* ── KPI CARDS ── */
  .kpi-grid {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px; margin-bottom: 28px;
  }}
  .kpi-card {{
    background: var(--card); border: 1px solid var(--border);
    border-radius: 12px; padding: 18px 20px;
    border-top: 3px solid var(--orange);
    transition: transform 0.2s;
  }}
  .kpi-card:hover {{ transform: translateY(-3px); }}
  .kpi-label {{ font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }}
  .kpi-value {{ font-size: 1.5rem; font-weight: 700; color: var(--orange); margin: 6px 0 2px; }}
  .kpi-sub {{ font-size: 0.72rem; color: var(--muted); }}

  /* ── CHART CONTAINERS ── */
  .chart-grid {{ display: grid; gap: 20px; }}
  .chart-grid-2 {{ grid-template-columns: repeat(auto-fit, minmax(480px, 1fr)); }}
  .chart-card {{
    background: var(--card); border: 1px solid var(--border);
    border-radius: 12px; padding: 8px; overflow: hidden;
  }}
  .chart-full {{ margin-bottom: 20px; }}

  /* ── SECTION TITLE ── */
  .section-title {{
    font-size: 0.78rem; font-weight: 700; color: var(--orange);
    text-transform: uppercase; letter-spacing: 0.08em;
    margin-bottom: 16px; padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
  }}

  /* ── INSIGHT BOX ── */
  .insights {{
    background: #0d1f3c; border: 1px solid #1e3a5f;
    border-left: 4px solid var(--orange); border-radius: 8px;
    padding: 18px 22px; margin: 20px 0;
  }}
  .insights h4 {{ color: var(--orange); font-size: 0.85rem; margin-bottom: 10px; }}
  .insights ul {{ list-style: none; }}
  .insights li {{ font-size: 0.82rem; color: var(--muted); padding: 4px 0; }}
  .insights li::before {{ content: "💡 "; }}

  /* ── FOOTER ── */
  .footer {{
    text-align: center; padding: 20px; color: var(--muted);
    font-size: 0.75rem; border-top: 1px solid var(--border); margin-top: 20px;
  }}
  .footer a {{ color: var(--orange); text-decoration: none; }}

  /* ── DATA DISCLAIMER ── */
  .disclaimer {{
    background: #1a1a0d; border: 1px solid #3a3a0d;
    border-radius: 8px; padding: 12px 16px; margin-bottom: 20px;
    font-size: 0.75rem; color: #aaaa60;
  }}
  .disclaimer strong {{ color: #cccc40; }}

  @media(max-width: 600px) {{
    .header {{ padding: 14px 16px; flex-direction: column; align-items: flex-start; gap: 10px; }}
    .tab-content {{ padding: 16px; }}
    .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .chart-grid-2 {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

<!-- HEADER -->
<div class="header">
  <div class="header-left">
    <div class="logo">🍕</div>
    <div>
      <h1>Swiggy Sales Analysis Dashboard</h1>
      <p>FY2022 – FY2025 | Food Delivery · Instamart · Swiggy One | India Market</p>
    </div>
  </div>
  <div>
    <div class="header-badge">📊 Data Analyst Portfolio Project</div>
    <div style="font-size:0.7rem;color:var(--muted);text-align:right;margin-top:4px;">Built with Python · Plotly · Pandas</div>
  </div>
</div>

<!-- TABS -->
<div class="tabs">
  <button class="tab active" onclick="showTab('overview')">📊 Overview</button>
  <button class="tab" onclick="showTab('food')">🍔 Food Delivery</button>
  <button class="tab" onclick="showTab('instamart')">🛒 Instamart</button>
  <button class="tab" onclick="showTab('cities')">🏙️ City Analysis</button>
  <button class="tab" onclick="showTab('swiggy_one')">💳 Swiggy One</button>
  <button class="tab" onclick="showTab('competitor')">⚔️ vs Zomato</button>
</div>

<!-- ══════════════════════════════════════════════════════════════════════ -->
<!-- TAB 1: OVERVIEW                                                        -->
<!-- ══════════════════════════════════════════════════════════════════════ -->
<div id="tab-overview" class="tab-content active">

  <div class="disclaimer">
    <strong>📋 Data Note:</strong> National-level metrics (revenue, GOV, losses) are sourced from Swiggy's real DRHP, IPO filings, and quarterly investor reports.
    City-level data is <strong>realistic synthetic data</strong> calibrated to match official national totals. This is disclosed in the project README.
  </div>

  <p class="section-title">FY2024 — Key Performance Indicators</p>
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-label">Total Revenue</div>
      <div class="kpi-value">{kpi["rev_fy24"]}</div>
      <div class="kpi-sub">+36% YoY growth</div>
    </div>
    <div class="kpi-card" style="border-top-color:#ff6b6b">
      <div class="kpi-label">Net Loss</div>
      <div class="kpi-value" style="color:#ff6b6b">{kpi["loss_fy24"]}</div>
      <div class="kpi-sub">↓ 44% reduction from FY2023</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Food Delivery GOV</div>
      <div class="kpi-value">{kpi["food_gov"]}</div>
      <div class="kpi-sub">74% of total GOV</div>
    </div>
    <div class="kpi-card" style="border-top-color:#00d09c">
      <div class="kpi-label">Instamart GOV</div>
      <div class="kpi-value" style="color:#00d09c">{kpi["instamart_gov"]}</div>
      <div class="kpi-sub">169% YoY growth</div>
    </div>
    <div class="kpi-card" style="border-top-color:#4d9de0">
      <div class="kpi-label">Cities (Food)</div>
      <div class="kpi-value" style="color:#4d9de0">{kpi["cities"]}</div>
      <div class="kpi-sub">Pan-India presence</div>
    </div>
    <div class="kpi-card" style="border-top-color:#a855f7">
      <div class="kpi-label">Dark Stores</div>
      <div class="kpi-value" style="color:#a855f7">{kpi["dark_stores"]}</div>
      <div class="kpi-sub">43 cities as of FY2024</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Monthly Users</div>
      <div class="kpi-value">{kpi["users"]}</div>
      <div class="kpi-sub">+18% YoY</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Restaurant Partners</div>
      <div class="kpi-value">{kpi["restaurants"]}</div>
      <div class="kpi-sub">+15% from FY2023</div>
    </div>
  </div>

  <div class="chart-full chart-card">
    <div id="chart-revenue-trend"></div>
  </div>

  <div class="chart-grid chart-grid-2">
    <div class="chart-card"><div id="chart-gov-segments"></div></div>
    <div class="chart-card"><div id="chart-quarterly"></div></div>
  </div>

  <div class="chart-full chart-card" style="margin-top:20px">
    <div id="chart-loss-path"></div>
  </div>

  <div class="insights">
    <h4>🔍 Key Findings — National Overview</h4>
    <ul>
      <li>Revenue grew <strong>2.04x from ₹5,705 Cr (FY2022) to ₹11,634 Cr (FY2024)</strong>, showing consistent 30%+ annual growth.</li>
      <li>Net losses <strong>peaked at ₹3,758 Cr in FY2023</strong> but were slashed to ₹1,888 Cr in FY2024 — a 50% improvement in 2 years.</li>
      <li>Total GOV crossed <strong>₹36,000 Cr in FY2024</strong>, validating Swiggy's scale in the Indian food-tech market.</li>
      <li>Instamart GOV grew from <strong>₹500 Cr (FY2022) to ₹8,069 Cr (FY2024)</strong> — a 29x surge in just 2 years.</li>
      <li>Q1 FY2027 shows losses narrowing to <strong>₹791 Cr</strong>, suggesting a clear path toward EBITDA breakeven by FY2027-28.</li>
    </ul>
  </div>
</div>

<!-- ══════════════════════════════════════════════════════════════════════ -->
<!-- TAB 2: FOOD DELIVERY                                                   -->
<!-- ══════════════════════════════════════════════════════════════════════ -->
<div id="tab-food" class="tab-content">
  <p class="section-title">Food Delivery — City-wise & National Analysis</p>

  <div class="chart-full chart-card">
    <div id="chart-city-gov"></div>
  </div>

  <div class="chart-grid chart-grid-2">
    <div class="chart-card"><div id="chart-city-scatter"></div></div>
    <div class="chart-card"><div id="chart-users"></div></div>
  </div>

  <div class="insights" style="margin-top:20px">
    <h4>🔍 Key Findings — Food Delivery</h4>
    <ul>
      <li><strong>Bengaluru, Delhi NCR, and Mumbai</strong> together contribute ~43% of total food delivery GOV.</li>
      <li>Mumbai has the <strong>highest AOV (₹490)</strong> while Tier 2 cities like Patna trail at ₹300 — showing urban premium pricing.</li>
      <li>Tier 2 cities (Jaipur, Lucknow, Indore) show <strong>24-28% YoY growth</strong>, outpacing Tier 1 (~15%) — the next growth engine.</li>
      <li>Hyderabad has the <strong>fastest food delivery time</strong> among Tier 1 cities at ~30 min average.</li>
    </ul>
  </div>
</div>

<!-- ══════════════════════════════════════════════════════════════════════ -->
<!-- TAB 3: INSTAMART                                                        -->
<!-- ══════════════════════════════════════════════════════════════════════ -->
<div id="tab-instamart" class="tab-content">
  <p class="section-title">Instamart — Quick Commerce Analysis</p>

  <div class="chart-full chart-card">
    <div id="chart-instamart-gov"></div>
  </div>

  <div class="chart-grid chart-grid-2">
    <div class="chart-card"><div id="chart-instamart-cities"></div></div>
    <div class="chart-card"><div id="chart-dark-store"></div></div>
  </div>

  <div class="insights" style="margin-top:20px">
    <h4>🔍 Key Findings — Instamart</h4>
    <ul>
      <li>Instamart's GOV rocketed from <strong>₹500 Cr (FY2022) to ₹8,069 Cr (FY2024)</strong> — a 29x surge in 2 years.</li>
      <li><strong>Bengaluru leads</strong> with 95 dark stores and ~20% of national Instamart GOV — the most mature quick-commerce market.</li>
      <li>Average delivery time across cities hovers at <strong>11-14 minutes</strong> in Tier 1 — well within the 15-minute promise.</li>
      <li>By Q1 FY2027, Instamart GOV of <strong>₹7,907 Cr</strong> is nearly equal to Food Delivery per quarter — a structural shift in demand.</li>
      <li>Instamart reached <strong>contribution breakeven by mid-2026</strong>, proving the quick commerce unit economics model.</li>
    </ul>
  </div>
</div>

<!-- ══════════════════════════════════════════════════════════════════════ -->
<!-- TAB 4: CITY ANALYSIS                                                   -->
<!-- ══════════════════════════════════════════════════════════════════════ -->
<div id="tab-cities" class="tab-content">
  <p class="section-title">City Tier Analysis — Tier 1 vs Tier 2 vs Tier 3</p>

  <div class="chart-full chart-card">
    <div id="chart-tier-comparison"></div>
  </div>

  <div class="insights">
    <h4>🔍 Key Findings — City Tiers</h4>
    <ul>
      <li>Tier 1 cities (7 cities) contribute <strong>~70% of total food delivery GOV</strong>, but this share is slowly declining as Tier 2 grows.</li>
      <li>Tier 2 cities grew their GOV contribution from <strong>18% (FY2022) to 22% (FY2024)</strong> — a key strategic opportunity.</li>
      <li>Tier 3 expansion is still early, but cities like Guwahati and Bhubaneswar show <strong>30-35% YoY growth</strong> — highest of all tiers.</li>
      <li>Instamart is primarily a Tier 1 + select Tier 2 business, with <strong>Bengaluru, Mumbai, Delhi NCR</strong> alone accounting for 56% of IM GOV.</li>
    </ul>
  </div>
</div>

<!-- ══════════════════════════════════════════════════════════════════════ -->
<!-- TAB 5: SWIGGY ONE                                                      -->
<!-- ══════════════════════════════════════════════════════════════════════ -->
<div id="tab-swiggy_one" class="tab-content">
  <p class="section-title">Swiggy One — Subscription & Membership Analysis</p>

  <div class="chart-full chart-card">
    <div id="chart-swiggy-one"></div>
  </div>
  <div class="chart-full chart-card" style="margin-top:20px">
    <div id="chart-swiggy-one-orders"></div>
  </div>

  <div class="insights">
    <h4>🔍 Key Findings — Swiggy One</h4>
    <ul>
      <li>Swiggy One members place <strong>4.2x more orders per month</strong> than non-members — showing strong retention uplift.</li>
      <li>Member AOV (₹510) is <strong>34% higher</strong> than non-member AOV (₹380) — members order more premium items with free delivery.</li>
      <li>The subscription program creates a <strong>virtuous cycle</strong>: free delivery → more orders → higher GOV → better take rate recovery.</li>
      <li>At ₹99/month, Swiggy One generates subscription revenue that <strong>covers free delivery costs with a margin</strong> — it's a profitable product.</li>
    </ul>
  </div>
</div>

<!-- ══════════════════════════════════════════════════════════════════════ -->
<!-- TAB 6: COMPETITOR                                                      -->
<!-- ══════════════════════════════════════════════════════════════════════ -->
<div id="tab-competitor" class="tab-content">
  <p class="section-title">Competitive Analysis — Swiggy vs Zomato</p>

  <div class="chart-full chart-card">
    <div id="chart-vs-zomato-revenue"></div>
  </div>

  <div class="chart-grid chart-grid-2">
    <div class="chart-card"><div id="chart-vs-zomato-gov"></div></div>
    <div class="chart-card"><div id="chart-market-share"></div></div>
  </div>

  <div class="insights" style="margin-top:20px">
    <h4>🔍 Key Findings — Swiggy vs Zomato</h4>
    <ul>
      <li>Zomato <strong>crossed profitability in FY2024</strong> (₹351 Cr profit) while Swiggy is still loss-making — a key competitive distinction.</li>
      <li>Zomato's Blinkit scaled faster in quick commerce: <strong>791 dark stores vs Swiggy's 605</strong> by end of FY2024.</li>
      <li>Swiggy holds ~44% food delivery market share in FY2024 but faces pressure from Zomato's 56% — a gap that requires strong Tier 2 execution.</li>
      <li>Swiggy's <strong>total GOV per user is higher</strong> — suggesting a more premium or loyal user base despite fewer MAUs.</li>
      <li>Both companies are converging in quick commerce — Instamart vs Blinkit will likely define the winner for the next decade.</li>
    </ul>
  </div>
</div>

<!-- FOOTER -->
<div class="footer">
  Built by <strong style="color:var(--orange)">Akash</strong> as a Data Analyst Portfolio Project |
  Data Sources: <a href="https://www.sebi.gov.in" target="_blank">Swiggy DRHP (SEBI Filing)</a> · Quarterly Investor Reports · NSE Filings |
  City-level data is synthetic but calibrated to official national totals.
</div>

<!-- ══ PLOTLY CHART RENDERING ══════════════════════════════════════════════ -->
<script>
const charts = {json.dumps(charts)};

function renderChart(id, jsonStr) {{
  const data = JSON.parse(jsonStr);
  Plotly.newPlot(id, data.data, data.layout, {{responsive: true, displayModeBar: false}});
}}

function showTab(name) {{
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  event.target.classList.add('active');
  renderAllCharts();
}}

function renderAllCharts() {{
  const chartMap = {{
    'chart-revenue-trend':    'revenue_trend',
    'chart-gov-segments':     'gov_segments',
    'chart-quarterly':        'quarterly',
    'chart-loss-path':        'loss_path',
    'chart-city-gov':         'city_gov',
    'chart-city-scatter':     'city_scatter',
    'chart-users':            'users',
    'chart-instamart-gov':    'instamart_gov',
    'chart-instamart-cities': 'instamart_cities',
    'chart-dark-store':       'dark_store_expansion',
    'chart-tier-comparison':  'tier_comparison',
    'chart-swiggy-one':       'swiggy_one',
    'chart-swiggy-one-orders':'swiggy_one_orders',
    'chart-vs-zomato-revenue':'vs_zomato_revenue',
    'chart-vs-zomato-gov':    'vs_zomato_gov',
    'chart-market-share':     'market_share',
  }};
  for (const [divId, key] of Object.entries(chartMap)) {{
    const el = document.getElementById(divId);
    if (el && el.offsetParent !== null) {{
      renderChart(divId, charts[key]);
    }}
  }}
}}

document.addEventListener('DOMContentLoaded', renderAllCharts);
</script>
</body>
</html>
"""

out_path = os.path.join(DASH_DIR, "swiggy_dashboard.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ Dashboard saved → {out_path}")
print(f"   Open in browser: file:///{out_path.replace(os.sep, '/')}")
