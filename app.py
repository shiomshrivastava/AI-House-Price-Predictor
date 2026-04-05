import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import os
import gdown

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="California House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== CUSTOM CSS ======================
st.markdown("""
<style>
/* ─── Fonts ─── */
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,700;0,900;1,300;1,700&family=Syne:wght@400;500;600;700&display=swap');

/* ─── Tokens ─── */
:root {
    --bg:          #07090D;
    --bg-1:        #0D1117;
    --bg-2:        #131923;
    --bg-3:        #1A2333;
    --border:      rgba(220,150,30,0.16);
    --border-hi:   rgba(220,150,30,0.42);
    --amber:       #DC961E;
    --amber-hi:    #F0B84A;
    --amber-glow:  rgba(220,150,30,0.18);
    --text:        #EBE6DE;
    --text-2:      #8A8278;
    --text-3:      #3E3A34;
    --green:       #3DD68C;
    --font-display:'Fraunces', Georgia, serif;
    --font-ui:     'Syne', system-ui, sans-serif;
    --r:           10px;
    --r-sm:        6px;
    --shadow:      0 8px 32px rgba(0,0,0,0.5);
    --shadow-glow: 0 0 40px rgba(220,150,30,0.15);
}

/* ─── Base ─── */
html, body { background: var(--bg) !important; }
.stApp     { background: var(--bg) !important; font-family: var(--font-ui); color: var(--text); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.8rem 2.2rem 4rem !important; max-width: 1320px !important; }

/* ─── Scrollbar ─── */
* { scrollbar-width: thin; scrollbar-color: var(--amber) var(--bg-1); }
::-webkit-scrollbar       { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg-1); }
::-webkit-scrollbar-thumb { background: var(--amber); border-radius: 4px; }

/* ════════════════════════════
   HEADER CARD
════════════════════════════ */
.main-header {
    background: linear-gradient(140deg, var(--bg-2) 0%, var(--bg-3) 100%);
    padding: 3rem 3.5rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    border: 1px solid var(--border);
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow);
}
/* amber corner glow */
.main-header::before {
    content: '';
    position: absolute;
    width: 380px; height: 380px;
    top: -130px; right: -80px;
    background: radial-gradient(circle, rgba(220,150,30,0.12) 0%, transparent 65%);
    border-radius: 50%;
}
/* thin top accent line */
.main-header::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent 0%, var(--amber) 40%, var(--amber-hi) 60%, transparent 100%);
    opacity: 0.7;
}
.header-badge {
    display: inline-block;
    font-family: var(--font-ui);
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 3.5px;
    text-transform: uppercase;
    color: var(--amber);
    background: rgba(220,150,30,0.1);
    border: 1px solid var(--border-hi);
    padding: 5px 14px;
    border-radius: 50px;
    margin-bottom: 1.1rem;
}
.header-title {
    font-family: var(--font-display);
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 900;
    color: var(--text);
    line-height: 1.08;
    letter-spacing: -0.025em;
    margin: 0 0 0.6rem;
}
.header-title span { color: var(--amber); font-style: italic; }
.header-desc {
    font-size: 0.88rem;
    font-weight: 400;
    color: var(--text-2);
    max-width: 500px;
    line-height: 1.65;
}
.header-stats {
    display: flex;
    gap: 2.5rem;
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
}
.stat-val  { font-family: var(--font-display); font-size: 1.45rem; font-weight: 700; color: var(--amber-hi); }
.stat-key  { font-size: 0.6rem; font-weight: 600; letter-spacing: 2.5px; text-transform: uppercase; color: var(--text-3); margin-top: 2px; }

/* ════════════════════════════
   SECTION LABELS
════════════════════════════ */
.sec-label {
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--text-3);
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.9rem;
}
.sec-label::after { content: ''; flex: 1; height: 1px; background: var(--border); }

/* ════════════════════════════
   PRESET BUTTONS
════════════════════════════ */
div[data-testid="stButton"] > button {
    font-family: var(--font-ui) !important;
    font-size: 0.74rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    background: var(--bg-2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-2) !important;
    border-radius: var(--r-sm) !important;
    padding: 0.65rem 1rem !important;
    transition: all 0.22s ease !important;
    width: 100% !important;
    height: auto !important;
}
div[data-testid="stButton"] > button:hover {
    background: var(--bg-3) !important;
    border-color: var(--amber) !important;
    color: var(--amber-hi) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(220,150,30,0.15) !important;
}

/* Primary predict button */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, var(--amber) 0%, #C87010 100%) !important;
    border: none !important;
    color: #07090D !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    padding: 0.95rem 2rem !important;
    border-radius: var(--r) !important;
    box-shadow: 0 4px 24px rgba(220,150,30,0.3) !important;
    transition: all 0.25s ease !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg, var(--amber-hi) 0%, var(--amber) 100%) !important;
    box-shadow: 0 6px 40px rgba(220,150,30,0.45) !important;
    transform: translateY(-2px) !important;
}

/* ════════════════════════════
   INPUT PANEL WRAPPER
════════════════════════════ */
.input-panel {
    background: var(--bg-1);
    border: 1px solid var(--border);
    border-radius: var(--r);
    padding: 1.6rem 1.8rem;
    position: relative;
}
.input-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: var(--r) var(--r) 0 0;
    background: linear-gradient(90deg, transparent, var(--amber), transparent);
    opacity: 0.5;
}
.panel-title {
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--text-3);
    margin-bottom: 1.1rem;
}

/* Number inputs */
div[data-testid="stNumberInput"] label p,
div[data-testid="stSelectbox"]   label p,
div[data-testid="stWidgetLabel"] p {
    font-family: var(--font-ui) !important;
    font-size: 0.67rem !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--text-2) !important;
}
div[data-testid="stNumberInput"] input {
    background: var(--bg-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
    color: var(--text) !important;
    font-family: var(--font-ui) !important;
    font-size: 0.92rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: var(--amber) !important;
    box-shadow: 0 0 0 3px rgba(220,150,30,0.12) !important;
}
/* stepper buttons */
div[data-testid="stNumberInput"] button {
    background: var(--bg-3) !important;
    border-color: var(--border) !important;
    color: var(--text-2) !important;
}
div[data-testid="stNumberInput"] button:hover {
    border-color: var(--amber) !important;
    color: var(--amber) !important;
}

/* Selectbox */
div[data-testid="stSelectbox"] > div > div {
    background: var(--bg-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
    color: var(--text) !important;
    font-family: var(--font-ui) !important;
}
div[data-testid="stSelectbox"] > div > div:hover,
div[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: var(--amber) !important;
    box-shadow: 0 0 0 3px rgba(220,150,30,0.1) !important;
}
/* dropdown list */
div[data-baseweb="popover"] ul {
    background: var(--bg-2) !important;
    border: 1px solid var(--border-hi) !important;
    border-radius: var(--r-sm) !important;
}
div[data-baseweb="popover"] li:hover { background: var(--bg-3) !important; }

/* ════════════════════════════
   RESULT CARD
════════════════════════════ */
@keyframes revealUp  { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }
@keyframes glowPulse { 0%,100% { text-shadow:0 0 30px rgba(220,150,30,0.25); } 50% { text-shadow:0 0 70px rgba(220,150,30,0.6), 0 0 120px rgba(220,150,30,0.2); } }
@keyframes sweep     { 0% { top:-30%; } 100% { top:130%; } }

.result-card {
    background: linear-gradient(145deg, var(--bg-2) 0%, var(--bg-3) 100%);
    padding: 3rem 2.5rem 2.5rem;
    border-radius: var(--r);
    border: 1px solid rgba(220,150,30,0.28);
    text-align: center;
    margin: 1.8rem 0;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow), var(--shadow-glow);
    animation: revealUp 0.5s cubic-bezier(0.16,1,0.3,1) both;
}
/* ambient glow top */
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse 70% 40% at 50% 0%, rgba(220,150,30,0.09), transparent);
    pointer-events: none;
}
/* top line */
.result-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--amber-hi), transparent);
}
/* sweep shimmer */
.result-sweep {
    position: absolute;
    left: 0; right: 0; height: 40%;
    background: linear-gradient(180deg, transparent, rgba(220,150,30,0.04), transparent);
    animation: sweep 1.8s ease 0.2s 1;
    pointer-events: none;
}
.result-eyebrow {
    font-size: 0.6rem; font-weight: 700; letter-spacing: 3.5px;
    text-transform: uppercase; color: var(--amber); margin-bottom: 0.6rem;
}
.result-price {
    font-family: var(--font-display);
    font-size: clamp(3.2rem, 6vw, 5rem);
    font-weight: 900;
    color: var(--amber-hi);
    letter-spacing: -0.025em;
    line-height: 1;
    margin: 0.4rem 0 0.8rem;
    animation: glowPulse 2s ease 0.5s infinite;
}
.result-divider { height:1px; background:var(--border); margin:1.4rem 0; }
.result-stats { display:grid; grid-template-columns:repeat(3,1fr); gap:0.8rem; }
.rs-val { font-family:var(--font-display); font-size:1.1rem; font-weight:700; color:var(--text); }
.rs-key { font-size:0.58rem; font-weight:600; letter-spacing:2px; text-transform:uppercase; color:var(--text-3); margin-top:3px; }
.result-location {
    margin-top:1.2rem;
    font-size:0.75rem; color:var(--text-2); letter-spacing:0.4px; line-height:1.6;
}
.result-location b { color:var(--amber); font-weight:600; }

/* ════════════════════════════
   MAP CONTAINER
════════════════════════════ */
.map-wrap {
    border-radius: var(--r);
    overflow: hidden;
    border: 1px solid var(--border);
    margin-top: 1.6rem;
    box-shadow: var(--shadow);
}
.map-label {
    font-size: 0.62rem; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: var(--text-3);
    margin-bottom: 0.7rem; margin-top: 1.8rem;
    display: flex; align-items: center; gap: 0.6rem;
}
.map-label::after { content:''; flex:1; height:1px; background:var(--border); }

/* ════════════════════════════
   SIDEBAR
════════════════════════════ */
section[data-testid="stSidebar"] {
    background: var(--bg-1) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div { padding: 1.6rem 1.3rem !important; }

/* override ALL text inside sidebar */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] small,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] div { color: var(--text) !important; }

.sb-logo {
    font-family: var(--font-display);
    font-size: 1.4rem; font-weight: 900; font-style: italic;
    color: var(--amber) !important; line-height: 1.15; margin-bottom: 0.2rem;
}
.sb-sub {
    font-size: 0.58rem; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: var(--text-3) !important; margin-bottom: 1.4rem;
}
.sb-divider { height:1px; background:var(--border); margin: 1.1rem 0; }
.sb-sec-title {
    font-size: 0.58rem; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: var(--text-3) !important;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 0.8rem;
}
.hist-row {
    background: var(--bg-2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--amber);
    border-radius: var(--r-sm);
    padding: 0.75rem 0.95rem;
    margin-bottom: 0.5rem;
    transition: border-color 0.2s;
}
.hist-row:hover { border-color: var(--amber-hi); }
.hist-price { font-family:var(--font-display); font-size:1.05rem; font-weight:700; color:var(--amber-hi) !important; }
.hist-meta  { font-size:0.65rem; color:var(--text-3) !important; margin-top:2px; letter-spacing:0.3px; }
.hist-empty {
    font-size:0.75rem; color:var(--text-3) !important;
    text-align:center; padding:1.4rem 0; letter-spacing:0.5px;
    font-style:italic;
}
.sb-info-box {
    background: rgba(220,150,30,0.07);
    border: 1px solid rgba(220,150,30,0.2);
    border-radius: var(--r-sm);
    padding: 0.6rem 0.9rem;
    font-size: 0.65rem;
    color: var(--text-2) !important;
    line-height: 1.7;
    font-family: monospace;
}

/* ════════════════════════════
   SPINNER, CAPTION, ALERTS
════════════════════════════ */
div[data-testid="stSpinner"] > div { border-top-color: var(--amber) !important; }
div[data-testid="stSpinner"] p     { color: var(--text-2) !important; font-family: var(--font-ui) !important; font-size: 0.82rem !important; }

div[data-testid="stCaptionContainer"] p {
    font-family: var(--font-ui) !important;
    font-size: 0.65rem !important;
    letter-spacing: 1px !important;
    color: var(--text-3) !important;
    text-align: center !important;
    margin-top: 2.5rem !important;
}

/* Warning / info boxes */
div[data-testid="stAlert"] {
    background: rgba(220,150,30,0.07) !important;
    border: 1px solid rgba(220,150,30,0.2) !important;
    border-radius: var(--r-sm) !important;
    color: var(--text-2) !important;
}

/* st.divider */
hr { border-color: var(--border) !important; }

/* Column gap */
div[data-testid="stHorizontalBlock"] { gap: 0.9rem !important; }
</style>
""", unsafe_allow_html=True)

# ====================== LOAD MODEL ======================
@st.cache_resource
def load_model():
    if not os.path.exists("model.pkl"):
        url = "https://drive.google.com/uc?id=1qQjl456I9H6Cz_kVjMwNOmUXdetxgvl1"
        gdown.download(url, "model.pkl", quiet=False)

    model = joblib.load("model.pkl")
    pipeline = joblib.load("pipeline.pkl")
    return model, pipeline

model, pipeline = load_model()

# ====================== SESSION STATE ======================
if "history" not in st.session_state:
    st.session_state.history = []
if "preset" not in st.session_state:
    st.session_state.preset = {}

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("<div class='sb-logo'>CA House<br>Predictor</div>", unsafe_allow_html=True)
    st.markdown("<div class='sb-sub'>ML Valuation Engine</div>", unsafe_allow_html=True)
    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    st.markdown("<div class='sb-sec-title'>Recent Predictions</div>", unsafe_allow_html=True)

    if st.session_state.history:
        for pred in reversed(st.session_state.history[-5:]):
            st.markdown(f"""
            <div class='hist-row'>
                <div class='hist-price'>${pred['price']:,.0f}</div>
                <div class='hist-meta'>{pred['ocean_proximity']} &nbsp;·&nbsp; {pred['timestamp']}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div class='hist-empty'>No predictions yet</div>", unsafe_allow_html=True)

    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='sb-sec-title'>Model Info</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='sb-info-box'>
        ALGO &nbsp;Random Forest<br>
        DATA &nbsp;CA Housing 1990<br>
        FEAT &nbsp;12 (incl. engineered)<br>
        TASK &nbsp;Regression
    </div>""", unsafe_allow_html=True)

# ====================== HEADER ======================
st.markdown("""
<div class='main-header'>
    <div class='header-badge'>✦ AI-Powered Real Estate Valuation</div>
    <h1 class='header-title'>California <span>House Price</span> Predictor</h1>
    <p class='header-desc'>
        Enter block-level census attributes to receive an instant machine-learning
        valuation from a tuned Random Forest model trained on ~20,000 CA census blocks.
    </p>
    <div class='header-stats'>
        <div><div class='stat-val'>~20K</div><div class='stat-key'>Training Samples</div></div>
        <div><div class='stat-val'>12</div><div class='stat-key'>Input Features</div></div>
        <div><div class='stat-val'>RF</div><div class='stat-key'>Algorithm</div></div>
        <div><div class='stat-val'>1990</div><div class='stat-key'>Census Vintage</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ====================== PRESET BUTTONS ======================
st.markdown("<div class='sec-label'>Quick Presets — Load Sample Property</div>", unsafe_allow_html=True)

presets = {
    "🌉  Bay Area":    {"long": -122.42, "lat": 37.77, "age": 35, "rooms": 2500, "bed": 450,
                        "pop": 1100, "hh": 420, "inc": 7.5, "ocean": "NEAR BAY"},
    "🌴  Los Angeles": {"long": -118.25, "lat": 34.05, "age": 28, "rooms": 1800, "bed": 380,
                        "pop": 950,  "hh": 360, "inc": 5.2, "ocean": "<1H OCEAN"},
    "🏜️  Inland":      {"long": -117.30, "lat": 34.10, "age": 20, "rooms": 2200, "bed": 500,
                        "pop": 1400, "hh": 480, "inc": 3.8, "ocean": "INLAND"},
    "🌊  Coastal":     {"long": -121.89, "lat": 36.60, "age": 40, "rooms": 1500, "bed": 310,
                        "pop": 750,  "hh": 290, "inc": 6.1, "ocean": "NEAR OCEAN"},
}

cols = st.columns(4)
for col, (label, data) in zip(cols, presets.items()):
    with col:
        if st.button(label, use_container_width=True, key=f"preset_{label}"):
            st.session_state.preset = data
            st.rerun()

# ====================== INPUT FORM ======================
pv = st.session_state.preset
ocean_options = ["<1H OCEAN", "INLAND", "NEAR OCEAN", "NEAR BAY", "ISLAND"]
default_ocean = pv.get("ocean", "<1H OCEAN")
ocean_idx     = ocean_options.index(default_ocean) if default_ocean in ocean_options else 0

st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

colA, colB = st.columns(2, gap="medium")

with colA:
    st.markdown("<div class='input-panel'><div class='panel-title'>📍 Location &amp; Structure</div>",
                unsafe_allow_html=True)
    longitude          = st.number_input("Longitude", value=float(pv.get("long", -122.0)),
                                         format="%.4f", min_value=-124.5, max_value=-114.0, step=0.01)
    latitude           = st.number_input("Latitude",  value=float(pv.get("lat", 37.0)),
                                         format="%.4f", min_value=32.5, max_value=42.0, step=0.01)
    housing_median_age = st.number_input("Housing Median Age (yrs)", value=int(pv.get("age", 30)),
                                         min_value=1, max_value=52, step=1)
    total_rooms        = st.number_input("Total Rooms", value=int(pv.get("rooms", 2000)),
                                         min_value=1, max_value=39320, step=50)
    st.markdown("</div>", unsafe_allow_html=True)

with colB:
    st.markdown("<div class='input-panel'><div class='panel-title'>👥 Demographics &amp; Economy</div>",
                unsafe_allow_html=True)
    total_bedrooms  = st.number_input("Total Bedrooms", value=int(pv.get("bed", 400)),
                                      min_value=1, max_value=6445, step=10)
    population      = st.number_input("Population",     value=int(pv.get("pop", 1000)),
                                      min_value=3, max_value=35682, step=50)
    households      = st.number_input("Households",     value=int(pv.get("hh", 350)),
                                      min_value=1, max_value=6082, step=10)
    median_income   = st.number_input("Median Income (×$10K)", value=float(pv.get("inc", 4.5)),
                                      min_value=0.5, max_value=15.0, step=0.1, format="%.2f")
    ocean_proximity = st.selectbox("Ocean Proximity", ocean_options, index=ocean_idx)
    st.markdown("</div>", unsafe_allow_html=True)

# ====================== PREDICT BUTTON ======================
st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

if st.button("🔮  Predict House Price", type="primary", use_container_width=True):
    with st.spinner("Running model inference…"):

        # Build input dataframe
        input_data = {
            "longitude":          longitude,
            "latitude":           latitude,
            "housing_median_age": housing_median_age,
            "total_rooms":        total_rooms,
            "total_bedrooms":     total_bedrooms,
            "population":         population,
            "households":         households,
            "median_income":      median_income,
            "ocean_proximity":    ocean_proximity,
        }
        df = pd.DataFrame([input_data])

        # ── Feature Engineering ──────────────────────────
        # BUG FIX: guard against division-by-zero
        df["rooms_per_household"]      = df["total_rooms"] / df["households"].replace(0, 1)
        df["bedrooms_per_room"]        = df["total_bedrooms"] / df["total_rooms"].replace(0, 1)
        df["population_per_household"] = df["population"] / df["households"].replace(0, 1)

        # 🔥 FIX: column order match with training
        final_cols = [
            'longitude',
            'latitude',
            'housing_median_age',
            'total_rooms',
            'total_bedrooms',
            'population',
            'households',
            'median_income',
            'rooms_per_household',
            'bedrooms_per_room',
            'population_per_household',
            'ocean_proximity'
        ]
        df = df[final_cols]

        # ── Prediction ───────────────────────────────────
        prepared   = pipeline.transform(df)
        prediction = model.predict(prepared)[0]

        # Derived display values
        rph = total_rooms    / households   if households > 0 else 0.0
        bpr = total_bedrooms / total_rooms  if total_rooms > 0 else 0.0
        pph = population     / households   if households > 0 else 0.0

    # Save to history
    st.session_state.history.append({
        "price":           prediction,
        "ocean_proximity": ocean_proximity,
        "timestamp":       datetime.now().strftime("%H:%M"),
    })

    # ── Result card ──────────────────────────────────
    st.markdown(f"""
    <div class='result-card'>
        <div class='result-sweep'></div>
        <div class='result-eyebrow'>Estimated Market Value</div>
        <div class='result-price'>${prediction:,.0f}</div>
        <div class='result-divider'></div>
        <div class='result-stats'>
            <div>
                <div class='rs-val'>{rph:.1f}</div>
                <div class='rs-key'>Rooms / HH</div>
            </div>
            <div>
                <div class='rs-val'>{bpr:.3f}</div>
                <div class='rs-key'>Beds / Room</div>
            </div>
            <div>
                <div class='rs-val'>{pph:.1f}</div>
                <div class='rs-key'>Pop / HH</div>
            </div>
        </div>
        <div class='result-location'>
            <b>{latitude:.4f}°N, {abs(longitude):.4f}°W</b>
            &nbsp;·&nbsp; {ocean_proximity}
            &nbsp;·&nbsp; Median age {housing_median_age} yrs
            &nbsp;·&nbsp; Income {median_income:.1f}×$10K
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Interactive Map ───────────────────────────────
    # BUG FIX: narrow exception to ImportError only; removed invalid
    #          `use_container_width` param from st_folium (not supported)
    try:
        import folium
        from streamlit_folium import st_folium

        st.markdown("<div class='map-label'>📍 Property Location</div>", unsafe_allow_html=True)
        st.markdown("<div class='map-wrap'>", unsafe_allow_html=True)

        m = folium.Map(location=[latitude, longitude], zoom_start=12,
                       tiles="CartoDB positron")
        folium.Marker(
            [latitude, longitude],
            popup=folium.Popup(f"<b>${prediction:,.0f}</b><br>{ocean_proximity}", max_width=180),
            tooltip="Predicted Price",
            icon=folium.Icon(color="red", icon="home", prefix="fa"),
        ).add_to(m)
        folium.Circle(
            [latitude, longitude], radius=1800,
            color="#DC961E", fill=True, fill_opacity=0.08, weight=1.5,
        ).add_to(m)

        # BUG FIX: `use_container_width` is not a valid st_folium parameter — removed
        st_folium(m, width="100%", height=400, returned_objects=[])
        st.markdown("</div>", unsafe_allow_html=True)

    except ImportError:
        st.warning("Install `folium` and `streamlit-folium` for an interactive map.")

# ====================== FOOTER ======================
st.caption("Built with ❤️ using Streamlit  ·  Random Forest Model  ·  California Housing Dataset")
