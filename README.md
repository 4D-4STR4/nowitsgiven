# 🔬 PulseScan — Elite Risk Intelligence Dashboard

> Real-time macro + government risk synthesis powered by FRED · Finnhub · Congress.gov · Claude AI

---

## What It Does

PulseScan performs a deep, multi-source scan of the current macroeconomic and geopolitical
environment and instantly synthesizes a clear **Risk On / Risk Off** verdict for today (24h)
and this week (5-7 trading days). It optionally adds **personalized portfolio impact analysis**
for any tickers you enter.

### Analysis Architecture (5 modular AI calls, temperature=0.0)

| Step | Analyst | Weight | Data Sources |
|------|---------|--------|-------------|
| 1 | Government & Policy Analyst | **60%** | Congress.gov bills, Finnhub news |
| 2 | Macro & Economic Analyst | **25%** | FRED (12 series), Finnhub economic calendar |
| 3 | Market Technicals & Sentiment | **15%** | FRED VIX/yields, Finnhub market news |
| 4 | Portfolio Impact Analyst | conditional | Finnhub profile2 + 30-day company news |
| 5 | Final Synthesizer | — | All above outputs |

---

## Prerequisites

- Python 3.10+
- API keys for: **Anthropic**, **FRED**, **Finnhub**, **Congress.gov** (all free tiers work)

---

## Local Setup

### 1. Clone & install

```bash
git clone <your-repo-url>
cd nowitsgiven
pip install -r requirements.txt
```

### 2. Configure secrets

```bash
cp .streamlit/secrets.toml .streamlit/secrets.toml.bak  # backup example
```

Edit `.streamlit/secrets.toml` and fill in your real API keys:

```toml
ANTHROPIC_API_KEY  = "sk-ant-api03-..."
FRED_API_KEY       = "your_fred_key"
FINNHUB_API_KEY    = "your_finnhub_key"
CONGRESS_API_KEY   = "your_congress_key"
```

**Get your keys here:**
- Anthropic: https://console.anthropic.com/
- FRED (free): https://fred.stlouisfed.org/docs/api/api_key.html
- Finnhub (free tier): https://finnhub.io/register
- Congress.gov (free): https://api.congress.gov/sign-up/

### 3. Run

```bash
streamlit run app.py
```

Open http://localhost:8501

---

## Streamlit Cloud Deployment

### 1. Push to GitHub

```bash
git add app.py requirements.txt .streamlit/config.toml README.md
git commit -m "Initial PulseScan deploy"
git push origin main
```

> **Do NOT push `secrets.toml`** — add it to `.gitignore`.

### 2. Create `.gitignore`

```
.streamlit/secrets.toml
__pycache__/
*.pyc
.env
```

### 3. Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click **New app** → connect your GitHub repo
3. Set **Main file path** to `app.py`
4. Open **Advanced settings → Secrets** and paste:

```toml
ANTHROPIC_API_KEY  = "sk-ant-api03-..."
FRED_API_KEY       = "your_fred_key"
FINNHUB_API_KEY    = "your_finnhub_key"
CONGRESS_API_KEY   = "your_congress_key"
```

5. Click **Deploy** — your app will be live in ~60 seconds.

---

## Usage

### Basic Scan
1. Open the app → click **🚀 INITIATE PULSE SCAN**
2. Watch the 5-step live analysis run
3. View your **Risk On / Risk Off** verdict + gauge + key drivers + timing advice

### Portfolio Scan
1. Enter tickers in the field above the button: `PLTR, LMT, AAPL, XOM`
2. Click **🚀 INITIATE PULSE SCAN**
3. After the core scan, a 4th AI step analyzes each ticker specifically
4. Cards show bullish/bearish rating, reason, suggested action, expected move

### Tabs
- **🔬 Scan** — main interface
- **📈 History** — last 7 scans with full expandable details
- **⚙️ Settings** — API key status, cache management, about

### Scan Modes
- **Deep Scan** (default) — full 5-step analysis, most accurate
- **Quick Scan** — same pipeline, slightly less token depth

---

## Output Schema

```json
{
  "daily_risk":         "ON" | "OFF",
  "weekly_risk":        "ON" | "OFF",
  "daily_confidence":   0-100,
  "weekly_confidence":  0-100,
  "summary":            "2-3 sentences",
  "timing_advice":      "precise actionable sentence",
  "key_drivers":        ["Gov/Policy: ...", "Macro: ...", "Technical: ..."],
  "ticker_impacts": [
    {
      "ticker":           "PLTR",
      "impact":           "strongly_bullish | bullish | neutral | bearish | strongly_bearish",
      "reason":           "one crisp sentence",
      "suggested_action": "Enter now | Wait for pullback | Reduce exposure | etc.",
      "expected_move":    "8-15% upside in 7-14 days"
    }
  ],
  "sources": ["FRED", "Finnhub", "Congress.gov", "Anthropic AI Analysis"]
}
```

---

## Risk Definitions

| Signal | Meaning |
|--------|---------|
| **RISK ON** 🔥 | Bullish equities/crypto/high-yield; falling VIX; strong growth signals; dovish Fed; fiscal stimulus; geopolitical calm; strong momentum |
| **RISK OFF** ❄️ | Bearish equities; rising VIX; credit stress; hawkish Fed; geopolitical escalation; fiscal tightening; economic contraction; flight to safety |

---

## FRED Data Series Used

| Indicator | Series ID |
|-----------|-----------|
| Fed Funds Rate | FEDFUNDS |
| CPI (YoY) | CPIAUCSL |
| Unemployment Rate | UNRATE |
| Real GDP Growth | A191RL1Q225SBEA |
| 10Y Treasury | DGS10 |
| 2Y Treasury | DGS2 |
| 10Y-2Y Spread | T10Y2Y |
| VIX | VIXCLS |
| M2 Money Supply | M2SL |
| Retail Sales | RSAFS |
| ISM PMI Proxy | MANEMP |
| Initial Jobless Claims | IC4WSA |

---

## ⚠️ Disclaimer

**PulseScan is for informational and educational purposes only.**
It is NOT financial advice. All analysis is AI-generated and may be incorrect or outdated.
Past signals do not guarantee future results. Always do your own research before making
any investment decisions. The creators of PulseScan are not responsible for any financial
losses incurred from using this tool.
