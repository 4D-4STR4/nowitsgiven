"""
PulseScan — Elite Risk Intelligence Dashboard
A mobile-first fintech web app for deep macro + government risk analysis
with optional portfolio ticker impact analysis.
"""

import streamlit as st
import anthropic
import requests
import json
import time
import datetime
import plotly.graph_objects as go
from typing import Optional

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PulseScan | Risk Intelligence",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={"About": "PulseScan — Macro Risk Intelligence by PulseScan Architect"},
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

  :root {
    --bg-primary:     #0a0d14;
    --bg-secondary:   #0f1320;
    --bg-card:        #131929;
    --bg-card-hover:  #1a2235;
    --border:         #1e2d45;
    --border-glow:    #1e4080;
    --text-primary:   #e8edf5;
    --text-secondary: #7a8ba8;
    --text-muted:     #4a5a72;
    --accent-blue:    #2563eb;
    --accent-cyan:    #06b6d4;
    --accent-green:   #10b981;
    --accent-red:     #ef4444;
    --accent-orange:  #f59e0b;
    --accent-purple:  #8b5cf6;
    --glow-blue:      rgba(37, 99, 235, 0.4);
    --glow-cyan:      rgba(6, 182, 212, 0.35);
    --glow-green:     rgba(16, 185, 129, 0.35);
    --glow-red:       rgba(239, 68, 68, 0.35);
  }

  html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
  }

  /* ── Streamlit chrome overrides ── */
  .stApp { background-color: var(--bg-primary) !important; }
  section[data-testid="stSidebar"] { background-color: var(--bg-secondary) !important; border-right: 1px solid var(--border); }
  .stTabs [data-baseweb="tab-list"] { background-color: var(--bg-secondary) !important; border-radius: 12px; padding: 4px; gap: 4px; }
  .stTabs [data-baseweb="tab"] { background-color: transparent !important; color: var(--text-secondary) !important; border-radius: 8px !important; font-weight: 500; transition: all 0.2s; }
  .stTabs [aria-selected="true"] { background-color: var(--bg-card) !important; color: var(--text-primary) !important; box-shadow: 0 0 12px rgba(37,99,235,0.2); }
  .stTabs [data-baseweb="tab-panel"] { padding-top: 24px !important; }

  div[data-testid="stTextInput"] > div > div > input,
  div[data-testid="stTextArea"] > div > textarea {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  div[data-testid="stTextInput"] > div > div > input:focus,
  div[data-testid="stTextArea"] > div > textarea:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.15) !important;
  }

  div[data-testid="stSelectbox"] > div > div {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
  }

  div[data-testid="stToggle"] label { color: var(--text-primary) !important; }

  div[data-testid="metric-container"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
  }
  div[data-testid="metric-container"] label { color: var(--text-secondary) !important; font-size: 12px !important; text-transform: uppercase; letter-spacing: 0.08em; }
  div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: var(--text-primary) !important; font-size: 24px !important; font-weight: 700 !important; }

  div[data-testid="stProgress"] > div > div > div {
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan)) !important;
    border-radius: 4px;
  }
  div[data-testid="stProgress"] > div { background-color: var(--border) !important; border-radius: 4px; }

  .stExpander { border: 1px solid var(--border) !important; border-radius: 12px !important; background-color: var(--bg-card) !important; }
  .stExpander summary { color: var(--text-secondary) !important; }
  .stExpander[open] summary { color: var(--text-primary) !important; }

  div[data-testid="stAlert"] { border-radius: 10px !important; }

  /* ── Hero / Landing ── */
  .hero-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 70vh;
    gap: 32px;
    padding: 40px 20px;
  }
  .hero-logo {
    font-size: clamp(28px, 5vw, 42px);
    font-weight: 900;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #2563eb 0%, #06b6d4 50%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    line-height: 1.1;
  }
  .hero-tagline {
    font-size: clamp(13px, 2vw, 15px);
    color: var(--text-secondary);
    text-align: center;
    max-width: 480px;
    line-height: 1.6;
    font-weight: 400;
  }
  .ticker-label {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
    text-align: center;
  }

  /* ── Glowing Scan Button ── */
  .glow-btn-wrapper { display: flex; justify-content: center; width: 100%; }
  .glow-btn-wrapper .stButton > button {
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 40%, #0891b2 100%) !important;
    color: #ffffff !important;
    font-size: clamp(16px, 2.5vw, 20px) !important;
    font-weight: 800 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.02em !important;
    padding: 20px 52px !important;
    border-radius: 50px !important;
    border: 1px solid rgba(37,99,235,0.6) !important;
    box-shadow:
      0 0 20px rgba(37,99,235,0.5),
      0 0 50px rgba(37,99,235,0.25),
      0 0 90px rgba(6,182,212,0.15),
      inset 0 1px 0 rgba(255,255,255,0.1) !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
    min-width: 280px !important;
    animation: pulseGlow 3s ease-in-out infinite;
  }
  .glow-btn-wrapper .stButton > button:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow:
      0 0 30px rgba(37,99,235,0.7),
      0 0 70px rgba(37,99,235,0.4),
      0 0 120px rgba(6,182,212,0.2),
      inset 0 1px 0 rgba(255,255,255,0.15) !important;
  }
  .glow-btn-wrapper .stButton > button:active { transform: translateY(0) scale(0.99) !important; }
  @keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 20px rgba(37,99,235,0.5), 0 0 50px rgba(37,99,235,0.25), 0 0 90px rgba(6,182,212,0.15), inset 0 1px 0 rgba(255,255,255,0.1); }
    50%       { box-shadow: 0 0 35px rgba(37,99,235,0.7), 0 0 75px rgba(37,99,235,0.4), 0 0 120px rgba(6,182,212,0.25), inset 0 1px 0 rgba(255,255,255,0.15); }
  }

  /* ── Risk Verdict Header ── */
  .verdict-banner {
    border-radius: 16px;
    padding: 28px 32px;
    text-align: center;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
  }
  .verdict-banner::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 16px;
    pointer-events: none;
  }
  .verdict-on {
    background: linear-gradient(135deg, rgba(16,185,129,0.12) 0%, rgba(6,182,212,0.08) 100%);
    border: 1px solid rgba(16,185,129,0.35);
    box-shadow: 0 0 40px rgba(16,185,129,0.12), inset 0 1px 0 rgba(16,185,129,0.15);
  }
  .verdict-off {
    background: linear-gradient(135deg, rgba(239,68,68,0.12) 0%, rgba(245,158,11,0.08) 100%);
    border: 1px solid rgba(239,68,68,0.35);
    box-shadow: 0 0 40px rgba(239,68,68,0.12), inset 0 1px 0 rgba(239,68,68,0.15);
  }
  .verdict-title {
    font-size: clamp(13px, 2vw, 14px);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--text-secondary);
    margin-bottom: 10px;
  }
  .verdict-value {
    font-size: clamp(32px, 6vw, 52px);
    font-weight: 900;
    letter-spacing: -0.02em;
    line-height: 1;
    margin-bottom: 8px;
  }
  .verdict-on  .verdict-value { color: #10b981; text-shadow: 0 0 30px rgba(16,185,129,0.5); }
  .verdict-off .verdict-value { color: #ef4444; text-shadow: 0 0 30px rgba(239,68,68,0.5); }
  .verdict-confidence {
    font-size: 15px;
    color: var(--text-secondary);
    font-weight: 500;
  }

  /* ── Info / Timing Card ── */
  .timing-card {
    background: linear-gradient(135deg, rgba(139,92,246,0.1) 0%, rgba(37,99,235,0.06) 100%);
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 12px;
    padding: 18px 22px;
    font-size: 15px;
    font-weight: 500;
    color: var(--text-primary);
    line-height: 1.5;
    box-shadow: 0 0 20px rgba(139,92,246,0.08);
  }
  .timing-label {
    font-size: 11px;
    font-weight: 700;
    color: #8b5cf6;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 8px;
  }

  /* ── Driver Bullets ── */
  .driver-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    margin-bottom: 8px;
    font-size: 14px;
    line-height: 1.5;
    color: var(--text-primary);
    transition: border-color 0.2s;
  }
  .driver-item:hover { border-color: var(--border-glow); }
  .driver-dot {
    width: 8px;
    height: 8px;
    min-width: 8px;
    border-radius: 50%;
    margin-top: 6px;
  }
  .driver-gov  .driver-dot { background: var(--accent-orange); box-shadow: 0 0 8px rgba(245,158,11,0.5); }
  .driver-macro .driver-dot { background: var(--accent-cyan);   box-shadow: 0 0 8px rgba(6,182,212,0.5);  }
  .driver-tech  .driver-dot { background: var(--accent-purple); box-shadow: 0 0 8px rgba(139,92,246,0.5); }

  /* ── Portfolio Ticker Cards ── */
  .ticker-card {
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
  }
  .ticker-card:hover { transform: translateY(-2px); }
  .tc-strongly-bullish { background: linear-gradient(135deg,rgba(16,185,129,0.14),rgba(6,182,212,0.07)); border: 1px solid rgba(16,185,129,0.4); box-shadow: 0 0 24px rgba(16,185,129,0.1); }
  .tc-bullish           { background: linear-gradient(135deg,rgba(16,185,129,0.08),rgba(6,182,212,0.04)); border: 1px solid rgba(16,185,129,0.25); }
  .tc-neutral           { background: linear-gradient(135deg,rgba(245,158,11,0.08),rgba(37,99,235,0.04));  border: 1px solid rgba(245,158,11,0.25); }
  .tc-bearish           { background: linear-gradient(135deg,rgba(239,68,68,0.08),rgba(245,158,11,0.04));  border: 1px solid rgba(239,68,68,0.25); }
  .tc-strongly-bearish  { background: linear-gradient(135deg,rgba(239,68,68,0.14),rgba(245,158,11,0.07));  border: 1px solid rgba(239,68,68,0.4); box-shadow: 0 0 24px rgba(239,68,68,0.1); }

  .tc-ticker   { font-size: 20px; font-weight: 900; letter-spacing: -0.01em; margin-bottom: 4px; font-family: 'JetBrains Mono', monospace; }
  .tc-strongly-bullish .tc-ticker, .tc-bullish .tc-ticker { color: #10b981; }
  .tc-neutral .tc-ticker { color: #f59e0b; }
  .tc-bearish .tc-ticker, .tc-strongly-bearish .tc-ticker { color: #ef4444; }

  .tc-badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 10px;
  }
  .tc-strongly-bullish .tc-badge { background: rgba(16,185,129,0.2); color: #10b981; }
  .tc-bullish .tc-badge           { background: rgba(16,185,129,0.13); color: #34d399; }
  .tc-neutral .tc-badge           { background: rgba(245,158,11,0.15); color: #f59e0b; }
  .tc-bearish .tc-badge           { background: rgba(239,68,68,0.13); color: #f87171; }
  .tc-strongly-bearish .tc-badge  { background: rgba(239,68,68,0.2); color: #ef4444; }

  .tc-reason  { font-size: 13px; color: var(--text-secondary); margin-bottom: 10px; line-height: 1.5; }
  .tc-move    { font-size: 13px; color: var(--text-muted); margin-bottom: 10px; font-family: 'JetBrains Mono', monospace; }
  .tc-action  { font-size: 13px; font-weight: 600; color: var(--text-primary); }
  .tc-action-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted); margin-bottom: 2px; }

  /* ── Sources ── */
  .source-tag {
    display: inline-block;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 12px;
    color: var(--text-muted);
    margin: 3px;
    font-family: 'JetBrains Mono', monospace;
  }

  /* ── History Card ── */
  .history-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 16px;
    transition: border-color 0.2s;
    cursor: pointer;
  }
  .history-card:hover { border-color: var(--border-glow); }
  .history-ts { font-size: 12px; color: var(--text-muted); font-family: 'JetBrains Mono', monospace; min-width: 110px; }
  .history-verdict { font-size: 14px; font-weight: 700; }
  .history-on  { color: #10b981; }
  .history-off { color: #ef4444; }
  .history-conf { font-size: 12px; color: var(--text-secondary); margin-left: auto; }

  /* ── Disclaimer Banner ── */
  .disclaimer-banner {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(239,68,68,0.12);
    border-top: 1px solid rgba(239,68,68,0.3);
    padding: 8px 16px;
    font-size: 11px;
    color: rgba(239,68,68,0.9);
    text-align: center;
    z-index: 9999;
    backdrop-filter: blur(8px);
    font-weight: 500;
  }

  /* ── Section Headers ── */
  .section-header {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--text-muted);
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }

  /* ── Scan Mode Toggle ── */
  .scan-mode-label { font-size: 12px; color: var(--text-muted); text-align: center; }

  /* ── Responsive tweaks ── */
  @media (max-width: 640px) {
    .verdict-value { font-size: 36px !important; }
    .glow-btn-wrapper .stButton > button { padding: 18px 36px !important; font-size: 16px !important; min-width: 240px !important; }
    .hero-container { min-height: 60vh; gap: 24px; padding: 24px 12px; }
  }
</style>

<div class="disclaimer-banner">
  ⚠️ DISCLAIMER: PulseScan is for informational & educational purposes only. NOT financial advice.
  All analysis is AI-generated. Do your own research. Past signals do not guarantee future results.
</div>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ─── Constants ─────────────────────────────────────────────────────────────────
SCAN_HISTORY_KEY = "scan_history"
MAX_HISTORY = 7

# ─── Helper: Load API Keys ──────────────────────────────────────────────────────
def get_secret(key: str, default: str = "") -> str:
    try:
        return st.secrets[key]
    except Exception:
        return default

ANTHROPIC_KEY  = get_secret("ANTHROPIC_API_KEY")
FRED_KEY       = get_secret("FRED_API_KEY")
FINNHUB_KEY    = get_secret("FINNHUB_API_KEY")
CONGRESS_KEY   = get_secret("CONGRESS_API_KEY")

# ─── Data Fetchers ─────────────────────────────────────────────────────────────

@st.cache_data(ttl=900)
def fetch_fred_series(series_id: str) -> dict:
    """Fetch most recent FRED observation for a series."""
    try:
        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            "series_id": series_id,
            "api_key": FRED_KEY,
            "file_type": "json",
            "sort_order": "desc",
            "limit": 3,
        }
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        obs = r.json().get("observations", [])
        values = [(o["date"], o["value"]) for o in obs if o["value"] != "."]
        return {"series": series_id, "latest": values[0] if values else ("N/A", "N/A"), "prev": values[1] if len(values) > 1 else ("N/A", "N/A")}
    except Exception as e:
        return {"series": series_id, "latest": ("N/A", "N/A"), "prev": ("N/A", "N/A"), "error": str(e)}


@st.cache_data(ttl=900)
def fetch_fred_macro() -> dict:
    """Fetch key FRED macro indicators."""
    series_map = {
        "fed_funds_rate":   "FEDFUNDS",
        "cpi_yoy":         "CPIAUCSL",
        "unemployment":    "UNRATE",
        "gdp_growth":      "A191RL1Q225SBEA",
        "10y_treasury":    "DGS10",
        "2y_treasury":     "DGS2",
        "yield_curve_10_2":"T10Y2Y",
        "vix":             "VIXCLS",
        "m2_money_supply": "M2SL",
        "retail_sales":    "RSAFS",
        "ism_pmi":         "MANEMP",
        "initial_claims":  "IC4WSA",
    }
    result = {}
    for name, sid in series_map.items():
        result[name] = fetch_fred_series(sid)
    return result


@st.cache_data(ttl=600)
def fetch_finnhub_market_news() -> list:
    """Fetch general market news from Finnhub."""
    try:
        url = "https://finnhub.io/api/v1/news"
        params = {"category": "general", "token": FINNHUB_KEY, "minId": 0}
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        items = r.json()[:20]
        return [{"headline": i.get("headline",""), "summary": i.get("summary","")[:200], "source": i.get("source",""), "datetime": i.get("datetime",0)} for i in items]
    except Exception as e:
        return [{"error": str(e)}]


@st.cache_data(ttl=600)
def fetch_finnhub_economic_calendar() -> list:
    """Fetch economic calendar events from Finnhub."""
    try:
        today = datetime.date.today()
        week  = today + datetime.timedelta(days=7)
        url   = "https://finnhub.io/api/v1/calendar/economic"
        params = {"from": str(today), "to": str(week), "token": FINNHUB_KEY}
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        events = r.json().get("economicCalendar", [])[:15]
        return [{"event": e.get("event",""), "impact": e.get("impact",""), "country": e.get("country",""), "actual": e.get("actual",""), "estimate": e.get("estimate",""), "time": e.get("time","")} for e in events]
    except Exception as e:
        return [{"error": str(e)}]


@st.cache_data(ttl=600)
def fetch_congress_recent() -> list:
    """Fetch recent Congressional activity."""
    try:
        url = "https://api.congress.gov/v3/bill"
        params = {"api_key": CONGRESS_KEY, "limit": 15, "sort": "updateDate+desc", "format": "json"}
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        bills = r.json().get("bills", [])
        return [{"title": b.get("title","")[:180], "congress": b.get("congress",""), "type": b.get("type",""), "latestAction": b.get("latestAction",{}).get("text","")[:120], "updateDate": b.get("updateDate","")} for b in bills]
    except Exception as e:
        return [{"error": str(e)}]


@st.cache_data(ttl=600)
def fetch_finnhub_company_profile(ticker: str) -> dict:
    """Fetch company profile from Finnhub."""
    try:
        url = "https://finnhub.io/api/v1/stock/profile2"
        params = {"symbol": ticker.upper(), "token": FINNHUB_KEY}
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e), "symbol": ticker}


@st.cache_data(ttl=600)
def fetch_finnhub_company_news(ticker: str) -> list:
    """Fetch last 30 days of company news from Finnhub."""
    try:
        today    = datetime.date.today()
        from_dt  = today - datetime.timedelta(days=30)
        url      = "https://finnhub.io/api/v1/company-news"
        params   = {"symbol": ticker.upper(), "from": str(from_dt), "to": str(today), "token": FINNHUB_KEY}
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        items = r.json()[:12]
        return [{"headline": i.get("headline",""), "summary": i.get("summary","")[:200], "source": i.get("source",""), "datetime": i.get("datetime",0)} for i in items]
    except Exception as e:
        return [{"error": str(e)}]


@st.cache_data(ttl=600)
def fetch_finnhub_quote(ticker: str) -> dict:
    """Fetch real-time quote from Finnhub."""
    try:
        url    = "https://finnhub.io/api/v1/quote"
        params = {"symbol": ticker.upper(), "token": FINNHUB_KEY}
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def fetch_portfolio_data(tickers: list) -> dict:
    """Batch-fetch profile + news + quote for each ticker."""
    portfolio = {}
    for t in tickers:
        t = t.strip().upper()
        if not t:
            continue
        portfolio[t] = {
            "profile": fetch_finnhub_company_profile(t),
            "news":    fetch_finnhub_company_news(t),
            "quote":   fetch_finnhub_quote(t),
        }
    return portfolio

# ─── AI Prompts & Callers ───────────────────────────────────────────────────────

GOVT_POLICY_PROMPT = """You are an elite Government & Policy Risk Analyst at a macro hedge fund.
You have just received the latest data on U.S. Congressional bills and activities.
Your job: analyze the government/policy landscape for market risk implications.

CONGRESSIONAL DATA:
{congress_data}

MARKET NEWS (policy-relevant excerpts):
{market_news}

Respond with a JSON object ONLY (no markdown, no explanation outside JSON):
{{
  "policy_risk_level": "high"|"medium"|"low",
  "direction": "risk_on"|"risk_off"|"neutral",
  "confidence": 0-100,
  "key_factors": ["factor1","factor2","factor3","factor4"],
  "legislative_outlook_7d": "one concise sentence",
  "geopolitical_flag": true|false,
  "geopolitical_note": "brief note or empty string",
  "reasoning": "2-3 sentences max"
}}
Weight: This analysis carries 60% of the final risk score. Be precise and evidence-based."""

MACRO_PROMPT = """You are a Senior Macro & Economic Analyst at a global macro hedge fund.
Analyze the following FRED economic data and upcoming economic calendar events.

FRED MACRO DATA:
{fred_data}

ECONOMIC CALENDAR (next 7 days):
{calendar_data}

Respond with a JSON object ONLY (no markdown, no explanation outside JSON):
{{
  "macro_risk_level": "high"|"medium"|"low",
  "direction": "risk_on"|"risk_off"|"neutral",
  "confidence": 0-100,
  "key_factors": ["factor1","factor2","factor3"],
  "yield_curve_signal": "inverted"|"flat"|"normal"|"steepening",
  "fed_stance": "hawkish"|"neutral"|"dovish",
  "inflation_trend": "accelerating"|"stable"|"decelerating",
  "economic_momentum": "expanding"|"stable"|"contracting",
  "major_calendar_risk": "brief note on biggest upcoming event",
  "reasoning": "2-3 sentences max"
}}"""

TECHNICALS_PROMPT = """You are a Chief Market Technicals & Sentiment Analyst at a hedge fund.
Analyze the following recent market news and sentiment data.

MARKET NEWS & SENTIMENT:
{market_news}

VIX DATA: {vix_data}
10Y TREASURY: {treasury_10y}
2Y TREASURY: {treasury_2y}
YIELD CURVE (10Y-2Y): {yield_curve}

Respond with a JSON object ONLY (no markdown, no explanation outside JSON):
{{
  "technical_risk_level": "high"|"medium"|"low",
  "direction": "risk_on"|"risk_off"|"neutral",
  "confidence": 0-100,
  "key_factors": ["factor1","factor2","factor3"],
  "vix_signal": "fear"|"elevated"|"normal"|"complacency",
  "sentiment_bias": "bullish"|"neutral"|"bearish",
  "momentum": "strong_up"|"up"|"flat"|"down"|"strong_down",
  "key_risk_events": ["event1","event2"],
  "reasoning": "2-3 sentences max"
}}"""

PORTFOLIO_PROMPT = """You are an Elite Portfolio Impact Analyst at a macro hedge fund.
Given the current macro, government/policy, and market environment described below,
analyze the specific impact on each ticker in the portfolio.

CURRENT ENVIRONMENT SUMMARY:
- Policy/Gov Direction: {policy_direction} (confidence: {policy_confidence}%)
- Macro Direction: {macro_direction} (confidence: {macro_confidence}%)
- Technical Direction: {tech_direction} (confidence: {tech_confidence}%)
- Key Gov Factors: {gov_factors}
- Key Macro Factors: {macro_factors}

PORTFOLIO DATA (profile + recent 30-day news per ticker):
{portfolio_data}

For EACH ticker, provide a precise impact assessment. Consider:
- Company sector vs. current policy/gov spending priorities
- How macro environment (rates, growth, inflation) affects this specific business
- Recent company-specific news catalysts
- Sector rotation implications given the risk environment

Respond with a JSON object ONLY (no markdown, no explanation outside JSON):
{{
  "ticker_impacts": [
    {{
      "ticker": "SYMBOL",
      "impact": "strongly_bullish"|"bullish"|"neutral"|"bearish"|"strongly_bearish",
      "reason": "one crisp sentence explaining the specific catalysts",
      "suggested_action": "Enter now"|"Wait for pullback"|"Scale in slowly"|"Hold current position"|"Reduce exposure"|"Exit / Avoid",
      "expected_move": "X-Y% upside/downside in N-M days (or empty string if uncertain)"
    }}
  ]
}}"""

SYNTHESIZER_PROMPT = """You are the Chief Risk Officer and Final Synthesizer at an elite macro hedge fund.
You must produce the definitive Risk On / Risk Off verdict by weighing:
- Government/Policy Analysis (60% weight — MOST IMPORTANT)
- Macro/Economic Analysis (25% weight)
- Market Technicals/Sentiment (15% weight)

GOVERNMENT/POLICY ANALYSIS (60% weight):
{govt_analysis}

MACRO ANALYSIS (25% weight):
{macro_analysis}

TECHNICALS ANALYSIS (15% weight):
{tech_analysis}

{ticker_section}

RISK DEFINITIONS (enforce strictly):
- RISK ON:  Bullish equities/crypto/high-yield, falling VIX, strong growth signals,
            dovish Fed, fiscal stimulus, geopolitical calm, strong momentum.
- RISK OFF: Bearish equities, rising VIX, credit stress, hawkish Fed, geopolitical
            escalation, fiscal tightening, economic contraction signals, flight to safety.

Produce the final verdict for TODAY (next 24h) and THIS WEEK (next 5-7 trading days).
Be opinionated and precise. Do NOT hedge excessively.

Respond with a JSON object ONLY (no markdown, no explanation outside JSON):
{{
  "daily_risk": "ON"|"OFF",
  "weekly_risk": "ON"|"OFF",
  "daily_confidence": 0-100,
  "weekly_confidence": 0-100,
  "summary": "2-3 sentences explaining the verdict",
  "timing_advice": "one precise, actionable sentence (e.g., 'Add risk exposure in first 90 mins of tomorrow session; cut if SPY loses 5,480')",
  "key_drivers": [
    "Gov/Policy: ...",
    "Gov/Policy: ...",
    "Macro: ...",
    "Technical: ..."
  ],
  "ticker_impacts": {ticker_impacts_placeholder},
  "sources": ["FRED", "Finnhub", "Congress.gov", "Anthropic AI Analysis"]
}}"""


def call_anthropic(prompt: str, system: str = "You are a precise financial analyst. Output valid JSON only.") -> dict:
    """Call Anthropic API and return parsed JSON."""
    if not ANTHROPIC_KEY:
        return {"error": "ANTHROPIC_API_KEY not configured"}
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            temperature=0.0,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = msg.content[0].text.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)
    except json.JSONDecodeError as e:
        return {"error": f"JSON parse error: {e}", "raw": raw if 'raw' in dir() else ""}
    except Exception as e:
        return {"error": str(e)}


# ─── Core Scan Orchestrator ─────────────────────────────────────────────────────

def run_scan(tickers: list, deep: bool = True) -> dict:
    """
    Execute the full 5-step PulseScan analysis.
    Returns the synthesized result dict.
    """
    steps_total = 5 + (1 if tickers else 0)
    step_n = [0]

    status_container = st.empty()

    def advance(label: str):
        step_n[0] += 1
        status_container.markdown(
            f"""
            <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:16px 20px;margin-bottom:8px;">
              <div style="font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;">
                Step {step_n[0]} / {steps_total}
              </div>
              <div style="font-size:14px;color:var(--text-primary);font-weight:500;">
                ⚡ {label}
              </div>
              <div style="margin-top:10px;height:3px;background:var(--border);border-radius:2px;overflow:hidden;">
                <div style="height:100%;width:{int(step_n[0]/steps_total*100)}%;background:linear-gradient(90deg,#2563eb,#06b6d4);border-radius:2px;transition:width 0.4s;"></div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Step 1: Fetch Data ────────────────────────────────────────────────────
    advance("Fetching live data — FRED, Finnhub, Congress.gov...")
    fred_data      = fetch_fred_macro()
    market_news    = fetch_finnhub_market_news()
    calendar_data  = fetch_finnhub_economic_calendar()
    congress_data  = fetch_congress_recent()

    portfolio_data = {}
    if tickers:
        portfolio_data = fetch_portfolio_data(tickers)

    # ── Step 2: Government & Policy Analyst (60% weight) ─────────────────────
    advance("Running Government & Policy Analyst (60% weight)...")
    govt_result = call_anthropic(
        GOVT_POLICY_PROMPT.format(
            congress_data=json.dumps(congress_data, indent=2)[:6000],
            market_news=json.dumps(market_news[:8], indent=2)[:3000],
        )
    )

    # ── Step 3: Macro & Economic Analyst (25% weight) ─────────────────────────
    advance("Running Macro & Economic Analyst (25% weight)...")
    macro_result = call_anthropic(
        MACRO_PROMPT.format(
            fred_data=json.dumps(fred_data, indent=2)[:6000],
            calendar_data=json.dumps(calendar_data, indent=2)[:3000],
        )
    )

    # ── Step 4: Market Technicals & Sentiment (15% weight) ───────────────────
    advance("Running Market Technicals & Sentiment Analyst (15% weight)...")
    vix_data     = fred_data.get("vix", {}).get("latest", ("N/A","N/A"))
    t10y         = fred_data.get("10y_treasury", {}).get("latest", ("N/A","N/A"))
    t2y          = fred_data.get("2y_treasury", {}).get("latest", ("N/A","N/A"))
    yc           = fred_data.get("yield_curve_10_2", {}).get("latest", ("N/A","N/A"))
    tech_result  = call_anthropic(
        TECHNICALS_PROMPT.format(
            market_news=json.dumps(market_news, indent=2)[:6000],
            vix_data=f"{vix_data[1]} (as of {vix_data[0]})",
            treasury_10y=f"{t10y[1]}% (as of {t10y[0]})",
            treasury_2y=f"{t2y[1]}% (as of {t2y[0]})",
            yield_curve=f"{yc[1]}bp (as of {yc[0]})",
        )
    )

    # ── Step 5 (optional): Portfolio Impact Analyst ───────────────────────────
    portfolio_result = {}
    if tickers:
        advance("Running Portfolio Impact Analyst for your tickers...")
        portfolio_result = call_anthropic(
            PORTFOLIO_PROMPT.format(
                policy_direction=govt_result.get("direction","unknown"),
                policy_confidence=govt_result.get("confidence",0),
                macro_direction=macro_result.get("direction","unknown"),
                macro_confidence=macro_result.get("confidence",0),
                tech_direction=tech_result.get("direction","unknown"),
                tech_confidence=tech_result.get("confidence",0),
                gov_factors=json.dumps(govt_result.get("key_factors",[])),
                macro_factors=json.dumps(macro_result.get("key_factors",[])),
                portfolio_data=json.dumps(portfolio_data, indent=2)[:8000],
            )
        )

    # ── Final Step: Synthesizer ───────────────────────────────────────────────
    advance("Synthesizing final Risk On / Risk Off verdict...")
    ticker_section = ""
    ticker_impacts_placeholder = "[]"
    if tickers and portfolio_result.get("ticker_impacts"):
        ticker_section = f"\nPORTFOLIO IMPACT ANALYSIS:\n{json.dumps(portfolio_result['ticker_impacts'], indent=2)}"
        ticker_impacts_placeholder = json.dumps(portfolio_result["ticker_impacts"])

    final_result = call_anthropic(
        SYNTHESIZER_PROMPT.format(
            govt_analysis=json.dumps(govt_result, indent=2)[:3000],
            macro_analysis=json.dumps(macro_result, indent=2)[:2000],
            tech_analysis=json.dumps(tech_result, indent=2)[:2000],
            ticker_section=ticker_section,
            ticker_impacts_placeholder=ticker_impacts_placeholder,
        )
    )

    status_container.empty()

    # Attach sub-analyses for reasoning trace
    final_result["_govt"]      = govt_result
    final_result["_macro"]     = macro_result
    final_result["_tech"]      = tech_result
    final_result["_portfolio"] = portfolio_result
    final_result["_ts"]        = datetime.datetime.now().isoformat()
    final_result["_tickers"]   = tickers

    return final_result

# ─── Rendering Helpers ──────────────────────────────────────────────────────────

def render_verdict_banner(period: str, risk: str, confidence: int):
    """Render a big Risk ON / Risk OFF banner."""
    icon  = "🔥" if risk == "ON" else "❄️"
    cls   = "verdict-on" if risk == "ON" else "verdict-off"
    label = "RISK ON" if risk == "ON" else "RISK OFF"
    st.markdown(
        f"""
        <div class="verdict-banner {cls}">
          <div class="verdict-title">{period}</div>
          <div class="verdict-value">{icon} {label}</div>
          <div class="verdict-confidence">Confidence: {confidence}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_gauge(daily_conf: int, weekly_conf: int, daily_risk: str, weekly_risk: str):
    """Render a Plotly gauge for composite risk confidence."""
    daily_score  = daily_conf  if daily_risk  == "ON" else -daily_conf
    weekly_score = weekly_conf if weekly_risk == "ON" else -weekly_conf
    composite    = (daily_score * 0.55 + weekly_score * 0.45)
    gauge_val    = (composite + 100) / 2  # map -100..+100 → 0..100

    color = "#10b981" if composite > 0 else "#ef4444"
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=gauge_val,
        number={"suffix": "", "font": {"size": 32, "color": color, "family": "Inter"}},
        delta={"reference": 50, "increasing": {"color": "#10b981"}, "decreasing": {"color": "#ef4444"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#4a5a72",
                     "tickvals": [0,25,50,75,100], "ticktext":["MAX\nRISK OFF","","NEUTRAL","","MAX\nRISK ON"],
                     "tickfont": {"color":"#4a5a72","size":9}},
            "bar": {"color": color, "thickness": 0.25},
            "bgcolor": "#131929",
            "borderwidth": 0,
            "steps": [
                {"range":[0,25],  "color":"rgba(239,68,68,0.15)"},
                {"range":[25,42], "color":"rgba(245,158,11,0.1)"},
                {"range":[42,58], "color":"rgba(100,116,139,0.1)"},
                {"range":[58,75], "color":"rgba(16,185,129,0.1)"},
                {"range":[75,100],"color":"rgba(16,185,129,0.15)"},
            ],
            "threshold": {"line":{"color":"white","width":2},"thickness":0.8,"value":gauge_val},
        },
        title={"text":"RISK COMPOSITE SCORE","font":{"size":11,"color":"#7a8ba8","family":"Inter"}},
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color":"#e8edf5","family":"Inter"},
        height=220,
        margin=dict(t=40,b=0,l=20,r=20),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_key_drivers(drivers: list):
    """Render key driver bullets with color-coded dots."""
    st.markdown('<div class="section-header">KEY DRIVERS</div>', unsafe_allow_html=True)
    for i, d in enumerate(drivers):
        if i < 2:
            cls = "driver-gov"
        elif i == 2:
            cls = "driver-macro"
        else:
            cls = "driver-tech"
        st.markdown(
            f'<div class="driver-item {cls}"><span class="driver-dot"></span><span>{d}</span></div>',
            unsafe_allow_html=True,
        )


def render_timing_card(advice: str):
    """Render the timing recommendation card."""
    st.markdown(
        f"""
        <div class="timing-card">
          <div class="timing-label">⏱ Timing Recommendation</div>
          {advice}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_ticker_cards(ticker_impacts: list):
    """Render beautiful portfolio impact cards."""
    if not ticker_impacts:
        return
    st.markdown('<div class="section-header" style="margin-top:24px;">YOUR PORTFOLIO IMPACT</div>', unsafe_allow_html=True)
    for ti in ticker_impacts:
        impact = ti.get("impact","neutral").lower().replace(" ","_")
        css_cls = f"tc-{impact}"
        badge_text = impact.replace("_"," ").upper()
        move   = ti.get("expected_move","")
        move_html = f'<div class="tc-move">📊 {move}</div>' if move else ""
        st.markdown(
            f"""
            <div class="ticker-card {css_cls}">
              <div class="tc-ticker">{ti.get("ticker","?")}</div>
              <span class="tc-badge">{badge_text}</span>
              <div class="tc-reason">{ti.get("reason","")}</div>
              {move_html}
              <div class="tc-action-label">Suggested Action</div>
              <div class="tc-action">→ {ti.get("suggested_action","")}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_sources(sources: list):
    """Render source tags."""
    st.markdown('<div class="section-header" style="margin-top:20px;">DATA SOURCES</div>', unsafe_allow_html=True)
    tags_html = "".join(f'<span class="source-tag">{s}</span>' for s in sources)
    st.markdown(f'<div>{tags_html}</div>', unsafe_allow_html=True)


def render_results(result: dict):
    """Render the full results panel."""
    if result.get("error"):
        st.error(f"Scan error: {result['error']}")
        return

    daily_risk    = result.get("daily_risk","?")
    weekly_risk   = result.get("weekly_risk","?")
    daily_conf    = result.get("daily_confidence",50)
    weekly_conf   = result.get("weekly_confidence",50)
    summary       = result.get("summary","")
    timing        = result.get("timing_advice","")
    drivers       = result.get("key_drivers",[])
    ticker_imp    = result.get("ticker_impacts",[])
    sources       = result.get("sources",["FRED","Finnhub","Congress.gov"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Verdict banners ──────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        render_verdict_banner("TODAY (24H)", daily_risk, daily_conf)
    with col2:
        render_verdict_banner("THIS WEEK (5-7D)", weekly_risk, weekly_conf)

    # ── Gauge ───────────────────────────────────────────────────────────────
    render_gauge(daily_conf, weekly_conf, daily_risk, weekly_risk)

    # ── Summary ─────────────────────────────────────────────────────────────
    if summary:
        st.markdown(
            f'<div style="background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:16px 20px;color:var(--text-secondary);font-size:14px;line-height:1.7;margin-bottom:20px;">{summary}</div>',
            unsafe_allow_html=True,
        )

    # ── Timing ──────────────────────────────────────────────────────────────
    if timing:
        render_timing_card(timing)
        st.markdown("<br>", unsafe_allow_html=True)

    # ── Metrics bar ─────────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    fred = st.session_state.get("_last_fred", {})
    with m1:
        vix = fred.get("vix",{}).get("latest",("N/A","N/A"))
        st.metric("VIX", vix[1], delta=None)
    with m2:
        t10 = fred.get("10y_treasury",{}).get("latest",("N/A","N/A"))
        st.metric("10Y Yield", f"{t10[1]}%")
    with m3:
        yc  = fred.get("yield_curve_10_2",{}).get("latest",("N/A","N/A"))
        st.metric("10Y-2Y Spread", f"{yc[1]}")
    with m4:
        un  = fred.get("unemployment",{}).get("latest",("N/A","N/A"))
        st.metric("Unemployment", f"{un[1]}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Key Drivers ─────────────────────────────────────────────────────────
    render_key_drivers(drivers)

    # ── Portfolio Impact ─────────────────────────────────────────────────────
    if ticker_imp:
        render_ticker_cards(ticker_imp)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Full Reasoning Trace ─────────────────────────────────────────────────
    with st.expander("🔬 Full Reasoning Trace", expanded=False):
        govt = result.get("_govt",{})
        macro = result.get("_macro",{})
        tech  = result.get("_tech",{})
        port  = result.get("_portfolio",{})

        st.markdown("**Government & Policy Analyst (60% weight)**")
        st.markdown(f"Direction: `{govt.get('direction','?')}` | Confidence: `{govt.get('confidence','?')}%` | Risk Level: `{govt.get('policy_risk_level','?')}`")
        if govt.get("reasoning"): st.caption(govt["reasoning"])
        if govt.get("geopolitical_flag"): st.warning(f"🌍 Geopolitical Flag: {govt.get('geopolitical_note','')}")

        st.divider()
        st.markdown("**Macro & Economic Analyst (25% weight)**")
        st.markdown(f"Direction: `{macro.get('direction','?')}` | Fed: `{macro.get('fed_stance','?')}` | Inflation: `{macro.get('inflation_trend','?')}`")
        if macro.get("reasoning"): st.caption(macro["reasoning"])

        st.divider()
        st.markdown("**Market Technicals & Sentiment (15% weight)**")
        st.markdown(f"Direction: `{tech.get('direction','?')}` | Sentiment: `{tech.get('sentiment_bias','?')}` | VIX Signal: `{tech.get('vix_signal','?')}`")
        if tech.get("reasoning"): st.caption(tech["reasoning"])

        if port:
            st.divider()
            st.markdown("**Portfolio Impact Analyst**")
            st.json(port)

    # ── Sources ─────────────────────────────────────────────────────────────
    render_sources(sources)

    st.markdown("<br><br>", unsafe_allow_html=True)  # space above disclaimer

# ─── History Helpers ────────────────────────────────────────────────────────────

def save_to_history(result: dict):
    if SCAN_HISTORY_KEY not in st.session_state:
        st.session_state[SCAN_HISTORY_KEY] = []
    history = st.session_state[SCAN_HISTORY_KEY]
    slim = {
        "ts": result.get("_ts", datetime.datetime.now().isoformat()),
        "daily_risk": result.get("daily_risk","?"),
        "weekly_risk": result.get("weekly_risk","?"),
        "daily_confidence": result.get("daily_confidence",0),
        "weekly_confidence": result.get("weekly_confidence",0),
        "summary": result.get("summary",""),
        "timing_advice": result.get("timing_advice",""),
        "key_drivers": result.get("key_drivers",[]),
        "ticker_impacts": result.get("ticker_impacts",[]),
        "tickers": result.get("_tickers",[]),
    }
    history.insert(0, slim)
    st.session_state[SCAN_HISTORY_KEY] = history[:MAX_HISTORY]


def render_history_tab():
    history = st.session_state.get(SCAN_HISTORY_KEY, [])
    if not history:
        st.markdown(
            '<div style="text-align:center;padding:60px 20px;color:var(--text-muted);font-size:14px;">No scans yet. Run your first PulseScan!</div>',
            unsafe_allow_html=True,
        )
        return

    for h in history:
        ts      = h.get("ts","")[:16].replace("T"," ")
        d_risk  = h.get("daily_risk","?")
        w_risk  = h.get("weekly_risk","?")
        d_conf  = h.get("daily_confidence",0)
        w_conf  = h.get("weekly_confidence",0)
        tickers = h.get("tickers",[])
        dcls    = "history-on" if d_risk == "ON" else "history-off"
        wcls    = "history-on" if w_risk == "ON" else "history-off"
        icon_d  = "🔥" if d_risk == "ON" else "❄️"
        icon_w  = "🔥" if w_risk == "ON" else "❄️"

        ticker_str = f" | 📊 {', '.join(tickers)}" if tickers else ""

        with st.expander(
            f"{ts}  —  Daily: {icon_d} {d_risk}  •  Weekly: {icon_w} {w_risk}{ticker_str}",
            expanded=False,
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Daily Risk", f"{icon_d} RISK {d_risk}", f"{d_conf}% confidence")
            with col2:
                st.metric("Weekly Risk", f"{icon_w} RISK {w_risk}", f"{w_conf}% confidence")

            if h.get("summary"):
                st.caption(h["summary"])
            if h.get("timing_advice"):
                render_timing_card(h["timing_advice"])
            if h.get("key_drivers"):
                render_key_drivers(h["key_drivers"])
            if h.get("ticker_impacts"):
                render_ticker_cards(h["ticker_impacts"])

# ─── Settings Page ──────────────────────────────────────────────────────────────

def render_settings_tab():
    st.markdown('<div class="section-header">CONFIGURATION</div>', unsafe_allow_html=True)

    st.markdown("**API Key Status**")
    keys = {
        "Anthropic (AI Engine)": ANTHROPIC_KEY,
        "FRED (Economic Data)": FRED_KEY,
        "Finnhub (Market Data)": FINNHUB_KEY,
        "Congress.gov (Policy)": CONGRESS_KEY,
    }
    for name, val in keys.items():
        status = "✅ Configured" if val else "❌ Missing"
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{name}**")
        with col2:
            st.markdown(status)

    st.markdown("---")
    st.markdown("**Cache Settings**")
    st.info("Data is cached for 15 minutes (market news & quotes) or 15 minutes (FRED/Congress). Caches clear automatically.", icon="ℹ️")
    if st.button("🗑️ Clear All Caches", type="secondary"):
        fetch_fred_macro.clear()
        fetch_finnhub_market_news.clear()
        fetch_finnhub_economic_calendar.clear()
        fetch_congress_recent.clear()
        fetch_finnhub_company_profile.clear()
        fetch_finnhub_company_news.clear()
        fetch_finnhub_quote.clear()
        st.success("All caches cleared!")

    st.markdown("---")
    st.markdown("**About PulseScan**")
    st.markdown(
        """
        - **Version**: 1.0.0
        - **Model**: claude-sonnet-4-6 (temperature=0.0)
        - **Architecture**: 5 modular AI calls (Gov 60% / Macro 25% / Tech 15%)
        - **Data Sources**: FRED, Finnhub, Congress.gov
        - **Built by**: PulseScan Architect
        """
    )
    st.markdown("---")
    st.error(
        "⚠️ **DISCLAIMER**: PulseScan is for informational and educational purposes only. "
        "It is NOT financial advice. All analysis is AI-generated and may be incorrect. "
        "Past signals do not guarantee future results. Always do your own research before "
        "making any investment decisions. The creators of PulseScan are not liable for any "
        "financial losses incurred from using this tool.",
        icon="🚫",
    )

# ─── Main App ───────────────────────────────────────────────────────────────────

def main():
    # ── Tab Navigation ────────────────────────────────────────────────────────
    tab_scan, tab_history, tab_settings = st.tabs(["🔬 Scan", "📈 History", "⚙️ Settings"])

    # ─────────────────────────── SCAN TAB ────────────────────────────────────
    with tab_scan:
        # ── Hero ──────────────────────────────────────────────────────────────
        st.markdown(
            """
            <div class="hero-container">
              <div class="hero-logo">🔬 PulseScan<br><span style="font-size:0.55em;font-weight:300;background:linear-gradient(90deg,#7a8ba8,#4a5a72);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">RISK INTELLIGENCE</span></div>
              <div class="hero-tagline">
                Real-time macro + government risk synthesis.<br>
                Powered by FRED · Finnhub · Congress.gov · Claude AI
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Center controls using columns
        _, center_col, _ = st.columns([1, 3, 1])
        with center_col:
            # ── Scan Mode Toggle ─────────────────────────────────────────────
            scan_mode_col1, scan_mode_col2 = st.columns([1, 2])
            with scan_mode_col1:
                deep_scan = st.toggle("Deep Scan", value=True, help="Deep Scan runs more thorough analysis. Quick Scan is faster.")
            with scan_mode_col2:
                mode_label = "🔭 Deep Scan (5+ steps)" if deep_scan else "⚡ Quick Scan (faster)"
                st.markdown(f'<div class="scan-mode-label" style="padding-top:8px;">{mode_label}</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Ticker Input ─────────────────────────────────────────────────
            st.markdown('<div class="ticker-label">Optional: My Portfolio Tickers</div>', unsafe_allow_html=True)
            ticker_input = st.text_input(
                label="tickers",
                placeholder="e.g. PLTR, LMT, AAPL, XOM",
                label_visibility="collapsed",
                help="Comma-separated ticker symbols. Leave blank for a pure macro scan.",
                key="ticker_input",
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Glowing Scan Button ───────────────────────────────────────────
            st.markdown('<div class="glow-btn-wrapper">', unsafe_allow_html=True)
            scan_clicked = st.button("🚀 INITIATE PULSE SCAN", type="primary", use_container_width=False, key="scan_btn")
            st.markdown("</div>", unsafe_allow_html=True)

        # ── Execute Scan ──────────────────────────────────────────────────────
        if scan_clicked:
            tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()] if ticker_input else []

            st.markdown("<br>", unsafe_allow_html=True)
            with st.status("🔬 PulseScan in progress...", expanded=True) as status_widget:
                try:
                    result = run_scan(tickers=tickers, deep=deep_scan)
                    # Cache FRED data for metrics display
                    st.session_state["_last_fred"] = fetch_fred_macro()
                    save_to_history(result)
                    st.session_state["last_result"] = result
                    status_widget.update(label="✅ PulseScan complete!", state="complete")
                except Exception as e:
                    status_widget.update(label=f"❌ Scan failed: {e}", state="error")
                    st.error(str(e))

        # ── Show Last Result ──────────────────────────────────────────────────
        if "last_result" in st.session_state:
            render_results(st.session_state["last_result"])
        elif not scan_clicked:
            # Idle state hint
            st.markdown(
                """
                <div style="text-align:center;padding:20px;color:var(--text-muted);font-size:13px;margin-top:-20px;">
                  Enter tickers above (optional), then hit the button to begin.<br>
                  Gov/Policy analysis · Macro data · Market sentiment · AI synthesis
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ─────────────────────────── HISTORY TAB ─────────────────────────────────
    with tab_history:
        render_history_tab()

    # ─────────────────────────── SETTINGS TAB ────────────────────────────────
    with tab_settings:
        render_settings_tab()


if __name__ == "__main__":
    main()
