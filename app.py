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
    CATEGORIES, MESSAGES, FASHION_NEWS, AUDIENCE_DATA,
    check_illegal_content, get_ai_response
)

st.set_page_config(page_title="Trendora", page_icon="◆", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; font-weight: 300; }
[data-testid="stSidebar"] { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
[data-testid="stAppViewContainer"] { padding-top: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
.stDeployButton { display: none !important; }

/* ── COLOUR TOKENS ── */
/* BG-BLACK  = #0a0a0a  TEXT = #fff or #C41E3A */
/* BG-RED    = #C41E3A  TEXT = #fff or #0a0a0a  */
/* BG-WHITE  = #fff     TEXT = #0a0a0a or #C41E3A */

/* ── NAV — Vogue-style thin strip ── */
.tnav {
    background: #0a0a0a;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 36px;
    border-bottom: 1px solid #222;
    position: sticky;
    top: 0;
    z-index: 999;
}
.tnav-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 600;
    color: #fff;
    letter-spacing: 0.04em;
    white-space: nowrap;
}
.tnav-logo em { color: #C41E3A; font-style: normal; }
.tnav-center {
    display: flex;
    gap: 0;
    align-items: center;
}
.tnav-link {
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #888;
    padding: 0 14px;
    border-right: 1px solid #222;
    line-height: 44px;
    cursor: pointer;
    transition: color 0.15s;
    white-space: nowrap;
    font-weight: 400;
}
.tnav-link:first-child { border-left: 1px solid #222; }
.tnav-link:hover { color: #fff; }
.tnav-link.active { color: #fff; }
.tnav-right {
    font-size: 0.62rem;
    color: #555;
    letter-spacing: 0.06em;
    white-space: nowrap;
}
.tnav-right strong { color: #C41E3A; font-weight: 400; }

/* ── NAV STREAMLIT BUTTONS (hidden visually, used for logic) ── */
.nav-row { display: flex; gap: 4px; padding: 8px 36px; background: #fff; border-bottom: 1px solid #eee; }

/* ── MASTHEAD ── */
.mhead {
    background: #0a0a0a;
    padding: 36px 36px 28px;
    border-bottom: 2px solid #C41E3A;
    margin-bottom: 28px;
}
.mhead-eye { font-size: 0.6rem; letter-spacing: 0.22em; text-transform: uppercase; color: #C41E3A; margin-bottom: 6px; font-weight: 400; }
.mhead-title { font-family: 'Playfair Display', serif; font-size: 2.6rem; font-weight: 600; color: #fff; line-height: 1.05; }
.mhead-sub { font-size: 0.72rem; color: #555; margin-top: 8px; letter-spacing: 0.04em; font-weight: 300; }

/* ── PAGE WRAP ── */
.pwrap { padding: 0 36px 48px; }

/* ── METRIC CARDS ── */
.mc { background: #0a0a0a; padding: 20px 18px; margin-bottom: 8px; border-radius: 1px; }
.mc-val { font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 600; color: #fff; line-height: 1; }
.mc-lbl { font-size: 0.58rem; letter-spacing: 0.16em; text-transform: uppercase; color: #555; margin-top: 4px; font-weight: 400; }
.mc-d { font-size: 0.72rem; color: #C41E3A; margin-top: 5px; font-weight: 400; }

/* ── TREND CARDS ── */
.tc { background: #fff; border-left: 3px solid #C41E3A; padding: 18px; margin-bottom: 12px; box-shadow: 0 1px 6px rgba(0,0,0,0.07); }
.tc.med { border-left-color: #888; }
.tc.lo  { border-left-color: #ccc; }
.tc.dead{ border-left-color: #e0e0e0; }
.tc-name { font-family: 'Playfair Display', serif; font-size: 1.05rem; font-weight: 600; color: #0a0a0a; margin-bottom: 3px; }
.tc-meta { font-size: 0.68rem; color: #888; margin-bottom: 6px; font-weight: 300; }
.tc-desc { font-size: 0.78rem; color: #333; line-height: 1.55; font-weight: 300; }
.hbar { background: #eee; height: 4px; border-radius: 2px; margin: 10px 0 3px; }
.hfill { height: 4px; border-radius: 2px; background: linear-gradient(90deg,#C41E3A,#ff6b6b); }
.badge { display:inline-block; padding:1px 9px; border-radius:20px; font-size:0.58rem; letter-spacing:0.1em; text-transform:uppercase; font-weight:500; margin-bottom:6px; }
.bh { background:#fff0f0; color:#C41E3A; }
.bm { background:#f5f5f5; color:#555; }
.bl { background:#f5f5f5; color:#888; }
.bd { background:#f0f0f0; color:#aaa; }

/* ── SECTION TITLES ── */
.eye { font-size:0.58rem; letter-spacing:0.2em; text-transform:uppercase; color:#C41E3A; font-weight:400; margin-bottom:3px; }
.stitle { font-family:'Playfair Display',serif; font-size:1.5rem; font-weight:600; color:#0a0a0a; border-bottom:1px solid #0a0a0a; padding-bottom:8px; margin-bottom:20px; }

/* ── ALERTS ── */
.al { padding:10px 14px; margin:6px 0; font-size:0.78rem; color:#0a0a0a; font-weight:300; }
.al-r  { background:#fff0f2; border-left:2px solid #C41E3A; }
.al-g  { background:#fff8ec; border-left:2px solid #888; }
.al-b  { background:#f5f5f5; border-left:2px solid #0a0a0a; }
.al-red { background:#C41E3A; color:#fff; border-left:none; padding:10px 14px; font-weight:400; font-size:0.78rem; }

/* ── WHOLESALER CARDS ── */
.wc { background:#fff; border-top:2px solid #0a0a0a; padding:20px; margin-bottom:16px; box-shadow:0 1px 6px rgba(0,0,0,0.06); }
.wc-name { font-family:'Playfair Display',serif; font-size:1.05rem; font-weight:600; color:#0a0a0a; }
.wc-meta { font-size:0.68rem; color:#888; margin-top:2px; font-weight:300; }
.wtag { display:inline-block; padding:1px 7px; background:#0a0a0a; color:#fff; font-size:0.55rem; letter-spacing:0.1em; text-transform:uppercase; border-radius:1px; margin:2px 2px 0 0; }

/* ── NEWS ── */
.nc { border-bottom:1px solid #eee; padding:14px 0; }
.nc-h { font-family:'Playfair Display',serif; font-size:0.95rem; font-weight:600; color:#0a0a0a; margin-bottom:3px; }
.nc-m { font-size:0.65rem; color:#aaa; margin-bottom:5px; font-weight:300; }
.nc-b { font-size:0.78rem; color:#444; line-height:1.5; font-weight:300; }

/* ── CHAT ── */
.cwrap { background:#f7f7f7; padding:16px; min-height:260px; margin-bottom:14px; }
.cu { background:#0a0a0a; color:#fff; border-radius:16px 16px 3px 16px; padding:9px 14px; margin:6px 0 6px auto; max-width:72%; font-size:0.8rem; width:fit-content; margin-left:auto; font-weight:300; }
.cb { background:#fff; color:#0a0a0a; border-radius:16px 16px 16px 3px; padding:9px 14px; margin:6px 0; max-width:72%; font-size:0.8rem; border:1px solid #e8e8e8; font-weight:300; }
.cs { font-size:0.6rem; color:#aaa; margin-bottom:2px; font-weight:300; }

/* ── LOGIN ── */
.lwrap { max-width:420px; margin:60px auto; padding:40px 36px; background:#fff; box-shadow:0 2px 24px rgba(0,0,0,0.09); border-top:2px solid #C41E3A; }
.llogo { font-family:'Playfair Display',serif; font-size:1.8rem; font-weight:600; color:#0a0a0a; text-align:center; margin-bottom:3px; }
.llogo em { color:#C41E3A; font-style:normal; }
.lsub { font-size:0.62rem; letter-spacing:0.16em; text-transform:uppercase; color:#aaa; text-align:center; margin-bottom:28px; font-weight:300; }

/* ── IMAGE BOARD ── */
.img-strip { display:flex; gap:8px; flex-wrap:wrap; margin-top:8px; }
.img-item { position:relative; width:calc(25% - 6px); aspect-ratio:1; overflow:hidden; background:#f0f0f0; }
.img-item img { width:100%; height:100%; object-fit:cover; display:block; }
.img-cap { font-size:0.6rem; color:#888; padding:4px 6px; background:#fafafa; border-top:1px solid #eee; font-weight:300; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }

/* ── BUTTONS ── */
.stButton > button {
    background: #0a0a0a !important;
    color: #fff !important;
    border: none !important;
    border-radius: 1px !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-weight: 400 !important;
    padding: 8px 20px !important;
    transition: background 0.15s !important;
}
.stButton > button:hover { background: #C41E3A !important; }

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border: 1px solid #ddd !important;
    border-radius: 1px !important;
    font-size: 0.82rem !important;
    color: #0a0a0a !important;
    font-weight: 300 !important;
    font-family: 'Inter', sans-serif !important;
}
.stSelectbox label, .stTextInput label, .stTextArea label, .stMultiSelect label, .stNumberInput label {
    font-size: 0.62rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #888 !important;
    font-weight: 400 !important;
}
[data-baseweb="select"] { border-radius: 1px !important; }
[data-baseweb="select"] * { font-size: 0.82rem !important; color: #0a0a0a !important; font-weight: 300 !important; }

/* ── METRICS (st.metric) ── */
[data-testid="metric-container"] label { font-size:0.58rem !important; color:#888 !important; text-transform:uppercase !important; letter-spacing:0.1em !important; font-weight:400 !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { font-size:1.1rem !important; color:#0a0a0a !important; font-weight:500 !important; }
[data-testid="metric-container"] [data-testid="stMetricDelta"] { font-size:0.7rem !important; }

/* ── EXPANDER ── */
details summary { font-size:0.78rem !important; color:#0a0a0a !important; font-weight:400 !important; }

/* ── DIVIDER ── */
hr { border:none; border-top:1px solid #eee; margin:20px 0; }

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] { font-size:0.78rem !important; }

/* ── FILE UPLOADER compact ── */
[data-testid="stFileUploader"] { padding: 0 !important; }
[data-testid="stFileUploader"] > div { padding: 8px 12px !important; border: 1px dashed #ddd !important; border-radius: 1px !important; background: #fafafa !important; }
[data-testid="stFileUploader"] span { font-size:0.72rem !important; color:#888 !important; font-weight:300 !important; }
[data-testid="stFileDropzoneInstructions"] { display:none !important; }

/* ── TABS ── */
[data-baseweb="tab"] { font-size:0.62rem !important; letter-spacing:0.1em !important; text-transform:uppercase !important; color:#888 !important; font-weight:400 !important; }
[aria-selected="true"] { color:#0a0a0a !important; border-bottom-color:#0a0a0a !important; }
</style>
""", unsafe_allow_html=True)

# ══ SESSION STATE ══════════════════════════════════════════════════════════════
for k, v in [
    ("logged_in", False), ("username", ""), ("role", ""),
    ("page", "Trends"), ("chat_history", []),
    ("messages", list(MESSAGES)), ("board", []), ("auth_mode", "login"),
    ("user_db", {
        "buyer1":  {"password":"buy123",  "role":"buyer",  "name":"Priya Sharma",  "email":"priya@email.com",  "city":"Hyderabad","business":"Priya Boutique"},
        "buyer2":  {"password":"buy456",  "role":"buyer",  "name":"Ananya Reddy",  "email":"ananya@email.com", "city":"Bangalore","business":"Ananya Fashion House"},
        "seller1": {"password":"sell123", "role":"seller", "name":"Rajesh Gupta",  "email":"rajesh@email.com", "city":"Surat",    "business":"Rajesh Textiles & Exports"},
        "seller2": {"password":"sell456", "role":"seller", "name":"Meena Patel",   "email":"meena@email.com",  "city":"Jaipur",   "business":"Femina Fashion House"},
    })
]:
    if k not in st.session_state:
        st.session_state[k] = v

# ══ AUTH ═══════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    st.markdown("""
    <div style='background:#0a0a0a;padding:14px 36px;border-bottom:1px solid #222;'>
        <div style='font-family:"Playfair Display",serif;font-size:1.15rem;font-weight:600;color:#fff;letter-spacing:0.04em;'>
            Trend<em style='color:#C41E3A;font-style:normal;'>ora</em>
        </div>
    </div>""", unsafe_allow_html=True)

    _, cm, _ = st.columns([1, 1.1, 1])
    with cm:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

        t1, t2 = st.columns(2)
        with t1:
            if st.button("Sign In", key="go_login"):
                st.session_state.auth_mode = "login"; st.rerun()
        with t2:
            if st.button("Create Account", key="go_signup"):
                st.session_state.auth_mode = "signup"; st.rerun()

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        if st.session_state.auth_mode == "login":
            st.markdown("<div class='lwrap'><div class='llogo'>Trend<em>ora</em></div><div class='lsub'>Sign in to continue</div></div>", unsafe_allow_html=True)

            role_sel = st.selectbox("I am a", ["Buyer — purchasing stock", "Seller — selling wholesale"])
            username = st.text_input("Username or Email")
            password = st.text_input("Password", type="password")

            st.markdown("""<div style='background:#f7f7f7;padding:10px 12px;font-size:0.7rem;color:#888;margin:8px 0 14px;font-weight:300;'>
                Demo — Buyer: <code>buyer1</code> / <code>buy123</code> &nbsp;·&nbsp; Seller: <code>seller1</code> / <code>sell123</code>
            </div>""", unsafe_allow_html=True)

            if st.button("Sign In →", key="login_btn"):
                db = st.session_state.user_db
                matched = None
                for uname, udata in db.items():
                    if (uname == username or udata.get("email","") == username) and udata["password"] == password:
                        matched = (uname, udata); break
                if matched:
                    uname, udata = matched
                    sel_role = "buyer" if "Buyer" in role_sel else "seller"
                    if udata["role"] == sel_role or udata["role"] == "admin":
                        st.session_state.update({"logged_in":True,"username":uname,"role":udata["role"],"page":"Trends"})
                        st.rerun()
                    else:
                        st.error("Role doesn't match this account.")
                else:
                    st.error("Incorrect username/email or password.")

        else:
            st.markdown("<div class='lwrap'><div class='llogo'>Trend<em>ora</em></div><div class='lsub'>Create your free account</div></div>", unsafe_allow_html=True)

            su_role     = st.selectbox("I am a", ["Buyer — purchasing stock", "Seller — selling wholesale"], key="su_r")
            su_name     = st.text_input("Full Name", placeholder="Priya Sharma")
            su_business = st.text_input("Business Name", placeholder="Priya Boutique")
            su_city     = st.text_input("City", placeholder="Hyderabad")
            su_email    = st.text_input("Email Address", placeholder="any@email.com")
            su_username = st.text_input("Choose Username", placeholder="priya_boutique")
            su_password = st.text_input("Password", type="password", placeholder="Any password you like")
            su_confirm  = st.text_input("Confirm Password", type="password")

            if st.button("Create Account →", key="signup_btn"):
                errs = []
                if not su_name.strip(): errs.append("Full name required.")
                if not su_email.strip(): errs.append("Email required.")
                if not su_username.strip() or len(su_username) < 3: errs.append("Username must be 3+ characters.")
                if su_username in st.session_state.user_db: errs.append("Username taken.")
                if any(u.get("email","") == su_email for u in st.session_state.user_db.values()): errs.append("Email already registered.")
                if not su_password: errs.append("Password required.")
                if su_password != su_confirm: errs.append("Passwords don't match.")
                if not su_business.strip(): errs.append("Business name required.")
                flagged = check_illegal_content(su_name + " " + su_business)
                if flagged: errs.append(f"Flagged content: {', '.join(flagged)}")

                if errs:
                    for e in errs: st.error(e)
                else:
                    new_role = "buyer" if "Buyer" in su_role else "seller"
                    st.session_state.user_db[su_username] = {
                        "password": su_password, "role": new_role,
                        "name": su_name, "email": su_email,
                        "city": su_city, "business": su_business,
                    }
                    st.session_state.update({"logged_in":True,"username":su_username,"role":new_role,"page":"Trends"})
                    st.success(f"Welcome to Trendora, {su_name}! 🎉")
                    st.rerun()
    st.stop()

# ══ TOP NAV ════════════════════════════════════════════════════════════════════
user_info = st.session_state.user_db.get(st.session_state.username, {})
role      = st.session_state.role

if role == "buyer":
    nav_items = ["Trends","Forecast","My Stock","Pricing","Marketplace","Messages","AI Advisor","News"]
else:
    nav_items = ["My Products","Orders","My Stock","Pricing","Messages","AI Advisor","News"]

st.markdown(f"""
<div class='tnav'>
    <div class='tnav-logo'>Trend<em>ora</em></div>
    <div class='tnav-center'>
        {''.join([f"<div class='tnav-link {'active' if st.session_state.page==item else ''}'>{item}</div>" for item in nav_items])}
    </div>
    <div class='tnav-right'>
        <strong>{user_info.get('name', st.session_state.username)}</strong> &nbsp;·&nbsp; {role.upper()}
    </div>
</div>""", unsafe_allow_html=True)

# Functional nav row (Streamlit buttons, styled subtly)
nav_cols = st.columns(len(nav_items) + 1)
for i, item in enumerate(nav_items):
    with nav_cols[i]:
        if st.button(item, key=f"n_{item}"):
            st.session_state.page = item; st.rerun()
with nav_cols[-1]:
    if st.button("Sign Out", key="so"):
        for k in ["logged_in","username","role","page","chat_history","messages","board","auth_mode"]:
            st.session_state.pop(k, None)
        st.rerun()

page = st.session_state.page

# ══ TRENDS ═════════════════════════════════════════════════════════════════════
if page == "Trends":
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

    # ── Inspiration Board — compact ────────────────────────────────────────────
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Inspiration Board</div>", unsafe_allow_html=True)

    bc1, bc2, bc3 = st.columns([2, 2, 1])
    with bc1:
        pin_url = st.text_input("Image URL", placeholder="https://i.pinimg.com/… or any image link", label_visibility="collapsed")
    with bc2:
        pin_cap = st.text_input("Caption", placeholder="Optional caption", label_visibility="collapsed")
    with bc3:
        if st.button("Add →", key="add_pin"):
            if pin_url.strip():
                flagged = check_illegal_content(pin_url + " " + pin_cap)
                if flagged:
                    st.markdown(f"<div class='al al-red'>🚫 Flagged: {', '.join(flagged)}</div>", unsafe_allow_html=True)
                else:
                    st.session_state.board.append({"url": pin_url.strip(), "cap": pin_cap, "type": "url"})
                    st.rerun()

    up_col1, up_col2 = st.columns([3, 1])
    with up_col1:
        up_file = st.file_uploader("", type=["jpg","jpeg","png","webp","gif"], label_visibility="collapsed")
    with up_col2:
        up_cap = st.text_input("Caption", placeholder="Caption", key="ucap", label_visibility="collapsed")
        if st.button("Upload →", key="upl") and up_file:
            st.session_state.board.append({"url": up_file, "cap": up_cap, "type": "upload"})
            st.rerun()

    if st.session_state.board:
        cols = st.columns(5)
        for i, img in enumerate(st.session_state.board):
            with cols[i % 5]:
                try:
                    if img["type"] == "url":
                        st.markdown(f"""<div class='img-item'><img src='{img["url"]}' onerror="this.style.display='none'"/><div class='img-cap'>{img['cap'] or '—'}</div></div>""", unsafe_allow_html=True)
                    else:
                        st.image(img["url"], use_column_width=True, caption=img["cap"] or None)
                except: pass
        if st.button("Clear board", key="clrb"):
            st.session_state.board = []; st.rerun()

    # ── Trend cards ───────────────────────────────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)
    fc1, fc2, _ = st.columns([1,1,3])
    with fc1: cat_f = st.selectbox("Category", CATEGORIES, key="tc")
    with fc2: urg_f = st.selectbox("Urgency", ["All","HIGH","MEDIUM","LOW","DEAD_STOCK"], key="tu")

    filtered = [t for t in TRENDS if (cat_f=="All" or t["category"]==cat_f) and (urg_f=="All" or t["urgency"]==urg_f)]
    ca, cb = st.columns(2)
    for i, t in enumerate(filtered):
        col = ca if i%2==0 else cb
        if t["urgency"]=="HIGH": cc,bc="","bh"
        elif t["urgency"]=="MEDIUM": cc,bc="med","bm"
        elif t["urgency"]=="LOW": cc,bc="lo","bl"
        else: cc,bc="dead","bd"
        tags = "".join([f"<span style='background:#f2f2f2;padding:1px 8px;border-radius:20px;font-size:0.6rem;margin-right:3px;color:#555;font-weight:300;'>{x}</span>" for x in t["tags"]])
        with col:
            st.markdown(f"""<div class='tc {cc}'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                    <div><div class='tc-name'>{t['name']}</div><div class='tc-meta'>{t['category']} · {t['city']} · {t['direction']}</div></div>
                    <div style='font-size:1.6rem;font-weight:600;color:#0a0a0a;line-height:1;'>{t['heat']}</div>
                </div>
                <span class='badge {bc}'>{t['urgency'].replace('_',' ')}</span>
                <div style='color:#C41E3A;font-size:0.78rem;margin-bottom:6px;font-weight:400;'>{t['change']} demand</div>
                <div class='tc-desc'>{t['description']}</div>
                <div style='margin:8px 0 3px;font-size:0.58rem;color:#aaa;text-transform:uppercase;letter-spacing:0.1em;'>Heat</div>
                <div class='hbar'><div class='hfill' style='width:{t["heat"]}%'></div></div>
                <div style='margin-top:8px;'>{tags}</div>
                <div style='font-size:0.65rem;color:#aaa;margin-top:6px;font-weight:300;'>⏱ Peak ~{t['peak_weeks']} weeks</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Analytics</div><div class='stitle'>Trend Heat Comparison</div>", unsafe_allow_html=True)
    names  = [t["name"] for t in TRENDS]
    heats  = [t["heat"] for t in TRENDS]
    bclrs  = ["#C41E3A" if h>80 else "#555" if h>60 else "#ccc" for h in heats]
    fig = go.Figure(go.Bar(x=heats, y=names, orientation='h', marker_color=bclrs,
        text=heats, textposition='outside', textfont=dict(color='#0a0a0a', size=11)))
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white',
        font=dict(family='Inter', size=11, color='#0a0a0a'),
        xaxis=dict(showgrid=False, showticklabels=False, range=[0,115]),
        yaxis=dict(showgrid=False), margin=dict(l=10,r=40,t=8,b=8), height=320)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══ FORECAST ═══════════════════════════════════════════════════════════════════
elif page == "Forecast":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>◈ Predictive Analytics</div>
        <div class='mhead-title'>Demand Forecast</div>
        <div class='mhead-sub'>12-Week Outlook · Revenue · Audience Intelligence</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    data = get_forecast_data(); rev = get_revenue_data()

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown("<div class='mc'><div class='mc-val'>+41%</div><div class='mc-lbl'>Peak Demand Surge</div><div class='mc-d'>Cargo Pants · W5</div></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='mc'><div class='mc-val'>₹2.45L</div><div class='mc-lbl'>June Revenue</div><div class='mc-d'>↑ 24% vs target</div></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='mc'><div class='mc-val'>198</div><div class='mc-lbl'>Units Sold June</div><div class='mc-d'>Best month ever</div></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='mc'><div class='mc-val'>W6</div><div class='mc-lbl'>Peak Week</div><div class='mc-d'>Highest demand</div></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Revenue vs Target</div><div class='stitle'>Monthly Performance</div>", unsafe_allow_html=True)
    fig_rev = go.Figure()
    fig_rev.add_trace(go.Bar(x=rev["months"], y=rev["revenue"], name="Actual", marker_color="#0a0a0a",
        text=[f"₹{v//1000}K" for v in rev["revenue"]], textposition='outside', textfont=dict(color='#0a0a0a',size=10)))
    fig_rev.add_trace(go.Scatter(x=rev["months"], y=rev["target"], name="Target",
        line=dict(color="#C41E3A", dash="dash", width=1.5), mode='lines+markers', marker=dict(size=6)))
    fig_rev.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family='Inter',size=11,color='#0a0a0a'),
        legend=dict(orientation='h',y=1.08,font=dict(size=10)),
        yaxis=dict(showgrid=True,gridcolor='#f0f0f0',tickprefix='₹'),
        xaxis=dict(showgrid=False), margin=dict(l=10,r=10,t=24,b=8), height=280)
    st.plotly_chart(fig_rev, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ 12-Week Projection</div><div class='stitle'>Demand Curves</div>", unsafe_allow_html=True)
    prod_sel = st.multiselect("Products", list(data.keys())[1:], default=["Baggy Cargo Pants","Printed Maxi Dresses","Crochet Mini Skirts"])
    if prod_sel:
        palette = ["#C41E3A","#0a0a0a","#888","#333","#ccc"]
        fig2 = go.Figure()
        for i, prod in enumerate(prod_sel):
            fig2.add_trace(go.Scatter(x=data["weeks"], y=data[prod], name=prod,
                mode='lines+markers', line=dict(color=palette[i%len(palette)],width=2), marker=dict(size=5)))
        fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family='Inter',size=11,color='#0a0a0a'),
            legend=dict(orientation='h',y=1.08,font=dict(size=10)),
            xaxis=dict(showgrid=False,title="Week"), yaxis=dict(showgrid=True,gridcolor='#f0f0f0',title="Units"),
            margin=dict(l=10,r=10,t=24,b=8), height=320)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Audience</div><div class='stitle'>Who Is Buying</div>", unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca:
        fig_age = go.Figure(go.Pie(labels=list(AUDIENCE_DATA["age_groups"].keys()),
            values=list(AUDIENCE_DATA["age_groups"].values()), hole=0.5,
            marker_colors=["#0a0a0a","#C41E3A","#888","#555","#ccc"]))
        fig_age.update_layout(title=dict(text="Age Groups",font=dict(size=12,color='#0a0a0a')),
            paper_bgcolor='white', font=dict(color='#0a0a0a',size=11), margin=dict(l=10,r=10,t=36,b=8), height=240)
        st.plotly_chart(fig_age, use_container_width=True)
    with cb:
        fig_city = go.Figure(go.Pie(labels=list(AUDIENCE_DATA["cities"].keys()),
            values=list(AUDIENCE_DATA["cities"].values()), hole=0.5,
            marker_colors=["#C41E3A","#0a0a0a","#888","#555","#ccc"]))
        fig_city.update_layout(title=dict(text="Top Cities",font=dict(size=12,color='#0a0a0a')),
            paper_bgcolor='white', font=dict(color='#0a0a0a',size=11), margin=dict(l=10,r=10,t=36,b=8), height=240)
        st.plotly_chart(fig_city, use_container_width=True)
    st.markdown("<div class='al al-b'>👥 68% of buyers are women aged 18–34 in Hyderabad. Best categories: Crochet Skirts, Maxi Dresses, Co-ord Sets.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══ MY STOCK ═══════════════════════════════════════════════════════════════════
elif page == "My Stock":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>◉ Inventory Control</div>
        <div class='mhead-title'>My Stock</div>
        <div class='mhead-sub'>Live Inventory · Auto Alerts · Reorder Suggestions</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    reorder = [i for i in INVENTORY if i["status"]=="REORDER NOW"]
    dead    = [i for i in INVENTORY if i["status"]=="DEAD STOCK"]
    over    = [i for i in INVENTORY if i["status"]=="OVERSTOCK"]

    if reorder: st.markdown(f"<div class='al al-r'>🚨 <strong>REORDER NOW:</strong> {', '.join([i['name'].split(' - ')[0] for i in reorder])}</div>", unsafe_allow_html=True)
    if dead:    st.markdown(f"<div class='al al-g'>⚠️ <strong>DEAD STOCK:</strong> {', '.join([i['name'].split(' - ')[0] for i in dead])} — start clearance.</div>", unsafe_allow_html=True)
    if over:    st.markdown(f"<div class='al al-g'>📦 <strong>OVERSTOCK:</strong> {', '.join([i['name'].split(' - ')[0] for i in over])} — pause reordering.</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    total_val = sum(i["qty"]*i["cost"] for i in INVENTORY)
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(f"<div class='mc'><div class='mc-val'>₹{total_val//1000}K</div><div class='mc-lbl'>Total Stock Value</div><div class='mc-d'>At cost</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='mc'><div class='mc-val'>{len(reorder)}</div><div class='mc-lbl'>Reorder Alerts</div><div class='mc-d'>Urgent</div></div>", unsafe_allow_html=True)
    with c3:
        dv = sum(i['qty']*i['cost'] for i in dead)
        st.markdown(f"<div class='mc'><div class='mc-val'>₹{dv//1000}K</div><div class='mc-lbl'>Dead Stock Value</div><div class='mc-d'>Run clearance</div></div>", unsafe_allow_html=True)
    with c4:
        fast = sum(1 for i in INVENTORY if i["velocity"]=="Fast")
        st.markdown(f"<div class='mc'><div class='mc-val'>{fast}</div><div class='mc-lbl'>Fast-Moving SKUs</div><div class='mc-d'>High demand</div></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ All SKUs</div><div class='stitle'>Inventory Dashboard</div>", unsafe_allow_html=True)
    cat_s = st.selectbox("Filter", CATEGORIES, key="sc")
    inv_f = INVENTORY if cat_s=="All" else [i for i in INVENTORY if i["category"]==cat_s]

    for item in inv_f:
        s    = item["status"]
        icon = "🔴" if s=="REORDER NOW" else "🟢" if s=="HEALTHY" else "🟡" if s=="OVERSTOCK" else "⚫"
        pct  = min(100, int(item["qty"]/max(item["reorder_point"]*2,1)*100))
        bc   = "#C41E3A" if pct<35 else "#888" if pct<60 else "#2E7D32"
        margin = int((item["selling_price"]-item["cost"])/item["selling_price"]*100)
        with st.expander(f"{icon}  {item['name']}  ·  {s}  ·  Score {item['trend_alignment']}/100"):
            c1,c2,c3,c4,c5 = st.columns(5)
            c1.metric("In Stock", f"{item['qty']}")
            c2.metric("Reorder At", f"{item['reorder_point']}")
            c3.metric("Days Left", f"{item['days_of_stock']}")
            c4.metric("Velocity", item["velocity"])
            c5.metric("Margin", f"{margin}%")
            st.markdown(f"""<div style='margin:10px 0 3px;font-size:0.6rem;color:#aaa;text-transform:uppercase;letter-spacing:0.1em;'>Stock Level</div>
            <div style='background:#eee;border-radius:2px;height:6px;'>
                <div style='width:{pct}%;height:6px;border-radius:2px;background:{bc};'></div>
            </div>""", unsafe_allow_html=True)
            if s=="REORDER NOW":
                sq = item["reorder_point"]*3
                st.markdown(f"<div class='al al-r' style='margin-top:8px;'>💡 Order <strong>{sq} units</strong> — est. ₹{sq*item['cost']:,}</div>", unsafe_allow_html=True)
            elif s=="DEAD STOCK":
                st.markdown(f"<div class='al al-g' style='margin-top:8px;'>💡 Flash sale at ₹{int(item['selling_price']*0.7)} (30% off)</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Visual</div><div class='stitle'>Stock vs Reorder Point</div>", unsafe_allow_html=True)
    skus = [i["sku"] for i in INVENTORY]; qtys = [i["qty"] for i in INVENTORY]; rpts = [i["reorder_point"] for i in INVENTORY]
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(name='Stock', x=skus, y=qtys, marker_color=['#C41E3A' if q<r else '#0a0a0a' for q,r in zip(qtys,rpts)],
        text=qtys, textposition='outside', textfont=dict(color='#0a0a0a',size=10)))
    fig4.add_trace(go.Scatter(name='Reorder Point', x=skus, y=rpts, mode='lines+markers',
        line=dict(color='#888',dash='dash',width=1.5), marker=dict(size=6)))
    fig4.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family='Inter',size=11,color='#0a0a0a'),
        legend=dict(orientation='h',y=1.08,font=dict(size=10)),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True,gridcolor='#f0f0f0',title="Units"),
        margin=dict(l=10,r=10,t=24,b=8), height=280)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══ PRICING ════════════════════════════════════════════════════════════════════
elif page == "Pricing":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>◎ Margin Intelligence</div>
        <div class='mhead-title'>Pricing Studio</div>
        <div class='mhead-sub'>Market Benchmarking · Competitor Ranges · Margin Optimisation</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    with c1: st.markdown("<div class='mc'><div class='mc-val'>₹950</div><div class='mc-lbl'>Avg Market Price</div><div class='mc-d'>All SKUs</div></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='mc'><div class='mc-val'>5</div><div class='mc-lbl'>Price Up Opportunities</div><div class='mc-d'>+₹18K/month</div></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='mc'><div class='mc-val'>64%</div><div class='mc-lbl'>Avg Gross Margin</div><div class='mc-d'>Trending products</div></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Per Product</div><div class='stitle'>Price Positioning</div>", unsafe_allow_html=True)
    for p in PRICING:
        opp = p["opportunity"]
        oc  = "#C41E3A" if "UP" in opp else "#888" if "Reduce" in opp else "#555"
        with st.expander(f"{p['product']}  ·  Your Price ₹{p['your_price']}  ·  {opp}"):
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Your Price", f"₹{p['your_price']}")
            c2.metric("Market Avg", f"₹{p['market_avg']}", delta=f"{p['your_price']-p['market_avg']:+}")
            c3.metric("Suggested", f"₹{p['suggested']}")
            c4.metric("Margin", f"{p['margin_pct']}%")
            rs = p["high"]-p["low"]
            yp = int((p["your_price"]-p["low"])/rs*100) if rs else 50
            sp = int((p["suggested"]-p["low"])/rs*100) if rs else 50
            st.markdown(f"""<div style='margin:10px 0 3px;font-size:0.6rem;color:#aaa;text-transform:uppercase;'>Market Range · Low ₹{p['low']} → High ₹{p['high']}</div>
            <div style='position:relative;background:#eee;border-radius:2px;height:8px;'>
                <div style='position:absolute;left:{yp}%;top:-3px;width:4px;height:14px;background:#0a0a0a;border-radius:1px;'></div>
                <div style='position:absolute;left:{sp}%;top:-3px;width:4px;height:14px;background:#C41E3A;border-radius:1px;'></div>
            </div>
            <div style='display:flex;justify-content:space-between;font-size:0.65rem;margin-top:5px;color:#888;'>
                <span>■ Your price: ₹{p['your_price']}</span><span style='color:#C41E3A;'>■ Suggested: ₹{p['suggested']}</span>
            </div>
            <div style='margin-top:8px;padding:8px 12px;background:#f7f7f7;border-left:2px solid {oc};font-size:0.78rem;color:#0a0a0a;'>{opp}</div>
            """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Visual</div><div class='stitle'>Margin Breakdown</div>", unsafe_allow_html=True)
    prods = [p["product"] for p in PRICING]; margins = [p["margin_pct"] for p in PRICING]
    mc2 = ["#0a0a0a" if m>60 else "#888" if m>40 else "#C41E3A" for m in margins]
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(x=prods, y=margins, marker_color=mc2, text=[f"{m}%" for m in margins], textposition='outside', textfont=dict(color='#0a0a0a',size=10)))
    fig5.add_hline(y=50, line_dash="dash", line_color="#888", annotation_text="Min 50%", annotation_font_color="#888", annotation_font_size=10)
    fig5.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family='Inter',size=11,color='#0a0a0a'),
        yaxis=dict(showgrid=True,gridcolor='#f0f0f0',title="Gross Margin %",range=[0,90]),
        xaxis=dict(showgrid=False,tickangle=-18), margin=dict(l=10,r=10,t=16,b=70), height=320)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══ MARKETPLACE ════════════════════════════════════════════════════════════════
elif page == "Marketplace":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>◇ Supplier Network</div>
        <div class='mhead-title'>Wholesaler Marketplace</div>
        <div class='mhead-sub'>Verified Suppliers · Pan India · Direct Ordering</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    cs,cc,cm = st.columns([2,1,1])
    with cs: search = st.text_input("Search suppliers or products", placeholder="cargo pants, Surat, linen…")
    with cc: city_f = st.selectbox("City", ["All","Surat","Jaipur","Mumbai","Tirupur"])
    with cm: cat_f  = st.selectbox("Category", CATEGORIES, key="wc")

    st.markdown("<hr>", unsafe_allow_html=True)
    for wh in WHOLESALERS:
        if city_f!="All" and wh["city"]!=city_f: continue
        if search and search.lower() not in wh["name"].lower() and not any(search.lower() in p["name"].lower() for p in wh["products"]): continue
        stars = "★"*int(wh["rating"])+"☆"*(5-int(wh["rating"]))
        tags_html = "".join([f"<span class='wtag'>{t}</span>" for t in wh["tags"]])
        st.markdown(f"""<div class='wc'>
            <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                <div>
                    <div class='wc-name'>{wh['name']}</div>
                    <div class='wc-meta'>📍 {wh['city']} · {wh['speciality']} · {wh['years']} years</div>
                    <div style='margin-top:6px;'>{tags_html}</div>
                </div>
                <div style='text-align:right;'>
                    <div style='color:#C41E3A;font-size:0.9rem;'>{stars}</div>
                    <div style='font-size:0.65rem;color:#555;'>{wh['rating']}/5 · ✅ Verified</div>
                    <div style='font-size:0.62rem;color:#888;margin-top:2px;'>Min ₹{wh['min_order_value']//1000}K</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
        for prod in wh["products"]:
            if cat_f!="All" and prod["category"]!=cat_f: continue
            with st.expander(f"  {prod['name']}  ·  MOQ {prod['moq']}  ·  ₹{prod['price_per_unit']}/unit"):
                c1,c2,c3,c4,c5 = st.columns(5)
                c1.metric("Price/Unit", f"₹{prod['price_per_unit']}")
                c2.metric("MOQ", f"{prod['moq']}")
                c3.metric("Fabric", prod["fabric"])
                c4.metric("Lead", f"{prod['lead_days']}d")
                c5.metric("Colors", prod["colors"])
                total = prod["price_per_unit"]*prod["moq"]
                st.markdown(f"<div style='background:#f7f7f7;padding:8px 12px;font-size:0.75rem;color:#0a0a0a;margin-top:6px;'>Min order: {prod['moq']} × ₹{prod['price_per_unit']} = <strong>₹{total:,}</strong> · Sizes: {prod['sizes']}</div>", unsafe_allow_html=True)
                b1,b2,b3,_ = st.columns([1,1,1,3])
                with b1:
                    if st.button("📩 Enquire", key=f"e_{wh['id']}_{prod['name'][:6]}"): st.success(f"Enquiry sent to {wh['name']}!")
                with b2:
                    if st.button("🛒 Order", key=f"o_{wh['id']}_{prod['name'][:6]}"): st.success(f"Order placed with {wh['name']}!")
                with b3:
                    if st.button("💬 Message", key=f"m_{wh['id']}_{prod['name'][:6]}"):
                        st.session_state.page = "Messages"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ══ MESSAGES ═══════════════════════════════════════════════════════════════════
elif page == "Messages":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>✉ Direct Messaging</div>
        <div class='mhead-title'>Messages</div>
        <div class='mhead-sub'>Connect buyers and sellers · All messages safety-monitored</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    uname   = st.session_state.username
    my_msgs = [m for m in st.session_state.messages if m["from"]==uname or m["to"]==uname]
    contacts = set()
    for m in my_msgs:
        contacts.add(m["to"] if m["from"]==uname else m["from"])
    if not contacts:
        contacts = {"seller1"} if role=="buyer" else {"buyer1"}

    all_users = [u for u in st.session_state.user_db if u != uname]
    contact_options = list(contacts) + [u for u in all_users if u not in contacts]
    sel_contact = st.selectbox("Conversation with", contact_options)

    convo = [m for m in st.session_state.messages if
             (m["from"]==uname and m["to"]==sel_contact) or
             (m["from"]==sel_contact and m["to"]==uname)]

    st.markdown("<div class='cwrap'>", unsafe_allow_html=True)
    if not convo:
        st.markdown("<div style='text-align:center;color:#aaa;padding:32px;font-size:0.78rem;font-weight:300;'>No messages yet — start the conversation below.</div>", unsafe_allow_html=True)
    for m in convo:
        sname = st.session_state.user_db.get(m["from"],{}).get("name",m["from"])
        if m["from"]==uname:
            st.markdown(f"<div style='text-align:right;'><div class='cs' style='text-align:right;'>You · {m['time']}</div><div class='cu'>{m['text']}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div><div class='cs'>{sname} · {m['time']}</div><div class='cb'>{m['text']}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    mc1, mc2 = st.columns([5,1])
    with mc1: new_msg = st.text_input("", placeholder="Type a message…", key="nm", label_visibility="collapsed")
    with mc2:
        if st.button("Send →", key="snd"):
            if new_msg.strip():
                flagged = check_illegal_content(new_msg)
                if flagged:
                    st.markdown(f"<div class='al al-red'>🚫 Blocked — flagged: {', '.join(flagged)}</div>", unsafe_allow_html=True)
                else:
                    now = datetime.now().strftime("%I:%M %p")
                    st.session_state.messages.append({"id":len(st.session_state.messages)+1,"from":uname,"to":sel_contact,"text":new_msg,"time":now,"date":"Today"})
                    st.rerun()
    st.markdown("<div class='al al-b' style='margin-top:12px;font-size:0.72rem;'>🛡️ All messages monitored. Illegal content or fraud results in immediate suspension.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══ AI ADVISOR ═════════════════════════════════════════════════════════════════
elif page == "AI Advisor":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>✦ Powered by AI</div>
        <div class='mhead-title'>AI Business Advisor</div>
        <div class='mhead-sub'>Ask anything · Trend-aware · Inventory-smart · Always on</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    st.markdown(f"""<div style='background:#0a0a0a;color:#fff;padding:14px 18px;margin-bottom:18px;border-left:3px solid #C41E3A;'>
        <div style='font-family:"Playfair Display",serif;font-size:0.95rem;font-weight:600;margin-bottom:3px;'>Hello, {user_info.get('name','there')} 👋</div>
        <div style='font-size:0.75rem;color:#888;font-weight:300;'>I know your inventory, trends, prices, and suppliers. Ask me anything.</div>
    </div>""", unsafe_allow_html=True)

    quick_qs = ["What should I reorder this week?","Which dead stock to clear?","How to improve my margins?","Best wholesaler for cargo pants?","Who is my target audience?","What is trending right now?","Revenue performance?","What to stock for festive season?"]
    st.markdown("<div style='font-size:0.58rem;letter-spacing:0.14em;text-transform:uppercase;color:#aaa;margin-bottom:8px;'>Quick Questions</div>", unsafe_allow_html=True)
    qcols = st.columns(4)
    for i, q in enumerate(quick_qs):
        with qcols[i%4]:
            if st.button(q, key=f"q{i}"):
                st.session_state.chat_history.append({"role":"user","text":q})
                st.session_state.chat_history.append({"role":"bot","text":get_ai_response(q,role)})
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='cwrap'>", unsafe_allow_html=True)
    if not st.session_state.chat_history:
        st.markdown("<div style='text-align:center;color:#aaa;padding:32px;font-size:0.78rem;font-weight:300;'>Ask anything about your fashion business ↓</div>", unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        if msg["role"]=="user":
            st.markdown(f"<div style='text-align:right;'><div class='cs' style='text-align:right;'>You</div><div class='cu'>{msg['text']}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div><div class='cs'>Trendora AI</div><div class='cb'>{msg['text']}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    ai1,ai2,ai3 = st.columns([5,1,1])
    with ai1: user_q = st.text_input("", placeholder="Ask Trendora AI…", key="aiq", label_visibility="collapsed")
    with ai2:
        if st.button("Ask →", key="ask"):
            if user_q.strip():
                flagged = check_illegal_content(user_q)
                if flagged:
                    st.markdown(f"<div class='al al-red'>🚫 Flagged: {', '.join(flagged)}</div>", unsafe_allow_html=True)
                else:
                    st.session_state.chat_history.append({"role":"user","text":user_q})
                    st.session_state.chat_history.append({"role":"bot","text":get_ai_response(user_q,role)})
                    st.rerun()
    with ai3:
        if st.button("Clear", key="clr"): st.session_state.chat_history=[]; st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Auto Intelligence</div><div class='stitle'>This Week's Digest</div>", unsafe_allow_html=True)
    digests = [
        ("#C41E3A","🔴 URGENT","Stock out in 4 days","Baggy Cargo Pants, Crochet Skirts, and Maxi Dresses running out. Contact Rajesh Textiles and Femina today."),
        ("#0a0a0a","💰 OPPORTUNITY","₹18K margin available","Raise prices on 5 products to market average — adds ₹18,000/month in pure margin, zero extra cost."),
        ("#888","📦 ACTION","₹70K dead stock","78 blazers, 90+ days unsold. 30% clearance recovers ₹81K and frees capital for trending items."),
        ("#C41E3A","📈 TREND","Crochet peaks in 3 weeks","Highest-margin item at 71%. Only 6 units. Order 75 units from Femina immediately."),
    ]
    dc = st.columns(2)
    for i,(color,label,title,body) in enumerate(digests):
        with dc[i%2]:
            st.markdown(f"""<div style='background:#fff;border-left:3px solid {color};padding:14px 18px;margin-bottom:10px;box-shadow:0 1px 6px rgba(0,0,0,0.06);'>
                <div style='font-size:0.58rem;letter-spacing:0.15em;text-transform:uppercase;color:{color};font-weight:400;margin-bottom:3px;'>{label}</div>
                <div style='font-family:"Playfair Display",serif;font-size:0.9rem;font-weight:600;color:#0a0a0a;margin-bottom:5px;'>{title}</div>
                <div style='font-size:0.75rem;color:#444;line-height:1.5;font-weight:300;'>{body}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══ NEWS ═══════════════════════════════════════════════════════════════════════
elif page == "News":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>📰 Industry Intelligence</div>
        <div class='mhead-title'>Fashion News</div>
        <div class='mhead-sub'>Market updates · Industry reports · June 2025</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    impact_f = st.selectbox("Filter", ["All","HIGH","MEDIUM","LOW"])
    fn = FASHION_NEWS if impact_f=="All" else [n for n in FASHION_NEWS if n["impact"]==impact_f]
    for news in fn:
        ic = "#C41E3A" if news["impact"]=="HIGH" else "#888" if news["impact"]=="MEDIUM" else "#ccc"
        st.markdown(f"""<div class='nc'>
            <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px;'>
                <div class='nc-h'>{news['headline']}</div>
                <span style='background:{ic};color:#fff;padding:1px 9px;border-radius:20px;font-size:0.58rem;letter-spacing:0.1em;text-transform:uppercase;font-weight:400;white-space:nowrap;margin-left:12px;'>{news['impact']}</span>
            </div>
            <div class='nc-m'>{news['source']} · {news['date']}</div>
            <div class='nc-b'>{news['summary']}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══ MY PRODUCTS (Seller) ═══════════════════════════════════════════════════════
elif page == "My Products":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>◆ Seller Dashboard</div>
        <div class='mhead-title'>My Products</div>
        <div class='mhead-sub'>Manage listings · Track enquiries · Add new products</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    my_wh = [w for w in WHOLESALERS if w.get("username")==st.session_state.username]
    if my_wh:
        wh = my_wh[0]
        st.markdown(f"""<div class='wc'>
            <div class='wc-name'>{wh['name']}</div>
            <div class='wc-meta'>📍 {wh['city']} · {wh['speciality']} · ⭐ {wh['rating']}/5 · ✅ Verified</div>
            <div style='margin-top:6px;'>{"".join([f"<span class='wtag'>{t}</span>" for t in wh['tags']])}</div>
        </div>""", unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1: st.markdown(f"<div class='mc'><div class='mc-val'>{len(wh['products'])}</div><div class='mc-lbl'>Active Listings</div><div class='mc-d'>Live</div></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='mc'><div class='mc-val'>3</div><div class='mc-lbl'>New Enquiries</div><div class='mc-d'>Respond within 24h</div></div>", unsafe_allow_html=True)
        with c3:
            tv = sum(p["moq"]*p["price_per_unit"] for p in wh["products"])
            st.markdown(f"<div class='mc'><div class='mc-val'>₹{tv//1000}K</div><div class='mc-lbl'>Min Order Value</div><div class='mc-d'>All products</div></div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='eye'>◆ Listings</div><div class='stitle'>Your Products</div>", unsafe_allow_html=True)
        for prod in wh["products"]:
            with st.expander(f"  {prod['name']}  ·  ₹{prod['price_per_unit']}/unit  ·  MOQ {prod['moq']}"):
                c1,c2,c3,c4 = st.columns(4)
                c1.metric("Price/Unit", f"₹{prod['price_per_unit']}")
                c2.metric("MOQ", prod["moq"])
                c3.metric("Lead", f"{prod['lead_days']}d")
                c4.metric("Colors", prod["colors"])
                st.markdown(f"<div style='background:#f7f7f7;padding:8px;font-size:0.75rem;color:#0a0a0a;margin-top:6px;'>Fabric: {prod['fabric']} · Sizes: {prod['sizes']}</div>", unsafe_allow_html=True)
    else:
        c1,c2,c3 = st.columns(3)
        with c1: st.markdown("<div class='mc'><div class='mc-val'>0</div><div class='mc-lbl'>Active Listings</div><div class='mc-d'>Add your first</div></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Add New</div><div class='stitle'>List a Product</div>", unsafe_allow_html=True)
    with st.form("np"):
        np_name = st.text_input("Product Name", placeholder="e.g. Baggy Cargo Pants (Bulk)")
        c1,c2 = st.columns(2)
        with c1:
            np_price = st.number_input("Price per Unit (₹)", min_value=1, value=300)
            np_moq   = st.number_input("MOQ (units)", min_value=1, value=50)
            np_lead  = st.number_input("Lead Time (days)", min_value=1, value=7)
        with c2:
            np_fabric = st.text_input("Fabric", placeholder="Cotton-Poly Blend")
            np_sizes  = st.text_input("Sizes", placeholder="S-XXL")
            np_colors = st.number_input("Colors", min_value=1, value=5)
        np_desc = st.text_area("Description", placeholder="Describe your product…", height=80)
        if st.form_submit_button("List Product →") and np_name:
            flagged = check_illegal_content(np_name+" "+np_desc)
            if flagged:
                st.markdown(f"<div class='al al-red'>🚫 Blocked — flagged: {', '.join(flagged)}</div>", unsafe_allow_html=True)
            else:
                st.success(f"✅ '{np_name}' listed on Trendora Marketplace!")
    st.markdown("</div>", unsafe_allow_html=True)

# ══ ORDERS (Seller) ════════════════════════════════════════════════════════════
elif page == "Orders":
    st.markdown("""<div class='mhead'>
        <div class='mhead-eye'>◆ Order Management</div>
        <div class='mhead-title'>Orders</div>
        <div class='mhead-sub'>Incoming orders · Confirm · Dispatch · Track</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='pwrap'>", unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    with c1: st.markdown("<div class='mc'><div class='mc-val'>3</div><div class='mc-lbl'>New Orders</div><div class='mc-d'>Action required</div></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='mc'><div class='mc-val'>₹1.2L</div><div class='mc-lbl'>This Month</div><div class='mc-d'>↑ 18% vs last</div></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='mc'><div class='mc-val'>7</div><div class='mc-lbl'>Pending Dispatch</div><div class='mc-d'>Ship within 48h</div></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='eye'>◆ Incoming</div><div class='stitle'>Order Queue</div>", unsafe_allow_html=True)
    orders = [
        {"id":"ORD-001","buyer":"Priya Boutique","product":"Baggy Cargo Pants","qty":100,"value":32000,"status":"New","date":"Today"},
        {"id":"ORD-002","buyer":"Ananya Fashion House","product":"Linen Trousers","qty":50,"value":14000,"status":"Confirmed","date":"Yesterday"},
        {"id":"ORD-003","buyer":"StyleHub Hyderabad","product":"Baggy Cargo Pants","qty":75,"value":24000,"status":"Dispatched","date":"3 days ago"},
    ]
    for o in orders:
        sc = "#C41E3A" if o["status"]=="New" else "#888" if o["status"]=="Confirmed" else "#2E7D32"
        with st.expander(f"{o['id']}  ·  {o['buyer']}  ·  ₹{o['value']:,}  ·  {o['status']}"):
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Qty", f"{o['qty']}")
            c2.metric("Value", f"₹{o['value']:,}")
            c3.metric("Date", o["date"])
            c4.metric("Status", o["status"])
            st.markdown(f"<div style='margin-top:6px;padding:7px 12px;background:#f7f7f7;border-left:2px solid {sc};font-size:0.75rem;color:#0a0a0a;'>Status: {o['status']}</div>", unsafe_allow_html=True)
            if o["status"]=="New":
                b1,b2,_ = st.columns([1,1,4])
                with b1:
                    if st.button("✅ Confirm", key=f"c_{o['id']}"): st.success("Confirmed!")
                with b2:
                    if st.button("❌ Decline", key=f"d_{o['id']}"): st.error("Declined.")
    st.markdown("</div>", unsafe_allow_html=True)

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='border-top:1px solid #eee;text-align:center;padding:16px;font-size:0.58rem;color:#ccc;letter-spacing:0.16em;text-transform:uppercase;font-weight:300;'>
    Trendora · Fashion Intelligence Platform · All activity monitored · © 2025
</div>""", unsafe_allow_html=True)
