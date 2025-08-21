# app.py  -- Streamlit Stock Alert MVP
import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="Stock Pop-up Alerts", page_icon="📈", layout="centered")
st.title("📈 Stock Pop-up Alerts — MVP")

# --- Controls
symbol = st.text_input("Ticker (e.g., AAPL, TSLA, INFY.NS)", value="AAPL").upper()
threshold = st.number_input("Alert when move is at least (%)", value=0.5, step=0.1, min_value=0.1)
refresh_sec = st.number_input("Refresh every (sec)", value=5, step=1, min_value=2)

# Initialize session state
if "prev_price" not in st.session_state:
    st.session_state.prev_price = None

# helper to get latest price using yfinance
def get_price(ticker: str):
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="1d", interval="1m")
        if hist is None or hist.empty:
            return None
        return float(hist["Close"].dropna().iloc[-1])
    except Exception as e:
        return None

# show current / previous
latest = get_price(symbol)
prev = st.session_state.prev_price

col1, col2 = st.columns(2)
with col1:
    st.subheader("Current Price")
    st.write(f"{latest:.6f}" if latest else "—")
with col2:
    st.subheader("Previous Price")
    st.write(f"{prev:.6f}" if prev else "—")

# alert logic
if latest is not None and prev is not None and prev > 0:
    pct = (latest - prev) / prev * 100
    if pct >= threshold:
        st.toast(f"✅ {symbol} UP {pct:.2f}% → {latest:.4f}", icon="✅")
    elif pct <= -threshold:
        st.toast(f"⚠️ {symbol} DOWN {pct:.2f}% → {latest:.4f}", icon="⚠️")

# update prev
if latest is not None:
    st.session_state.prev_price = latest

# auto-refresh loop
time.sleep(int(refresh_sec))
st.experimental_rerun()
