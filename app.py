import yfinance as yf
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Gmail Settings ---
EMAIL_ADDRESS = "arshadvoyager@gmail.com"   # replace with your Gmail
EMAIL_PASSWORD = "rukk teym msdw uxuq"     # use App Password (not normal password)
TO_EMAIL = ""      # where to send alerts

def send_email_alert(stock, current_price, change_percent, threshold):
    subject = f"📈 Stock Alert: {stock}"
    body = f"""
    Alert for {stock} 🚨
    Current Price: {current_price:.2f}
    Change: {change_percent:.2f}%
    Threshold: {threshold}%
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return "✅ Email Sent!"
    except Exception as e:
        return f"❌ Error: {e}"


# --- Streamlit UI ---
st.title("📊 Stock Percentage Alert System (India & Global)")

stock_symbol = st.text_input("Enter Stock Symbol (e.g. RELIANCE.BO, TCS.NS, AAPL)", "RELIANCE.BO")
threshold = st.number_input("Alert when % change is greater than", value=2.0, step=0.5)

if st.button("Check Now"):
    stock = yf.Ticker(stock_symbol)
    hist = stock.history(period="1d", interval="1m")

    if not hist.empty:
        current_price = hist["Close"].iloc[-1]
        open_price = hist["Open"].iloc[0]
        change_percent = ((current_price - open_price) / open_price) * 100

        st.write(f"📍 Current Price: {current_price:.2f}")
        st.write(f"📈 Change: {change_percent:.2f}%")

        if abs(change_percent) >= threshold:
            st.success(f"🚨 Alert! {stock_symbol} moved {change_percent:.2f}%")
            result = send_email_alert(stock_symbol, current_price, change_percent, threshold)
            st.write(result)
        else:
            st.info(f"No alert yet. Change is {change_percent:.2f}% (< {threshold}%)")
    else:
        st.error("❌ Could not fetch stock data. Try again later.")
