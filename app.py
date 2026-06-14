import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from data.mock_data import (
    TRENDS, INVENTORY, PRICING, WHOLESALERS,
    get_forecast_data, get_sales_history, CATEGORIES
)

st.set_page_config(
    page_title="FashionIQ — Trend Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Inter:wght@300;400;500;600&family=Space+Mono&display=swap');
:root {
    --crimson: #C41E3A;
    --ink: #0A0A0A;
    --paper: #F7F5F0;
    --warm-grey: #8C8C8C;
    --rule: #D4D0C8;
    --gold: #B8964A;
}
html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #0A0A0A; }
.stApp { background: #F7F5F0; }
[data-testid="stSidebar"] { background: #0A0A0A !important; border-right: 1px solid #222; }
[data-testid="stSidebar"] * { color: #F7F5F0 !important; }
header[data-testid="stHeader"] { display: none; }
.metric-card { background: #0A0A0A; color: #F7F5F0; padding: 24px 20px; border-radius: 2px; }
.metric-card .val { font-family: 'Playfair Display', serif; font-size: 2.2rem; font-weight: 900; color: #F7F5F0; line-height: 1; margin-bottom: 4px; }
.metric-card .lbl { font-size: 0.65rem; letter-spacing: 0.15em; text-transform: uppercase; color: #8C8C8C; }
.metric-card .delta { font-size: 0.8rem; color: #C41E3A; margin-top: 6px; font-weight: 600; }
.trend-card { background: white; border-radius: 2px; padding: 20px; border-left: 4px solid #C41E3A; margin-bottom: 16px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.trend-card.medium { border-left-color: #B8964A; }
.trend-card.low { border-left-color: #8C8C8C; }
.trend-card.dead { border-left-color: #D4D0C8; }
.trend-name { font-family: 'Playfair Display', serif; font-size: 1.2rem; font-weight: 700; margin-bottom: 4px; }
.trend-meta { font-size: 0.75rem; color: #8C8C8C; margin-bottom: 8px; }
.trend-desc { font-size: 0.85rem; color: #333; line-height: 1.5; }
.urgency-badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; font-weight: 600; margin-bottom: 8px; }
.badge-high { background: #FFF0F0; color: #C41E3A; }
.badge-medium { background: #FFF8EC; color: #B8964A; }
.badge-low { background: #F5F5F5; color: #555; }
.badge-dead { background: #F0F0F0; color: #888; }
.heat-bar-wrap { margin: 10px 0 4px; }
.heat-bar-bg { background: #EEE; border-radius: 2px; height: 6px; width: 100%; }
.heat-bar-fill { height: 6px; border-radius: 2px; background: linear-gradient(90deg, #C41E3A, #FF6B6B); }
.section-eyebrow { font-size: 0.65rem; letter-spacing: 0.2em; text-transform: uppercase; color: #C41E3A; font-weight: 600; margin-bottom: 4px; }
.section-title { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 900; color: #0A0A0A; margin-bottom: 24px; border-bottom: 2px solid #0A0A0A; padding-bottom: 12px; }
.wh-card { background: white; border-radius: 2px; padding: 24px; margin-bottom: 20px; box-shadow: 0 1px 6px rgba(0,0,0,0.07); border-top: 3px solid #0A0A0A; }
.wh-name { font-family: 'Playfair Display', serif; font-size: 1.3rem; font-weight: 700; }
.wh-city { font-size: 0.8rem; color: #8C8C8C; letter-spacing: 0.05em; }
.wh-tag { display: inline-block; padding: 2px 8px; background: #0A0A0A; color: #F7F5F0; font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; border-radius: 2px; margin-right: 4px; margin-top: 4px; }
.page-masthead { background: #0A0A0A; color: #F7F5F0; padding: 28px 32px 24px; margin: -16px -16px 32px; border-bottom: 3px solid #C41E3A; }
.masthead-title { font-family: 'Playfair Display', serif; font-size: 2.8rem; font-weight: 900; letter-spacing: -0.02em; line-height: 1; }
.masthead-sub { font-size: 0.7rem; letter-spacing: 0.25em; text-transform: uppercase; color: #C41E3A; margin-top: 6px; }
.masthead-date { font-size: 0.7rem; color: #8C8C8C; letter-spacing: 0.1em; margin-top: 4px; }
.stButton > button { background: #0A0A0A !important; color: #F7F5F0 !important; border: none !important; border-radius: 2px !important; font-size: 0.75rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; font-weight: 600 !important; padding: 10px 24px !important; }
.stButton > button:hover { background: #C41E3A !important; }
.alert-box { padding: 12px 16px; border-radius: 2px; margin: 8px 0; font-size: 0.85rem; }
.alert-red { background: #FFF0F2; border-left: 3px solid #C41E3A; color: #7A0020; }
.alert-gold { background: #FFF8EC; border-left: 3px solid #B8964A; color: #7A5A00; }
.alert-green { background: #F0FFF4; border-left: 3px solid #2E7D32; color: #1B4F1E; }
.ai-msg { background: #0A0A0A; color: #F7F5F0; border-radius: 2px; padding: 16px 20px; font-size: 0.88rem; line-height: 1.6; margin-top: 12px; border-left: 3px solid #C41E3A; }
hr { border: none; border-top: 1px solid #D4D0C8; margin: 24px 0; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 0 24px;'>
        <div style='font-family: "Playfair Display", serif; font-size: 1.6rem; font-weight: 900; color: #F7F5F0;'>
            Fashion<span style='color:#C41E3A;'>IQ</span>
        </div>
        <div style='font-size: 0.6rem; letter-spacing: 0.2em; text-transform: uppercase; color: #555; margin-top: 2px;'>Trend Intelligence Platform</div>
        <hr style='border-color: #222; margin: 16px 0;'>
    </div>
    """, unsafe_allow_html=True)

    page = st.selectbox("Navigate", [
        "◆  Trend Intelligence",
        "◈  Demand Forecast",
        "◉  Stock Manager",
        "◎  Pricing Studio",
        "◇  Wholesaler Market",
        "✦  AI Advisor",
    ], label_visibility="collapsed")

    st.markdown("<hr style='border-color:#222;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.65rem; color:#555; letter-spacing:0.1em; text-transform:uppercase;'>
        Live · Hyderabad Market<br><span style='color:#C41E3A;'>● Active</span>
    </div>
    """, unsafe_allow_html=True)

# ── PAGE 1: TREND INTELLIGENCE ────────────────────────────────────────────────
if "Trend Intelligence" in page:
    st.markdown("""
    <div class='page-masthead'>
        <div class='masthead-sub'>◆ Fashion Intelligence</div>
        <div class='masthead-title'>Trend Report</div>
        <div class='masthead-date'>Hyderabad Market · June 2025 Edition</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='metric-card'><div class='val'>8</div><div class='lbl'>Active Trends</div><div class='delta'>↑ 3 new this week</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'><div class='val'>4</div><div class='lbl'>High Urgency Alerts</div><div class='delta'>Reorder recommended</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'><div class='val'>₹2.1L</div><div class='lbl'>Revenue at Risk</div><div class='delta'>From dead stock items</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='metric-card'><div class='val'>94</div><div class='lbl'>Top Trend Score</div><div class='delta'>Baggy Cargo Pants 🔥</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    col_f1, col_f2, _ = st.columns([1, 1, 3])
    with col_f1:
        cat_filter = st.selectbox("Category", CATEGORIES, key="trend_cat")
    with col_f2:
        urgency_filter = st.selectbox("Urgency", ["All", "HIGH", "MEDIUM", "LOW", "DEAD_STOCK"])

    filtered = TRENDS
    if cat_filter != "All":
        filtered = [t for t in filtered if t["category"] == cat_filter]
    if urgency_filter != "All":
        filtered = [t for t in filtered if t["urgency"] == urgency_filter]

    st.markdown("<hr>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    for i, trend in enumerate(filtered):
        col = col_a if i % 2 == 0 else col_b
        if trend["urgency"] == "HIGH":
            card_cls = ""; badge_cls = "badge-high"
        elif trend["urgency"] == "MEDIUM":
            card_cls = "medium"; badge_cls = "badge-medium"
        elif trend["urgency"] == "LOW":
            card_cls = "low"; badge_cls = "badge-low"
        else:
            card_cls = "dead"; badge_cls = "badge-dead"

        tags_html = "".join([f"<span style='background:#f0f0f0;padding:2px 8px;border-radius:20px;font-size:0.65rem;margin-right:4px;color:#555;'>{t}</span>" for t in trend["tags"]])

        with col:
            st.markdown(f"""
            <div class='trend-card {card_cls}'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                    <div>
                        <div class='trend-name'>{trend['name']}</div>
                        <div class='trend-meta'>{trend['category']} · {trend['city']} · {trend['direction']}</div>
                    </div>
                    <div style='font-size:1.6rem;font-weight:700;color:#0A0A0A;'>{trend['heat']}</div>
                </div>
                <span class='urgency-badge {badge_cls}'>{trend['urgency'].replace('_',' ')}</span>
                <div style='color:#C41E3A;font-weight:700;font-size:0.85rem;margin-bottom:8px;'>{trend['change']} demand</div>
                <div class='trend-desc'>{trend['description']}</div>
                <div class='heat-bar-wrap'>
                    <div style='font-size:0.65rem;color:#8C8C8C;margin-bottom:4px;'>TREND HEAT</div>
                    <div class='heat-bar-bg'><div class='heat-bar-fill' style='width:{trend["heat"]}%;'></div></div>
                </div>
                <div style='margin-top:10px;'>{tags_html}</div>
                <div style='font-size:0.72rem;color:#8C8C8C;margin-top:10px;'>⏱ Peak in ~{trend['peak_weeks']} weeks</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='section-eyebrow'>◆ Analytics</div><div class='section-title'>Trend Heat Comparison</div>", unsafe_allow_html=True)

    names = [t["name"] for t in TRENDS]
    heats = [t["heat"] for t in TRENDS]
    colors = ["#C41E3A" if h > 80 else "#B8964A" if h > 60 else "#8C8C8C" for h in heats]
    fig = go.Figure(go.Bar(x=heats, y=names, orientation='h', marker_color=colors, text=[f"{h}" for h in heats], textposition='outside'))
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family='Inter', size=12),
        xaxis=dict(showgrid=False, showticklabels=False, range=[0, 110]),
        yaxis=dict(showgrid=False), margin=dict(l=10, r=40, t=10, b=10), height=340)
    st.plotly_chart(fig, use_container_width=True)

# ── PAGE 2: DEMAND FORECAST ───────────────────────────────────────────────────
elif "Demand Forecast" in page:
    st.markdown("""
    <div class='page-masthead'>
        <div class='masthead-sub'>◈ Predictive Analytics</div>
        <div class='masthead-title'>Demand Forecast</div>
        <div class='masthead-date'>12-Week Outlook · Hyderabad</div>
    </div>
    """, unsafe_allow_html=True)

    data = get_forecast_data()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<div class='metric-card'><div class='val'>+41%</div><div class='lbl'>Peak Demand Surge</div><div class='delta'>Cargo Pants · W5</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='metric-card'><div class='val'>5</div><div class='lbl'>Rising Products</div><div class='delta'>Reorder now</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='metric-card'><div class='val'>1</div><div class='lbl'>Declining SKU</div><div class='delta'>Clear blazers</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='metric-card'><div class='val'>W6</div><div class='lbl'>Peak Week</div><div class='delta'>Highest across board</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-eyebrow'>◆ 12-Week Projection</div><div class='section-title'>Demand Curves</div>", unsafe_allow_html=True)

    product_sel = st.multiselect("Select Products", list(data.keys())[1:],
        default=["Baggy Cargo Pants", "Pastel Oversized Shirts", "Printed Maxi Dresses"])

    if product_sel:
        fig2 = go.Figure()
        palette = ["#C41E3A", "#0A0A0A", "#B8964A", "#555", "#2E7D32"]
        for i, prod in enumerate(product_sel):
            fig2.add_trace(go.Scatter(x=data["weeks"], y=data[prod], name=prod,
                mode='lines+markers', line=dict(color=palette[i % len(palette)], width=2.5), marker=dict(size=6)))
        fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family='Inter', size=12),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            xaxis=dict(showgrid=False, title="Week"), yaxis=dict(showgrid=True, gridcolor='#EEE', title="Units"),
            margin=dict(l=10, r=10, t=30, b=10), height=380)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='section-eyebrow'>◆ Summary</div><div class='section-title'>Demand Intelligence Table</div>", unsafe_allow_html=True)
    demand_summary = [
        {"Product": "Baggy Cargo Pants", "Avg Weekly Demand": 47, "Peak Demand": 74, "Peak Week": "W7", "Trend": "📈 Rising Fast", "Action": "🔴 Reorder Now"},
        {"Product": "Printed Maxi Dresses", "Avg Weekly Demand": 49, "Peak Demand": 70, "Peak Week": "W6", "Trend": "🔥 Viral", "Action": "🔴 Reorder Now"},
        {"Product": "Crochet Mini Skirts", "Avg Weekly Demand": 40, "Peak Demand": 68, "Peak Week": "W7", "Trend": "📈 Rising Fast", "Action": "🔴 Reorder Now"},
        {"Product": "Pastel Oversized Shirts", "Avg Weekly Demand": 43, "Peak Demand": 65, "Peak Week": "W7", "Trend": "📈 Rising", "Action": "🟡 Order Soon"},
        {"Product": "Formal Blazers", "Avg Weekly Demand": 9, "Peak Demand": 20, "Peak Week": "W1", "Trend": "📉 Declining", "Action": "🔵 Clearance"},
    ]
    st.dataframe(pd.DataFrame(demand_summary), use_container_width=True, hide_index=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='section-eyebrow'>◆ Historical</div><div class='section-title'>Last 30 Days Revenue</div>", unsafe_allow_html=True)
    hist = get_sales_history()
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=hist["date"], y=hist["revenue"], fill='tozeroy',
        fillcolor='rgba(196,30,58,0.08)', line=dict(color='#C41E3A', width=2), name="Daily Revenue"))
    fig3.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family='Inter', size=12),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#EEE', tickprefix='₹'),
        margin=dict(l=10, r=10, t=10, b=10), height=280)
    st.plotly_chart(fig3, use_container_width=True)

# ── PAGE 3: STOCK MANAGER ─────────────────────────────────────────────────────
elif "Stock Manager" in page:
    st.markdown("""
    <div class='page-masthead'>
        <div class='masthead-sub'>◉ Inventory Control</div>
        <div class='masthead-title'>Stock Manager</div>
        <div class='masthead-date'>Live Inventory · 8 SKUs</div>
    </div>
    """, unsafe_allow_html=True)

    reorder = [i for i in INVENTORY if i["status"] == "REORDER NOW"]
    dead = [i for i in INVENTORY if i["status"] == "DEAD STOCK"]
    over = [i for i in INVENTORY if i["status"] == "OVERSTOCK"]

    if reorder:
        items_str = ", ".join([i["name"].split(" - ")[0] for i in reorder])
        st.markdown(f"<div class='alert-box alert-red'>🚨 <strong>REORDER ALERT:</strong> {items_str} — running critically low.</div>", unsafe_allow_html=True)
    if dead:
        items_str = ", ".join([i["name"].split(" - ")[0] for i in dead])
        st.markdown(f"<div class='alert-box alert-gold'>⚠️ <strong>DEAD STOCK:</strong> {items_str} — consider clearance pricing.</div>", unsafe_allow_html=True)
    if over:
        items_str = ", ".join([i["name"].split(" - ")[0] for i in over])
        st.markdown(f"<div class='alert-box alert-gold'>📦 <strong>OVERSTOCK:</strong> {items_str} — pause reordering.</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    total_val = sum([i["qty"] * i["cost"] for i in INVENTORY])
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='metric-card'><div class='val'>₹{total_val//1000}K</div><div class='lbl'>Total Stock Value</div><div class='delta'>At cost price</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card'><div class='val'>{len(reorder)}</div><div class='lbl'>Reorder Alerts</div><div class='delta'>Act now</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-card'><div class='val'>{len(dead)}</div><div class='lbl'>Dead Stock SKUs</div><div class='delta'>₹{sum([i['qty']*i['cost'] for i in dead])//1000}K blocked</div></div>", unsafe_allow_html=True)
    with c4:
        fast_count = sum(1 for i in INVENTORY if i["velocity"] == "Fast")
        st.markdown(f"<div class='metric-card'><div class='val'>{fast_count}</div><div class='lbl'>Fast-Moving SKUs</div><div class='delta'>High velocity</div></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='section-eyebrow'>◆ Inventory</div><div class='section-title'>All SKUs</div>", unsafe_allow_html=True)

    cat_sel = st.selectbox("Filter by Category", CATEGORIES, key="stock_cat")
    inv_filtered = INVENTORY if cat_sel == "All" else [i for i in INVENTORY if i["category"] == cat_sel]

    for item in inv_filtered:
        stat = item["status"]
        icon = "🔴" if stat == "REORDER NOW" else "🟢" if stat == "HEALTHY" else "🟡" if stat == "OVERSTOCK" else "⚫"
        pct = min(100, int(item["qty"] / (item["reorder_point"] * 2) * 100))
        bar_color = "#C41E3A" if pct < 35 else "#B8964A" if pct < 60 else "#2E7D32"
        margin = int((item["selling_price"] - item["cost"]) / item["selling_price"] * 100)

        with st.expander(f"{icon}  {item['name']}  ·  {stat}"):
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("In Stock", f"{item['qty']} units")
            c2.metric("Reorder Point", f"{item['reorder_point']} units")
            c3.metric("Days of Stock", f"{item['days_of_stock']} days")
            c4.metric("Velocity", item['velocity'])
            c5.metric("Margin", f"{margin}%")
            st.markdown(f"""
            <div style='margin:12px 0 4px;font-size:0.7rem;color:#8C8C8C;text-transform:uppercase;'>Stock Level</div>
            <div style='background:#EEE;border-radius:2px;height:8px;width:100%;'>
                <div style='width:{pct}%;height:8px;border-radius:2px;background:{bar_color};'></div>
            </div>""", unsafe_allow_html=True)
            if stat == "REORDER NOW":
                suggest_qty = item["reorder_point"] * 3
                st.markdown(f"<div class='alert-box alert-red'>💡 Suggested reorder: <strong>{suggest_qty} units</strong></div>", unsafe_allow_html=True)
            elif stat == "DEAD STOCK":
                st.markdown(f"<div class='alert-box alert-gold'>💡 Try discount price: ₹{int(item['selling_price'] * 0.7)} (30% off)</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='section-eyebrow'>◆ Visual</div><div class='section-title'>Stock vs Reorder Point</div>", unsafe_allow_html=True)
    names = [i["sku"] for i in INVENTORY]
    qty = [i["qty"] for i in INVENTORY]
    reorder_pts = [i["reorder_point"] for i in INVENTORY]
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(name='Current Stock', x=names, y=qty,
        marker_color=['#C41E3A' if q < r else '#0A0A0A' for q, r in zip(qty, reorder_pts)]))
    fig4.add_trace(go.Scatter(name='Reorder Point', x=names, y=reorder_pts,
        mode='lines+markers', line=dict(color='#B8964A', dash='dash', width=2), marker=dict(size=8)))
    fig4.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family='Inter', size=12),
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#EEE', title="Units"),
        margin=dict(l=10, r=10, t=30, b=10), height=320)
    st.plotly_chart(fig4, use_container_width=True)

# ── PAGE 4: PRICING STUDIO ────────────────────────────────────────────────────
elif "Pricing Studio" in page:
    st.markdown("""
    <div class='page-masthead'>
        <div class='masthead-sub'>◎ Margin Intelligence</div>
        <div class='masthead-title'>Pricing Studio</div>
        <div class='masthead-date'>Market Benchmarking · Hyderabad</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='metric-card'><div class='val'>₹950</div><div class='lbl'>Avg Market Price</div><div class='delta'>Across tracked SKUs</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='metric-card'><div class='val'>5</div><div class='lbl'>Pricing Opportunities</div><div class='delta'>Price up to capture margin</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='metric-card'><div class='val'>64%</div><div class='lbl'>Avg Gross Margin</div><div class='delta'>Trending products</div></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='section-eyebrow'>◆ Analysis</div><div class='section-title'>Price Positioning</div>", unsafe_allow_html=True)

    for p in PRICING:
        opp = p["opportunity"]
        opp_color = "#C41E3A" if "UP" in opp else "#B8964A" if "Reduce" in opp else "#555"
        with st.expander(f"  {p['product']}  ·  Your Price: ₹{p['your_price']}  ·  {opp}"):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Your Price", f"₹{p['your_price']}")
            c2.metric("Market Avg", f"₹{p['market_avg']}", delta=f"{p['your_price']-p['market_avg']:+}")
            c3.metric("Suggested Price", f"₹{p['suggested']}")
            c4.metric("Gross Margin", f"{p['margin_pct']}%")
            range_span = p["high"] - p["low"]
            your_pct = int((p["your_price"] - p["low"]) / range_span * 100) if range_span else 50
            sugg_pct = int((p["suggested"] - p["low"]) / range_span * 100) if range_span else 50
            st.markdown(f"""
            <div style='margin:12px 0 4px;font-size:0.7rem;color:#8C8C8C;text-transform:uppercase;'>Market Price Range</div>
            <div style='position:relative;background:#EEE;border-radius:2px;height:10px;width:100%;'>
                <div style='position:absolute;left:{your_pct}%;top:-3px;width:4px;height:16px;background:#0A0A0A;border-radius:2px;'></div>
                <div style='position:absolute;left:{sugg_pct}%;top:-3px;width:4px;height:16px;background:#C41E3A;border-radius:2px;'></div>
            </div>
            <div style='display:flex;justify-content:space-between;font-size:0.7rem;color:#8C8C8C;margin-top:6px;'>
                <span>Low ₹{p['low']}</span><span style='color:#0A0A0A;'>■ Your price</span>
                <span style='color:#C41E3A;'>■ Suggested</span><span>High ₹{p['high']}</span>
            </div>
            <div style='margin-top:10px;padding:10px 14px;background:#F7F5F0;border-left:3px solid {opp_color};font-size:0.82rem;color:{opp_color};font-weight:600;'>
                {opp}
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='section-eyebrow'>◆ Visual</div><div class='section-title'>Margin Breakdown</div>", unsafe_allow_html=True)
    products = [p["product"] for p in PRICING]
    margins = [p["margin_pct"] for p in PRICING]
    mcolors = ["#2E7D32" if m > 60 else "#B8964A" if m > 40 else "#C41E3A" for m in margins]
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(x=products, y=margins, marker_color=mcolors,
        text=[f"{m}%" for m in margins], textposition='outside'))
    fig5.add_hline(y=50, line_dash="dash", line_color="#B8964A", annotation_text="Min target 50%")
    fig5.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family='Inter', size=11),
        yaxis=dict(showgrid=True, gridcolor='#EEE', title="Gross Margin %", range=[0, 90]),
        xaxis=dict(showgrid=False, tickangle=-20), margin=dict(l=10, r=10, t=20, b=80), height=340)
    st.plotly_chart(fig5, use_container_width=True)

# ── PAGE 5: WHOLESALER MARKETPLACE ───────────────────────────────────────────
elif "Wholesaler Market" in page:
    st.markdown("""
    <div class='page-masthead'>
        <div class='masthead-sub'>◇ Supplier Network</div>
        <div class='masthead-title'>Wholesaler Marketplace</div>
        <div class='masthead-date'>Verified Suppliers · Pan India</div>
    </div>
    """, unsafe_allow_html=True)

    col_s, col_c, col_m = st.columns([2, 1, 1])
    with col_s:
        search = st.text_input("Search suppliers or products", placeholder="e.g. cargo pants, Surat…")
    with col_c:
        city_filter = st.selectbox("City", ["All", "Surat", "Jaipur", "Mumbai", "Tirupur"])
    with col_m:
        cat_filter_wh = st.selectbox("Category", CATEGORIES, key="wh_cat")

    st.markdown("<hr>", unsafe_allow_html=True)

    for wh in WHOLESALERS:
        if city_filter != "All" and wh["city"] != city_filter:
            continue
        if search and search.lower() not in wh["name"].lower() and not any(search.lower() in p["name"].lower() for p in wh["products"]):
            continue
        tags_html = "".join([f"<span class='wh-tag'>{t}</span>" for t in wh["tags"]])
        stars = "★" * int(wh["rating"]) + "☆" * (5 - int(wh["rating"]))
        st.markdown(f"""
        <div class='wh-card'>
            <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                <div>
                    <div class='wh-name'>{wh['name']}</div>
                    <div class='wh-city'>📍 {wh['city']} · {wh['speciality']}</div>
                    <div style='margin-top:6px;'>{tags_html}</div>
                </div>
                <div style='text-align:right;'>
                    <div style='color:#B8964A;font-size:1.1rem;'>{stars}</div>
                    <div style='font-size:0.75rem;color:#555;'>{wh['rating']}/5.0 ✅ Verified</div>
                    <div style='font-size:0.72rem;color:#8C8C8C;margin-top:4px;'>Min order: ₹{wh['min_order_value']//1000}K</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        for prod in wh["products"]:
            if cat_filter_wh != "All" and prod["category"] != cat_filter_wh:
                continue
            with st.expander(f"   {prod['name']}  ·  MOQ {prod['moq']} units  ·  ₹{prod['price_per_unit']}/unit"):
                c1, c2, c3, c4, c5 = st.columns(5)
                c1.metric("Price/Unit", f"₹{prod['price_per_unit']}")
                c2.metric("MOQ", f"{prod['moq']} units")
                c3.metric("Fabric", prod["fabric"])
                c4.metric("Lead Time", f"{prod['lead_days']} days")
                c5.metric("Colors", f"{prod['colors']} options")
                total_cost = prod["price_per_unit"] * prod["moq"]
                st.markdown(f"<div style='background:#F7F5F0;padding:10px 16px;border-radius:2px;font-size:0.82rem;margin-top:8px;'>Minimum Order: {prod['moq']} units × ₹{prod['price_per_unit']} = <strong>₹{total_cost:,}</strong> · Sizes: {prod['sizes']}</div>", unsafe_allow_html=True)
                col_btn1, col_btn2, _ = st.columns([1, 1, 4])
                with col_btn1:
                    if st.button(f"📩 Enquire", key=f"enq_{wh['id']}_{prod['name'][:8]}"):
                        st.success(f"✅ Enquiry sent to {wh['name']}!")
                with col_btn2:
                    if st.button(f"🛒 Order", key=f"ord_{wh['id']}_{prod['name'][:8]}"):
                        st.success(f"🎉 Order placed with {wh['name']}!")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='section-eyebrow'>◆ Compare</div><div class='section-title'>Supplier Ratings</div>", unsafe_allow_html=True)
    wh_names = [w["name"].split(" ")[0] + " " + w["name"].split(" ")[1] for w in WHOLESALERS]
    wh_ratings = [w["rating"] for w in WHOLESALERS]
    fig6 = go.Figure()
    fig6.add_trace(go.Bar(x=wh_names, y=wh_ratings, marker_color='#0A0A0A',
        text=[f"{r}" for r in wh_ratings], textposition='outside'))
    fig6.add_hline(y=4.5, line_dash="dot", line_color="#C41E3A", annotation_text="Top tier")
    fig6.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family='Inter', size=12),
        yaxis=dict(range=[0, 5.5], showgrid=True, gridcolor='#EEE', title="Rating"),
        xaxis=dict(showgrid=False), margin=dict(l=10, r=10, t=20, b=10), height=280)
    st.plotly_chart(fig6, use_container_width=True)

# ── PAGE 6: AI ADVISOR ────────────────────────────────────────────────────────
elif "AI Advisor" in page:
    st.markdown("""
    <div class='page-masthead'>
        <div class='masthead-sub'>✦ Powered by Claude AI</div>
        <div class='masthead-title'>AI Fashion Advisor</div>
        <div class='masthead-date'>Your personal inventory strategist</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:white;border-radius:2px;padding:20px 24px;margin-bottom:20px;border-left:4px solid #0A0A0A;'>
        <div style='font-family:"Playfair Display",serif;font-size:1rem;font-weight:700;margin-bottom:6px;'>Ask me anything about your fashion business</div>
        <div style='font-size:0.82rem;color:#555;'>Get AI-powered advice on trends, stock, pricing, and suppliers.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:#8C8C8C;margin-bottom:10px;'>Quick Questions</div>", unsafe_allow_html=True)
    quick_qs = ["What should I reorder this week?", "Which dead stock should I clear?", "How can I improve my margins?", "Which wholesaler for cargo pants?", "What trends to stock next month?"]
    cols = st.columns(3)
    for i, q in enumerate(quick_qs[:3]):
        with cols[i]:
            if st.button(q, key=f"quick_{i}"):
                st.session_state["ai_input"] = q
    cols2 = st.columns(2)
    for i, q in enumerate(quick_qs[3:]):
        with cols2[i]:
            if st.button(q, key=f"quick2_{i}"):
                st.session_state["ai_input"] = q

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    default_val = st.session_state.get("ai_input", "")
    user_input = st.text_area("Your question", value=default_val, height=90,
        placeholder="e.g. Which products should I prioritise buying this week?")

    if st.button("✦ Get AI Advice", key="ai_submit"):
        if user_input.strip():
            with st.spinner("Analysing your business data…"):
                lower_q = user_input.lower()
                if "reorder" in lower_q or "buy" in lower_q or "stock" in lower_q:
                    advice = "🔴 **Priority reorders this week:** Baggy Cargo Pants (only 4 days of stock — order 90 units from Rajesh Textiles at ₹320/unit = ₹28,800), Crochet Mini Skirts (3 days left — order 75 units from Femina Fashion House), and Printed Maxi Dresses (order 120 units immediately). These are your highest-velocity items with peak demand in 5–7 weeks."
                elif "dead" in lower_q or "clear" in lower_q or "blazer" in lower_q:
                    advice = "📦 **Dead stock action plan:** Your 78 Straight Blazers are your biggest risk — ₹69,420 tied up at cost. Run a 30% off flash sale immediately (₹1,049 from ₹1,499). Push on Instagram with a '72-hour offer'. At 10 units/week you'll clear in ~8 weeks and recover ₹81,822. Don't reorder under any circumstances."
                elif "margin" in lower_q or "profit" in lower_q or "price" in lower_q:
                    advice = "💹 **Margin improvement:** Price up Baggy Cargo Pants to ₹1,399, Crochet Skirts to ₹899, and Maxi Dresses to ₹1,649 — all below market average right now. Combined on expected monthly volume, that's ~₹18,000 additional margin at zero extra cost."
                elif "wholesaler" in lower_q or "supplier" in lower_q or "cargo" in lower_q:
                    advice = "🏭 **Best for cargo pants:** Rajesh Textiles & Exports in Surat — rated 4.8/5, 14 years experience, MOQ 50 units at ₹320/unit. Lead time is 7 days which fits your 4-day stock emergency. Order immediately and request express dispatch."
                elif "trend" in lower_q or "next month" in lower_q:
                    advice = "📈 **Next month priorities:** Double down on Crochet Mini Skirts (peaking in 3 weeks, 71% margin), Printed Maxi Dresses (viral, +29% demand), and start stocking Ethnic Co-ord Sets ahead of the festive season. Avoid restocking Blazers — that category is cooling citywide."
                else:
                    advice = "📊 **Strategic advice:** Your immediate priority is restocking the 4 fast-moving items before they stock out. Baggy Cargo Pants and Maxi Dresses are in viral territory — every day out of stock is lost revenue. Simultaneously, start clearing your Blazers with a discount campaign. Your margin profile is strong at 64% on trending items."
                st.markdown(f"<div class='ai-msg'>✦ {advice}</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='section-eyebrow'>◆ Auto-Generated</div><div class='section-title'>This Week's Intelligence Digest</div>", unsafe_allow_html=True)
    digests = [
        ("🔴 URGENT", "#C41E3A", "Stock out risk in 4 days", "Baggy Cargo Pants, Crochet Mini Skirts, and Maxi Dresses will be out of stock before weekend. Contact Rajesh Textiles and Femina today."),
        ("💰 OPPORTUNITY", "#2E7D32", "₹18K margin on the table", "Raising prices on 5 products to market average adds ₹18,000/month at current volume. No extra procurement needed."),
        ("📦 ACTION", "#B8964A", "₹70K in dead stock", "78 blazers sitting unsold for 90+ days. A 30% clearance campaign can recover ₹81K and free up shelf space for trending items."),
        ("📈 TREND", "#0A0A0A", "Crochet season is now", "Crochet Mini Skirts peaking in 3 weeks. You have only 6 units. This is your highest-margin item at 71% — don't miss this window."),
    ]
    for label, color, title, body in digests:
        st.markdown(f"""
        <div style='background:white;border-radius:2px;padding:16px 20px;margin-bottom:12px;border-left:4px solid {color};'>
            <div style='font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;color:{color};font-weight:700;margin-bottom:4px;'>{label}</div>
            <div style='font-family:"Playfair Display",serif;font-size:1rem;font-weight:700;margin-bottom:6px;'>{title}</div>
            <div style='font-size:0.83rem;color:#444;line-height:1.5;'>{body}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<hr><div style='text-align:center;padding:16px 0;font-size:0.65rem;color:#8C8C8C;letter-spacing:0.15em;text-transform:uppercase;'>FashionIQ · Trend Intelligence Platform · Hyderabad</div>", unsafe_allow_html=True)
