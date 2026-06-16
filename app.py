import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from data.mock_data import (
    TRENDS, INVENTORY, PRICING, WHOLESALERS,
    get_forecast_data, get_revenue_data,
    CATEGORIES, MESSAGES, FASHION_NEWS, AUDIENCE_DATA,
    check_illegal_content, get_ai_response
)

st.set_page_config(page_title="Trendora", page_icon="◆", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #fff; color: #0a0a0a; }
[data-testid="stSidebar"] { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
[data-testid="stAppViewContainer"] { padding-top: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
.stDeployButton { display: none !important; }

/* ── NAV ── */
.tnav {
    background: #0a0a0a;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 32px;
    border-bottom: 2px solid #C41E3A;
    position: sticky;
    top: 0;
    z-index: 999;
}
.tnav-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #fff;
    letter-spacing: 0.02em;
    white-space: nowrap;
    min-width: 140px;
}
.tnav-logo em { color: #C41E3A; font-style: normal; }
.tnav-right {
    font-size: 0.65rem;
    color: #888;
    letter-spacing: 0.06em;
    white-space: nowrap;
    text-align: right;
}
.tnav-right strong { color: #C41E3A; font-weight: 500; }

/* ── NAV BUTTONS ROW ── */
.nav-row-wrap {
    background: #111;
    border-bottom: 1px solid #222;
    padding: 0;
    display: flex;
    overflow-x: auto;
}

/* ── MASTHEAD ── */
.mhead { background: #0a0a0a; padding: 40px 40px 32px; border-bottom: 2px solid #C41E3A; margin-bottom: 0; }
.mhead-eye { font-size: 0.6rem; letter-spacing: 0.24em; text-transform: uppercase; color: #C41E3A; margin-bottom: 8px; font-weight: 500; }
.mhead-title { font-family: 'Playfair Display', serif; font-size: 2.8rem; font-weight: 700; color: #fff; line-height: 1.05; }
.mhead-sub { font-size: 0.75rem; color: #666; margin-top: 8px; letter-spacing: 0.04em; }

/* ── PAGE WRAP ── */
.pwrap { padding: 32px 40px 56px; background: #fff; }

/* ── METRIC CARDS ── */
.mc { background: #0a0a0a; padding: 22px 18px; margin-bottom: 8px; }
.mc-val { font-family: 'Playfair Display', serif; font-size: 1.9rem; font-weight: 700; color: #fff; line-height: 1; }
.mc-lbl { font-size: 0.58rem; letter-spacing: 0.16em; text-transform: uppercase; color: #666; margin-top: 5px; }
.mc-d { font-size: 0.72rem; color: #C41E3A; margin-top: 6px; font-weight: 500; }

/* ── TREND CARDS ── */
.tc { background: #fff; border-left: 3px solid #C41E3A; padding: 18px; margin-bottom: 14px; box-shadow: 0 1px 8px rgba(0,0,0,0.08); }
.tc.med { border-left-color: #999; }
.tc.lo  { border-left-color: #ccc; }
.tc.dead{ border-left-color: #e0e0e0; }
.tc-name { font-family: 'Playfair Display', serif; font-size: 1.05rem; font-weight: 700; color: #0a0a0a; margin-bottom: 3px; }
.tc-meta { font-size: 0.68rem; color: #777; margin-bottom: 6px; }
.tc-desc { font-size: 0.78rem; color: #333; line-height: 1.55; margin-bottom: 8px; }
.tc-insight { font-size: 0.74rem; color: #0a0a0a; background: #f9f9f9; border-left: 2px solid #C41E3A; padding: 8px 10px; margin-top: 8px; line-height: 1.5; }
.hbar { background: #eee; height: 4px; border-radius: 2px; margin: 8px 0 3px; }
.hfill { height: 4px; border-radius: 2px; background: linear-gradient(90deg,#C41E3A,#ff6b6b); }
.badge { display:inline-block; padding:2px 9px; border-radius:20px; font-size:0.58rem; letter-spacing:0.1em; text-transform:uppercase; font-weight:600; margin-bottom:6px; }
.bh { background:#fff0f0; color:#C41E3A; }
.bm { background:#f5f5f5; color:#555; }
.bl { background:#f5f5f5; color:#888; }
.bd { background:#f0f0f0; color:#aaa; }

/* ── SECTION TITLES (always on white bg) ── */
.eye { font-size:0.58rem; letter-spacing:0.2em; text-transform:uppercase; color:#C41E3A; font-weight:600; margin-bottom:4px; }
.stitle { font-family:'Playfair Display',serif; font-size:1.6rem; font-weight:700; color:#0a0a0a; border-bottom:2px solid #0a0a0a; padding-bottom:8px; margin-bottom:20px; margin-top:4px; }

/* ── ALERTS ── */
.al { padding:10px 14px; margin:6px 0; font-size:0.78rem; color:#0a0a0a; }
.al-r  { background:#fff0f2; border-left:3px solid #C41E3A; }
.al-g  { background:#fff8ec; border-left:3px solid #999; }
.al-b  { background:#f5f5f5; border-left:3px solid #0a0a0a; }
.al-red { background:#C41E3A; color:#fff; padding:10px 14px; font-weight:600; font-size:0.78rem; }

/* ── INSIGHT BOX ── */
.insight-box { background:#0a0a0a; color:#fff; padding:14px 16px; margin:10px 0; font-size:0.78rem; line-height:1.6; border-left:3px solid #C41E3A; }
.insight-box strong { color:#C41E3A; }

/* ── WHOLESALER CARDS ── */
.wc { background:#fff; border-top:2px solid #0a0a0a; padding:20px; margin-bottom:16px; box-shadow:0 1px 8px rgba(0,0,0,0.07); }
.wc-name { font-family:'Playfair Display',serif; font-size:1.1rem; font-weight:700; color:#0a0a0a; }
.wc-meta { font-size:0.68rem; color:#777; margin-top:2px; }
.wc-about { font-size:0.76rem; color:#444; margin-top:8px; line-height:1.5; }
.wtag { display:inline-block; padding:2px 8px; background:#0a0a0a; color:#fff; font-size:0.55rem; letter-spacing:0.1em; text-transform:uppercase; border-radius:1px; margin:2px 2px 0 0; }

/* ── NEWS CARDS ── */
.nc { border-bottom:1px solid #eee; padding:16px 0; }
.nc-h { font-family:'Playfair Display',serif; font-size:1rem; font-weight:700; color:#0a0a0a; margin-bottom:4px; }
.nc-m { font-size:0.65rem; color:#aaa; margin-bottom:6px; }
.nc-b { font-size:0.78rem; color:#333; line-height:1.55; }

/* ── SOCIAL CHAT (Messages) ── */
.chat-outer { background:#fff; border:1px solid #eee; border-radius:4px; overflow:hidden; }
.contact-list { background:#f9f9f9; border-right:1px solid #eee; min-height:400px; }
.contact-item { padding:14px 16px; border-bottom:1px solid #eee; cursor:pointer; display:flex; align-items:center; gap:10px; }
.contact-item:hover { background:#f0f0f0; }
.contact-item.active { background:#fff0f0; border-left:3px solid #C41E3A; }
.contact-avatar { width:36px; height:36px; border-radius:50%; background:#0a0a0a; display:flex; align-items:center; justify-content:center; color:#fff; font-size:0.75rem; font-weight:600; flex-shrink:0; }
.contact-name { font-size:0.82rem; font-weight:600; color:#0a0a0a; }
.contact-preview { font-size:0.68rem; color:#888; margin-top:1px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:160px; }
.chat-area { background:#fff; min-height:400px; padding:16px; display:flex; flex-direction:column; }
.chat-messages { flex:1; min-height:300px; overflow-y:auto; padding-bottom:8px; }
.msg-row-right { display:flex; justify-content:flex-end; margin:6px 0; }
.msg-row-left { display:flex; justify-content:flex-start; margin:6px 0; align-items:flex-end; gap:8px; }
.msg-avatar { width:28px; height:28px; border-radius:50%; background:#0a0a0a; display:flex; align-items:center; justify-content:center; color:#fff; font-size:0.6rem; font-weight:600; flex-shrink:0; }
.msg-bubble-right { background:#0a0a0a; color:#fff; border-radius:18px 18px 4px 18px; padding:10px 14px; max-width:65%; font-size:0.8rem; line-height:1.45; }
.msg-bubble-left { background:#f2f2f2; color:#0a0a0a; border-radius:18px 18px 18px 4px; padding:10px 14px; max-width:65%; font-size:0.8rem; line-height:1.45; }
.msg-time { font-size:0.58rem; color:#bbb; margin-top:3px; text-align:right; }
.msg-time-left { font-size:0.58rem; color:#bbb; margin-top:3px; }
.chat-header { background:#0a0a0a; color:#fff; padding:12px 16px; display:flex; align-items:center; gap:10px; }
.chat-header-name { font-size:0.85rem; font-weight:600; color:#fff; }
.chat-header-status { font-size:0.62rem; color:#C41E3A; }

/* ── AI CHAT ── */
.cwrap { background:#f9f9f9; padding:16px; min-height:220px; margin-bottom:14px; }
.cu { background:#0a0a0a; color:#fff; border-radius:18px 18px 4px 18px; padding:10px 14px; margin:6px 0 6px auto; max-width:70%; font-size:0.8rem; width:fit-content; margin-left:auto; line-height:1.45; white-space:pre-line; }
.cb { background:#fff; color:#0a0a0a; border-radius:18px 18px 18px 4px; padding:10px 14px; margin:6px 0; max-width:70%; font-size:0.8rem; border:1px solid #eee; line-height:1.45; white-space:pre-line; }
.cs { font-size:0.6rem; color:#aaa; margin-bottom:2px; }

/* ── LOGIN ── */
.lwrap { max-width:420px; margin:50px auto; padding:40px 36px; background:#fff; box-shadow:0 2px 24px rgba(0,0,0,0.1); border-top:3px solid #C41E3A; }
.llogo { font-family:'Playfair Display',serif; font-size:1.9rem; font-weight:700; color:#0a0a0a; text-align:center; margin-bottom:4px; }
.llogo em { color:#C41E3A; font-style:normal; }
.lsub { font-size:0.62rem; letter-spacing:0.16em; text-transform:uppercase; color:#aaa; text-align:center; margin-bottom:28px; }

/* ── HOME PAGE ── */
.hero { background:#0a0a0a; padding:64px 40px 56px; text-align:center; border-bottom:3px solid #C41E3A; }
.hero-eye { font-size:0.62rem; letter-spacing:0.28em; text-transform:uppercase; color:#C41E3A; margin-bottom:12px; font-weight:500; }
.hero-title { font-family:'Playfair Display',serif; font-size:3.8rem; font-weight:900; color:#fff; line-height:1; letter-spacing:-0.02em; margin-bottom:16px; }
.hero-title em { color:#C41E3A; font-style:normal; }
.hero-sub { font-size:0.95rem; color:#888; max-width:580px; margin:0 auto 28px; line-height:1.6; }
.feature-card { background:#fff; border-top:3px solid #0a0a0a; padding:24px 20px; height:100%; box-shadow:0 1px 8px rgba(0,0,0,0.07); }
.feature-icon { font-size:1.6rem; margin-bottom:10px; }
.feature-title { font-family:'Playfair
