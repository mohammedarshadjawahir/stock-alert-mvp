import streamlit as st
import yfinance as yf
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send Gmail alert
def send_email_alert(receiver_email, stock_symbol, current_price, target_price):
    sender_email = "your_email@gmail.com"
    app_password = "your_app_password_here"  # Use 16-digit App Password

    subject = f"Stock Alert: {stock_symbol}"
    body = f"""
    Alert! 📈

    Stock {stock_symbol} has reached the target price.

    Current Price: {current_price}
    Target Price: {target_price}

    Check your trading app now!
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        return "✅ Email sent successfully!"
    except Exception as e:
        return f"❌ Error sending email: {e}"

# Streamlit UI
st.title("📊 Stock Price Alert with Email Notification")

stock_symbol = st.text_input("Enter Stock Symbol (e.g. RELIANCE.NS, TCS.NS, INFY.NS)", "RELIANCE.NS")
target_price = st.number_input("Enter Target Price", value=2500.0)
receiver_email = st.text_input("Enter Your Email to Receive Alert")

if st.button("Check Price"):
    stock = yf.Ticker(stock_symbol)
    data = stock.history(period="1d", interval="1m")

    if not data.empty:
        current_price = data["Close"].iloc[-1]
        st.write(f"📌 Current Price of {stock_symbol}: **{current_price:.2f}**")

        if current_price >= target_price:
            st.success(f"🎉 Target reached! Sending email alert...")
            result = send_email_alert(receiver_email, stock_symbol, current_price, target_price)
            st.write(result)
        else:
            st.info(f"Target not yet reached. Current: {current_price:.2f}, Target: {target_price:.2f}")
    else:
        st.error("⚠️ Could not fetch stock data. Check symbol or market hours.")
