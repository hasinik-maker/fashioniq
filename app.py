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
.feature-title { font-family:'Playfair Display',serif; font-size:1rem; font-weight:700; color:#0a0a0a; margin-bottom:6px; }
.feature-desc { font-size:0.76rem; color:#555; line-height:1.55; }
.who-card { background:#f9f9f9; border-left:3px solid #C41E3A; padding:16px 20px; margin-bottom:10px; }
.who-title { font-weight:700; font-size:0.88rem; color:#0a0a0a; margin-bottom:4px; }
.who-desc { font-size:0.76rem; color:#555; line-height:1.5; }
.step-num { font-family:'Playfair Display',serif; font-size:2rem; font-weight:900; color:#C41E3A; line-height:1; margin-bottom:6px; }
.step-title { font-weight:700; font-size:0.85rem; color:#0a0a0a; margin-bottom:4px; }
.step-desc { font-size:0.74rem; color:#666; line-height:1.5; }
.collage-zone { border:2px dashed #ddd; border-radius:4px; padding:32px; text-align:center; background:#fafafa; min-height:200px; }
.collage-title { font-family:'Playfair Display',serif; font-size:1rem; font-weight:700; color:#0a0a0a; margin-bottom:6px; }
.collage-sub { font-size:0.74rem; color:#aaa; }

/* ── BUTTONS ── */
.stButton > button { background:#0a0a0a !important; color:#fff !important; border:none !important; border-radius:1px !important; font-size:0.65rem !important; letter-spacing:0.12em !important; text-transform:uppercase !important; font-weight:600 !important; padding:9px 22px !important; transition:background 0.15s !important; }
.stButton > button:hover { background:#C41E3A !important; }

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border:1px solid #ddd !important; border-radius:1px !important;
    font-size:0.82rem !important; color:#0a0a0a !important; font-family:'Inter',sans-serif !important;
}
.stSelectbox label, .stTextInput label, .stTextArea label, .stMultiSelect label, .stNumberInput label {
    font-size:0.6rem !important; letter-spacing:0.1em !important;
    text-transform:uppercase !important; color:#888 !important; font-weight:500 !important;
}
[data-baseweb="select"] * { font-size:0.82rem !important; color:#0a0a0a !important; }
[data-testid="metric-container"] label { font-size:0.58rem !important; color:#777 !important; text-transform:uppercase !important; letter-spacing:0.1em !important; font-weight:500 !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { font-size:1.05rem !important; color:#0a0a0a !important; font-weight:600 !important; }
details summary { font-size:0.78rem !important; color:#0a0a0a !important; font-weight:500 !important; }
hr { border:none; border-top:1px solid #eee; margin:20px 0; }
[data-testid="stDataFrame"] { font-size:0.78rem !important; }
</style>
""", unsafe_allow_html=True)

# ══ SESSION STATE ══════════════════════════════════════════════════════════════
for k, v in [
    ("logged_in",False),("username",""),("role",""),
    ("page","Home"),("chat_history",[]),
    ("messages",list(MESSAGES)),("auth_mode","login"),
    ("collage_images",[]),("active_contact",None),
    ("user_db",{
        "buyer1": {"password":"buy123","role":"buyer","name":"Priya Sharma","email":"priya@email.com","city":"Hyderabad","business":"Priya Boutique"},
        "buyer2": {"password":"buy456","role":"buyer","name":"Ananya Reddy","email":"ananya@email.com","city":"Bangalore","business":"Ananya Fashion House"},
        "seller1":{"password":"sell123","role":"seller","name":"Rajesh Gupta","email":"rajesh@email.com","city":"Surat","business":"Rajesh Textiles & Exports"},
        "seller2":{"password":"sell456","role":"seller","name":"Meena Patel","email":"meena@email.com","city":"Jaipur","business":"Femina Fashion House"},
    })
]:
    if k not in st.session_state:
        st.session_state[k] = v

# ══ AUTH PAGE ══════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    st.markdown("""
    <div style='background:#0a0a0a;padding:14px 36px;border-bottom:2px solid #C41E3A;'>
        <div style='font-family:"Playfair Display",serif;font-size:1.5rem;font-weight:700;color:#fff;'>
            Trend<em style='color:#C41E3A;font-style:normal;'>ora</em>
        </div>
    </div>""", unsafe_allow_html=True)

    _, cm, _ = st.columns([1,1.1,1])
    with cm:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        t1,t2 = st.columns(2)
        with t1:
            if st.button("Sign In", key="go_login"):
                st.session_state.auth_mode="login"; st.rerun()
        with t2:
            if st.button("Create Account", key="go_signup"):
                st.session_state.auth_mode="signup"; st.rerun()

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if st.session_state.auth_mode == "login":
            st.markdown("<div class='lwrap'><div class='llogo'>Trend<em>ora</em></div><div class='lsub'>Sign in to continue</div></div>", unsafe_allow_html=True)
            role_sel = st.selectbox("I am a", ["Buyer — purchasing stock","Seller — selling wholesale"])
            username = st.text_input("Username or Email")
            password = st.text_input("Password", type="password")
            st.markdown("""<div style='background:#f7f7f7;padding:10px 12px;font-size:0.7rem;color:#777;margin:8px 0 14px;'>
                Demo — Buyer: <code>buyer1</code> / <code>buy123</code> &nbsp;·&nbsp; Seller: <code>seller1</code> / <code>sell123</code>
            </div>""", unsafe_allow_html=True)
            if st.button("Sign In →", key="login_btn"):
                db = st.session_state.user_db
                matched = None
                for uname, udata in db.items():
                    if (uname==username or udata.get("email","")==username) and udata["password"]==password:
                        matched=(uname,udata); break
                if matched:
                    uname,udata = matched
                    sel_role = "buyer" if "Buyer" in role_sel else "seller"
                    if udata["role"]==sel_role or udata["role"]=="admin":
                        st.session_state.update({"logged_in":True,"username":uname,"role":udata["role"],"page":"Home"})
                        st.rerun()
                    else:
                        st.error("Role doesn't match this account.")
                else:
                    st.error("Incorrect username or password.")
        else:
            st.markdown("<div class='lwrap'><div class='llogo'>Trend<em>ora</em></div><div class='lsub'>Create your free account</div></div>", unsafe_allow_html=True)
            su_role     = st.selectbox("I am a", ["Buyer — purchasing stock","Seller — selling wholesale"], key="su_r")
            su_name     = st.text_input("Full Name", placeholder="Priya Sharma")
            su_business = st.text_input("Business Name", placeholder="Priya Boutique")
            su_city     = st.text_input("City", placeholder="Hyderabad")
            su_email    = st.text_input("Email Address", placeholder="any@email.com")
            su_username = st.text_input("Username", placeholder="priya_boutique")
            su_password = st.text_input("Password", type="password")
            su_confirm  = st.text_input("Confirm Password", type="password")
            if st.button("Create Account →", key="signup_btn"):
                errs=[]
                if not su_name.strip(): errs.append("Full name required.")
                if not su_email.strip() or "@" not in su_email: errs.append("Valid email required.")
                if not su_username.strip() or len(su_username)<3: errs.append("Username must be 3+ characters.")
                if su_username in st.session_state.user_db: errs.append("Username already taken.")
                if any(u.get("email","")==su_email for u in st.session_state.user_db.values()): errs.append("Email already registered.")
                if not su_password: errs.append("Password required.")
                if su_password!=su_confirm: errs.append("Passwords don't match.")
                if not su_business.strip(): errs.append("Business name required.")
                flagged=check_illegal_content(su_name+" "+su_business)
                if flagged: errs.append(f"Flagged content: {', '.join(flagged)}")
                if errs:
                    for e in errs: st.error(e)
                else:
                    new_role="buyer" if "Buyer" in su_role else "seller"
                    st.session_state.user_db[su_username]={"password":su_password,"role":new_role,"name":su_name,"email":su_email,"city":su_city,"business":su_business}
                    st.session_state.update({"logged_in":True,"username":su_username,"role":new_role,"page":"Home"})
                    st.success(f"Welcome to Trendora, {su_name}!")
                    st.rerun()
    st.stop()

# ══ TOP NAV ════════════════════════════════════════════════════════════════════
user_info = st.session_state.user_db.get(st.session_state.username, {})
role = st.session_state.role

if role=="buyer":
    nav_items=["Home","Trends","Forecast","My Stock","Pricing","Marketplace","Messages","AI Advisor","News"]
else:
    nav_items=["Home","My Products","Orders","My Stock","Pricing","Messages","AI Advisor","News"]

st.markdown(f"""
<div class='tnav'>
    <div class='tnav-logo'>Trend<em>ora</em></div>
    <div class='tnav-right'>
        <strong>{user_info.get('name', st.session_state.username)}</strong><br>
        {role.upper()} · {user_info.get('business','')}
    </div>
</div>""", unsafe_allow_html=True)

# ── Single clean nav row ───────────────────────────────────────────────────────
nav_cols = st.columns(len(nav_items)+1)
for i, item in enumerate(nav_items):
    with nav_cols[i]:
        if st.button(item, key=f"n_{item}"):
            st.session_state.page=item; st.rerun()
with nav_cols[-1]:
    if st.button("Sign Out", key="so"):
        for k in ["logged_in","username","role","page","chat_history","messages","auth_mode","collage_images","active_contact"]:
            st.session_state.pop(k,None)
        st.rerun()

page = st.session_state.page

# ══════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════════════════════════
if page == "Home":
    uname_display = user_info.get('name','there').split()[0]

    st.markdown(f"""
    <div class='hero'>
        <div class='hero-eye'>◆ Fashion Intelligence Platform</div>
        <div class='hero-title'>Welcome back,<br><em>{uname_display}</em></div>
        <div class='hero-sub'>Trendora is your all-in-one fashion business command centre. Real-time trend alerts, demand forecasting, inventory management, pricing intelligence, and direct supplier connections — all in one place.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    # ── What is Trendora ──────────────────────────────────────────────────────
    st.markdown("<div class='eye'>◆ About</div><div class='stitle'>What is Trendora?</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.88rem;color:#333;line-height:1.8;max-width:720px;margin-bottom:28px;'>
        Trendora is a <strong>fashion trend intelligence platform</strong> built for small and medium apparel businesses in India.
        We bridge the gap between what's trending on the streets and what's sitting in your stockroom.
        Stop guessing. Start selling smarter.
    </div>""", unsafe_allow_html=True)

    f1,f2,f3 = st.columns(3)
    features = [
        ("🔥","Trend Intelligence","Live trend alerts for your city. Know what's viral before your competitors do. Heat scores, urgency ratings, and peak timing — all in one place."),
        ("📈","Demand Forecast","12-week demand projections for every product. See exactly when to order and how much. Never overstock or understock again."),
        ("📦","Stock Manager","Real-time inventory dashboard with automatic reorder alerts, dead stock warnings, and AI-powered reorder quantity suggestions."),
        ("💰","Pricing Studio","Market benchmarking against competitors. Know if you are overpriced or underpriced. Get margin improvement suggestions tailored to your audience."),
        ("🏭","Wholesaler Marketplace","Connect directly with verified Pan-India suppliers. Compare MOQ, pricing, lead times. Message and order without leaving the app."),
        ("✦","AI Business Advisor","Ask anything. Get sharp, specific advice on your inventory, trends, pricing, and strategy — powered by AI that knows YOUR business data."),
    ]
    cols = [f1,f2,f3]
    for i,(icon,title,desc) in enumerate(features):
        with cols[i%3]:
            st.markdown(f"""
            <div class='feature-card' style='margin-bottom:16px;'>
                <div class='feature-icon'>{icon}</div>
                <div class='feature-title'>{title}</div>
                <div class='feature-desc'>{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Who is it for ─────────────────────────────────────────────────────────
    st.markdown("<div class='eye'>◆ Perfect For</div><div class='stitle'>Who Needs Trendora?</div>", unsafe_allow_html=True)
    w1,w2 = st.columns(2)
    who = [
        ("👗 Boutique Owners","You run a small fashion boutique and struggle to decide what stock to buy. Trendora tells you exactly what is trending in your city, when to order, and from whom — so you never miss a viral trend."),
        ("🛍️ Online Fashion Sellers","You sell on Instagram, Meesho, or your own website. Trendora helps you stay ahead of trends, price correctly, and connect with wholesalers who supply the hottest items."),
        ("🏭 Wholesale Suppliers","You are a wholesaler in Surat, Jaipur, or Mumbai. Trendora gives you a marketplace to list products, receive enquiries, and connect directly with retailers across India."),
        ("📊 Fashion Entrepreneurs","You are building a fashion business and need data-driven decisions. Trendora gives you the intelligence normally only available to large brands — at zero cost."),
    ]
    for i,(title,desc) in enumerate(who):
        with (w1 if i%2==0 else w2):
            st.markdown(f"<div class='who-card'><div class='who-title'>{title}</div><div class='who-desc'>{desc}</div></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── How to use ────────────────────────────────────────────────────────────
    st.markdown("<div class='eye'>◆ Getting Started</div><div class='stitle'>How to Use Trendora</div>", unsafe_allow_html=True)
    s1,s2,s3,s4 = st.columns(4)
    steps = [
        ("01","Check Trends","Go to Trend Intelligence every Monday. See what is rising, viral, or declining in your market. Note the heat score and urgency level."),
        ("02","Check Your Stock","Open My Stock. Look for red alerts — these are items running out. Check dead stock warnings and act fast."),
        ("03","Order Smart","Go to Marketplace. Find verified suppliers for your trending items. Message them directly and place orders."),
        ("04","Ask the AI","Go to AI Advisor anytime. Ask questions like 'what should I reorder?' or 'how to improve my margins?' and get instant advice."),
    ]
    for col,(num,title,desc) in zip([s1,s2,s3,s4],steps):
        with col:
            st.markdown(f"""
            <div style='padding:20px 16px;background:#f9f9f9;border-top:3px solid #0a0a0a;height:100%;margin-bottom:16px;'>
                <div class='step-num'>{num}</div>
                <div class='step-title'>{title}</div>
                <div class='step-desc'>{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Important rules ───────────────────────────────────────────────────────
    st.markdown("<div class='eye'>◆ Safety & Rules</div><div class='stitle'>What You Must Know</div>", unsafe_allow_html=True)
    rules = [
        ("🛡️ Zero Tolerance for Illegal Activity","Trendora automatically detects and blocks any attempt to buy, sell, or communicate about drugs, weapons, counterfeit goods, child labour, human trafficking, or financial fraud. Violations result in immediate permanent suspension and may be reported to authorities."),
        ("✅ Verified Sellers Only","All wholesalers on the Trendora marketplace are manually verified before listing. Look for the ✅ Verified badge. Never pay outside the platform."),
        ("🔒 Your Messages are Monitored","All messages between buyers and sellers are automatically scanned for illegal content. This keeps the community safe for everyone."),
        ("📱 Keep Your Account Secure","Never share your password. Do not use the same password as other apps. Log out when using shared devices."),
    ]
    for icon_title, desc in rules:
        st.markdown(f"""
        <div style='background:#f9f9f9;border-left:3px solid #0a0a0a;padding:14px 18px;margin-bottom:10px;'>
            <div style='font-weight:700;font-size:0.85rem;color:#0a0a0a;margin-bottom:4px;'>{icon_title}</div>
            <div style='font-size:0.76rem;color:#555;line-height:1.55;'>{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Collage Zone ──────────────────────────────────────────────────────────
    st.markdown("<div class='eye'>◆ Your Space</div><div class='stitle'>My Collage Board</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.78rem;color:#777;margin-bottom:16px;'>
        Add your mood board, brand inspiration, product photos, or college project visuals here.
    </div>""", unsafe_allow_html=True)

    cc1,cc2,cc3 = st.columns([2,2,1])
    with cc1:
        col_url = st.text_input("Image URL or Pinterest link", placeholder="https://i.pinimg.com/…", key="col_url")
    with cc2:
        col_cap = st.text_input("Caption", placeholder="e.g. Summer mood board", key="col_cap")
    with cc3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("Add →", key="add_col"):
            if col_url.strip():
                flagged=check_illegal_content(col_url+" "+col_cap)
                if flagged:
                    st.markdown(f"<div class='al al-red'>🚫 Flagged: {', '.join(flagged)}</div>", unsafe_allow_html=True)
                else:
                    st.session_state.collage_images.append({"url":col_url.strip(),"cap":col_cap,"type":"url"})
                    st.rerun()

    up1,up2 = st.columns([3,1])
    with up1:
        col_file = st.file_uploader("Upload image", type=["jpg","jpeg","png","webp","gif"], key="col_file", label_visibility="collapsed")
    with up2:
        col_file_cap = st.text_input("Caption", placeholder="Caption", key="col_file_cap", label_visibility="collapsed")
        if st.button("Upload", key="upl_col") and col_file:
            st.session_state.collage_images.append({"url":col_file,"cap":col_file_cap,"type":"upload"})
            st.rerun()

    if st.session_state.collage_images:
        img_cols = st.columns(4)
        for i,img in enumerate(st.session_state.collage_images):
            with img_cols[i%4]:
                try:
                    if img["type"]=="url":
                        st.markdown(f"""<div style='border:1px solid #eee;border-radius:2px;overflow:hidden;margin-bottom:10px;'>
                            <img src='{img["url"]}' style='width:100%;display:block;' onerror="this.style.display='none'"/>
                            <div style='font-size:0.62rem;color:#777;padding:6px 8px;background:#fafafa;'>{img['cap'] or '—'}</div>
                        </div>""", unsafe_allow_html=True)
                    else:
                        st.image(img["url"], use_column_width=True, caption=img["cap"] or None)
                except: pass
        if st.button("Clear board", key="clr_col"):
            st.session_state.collage_images=[]; st.rerun()
    else:
        st.markdown("""
        <div class='collage-zone'>
            <div class='collage-title'>Your collage goes here</div>
            <div class='collage-sub'>Add image URLs or upload files above · Perfect for mood boards, inspo, or your college project visuals</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TRENDS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Trends":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>◆ Live Intelligence</div>
        <div class='mhead-title'>Trend Report</div>
        <div class='mhead-sub'>Hyderabad Market · June 2025 · Updated Daily</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown("<div class='mc'><div class='mc-val'>8</div><div class='mc-lbl'>Active Trends</div><div class='mc-d'>↑ 3 new this week</div></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='mc'><div class='mc-val'>4</div><div class='mc-lbl'>Urgent Alerts</div><div class='mc-d'>Reorder now</div></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='mc'><div class='mc-val'>94</div><div class='mc-lbl'>Top Heat Score</div><div class='mc-d'>Cargo Pants 🔥</div></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='mc'><div class='mc-val'>₹2.1L</div><div class='mc-lbl'>Revenue at Risk</div><div class='mc-d'>Dead stock items</div></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    fc1,fc2,_ = st.columns([1,1,3])
    with fc1: cat_f=st.selectbox("Category",CATEGORIES,key="tc")
    with fc2: urg_f=st.selectbox("Urgency",["All","HIGH","MEDIUM","LOW","DEAD_STOCK"],key="tu")

    filtered=[t for t in TRENDS if (cat_f=="All" or t["category"]==cat_f) and (urg_f=="All" or t["urgency"]==urg_f)]
    ca,cb=st.columns(2)
    for i,t in enumerate(filtered):
        col=ca if i%2==0 else cb
        if t["urgency"]=="HIGH": cc,bc="","bh"
        elif t["urgency"]=="MEDIUM": cc,bc="med","bm"
        elif t["urgency"]=="LOW": cc,bc="lo","bl"
        else: cc,bc="dead","bd"
        tags="".join([f"<span style='background:#f2f2f2;padding:1px 8px;border-radius:20px;font-size:0.6rem;margin-right:3px;color:#555;'>{x}</span>" for x in t["tags"]])
        with col:
            st.markdown(f"""<div class='tc {cc}'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                    <div><div class='tc-name'>{t['name']}</div><div class='tc-meta'>{t['category']} · {t['city']} · {t['direction']}</div></div>
                    <div style='font-size:1.7rem;font-weight:700;color:#0a0a0a;line-height:1;'>{t['heat']}</div>
                </div>
                <span class='badge {bc}'>{t['urgency'].replace('_',' ')}</span>
                <div style='color:#C41E3A;font-size:0.78rem;margin-bottom:6px;font-weight:600;'>{t['change']} demand</div>
                <div class='tc-desc'>{t['description']}</div>
                <div style='margin:8px 0 3px;font-size:0.58rem;color:#aaa;text-transform:uppercase;letter-spacing:0.1em;'>Heat Score</div>
                <div class='hbar'><div class='hfill' style='width:{t["heat"]}%'></div></div>
                <div style='margin-top:8px;'>{tags}</div>
                <div class='tc-insight'><strong>💡 Insight:</strong> {t['insight']}</div>
                <div style='font-size:0.65rem;color:#aaa;margin-top:8px;'>⏱ Peak ~{t['peak_weeks']} weeks</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Analytics</div><div class='stitle'>Trend Heat Comparison</div>", unsafe_allow_html=True)
    names=[t["name"] for t in TRENDS]; heats=[t["heat"] for t in TRENDS]
    bclrs=["#C41E3A" if h>80 else "#555" if h>60 else "#ccc" for h in heats]
    fig=go.Figure(go.Bar(x=heats,y=names,orientation='h',marker_color=bclrs,
        text=heats,textposition='outside',textfont=dict(color='#0a0a0a',size=11)))
    fig.update_layout(plot_bgcolor='white',paper_bgcolor='white',
        font=dict(family='Inter',size=11,color='#0a0a0a'),
        xaxis=dict(showgrid=False,showticklabels=False,range=[0,115]),
        yaxis=dict(showgrid=False,tickfont=dict(color='#0a0a0a')),
        margin=dict(l=10,r=40,t=8,b=8),height=320)
    st.plotly_chart(fig,use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FORECAST
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Forecast":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>◈ Predictive Analytics</div>
        <div class='mhead-title'>Demand Forecast</div>
        <div class='mhead-sub'>12-Week Outlook · Revenue · Audience Intelligence</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    data=get_forecast_data(); rev=get_revenue_data()

    c1,c2,c3,c4=st.columns(4)
    with c1: st.markdown("<div class='mc'><div class='mc-val'>+41%</div><div class='mc-lbl'>Peak Demand Surge</div><div class='mc-d'>Cargo Pants · W5</div></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='mc'><div class='mc-val'>₹2.45L</div><div class='mc-lbl'>June Revenue</div><div class='mc-d'>↑ 24% vs target</div></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='mc'><div class='mc-val'>198</div><div class='mc-lbl'>Units Sold June</div><div class='mc-d'>Best month ever</div></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='mc'><div class='mc-val'>W6</div><div class='mc-lbl'>Peak Week</div><div class='mc-d'>Highest demand</div></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Revenue vs Target</div><div class='stitle'>Monthly Performance</div>", unsafe_allow_html=True)
    fig_rev=go.Figure()
    fig_rev.add_trace(go.Bar(x=rev["months"],y=rev["revenue"],name="Actual",marker_color="#0a0a0a",
        text=[f"₹{v//1000}K" for v in rev["revenue"]],textposition='outside',textfont=dict(color='#0a0a0a',size=10)))
    fig_rev.add_trace(go.Scatter(x=rev["months"],y=rev["target"],name="Target",
        line=dict(color="#C41E3A",dash="dash",width=1.5),mode='lines+markers',marker=dict(size=6)))
    fig_rev.update_layout(plot_bgcolor='white',paper_bgcolor='white',
        font=dict(family='Inter',size=11,color='#0a0a0a'),
        legend=dict(orientation='h',y=1.08,font=dict(size=10),bgcolor='white'),
        yaxis=dict(showgrid=True,gridcolor='#f0f0f0',tickprefix='₹',tickfont=dict(color='#0a0a0a')),
        xaxis=dict(showgrid=False,tickfont=dict(color='#0a0a0a')),
        margin=dict(l=10,r=10,t=24,b=8),height=280)
    st.plotly_chart(fig_rev,use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ 12-Week Projection</div><div class='stitle'>Demand Curves</div>", unsafe_allow_html=True)
    prod_sel=st.multiselect("Products",list(data.keys())[1:],default=["Baggy Cargo Pants","Printed Maxi Dresses","Crochet Mini Skirts"])
    if prod_sel:
        palette=["#C41E3A","#0a0a0a","#888","#333","#ccc"]
        fig2=go.Figure()
        for i,prod in enumerate(prod_sel):
            fig2.add_trace(go.Scatter(x=data["weeks"],y=data[prod],name=prod,
                mode='lines+markers',line=dict(color=palette[i%len(palette)],width=2),marker=dict(size=5)))
        fig2.update_layout(plot_bgcolor='white',paper_bgcolor='white',
            font=dict(family='Inter',size=11,color='#0a0a0a'),
            legend=dict(orientation='h',y=1.08,font=dict(size=10),bgcolor='white'),
            xaxis=dict(showgrid=False,title="Week",tickfont=dict(color='#0a0a0a')),
            yaxis=dict(showgrid=True,gridcolor='#f0f0f0',title="Units",tickfont=dict(color='#0a0a0a')),
            margin=dict(l=10,r=10,t=24,b=8),height=320)
        st.plotly_chart(fig2,use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Audience Intelligence</div><div class='stitle'>Who Is Buying</div>", unsafe_allow_html=True)
    ca,cb=st.columns(2)
    with ca:
        fig_age=go.Figure(go.Pie(labels=list(AUDIENCE_DATA["age_groups"].keys()),
            values=list(AUDIENCE_DATA["age_groups"].values()),hole=0.5,
            marker_colors=["#0a0a0a","#C41E3A","#888","#555","#ccc"]))
        fig_age.update_layout(title=dict(text="Age Groups",font=dict(size=13,color='#0a0a0a')),
            paper_bgcolor='white',font=dict(color='#0a0a0a',size=11),margin=dict(l=10,r=10,t=36,b=8),height=260)
        st.plotly_chart(fig_age,use_container_width=True)
    with cb:
        fig_city=go.Figure(go.Pie(labels=list(AUDIENCE_DATA["cities"].keys()),
            values=list(AUDIENCE_DATA["cities"].values()),hole=0.5,
            marker_colors=["#C41E3A","#0a0a0a","#888","#555","#ccc"]))
        fig_city.update_layout(title=dict(text="Top Cities",font=dict(size=13,color='#0a0a0a')),
            paper_bgcolor='white',font=dict(color='#0a0a0a',size=11),margin=dict(l=10,r=10,t=36,b=8),height=260)
        st.plotly_chart(fig_city,use_container_width=True)

    st.markdown("""
    <div class='insight-box'>
        <strong>Your Audience:</strong> 68% women aged 18–34, based primarily in Hyderabad (45%) and Bangalore (22%).
        They shop for Bottoms (34%), Tops (28%), and Dresses (20%). They are driven by Instagram and Pinterest trends.
        <strong>Your niche: casual-to-festive women's fashion for Gen-Z and millennials.</strong>
        Focus on crochet, maxi dresses, cargo pants, and ethnic fusion — not formal or corporate wear.
    </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MY STOCK
# ══════════════════════════════════════════════════════════════════════════════
elif page == "My Stock":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>◉ Inventory Control</div>
        <div class='mhead-title'>My Stock</div>
        <div class='mhead-sub'>Live Inventory · Auto Alerts · AI Reorder Suggestions · Audience Insights</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    reorder=[i for i in INVENTORY if i["status"]=="REORDER NOW"]
    dead=[i for i in INVENTORY if i["status"]=="DEAD STOCK"]
    over=[i for i in INVENTORY if i["status"]=="OVERSTOCK"]

    if reorder: st.markdown(f"<div class='al al-r'>🚨 <strong>REORDER NOW:</strong> {', '.join([i['name'].split(' - ')[0] for i in reorder])} — running critically low.</div>", unsafe_allow_html=True)
    if dead:    st.markdown(f"<div class='al al-g'>⚠️ <strong>DEAD STOCK:</strong> {', '.join([i['name'].split(' - ')[0] for i in dead])} — start clearance immediately.</div>", unsafe_allow_html=True)
    if over:    st.markdown(f"<div class='al al-g'>📦 <strong>OVERSTOCK:</strong> {', '.join([i['name'].split(' - ')[0] for i in over])} — pause reordering.</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='insight-box' style='margin-bottom:20px;'>
        <strong>Your Niche Profile:</strong> You serve Gen-Z and millennial women (18–34) in Hyderabad who buy casual, boho, and festive fashion.
        Your fast-moving categories are Bottoms, Dresses, and Tops. <strong>Trend Score</strong> tells you how well each item matches what your audience is buying right now — 
        above 75 means stock urgently, below 50 means reduce or clear.
    </div>""", unsafe_allow_html=True)

    total_val=sum(i["qty"]*i["cost"] for i in INVENTORY)
    c1,c2,c3,c4=st.columns(4)
    with c1: st.markdown(f"<div class='mc'><div class='mc-val'>₹{total_val//1000}K</div><div class='mc-lbl'>Total Stock Value</div><div class='mc-d'>At cost</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='mc'><div class='mc-val'>{len(reorder)}</div><div class='mc-lbl'>Reorder Alerts</div><div class='mc-d'>Act today</div></div>", unsafe_allow_html=True)
    with c3:
        dv=sum(i['qty']*i['cost'] for i in dead)
        st.markdown(f"<div class='mc'><div class='mc-val'>₹{dv//1000}K</div><div class='mc-lbl'>Dead Stock Value</div><div class='mc-d'>Run clearance</div></div>", unsafe_allow_html=True)
    with c4:
        fast=sum(1 for i in INVENTORY if i["velocity"]=="Fast")
        st.markdown(f"<div class='mc'><div class='mc-val'>{fast}</div><div class='mc-lbl'>Fast-Moving SKUs</div><div class='mc-d'>High demand</div></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ All SKUs</div><div class='stitle'>Inventory Dashboard</div>", unsafe_allow_html=True)
    cat_s=st.selectbox("Filter",CATEGORIES,key="sc")
    inv_f=INVENTORY if cat_s=="All" else [i for i in INVENTORY if i["category"]==cat_s]

    for item in inv_f:
        s=item["status"]
        icon="🔴" if s=="REORDER NOW" else "🟢" if s=="HEALTHY" else "🟡" if s=="OVERSTOCK" else "⚫"
        pct=min(100,int(item["qty"]/max(item["reorder_point"]*2,1)*100))
        bc="#C41E3A" if pct<35 else "#888" if pct<60 else "#2E7D32"
        margin=int((item["selling_price"]-item["cost"])/item["selling_price"]*100)
        score=item["trend_alignment"]
        score_color="#C41E3A" if score>80 else "#555" if score>60 else "#aaa"

        with st.expander(f"{icon}  {item['name']}  ·  {s}"):
            c1,c2,c3,c4,c5=st.columns(5)
            c1.metric("In Stock",f"{item['qty']} units")
            c2.metric("Reorder At",f"{item['reorder_point']} units")
            c3.metric("Days Left",f"{item['days_of_stock']}")
            c4.metric("Velocity",item["velocity"])
            c5.metric("Margin",f"{margin}%")

            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:12px;margin:10px 0 6px;'>
                <div style='flex:1;'>
                    <div style='font-size:0.6rem;color:#aaa;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px;'>Stock Level</div>
                    <div style='background:#eee;border-radius:2px;height:6px;'>
                        <div style='width:{pct}%;height:6px;border-radius:2px;background:{bc};'></div>
                    </div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:0.58rem;color:#aaa;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:2px;'>Trend Score</div>
                    <div style='font-family:"Playfair Display",serif;font-size:1.4rem;font-weight:700;color:{score_color};line-height:1;'>{score}</div>
                    <div style='font-size:0.58rem;color:#aaa;'>/100</div>
                </div>
            </div>""", unsafe_allow_html=True)

            st.markdown(f"<div class='insight-box'>{item['insight']}</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Visual</div><div class='stitle'>Stock vs Reorder Point</div>", unsafe_allow_html=True)
    skus=[i["sku"] for i in INVENTORY]; qtys=[i["qty"] for i in INVENTORY]; rpts=[i["reorder_point"] for i in INVENTORY]
    fig4=go.Figure()
    fig4.add_trace(go.Bar(name='Stock',x=skus,y=qtys,
        marker_color=['#C41E3A' if q<r else '#0a0a0a' for q,r in zip(qtys,rpts)],
        text=qtys,textposition='outside',textfont=dict(color='#0a0a0a',size=10)))
    fig4.add_trace(go.Scatter(name='Reorder Point',x=skus,y=rpts,mode='lines+markers',
        line=dict(color='#888',dash='dash',width=1.5),marker=dict(size=6)))
    fig4.update_layout(plot_bgcolor='white',paper_bgcolor='white',
        font=dict(family='Inter',size=11,color='#0a0a0a'),
        legend=dict(orientation='h',y=1.08,bgcolor='white'),
        xaxis=dict(showgrid=False,tickfont=dict(color='#0a0a0a')),
        yaxis=dict(showgrid=True,gridcolor='#f0f0f0',title="Units",tickfont=dict(color='#0a0a0a')),
        margin=dict(l=10,r=10,t=24,b=8),height=280)
    st.plotly_chart(fig4,use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PRICING
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Pricing":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>◎ Margin Intelligence</div>
        <div class='mhead-title'>Pricing Studio</div>
        <div class='mhead-sub'>Market Benchmarking · Competitor Analysis · Audience-Aware Pricing</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    st.markdown("""
    <div class='insight-box' style='margin-bottom:20px;'>
        <strong>Your Pricing Context:</strong> Your audience is Gen-Z and millennial women aged 18–34 in Hyderabad.
        They have a price sweet spot of <strong>₹799–1,799</strong> — they will pay premium for items that feel trendy but won't go above ₹2,000 for casual wear.
        Use this to set prices: trending items can go to the upper range, slow-movers need to be priced competitively or cleared.
    </div>""", unsafe_allow_html=True)

    c1,c2,c3=st.columns(3)
    with c1: st.markdown("<div class='mc'><div class='mc-val'>₹950</div><div class='mc-lbl'>Avg Market Price</div><div class='mc-d'>Across all SKUs</div></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='mc'><div class='mc-val'>5</div><div class='mc-lbl'>Price Up Opportunities</div><div class='mc-d'>+₹18K/month margin</div></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='mc'><div class='mc-val'>64%</div><div class='mc-lbl'>Avg Gross Margin</div><div class='mc-d'>Trending products</div></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Per Product</div><div class='stitle'>Price Positioning</div>", unsafe_allow_html=True)

    for p in PRICING:
        opp=p["opportunity"]
        oc="#C41E3A" if "UP" in opp else "#888" if "Reduce" in opp else "#555"
        with st.expander(f"{p['product']}  ·  Your Price ₹{p['your_price']}  ·  {opp}"):
            c1,c2,c3,c4=st.columns(4)
            c1.metric("Your Price",f"₹{p['your_price']}")
            c2.metric("Market Avg",f"₹{p['market_avg']}",delta=f"{p['your_price']-p['market_avg']:+}")
            c3.metric("Suggested",f"₹{p['suggested']}")
            c4.metric("Margin",f"{p['margin_pct']}%")
            rs=p["high"]-p["low"]
            yp=int((p["your_price"]-p["low"])/rs*100) if rs else 50
            sp=int((p["suggested"]-p["low"])/rs*100) if rs else 50
            st.markdown(f"""
            <div style='margin:10px 0 3px;font-size:0.6rem;color:#aaa;text-transform:uppercase;'>Market Range · Low ₹{p['low']} → High ₹{p['high']}</div>
            <div style='position:relative;background:#eee;border-radius:2px;height:8px;'>
                <div style='position:absolute;left:{yp}%;top:-3px;width:4px;height:14px;background:#0a0a0a;border-radius:1px;'></div>
                <div style='position:absolute;left:{sp}%;top:-3px;width:4px;height:14px;background:#C41E3A;border-radius:1px;'></div>
            </div>
            <div style='display:flex;justify-content:space-between;font-size:0.65rem;margin-top:5px;color:#555;'>
                <span>■ Your price: ₹{p['your_price']}</span><span style='color:#C41E3A;'>■ Suggested: ₹{p['suggested']}</span>
            </div>""", unsafe_allow_html=True)
            st.markdown(f"<div class='insight-box' style='margin-top:10px;'><strong>💡 Tip:</strong> {p['tip']}</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Visual</div><div class='stitle'>Margin Breakdown</div>", unsafe_allow_html=True)
    prods=[p["product"] for p in PRICING]; margins=[p["margin_pct"] for p in PRICING]
    mc2=["#0a0a0a" if m>60 else "#888" if m>40 else "#C41E3A" for m in margins]
    fig5=go.Figure()
    fig5.add_trace(go.Bar(x=prods,y=margins,marker_color=mc2,
        text=[f"{m}%" for m in margins],textposition='outside',textfont=dict(color='#0a0a0a',size=10)))
    fig5.add_hline(y=50,line_dash="dash",line_color="#888",
        annotation_text="Min target 50%",annotation_font_color="#555",annotation_font_size=10)
    fig5.update_layout(plot_bgcolor='white',paper_bgcolor='white',
        font=dict(family='Inter',size=11,color='#0a0a0a'),
        yaxis=dict(showgrid=True,gridcolor='#f0f0f0',title="Gross Margin %",range=[0,90],tickfont=dict(color='#0a0a0a')),
        xaxis=dict(showgrid=False,tickangle=-18,tickfont=dict(color='#0a0a0a')),
        margin=dict(l=10,r=10,t=16,b=70),height=320)
    st.plotly_chart(fig5,use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MARKETPLACE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Marketplace":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>◇ Supplier Network</div>
        <div class='mhead-title'>Wholesaler Marketplace</div>
        <div class='mhead-sub'>Verified Suppliers · Pan India · Message · Order · Connect</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    cs,cc,cm=st.columns([2,1,1])
    with cs: search=st.text_input("Search suppliers or products",placeholder="cargo pants, Surat, linen, dresses…")
    with cc: city_f=st.selectbox("City",["All","Surat","Jaipur","Mumbai","Tirupur"])
    with cm: cat_f=st.selectbox("Category",CATEGORIES,key="wc")

    st.markdown("<hr>", unsafe_allow_html=True)

    for wh in WHOLESALERS:
        if city_f!="All" and wh["city"]!=city_f: continue
        if search and search.lower() not in wh["name"].lower() and not any(search.lower() in p["name"].lower() for p in wh["products"]): continue
        stars="★"*int(wh["rating"])+"☆"*(5-int(wh["rating"]))
        tags_html="".join([f"<span class='wtag'>{t}</span>" for t in wh["tags"]])

        st.markdown(f"""<div class='wc'>
            <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                <div>
                    <div class='wc-name'>{wh['name']}</div>
                    <div class='wc-meta'>📍 {wh['city']} · {wh['speciality']} · {wh['years']} years in business</div>
                    <div class='wc-about'>{wh['about']}</div>
                    <div style='margin-top:8px;'>{tags_html}</div>
                </div>
                <div style='text-align:right;min-width:100px;'>
                    <div style='color:#C41E3A;font-size:1rem;'>{stars}</div>
                    <div style='font-size:0.68rem;color:#555;margin-top:2px;'>{wh['rating']}/5 · ✅ Verified</div>
                    <div style='font-size:0.62rem;color:#888;margin-top:3px;'>Min order ₹{wh['min_order_value']//1000}K</div>
                </div>
            </div>
            <div style='margin-top:12px;display:flex;gap:8px;'>
        </div>
        </div>""", unsafe_allow_html=True)

        mb1,mb2,_ = st.columns([1,1,5])
        with mb1:
            if st.button(f"💬 Message {wh['name'].split()[0]}", key=f"msg_wh_{wh['id']}"):
                st.session_state.page="Messages"
                st.session_state.active_contact=wh["username"]
                st.rerun()
        with mb2:
            if st.button(f"📋 View All Products", key=f"view_wh_{wh['id']}"):
                pass

        for prod in wh["products"]:
            if cat_f!="All" and prod["category"]!=cat_f: continue
            with st.expander(f"  {prod['name']}  ·  MOQ {prod['moq']} units  ·  ₹{prod['price_per_unit']}/unit"):
                c1,c2,c3,c4,c5=st.columns(5)
                c1.metric("Price/Unit",f"₹{prod['price_per_unit']}")
                c2.metric("MOQ",f"{prod['moq']} units")
                c3.metric("Fabric",prod["fabric"])
                c4.metric("Lead Time",f"{prod['lead_days']} days")
                c5.metric("Colors",f"{prod['colors']} options")

                st.markdown(f"""
                <div style='background:#f9f9f9;padding:10px 14px;font-size:0.76rem;color:#0a0a0a;margin-top:8px;line-height:1.6;'>
                    <strong>Description:</strong> {prod['description']}<br>
                    <strong>Sizes:</strong> {prod['sizes']} &nbsp;·&nbsp;
                    <strong>Min Order:</strong> {prod['moq']} × ₹{prod['price_per_unit']} = <strong>₹{prod['moq']*prod['price_per_unit']:,}</strong>
                </div>""", unsafe_allow_html=True)

                pb1,pb2,pb3,_=st.columns([1,1,1,3])
                with pb1:
                    if st.button("📩 Enquire",key=f"e_{wh['id']}_{prod['name'][:6]}"): st.success(f"Enquiry sent to {wh['name']}!")
                with pb2:
                    if st.button("🛒 Order",key=f"o_{wh['id']}_{prod['name'][:6]}"): st.success(f"Order placed with {wh['name']}!")
                with pb3:
                    if st.button("💬 Message",key=f"m_{wh['id']}_{prod['name'][:6]}"):
                        st.session_state.page="Messages"
                        st.session_state.active_contact=wh["username"]
                        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MESSAGES — Social media style
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Messages":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>✉ Direct Messaging</div>
        <div class='mhead-title'>Messages</div>
        <div class='mhead-sub'>Connect with buyers and sellers · All messages safety monitored</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    uname=st.session_state.username
    my_msgs=[m for m in st.session_state.messages if m["from"]==uname or m["to"]==uname]
    contacts=set()
    for m in my_msgs:
        contacts.add(m["to"] if m["from"]==uname else m["from"])
    if not contacts:
        contacts={"seller1"} if role=="buyer" else {"buyer1"}

    all_users=[u for u in st.session_state.user_db if u!=uname]
    contact_options=list(contacts)+[u for u in all_users if u not in contacts]

    if st.session_state.active_contact and st.session_state.active_contact in contact_options:
        default_idx=contact_options.index(st.session_state.active_contact)
    else:
        default_idx=0

    col_contacts, col_chat = st.columns([1,3])

    with col_contacts:
        st.markdown("<div style='font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#888;margin-bottom:10px;font-weight:600;'>Conversations</div>", unsafe_allow_html=True)
        for contact in contact_options:
            cinfo=st.session_state.user_db.get(contact,{})
            cname=cinfo.get("name",contact)
            cbiz=cinfo.get("business","")
            initials="".join([w[0].upper() for w in cname.split()[:2]])
            last_msgs=[m for m in st.session_state.messages if (m["from"]==uname and m["to"]==contact) or (m["from"]==contact and m["to"]==uname)]
            last_text=last_msgs[-1]["text"][:30]+"…" if last_msgs else "Start a conversation"
            is_active=(st.session_state.active_contact==contact or (st.session_state.active_contact is None and contact==contact_options[0]))
            active_style="background:#fff0f0;border-left:3px solid #C41E3A;" if is_active else "background:#f9f9f9;border-left:3px solid transparent;"
            st.markdown(f"""
            <div style='{active_style}padding:12px 14px;border-bottom:1px solid #eee;cursor:pointer;display:flex;align-items:center;gap:10px;margin-bottom:1px;'>
                <div style='width:36px;height:36px;border-radius:50%;background:#0a0a0a;display:flex;align-items:center;justify-content:center;color:#fff;font-size:0.72rem;font-weight:600;flex-shrink:0;'>{initials}</div>
                <div style='overflow:hidden;'>
                    <div style='font-size:0.8rem;font-weight:600;color:#0a0a0a;'>{cname}</div>
                    <div style='font-size:0.65rem;color:#888;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:140px;'>{last_text}</div>
                </div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Open", key=f"open_{contact}", help=cname):
                st.session_state.active_contact=contact; st.rerun()

    with col_chat:
        sel_contact=st.session_state.active_contact if st.session_state.active_contact else contact_options[0]
        cinfo=st.session_state.user_db.get(sel_contact,{})
        cname=cinfo.get("name",sel_contact)
        cbiz=cinfo.get("business","")
        crole=cinfo.get("role","").upper()
        initials="".join([w[0].upper() for w in cname.split()[:2]])

        st.markdown(f"""
        <div style='background:#0a0a0a;padding:12px 16px;display:flex;align-items:center;gap:12px;margin-bottom:0;'>
            <div style='width:36px;height:36px;border-radius:50%;background:#C41E3A;display:flex;align-items:center;justify-content:center;color:#fff;font-size:0.72rem;font-weight:600;flex-shrink:0;'>{initials}</div>
            <div>
                <div style='font-size:0.88rem;font-weight:600;color:#fff;'>{cname}</div>
                <div style='font-size:0.62rem;color:#C41E3A;'>{cbiz} · {crole}</div>
            </div>
            <div style='margin-left:auto;'>
                <div style='width:8px;height:8px;border-radius:50%;background:#2E7D32;display:inline-block;'></div>
                <span style='font-size:0.62rem;color:#888;margin-left:4px;'>Online</span>
            </div>
        </div>""", unsafe_allow_html=True)

        convo=[m for m in st.session_state.messages if
               (m["from"]==uname and m["to"]==sel_contact) or
               (m["from"]==sel_contact and m["to"]==uname)]

        st.markdown("<div style='background:#f9f9f9;padding:16px;min-height:320px;border:1px solid #eee;border-top:none;'>", unsafe_allow_html=True)
        if not convo:
            st.markdown(f"<div style='text-align:center;padding:48px 20px;color:#aaa;font-size:0.78rem;'>Send {cname} a message to start the conversation</div>", unsafe_allow_html=True)
        for m in convo:
            sname=st.session_state.user_db.get(m["from"],{}).get("name",m["from"])
            sin="".join([w[0].upper() for w in sname.split()[:2]])
            if m["from"]==uname:
                st.markdown(f"""
                <div style='display:flex;justify-content:flex-end;margin:8px 0;'>
                    <div>
                        <div style='background:#0a0a0a;color:#fff;border-radius:18px 18px 4px 18px;padding:10px 14px;max-width:65%;font-size:0.8rem;line-height:1.45;'>{m['text']}</div>
                        <div style='font-size:0.58rem;color:#bbb;margin-top:3px;text-align:right;'>{m['time']}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='display:flex;align-items:flex-end;gap:8px;margin:8px 0;'>
                    <div style='width:28px;height:28px;border-radius:50%;background:#C41E3A;display:flex;align-items:center;justify-content:center;color:#fff;font-size:0.6rem;font-weight:600;flex-shrink:0;'>{sin}</div>
                    <div>
                        <div style='background:#fff;color:#0a0a0a;border-radius:18px 18px 18px 4px;padding:10px 14px;max-width:65%;font-size:0.8rem;line-height:1.45;border:1px solid #eee;'>{m['text']}</div>
                        <div style='font-size:0.58rem;color:#bbb;margin-top:3px;'>{m['time']}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        mc1,mc2=st.columns([5,1])
        with mc1: new_msg=st.text_input("",placeholder=f"Message {cname}…",key="nm",label_visibility="collapsed")
        with mc2:
            if st.button("Send →",key="snd"):
                if new_msg.strip():
                    flagged=check_illegal_content(new_msg)
                    if flagged:
                        st.markdown(f"<div class='al al-red'>🚫 Blocked — illegal content detected: {', '.join(flagged)}</div>", unsafe_allow_html=True)
                    else:
                        now=datetime.now().strftime("%I:%M %p")
                        st.session_state.messages.append({"id":len(st.session_state.messages)+1,"from":uname,"to":sel_contact,"text":new_msg,"time":now,"date":"Today"})
                        st.rerun()

    st.markdown("<div class='al al-b' style='margin-top:12px;font-size:0.72rem;'>🛡️ All messages monitored. Illegal content or fraud = immediate suspension.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# AI ADVISOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "AI Advisor":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>✦ Powered by AI</div>
        <div class='mhead-title'>AI Business Advisor</div>
        <div class='mhead-sub'>Ask anything · Knows your inventory · Trend-aware · Always available</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:#0a0a0a;color:#fff;padding:16px 20px;margin-bottom:20px;border-left:3px solid #C41E3A;'>
        <div style='font-family:"Playfair Display",serif;font-size:1rem;font-weight:700;margin-bottom:4px;'>Hello, {user_info.get('name','there').split()[0]} 👋</div>
        <div style='font-size:0.76rem;color:#888;line-height:1.5;'>I am Trendora AI. I know your full inventory, current trend data for Hyderabad, your pricing vs the market, your target audience profile, and your revenue numbers. Ask me anything.</div>
    </div>""", unsafe_allow_html=True)

    quick_qs=["What should I reorder this week?","Which dead stock to clear?","How to improve margins?","Best wholesaler for cargo pants?","Who is my target audience?","What is trending right now?","Revenue performance?","What to stock for festive season?"]
    st.markdown("<div style='font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#888;margin-bottom:10px;font-weight:600;'>Quick Questions</div>", unsafe_allow_html=True)
    qcols=st.columns(4)
    for i,q in enumerate(quick_qs):
        with qcols[i%4]:
            if st.button(q,key=f"q{i}"):
                st.session_state.chat_history.append({"role":"user","text":q})
                st.session_state.chat_history.append({"role":"bot","text":get_ai_response(q,role)})
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<div class='cwrap'>", unsafe_allow_html=True)
    if not st.session_state.chat_history:
        st.markdown("<div style='text-align:center;color:#aaa;padding:32px;font-size:0.78rem;'>Click a quick question above or type below ↓</div>", unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        if msg["role"]=="user":
            st.markdown(f"<div style='text-align:right;margin:8px 0;'><div class='cs' style='text-align:right;'>You</div><div class='cu'>{msg['text']}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='margin:8px 0;'><div class='cs'>Trendora AI</div><div class='cb'>{msg['text']}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    ai1,ai2,ai3=st.columns([5,1,1])
    with ai1: user_q=st.text_input("",placeholder="Ask Trendora AI anything about your business…",key="aiq",label_visibility="collapsed")
    with ai2:
        if st.button("Ask →",key="ask"):
            if user_q.strip():
                flagged=check_illegal_content(user_q)
                if flagged:
                    st.markdown(f"<div class='al al-red'>🚫 Flagged query: {', '.join(flagged)}</div>", unsafe_allow_html=True)
                else:
                    st.session_state.chat_history.append({"role":"user","text":user_q})
                    st.session_state.chat_history.append({"role":"bot","text":get_ai_response(user_q,role)})
                    st.rerun()
    with ai3:
        if st.button("Clear",key="clr"): st.session_state.chat_history=[]; st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Auto Intelligence</div><div class='stitle'>This Week's Digest</div>", unsafe_allow_html=True)
    digests=[
        ("#C41E3A","🔴 URGENT","Stock out in 4 days","Baggy Cargo Pants, Crochet Skirts, and Maxi Dresses will hit zero stock before the weekend. Contact Rajesh Textiles and Femina Fashion House today."),
        ("#0a0a0a","💰 OPPORTUNITY","₹18K margin available","Raise prices on 5 products to market average — adds ₹18,000/month in pure margin at zero additional cost."),
        ("#888","📦 ACTION","₹70K dead stock to clear","78 blazers, 90+ days unsold. 30% flash sale this week recovers ₹81K and frees capital for trending items."),
        ("#C41E3A","📈 TREND","Crochet peaks in 3 weeks","Your highest-margin item (71%). Only 6 units left. Order 75 units from Femina Fashion House immediately — this is your best profit window."),
    ]
    dc=st.columns(2)
    for i,(color,label,title,body) in enumerate(digests):
        with dc[i%2]:
            st.markdown(f"""
            <div style='background:#fff;border-left:3px solid {color};padding:16px 18px;margin-bottom:12px;box-shadow:0 1px 8px rgba(0,0,0,0.06);'>
                <div style='font-size:0.58rem;letter-spacing:0.15em;text-transform:uppercase;color:{color};font-weight:700;margin-bottom:4px;'>{label}</div>
                <div style='font-family:"Playfair Display",serif;font-size:0.95rem;font-weight:700;color:#0a0a0a;margin-bottom:6px;'>{title}</div>
                <div style='font-size:0.76rem;color:#444;line-height:1.55;'>{body}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# NEWS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "News":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>📰 Industry Intelligence</div>
        <div class='mhead-title'>Fashion News</div>
        <div class='mhead-sub'>Current market updates · Industry reports · June 2025</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    impact_f=st.selectbox("Filter by Impact",["All","HIGH","MEDIUM","LOW"])
    fn=FASHION_NEWS if impact_f=="All" else [n for n in FASHION_NEWS if n["impact"]==impact_f]

    for news in fn:
        ic="#C41E3A" if news["impact"]=="HIGH" else "#888" if news["impact"]=="MEDIUM" else "#ccc"
        st.markdown(f"""
        <div class='nc'>
            <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:5px;'>
                <div class='nc-h'>{news['headline']}</div>
                <span style='background:{ic};color:#fff;padding:2px 10px;border-radius:20px;font-size:0.58rem;letter-spacing:0.1em;text-transform:uppercase;font-weight:600;white-space:nowrap;margin-left:14px;flex-shrink:0;'>{news['impact']}</span>
            </div>
            <div class='nc-m'>{news['source']} · {news['date']}</div>
            <div class='nc-b'>{news['summary']}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MY PRODUCTS (Seller)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "My Products":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>◆ Seller Dashboard</div>
        <div class='mhead-title'>My Products</div>
        <div class='mhead-sub'>Manage listings · Track enquiries · Upload new products</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    my_wh=[w for w in WHOLESALERS if w.get("username")==st.session_state.username]
    if my_wh:
        wh=my_wh[0]
        st.markdown(f"""<div class='wc'>
            <div class='wc-name'>{wh['name']}</div>
            <div class='wc-meta'>📍 {wh['city']} · {wh['speciality']} · ⭐ {wh['rating']}/5 · ✅ Verified</div>
            <div class='wc-about'>{wh['about']}</div>
            <div style='margin-top:8px;'>{"".join([f"<span class='wtag'>{t}</span>" for t in wh['tags']])}</div>
        </div>""", unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)
        with c1: st.markdown(f"<div class='mc'><div class='mc-val'>{len(wh['products'])}</div><div class='mc-lbl'>Active Listings</div><div class='mc-d'>Live on marketplace</div></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='mc'><div class='mc-val'>3</div><div class='mc-lbl'>New Enquiries</div><div class='mc-d'>Respond within 24h</div></div>", unsafe_allow_html=True)
        with c3:
            tv=sum(p["moq"]*p["price_per_unit"] for p in wh["products"])
            st.markdown(f"<div class='mc'><div class='mc-val'>₹{tv//1000}K</div><div class='mc-lbl'>Min Order Value</div><div class='mc-d'>All products</div></div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='eye'>◆ Current Listings</div><div class='stitle'>Your Products</div>", unsafe_allow_html=True)
        for prod in wh["products"]:
            with st.expander(f"  {prod['name']}  ·  ₹{prod['price_per_unit']}/unit  ·  MOQ {prod['moq']}"):
                c1,c2,c3,c4=st.columns(4)
                c1.metric("Price/Unit",f"₹{prod['price_per_unit']}")
                c2.metric("MOQ",prod["moq"])
                c3.metric("Lead",f"{prod['lead_days']}d")
                c4.metric("Colors",prod["colors"])
                st.markdown(f"<div style='background:#f7f7f7;padding:10px;font-size:0.76rem;color:#0a0a0a;margin-top:8px;line-height:1.5;'>Fabric: {prod['fabric']} · Sizes: {prod['sizes']}<br>{prod['description']}</div>", unsafe_allow_html=True)
    else:
        c1,c2,c3=st.columns(3)
        with c1: st.markdown("<div class='mc'><div class='mc-val'>0</div><div class='mc-lbl'>Active Listings</div><div class='mc-d'>Add your first</div></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='mc'><div class='mc-val'>0</div><div class='mc-lbl'>Enquiries</div><div class='mc-d'>List to receive</div></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='mc'><div class='mc-val'>New</div><div class='mc-lbl'>Account</div><div class='mc-d'>Get verified</div></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Upload New</div><div class='stitle'>List a Product</div>", unsafe_allow_html=True)
    with st.form("np"):
        np_name=st.text_input("Product Name",placeholder="e.g. Baggy Cargo Pants (Bulk)")
        c1,c2=st.columns(2)
        with c1:
            np_price=st.number_input("Price per Unit (₹)",min_value=1,value=300)
            np_moq=st.number_input("MOQ (units)",min_value=1,value=50)
            np_lead=st.number_input("Lead Time (days)",min_value=1,value=7)
        with c2:
            np_fabric=st.text_input("Fabric",placeholder="Cotton-Poly Blend")
            np_sizes=st.text_input("Sizes",placeholder="S-XXL")
            np_colors=st.number_input("Number of Colors",min_value=1,value=5)
        np_desc=st.text_area("Description",placeholder="Describe your product in detail…",height=80)
        np_img=st.text_input("Product Image URL (optional)",placeholder="https://…")
        if st.form_submit_button("List Product →") and np_name:
            flagged=check_illegal_content(np_name+" "+np_desc)
            if flagged:
                st.markdown(f"<div class='al al-red'>🚫 Blocked — flagged content: {', '.join(flagged)}</div>", unsafe_allow_html=True)
            else:
                st.success(f"✅ '{np_name}' is now live on Trendora Marketplace! Buyers across India can find and order your product.")
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ORDERS (Seller)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Orders":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>◆ Order Management</div>
        <div class='mhead-title'>Orders</div>
        <div class='mhead-sub'>Incoming orders · Confirm · Dispatch · Track</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    c1,c2,c3=st.columns(3)
    with c1: st.markdown("<div class='mc'><div class='mc-val'>3</div><div class='mc-lbl'>New Orders</div><div class='mc-d'>Action required</div></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='mc'><div class='mc-val'>₹1.2L</div><div class='mc-lbl'>This Month</div><div class='mc-d'>↑ 18% vs last</div></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='mc'><div class='mc-val'>7</div><div class='mc-lbl'>Pending Dispatch</div><div class='mc-d'>Ship within 48h</div></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Incoming</div><div class='stitle'>Order Queue</div>", unsafe_allow_html=True)
    orders=[
        {"id":"ORD-001","buyer":"Priya Boutique","product":"Baggy Cargo Pants","qty":100,"value":32000,"status":"New","date":"Today"},
        {"id":"ORD-002","buyer":"Ananya Fashion House","product":"Linen Trousers","qty":50,"value":14000,"status":"Confirmed","date":"Yesterday"},
        {"id":"ORD-003","buyer":"StyleHub Hyderabad","product":"Baggy Cargo Pants","qty":75,"value":24000,"status":"Dispatched","date":"3 days ago"},
    ]
    for o in orders:
        sc="#C41E3A" if o["status"]=="New" else "#888" if o["status"]=="Confirmed" else "#2E7D32"
        with st.expander(f"{o['id']}  ·  {o['buyer']}  ·  ₹{o['value']:,}  ·  {o['status']}"):
            c1,c2,c3,c4=st.columns(4)
            c1.metric("Qty",f"{o['qty']} units")
            c2.metric("Value",f"₹{o['value']:,}")
            c3.metric("Date",o["date"])
            c4.metric("Status",o["status"])
            st.markdown(f"<div style='margin-top:8px;padding:8px 12px;background:#f7f7f7;border-left:2px solid {sc};font-size:0.76rem;color:#0a0a0a;font-weight:600;'>Status: {o['status']}</div>", unsafe_allow_html=True)
            if o["status"]=="New":
                b1,b2,_=st.columns([1,1,4])
                with b1:
                    if st.button("✅ Confirm",key=f"c_{o['id']}"): st.success("Order confirmed!")
                with b2:
                    if st.button("❌ Decline",key=f"d_{o['id']}"): st.error("Order declined.")
    st.markdown("</div>", unsafe_allow_html=True)

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='border-top:1px solid #eee;text-align:center;padding:18px;font-size:0.58rem;color:#ccc;letter-spacing:0.16em;text-transform:uppercase;background:#fff;'>
    Trendora · Fashion Intelligence Platform · All activity monitored · © 2025
</div>""", unsafe_allow_html=True)
