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
.trend-card { background: #fff; border-left: 4px solid #C41E3A;
