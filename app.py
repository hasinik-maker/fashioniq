import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from data.mock_data import (
    TRENDS, INVENTORY, PRICING, WHOLESALERS,
    get_forecast_data, get_sales_history, get_revenue_data,
    CATEGORIES, USERS, MESSAGES, FASHION_NEWS, AUDIENCE_DATA,
    check_illegal_content, get_ai_response
)

st.set_page_config(
    page_title="Trendora",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #fff; }
[data-testid="stSidebar"] { display: none; }
header[data-testid="stHeader"] { display: none; }
[data-testid="stAppViewContainer"] { padding-top: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── TOP NAV ── */
.topnav {
    background: #000;
    width: 100%;
    padding: 0 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 56px;
    position: sticky;
    top: 0;
    z-index: 999;
    border-bottom: 2px solid #C41E3A;
}
.topnav-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 900;
    color: #fff;
    letter-spacing: -0.02em;
}
.topnav-logo span { color: #C41E3A; }
.topnav-links {
    display: flex;
    gap: 6px;
    align-items: center;
}
.nav-btn {
    background: transparent;
    border: none;
    color: #aaa;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 600;
    cursor: pointer;
    padding: 6px 14px;
    border-radius: 2px;
    transition: all 0.2s;
    font-family: 'Inter', sans-serif;
}
.nav-btn:hover, .nav-btn.active { background: #C41E3A; color: #fff; }
.topnav-user {
    font-size: 0.72rem;
    color: #aaa;
    letter-spacing: 0.05em;
}
.topnav-user strong { color: #fff; }

/* ── PAGE WRAPPER ── */
.page-wrap { padding: 32px 40px; background: #fff; min-height: 100vh; }

/* ── MASTHEAD ── */
.masthead {
    background: #000;
    color: #fff;
    padding: 40px 40px 32px;
    border-bottom: 3px solid #C41E3A;
    margin-bottom: 32px;
}
.masthead-eyebrow { font-size: 0.65rem; letter-spacing: 0.25em; text-transform: uppercase; color: #C41E3A; margin-bottom: 8px; }
.masthead-title { font-family: 'Playfair Display', serif; font-size: 3rem; font-weight: 900; color: #fff; line-height: 1; }
.masthead-sub { font-size: 0.8rem; color: #aaa; margin-top: 8px; letter-spacing: 0.05em; }

/* ── METRIC CARDS ── */
.metric-card { background: #000; padding: 24px 20px; border-radius: 2px; margin-bottom: 8px; }
.metric-val { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 900; color: #fff; line-height: 1; }
.metric-lbl { font-size: 0.62rem; letter-spacing: 0.15em; text-transform: uppercase; color: #888; margin-top: 4px; }
.metric-delta { font-size: 0.78rem; color: #C41E3A; margin-top: 6px; font-weight: 600; }

/* ── TREND CARDS ── */
.trend-card { background: #fff; border-left: 4px solid #C41E3A; padding: 20px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-radius: 2px; }
.trend-card.medium { border-left-color: #B8964A; }
.trend-card.low { border-left-color: #555; }
.trend-card.dead { border-left-color: #ddd; }
.trend-name { font-family: 'Playfair Display', serif; font-size: 1.15rem; font-weight: 700; color: #000; margin-bottom: 4px; }
.trend-meta { font-size: 0.73rem; color: #555; margin-bottom: 8px; }
.trend-desc { font-size: 0.83rem; color: #222; line-height: 1.55; }
.heat-bg { background: #eee; height: 6px; border-radius: 3px; margin: 10px 0 4px; }
.heat-fill { height: 6px; border-radius: 3px; background: linear-gradient(90deg, #C41E3A, #ff6b6b); }
.badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; font-weight: 700; margin-bottom: 8px; }
.badge-high { background: #fff0f0; color: #C41E3A; }
.badge-medium { background: #fff8ec; color: #B8964A; }
.badge-low { background: #f5f5f5; color: #555; }
.badge-dead { background: #f0f0f0; color: #888; }

/* ── SECTION TITLES ── */
.eyebrow { font-size: 0.62rem; letter-spacing: 0.2em; text-transform: uppercase; color: #C41E3A; font-weight: 700; margin-bottom: 4px; }
.section-title { font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 900; color: #000; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 24px; }

/* ── ALERTS ── */
.alert { padding: 12px 16px; border-radius: 2px; margin: 8px 0; font-size: 0.84rem; color: #000; }
.alert-red { background: #fff0f2; border-left: 3px solid #C41E3A; }
.alert-gold { background: #fff8ec; border-left: 3px solid #B8964A; }
.alert-green { background: #f0fff4; border-left: 3px solid #2E7D32; }
.alert-black { background: #f5f5f5; border-left: 3px solid #000; }

/* ── WHOLESALER CARDS ── */
.wh-card { background: #fff; border-top: 3px solid #000; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.07); }
.wh-name { font-family: 'Playfair Display', serif; font-size: 1.2rem; font-weight: 700; color: #000; }
.wh-meta { font-size: 0.78rem; color: #555; margin-top: 2px; }
.wh-tag { display: inline-block; padding: 2px 8px; background: #000; color: #fff; font-size: 0.58rem; letter-spacing: 0.1em; text-transform: uppercase; border-radius: 2px; margin: 2px 2px 0 0; }

/* ── NEWS CARDS ── */
.news-card { background: #fff; border-bottom: 1px solid #eee; padding: 16px 0; }
.news-headline { font-family: 'Playfair Display', serif; font-size: 1rem; font-weight: 700; color: #000; margin-bottom: 4px; }
.news-meta { font-size: 0.7rem; color: #888; margin-bottom: 6px; }
.news-body { font-size: 0.82rem; color: #333; line-height: 1.5; }

/* ── CHAT ── */
.chat-wrap { background: #f9f9f9; border-radius: 4px; padding: 20px; min-height: 300px; margin-bottom: 16px; }
.chat-msg-user { background: #000; color: #fff; border-radius: 16px 16px 4px 16px; padding: 10px 16px; margin: 8px 0 8px auto; max-width: 75%; font-size: 0.85rem; width: fit-content; margin-left: auto; }
.chat-msg-bot { background: #fff; color: #000; border-radius: 16px 16px 16px 4px; padding: 10px 16px; margin: 8px 0; max-width: 75%; font-size: 0.85rem; border: 1px solid #eee; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.chat-sender { font-size: 0.65rem; color: #888; margin-bottom: 2px; }

/* ── LOGIN ── */
.login-wrap { max-width: 440px; margin: 80px auto; padding: 48px 40px; background: #fff; box-shadow: 0 4px 32px rgba(0,0,0,0.1); border-top: 4px solid #C41E3A; }
.login-logo { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 900; color: #000; text-align: center; margin-bottom: 4px; }
.login-logo span { color: #C41E3A; }
.login-sub { font-size: 0.72rem; letter-spacing: 0.15em; text-transform: uppercase; color: #888; text-align: center; margin-bottom: 32px; }

/* ── SAFETY BANNER ── */
.safety-banner { background: #C41E3A; color: #fff; padding: 12px 20px; border-radius: 2px; font-size: 0.85rem; font-weight: 600; margin: 12px 0; }

/* ── BUTTONS ── */
.stButton > button { background: #000 !important; color: #fff !important; border: none !important; border-radius: 2px !important; font-size: 0.72rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; font-weight: 700 !important; padding: 10px 24px !important; transition: all 0.2s !important; }
.stButton > button:hover { background: #C41E3A !important; }

/* ── INPUTS ── */
.stTextInput > div > div > input { border: 1px solid #ddd !important; border-radius: 2px !important; font-family: 'Inter', sans-serif !important; color: #000 !important; }
.stTextArea > div > div > textarea { border: 1px solid #ddd !important; border-radius: 2px !important; font-family: 'Inter', sans-serif !important; color: #000 !important; }
.stSelectbox > div { border-radius: 2px !important; color: #000 !important; }

/* ── DIVIDER ── */
hr { border: none; border-top: 1px solid #eee; margin: 24px 0; }

/* ── INVENTORY TABLE ── */
.inv-row { display: flex; justify-content: space-between; align-items: center; padding: 14px 0; border-bottom: 1px solid #f0f0f0; }
.inv-name { font-weight: 600; font-size: 0.88rem; color: #000; }
.inv-meta { font-size: 0.73rem; color: #555; margin-top: 2px; }
.status-red { color: #C41E3A; font-weight: 700; font-size: 0.72rem; }
.status-green { color: #2E7D32; font-weight: 700; font-size: 0.72rem; }
.status-gold { color: #B8964A; font-weight: 700; font-size: 0.72rem; }
.status-grey { color: #888; font-weight: 700; font-size: 0.72rem; }

/* image upload area */
.img-card { border: 1px solid #eee; border-radius: 4px; overflow: hidden; margin-bottom: 12px; }
.img-caption { font-size: 0.75rem; color: #555; padding: 8px 12px; background: #fafafa; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════════════════
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "page" not in st.session_state:
    st.session_state.page = "Trends"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "messages" not in st.session_state:
    st.session_state.messages = list(MESSAGES)
if "pinterest_images" not in st.session_state:
    st.session_state.pinterest_images = []

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    st.markdown("""
    <div style='background:#000;padding:20px 40px;border-bottom:2px solid #C41E3A;'>
        <div style='font-family:"Playfair Display",serif;font-size:1.4rem;font-weight:900;color:#fff;'>
            Trend<span style='color:#C41E3A;'>ora</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 1.2, 1])
    with col_m:
        st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='login-wrap'>
            <div class='login-logo'>Trend<span>ora</span></div>
            <div class='login-sub'>Fashion Intelligence Platform</div>
        </div>
        """, unsafe_allow_html=True)

        role = st.selectbox("I am a", ["Buyer — I want to purchase stock", "Seller — I want to sell wholesale"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        st.markdown("""
        <div style='background:#f9f9f9;padding:12px 16px;border-radius:2px;font-size:0.75rem;color:#555;margin:8px 0 16px;'>
            <strong style='color:#000;'>Demo accounts:</strong><br>
            Buyer: <code>buyer1</code> / <code>buy123</code><br>
            Seller: <code>seller1</code> / <code>sell123</code>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Sign In →", key="login_btn"):
            if username in USERS and USERS[username]["password"] == password:
                user_role = USERS[username]["role"]
                selected_role = "buyer" if "Buyer" in role else "seller"
                if user_role == selected_role or user_role == "admin":
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = user_role
                    st.session_state.page = "Trends"
                    st.rerun()
                else:
                    st.error("Role does not match. Please select the correct role.")
            else:
                st.error("Incorrect username or password.")

        st.markdown("""
        <div style='text-align:center;margin-top:16px;font-size:0.72rem;color:#888;'>
            By signing in you agree to Trendora's Terms of Service.<br>
            All activity is monitored for illegal content.
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# TOP NAV (shown after login)
# ══════════════════════════════════════════════════════════════════════════════
user_info = USERS[st.session_state.username]
role = st.session_state.role

if role == "buyer":
    nav_items = ["Trends", "Forecast", "My Stock", "Pricing", "Marketplace", "Messages", "AI Advisor", "News"]
elif role == "seller":
    nav_items = ["My Products", "Orders", "My Stock", "Pricing", "Messages", "AI Advisor", "News"]
else:
    nav_items = ["Trends", "Forecast", "My Stock", "Pricing", "Marketplace", "Messages", "AI Advisor", "News"]

nav_html = "".join([
    f"<button class='nav-btn {'active' if st.session_state.page == item else ''}' "
    f"onclick=\"window.location.href='?page={item}'\">{item}</button>"
    for item in nav_items
])

st.markdown(f"""
<div class='topnav'>
    <div class='topnav-logo'>Trend<span>ora</span></div>
    <div class='topnav-links'>{nav_html}</div>
    <div class='topnav-user'>
        <strong>{user_info['name']}</strong> · {role.upper()}
    </div>
</div>
""", unsafe_allow_html=True)

col_nav = st.columns(len(nav_items) + 1)
for i, item in enumerate(nav_items):
    with col_nav[i]:
        if st.button(item, key=f"nav_{item}"):
            st.session_state.page = item
            st.rerun()
with col_nav[-1]:
    if st.button("Sign Out", key="signout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.session_state.page = "Trends"
        st.rerun()

page = st.session_state.page

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: TRENDS
# ══════════════════════════════════════════════════════════════════════════════
if page == "Trends":
    st.markdown("""
    <div class='masthead'>
        <div class='masthead-eyebrow'>◆ Live Intelligence</div>
        <div class='masthead-title'>Trend Report</div>
        <div class='masthead-sub'>Hyderabad Market · June 2025 · Updated Daily</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<div class='metric-card'><div class='metric-val'>8</div><div class='metric-lbl'>Active Trends</div><div class='metric-delta'>↑ 3 new this week</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='metric-card'><div class='metric-val'>4</div><div class='metric-lbl'>Urgent Alerts</div><div class='metric-delta'>Reorder now</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='metric-card'><div class='metric-val'>94</div><div class='metric-lbl'>Top Heat Score</div><div class='metric-delta'>Cargo Pants 🔥</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='metric-card'><div class='metric-val'>₹2.1L</div><div class='metric-lbl'>Revenue at Risk</div><div class='metric-delta'>Dead stock items</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>◆ Pinterest Inspiration Board</div>", unsafe_allow_html=True)

    with st.expander("➕ Add Pinterest Images"):
        tab1, tab2 = st.tabs(["Paste Link", "Upload File"])
        with tab1:
            pin_url = st.text_input("Paste Pinterest image link", placeholder="https://i.pinimg.com/...")
            pin_caption = st.text_input("Caption (optional)", placeholder="e.g. Cargo pants inspo")
            if st.button("Add Image", key="add_pin"):
                if pin_url:
                    flagged = check_illegal_content(pin_url + " " + pin_caption)
                    if flagged:
                        st.markdown(f"<div class='safety-banner'>🚫 Content flagged: {', '.join(flagged)}. Not allowed.</div>", unsafe_allow_html=True)
                    else:
                        st.session_state.pinterest_images.append({"url": pin_url, "caption": pin_caption, "type": "link"})
                        st.success("Image added!")
        with tab2:
            uploaded = st.file_uploader("Upload image", type=["jpg", "jpeg", "png", "webp"])
            up_caption = st.text_input("Caption", placeholder="e.g. Summer inspo", key="up_cap")
            if st.button("Upload", key="upload_btn") and uploaded:
                st.session_state.pinterest_images.append({"url": uploaded, "caption": up_caption, "type": "upload"})
                st.success("Image uploaded!")

    if st.session_state.pinterest_images:
        img_cols = st.columns(4)
        for i, img in enumerate(st.session_state.pinterest_images):
            with img_cols[i % 4]:
                try:
                    if img["type"] == "link":
                        st.markdown(f"<div class='img-card'><img src='{img['url']}' style='width:100%;'><div class='img-caption'>{img['caption']}</div></div>", unsafe_allow_html=True)
                    else:
                        st.image(img["url"], caption=img["caption"], use_column_width=True)
                except:
                    pass

    st.markdown("<hr>", unsafe_allow_html=True)
    cf1, cf2, _ = st.columns([1, 1, 3])
    with cf1:
        cat_f = st.selectbox("Category", CATEGORIES, key="t_cat")
    with cf2:
        urg_f = st.selectbox("Urgency", ["All", "HIGH", "MEDIUM", "LOW", "DEAD_STOCK"], key="t_urg")

    filtered = [t for t in TRENDS if (cat_f == "All" or t["category"] == cat_f) and (urg_f == "All" or t["urgency"] == urg_f)]

    col_a, col_b = st.columns(2)
    for i, trend in enumerate(filtered):
        col = col_a if i % 2 == 0 else col_b
        if trend["urgency"] == "HIGH": cc, bc = "", "badge-high"
        elif trend["urgency"] == "MEDIUM": cc, bc = "medium", "badge-medium"
        elif trend["urgency"] == "LOW": cc, bc = "low", "badge-low"
        else: cc, bc = "dead", "badge-dead"
        tags = "".join([f"<span style='background:#f0f0f0;padding:2px 8px;border-radius:20px;font-size:0.62rem;margin-right:4px;color:#333;'>{t}</span>" for t in trend["tags"]])
        with col:
            st.markdown(f"""
            <div class='trend-card {cc}'>
                <div style='display:flex;justify-content:space-between;'>
                    <div>
                        <div class='trend-name'>{trend['name']}</div>
                        <div class='trend-meta'>{trend['category']} · {trend['city']} · {trend['direction']}</div>
                    </div>
                    <div style='font-size:1.8rem;font-weight:900;color:#000;'>{trend['heat']}</div>
                </div>
                <span class='badge {bc}'>{trend['urgency'].replace('_',' ')}</span>
                <div style='color:#C41E3A;font-weight:700;font-size:0.85rem;margin-bottom:8px;'>{trend['change']} demand</div>
                <div class='trend-desc'>{trend['description']}</div>
                <div style='margin:10px 0 4px;font-size:0.62rem;color:#888;text-transform:uppercase;letter-spacing:0.1em;'>Trend Heat</div>
                <div class='heat-bg'><div class='heat-fill' style='width:{trend["heat"]}%'></div></div>
                <div style='margin-top:10px;'>{tags}</div>
                <div style='font-size:0.7rem;color:#555;margin-top:8px;'>⏱ Peak in ~{trend['peak_weeks']} weeks</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>◆ Analytics</div><div class='section-title'>Trend Heat Comparison</div>", unsafe_allow_html=True)
    names = [t["name"] for t in TRENDS]
    heats = [t["heat"] for t in TRENDS]
    bar_colors = ["#C41E3A" if h > 80 else "#B8964A" if h > 60 else "#555" for h in heats]
    fig = go.Figure(go.Bar(x=heats, y=names, orientation='h', marker_color=bar_colors,
        text=heats, textposition='outside', textfont=dict(color='#000')))
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white',
        font=dict(family='Inter', size=12, color='#000'),
        xaxis=dict(showgrid=False, showticklabels=False, range=[0, 115]),
        yaxis=dict(showgrid=False), margin=dict(l=10, r=40, t=10, b=10), height=340)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: FORECAST
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Forecast":
    st.markdown("""
    <div class='masthead'>
        <div class='masthead-eyebrow'>◈ Predictive Analytics</div>
        <div class='masthead-title'>Demand Forecast</div>
        <div class='masthead-sub'>12-Week Outlook · Hyderabad Market</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)

    data = get_forecast_data()
    rev = get_revenue_data()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<div class='metric-card'><div class='metric-val'>+41%</div><div class='metric-lbl'>Peak Demand Surge</div><div class='metric-delta'>Cargo Pants · W5</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='metric-card'><div class='metric-val'>₹2.45L</div><div class='metric-lbl'>June Revenue</div><div class='metric-delta'>↑ 24% vs target</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='metric-card'><div class='metric-val'>198</div><div class='metric-lbl'>Units Sold (June)</div><div class='metric-delta'>Best month ever</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='metric-card'><div class='metric-val'>W6</div><div class='metric-lbl'>Peak Week</div><div class='metric-delta'>Highest demand point</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>◆ Revenue vs Target</div><div class='section-title'>Monthly Performance</div>", unsafe_allow_html=True)

    fig_rev = go.Figure()
    fig_rev.add_trace(go.Bar(x=rev["months"], y=rev["revenue"], name="Actual Revenue",
        marker_color="#000", text=[f"₹{v//1000}K" for v in rev["revenue"]], textposition='outside', textfont=dict(color='#000')))
    fig_rev.add_trace(go.Scatter(x=rev["months"], y=rev["target"], name="Target",
        line=dict(color="#C41E3A", dash="dash", width=2), mode='lines+markers', marker=dict(size=8)))
    fig_rev.update_layout(plot_bgcolor='white', paper_bgcolor='white',
        font=dict(family='Inter', size=12, color='#000'),
        legend=dict(orientation='h', y=1.1),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', tickprefix='₹', title="Revenue"),
        xaxis=dict(showgrid=False),
        margin=dict(l=10, r=10, t=30, b=10), height=320)
    st.plotly_chart(fig_rev, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>◆ 12-Week Projection</div><div class='section-title'>Demand Curves</div>", unsafe_allow_html=True)

    prod_sel = st.multiselect("Products", list(data.keys())[1:],
        default=["Baggy Cargo Pants", "Printed Maxi Dresses", "Crochet Mini Skirts"])

    if prod_sel:
        palette = ["#C41E3A", "#000", "#B8964A", "#2E7D32", "#555"]
        fig2 = go.Figure()
        for i, prod in enumerate(prod_sel):
            fig2.add_trace(go.Scatter(x=data["weeks"], y=data[prod], name=prod,
                mode='lines+markers', line=dict(color=palette[i % len(palette)], width=2.5), marker=dict(size=6)))
        fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white',
            font=dict(family='Inter', size=12, color='#000'),
            legend=dict(orientation='h', y=1.1),
            xaxis=dict(showgrid=False, title="Week"),
            yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title="Units"),
            margin=dict(l=10, r=10, t=30, b=10), height=360)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>◆ Audience Intelligence</div><div class='section-title'>Who Is Buying</div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        fig_age = go.Figure(go.Pie(
            labels=list(AUDIENCE_DATA["age_groups"].keys()),
            values=list(AUDIENCE_DATA["age_groups"].values()),
            hole=0.5,
            marker_colors=["#000", "#C41E3A", "#B8964A", "#555", "#aaa"]
        ))
        fig_age.update_layout(title=dict(text="Age Groups", font=dict(size=14, color='#000')),
            paper_bgcolor='white', font=dict(color='#000'), margin=dict(l=10, r=10, t=40, b=10), height=280)
        st.plotly_chart(fig_age, use_container_width=True)

    with col_b:
        fig_city = go.Figure(go.Pie(
            labels=list(AUDIENCE_DATA["cities"].keys()),
            values=list(AUDIENCE_DATA["cities"].values()),
            hole=0.5,
            marker_colors=["#C41E3A", "#000", "#B8964A", "#555", "#aaa"]
        ))
        fig_city.update_layout(title=dict(text="Top Cities", font=dict(size=14, color='#000')),
            paper_bgcolor='white', font=dict(color='#000'), margin=dict(l=10, r=10, t=40, b=10), height=280)
        st.plotly_chart(fig_city, use_container_width=True)

    st.markdown("<div class='alert alert-black'>👥 <strong>Key insight:</strong> 68% of your buyers are women aged 18-34 based in Hyderabad. Stock products that appeal to this segment — Crochet Skirts, Maxi Dresses, and Co-ord Sets are your highest-conversion categories with this audience.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MY STOCK
# ══════════════════════════════════════════════════════════════════════════════
elif page == "My Stock":
    st.markdown("""
    <div class='masthead'>
        <div class='masthead-eyebrow'>◉ Inventory Control</div>
        <div class='masthead-title'>My Stock</div>
        <div class='masthead-sub'>Live Inventory · 8 SKUs · All alerts auto-generated</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)

    reorder = [i for i in INVENTORY if i["status"] == "REORDER NOW"]
    dead = [i for i in INVENTORY if i["status"] == "DEAD STOCK"]
    over = [i for i in INVENTORY if i["status"] == "OVERSTOCK"]

    if reorder:
        st.markdown(f"<div class='alert alert-red'>🚨 <strong>REORDER NOW:</strong> {', '.join([i['name'].split(' - ')[0] for i in reorder])} — critically low stock.</div>", unsafe_allow_html=True)
    if dead:
        st.markdown(f"<div class='alert alert-gold'>⚠️ <strong>DEAD STOCK:</strong> {', '.join([i['name'].split(' - ')[0] for i in dead])} — 90+ days unsold. Start clearance.</div>", unsafe_allow_html=True)
    if over:
        st.markdown(f"<div class='alert alert-gold'>📦 <strong>OVERSTOCK:</strong> {', '.join([i['name'].split(' - ')[0] for i in over])} — pause reordering.</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    total_val = sum(i["qty"] * i["cost"] for i in INVENTORY)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='metric-card'><div class='metric-val'>₹{total_val//1000}K</div><div class='metric-lbl'>Total Stock Value</div><div class='metric-delta'>At cost price</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card'><div class='metric-val'>{len(reorder)}</div><div class='metric-lbl'>Reorder Alerts</div><div class='metric-delta'>Urgent action needed</div></div>", unsafe_allow_html=True)
    with c3:
        dead_val = sum(i['qty']*i['cost'] for i in dead)
        st.markdown(f"<div class='metric-card'><div class='metric-val'>₹{dead_val//1000}K</div><div class='metric-lbl'>Blocked in Dead Stock</div><div class='metric-delta'>Run clearance now</div></div>", unsafe_allow_html=True)
    with c4:
        fast = sum(1 for i in INVENTORY if i["velocity"] == "Fast")
        st.markdown(f"<div class='metric-card'><div class='metric-val'>{fast}</div><div class='metric-lbl'>Fast-Moving SKUs</div><div class='metric-delta'>High demand velocity</div></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>◆ All SKUs</div><div class='section-title'>Inventory Dashboard</div>", unsafe_allow_html=True)

    cat_s = st.selectbox("Filter", CATEGORIES, key="s_cat")
    inv_f = INVENTORY if cat_s == "All" else [i for i in INVENTORY if i["category"] == cat_s]

    for item in inv_f:
        s = item["status"]
        icon = "🔴" if s == "REORDER NOW" else "🟢" if s == "HEALTHY" else "🟡" if s == "OVERSTOCK" else "⚫"
        pct = min(100, int(item["qty"] / max(item["reorder_point"] * 2, 1) * 100))
        bc = "#C41E3A" if pct < 35 else "#B8964A" if pct < 60 else "#2E7D32"
        margin = int((item["selling_price"] - item["cost"]) / item["selling_price"] * 100)
        trend_score = item["trend_alignment"]

        with st.expander(f"{icon}  {item['name']}  ·  {s}  ·  Trend Score: {trend_score}/100"):
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("In Stock", f"{item['qty']} units")
            c2.metric("Reorder Point", f"{item['reorder_point']} units")
            c3.metric("Days Left", f"{item['days_of_stock']} days")
            c4.metric("Velocity", item["velocity"])
            c5.metric("Margin", f"{margin}%")

            st.markdown(f"""
            <div style='margin:12px 0 4px;font-size:0.68rem;color:#888;text-transform:uppercase;letter-spacing:0.1em;'>Stock Level vs Reorder Point</div>
            <div style='background:#eee;border-radius:3px;height:8px;'>
                <div style='width:{pct}%;height:8px;border-radius:3px;background:{bc};'></div>
            </div>
            <div style='display:flex;justify-content:space-between;font-size:0.68rem;color:#888;margin-top:4px;'>
                <span>0</span><span style='color:#B8964A;'>Reorder point: {item['reorder_point']}</span><span>Max</span>
            </div>
            """, unsafe_allow_html=True)

            col_p, col_r = st.columns(2)
            with col_p:
                st.markdown(f"""
                <div style='background:#f9f9f9;padding:12px;border-radius:2px;margin-top:8px;'>
                    <div style='font-size:0.68rem;color:#888;text-transform:uppercase;margin-bottom:4px;'>Pricing</div>
                    <div style='font-size:0.85rem;color:#000;'>Cost: <strong>₹{item['cost']}</strong> · Selling: <strong>₹{item['selling_price']}</strong> · Margin: <strong style='color:#C41E3A;'>{margin}%</strong></div>
                </div>
                """, unsafe_allow_html=True)
            with col_r:
                if s == "REORDER NOW":
                    sq = item["reorder_point"] * 3
                    st.markdown(f"<div class='alert alert-red' style='margin-top:8px;'>💡 Order <strong>{sq} units</strong> — cost ₹{sq * item['cost']:,}</div>", unsafe_allow_html=True)
                elif s == "DEAD STOCK":
                    st.markdown(f"<div class='alert alert-gold' style='margin-top:8px;'>💡 Flash sale at <strong>₹{int(item['selling_price'] * 0.7)}</strong> (30% off) to clear stock</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>◆ Visual</div><div class='section-title'>Stock vs Reorder Point</div>", unsafe_allow_html=True)

    skus = [i["sku"] for i in INVENTORY]
    qtys = [i["qty"] for i in INVENTORY]
    rpts = [i["reorder_point"] for i in INVENTORY]
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(name='Current Stock', x=skus, y=qtys,
        marker_color=['#C41E3A' if q < r else '#000' for q, r in zip(qtys, rpts)],
        text=qtys, textposition='outside', textfont=dict(color='#000')))
    fig4.add_trace(go.Scatter(name='Reorder Point', x=skus, y=rpts,
        mode='lines+markers', line=dict(color='#B8964A', dash='dash', width=2), marker=dict(size=8)))
    fig4.update_layout(plot_bgcolor='white', paper_bgcolor='white',
        font=dict(family='Inter', size=12, color='#000'),
        legend=dict(orientation='h', y=1.1),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title="Units"),
        margin=dict(l=10, r=10, t=30, b=10), height=320)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PRICING
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Pricing":
    st.markdown("""
    <div class='masthead'>
        <div class='masthead-eyebrow'>◎ Margin Intelligence</div>
        <div class='masthead-title'>Pricing Studio</div>
        <div class='masthead-sub'>Market Benchmarking · Competitor Analysis · Margin Optimisation</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='metric-card'><div class='metric-val'>₹950</div><div class='metric-lbl'>Avg Market Price</div><div class='metric-delta'>Across all SKUs</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='metric-card'><div class='metric-val'>5</div><div class='metric-lbl'>Price Up Opportunities</div><div class='metric-delta'>₹18K extra margin/month</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='metric-card'><div class='metric-val'>64%</div><div class='metric-lbl'>Avg Gross Margin</div><div class='metric-delta'>Trending products only</div></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>◆ Per Product Analysis</div><div class='section-title'>Price Positioning</div>", unsafe_allow_html=True)

    for p in PRICING:
        opp = p["opportunity"]
        oc = "#C41E3A" if "UP" in opp else "#B8964A" if "Reduce" in opp else "#555"
        with st.expander(f"{p['product']}  ·  Your Price ₹{p['your_price']}  ·  {opp}"):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Your Price", f"₹{p['your_price']}")
            c2.metric("Market Avg", f"₹{p['market_avg']}", delta=f"{p['your_price']-p['market_avg']:+}")
            c3.metric("Suggested", f"₹{p['suggested']}")
            c4.metric("Margin", f"{p['margin_pct']}%")

            rs = p["high"] - p["low"]
            yp = int((p["your_price"] - p["low"]) / rs * 100) if rs else 50
            sp = int((p["suggested"] - p["low"]) / rs * 100) if rs else 50
            st.markdown(f"""
            <div style='margin:12px 0 4px;font-size:0.68rem;color:#888;text-transform:uppercase;'>Market Price Range  ·  Low ₹{p['low']} → High ₹{p['high']}</div>
            <div style='position:relative;background:#eee;border-radius:3px;height:10px;width:100%;'>
                <div style='position:absolute;left:{yp}%;top:-4px;width:5px;height:18px;background:#000;border-radius:2px;'></div>
                <div style='position:absolute;left:{sp}%;top:-4px;width:5px;height:18px;background:#C41E3A;border-radius:2px;'></div>
            </div>
            <div style='display:flex;justify-content:space-between;font-size:0.68rem;margin-top:6px;'>
                <span style='color:#000;'>■ Your price: ₹{p['your_price']}</span>
                <span style='color:#C41E3A;'>■ Suggested: ₹{p['suggested']}</span>
            </div>
            <div style='margin-top:10px;padding:10px 14px;background:#f9f9f9;border-left:3px solid {oc};font-size:0.82rem;color:#000;font-weight:600;'>{opp}</div>
            """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>◆ Visual</div><div class='section-title'>Margin Breakdown</div>", unsafe_allow_html=True)
    prods = [p["product"] for p in PRICING]
    margins = [p["margin_pct"] for p in PRICING]
    mc = ["#2E7D32" if m > 60 else "#B8964A" if m > 40 else "#C41E3A" for m in margins]
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(x=prods, y=margins, marker_color=mc,
        text=[f"{m}%" for m in margins], textposition='outside', textfont=dict(color='#000')))
    fig5.add_hline(y=50, line_dash="dash", line_color="#B8964A", annotation_text="Min target 50%", annotation_font_color="#000")
    fig5.update_layout(plot_bgcolor='white', paper_bgcolor='white',
        font=dict(family='Inter', size=11, color='#000'),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title="Gross Margin %", range=[0, 90]),
        xaxis=dict(showgrid=False, tickangle=-20),
        margin=dict(l=10, r=10, t=20, b=80), height=340)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MARKETPLACE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Marketplace":
    st.markdown("""
    <div class='masthead'>
        <div class='masthead-eyebrow'>◇ Supplier Network</div>
        <div class='masthead-title'>Wholesaler Marketplace</div>
        <div class='masthead-sub'>Verified Suppliers · Pan India · Direct Ordering</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)

    cs, cc, cm = st.columns([2, 1, 1])
    with cs:
        search = st.text_input("Search", placeholder="e.g. cargo pants, Surat, linen…")
    with cc:
        city_f = st.selectbox("City", ["All", "Surat", "Jaipur", "Mumbai", "Tirupur"])
    with cm:
        cat_f = st.selectbox("Category", CATEGORIES, key="wh_cat")

    st.markdown("<hr>", unsafe_allow_html=True)

    for wh in WHOLESALERS:
        if city_f != "All" and wh["city"] != city_f:
            continue
        if search and search.lower() not in wh["name"].lower() and not any(search.lower() in p["name"].lower() for p in wh["products"]):
            continue

        stars = "★" * int(wh["rating"]) + "☆" * (5 - int(wh["rating"]))
        tags_html = "".join([f"<span class='wh-tag'>{t}</span>" for t in wh["tags"]])

        st.markdown(f"""
        <div class='wh-card'>
            <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                <div>
                    <div class='wh-name'>{wh['name']}</div>
                    <div class='wh-meta'>📍 {wh['city']} · {wh['speciality']} · {wh['years']} years</div>
                    <div style='margin-top:8px;'>{tags_html}</div>
                </div>
                <div style='text-align:right;'>
                    <div style='color:#B8964A;font-size:1.1rem;'>{stars}</div>
                    <div style='font-size:0.73rem;color:#000;'>{wh['rating']}/5 · ✅ Verified</div>
                    <div style='font-size:0.7rem;color:#555;margin-top:2px;'>Min order ₹{wh['min_order_value']//1000}K</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for prod in wh["products"]:
            if cat_f != "All" and prod["category"] != cat_f:
                continue
            with st.expander(f"  {prod['name']}  ·  MOQ {prod['moq']} units  ·  ₹{prod['price_per_unit']}/unit"):
                c1, c2, c3, c4, c5 = st.columns(5)
                c1.metric("Price/Unit", f"₹{prod['price_per_unit']}")
                c2.metric("MOQ", f"{prod['moq']} units")
                c3.metric("Fabric", prod["fabric"])
                c4.metric("Lead Time", f"{prod['lead_days']} days")
                c5.metric("Colors", f"{prod['colors']}")

                total = prod["price_per_unit"] * prod["moq"]
                st.markdown(f"<div style='background:#f9f9f9;padding:10px 16px;font-size:0.82rem;color:#000;border-radius:2px;margin-top:8px;'>Min order: {prod['moq']} × ₹{prod['price_per_unit']} = <strong>₹{total:,}</strong> · Sizes: {prod['sizes']}</div>", unsafe_allow_html=True)

                b1, b2, b3, _ = st.columns([1, 1, 1, 3])
                with b1:
                    if st.button("📩 Enquire", key=f"enq_{wh['id']}_{prod['name'][:8]}"):
                        st.success(f"Enquiry sent to {wh['name']}!")
                with b2:
                    if st.button("🛒 Order", key=f"ord_{wh['id']}_{prod['name'][:8]}"):
                        st.success(f"Order placed with {wh['name']}!")
                with b3:
                    if st.button("💬 Message", key=f"msg_{wh['id']}_{prod['name'][:8]}"):
                        st.session_state.page = "Messages"
                        st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>◆ Compare</div><div class='section-title'>Supplier Ratings</div>", unsafe_allow_html=True)
    wn = [w["name"].split(" ")[0] + " " + w["name"].split(" ")[1] for w in WHOLESALERS]
    wr = [w["rating"] for w in WHOLESALERS]
    fig6 = go.Figure(go.Bar(x=wn, y=wr, marker_color='#000',
        text=wr, textposition='outside', textfont=dict(color='#000')))
    fig6.add_hline(y=4.5, line_dash="dot", line_color="#C41E3A", annotation_text="Top tier", annotation_font_color="#000")
    fig6.update_layout(plot_bgcolor='white', paper_bgcolor='white',
        font=dict(family='Inter', size=12, color='#000'),
        yaxis=dict(range=[0, 5.5], showgrid=True, gridcolor='#f0f0f0'),
        xaxis=dict(showgrid=False),
        margin=dict(l=10, r=10, t=20, b=10), height=260)
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MESSAGES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Messages":
    st.markdown("""
    <div class='masthead'>
        <div class='masthead-eyebrow'>✉ Direct Messaging</div>
        <div class='masthead-title'>Messages</div>
        <div class='masthead-sub'>Connect buyers and sellers directly · All messages monitored for safety</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)

    uname = st.session_state.username
    my_msgs = [m for m in st.session_state.messages if m["from"] == uname or m["to"] == uname]

    contacts = set()
    for m in my_msgs:
        contacts.add(m["to"] if m["from"] == uname else m["from"])

    if not contacts:
        contacts = {"seller1"} if role == "buyer" else {"buyer1"}

    selected_contact = st.selectbox("Conversation with", list(contacts))

    convo = [m for m in st.session_state.messages if
             (m["from"] == uname and m["to"] == selected_contact) or
             (m["from"] == selected_contact and m["to"] == uname)]

    st.markdown("<div class='chat-wrap'>", unsafe_allow_html=True)
    if not convo:
        st.markdown("<div style='text-align:center;color:#888;padding:40px;font-size:0.85rem;'>No messages yet. Start the conversation below.</div>", unsafe_allow_html=True)
    for m in convo:
        if m["from"] == uname:
            st.markdown(f"<div style='text-align:right;'><div class='chat-sender' style='text-align:right;'>You · {m['time']}</div><div class='chat-msg-user'>{m['text']}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div><div class='chat-sender'>{USERS.get(m['from'], {}).get('name', m['from'])} · {m['time']}</div><div class='chat-msg-bot'>{m['text']}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    new_msg = st.text_input("Type a message…", placeholder="e.g. Can you do 150 units at ₹280?", key="new_msg")
    if st.button("Send →", key="send_msg"):
        if new_msg.strip():
            flagged = check_illegal_content(new_msg)
            if flagged:
                st.markdown(f"<div class='safety-banner'>🚫 Message blocked — contains flagged content: {', '.join(flagged)}. Trendora prohibits illegal activity.</div>", unsafe_allow_html=True)
            else:
                now = datetime.now().strftime("%I:%M %p")
                st.session_state.messages.append({
                    "id": len(st.session_state.messages) + 1,
                    "from": uname, "to": selected_contact,
                    "text": new_msg, "time": now, "date": "Today"
                })
                st.rerun()

    st.markdown("<div class='alert alert-black' style='margin-top:16px;'>🛡️ All messages are monitored by Trendora's safety system. Illegal content, counterfeit goods, or fraudulent activity will result in immediate account suspension.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: AI ADVISOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "AI Advisor":
    st.markdown("""
    <div class='masthead'>
        <div class='masthead-eyebrow'>✦ Powered by AI</div>
        <div class='masthead-title'>AI Business Advisor</div>
        <div class='masthead-sub'>Ask anything · Get instant strategy · Trend-aware · Always on</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#000;color:#fff;padding:16px 20px;border-radius:2px;margin-bottom:20px;border-left:4px solid #C41E3A;'>
        <div style='font-family:"Playfair Display",serif;font-size:1rem;font-weight:700;margin-bottom:4px;'>Hello, I am Trendora AI 👋</div>
        <div style='font-size:0.82rem;color:#aaa;'>I know your inventory, current trends, market prices, and supplier data. Ask me anything.</div>
    </div>
    """, unsafe_allow_html=True)

    quick_qs = [
        "What should I reorder this week?",
        "Which dead stock should I clear?",
        "How can I improve my margins?",
        "Which wholesaler is best for cargo pants?",
        "Who is my target audience?",
        "What is trending right now?",
        "How is my revenue performing?",
        "What should I stock for the festive season?",
    ]

    st.markdown("<div style='font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;color:#888;margin-bottom:10px;'>Quick Questions</div>", unsafe_allow_html=True)
    qcols = st.columns(4)
    for i, q in enumerate(quick_qs):
        with qcols[i % 4]:
            if st.button(q, key=f"q_{i}"):
                st.session_state.chat_history.append({"role": "user", "text": q})
                response = get_ai_response(q, role)
                st.session_state.chat_history.append({"role": "bot", "text": response})
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='chat-wrap'>", unsafe_allow_html=True)
    if not st.session_state.chat_history:
        st.markdown("<div style='text-align:center;color:#888;padding:40px;font-size:0.85rem;'>Ask me anything about your fashion business ↓</div>", unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"<div style='text-align:right;'><div class='chat-sender' style='text-align:right;'>You</div><div class='chat-msg-user'>{msg['text']}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div><div class='chat-sender'>Trendora AI</div><div class='chat-msg-bot'>{msg['text']}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    user_q = st.text_input("Ask Trendora AI…", placeholder="e.g. Should I increase my cargo pants price?", key="ai_q")
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("Ask →", key="ask_btn"):
            if user_q.strip():
                flagged = check_illegal_content(user_q)
                if flagged:
                    st.markdown(f"<div class='safety-banner'>🚫 Query flagged: {', '.join(flagged)}</div>", unsafe_allow_html=True)
                else:
                    st.session_state.chat_history.append({"role": "user", "text": user_q})
                    response = get_ai_response(user_q, role)
                    st.session_state.chat_history.append({"role": "bot", "text": response})
                    st.rerun()
    with c2:
        if st.button("Clear Chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>◆ Auto Intelligence</div><div class='section-title'>This Week's Digest</div>", unsafe_allow_html=True)
    digests = [
        ("#C41E3A", "🔴 URGENT", "Stock out in 4 days", "Baggy Cargo Pants, Crochet Mini Skirts, and Maxi Dresses will be out of stock before the weekend. Contact Rajesh Textiles and Femina Fashion House today."),
        ("#2E7D32", "💰 OPPORTUNITY", "₹18K margin available", "Raise prices on 5 products to market average — adds ₹18,000/month in pure margin at zero extra cost. No procurement needed."),
        ("#B8964A", "📦 ACTION", "₹70K dead stock to clear", "78 blazers unsold for 90+ days. Run a 30% clearance sale to recover ₹81K and free up capital for trending items."),
        ("#000", "📈 TREND", "Crochet peaks in 3 weeks", "Your highest-margin item at 71%. Only 6 units in stock. Order 75 units from Femina Fashion House immediately."),
    ]
    dc = st.columns(2)
    for i, (color, label, title, body) in enumerate(digests):
        with dc[i % 2]:
            st.markdown(f"""
            <div style='background:#fff;border-left:4px solid {color};padding:16px 20px;margin-bottom:12px;box-shadow:0 2px 8px rgba(0,0,0,0.06);border-radius:2px;'>
                <div style='font-size:0.6rem;letter-spacing:0.15em;text-transform:uppercase;color:{color};font-weight:700;margin-bottom:4px;'>{label}</div>
                <div style='font-family:"Playfair Display",serif;font-size:0.95rem;font-weight:700;color:#000;margin-bottom:6px;'>{title}</div>
                <div style='font-size:0.8rem;color:#333;line-height:1.5;'>{body}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: NEWS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "News":
    st.markdown("""
    <div class='masthead'>
        <div class='masthead-eyebrow'>📰 Industry Intelligence</div>
        <div class='masthead-title'>Fashion News</div>
        <div class='masthead-sub'>Current trends · Market updates · Industry reports · June 2025</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)

    impact_f = st.selectbox("Filter by Impact", ["All", "HIGH", "MEDIUM", "LOW"])
    filtered_news = FASHION_NEWS if impact_f == "All" else [n for n in FASHION_NEWS if n["impact"] == impact_f]

    for news in filtered_news:
        ic = "#C41E3A" if news["impact"] == "HIGH" else "#B8964A" if news["impact"] == "MEDIUM" else "#888"
        st.markdown(f"""
        <div class='news-card'>
            <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;'>
                <div class='news-headline'>{news['headline']}</div>
                <span style='background:{ic};color:#fff;padding:2px 10px;border-radius:20px;font-size:0.6rem;letter-spacing:0.1em;text-transform:uppercase;font-weight:700;white-space:nowrap;margin-left:12px;'>{news['impact']}</span>
            </div>
            <div class='news-meta'>{news['source']} · {news['date']}</div>
            <div class='news-body'>{news['summary']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MY PRODUCTS (Seller only)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "My Products":
    st.markdown("""
    <div class='masthead'>
        <div class='masthead-eyebrow'>◆ Seller Dashboard</div>
        <div class='masthead-title'>My Products</div>
        <div class='masthead-sub'>Manage your listings · View enquiries · Track performance</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)

    my_wh = [w for w in WHOLESALERS if w.get("username") == st.session_state.username]

    if my_wh:
        wh = my_wh[0]
        st.markdown(f"""
        <div class='wh-card'>
            <div class='wh-name'>{wh['name']}</div>
            <div class='wh-meta'>📍 {wh['city']} · {wh['speciality']} · ⭐ {wh['rating']}/5 · ✅ Verified</div>
            <div style='margin-top:8px;'>{"".join([f"<span class='wh-tag'>{t}</span>" for t in wh['tags']])}</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='metric-card'><div class='metric-val'>{len(wh['products'])}</div><div class='metric-lbl'>Active Listings</div><div class='metric-delta'>Live on marketplace</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='metric-card'><div class='metric-val'>3</div><div class='metric-lbl'>New Enquiries</div><div class='metric-delta'>Respond within 24h</div></div>", unsafe_allow_html=True)
        with c3:
            total_moq_val = sum(p["moq"] * p["price_per_unit"] for p in wh["products"])
            st.markdown(f"<div class='metric-card'><div class='metric-val'>₹{total_moq_val//1000}K</div><div class='metric-lbl'>Min Order Value</div><div class='metric-delta'>Across all products</div></div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='eyebrow'>◆ Listings</div><div class='section-title'>Your Products</div>", unsafe_allow_html=True)

        for prod in wh["products"]:
            with st.expander(f"  {prod['name']}  ·  ₹{prod['price_per_unit']}/unit  ·  MOQ {prod['moq']}"):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Price/Unit", f"₹{prod['price_per_unit']}")
                c2.metric("MOQ", f"{prod['moq']}")
                c3.metric("Lead Time", f"{prod['lead_days']} days")
                c4.metric("Colors", prod["colors"])
                st.markdown(f"<div style='background:#f9f9f9;padding:10px;border-radius:2px;font-size:0.82rem;color:#000;margin-top:8px;'>Fabric: {prod['fabric']} · Sizes: {prod['sizes']}</div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='eyebrow'>◆ Add New</div><div class='section-title'>List a New Product</div>", unsafe_allow_html=True)
        with st.form("new_product"):
            np_name = st.text_input("Product Name")
            np_price = st.number_input("Price per Unit (₹)", min_value=1)
            np_moq = st.number_input("MOQ (units)", min_value=1)
            np_fabric = st.text_input("Fabric")
            np_lead = st.number_input("Lead Time (days)", min_value=1)
            np_desc = st.text_area("Description")
            submitted = st.form_submit_button("List Product →")
            if submitted:
                if np_name:
                    flagged = check_illegal_content(np_name + " " + np_desc)
                    if flagged:
                        st.markdown(f"<div class='safety-banner'>🚫 Listing blocked — flagged content: {', '.join(flagged)}</div>", unsafe_allow_html=True)
                    else:
                        st.success(f"✅ '{np_name}' listed successfully on Trendora Marketplace!")
    else:
        st.markdown("<div class='alert alert-gold'>You don't have a seller profile set up yet. Contact Trendora support to get verified.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ORDERS (Seller)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Orders":
    st.markdown("""
    <div class='masthead'>
        <div class='masthead-eyebrow'>◆ Order Management</div>
        <div class='masthead-title'>Orders</div>
        <div class='masthead-sub'>Incoming orders · Enquiries · Dispatch tracking</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='metric-card'><div class='metric-val'>3</div><div class='metric-lbl'>New Orders</div><div class='metric-delta'>Action required</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='metric-card'><div class='metric-val'>₹1.2L</div><div class='metric-lbl'>Orders This Month</div><div class='metric-delta'>↑ 18% vs last month</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='metric-card'><div class='metric-val'>7</div><div class='metric-lbl'>Pending Dispatch</div><div class='metric-delta'>Ship within 48h</div></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>◆ Recent Orders</div><div class='section-title'>Order Queue</div>", unsafe_allow_html=True)

    orders = [
        {"id": "ORD-001", "buyer": "Priya Boutique", "product": "Baggy Cargo Pants", "qty": 100, "value": 32000, "status": "New", "date": "Today"},
        {"id": "ORD-002", "buyer": "Ananya Fashion House", "product": "Linen Trousers", "qty": 50, "value": 14000, "status": "Confirmed", "date": "Yesterday"},
        {"id": "ORD-003", "buyer": "StyleHub Hyderabad", "product": "Baggy Cargo Pants", "qty": 75, "value": 24000, "status": "Dispatched", "date": "3 days ago"},
    ]

    for o in orders:
        sc = "#C41E3A" if o["status"] == "New" else "#B8964A" if o["status"] == "Confirmed" else "#2E7D32"
        with st.expander(f"{o['id']}  ·  {o['buyer']}  ·  {o['product']}  ·  ₹{o['value']:,}"):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Quantity", f"{o['qty']} units")
            c2.metric("Order Value", f"₹{o['value']:,}")
            c3.metric("Date", o["date"])
            c4.metric("Status", o["status"])
            st.markdown(f"<div style='margin-top:8px;padding:8px 14px;background:#f9f9f9;border-left:3px solid {sc};font-size:0.82rem;color:#000;font-weight:600;'>Status: {o['status']}</div>", unsafe_allow_html=True)
            if o["status"] == "New":
                b1, b2, _ = st.columns([1, 1, 4])
                with b1:
                    if st.button("✅ Confirm", key=f"conf_{o['id']}"):
                        st.success("Order confirmed!")
                with b2:
                    if st.button("❌ Decline", key=f"dec_{o['id']}"):
                        st.error("Order declined.")
    st.markdown("</div>", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr>
<div style='text-align:center;padding:20px;font-size:0.65rem;color:#888;letter-spacing:0.15em;text-transform:uppercase;background:#fff;'>
    Trendora · Fashion Intelligence Platform · All activity monitored · © 2025
</div>
""", unsafe_allow_html=True)
